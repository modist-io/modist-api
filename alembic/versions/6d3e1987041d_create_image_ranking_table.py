"""Create image_ranking table.

Revision ID: 6d3e1987041d
Revises: 4cb305a398ac
Create Date: 2020-04-16 13:48:12.904493

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "6d3e1987041d"
down_revision = "4cb305a398ac"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "image_ranking",
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
        sa.Column("image_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ranking_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["image_id"], ["image.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["ranking_id"], ["ranking.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("image_id", "ranking_id"),
        sa.UniqueConstraint("image_id", "user_id"),
    )
    op.create_refresh_updated_at_trigger("image_ranking")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("image_ranking")
    op.drop_table("image_ranking")
