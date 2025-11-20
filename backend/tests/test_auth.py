"""
Unit и Integration тесты для модуля авторизации

Тестируемые модули:
- app/utils/telegram.py — валидация Telegram initData
- app/utils/jwt.py — создание и верификация JWT токенов
- app/api/v1/endpoints/auth.py — API endpoints авторизации
"""

import json
import hashlib
import hmac
from datetime import datetime, timedelta
from urllib.parse import urlencode

import pytest

from app.core.config import settings
from app.utils.jwt import JWTTokenError, create_access_token, verify_token
from app.utils.telegram import TelegramInitDataError, validate_telegram_init_data


class TestTelegramValidation:
    """Тесты валидации Telegram initData"""

    @staticmethod
    def _build_init_data(user_data: dict, auth_date: int, bot_token: str) -> str:
        """Создание корректной строки initData с подписью."""
        payload = {
            "auth_date": str(auth_date),
            "user": json.dumps(user_data, separators=(",", ":")),
        }

        data_check_string = "\n".join(
            f"{key}={value}" for key, value in sorted(payload.items())
        )

        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256,
        ).digest()

        hash_value = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256,
        ).hexdigest()

        signed_payload = {**payload, "hash": hash_value}
        return urlencode(signed_payload)

    def test_validate_telegram_init_data_valid(self):
        """Тест успешной валидации правильного initData"""
        user_data = {
            "id": 123456789,
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
        }
        auth_date = int(datetime.utcnow().timestamp())

        init_data = self._build_init_data(user_data, auth_date, settings.TELEGRAM_BOT_TOKEN)

        result = validate_telegram_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)

        assert result is not None
        assert result["telegram_id"] == user_data["id"]
        assert result["first_name"] == user_data["first_name"]
        assert result["auth_date"] == auth_date

    def test_validate_telegram_init_data_invalid_hash(self):
        """Тест с неправильной подписью"""
        user_data = {"id": 123456789, "first_name": "Test"}
        auth_date = int(datetime.utcnow().timestamp())

        # Подделываем hash
        init_data = f"auth_date={auth_date}&user={json.dumps(user_data)}&hash=invalid_hash"

        with pytest.raises(TelegramInitDataError, match="Invalid hash signature"):
            validate_telegram_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)

    def test_validate_telegram_init_data_expired(self):
        """Тест с истёкшим auth_date (старше 24 часов)"""
        user_data = {"id": 123456789, "first_name": "Test"}
        auth_date = int((datetime.utcnow() - timedelta(hours=25)).timestamp())

        init_data = self._build_init_data(user_data, auth_date, settings.TELEGRAM_BOT_TOKEN)

        with pytest.raises(TelegramInitDataError, match="initData is too old"):
            validate_telegram_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)

    def test_validate_telegram_init_data_missing_params(self):
        """Тест с отсутствующими обязательными параметрами"""
        init_data = f"user={json.dumps({'id': 123})}&hash=somehash"

        with pytest.raises(TelegramInitDataError, match="Missing 'auth_date' parameter"):
            validate_telegram_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)


class TestJWT:
    """Тесты JWT токенов"""

    def test_create_access_token_default_expiry(self):
        """Тест создания токена с дефолтным сроком действия"""
        data = {"user_id": 123, "telegram_id": 456789}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_custom_expiry(self):
        """Тест создания токена с кастомным сроком действия"""
        data = {"user_id": 123}
        expires_delta = timedelta(minutes=5)
        token = create_access_token(data, expires_delta)

        assert token is not None
        assert isinstance(token, str)

    def test_verify_token_valid(self):
        """Тест верификации валидного токена"""
        data = {"user_id": 123, "telegram_id": 456789}
        token = create_access_token(data)

        payload = verify_token(token)

        assert payload is not None
        assert payload["user_id"] == 123
        assert payload["telegram_id"] == 456789
        assert "exp" in payload

    def test_verify_token_invalid(self):
        """Тест верификации невалидного токена"""
        invalid_token = "invalid.token.here"

        with pytest.raises(JWTTokenError, match="Invalid token"):
            verify_token(invalid_token)

    def test_verify_token_expired(self):
        """Тест верификации истёкшего токена"""
        data = {"user_id": 123}
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta)

        with pytest.raises(JWTTokenError, match="Invalid token"):
            verify_token(token)


# Integration тесты для API endpoints требуют настройки БД
# Будут добавлены после настройки test database

@pytest.mark.asyncio
class TestAuthAPI:
    """Integration тесты для Auth API endpoints"""

    @pytest.mark.skip(reason="Требует настройку test database")
    async def test_telegram_auth_success(self):
        """Тест успешной авторизации через Telegram"""
        # TODO: Реализовать после настройки test DB
        pass

    @pytest.mark.skip(reason="Требует настройку test database")
    async def test_telegram_auth_invalid_init_data(self):
        """Тест авторизации с невалидным initData"""
        # TODO: Реализовать после настройки test DB
        pass

    @pytest.mark.skip(reason="Требует настройку test database")
    async def test_get_current_user_valid_token(self):
        """Тест получения профиля с валидным токеном"""
        # TODO: Реализовать после настройки test DB
        pass

    @pytest.mark.skip(reason="Требует настройку test database")
    async def test_get_current_user_invalid_token(self):
        """Тест получения профиля с невалидным токеном"""
        # TODO: Реализовать после настройки test DB
        pass
