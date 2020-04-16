"""Create mod_ranking table.

Revision ID: e6bae18373c3
Revises: 34611e33e604
Create Date: 2020-04-16 12:21:12.005355

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "e6bae18373c3"
down_revision = "34611e33e604"
branch_labels = None
depends_on = None


def upgrade():
    """Pushes changes into the database."""

    op.create_table(
        "mod_ranking",
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
        sa.Column("mod_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("ranking_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(["mod_id"], ["mod.id"], ondelete="cascade"),
        sa.ForeignKeyConstraint(["ranking_id"], ["ranking.id"], ondelete="cascade"),
        sa.PrimaryKeyConstraint("mod_id", "ranking_id"),
    )
    op.create_refresh_updated_at_trigger("mod_ranking")


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.drop_refresh_updated_at_trigger("mod_ranking")
    op.drop_table("mod_ranking")
