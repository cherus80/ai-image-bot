"""
User Model — Модель пользователя.

Хранит информацию о пользователях, балансе кредитов и подписках.
"""

from datetime import datetime
from typing import Optional
import enum

from sqlalchemy import (
    BigInteger,
    Integer,
    String,
    Enum,
    DateTime,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class SubscriptionType(str, enum.Enum):
    """Типы подписок"""
    BASIC = "basic"      # 299₽/месяц — 50 действий
    PRO = "pro"          # 499₽/месяц — 150 действий
    PREMIUM = "premium"  # 899₽/месяц — 500 действий


class User(Base, TimestampMixin):
    """
    Модель пользователя.

    Хранит данные о пользователе Telegram, балансе кредитов,
    подписке и использовании Freemium.
    """

    __tablename__ = "users"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    # Telegram ID (уникальный идентификатор пользователя)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
        comment="Telegram user ID",
    )

    # Профиль пользователя
    username: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Telegram username",
    )

    first_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Telegram first name",
    )

    last_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="Telegram last name",
    )

    # Баланс кредитов
    balance_credits: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Количество кредитов (1 кредит = 1 действие)",
    )

    # Подписка
    subscription_type: Mapped[Optional[SubscriptionType]] = mapped_column(
        Enum(SubscriptionType, name="subscription_type_enum"),
        nullable=True,
        comment="Тип активной подписки",
    )

    subscription_end: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата окончания подписки",
    )

    # Freemium счётчик
    freemium_actions_used: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Количество использованных Freemium действий в текущем месяце",
    )

    freemium_reset_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата последнего сброса Freemium счётчика",
    )

    # Активность
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        comment="Активен ли пользователь",
    )

    is_banned: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="Забанен ли пользователь",
    )

    # Relationships
    generations: Mapped[list["Generation"]] = relationship(
        "Generation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    chat_histories: Mapped[list["ChatHistory"]] = relationship(
        "ChatHistory",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    payments: Mapped[list["Payment"]] = relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Рефералы (где пользователь — реферер)
    referrals_given: Mapped[list["Referral"]] = relationship(
        "Referral",
        foreign_keys="[Referral.referrer_id]",
        back_populates="referrer",
        cascade="all, delete-orphan",
    )

    # Рефералы (где пользователь — приглашённый)
    referrals_received: Mapped[list["Referral"]] = relationship(
        "Referral",
        foreign_keys="[Referral.referred_id]",
        back_populates="referred",
        cascade="all, delete-orphan",
    )

    # Индексы
    __table_args__ = (
        Index("idx_telegram_id", "telegram_id"),
        Index("idx_subscription_end", "subscription_end"),
        Index("idx_is_active", "is_active"),
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, telegram_id={self.telegram_id}, "
            f"username={self.username}, balance={self.balance_credits})>"
        )

    @property
    def has_active_subscription(self) -> bool:
        """Проверка активности подписки"""
        if not self.subscription_type or not self.subscription_end:
            return False
        # Используем UTC для корректного сравнения с timezone-aware datetime
        from datetime import timezone
        return self.subscription_end > datetime.now(timezone.utc)

    @property
    def can_use_freemium(self) -> bool:
        """Проверка доступности Freemium"""
        from app.core.config import settings
        return self.freemium_actions_used < settings.FREEMIUM_ACTIONS_PER_MONTH

    def reset_freemium_if_needed(self) -> None:
        """Сброс Freemium счётчика, если прошёл месяц"""
        from datetime import timezone

        if not self.freemium_reset_at:
            # Используем UTC для согласованности с БД (DateTime(timezone=True))
            self.freemium_reset_at = datetime.now(timezone.utc)
            return

        # Проверка, прошёл ли месяц
        now = datetime.now(timezone.utc)
        if (now - self.freemium_reset_at).days >= 30:
            self.freemium_actions_used = 0
            self.freemium_reset_at = now
