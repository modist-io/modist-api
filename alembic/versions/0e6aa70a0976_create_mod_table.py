"""Create mod table.

Revision ID: 0e6aa70a0976
Revises: a063cc924343
Create Date: 2020-04-15 17:20:28.990480

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "0e6aa70a0976"
down_revision = "a063cc924343"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod",
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
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("host_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("category_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("age_restriction_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["category_id"], ["category.id"], ondelete="set null"),
        sa.ForeignKeyConstraint(["host_id"], ["host.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(
            ["age_restriction_id"], ["age_restriction.id"], ondelete="cascade"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
        sa.UniqueConstraint("user_id", "slug"),
    )
    op.create_refresh_updated_at_trigger("mod")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod")
    op.drop_table("mod")
