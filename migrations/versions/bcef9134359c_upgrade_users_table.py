"""upgrade users table

Revision ID: bcef9134359c
Revises: 
Create Date: 2026-07-16 19:38:27.729553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcef9134359c'
down_revision: Union[str, Sequence[str], None] = 'f70d7d7b2fae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "users",
        sa.Column(
            "phone_number",
            sa.String(length=20),
            nullable=True
        )
    )

    op.add_column(
        "users",
        sa.Column(
            "profile_image",
            sa.String(length=500),
            nullable=True
        )
    )

    op.add_column(
        "users",
        sa.Column(
            "email_verified",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false()
        )
    )

    op.add_column(
        "users",
        sa.Column(
            "failed_login_attempts",
            sa.Integer(),
            nullable=False,
            server_default=sa.text("0")
        )
    )

    op.add_column(
        "users",
        sa.Column(
            "locked_until",
            sa.DateTime(),
            nullable=True
        )
    )

    op.add_column(
        "users",
        sa.Column(
            "deleted_at",
            sa.DateTime(),
            nullable=True
        )
    )
def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "deleted_at")
    op.drop_column("users", "locked_until")
    op.drop_column("users", "failed_login_attempts")
    op.drop_column("users", "email_verified")
    op.drop_column("users", "profile_image")
    op.drop_column("users", "phone_number")