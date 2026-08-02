"""add inventory transactions

Revision ID: afa38ed616c6
Revises: 31281ba1b3bd
Create Date: 2026-08-02 13:52:32.013251

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'afa38ed616c6'
down_revision: Union[str, Sequence[str], None] = '31281ba1b3bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.create_table(
    "inventory_transactions",

    sa.Column(
        "id",
        sa.Integer(),
        primary_key=True,
    ),

    sa.Column(
        "product_id",
        sa.Integer(),
        sa.ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    ),

    sa.Column(
        "change_type",
        sa.String(length=20),
        nullable=False,
    ),

    sa.Column(
        "quantity",
        sa.Integer(),
        nullable=False,
    ),

    sa.Column(
        "reason",
        sa.String(length=255),
        nullable=True,
    ),

    sa.Column(
        "created_by",
        sa.Integer(),
        sa.ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    ),

    sa.Column(
        "created_at",
        sa.DateTime(),
        nullable=False,
        server_default=sa.func.now(),
    ),
)


def downgrade() -> None:
    op.drop_table("inventory_transactions")
    
