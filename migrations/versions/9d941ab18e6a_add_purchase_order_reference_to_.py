"""add purchase order reference to inventory transactions

Revision ID: 9d941ab18e6a
Revises: 90b7a19919f3
Create Date: 2026-08-04 15:26:27.383581

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d941ab18e6a'
down_revision: Union[str, Sequence[str], None] = '90b7a19919f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "inventory_transactions",
        sa.Column(
            "purchase_order_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_inventory_transactions_purchase_order",
        "inventory_transactions",
        "purchase_orders",
        ["purchase_order_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:

    op.drop_constraint(
        "fk_inventory_transactions_purchase_order",
        "inventory_transactions",
        type_="foreignkey",
    )

    op.drop_column(
        "inventory_transactions",
        "purchase_order_id",
    )
    
