"""Create mod_release_download table.

Revision ID: 954d25e175b1
Revises: d215d41a65ef
Create Date: 2020-04-16 14:29:16.120929

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "954d25e175b1"
down_revision = "d215d41a65ef"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_release_download",
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
        sa.Column(
            "downloaded_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("ip", postgresql.INET(), nullable=False),
        sa.Column(
            "headers",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.Column("mod_release_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("mod_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["mod_id"], ["mod.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(
            ["mod_release_id"], ["mod_release.id"], ondelete="set null"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="set null"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_refresh_updated_at_trigger("mod_release_download")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_release_download")
    op.drop_table("mod_release_download")
