"""
Celery задачи для генерации редактирования изображений.
"""

import asyncio
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
from app.models.chat import ChatHistory
from app.services.file_storage import save_upload_file_by_content
from app.services.kie_ai import KieAIClient
from app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)


async def _update_generation_status(
    session: AsyncSession,
    generation_id: int,
    status: str,
    progress: Optional[int] = None,
    image_url: Optional[str] = None,
    error_message: Optional[str] = None,
):
    """
    Обновление статуса генерации в БД.

    Args:
        session: Async DB session
        generation_id: ID генерации
        status: Новый статус (processing, completed, failed)
        progress: Прогресс (0-100)
        image_url: URL результата (для completed)
        error_message: Сообщение об ошибке (для failed)
    """
    generation = await session.get(Generation, generation_id)
    if not generation:
        logger.error(f"Generation {generation_id} not found")
        return

    generation.status = status

    if progress is not None:
        generation.progress = progress

    if image_url:
        generation.image_url = image_url

    if error_message:
        generation.error_message = error_message

    await session.commit()
    logger.info(
        f"Updated generation {generation_id}: status={status}, progress={progress}"
    )


def _should_add_watermark(user: User) -> bool:
    """
    Проверка, нужен ли водяной знак.

    Args:
        user: User модель

    Returns:
        True, если нужен водяной знак (Freemium пользователь)
    """
    # Если у пользователя нет кредитов и нет активной подписки
    # и он использует Freemium — добавляем водяной знак
    has_credits = user.balance_credits > 0
    has_subscription = user.has_active_subscription

    return not has_credits and not has_subscription


class EditingTask(Task):
    """
    Базовый класс для задач редактирования с поддержкой прогресса.
    """

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Обработка ошибок задачи"""
        logger.error(
            f"Editing task {task_id} failed: {exc}",
            exc_info=einfo
        )

    def on_success(self, retval, task_id, args, kwargs):
        """Обработка успешного выполнения"""
        logger.info(f"Editing task {task_id} completed successfully")


@celery_app.task(
    bind=True,
    base=EditingTask,
    max_retries=3,
    default_retry_delay=60,  # 1 минута между попытками
    name="app.tasks.editing.generate_editing_task"
)
def generate_editing_task(
    self,
    generation_id: int,
    user_id: int,
    session_id: str,
    base_image_url: str,
    prompt: str,
) -> dict:
    """
    Celery задача для генерации редактирования изображения.

    Args:
        self: Celery task instance
        generation_id: ID записи Generation в БД
        user_id: ID пользователя
        session_id: UUID сессии чата
        base_image_url: URL базового изображения
        prompt: Промпт для редактирования

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

                # Обновление прогресса
                await _update_generation_status(
                    session,
                    generation_id,
                    "processing",
                    progress=30
                )

                # Вызов kie.ai API для редактирования изображения
                kie_client = KieAIClient(
                    api_key=settings.KIE_AI_API_KEY,
                    base_url=settings.KIE_AI_BASE_URL
                )

                logger.info(
                    f"Starting image editing for generation {generation_id}, "
                    f"prompt: {prompt[:100]}..."
                )

                # Обновление прогресса
                await _update_generation_status(
                    session,
                    generation_id,
                    "processing",
                    progress=50
                )

                # Генерация через kie.ai API (image editing)
                # Примечание: Реальный API endpoint может отличаться
                # Здесь используется упрощённая логика для демонстрации
                try:
                    result = await kie_client.edit_image(
                        base_image_url=base_image_url,
                        prompt=prompt,
                        add_watermark=has_watermark,
                        watermark_text=settings.FREEMIUM_WATERMARK_TEXT if has_watermark else None,
                    )

                    image_data = result.get("image_data")
                    if not image_data:
                        raise ValueError("No image data in kie.ai response")

                    # Обновление прогресса
                    await _update_generation_status(
                        session,
                        generation_id,
                        "processing",
                        progress=80
                    )

                    # Сохранение результата
                    file_id, image_url, file_size = await save_upload_file_by_content(
                        file_content=image_data,
                        user_id=user_id,
                        filename=f"editing_{generation_id}.png",
                    )

                    logger.info(
                        f"Saved edited image: {image_url} "
                        f"(size: {file_size} bytes, watermark: {has_watermark})"
                    )

                    # Обновление Generation с результатом
                    await _update_generation_status(
                        session,
                        generation_id,
                        "completed",
                        progress=100,
                        image_url=image_url,
                    )

                    # Добавление результата в историю чата
                    chat_history = await session.execute(
                        select(ChatHistory).where(
                            ChatHistory.session_id == session_id,
                            ChatHistory.user_id == user_id,
                        )
                    )
                    chat = chat_history.scalar_one_or_none()

                    if chat:
                        chat.add_message(
                            role="assistant",
                            content=f"Image edited successfully with prompt: {prompt}",
                            image_url=image_url,
                        )
                        await session.commit()
                        logger.info(f"Added result to chat history {session_id}")

                    return {
                        "status": "completed",
                        "image_url": image_url,
                        "has_watermark": has_watermark,
                        "generation_id": generation_id,
                    }

                except Exception as api_error:
                    logger.error(f"kie.ai API error: {api_error}")
                    raise

            except Exception as e:
                logger.error(
                    f"Error in editing generation {generation_id}: {e}",
                    exc_info=True
                )

                # Обновление статуса: failed
                await _update_generation_status(
                    session,
                    generation_id,
                    "failed",
                    error_message=str(e),
                )

                # Попытка retry
                try:
                    raise self.retry(exc=e, countdown=60)
                except self.MaxRetriesExceededError:
                    logger.error(
                        f"Max retries exceeded for generation {generation_id}"
                    )
                    return {
                        "status": "failed",
                        "error": str(e),
                        "generation_id": generation_id,
                    }

    # Запуск async функции
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(_run_generation())
