"""add payment method to orders

Revision ID: 31281ba1b3bd
Revises: 40f23ad446f6
Create Date: 2026-08-01 16:55:16.346860

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31281ba1b3bd'
down_revision: Union[str, Sequence[str], None] = '40f23ad446f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "orders",
        sa.Column(
            "payment_method",
            sa.String(length=20),
            nullable=False,
            server_default="cash"
        )
    )


def downgrade() -> None:

    op.drop_column(
        "orders",
        "payment_method"
    )
