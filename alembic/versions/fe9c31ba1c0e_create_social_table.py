"""Create social table.

Revision ID: fe9c31ba1c0e
Revises: 7512bb631d1c
Create Date: 2020-04-15 16:12:02.211522

"""
import sqlalchemy as sa
import sqlalchemy_utils as sau
from sqlalchemy.dialects import postgresql
from modist.models.common import SocialType

from alembic import op

# revision identifiers, used by Alembic.
revision = "fe9c31ba1c0e"
down_revision = "7512bb631d1c"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "social",
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
            "type", sa.Enum(SocialType), nullable=False, default=SocialType.GENERIC
        ),
        sa.Column("url", sau.types.url.URLType(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_unique_constraint("uq_social_type", "social", ["type", "url"])
    op.create_refresh_updated_at_trigger("social")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("social")
    op.drop_constraint("uq_social_type", "social")
    op.drop_table("social")
    sa.Enum(SocialType).drop(bind=op.get_bind())
