"""Create mod_release_dependency table.

Revision ID: 7333a2959aa8
Revises: 28df99db32ca
Create Date: 2020-04-15 18:17:11.147269

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "7333a2959aa8"
down_revision = "28df99db32ca"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_release_dependency",
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
    op.create_refresh_updated_at_trigger("mod_release_dependency")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_release_dependency")
    op.drop_table("mod_release_dependency")
