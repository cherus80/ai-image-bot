"""
Referral Model — Модель реферальной программы.

Хранит информацию о рефералах и начисленных бонусах.
"""

from sqlalchemy import (
    Integer,
    ForeignKey,
    Index,
    Boolean,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class Referral(Base, TimestampMixin):
    """
    Модель реферальной программы.

    Логика:
    - Пользователь A приглашает пользователя B
    - После первого действия пользователя B, пользователь A получает +10 кредитов
    - Один пользователь может пригласить множество друзей
    """

    __tablename__ = "referrals"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    # Foreign Keys
    referrer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID пользователя, который пригласил (реферер)",
    )

    referred_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID приглашённого пользователя (реферал)",
    )

    # Бонусы
    credits_awarded: Mapped[int] = mapped_column(
        Integer,
        default=10,
        nullable=False,
        comment="Количество начисленных кредитов реферу (+10 по умолчанию)",
    )

    # Статус
    is_awarded: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Были ли начислены кредиты (после первого действия реферала)",
    )

    # Relationships
    referrer: Mapped["User"] = relationship(
        "User",
        foreign_keys=[referrer_id],
        back_populates="referrals_given",
    )

    referred: Mapped["User"] = relationship(
        "User",
        foreign_keys=[referred_id],
        back_populates="referrals_received",
    )

    # Индексы
    __table_args__ = (
        Index("idx_referrer_id", "referrer_id"),
        Index("idx_referred_id", "referred_id"),
        Index("idx_is_awarded", "is_awarded"),
        # Уникальный constraint: один пользователь не может быть приглашён дважды
        Index(
            "idx_unique_referral",
            "referrer_id",
            "referred_id",
            unique=True,
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<Referral(id={self.id}, referrer_id={self.referrer_id}, "
            f"referred_id={self.referred_id}, is_awarded={self.is_awarded})>"
        )

    def award_credits(self) -> None:
        """Отметить, что кредиты начислены"""
        self.is_awarded = True
