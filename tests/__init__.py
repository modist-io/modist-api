# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""
"""

from typing import Generator
from contextlib import contextmanager

import attr
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

import modist.db
from modist.env import instance as env

SQLALCHEMY_ENGINE = create_engine(env.database.url)
SQLALCHEMY_SESSION_MAKER = sessionmaker(bind=SQLALCHEMY_ENGINE)
SQLALCHEMY_SESSION = SQLALCHEMY_SESSION_MAKER()


@attr.s(repr=False)
class MockDatabase(object):
    """A mock implementation of the database manager with a singular global session."""

    Meta = MetaData()
    Entity = declarative_base(metadata=Meta)

    url: str = attr.ib()
    echo: bool = attr.ib(default=True)

    @property
    def engine(self):
        return SQLALCHEMY_ENGINE

    @property
    def session_maker(self) -> sessionmaker:
        return SQLALCHEMY_SESSION_MAKER

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        yield SQLALCHEMY_SESSION


# NOTE: it is CRUCIAL that the general database class get FULLY replaced as it is
# marshalled by the Python runtime. Because testing requires a singular session for
# generating and verifying content, we just override the session and session maker
# features to point to a single global session during testing.
setattr(modist.db, "Database", MockDatabase)
