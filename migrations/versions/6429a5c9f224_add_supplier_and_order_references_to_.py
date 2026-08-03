"""add supplier and order references to inventory transactions

Revision ID: 6429a5c9f224
Revises: ff7eff4171ee
Create Date: 2026-08-03 14:37:56.023261

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6429a5c9f224'
down_revision: Union[str, Sequence[str], None] = 'ff7eff4171ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "inventory_transactions",
        sa.Column(
            "supplier_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_inventory_transactions_supplier",
        "inventory_transactions",
        "suppliers",
        ["supplier_id"],
        ["id"],
        ondelete="SET NULL",
    )

    op.add_column(
        "inventory_transactions",
        sa.Column(
            "order_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_inventory_transactions_order",
        "inventory_transactions",
        "orders",
        ["order_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:

    op.drop_constraint(
        "fk_inventory_transactions_order",
        "inventory_transactions",
        type_="foreignkey",
    )

    op.drop_column(
        "inventory_transactions",
        "order_id",
    )

    op.drop_constraint(
        "fk_inventory_transactions_supplier",
        "inventory_transactions",
        type_="foreignkey",
    )

    op.drop_column(
        "inventory_transactions",
        "supplier_id",
    )
