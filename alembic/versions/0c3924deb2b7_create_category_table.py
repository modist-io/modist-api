"""Create category table.

Revision ID: 0c3924deb2b7
Revises: f68e6dafb977
Create Date: 2020-04-15 17:01:38.788610

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from modist.models.common import CategoryType

from alembic import op

# revision identifiers, used by Alembic.
revision = "0c3924deb2b7"
down_revision = "f68e6dafb977"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "category",
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
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("parent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("type", sa.Enum(CategoryType), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("depth", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "lineage",
            postgresql.ARRAY(postgresql.UUID(as_uuid=True)),
            server_default="{}",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["parent_id"], ["category.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("parent_id", "name", "type"),
    )
    op.create_refresh_updated_at_trigger("category")
    op.create_refresh_depth_and_lineage_trigger("category")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_depth_and_lineage_trigger("category")
    op.drop_refresh_updated_at_trigger("category")
    op.drop_table("category")
    sa.Enum(CategoryType).drop(bind=op.get_bind())
