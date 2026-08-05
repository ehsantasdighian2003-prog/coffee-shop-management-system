"""create purchase orders tables

Revision ID: 90b7a19919f3
Revises: 6429a5c9f224
Create Date: 2026-08-04 13:32:26.122985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '90b7a19919f3'
down_revision: Union[str, Sequence[str], None] = '6429a5c9f224'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "purchase_orders",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "supplier_id",
            sa.Integer(),
            sa.ForeignKey(
                "suppliers.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="draft",
        ),

        sa.Column(
            "total_amount",
            sa.Numeric(10, 2),
            nullable=False,
            server_default="0",
        ),

        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
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


    op.create_table(
        "purchase_order_items",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "purchase_order_id",
            sa.Integer(),
            sa.ForeignKey(
                "purchase_orders.id",
                ondelete="CASCADE",
            ),
            nullable=False,
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
            "quantity",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "unit_price",
            sa.Numeric(10, 2),
            nullable=False,
        ),

        sa.Column(
            "total_price",
            sa.Numeric(10, 2),
            nullable=False,
        ),
    )


def downgrade() -> None:

    op.drop_table("purchase_order_items")

    op.drop_table("purchase_orders")