"""Create updated_at trigger function

Revision ID: 6b11ce07e430
Revises: a29b98ca21cf
Create Date: 2020-04-15 13:47:55.047140

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "6b11ce07e430"
down_revision = "a29b98ca21cf"
branch_labels = None
depends_on = None


CREATE_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION refresh_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
"""
DROP_FUNCTION_SQL = "DROP FUNCTION IF EXISTS refresh_updated_at"


def upgrade():
    """Pushes changes into the database."""

    op.execute(CREATE_FUNCTION_SQL)


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.execute(DROP_FUNCTION_SQL)
