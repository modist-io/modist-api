"""Create uuid-ossp extension.

Revision ID: a29b98ca21cf
Revises:
Create Date: 2020-04-15 13:47:10.381006

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a29b98ca21cf"
down_revision = None
branch_labels = None
depends_on = None

CREATE_EXTENSION_SQL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
"""
DROP_EXTENSION_SQL = """
DROP EXTENSION IF EXISTS "uuid-ossp";
"""


def upgrade():
    """Pushes changes into the database."""

    op.execute(CREATE_EXTENSION_SQL)


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.execute(DROP_EXTENSION_SQL)
