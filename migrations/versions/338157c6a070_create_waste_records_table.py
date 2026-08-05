"""create waste records table

Revision ID: 338157c6a070
Revises: 1107179818a7
Create Date: 2026-08-04 18:06:19.858897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '338157c6a070'
down_revision: Union[str, Sequence[str], None] = '1107179818a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "waste_records",

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
            "quantity",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "reason",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "cost",
            sa.Numeric(
                precision=10,
                scale=2,
            ),
            nullable=False,
            server_default="0",
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

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:

    op.drop_table(
        "waste_records"
    )
