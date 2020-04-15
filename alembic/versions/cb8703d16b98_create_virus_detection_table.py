"""Create virus_detection table.

Revision ID: cb8703d16b98
Revises: 3ea865991c72
Create Date: 2020-04-15 18:49:22.544399

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "cb8703d16b98"
down_revision = "3ea865991c72"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "virus_detection",
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
        sa.Column(
            "detected_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("detector", sa.Text(), nullable=False),
        sa.Column("detector_version", sa.Text(), nullable=True),
        sa.Column("checksum", sa.Text(), nullable=False),
        sa.Column("is_unsafe", sa.Boolean(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_refresh_updated_at_trigger("virus_detection")
    op.create_index(
        op.f("ix_virus_detection_checksum"),
        "virus_detection",
        ["checksum"],
        unique=False,
    )


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("virus_detection")
    op.drop_index(op.f("ix_virus_detection_checksum"), table_name="virus_detection")
    op.drop_table("virus_detection")
