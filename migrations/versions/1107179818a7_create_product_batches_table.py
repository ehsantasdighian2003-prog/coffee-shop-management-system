"""create product batches table

Revision ID: 1107179818a7
Revises: 6cfacb4f8962
Create Date: 2026-08-04 17:26:20.818817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1107179818a7'
down_revision: Union[str, Sequence[str], None] = '6cfacb4f8962'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "product_batches",

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
            "warehouse_id",
            sa.Integer(),
            sa.ForeignKey(
                "warehouses.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "batch_number",
            sa.String(length=100),
            nullable=False,
            unique=True,
        ),

        sa.Column(
            "quantity",
            sa.Integer(),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "production_date",
            sa.Date(),
            nullable=True,
        ),

        sa.Column(
            "expiration_date",
            sa.Date(),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:

    op.drop_table(
        "product_batches"
    )
