"""Create user table.

Revision ID: d67f84df8828
Revises: bef058def9c6
Create Date: 2020-04-15 15:33:02.893795

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "d67f84df8828"
down_revision = "bef058def9c6"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "user",
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
        sa.Column("verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("authenticated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("born_on", sa.Date(), nullable=True),
        sa.Column("is_anonymous", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("email", sau.types.email.EmailType(length=255), nullable=False),
        sa.Column("given_name", sa.String(length=64), nullable=True),
        sa.Column("family_name", sa.String(length=64), nullable=True),
        sa.Column("display_name", sa.String(length=64), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("avatar_image", sa.String(length=64), nullable=True),
        sa.Column("status_emoji", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=128), nullable=True),
        sa.Column(
            "preferences",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("display_name"),
        sa.UniqueConstraint("email"),
    )
    op.create_refresh_updated_at_trigger("user")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("user")
    op.drop_table("user")
