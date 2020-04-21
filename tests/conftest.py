# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc

from typing import Generator
from pathlib import Path

from pytest import yield_fixture
from sqlalchemy.orm import Session
from pytest_factoryboy import register as register_factory

from alembic.config import Config as AlembicConfig
from alembic.command import upgrade as alembic_upgrade

from . import factories

ALEMBIC_CONFIG_PATH = Path(__file__).parent.parent / "alembic.ini"
ALEMBIC_CONFIG = AlembicConfig(ALEMBIC_CONFIG_PATH.as_posix())


def pytest_configure(config):
    if "not db" in config.getoption("-m").lower():
        return

    # before testing session starts, ensure our database structure is up-to-date
    alembic_upgrade(ALEMBIC_CONFIG, "head")


# Register all importable SQLAlchemy model factory fixtures
for factory_name in factories.__all__:  # type: ignore
    factory = getattr(factories, factory_name)
    register_factory(factory, f"{factory._meta.model.__tablename__.lower()!s}_instance")


@yield_fixture
def db_session() -> Generator[Session, None, None]:
    """Fixture for generating a one-off SQLAlchemy session.

    :return: Yields a connected SQLAlchemy session
    :rtype: Generator[Session, None, None]
    """

    session_instance: Session = factories._common.SQLALCHEMY_SESSION
    yield session_instance
    session_instance.rollback()
