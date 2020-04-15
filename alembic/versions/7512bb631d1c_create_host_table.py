"""Create host table.

Revision ID: 7512bb631d1c
Revises: b4077c09993b
Create Date: 2020-04-15 15:56:34.392471

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "7512bb631d1c"
down_revision = "b4077c09993b"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "host",
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
        sa.Column("slug", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("banner_image", sa.String(length=255), nullable=True),
        sa.Column("avatar_image", sa.String(length=255), nullable=True),
        sa.Column("host_publisher_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["host_publisher_id"], ["host_publisher.id"],),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_refresh_updated_at_trigger("host")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("host")
    op.drop_table("host")
