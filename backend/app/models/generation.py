"""
Generation Model — Модель генерации изображений.

Хранит историю всех генераций (примерка и редактирование).
"""

from typing import Optional
import enum

from sqlalchemy import (
    Integer,
    String,
    Text,
    Enum,
    ForeignKey,
    Numeric,
    Index,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class GenerationType(str, enum.Enum):
    """Типы генераций"""
    FITTING = "fitting"      # Примерка одежды/аксессуаров
    EDITING = "editing"      # Редактирование изображений


class Generation(Base, TimestampMixin):
    """
    Модель генерации изображения.

    Хранит информацию о всех генерациях пользователя:
    - Примерка: user_photo + item_photo → result
    - Редактирование: base_photo + prompt → result
    """

    __tablename__ = "generations"

    # Primary Key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    # Foreign Key to User
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="ID пользователя",
    )

    # Тип генерации
    type: Mapped[GenerationType] = mapped_column(
        Enum(GenerationType, name="generation_type_enum"),
        nullable=False,
        index=True,
        comment="Тип генерации (примерка или редактирование)",
    )

    # Входные данные для примерки
    user_photo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="URL фото пользователя/модели (для примерки)",
    )

    item_photo_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="URL фото одежды/аксессуара (для примерки)",
    )

    # Зона для аксессуаров (для примерки)
    accessory_zone: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Зона размещения аксессуара (голова, шея, руки, ноги)",
    )

    # Промпт
    prompt: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Текстовый промпт для генерации/редактирования",
    )

    # Результат генерации
    image_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="URL сгенерированного изображения",
    )

    # Статус генерации
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
        comment="Статус: pending, processing, completed, failed",
    )

    # Прогресс генерации (0-100)
    progress: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Прогресс генерации в процентах (0-100)",
    )

    # Task ID для отслеживания прогресса
    task_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        index=True,
        comment="ID задачи Celery для отслеживания",
    )

    # Кредиты и токены
    credits_spent: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
        comment="Количество потраченных кредитов",
    )

    tokens_used: Mapped[Optional[float]] = mapped_column(
        Numeric(10, 2),
        nullable=True,
        comment="Количество использованных токенов (для редактирования с AI)",
    )

    # Водяной знак (для Freemium)
    has_watermark: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="Наличие водяного знака (Freemium)",
    )

    # Ошибки
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Сообщение об ошибке при генерации",
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="generations",
    )

    # Индексы
    __table_args__ = (
        Index("idx_gen_user_id_created", "user_id", "created_at"),
        Index("idx_gen_type_status", "type", "status"),
        Index("idx_gen_task_id", "task_id"),
    )

    def __repr__(self) -> str:
        return (
            f"<Generation(id={self.id}, type={self.type}, "
            f"user_id={self.user_id}, status={self.status})>"
        )

    @property
    def is_completed(self) -> bool:
        """Проверка завершённости генерации"""
        return self.status == "completed"

    @property
    def is_failed(self) -> bool:
        """Проверка ошибки генерации"""
        return self.status == "failed"
