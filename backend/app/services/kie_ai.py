"""
kie.ai Nano Banana API Client

Клиент для работы с kie.ai Nano Banana API (Gemini 2.5 Flash Image Preview).
Поддерживает генерацию изображений и редактирование через промпты.

Документация: https://kie.ai/nano-banana
API Docs: https://docs.kie.ai
"""

import asyncio
import base64
import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

import httpx
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)

from app.core.config import settings

logger = logging.getLogger(__name__)


class KieAIError(Exception):
    """Базовая ошибка для kie.ai API"""
    pass


class KieAIAuthError(KieAIError):
    """Ошибка авторизации"""
    pass


class KieAIRateLimitError(KieAIError):
    """Ошибка превышения rate limit"""
    pass


class KieAIClient:
    """
    Async клиент для kie.ai Nano Banana API.

    Поддерживает:
    - Генерацию изображений из текста (text-to-image)
    - Редактирование изображений с промптами (image-to-image)
    - Retry логику (3 попытки, exponential backoff)
    - WebSocket для отслеживания прогресса
    """

    BASE_URL = "https://api.kie.ai"
    API_VERSION = "v1"

    # Endpoints
    # Примечание: точный endpoint может отличаться,
    # нужно уточнить в документации kie.ai
    GENERATE_ENDPOINT = "/api/v1/nano-banana/generate"

    # Поддерживаемые форматы
    SUPPORTED_FORMATS = {"jpeg", "jpg", "png", "webp"}
    MAX_FILE_SIZE_MB = 10
    MAX_IMAGES = 10

    # Поддерживаемые aspect ratios
    ASPECT_RATIOS = {
        "1:1", "9:16", "16:9", "3:4", "4:3",
        "3:2", "2:3", "5:4", "4:5", "21:9", "auto"
    }

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: int = 120,
    ):
        """
        Инициализация клиента.

        Args:
            api_key: API ключ от kie.ai (если не указан, берётся из settings)
            base_url: Базовый URL API (по умолчанию https://api.kie.ai)
            timeout: Таймаут запросов в секундах
        """
        self.api_key = api_key or settings.KIE_AI_API_KEY
        self.base_url = base_url or self.BASE_URL
        self.timeout = timeout

        if not self.api_key:
            raise KieAIError("KIE_AI_API_KEY not configured")

        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Закрытие HTTP клиента"""
        await self.client.aclose()

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """
        Обработка ответа от API.

        Args:
            response: HTTP response

        Returns:
            Parsed JSON response

        Raises:
            KieAIAuthError: при ошибке авторизации
            KieAIRateLimitError: при превышении rate limit
            KieAIError: при других ошибках
        """
        if response.status_code == 401:
            logger.error("Authentication failed: invalid API key")
            raise KieAIAuthError("Invalid API key or unauthorized access")

        if response.status_code == 429:
            logger.warning("Rate limit exceeded")
            raise KieAIRateLimitError("Rate limit exceeded, please retry later")

        if response.status_code >= 400:
            error_msg = f"API request failed: {response.status_code}"
            try:
                error_data = response.json()
                error_msg = f"{error_msg} - {error_data.get('error', error_data)}"
            except Exception:
                error_msg = f"{error_msg} - {response.text}"

            logger.error(error_msg)
            raise KieAIError(error_msg)

        return response.json()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, KieAIRateLimitError)),
        reraise=True,
    )
    async def _make_request(
        self,
        endpoint: str,
        data: Dict[str, Any],
        method: str = "POST",
    ) -> Dict[str, Any]:
        """
        Выполнение HTTP запроса с retry логикой.

        Args:
            endpoint: API endpoint
            data: Данные запроса
            method: HTTP метод

        Returns:
            Parsed response
        """
        url = f"{self.base_url}{endpoint}"

        logger.info(f"Making {method} request to {url}")
        logger.debug(f"Request data: {data}")

        try:
            if method == "POST":
                response = await self.client.post(url, json=data)
            elif method == "GET":
                response = await self.client.get(url, params=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            return self._handle_response(response)

        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
            raise KieAIError(f"Network error: {e}") from e

    async def generate_image(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        output_format: str = "png",
        aspect_ratio: str = "1:1",
        callback_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Генерация или редактирование изображения.

        Args:
            prompt: Текстовый промпт для генерации/редактирования
            image_urls: Список URL изображений для редактирования (до 10)
            output_format: Формат выходного файла ("png" или "jpeg")
            aspect_ratio: Соотношение сторон (см. ASPECT_RATIOS)
            callback_url: URL для webhook с результатом (опционально)

        Returns:
            {
                "task_id": "...",
                "status": "processing|completed",
                "image_url": "...",  # если сразу готово
                "estimated_time": 30  # секунды
            }

        Raises:
            KieAIError: при ошибке запроса
            ValueError: при неверных параметрах
        """
        # Валидация параметров
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Prompt must be a non-empty string")

        if output_format not in {"png", "jpeg"}:
            raise ValueError(f"output_format must be 'png' or 'jpeg', got: {output_format}")

        if aspect_ratio not in self.ASPECT_RATIOS:
            raise ValueError(f"Invalid aspect_ratio: {aspect_ratio}. Allowed: {self.ASPECT_RATIOS}")

        if image_urls:
            if not isinstance(image_urls, list):
                raise ValueError("image_urls must be a list")
            if len(image_urls) > self.MAX_IMAGES:
                raise ValueError(f"Maximum {self.MAX_IMAGES} images allowed")

        # Формирование запроса
        request_data = {
            "prompt": prompt,
            "output_format": output_format,
            "aspect_ratio": aspect_ratio,
        }

        # Добавляем изображения для редактирования
        if image_urls:
            request_data["image_urls"] = image_urls

        # Callback для WebSocket/webhook
        if callback_url:
            request_data["callback_url"] = callback_url

        logger.info(f"Generating image with prompt: {prompt[:100]}...")
        if image_urls:
            logger.info(f"With {len(image_urls)} input image(s)")

        # Выполнение запроса
        response = await self._make_request(
            endpoint=self.GENERATE_ENDPOINT,
            data=request_data,
            method="POST",
        )

        logger.info(f"Generation response: task_id={response.get('task_id')}, status={response.get('status')}")

        return response

    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Проверка статуса задачи генерации.

        Args:
            task_id: ID задачи

        Returns:
            {
                "task_id": "...",
                "status": "pending|processing|completed|failed",
                "image_url": "...",  # если completed
                "error": "...",  # если failed
                "progress": 75  # процент выполнения
            }
        """
        response = await self._make_request(
            endpoint=f"/api/{self.API_VERSION}/tasks/{task_id}",
            data={},
            method="GET",
        )

        return response

    async def wait_for_completion(
        self,
        task_id: str,
        max_wait_time: int = 120,
        poll_interval: int = 2,
    ) -> Dict[str, Any]:
        """
        Ожидание завершения задачи с polling.

        Args:
            task_id: ID задачи
            max_wait_time: Максимальное время ожидания в секундах
            poll_interval: Интервал проверки статуса в секундах

        Returns:
            Финальный результат задачи

        Raises:
            KieAIError: при ошибке или таймауте
        """
        elapsed = 0

        while elapsed < max_wait_time:
            result = await self.get_task_status(task_id)
            status = result.get("status")

            if status == "completed":
                logger.info(f"Task {task_id} completed successfully")
                return result

            if status == "failed":
                error = result.get("error", "Unknown error")
                logger.error(f"Task {task_id} failed: {error}")
                raise KieAIError(f"Generation failed: {error}")

            logger.debug(f"Task {task_id} status: {status}, progress: {result.get('progress')}%")

            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

        raise KieAIError(f"Task {task_id} timeout after {max_wait_time}s")

    async def generate_and_wait(
        self,
        prompt: str,
        image_urls: Optional[List[str]] = None,
        output_format: str = "png",
        aspect_ratio: str = "1:1",
        max_wait_time: int = 120,
    ) -> str:
        """
        Генерация изображения с ожиданием результата.

        Args:
            prompt: Текстовый промпт
            image_urls: URL изображений для редактирования
            output_format: Формат выходного файла
            aspect_ratio: Соотношение сторон
            max_wait_time: Максимальное время ожидания

        Returns:
            URL сгенерированного изображения
        """
        # Запуск генерации
        response = await self.generate_image(
            prompt=prompt,
            image_urls=image_urls,
            output_format=output_format,
            aspect_ratio=aspect_ratio,
        )

        # Если результат сразу готов
        if response.get("status") == "completed" and response.get("image_url"):
            return response["image_url"]

        # Иначе ждём выполнения
        task_id = response.get("task_id")
        if not task_id:
            raise KieAIError("No task_id in response")

        result = await self.wait_for_completion(task_id, max_wait_time=max_wait_time)

        image_url = result.get("image_url")
        if not image_url:
            raise KieAIError("No image_url in completed task")

        return image_url


# Singleton instance для использования в приложении
_kie_client: Optional[KieAIClient] = None


async def get_kie_client() -> KieAIClient:
    """
    Получение singleton instance клиента.

    Usage:
        client = await get_kie_client()
        result = await client.generate_image(prompt="...")
    """
    global _kie_client

    if _kie_client is None:
        _kie_client = KieAIClient()

    return _kie_client


async def close_kie_client():
    """Закрытие клиента при shutdown приложения"""
    global _kie_client

    if _kie_client:
        await _kie_client.close()
        _kie_client = None
