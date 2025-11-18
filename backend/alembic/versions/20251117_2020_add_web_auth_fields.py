"""add_web_auth_fields_to_user

Revision ID: a1b2c3d4e5f6
Revises: 093f27321f56
Create Date: 2025-11-17 20:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '093f27321f56'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Создаём новый enum для auth_provider
    auth_provider_enum = postgresql.ENUM('email', 'google', 'telegram', name='auth_provider_enum')
    auth_provider_enum.create(op.get_bind(), checkfirst=True)

    # Добавляем новые поля для веб-авторизации
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=True, comment='Email address (unique, for web auth)'))
    op.add_column('users', sa.Column('email_verified', sa.Boolean(), nullable=False, server_default='false', comment='Is email verified'))
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True, comment='Bcrypt password hash (null for OAuth users)'))
    op.add_column('users', sa.Column('auth_provider', auth_provider_enum, nullable=False, server_default='email', comment='Authentication provider (email, google, telegram)'))
    op.add_column('users', sa.Column('oauth_provider_id', sa.String(length=255), nullable=True, comment='OAuth provider user ID (Google sub, etc.)'))

    # Делаем telegram_id nullable (опциональным)
    op.alter_column('users', 'telegram_id',
                    existing_type=sa.BigInteger(),
                    nullable=True,
                    existing_comment='Telegram user ID (optional, for legacy users)')

    # Создаём индексы для новых полей
    op.create_index('idx_email', 'users', ['email'], unique=False)
    op.create_index('idx_oauth_provider_id', 'users', ['oauth_provider_id'], unique=False)
    op.create_index('idx_auth_provider', 'users', ['auth_provider'], unique=False)

    # Создаём unique constraint для email
    op.create_unique_constraint('uq_users_email', 'users', ['email'])

    # Для существующих Telegram пользователей устанавливаем auth_provider = 'telegram'
    op.execute("""
        UPDATE users
        SET auth_provider = 'telegram'
        WHERE telegram_id IS NOT NULL
    """)


def downgrade() -> None:
    # Удаляем индексы
    op.drop_index('idx_auth_provider', table_name='users')
    op.drop_index('idx_oauth_provider_id', table_name='users')
    op.drop_index('idx_email', table_name='users')

    # Удаляем unique constraint
    op.drop_constraint('uq_users_email', 'users', type_='unique')

    # Возвращаем telegram_id обратно к NOT NULL
    op.alter_column('users', 'telegram_id',
                    existing_type=sa.BigInteger(),
                    nullable=False,
                    existing_comment='Telegram user ID')

    # Удаляем новые столбцы
    op.drop_column('users', 'oauth_provider_id')
    op.drop_column('users', 'auth_provider')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email_verified')
    op.drop_column('users', 'email')

    # Удаляем enum
    auth_provider_enum = postgresql.ENUM('email', 'google', 'telegram', name='auth_provider_enum')
    auth_provider_enum.drop(op.get_bind(), checkfirst=True)
