"""Create mod_image table.

Revision ID: d215d41a65ef
Revises: 6d3e1987041d
Create Date: 2020-04-16 14:20:21.250743

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "d215d41a65ef"
down_revision = "6d3e1987041d"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_image",
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
        sa.Column("image_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["image_id"], ["image.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["mod_id"], ["mod.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("mod_id", "image_id"),
    )
    op.create_refresh_updated_at_trigger("mod_image")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_image")
    op.drop_table("mod_image")
