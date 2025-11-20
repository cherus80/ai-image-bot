"""
Celery задачи для генерации примерки одежды/аксессуаров.
"""

import asyncio
import base64
import logging
from datetime import datetime
from typing import Optional

from celery import Task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import async_session
from app.models.generation import Generation
from app.models.user import User
from app.services.file_storage import save_upload_file_by_content, get_file_by_id
from app.services.kie_ai import KieAIClient
from app.services.openrouter import OpenRouterClient, OpenRouterError
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


# Фиксированные промпты для примерки
FITTING_PROMPTS = {
    "clothing": (
        "A high-quality fashion photoshoot showing a person wearing the clothing item. "
        "Professional studio lighting, clean background, realistic fit and draping. "
        "Photorealistic, 8k, detailed fabric texture."
    ),
    "accessory_head": (
        "A professional portrait showing a person wearing the accessory on their head. "
        "Clear focus on the accessory, natural lighting, realistic placement. "
        "High detail, photorealistic, 8k quality."
    ),
    "accessory_face": (
        "A professional close-up portrait showing a person wearing the accessory on their face. "
        "Clear focus on glasses/mask, natural lighting, realistic fit and placement. "
        "High detail, photorealistic, 8k quality."
    ),
    "accessory_neck": (
        "A fashion portrait focusing on the neck area with the accessory. "
        "Professional lighting, elegant pose, realistic jewelry placement. "
        "Photorealistic, high detail, 8k quality."
    ),
    "accessory_hands": (
        "A close-up shot of hands wearing the accessory. "
        "Professional lighting, natural hand position, realistic fit. "
        "High detail, photorealistic, 8k quality."
    ),
    "accessory_legs": (
        "A fashion shot showing legs wearing the accessory. "
        "Professional lighting, natural pose, realistic placement. "
        "Photorealistic, high detail, 8k quality."
    ),
    "accessory_body": (
        "A full-body fashion photoshoot showing a person wearing the clothing item. "
        "Professional studio lighting, clean background, realistic fit and draping. "
        "Photorealistic, 8k, detailed fabric texture, full body view."
    ),
}


def _get_prompt_for_zone(zone: Optional[str]) -> str:
    """
    Получить промпт в зависимости от зоны аксессуара.

    Args:
        zone: Зона аксессуара (head, face, neck, hands, legs, body) или None для одежды

    Returns:
        str: Промпт для генерации
    """
    if not zone:
        return FITTING_PROMPTS["clothing"]

    zone_key = f"accessory_{zone.lower()}"
    return FITTING_PROMPTS.get(zone_key, FITTING_PROMPTS["clothing"])


def _image_to_base64_data_url(file_path) -> str:
    """
    Преобразовать локальное изображение в base64 data URL.

    Args:
        file_path: Путь к файлу изображения (str или Path)

    Returns:
        str: Base64-encoded data URL (data:image/jpeg;base64,...)
    """
    # Конвертируем Path в строку если нужно
    file_path_str = str(file_path)

    with open(file_path_str, "rb") as f:
        image_data = f.read()

    # Определяем MIME type по расширению
    if file_path_str.lower().endswith(".png"):
        mime_type = "image/png"
    elif file_path_str.lower().endswith((".jpg", ".jpeg")):
        mime_type = "image/jpeg"
    elif file_path_str.lower().endswith(".webp"):
        mime_type = "image/webp"
    else:
        mime_type = "image/jpeg"  # Default

    base64_data = base64.b64encode(image_data).decode("utf-8")
    return f"data:{mime_type};base64,{base64_data}"


class FittingTask(Task):
    """
    Базовый класс для задач генерации с поддержкой прогресса.
    """

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Обработка ошибок задачи"""
        # Здесь можно добавить логику отправки уведомлений об ошибке
        pass

    def on_success(self, retval, task_id, args, kwargs):
        """Обработка успешного выполнения"""
        # Здесь можно добавить логику отправки уведомлений об успехе
        pass


@celery_app.task(
    bind=True,
    base=FittingTask,
    max_retries=3,
    default_retry_delay=60,  # 1 минута между попытками
    name="app.tasks.fitting.generate_fitting_task"
)
def generate_fitting_task(
    self,
    generation_id: int,
    user_id: int,
    user_photo_url: str,
    item_photo_url: str,
    accessory_zone: Optional[str] = None,
    credits_cost: int = 2  # Стоимость в кредитах (передаётся из endpoint)
) -> dict:
    """
    Celery задача для генерации примерки.

    Args:
        self: Celery task instance
        generation_id: ID записи Generation в БД
        user_id: ID пользователя
        user_photo_url: URL фото пользователя
        item_photo_url: URL фото одежды/аксессуара
        accessory_zone: Зона аксессуара (опционально)

    Returns:
        dict: Результат генерации
    """

    async def _run_generation():
        """Async функция для выполнения генерации"""
        async with async_session() as session:
            try:
                # Обновление статуса: processing
                await _update_generation_status(
                    session,
                    generation_id,
                    "processing",
                    progress=10
                )

                # Получение информации о пользователе
                user = await session.get(User, user_id)
                if not user:
                    raise ValueError(f"User {user_id} not found")

                # Определение, нужен ли водяной знак
                has_watermark = _should_add_watermark(user)

                # Получение промпта
                prompt = _get_prompt_for_zone(accessory_zone)

                # Обновление прогресса
                await _update_generation_status(
                    session,
                    generation_id,
                    "processing",
                    progress=30
                )

                # Получение путей к файлам
                user_photo_id = user_photo_url.split("/")[-1].split(".")[0]
                item_photo_id = item_photo_url.split("/")[-1].split(".")[0]

                user_photo_path = get_file_by_id(user_photo_id)
                item_photo_path = get_file_by_id(item_photo_id)

                if not user_photo_path or not item_photo_path:
                    raise ValueError("Photo files not found")

                # Обновление прогресса
                await _update_generation_status(
                    session,
                    generation_id,
                    "processing",
                    progress=50
                )

                # Генерация изображения с виртуальной примеркой
                # Пытаемся использовать kie.ai, при ошибке fallback на OpenRouter
                generated_image_url = None
                used_fallback = False

                # ===== Попытка 1: kie.ai API =====
                try:
                    kie_client = KieAIClient(
                        api_key=settings.KIE_AI_API_KEY,
                        base_url=settings.KIE_AI_BASE_URL
                    )

                    # Формируем полные URL для доступа к файлам
                    user_photo_full_url = f"{settings.BACKEND_URL}{user_photo_url}"
                    item_photo_full_url = f"{settings.BACKEND_URL}{item_photo_url}"
                    image_urls = [user_photo_full_url, item_photo_full_url]

                    result = await kie_client.generate_image(
                        prompt=prompt,
                        image_urls=image_urls,  # ← Передаём изображения для virtual try-on
                        output_format="png",
                        aspect_ratio="1:1",
                    )

                    # Получение URL сгенерированного изображения
                    # Если результат сразу готов - берём image_url
                    if result.get("status") == "completed" and result.get("image_url"):
                        generated_image_url = result["image_url"]
                    else:
                        # Иначе ждём выполнения задачи через task_id
                        task_id = result.get("task_id")
                        if not task_id:
                            raise ValueError("No task_id or image_url in kie.ai response")

                        # Ждём завершения задачи с периодическим обновлением статуса в БД
                        max_wait_time = 120  # 2 минуты максимум
                        poll_interval = 2
                        elapsed = 0

                        while elapsed < max_wait_time:
                            # Получаем статус от kie.ai
                            kie_status = await kie_client.get_task_status(task_id)
                            kie_status_value = kie_status.get("status")

                            # Обновляем прогресс в БД для frontend polling
                            kie_progress = kie_status.get("progress", 50)
                            await _update_generation_status(
                                session,
                                generation_id,
                                "processing",
                                progress=max(50, min(95, kie_progress))  # Между 50% и 95%
                            )

                            if kie_status_value == "completed":
                                generated_image_url = kie_status.get("image_url")
                                if not generated_image_url:
                                    raise ValueError("No image_url in completed kie.ai task")
                                break

                            if kie_status_value == "failed":
                                error = kie_status.get("error", "Unknown error")
                                raise ValueError(f"kie.ai generation failed: {error}")

                            await asyncio.sleep(poll_interval)
                            elapsed += poll_interval

                        if elapsed >= max_wait_time:
                            raise ValueError(f"kie.ai generation timeout after {max_wait_time}s")

                    logger.info(f"kie.ai virtual try-on successful")

                except Exception as kie_error:
                    # ===== Fallback: OpenRouter Nano Banana =====
                    logger.warning(f"kie.ai failed: {kie_error}. Trying fallback: OpenRouter Nano Banana")

                    try:
                        # Конвертируем изображения в base64 data URLs
                        user_photo_base64 = _image_to_base64_data_url(user_photo_path)
                        item_photo_base64 = _image_to_base64_data_url(item_photo_path)

                        # Создаём OpenRouter клиент
                        openrouter_client = OpenRouterClient()

                        # Обновляем прогресс
                        await _update_generation_status(
                            session,
                            generation_id,
                            "processing",
                            progress=60
                        )

                        # Генерируем через Nano Banana
                        generated_image_url = await openrouter_client.generate_virtual_tryon(
                            user_photo_data=user_photo_base64,
                            item_photo_data=item_photo_base64,
                            prompt=prompt,
                            aspect_ratio="1:1",
                        )

                        # Закрываем клиент
                        await openrouter_client.close()

                        used_fallback = True
                        logger.info(f"OpenRouter Nano Banana virtual try-on successful (fallback)")

                    except OpenRouterError as or_error:
                        logger.error(f"OpenRouter fallback also failed: {or_error}")
                        raise ValueError(f"Both kie.ai and OpenRouter failed. kie.ai: {kie_error}, OpenRouter: {or_error}")

                # Обновление прогресса
                await _update_generation_status(
                    session,
                    generation_id,
                    "processing",
                    progress=80
                )

                # TODO: Скачать изображение и сохранить локально
                # TODO: Добавить водяной знак если has_watermark=True

                # Если использовали OpenRouter fallback, нужно сохранить base64 изображение локально
                final_image_url = generated_image_url
                if used_fallback and generated_image_url.startswith("data:image"):
                    # Извлекаем base64 данные из data URL
                    import re
                    match = re.match(r'data:image/(\w+);base64,(.+)', generated_image_url)
                    if match:
                        image_format = match.group(1)  # png, jpeg, etc.
                        base64_data = match.group(2)

                        # Декодируем base64
                        image_bytes = base64.b64decode(base64_data)

                        # Сохраняем файл через file_storage
                        from io import BytesIO
                        from app.services.file_storage import save_upload_file_by_content

                        saved_file_id, saved_file_url, _ = await save_upload_file_by_content(
                            content=image_bytes,
                            filename=f"tryon_result_{generation_id}.{image_format}",
                            user_id=user_id,
                        )

                        final_image_url = saved_file_url
                        logger.info(f"Saved OpenRouter result to local storage: {saved_file_url}")

                # Обновление Generation в БД
                generation = await session.get(Generation, generation_id)
                if generation:
                    generation.status = "completed"
                    generation.image_url = final_image_url
                    generation.has_watermark = has_watermark
                    generation.prompt = prompt
                    generation.credits_spent = credits_cost  # Устанавливаем стоимость ПОСЛЕ успеха
                    await session.commit()

                    # СПИСЫВАЕМ КРЕДИТЫ ТОЛЬКО ПОСЛЕ УСПЕШНОЙ ГЕНЕРАЦИИ
                    user = await session.get(User, user_id)
                    if user:
                        from app.services.credits import deduct_credits
                        await deduct_credits(session, user, credits_cost, generation_id=generation_id)
                        logger.info(f"Credits deducted after successful generation: {credits_cost}")

                # Обновление прогресса
                await _update_generation_status(
                    session,
                    generation_id,
                    "completed",
                    progress=100
                )

                return {
                    "status": "completed",
                    "image_url": final_image_url,  # Возвращаем final_image_url (исправление 3C)
                    "has_watermark": has_watermark,
                }

            except Exception as e:
                # Обработка ошибки
                await _update_generation_status(
                    session,
                    generation_id,
                    "failed",
                    error_message=str(e)
                )

                # Retry при определенных ошибках
                if "API" in str(e) or "timeout" in str(e).lower():
                    raise self.retry(exc=e)

                raise

    # Запуск async функции
    return asyncio.run(_run_generation())


async def _update_generation_status(
    session: AsyncSession,
    generation_id: int,
    status: str,
    progress: Optional[int] = None,
    error_message: Optional[str] = None
):
    """
    Обновить статус генерации в БД.

    Args:
        session: SQLAlchemy async session
        generation_id: ID генерации
        status: Новый статус
        progress: Прогресс в процентах (опционально)
        error_message: Сообщение об ошибке (опционально)
    """
    generation = await session.get(Generation, generation_id)

    if generation:
        generation.status = status

        if progress is not None:
            generation.progress = progress

        if error_message:
            generation.error_message = error_message

        await session.commit()

    # TODO: Отправить обновление через WebSocket/Redis для real-time уведомлений


def _should_add_watermark(user: User) -> bool:
    """
    Определить, нужно ли добавлять водяной знак.

    Args:
        user: Объект пользователя

    Returns:
        bool: True если нужен водяной знак
    """
    # Водяной знак для Freemium пользователей
    if user.balance_credits > 0:
        return False

    if user.subscription_type and user.subscription_end:
        if user.subscription_end > datetime.utcnow():
            return False

    # Freemium пользователи получают водяной знак
    return True
