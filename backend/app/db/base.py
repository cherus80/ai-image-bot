"""
Базовый класс для всех SQLAlchemy моделей.
"""

from sqlalchemy.orm import DeclarativeBase, declared_attr
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей"""

    # Автоматическое именование таблиц
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Генерация имени таблицы из имени класса (snake_case)"""
        import re
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return name + 's' if not name.endswith('s') else name

    # Общие поля для всех моделей (можно переопределить)
    # id автоматически добавляется в конкретных моделях
    pass


class TimestampMixin:
    """Mixin для добавления timestamp полей"""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
