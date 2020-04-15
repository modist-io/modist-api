"""Create user_ban table.

Revision ID: 5b254b0fd942
Revises: c5b191c91531
Create Date: 2020-04-15 18:23:48.333447

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "5b254b0fd942"
down_revision = "c5b191c91531"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "user_ban",
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
        sa.Column("ban_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["ban_id"], ["ban.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("user_id", "ban_id"),
    )
    op.create_refresh_updated_at_trigger("user_ban")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("user_ban")
    op.drop_table("user_ban")
    # ### end Alembic commands ###
