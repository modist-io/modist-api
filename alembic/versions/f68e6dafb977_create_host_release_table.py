"""Create host_release table.

Revision ID: f68e6dafb977
Revises: b025d6932748
Create Date: 2020-04-15 16:44:26.135566

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from modist.models._types import SemverType

from alembic import op

# revision identifiers, used by Alembic.
revision = "f68e6dafb977"
down_revision = "b025d6932748"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "host_release",
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
        sa.Column("released_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("version", SemverType(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("host_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["host_id"], ["host.id"],),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("host_id", "version"),
    )
    op.create_unique_constraint(
        "uq_host_release_host_id", "host_release", ["host_id", "version"]
    )
    op.create_refresh_updated_at_trigger("host_release")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("host_release")
    op.drop_constraint("uq_host_release_host_id", "host_release")
    op.drop_table("host_release")
