"""Create host_publisher table.

Revision ID: b4077c09993b
Revises: d67f84df8828
Create Date: 2020-04-15 15:45:30.364085

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "b4077c09993b"
down_revision = "d67f84df8828"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "host_publisher",
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
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_refresh_updated_at_trigger("host_publisher")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("host_publisher")
    op.drop_table("host_publisher")
