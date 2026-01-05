"""
Password Reset Token Model — токены для сброса пароля.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class PasswordResetToken(Base, TimestampMixin):
    """
    Токен для сброса пароля.

    Токены имеют срок действия и могут быть использованы только один раз.
    """

    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID пользователя",
    )

    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
        comment="Уникальный токен сброса пароля",
    )

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        comment="Дата и время истечения токена",
    )

    consumed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Дата и время использования токена (null если не использован)",
    )

    request_ip: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True,
        comment="IP-адрес запроса",
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="User-Agent браузера",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="password_reset_tokens",
    )

    __table_args__ = (
        Index("idx_password_reset_token", "token"),
        Index("idx_password_reset_user_id", "user_id"),
        Index("idx_password_reset_expires_at", "expires_at"),
        Index("idx_password_reset_consumed_at", "consumed_at"),
    )

    @property
    def is_expired(self) -> bool:
        from datetime import timezone
        return datetime.now(timezone.utc) > self.expires_at

    @property
    def is_consumed(self) -> bool:
        return self.consumed_at is not None

    @property
    def is_valid(self) -> bool:
        return not self.is_expired and not self.is_consumed
