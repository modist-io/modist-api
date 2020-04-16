"""Create user_social table.

Revision ID: e549fdc916f2
Revises: 8ffc14d908d2
Create Date: 2020-04-16 12:06:16.599824

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "e549fdc916f2"
down_revision = "8ffc14d908d2"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "user_social",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("social_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["social_id"], ["social.id"],),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("user_id", "social_id"),
    )
    op.create_refresh_updated_at_trigger("user_social")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("user_social")
    op.drop_table("user_social")
