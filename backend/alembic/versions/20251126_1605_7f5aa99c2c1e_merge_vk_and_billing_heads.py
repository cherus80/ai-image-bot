"""Merge billing v4 and VK auth heads."""

from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401

# revision identifiers, used by Alembic.
revision = "7f5aa99c2c1e"
down_revision = ("5c1cce7df3e4", "f7g8h9i0j1k2")
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Merge only; no schema changes required.
    pass


def downgrade() -> None:
    # No downgrade because this is a merge point.
    pass
