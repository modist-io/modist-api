"""Create host_publisher_social table.

Revision ID: b025d6932748
Revises: fe9c31ba1c0e
Create Date: 2020-04-15 16:25:02.970363

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "b025d6932748"
down_revision = "fe9c31ba1c0e"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "host_publisher_social",
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
        sa.Column("host_publisher_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("social_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["host_publisher_id"], ["host_publisher.id"], ondelete="cascade"
        ),
        sa.ForeignKeyConstraint(["social_id"], ["social.id"],),
        sa.PrimaryKeyConstraint("host_publisher_id", "social_id"),
    )
    op.create_refresh_updated_at_trigger("host_publisher_social")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("host_publisher_social")
    op.drop_table("host_publisher_social")
