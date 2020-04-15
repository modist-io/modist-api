# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""The Alembic environment configuration."""

import os
import sys
from pathlib import Path
from logging.config import fileConfig

from sqlalchemy import pool, engine_from_config

from alembic import context

# NOTE: we must insert the current directories parent path in order to locally import
# operations for access to the custome Alembic operations defined within
sys.path.insert(0, Path(__file__).parent.absolute().as_posix())
import operations  # noqa isort:skip

# NOTE: we must import all available exposed models explicilty before we import the
# database client as we need to make sure all models are registered to the database's
# metadata before we attempt to build anything with the database.
from modist import models  # noqa isort:skip
from modist.db import Database  # noqa isort:skip


DATABASE_URL_VARNAME = "DATABASE_URL"

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# this is where we passthrough environment variables into the .ini config.
section = config.config_ini_section
config.set_section_option(
    section, DATABASE_URL_VARNAME, os.environ.get(DATABASE_URL_VARNAME)
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Database.Meta

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    url = os.environ.get(DATABASE_URL_VARNAME)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        connection.execute("CREATE SCHEMA IF NOT EXISTS alembic;")
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table="version",
            version_table_schema="alembic",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
