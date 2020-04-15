"""Create depth and lineage recursive function

Revision ID: bef058def9c6
Revises: 6b11ce07e430
Create Date: 2020-04-15 13:48:11.973099

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "bef058def9c6"
down_revision = "6b11ce07e430"
branch_labels = None
depends_on = None


CREATE_FUNCTION_SQL = """
CREATE OR REPLACE FUNCTION refresh_depth_and_lineage()
RETURNS TRIGGER AS
$$
DECLARE
  depth integer;
  lineage uuid[];
BEGIN
    EXECUTE FORMAT('
      WITH
      RECURSIVE ancestry AS (
        SELECT
          id,
          parent_id
        FROM
          %1$I.%2$I
        WHERE
          id = $1
        UNION
          SELECT
            grandparent.id,
            grandparent.parent_id
          FROM
            %1$I.%2$I grandparent
          INNER JOIN
            ancestry
          ON
            grandparent.id = ancestry.parent_id
      )
      SELECT
        COUNT(1) AS depth,
        array_remove(array_append(array_agg(target.parent_id), $1), NULL) AS lineage
      FROM
        ancestry
      INNER JOIN
        %1$I.%2$I target
      ON
        ancestry.id = target.id;
    '::text,
      TG_TABLE_SCHEMA,
      TG_TABLE_NAME
    )
    INTO depth, lineage
    USING NEW.parent_id;
  NEW.depth = depth;
  NEW.lineage = lineage;
  RETURN NEW;
END
$$
LANGUAGE plpgsql;
"""
DROP_FUNCTION_SQL = "DROP FUNCTION IF EXISTS refresh_depth_and_lineage"


def upgrade():
    """Pushes changes into the database."""

    op.execute(CREATE_FUNCTION_SQL)


def downgrade():
    """Reverts changes performed by upgrade()."""

    op.execute(DROP_FUNCTION_SQL)
