"""
Email Verification Token Model — Модель токенов для подтверждения email.

Хранит токены для верификации email-адресов пользователей.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class EmailVerificationToken(Base, TimestampMixin):
    """
    Модель токена для верификации email.

    Токены создаются при регистрации или по запросу пользователя,
    имеют ограниченный срок действия и могут быть использованы только один раз.
    """

    __tablename__ = "email_verification_tokens"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    # User ID (foreign key)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID пользователя",
    )

    # Token (unique random string)
    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Уникальный токен для верификации",
    )

    # Expiration time
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата и время истечения токена",
    )

    # Consumed (used) timestamp
    consumed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата и время использования токена (null если не использован)",
    )

    # Optional audit fields
    request_ip: Mapped[Optional[str]] = mapped_column(
        String(45),  # IPv4: 15 chars, IPv6: 45 chars
        nullable=True,
        comment="IP-адрес запроса",
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="User-Agent браузера",
    )

    # Relationship
    user: Mapped["User"] = relationship(
        "User",
        back_populates="email_verification_tokens",
    )

    # Indexes
    __table_args__ = (
        Index("idx_token", "token"),
        Index("idx_user_id", "user_id"),
        Index("idx_expires_at", "expires_at"),
        Index("idx_consumed_at", "consumed_at"),
    )

    def __repr__(self) -> str:
        return (
            f"<EmailVerificationToken(id={self.id}, user_id={self.user_id}, "
            f"expires_at={self.expires_at}, consumed={self.consumed_at is not None})>"
        )

    @property
    def is_expired(self) -> bool:
        """Проверка истечения срока действия токена"""
        from datetime import timezone
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_consumed(self) -> bool:
        """Проверка, был ли токен использован"""
        return self.consumed_at is not None

    @property
    def is_valid(self) -> bool:
        """Проверка валидности токена (не истек и не использован)"""
        return not self.is_expired and not self.is_consumed
