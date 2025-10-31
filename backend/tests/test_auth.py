"""
Unit и Integration тесты для модуля авторизации

Тестируемые модули:
- app/utils/telegram.py — валидация Telegram initData
- app/utils/jwt.py — создание и верификация JWT токенов
- app/api/v1/endpoints/auth.py — API endpoints авторизации
"""

import pytest
from datetime import datetime, timedelta
import hmac
import hashlib
from urllib.parse import urlencode

from app.utils.telegram import validate_telegram_init_data
from app.utils.jwt import create_access_token, verify_token
from app.core.config import settings


class TestTelegramValidation:
    """Тесты валидации Telegram initData"""

    def test_validate_telegram_init_data_valid(self):
        """Тест успешной валидации правильного initData"""
        # Подготовка тестовых данных
        user_data = {
            "id": 123456789,
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
        }
        auth_date = int(datetime.utcnow().timestamp())

        # Формирование data_check_string
        data_parts = [
            f"auth_date={auth_date}",
            f"user={str(user_data)}",
        ]
        data_check_string = "\n".join(sorted(data_parts))

        # Создание подписи
        secret_key = hmac.new(
            "WebAppData".encode(),
            settings.TELEGRAM_BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()
        hash_value = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        # Формирование init_data
        init_data = f"auth_date={auth_date}&user={str(user_data)}&hash={hash_value}"

        # Валидация
        result = validate_telegram_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)

        assert result is not None
        assert "user" in result
        assert result["auth_date"] == str(auth_date)

    def test_validate_telegram_init_data_invalid_hash(self):
        """Тест с неправильной подписью"""
        user_data = {"id": 123456789, "first_name": "Test"}
        auth_date = int(datetime.utcnow().timestamp())

        init_data = f"auth_date={auth_date}&user={str(user_data)}&hash=invalid_hash"

        with pytest.raises(ValueError, match="Invalid hash"):
            validate_telegram_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)

    def test_validate_telegram_init_data_expired(self):
        """Тест с истёкшим auth_date (старше 24 часов)"""
        user_data = {"id": 123456789, "first_name": "Test"}
        # auth_date 25 часов назад
        auth_date = int((datetime.utcnow() - timedelta(hours=25)).timestamp())

        # Создание правильной подписи для старого auth_date
        data_parts = [
            f"auth_date={auth_date}",
            f"user={str(user_data)}",
        ]
        data_check_string = "\n".join(sorted(data_parts))

        secret_key = hmac.new(
            "WebAppData".encode(),
            settings.TELEGRAM_BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()
        hash_value = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        init_data = f"auth_date={auth_date}&user={str(user_data)}&hash={hash_value}"

        with pytest.raises(ValueError, match="auth_date is too old"):
            validate_telegram_init_data(init_data, settings.TELEGRAM_BOT_TOKEN)

    def test_validate_telegram_init_data_missing_params(self):
        """Тест с отсутствующими обязательными параметрами"""
        # Нет auth_date
        init_data = "user={\"id\": 123}&hash=somehash"

        with pytest.raises(ValueError, match="Missing required parameters"):
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

        payload = verify_token(invalid_token)

        assert payload is None

    def test_verify_token_expired(self):
        """Тест верификации истёкшего токена"""
        data = {"user_id": 123}
        # Создаём токен, который истёк 1 секунду назад
        expires_delta = timedelta(seconds=-1)
        token = create_access_token(data, expires_delta)

        payload = verify_token(token)

        assert payload is None


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
