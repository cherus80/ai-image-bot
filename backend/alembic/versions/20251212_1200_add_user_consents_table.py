"""add user consents table

Revision ID: 20251212_user_consents
Revises: 20251201_billing_v5
Create Date: 2025-12-12 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20251212_user_consents"
down_revision: Union[str, None] = "20251201_billing_v5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user_consents",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, index=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="ID пользователя"),
        sa.Column("consent_version", sa.String(length=64), nullable=False, comment="Версия формы согласия на ПДн"),
        sa.Column("source", sa.String(length=32), nullable=False, comment="Где получено согласие (register/login)"),
        sa.Column("ip_address", sa.String(length=45), nullable=True, comment="IP-адрес клиента"),
        sa.Column("user_agent", sa.String(length=500), nullable=True, comment="User-Agent клиента"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    op.create_index("idx_user_consents_user_id", "user_consents", ["user_id"])
    op.create_index("idx_user_consents_user_version", "user_consents", ["user_id", "consent_version"])
    op.create_index("idx_user_consents_created_at", "user_consents", ["created_at"])


def downgrade() -> None:
    op.drop_index("idx_user_consents_created_at", table_name="user_consents")
    op.drop_index("idx_user_consents_user_version", table_name="user_consents")
    op.drop_index("idx_user_consents_user_id", table_name="user_consents")
    op.drop_table("user_consents")
