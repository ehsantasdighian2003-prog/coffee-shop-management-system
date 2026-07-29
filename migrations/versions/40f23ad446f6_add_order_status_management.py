"""add_order_status_management

Revision ID: 40f23ad446f6
Revises: e8b909cbdc54
Create Date: 2026-07-29 21:35:57.298513
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision: str = "40f23ad446f6"
down_revision: Union[str, Sequence[str], None] = "e8b909cbdc54"
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ==================================================
    # Update default value of order status
    # ==================================================

    op.alter_column(
        "orders",
        "status",
        existing_type=sa.String(),
        server_default="PENDING",
        existing_nullable=True,
    )

    # ==================================================
    # Order status history
    # ==================================================

    op.create_table(
        "order_status_history",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
        ),

        sa.Column(
            "order_id",
            sa.Integer(),
            sa.ForeignKey(
                "orders.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "changed_by",
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

    op.drop_table("order_status_history")

    op.alter_column(
        "orders",
        "status",
        existing_type=sa.String(),
        server_default="pending",
        existing_nullable=True,
    )