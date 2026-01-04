"""
Integration тесты для Auth API endpoints

Требует запущенную test database.
Запуск: pytest tests/test_auth_integration.py -v

Перед запуском:
1. Создайте test database: ./tests/create_test_db.sh
2. Убедитесь, что PostgreSQL запущен
"""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.utils.jwt import verify_token


@pytest.mark.asyncio
@pytest.mark.integration
class TestAuthIntegration:
    """Integration тесты для Auth API"""

    async def test_get_current_user_with_valid_token(
        self,
        authenticated_test_client: AsyncClient,
        test_user_with_credits: User,
    ):
        """
        GET /api/v1/auth/me с валидным токеном должен вернуть профиль пользователя
        """
        response = await authenticated_test_client.get("/api/v1/auth/me")

        assert response.status_code == 200

        data = response.json()
        assert data["telegram_id"] == test_user_with_credits.telegram_id
        assert data["username"] == test_user_with_credits.username
        assert data["balance_credits"] == test_user_with_credits.balance_credits
        assert data["subscription_type"] == test_user_with_credits.subscription_type.value

    async def test_get_current_user_without_token(self, test_client: AsyncClient):
        """
        GET /api/v1/auth/me без токена должен вернуть 401 Unauthorized
        """
        response = await test_client.get("/api/v1/auth/me")

        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    async def test_get_current_user_with_invalid_token(self, test_client: AsyncClient):
        """
        GET /api/v1/auth/me с невалидным токеном должен вернуть 401
        """
        test_client.headers["Authorization"] = "Bearer invalid.token.here"

        response = await test_client.get("/api/v1/auth/me")

        assert response.status_code == 401

    async def test_get_current_user_with_expired_token(self, test_client: AsyncClient):
        """
        GET /api/v1/auth/me с истёкшим токеном должен вернуть 401
        """
        from app.utils.jwt import create_access_token
        from datetime import timedelta

        # Создаём токен, который уже истёк
        expired_token = create_access_token(
            data={"user_id": 999, "telegram_id": 999},
            expires_delta=timedelta(seconds=-1)
        )

        test_client.headers["Authorization"] = f"Bearer {expired_token}"

        response = await test_client.get("/api/v1/auth/me")

        assert response.status_code == 401


@pytest.mark.asyncio
@pytest.mark.integration
class TestUserCreationAndRetrieval:
    """Тесты создания и получения пользователей через API"""

    async def test_user_profile_reflects_database_state(
        self,
        authenticated_test_client: AsyncClient,
        test_user_with_credits: User,
        test_db: AsyncSession,
    ):
        """
        Профиль пользователя должен отражать текущее состояние в БД
        """
        # Получаем профиль через API
        response = await authenticated_test_client.get("/api/v1/auth/me")
        assert response.status_code == 200

        profile_data = response.json()

        # Проверяем, что данные соответствуют БД
        assert profile_data["id"] == test_user_with_credits.id
        assert profile_data["telegram_id"] == test_user_with_credits.telegram_id
        assert profile_data["balance_credits"] == test_user_with_credits.balance_credits

        # Обновляем баланс в БД напрямую
        test_user_with_credits.balance_credits = 100
        await test_db.commit()
        await test_db.refresh(test_user_with_credits)

        # Получаем профиль снова
        response = await authenticated_test_client.get("/api/v1/auth/me")
        assert response.status_code == 200

        updated_profile = response.json()

        # Баланс должен обновиться
        assert updated_profile["balance_credits"] == 100

    async def test_user_has_correct_subscription_info(
        self,
        test_client: AsyncClient,
        test_user_premium: User,
    ):
        """
        Пользователь с подпиской должен видеть корректную информацию о подписке
        """
        from app.utils.jwt import create_access_token

        # Создаём токен для premium пользователя
        token = create_access_token(
            data={
                "user_id": test_user_premium.id,
                "telegram_id": test_user_premium.telegram_id
            }
        )

        test_client.headers["Authorization"] = f"Bearer {token}"

        response = await test_client.get("/api/v1/auth/me")

        assert response.status_code == 200

        data = response.json()

        # Проверяем информацию о подписке
        assert data["subscription_type"] == "premium"
        assert data["subscription_ops_remaining"] == 150
        assert "subscription_expires_at" in data
        assert data["subscription_expires_at"] is not None

    async def test_freemium_user_info(
        self,
        test_client: AsyncClient,
        test_user_freemium_only: User,
    ):
        """
        Freemium пользователь должен видеть корректную информацию о Freemium
        """
        from app.utils.jwt import create_access_token

        token = create_access_token(
            data={
                "user_id": test_user_freemium_only.id,
                "telegram_id": test_user_freemium_only.telegram_id
            }
        )

        test_client.headers["Authorization"] = f"Bearer {token}"

        response = await test_client.get("/api/v1/auth/me")

        assert response.status_code == 200

        data = response.json()

        # Проверяем Freemium информацию
        assert data["balance_credits"] == 0
        assert data["subscription_type"] is None
        assert data["freemium_actions_used"] == 5
        # Осталось 5 из 10 Freemium действий
        # (Если в API есть поле freemium_actions_left)


@pytest.mark.asyncio
@pytest.mark.integration
class TestJWTTokenValidation:
    """Тесты валидации JWT токенов"""

    async def test_jwt_token_contains_correct_claims(
        self,
        test_user_with_credits: User,
    ):
        """
        JWT токен должен содержать правильные claims
        """
        from app.utils.jwt import create_access_token, verify_token

        # Создаём токен
        token = create_access_token(
            data={
                "user_id": test_user_with_credits.id,
                "telegram_id": test_user_with_credits.telegram_id
            }
        )

        # Верифицируем токен
        payload = verify_token(token)

        assert payload is not None
        assert payload["user_id"] == test_user_with_credits.id
        assert payload["telegram_id"] == test_user_with_credits.telegram_id
        assert "exp" in payload  # expiration claim

    async def test_token_works_across_multiple_requests(
        self,
        authenticated_test_client: AsyncClient,
    ):
        """
        Один и тот же токен должен работать для нескольких запросов
        """
        # Первый запрос
        response1 = await authenticated_test_client.get("/api/v1/auth/me")
        assert response1.status_code == 200

        # Второй запрос с тем же токеном
        response2 = await authenticated_test_client.get("/api/v1/auth/me")
        assert response2.status_code == 200

        # Данные должны быть одинаковыми
        assert response1.json()["id"] == response2.json()["id"]


@pytest.mark.asyncio
@pytest.mark.integration
@pytest.mark.skip(reason="Требует реализацию POST /api/v1/auth/telegram endpoint")
class TestTelegramAuth:
    """
    Тесты авторизации через Telegram initData

    ПРИМЕЧАНИЕ: Эти тесты требуют полную реализацию endpoint'а
    POST /api/v1/auth/telegram с правильной валидацией HMAC SHA-256
    """

    async def test_telegram_auth_creates_new_user(
        self,
        test_client: AsyncClient,
        test_db: AsyncSession,
    ):
        """
        Авторизация через Telegram должна создать нового пользователя
        """
        # TODO: Реализовать после создания валидного Telegram initData
        pass

    async def test_telegram_auth_returns_jwt_token(
        self,
        test_client: AsyncClient,
    ):
        """
        Авторизация через Telegram должна вернуть JWT токен
        """
        # TODO: Реализовать
        pass

    async def test_telegram_auth_updates_existing_user(
        self,
        test_client: AsyncClient,
        test_user_with_credits: User,
    ):
        """
        Авторизация существующего пользователя должна обновить его данные
        """
        # TODO: Реализовать
        pass


# ==================== Вспомогательные функции ====================

def assert_user_profile_structure(profile_data: dict):
    """
    Проверяет, что структура профиля пользователя корректна
    """
    required_fields = [
        "id",
        "telegram_id",
        "username",
        "first_name",
        "balance_credits",
        "subscription_type",
        "freemium_actions_used",
        "created_at",
    ]

    for field in required_fields:
        assert field in profile_data, f"Missing field: {field}"

    # Проверка типов
    assert isinstance(profile_data["id"], int)
    assert isinstance(profile_data["telegram_id"], int)
    assert isinstance(profile_data["balance_credits"], int)
    assert profile_data["balance_credits"] >= 0


# Используем эту функцию в тестах для валидации структуры ответа
@pytest.mark.asyncio
@pytest.mark.integration
class TestResponseStructure:
    """Тесты структуры ответов API"""

    async def test_user_profile_has_correct_structure(
        self,
        authenticated_test_client: AsyncClient,
    ):
        """
        Профиль пользователя должен иметь правильную структуру
        """
        response = await authenticated_test_client.get("/api/v1/auth/me")

        assert response.status_code == 200

        profile_data = response.json()

        # Используем вспомогательную функцию для проверки
        assert_user_profile_structure(profile_data)
