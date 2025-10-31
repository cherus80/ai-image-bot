"""
Unit тесты для модуля управления кредитами

Тестируемый модуль:
- app/services/credits.py — проверка, списание, начисление кредитов
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch

from app.services.credits import (
    check_user_can_perform_action,
    deduct_credits,
    award_credits,
    award_subscription,
)
from app.models.user import User, SubscriptionType


class TestCheckUserCanPerformAction:
    """Тесты проверки возможности выполнения действия"""

    def test_user_with_credits(self):
        """Пользователь с достаточным количеством кредитов"""
        user = Mock(spec=User)
        user.balance_credits = 10
        user.subscription_type = SubscriptionType.NONE
        user.subscription_actions_left = 0
        user.freemium_actions_used = 10
        user.freemium_reset_date = datetime.utcnow()

        result = check_user_can_perform_action(user, cost=5)

        assert result["can_perform"] is True
        assert result["method"] == "credits"
        assert result["remaining_credits"] == 10

    def test_user_with_insufficient_credits(self):
        """Пользователь с недостаточным количеством кредитов"""
        user = Mock(spec=User)
        user.balance_credits = 2
        user.subscription_type = SubscriptionType.NONE
        user.subscription_actions_left = 0
        user.freemium_actions_used = 10
        user.freemium_reset_date = datetime.utcnow()

        result = check_user_can_perform_action(user, cost=5)

        assert result["can_perform"] is False
        assert result["method"] == "none"
        assert result["error"] == "Insufficient credits"

    def test_user_with_active_subscription(self):
        """Пользователь с активной подпиской"""
        user = Mock(spec=User)
        user.balance_credits = 0
        user.subscription_type = SubscriptionType.BASIC
        user.subscription_actions_left = 30
        user.subscription_end_date = datetime.utcnow() + timedelta(days=15)
        user.freemium_actions_used = 10
        user.freemium_reset_date = datetime.utcnow()

        result = check_user_can_perform_action(user, cost=1)

        assert result["can_perform"] is True
        assert result["method"] == "subscription"
        assert result["subscription_type"] == SubscriptionType.BASIC
        assert result["actions_left"] == 30

    def test_user_with_expired_subscription(self):
        """Пользователь с истёкшей подпиской"""
        user = Mock(spec=User)
        user.balance_credits = 0
        user.subscription_type = SubscriptionType.BASIC
        user.subscription_actions_left = 30
        user.subscription_end_date = datetime.utcnow() - timedelta(days=1)
        user.freemium_actions_used = 10
        user.freemium_reset_date = datetime.utcnow()

        result = check_user_can_perform_action(user, cost=1)

        assert result["can_perform"] is False
        assert result["method"] == "none"

    def test_user_with_freemium_available(self):
        """Пользователь может использовать Freemium"""
        user = Mock(spec=User)
        user.balance_credits = 0
        user.subscription_type = SubscriptionType.NONE
        user.subscription_actions_left = 0
        user.freemium_actions_used = 5
        user.freemium_reset_date = datetime.utcnow()

        result = check_user_can_perform_action(user, cost=1)

        assert result["can_perform"] is True
        assert result["method"] == "freemium"
        assert result["freemium_left"] == 5  # 10 - 5 = 5
        assert result["watermark"] is True

    def test_user_with_freemium_exhausted(self):
        """Пользователь исчерпал Freemium лимит"""
        user = Mock(spec=User)
        user.balance_credits = 0
        user.subscription_type = SubscriptionType.NONE
        user.subscription_actions_left = 0
        user.freemium_actions_used = 10
        user.freemium_reset_date = datetime.utcnow()

        result = check_user_can_perform_action(user, cost=1)

        assert result["can_perform"] is False
        assert result["method"] == "none"
        assert result["error"] == "Freemium limit reached"


@pytest.mark.asyncio
class TestDeductCredits:
    """Тесты списания кредитов"""

    async def test_deduct_from_balance_credits(self):
        """Списание с баланса кредитов"""
        user = Mock(spec=User)
        user.balance_credits = 10
        user.subscription_type = SubscriptionType.NONE
        user.subscription_actions_left = 0
        user.freemium_actions_used = 0

        db_mock = AsyncMock()

        result = await deduct_credits(db_mock, user, cost=3)

        assert result["success"] is True
        assert result["method"] == "credits"
        assert user.balance_credits == 7
        db_mock.commit.assert_called_once()

    async def test_deduct_from_subscription(self):
        """Списание с подписки"""
        user = Mock(spec=User)
        user.balance_credits = 0
        user.subscription_type = SubscriptionType.PREMIUM
        user.subscription_actions_left = 50
        user.subscription_end_date = datetime.utcnow() + timedelta(days=20)
        user.freemium_actions_used = 0

        db_mock = AsyncMock()

        result = await deduct_credits(db_mock, user, cost=1)

        assert result["success"] is True
        assert result["method"] == "subscription"
        assert user.subscription_actions_left == 49
        db_mock.commit.assert_called_once()

    async def test_deduct_from_freemium(self):
        """Списание с Freemium"""
        user = Mock(spec=User)
        user.balance_credits = 0
        user.subscription_type = SubscriptionType.NONE
        user.subscription_actions_left = 0
        user.freemium_actions_used = 3
        user.freemium_reset_date = datetime.utcnow()

        db_mock = AsyncMock()

        result = await deduct_credits(db_mock, user, cost=1)

        assert result["success"] is True
        assert result["method"] == "freemium"
        assert result["watermark"] is True
        assert user.freemium_actions_used == 4
        db_mock.commit.assert_called_once()

    async def test_deduct_insufficient_credits(self):
        """Попытка списания при недостатке средств"""
        user = Mock(spec=User)
        user.balance_credits = 1
        user.subscription_type = SubscriptionType.NONE
        user.subscription_actions_left = 0
        user.freemium_actions_used = 10
        user.freemium_reset_date = datetime.utcnow()

        db_mock = AsyncMock()

        result = await deduct_credits(db_mock, user, cost=5)

        assert result["success"] is False
        assert "error" in result
        db_mock.commit.assert_not_called()


@pytest.mark.asyncio
class TestAwardCredits:
    """Тесты начисления кредитов"""

    async def test_award_credits_success(self):
        """Успешное начисление кредитов"""
        user = Mock(spec=User)
        user.id = 123
        user.balance_credits = 10

        db_mock = AsyncMock()

        result = await award_credits(
            db_mock,
            user,
            amount=50,
            idempotency_key="test_payment_123"
        )

        assert result["success"] is True
        assert user.balance_credits == 60
        db_mock.commit.assert_called_once()

    async def test_award_credits_idempotency(self):
        """Проверка идемпотентности начисления"""
        # TODO: Требует mock для Payment модели
        pass


@pytest.mark.asyncio
class TestAwardSubscription:
    """Тесты начисления подписки"""

    async def test_award_subscription_new(self):
        """Начисление новой подписки"""
        user = Mock(spec=User)
        user.id = 123
        user.subscription_type = SubscriptionType.NONE
        user.subscription_actions_left = 0
        user.subscription_end_date = None

        db_mock = AsyncMock()

        result = await award_subscription(
            db_mock,
            user,
            subscription_type=SubscriptionType.PREMIUM,
            actions=150,
            idempotency_key="sub_payment_456"
        )

        assert result["success"] is True
        assert user.subscription_type == SubscriptionType.PREMIUM
        assert user.subscription_actions_left == 150
        assert user.subscription_end_date is not None
        db_mock.commit.assert_called_once()

    async def test_award_subscription_renewal(self):
        """Продление существующей подписки"""
        user = Mock(spec=User)
        user.id = 123
        user.subscription_type = SubscriptionType.BASIC
        user.subscription_actions_left = 10
        user.subscription_end_date = datetime.utcnow() + timedelta(days=10)

        db_mock = AsyncMock()

        result = await award_subscription(
            db_mock,
            user,
            subscription_type=SubscriptionType.PREMIUM,
            actions=150,
            idempotency_key="sub_payment_789"
        )

        assert result["success"] is True
        assert user.subscription_type == SubscriptionType.PREMIUM
        # Действия должны заменить старые, а не суммироваться
        assert user.subscription_actions_left == 150
        db_mock.commit.assert_called_once()
