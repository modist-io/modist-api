"""Create mod_release_conflict table.

Revision ID: c5b191c91531
Revises: 7333a2959aa8
Create Date: 2020-04-15 18:19:57.187237

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "c5b191c91531"
down_revision = "7333a2959aa8"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_release_conflict",
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
        sa.Column("mod_release_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("mod_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("version_expression", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["mod_id"], ["mod.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(
            ["mod_release_id"], ["mod_release.id"], ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("mod_release_id", "mod_id"),
    )
    op.create_refresh_updated_at_trigger("mod_release_conflict")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_release_conflict")
    op.drop_table("mod_release_conflict")
