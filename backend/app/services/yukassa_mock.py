"""
Mock-реализация ЮKassa клиента для локального тестирования.

ВНИМАНИЕ: Используется только в режиме разработки (PAYMENT_MOCK_MODE=true).
НЕ ИСПОЛЬЗОВАТЬ В PRODUCTION!
"""

import logging
import hmac
import hashlib
from typing import Optional
from decimal import Decimal
from uuid import uuid4
from datetime import datetime

from app.core.config import settings


logger = logging.getLogger(__name__)


class MockYuKassaClient:
    """
    Mock-клиент для эмуляции ЮKassa API.

    Эмулирует:
    - Создание платежей (всегда успешно)
    - Автоматическое подтверждение через 2-3 секунды
    - Webhook callbacks
    - Проверку подписи
    """

    # Хранилище "платежей" в памяти
    _payments = {}

    def __init__(
        self,
        shop_id: str,
        secret_key: str,
        return_url: Optional[str] = None,
    ):
        """
        Инициализация mock-клиента.

        Args:
            shop_id: ID магазина (не используется в mock)
            secret_key: Секретный ключ (используется для подписи)
            return_url: URL для возврата после оплаты
        """
        self.shop_id = shop_id
        self.secret_key = secret_key
        self.return_url = return_url or f"{settings.FRONTEND_URL}/payment/success"

        logger.warning("🔧 MockYuKassaClient initialized - PAYMENT_MOCK_MODE is enabled!")

    async def close(self):
        """Закрытие клиента (заглушка)"""
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def create_payment(
        self,
        amount: Decimal,
        description: str,
        idempotency_key: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """
        Эмуляция создания платежа в ЮKassa.

        Args:
            amount: Сумма платежа в рублях
            description: Описание платежа
            idempotency_key: Ключ идемпотентности (UUID)
            metadata: Метаданные платежа

        Returns:
            dict: Мокированный ответ от "ЮKassa"
        """
        if idempotency_key is None:
            idempotency_key = str(uuid4())

        # Генерация уникального payment_id
        payment_id = str(uuid4())

        # Создание confirmation_url для mock-обработчика
        confirmation_url = f"{settings.FRONTEND_URL}/mock-payment/{payment_id}"

        # Сохраняем "платёж" в памяти
        payment_data = {
            "id": payment_id,
            "status": "pending",
            "amount": {
                "value": f"{amount:.2f}",
                "currency": "RUB",
            },
            "description": description,
            "metadata": metadata or {},
            "confirmation": {
                "type": "redirect",
                "confirmation_url": confirmation_url,
            },
            "created_at": datetime.utcnow().isoformat() + "Z",
            "paid": False,
            "test": True,
        }

        self._payments[payment_id] = payment_data

        logger.info(
            f"🔧 MOCK: Payment created - {payment_id} for {amount} RUB\n"
            f"   Description: {description}\n"
            f"   Confirmation URL: {confirmation_url}"
        )

        return payment_data

    async def get_payment_info(self, payment_id: str) -> dict:
        """
        Получение информации о "платеже".

        Args:
            payment_id: UUID платежа

        Returns:
            dict: Данные платежа

        Raises:
            ValueError: Платёж не найден
        """
        payment = self._payments.get(payment_id)

        if not payment:
            logger.error(f"🔧 MOCK: Payment {payment_id} not found")
            raise ValueError(f"Payment {payment_id} not found")

        logger.info(f"🔧 MOCK: Get payment info - {payment_id}, status={payment['status']}")
        return payment

    def verify_webhook_signature(
        self, payload: str, signature: str
    ) -> bool:
        """
        Проверка подписи webhook (эмуляция).

        В mock-режиме используем тот же алгоритм HMAC SHA-256,
        но принимаем любую подпись как валидную для упрощения тестирования.

        Args:
            payload: Тело запроса (JSON string)
            signature: Значение заголовка X-Yookassa-Signature

        Returns:
            bool: True (всегда валидна в mock)
        """
        try:
            # В mock-режиме всегда возвращаем True для упрощения
            # Но можно включить проверку для тестирования
            if settings.ENVIRONMENT == "development":
                logger.info("🔧 MOCK: Webhook signature check - SKIPPED (mock mode)")
                return True

            # Реальная проверка (если нужно)
            secret_bytes = self.secret_key.encode("utf-8")
            payload_bytes = payload.encode("utf-8")

            expected_signature = hmac.new(
                secret_bytes, payload_bytes, hashlib.sha256
            ).hexdigest()

            return hmac.compare_digest(expected_signature, signature)

        except Exception as e:
            logger.error(f"Error verifying webhook signature: {e}")
            return True  # В mock всегда успешно

    @classmethod
    def get_payment(cls, payment_id: str) -> Optional[dict]:
        """Получить платёж из хранилища"""
        return cls._payments.get(payment_id)

    @classmethod
    def update_payment_status(cls, payment_id: str, status: str, paid: bool = False):
        """
        Обновить статус платежа (для эмулятора).

        Args:
            payment_id: UUID платежа
            status: Новый статус (succeeded, canceled и т.д.)
            paid: Оплачен или нет
        """
        if payment_id in cls._payments:
            cls._payments[payment_id]["status"] = status
            cls._payments[payment_id]["paid"] = paid
            logger.info(f"🔧 MOCK: Payment {payment_id} status updated to {status}")

    @classmethod
    def clear_payments(cls):
        """Очистить хранилище платежей"""
        cls._payments.clear()
        logger.info("🔧 MOCK: All payments cleared")


# Singleton instance для mock
_mock_yukassa_client: Optional[MockYuKassaClient] = None


def get_mock_yukassa_client() -> MockYuKassaClient:
    """
    Получение singleton экземпляра MockYuKassaClient.

    Returns:
        MockYuKassaClient: Mock-клиент ЮKassa
    """
    global _mock_yukassa_client

    if _mock_yukassa_client is None:
        _mock_yukassa_client = MockYuKassaClient(
            shop_id=settings.YUKASSA_SHOP_ID or "mock_shop_id",
            secret_key=settings.YUKASSA_SECRET_KEY or "mock_secret_key",
        )

    return _mock_yukassa_client


async def close_mock_yukassa_client():
    """Закрытие mock-клиента"""
    global _mock_yukassa_client

    if _mock_yukassa_client is not None:
        await _mock_yukassa_client.close()
        _mock_yukassa_client = None
