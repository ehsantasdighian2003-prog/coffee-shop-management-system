"""initial schema

Revision ID: f70d7d7b2fae
Revises: e8b909cbdc54
Create Date: 2026-07-25 18:27:35.437901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f70d7d7b2fae'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column(
            "role",
            sa.String(),
            nullable=False,
            server_default="user"
        ),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("last_login", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )


    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )


    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.Column(
            "stock",
            sa.Integer(),
            nullable=True,
            server_default="0"
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True,
            server_default=sa.true()
        ),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["categories.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )


    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("customer_name", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP")
        ),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column(
            "quantity",
            sa.Integer(),
            server_default="1"
        ),
        sa.Column(
            "total_price",
            sa.Numeric(),
            server_default="0"
        ),
        sa.Column(
            "status",
            sa.String(),
            server_default="pending"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )


    op.create_table(
        "order_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("order_id", sa.Integer(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Numeric(), nullable=False),
        sa.ForeignKeyConstraint(
            ["order_id"],
            ["orders.id"]
        ),
        sa.ForeignKeyConstraint(
            ["product_id"],
            ["products.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table("order_items")
    op.drop_table("orders")
    op.drop_table("products")
    op.drop_table("categories")
    op.drop_table("users")
