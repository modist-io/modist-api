"""Create comment_ranking table.

Revision ID: eb14f215e211
Revises: 461756447c4f
Create Date: 2020-04-16 12:47:33.714435

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "eb14f215e211"
down_revision = "461756447c4f"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "comment_ranking",
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
        sa.Column("comment_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ranking_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["comment_id"], ["comment.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["ranking_id"], ["ranking.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("comment_id", "ranking_id"),
        sa.UniqueConstraint("comment_id", "user_id"),
    )
    op.create_refresh_updated_at_trigger("comment_ranking")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("comment_ranking")
    op.drop_table("comment_ranking")
