"""Create mod_post table.

Revision ID: 67c1b54390ff
Revises: a1db27f3a43e
Create Date: 2020-04-16 13:28:31.106061

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "67c1b54390ff"
down_revision = "a1db27f3a43e"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_post",
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
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["mod_id"], ["mod.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["post_id"], ["post.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("mod_id", "post_id"),
    )
    op.create_refresh_updated_at_trigger("mod_post")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_post")
    op.drop_table("mod_post")
