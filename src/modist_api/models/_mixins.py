# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains miscellaneous mixins for database models."""

from uuid import UUID
from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime, func, text
from sqlalchemy.dialects import postgresql


class IdMixin(object):
    """A ORM model mixin for the default auto-generated UUID id column."""

    id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        server_default=text("uuid_generate_v4()"),
        primary_key=True,
    )


class TimestampMixin(object):
    """An ORM model mixin for auto-generated ``created_at`` and ``updated_at`` timestamps.

    .. note::
        In order for ``updated_at`` to be auto-update outside of the ORM functionality,
        we need to establish a trigger on the table. This functionality is already
        provided by the Alembic operations using the
        ``create_refresh_updated_at_trigger`` and ``drop_refresh_updated_at_trigger``
        methods. Please ensure that in the migrations these methods are invoked after
        creation and before removal respectively.

    """

    created_at: datetime = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        nullable=False,
        onupdate=func.now(),
        server_default=func.now(),
    )


class IsActiveMixin(object):
    """An ORM model mixin for ``is_active`` boolean flag.

    This flag is typically used by many models to provide a quick method of deactivating
    a record for any number of reasons. The flag defaults to ``true`` and should likely
    never be overriden as defaulting to ``false``. If you need something that indicates
    whether something is *visible* in the API or front-end, try to utilize a custom
    timestamp field instead. This field should be used for database management or
    content moderation purposes.
    """

    is_active: bool = Column(
        Boolean, nullable=False, default=True, server_default="true"
    )
