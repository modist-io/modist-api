"""Create mod_ban table.

Revision ID: 7dd3398efced
Revises: 5dc276e78e4a
Create Date: 2020-04-15 18:01:33.256027

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "7dd3398efced"
down_revision = "5dc276e78e4a"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_ban",
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
        sa.Column("mod_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ban_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["ban_id"], ["ban.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["mod_id"], ["mod.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("mod_id", "ban_id"),
    )
    op.create_refresh_updated_at_trigger("mod_ban")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_ban")
    op.drop_table("mod_ban")
