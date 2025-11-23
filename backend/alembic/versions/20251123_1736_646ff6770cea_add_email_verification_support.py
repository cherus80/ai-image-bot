"""add_email_verification_support

Revision ID: 646ff6770cea
Revises: 2668afdcce4b
Create Date: 2025-11-23 17:36:35.325875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '646ff6770cea'
down_revision: Union[str, None] = '2668afdcce4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add email_verified_at column to users table
    op.add_column(
        'users',
        sa.Column('email_verified_at', sa.DateTime(timezone=True), nullable=True, comment='Дата и время подтверждения email')
    )

    # Create email_verification_tokens table
    op.create_table(
        'email_verification_tokens',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='Primary key'),
        sa.Column('user_id', sa.Integer(), nullable=False, comment='ID пользователя'),
        sa.Column('token', sa.String(length=255), nullable=False, comment='Уникальный токен для верификации'),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False, comment='Дата и время истечения токена'),
        sa.Column('consumed_at', sa.DateTime(timezone=True), nullable=True, comment='Дата и время использования токена (null если не использован)'),
        sa.Column('request_ip', sa.String(length=45), nullable=True, comment='IP-адрес запроса'),
        sa.Column('user_agent', sa.String(length=500), nullable=True, comment='User-Agent браузера'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Дата создания'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='Дата обновления'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_token', 'email_verification_tokens', ['token'], unique=False)
    op.create_index('idx_user_id', 'email_verification_tokens', ['user_id'], unique=False)
    op.create_index('idx_expires_at', 'email_verification_tokens', ['expires_at'], unique=False)
    op.create_index('idx_consumed_at', 'email_verification_tokens', ['consumed_at'], unique=False)
    op.create_index(op.f('ix_email_verification_tokens_id'), 'email_verification_tokens', ['id'], unique=False)
    op.create_index(op.f('ix_email_verification_tokens_token'), 'email_verification_tokens', ['token'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_email_verification_tokens_token'), table_name='email_verification_tokens')
    op.drop_index(op.f('ix_email_verification_tokens_id'), table_name='email_verification_tokens')
    op.drop_index('idx_consumed_at', table_name='email_verification_tokens')
    op.drop_index('idx_expires_at', table_name='email_verification_tokens')
    op.drop_index('idx_user_id', table_name='email_verification_tokens')
    op.drop_index('idx_token', table_name='email_verification_tokens')

    # Drop email_verification_tokens table
    op.drop_table('email_verification_tokens')

    # Drop email_verified_at column from users table
    op.drop_column('users', 'email_verified_at')
