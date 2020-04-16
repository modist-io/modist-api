"""Create post table.

Revision ID: a1db27f3a43e
Revises: e79b5dcf9036
Create Date: 2020-04-16 13:19:45.634240

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "a1db27f3a43e"
down_revision = "e79b5dcf9036"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "post",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
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
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_refresh_updated_at_trigger("post")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("post")
    op.drop_table("post")
