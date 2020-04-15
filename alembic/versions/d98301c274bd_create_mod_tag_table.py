"""Create mod_tag table.

Revision ID: d98301c274bd
Revises: 79ee5a7a99a4
Create Date: 2020-04-15 17:53:33.123687

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "d98301c274bd"
down_revision = "79ee5a7a99a4"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_tag",
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
        sa.Column("tag_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["mod_id"], ["mod.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["tag_id"], ["tag.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("mod_id", "tag_id"),
    )
    op.create_refresh_updated_at_trigger("mod_tag")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_tag")
    op.drop_table("mod_tag")
