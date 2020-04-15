# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""The containing namespace for the database instance class."""

from typing import Callable, Optional, Generator
from contextlib import contextmanager

import attr
from sqlalchemy.orm import Session, sessionmaker, scoped_session
from cached_property import cached_property
from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base


@attr.s(repr=False)
class Database(object):
    """Database connection management instance.

    This database doesn't establish any connections on initialization or manage open
    connections during runtime. Instead it just provides a namespace for proper database
    sessions using the ``session()`` context manager. This is the proper way of
    managing SQLAlchemy connections as we can avoid connection leaks and mitigate
    SQL failures and rollbacks.

    Connections are only built during the entering of the ``session()`` context manager.
    These connections are subsequently destroyed when the context manager is exited.
    For an example how to utilize this manager, see the example below:

    >>> from modist.db import Database
    >>> from modist.models.user import User
    >>> db = Database(env.database.url)
    >>> with db.session() as session:
    ...     for user in session.query(User).all():
    ...         print(user.id)

    """

    Meta = MetaData()
    """The SQLAlchemy metadata instance that is used to contain declarative models."""

    Entity = declarative_base(metadata=Meta)
    """Marks a subclass of the entity under SQLAlchemy's declarative object metadata."""

    url: str = attr.ib()
    echo: bool = attr.ib(default=False)

    def __repr__(self) -> str:
        """Build a string representation to avoid printing sensitive data.

        :return: A string representation of the current database instance
        :rtype: str
        """

        return f"{self.__class__.__qualname__!s}(url='{self.engine.url!r}')"

    @cached_property
    def engine(self) -> Engine:
        """Build the SQLAlchemy engine instance use for connections with the given URL.

        .. note:: This is a cached property, updates of database instance's ``url``
            property will not trigger this property to rebuild a new engine instance.
            For all intensive purposes, we want a single immutable engine per database
            instance.

        :return: The SQLALchemy engine
        :rtype: sqlalchemy.engine.Engine
        """

        return create_engine(self.url, echo=self.echo)

    @cached_property
    def session_maker(self) -> sessionmaker:
        """Build a SQLAlchemy session maker class.

        .. note:: This is a cached property, updates of database instance's ``url``
            property will not trigger this property to rebuild a new session maker
            instance. For all intensive purposes, we want a single immutable session
            maker per database instance.

        :return: The session builder for building new sessions to the given URL.
        :rtype: sqlalchemy.orm.sessionmaker
        """

        self._session_maker = sessionmaker()
        self._session_maker.configure(bind=self.engine)
        return self._session_maker

    @contextmanager
    def session(
        self,
        reraise: bool = True,
        auto_commit: bool = True,
        auto_rollback: bool = True,
        scoped: bool = False,
    ) -> Generator[Session, None, None]:
        """Build a session context manager for a transactional connection to a database.

        :param bool reraise: Re-raises exceptions if they occur, optional,
            defaults to True
        :param bool auto_commit: Auto-commits any modifications to models when the
            context manager exists, optional, defaults to True
        :param bool auto_rollback: Auto-rollbacks any modifications to models when the
            context manager raises an exception or failure, optional, defaults to True
        :param bool scoped: Instead of using a default session, use a scoped-session
            which is necessary for multi-threaded connections, optional,
            defaults to False
        :raises exc: Raises any thrown exceptions within the context manager if
            ``reraise`` is true
        :rtype: Generator[Session, None, None]
        """

        working_session: Session = self.session_maker()
        if scoped:
            working_session = scoped_session(self.session_maker)()

        try:
            yield working_session
            if auto_commit:
                working_session.commit()
        except Exception as exc:
            if auto_rollback:
                working_session.rollback()
            if reraise:
                raise exc
        finally:
            working_session.close()
