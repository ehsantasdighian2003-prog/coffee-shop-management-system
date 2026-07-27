"""add security fields to users

Revision ID: e8b909cbdc54
Revises: bcef9134359c
Create Date: 2026-07-16 20:14:14.204280

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "e8b909cbdc54"
down_revision: str | Sequence[str] | None = "bcef9134359c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
