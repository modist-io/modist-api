"""Create mod_rating table.

Revision ID: e79b5dcf9036
Revises: 8b7f242cff8f
Create Date: 2020-04-16 13:08:20.884825

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from modist.models._types import SemverType

from alembic import op

# revision identifiers, used by Alembic.
revision = "e79b5dcf9036"
down_revision = "8b7f242cff8f"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_rating",
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
        sa.Column("rating_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version", SemverType(), nullable=False),
        sa.ForeignKeyConstraint(["mod_id"], ["mod.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["rating_id"], ["rating.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("mod_id", "rating_id", "user_id"),
        sa.UniqueConstraint("mod_id", "user_id", "version"),
    )
    op.create_refresh_updated_at_trigger("mod_rating")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_rating")
    op.drop_table("mod_rating")
