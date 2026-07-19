"""add security fields to users

Revision ID: e8b909cbdc54
Revises: bcef9134359c
Create Date: 2026-07-16 20:14:14.204280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8b909cbdc54'
down_revision: Union[str, Sequence[str], None] = 'bcef9134359c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
