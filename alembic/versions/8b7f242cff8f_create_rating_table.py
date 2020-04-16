"""Create rating table.

Revision ID: 8b7f242cff8f
Revises: eb14f215e211
Create Date: 2020-04-16 13:00:19.657370

"""
import sqlalchemy as sa
from modist.models.user import RatingType
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "8b7f242cff8f"
down_revision = "eb14f215e211"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "rating",
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
        sa.Column("type", sa.Enum("MOD", name="ratingtype"), nullable=False),
        sa.Column("rating", sa.Numeric(precision=3, scale=2), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_refresh_updated_at_trigger("rating")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("rating")
    op.drop_table("rating")
    sa.Enum(RatingType).drop(bind=op.get_bind())
