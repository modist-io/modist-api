"""Create age_restriction table.

Revision ID: a063cc924343
Revises: 0c3924deb2b7
Create Date: 2020-04-15 17:10:22.653024

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "a063cc924343"
down_revision = "0c3924deb2b7"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "age_restriction",
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
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("avatar_image", sa.String(length=255), nullable=True),
        sa.Column("minimum_age", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_refresh_updated_at_trigger("age_restriction")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("age_restriction")
    op.drop_table("age_restriction")
