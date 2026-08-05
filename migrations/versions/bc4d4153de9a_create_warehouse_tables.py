"""create warehouse tables

Revision ID: bc4d4153de9a
Revises: 9d941ab18e6a
Create Date: 2026-08-04 16:31:07.665508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc4d4153de9a'
down_revision: Union[str, Sequence[str], None] = '9d941ab18e6a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "warehouses",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "location",
            sa.String(length=255),
            nullable=True,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default="true",
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
        "warehouse_inventory",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
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
            server_default="0",
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
        "warehouse_inventory"
    )

    op.drop_table(
        "warehouses"
    )