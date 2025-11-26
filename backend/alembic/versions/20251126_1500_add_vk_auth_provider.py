"""add_vk_auth_provider

Revision ID: f7g8h9i0j1k2
Revises: 6c08b5a2b943
Create Date: 2025-11-26 15:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7g8h9i0j1k2'
down_revision: Union[str, None] = '6c08b5a2b943'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Добавляет значение 'vk' в enum auth_provider_enum для поддержки VK ID авторизации.

    ВАЖНО: ALTER TYPE ADD VALUE не может быть выполнен в транзакции в PostgreSQL.
    Alembic автоматически обрабатывает это, выполняя операцию вне транзакции.
    """
    # Добавляем новое значение 'vk' в существующий enum
    # PostgreSQL требует выполнения этой операции вне транзакционного блока
    op.execute("COMMIT")  # Завершаем текущую транзакцию
    op.execute("ALTER TYPE auth_provider_enum ADD VALUE IF NOT EXISTS 'vk'")


def downgrade() -> None:
    """
    Откат миграции (удаление 'vk' из enum).

    ВАЖНО: PostgreSQL не поддерживает удаление значений из enum напрямую.
    Для отката потребуется:
    1. Убедиться, что нет пользователей с auth_provider='vk'
    2. Пересоздать enum без значения 'vk' (сложная операция)

    В production окружении откат этой миграции НЕ РЕКОМЕНДУЕТСЯ.
    Если необходимо, выполните вручную через SQL:

    1. UPDATE users SET auth_provider='email' WHERE auth_provider='vk';
    2. CREATE TYPE auth_provider_enum_new AS ENUM ('email', 'google', 'telegram');
    3. ALTER TABLE users ALTER COLUMN auth_provider TYPE auth_provider_enum_new
       USING auth_provider::text::auth_provider_enum_new;
    4. DROP TYPE auth_provider_enum;
    5. ALTER TYPE auth_provider_enum_new RENAME TO auth_provider_enum;
    """
    # Предупреждение: откат этой миграции сложен и не рекомендуется
    print(
        "WARNING: Downgrade of this migration is not trivial. "
        "PostgreSQL does not support removing enum values directly. "
        "Manual intervention required. See migration file for SQL commands."
    )

    # Проверяем, есть ли пользователи с auth_provider='vk'
    connection = op.get_bind()
    result = connection.execute(
        sa.text("SELECT COUNT(*) FROM users WHERE auth_provider = 'vk'")
    )
    count = result.scalar()

    if count > 0:
        raise Exception(
            f"Cannot downgrade: {count} users have auth_provider='vk'. "
            "Please migrate these users to another auth provider first."
        )

    # Если пользователей с VK нет, можно попытаться пересоздать enum
    # (это сложная операция, поэтому просто выводим предупреждение)
    print(
        "No VK users found. To complete downgrade, manually remove 'vk' from "
        "auth_provider_enum using the SQL commands in the migration file."
    )
