"""
UserConsent Model — фиксация согласий на обработку ПДн.

Хранит факт согласия с версией формы, IP, User-Agent и источником (регистрация/логин).
"""

from typing import Optional

from sqlalchemy import Integer, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class UserConsent(Base, TimestampMixin):
    """Факт согласия пользователя на обработку ПДн."""

    __tablename__ = "user_consents"

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

    consent_version: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="Версия формы согласия на ПДн",
    )

    source: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        comment="Где получено согласие (register/login)",
    )

    ip_address: Mapped[Optional[str]] = mapped_column(
        String(45),  # IPv6 compatible
        nullable=True,
        comment="IP-адрес клиента",
    )

    user_agent: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="User-Agent клиента",
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="consents",
    )

    __table_args__ = (
        Index("idx_user_consents_user_version", "user_id", "consent_version"),
    )

    @property
    def granted_at(self):
        """Alias для времени выдачи согласия."""
        return self.created_at


__all__ = ["UserConsent"]
