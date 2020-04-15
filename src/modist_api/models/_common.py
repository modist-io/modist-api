# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains common functionality for inheriting database models."""

from ..db import Database
from ._mixins import IdMixin, IsActiveMixin, TimestampMixin


class BaseModel(Database.Entity, IdMixin, TimestampMixin, IsActiveMixin):
    """The base abstract model that all database serialized models should inherit from.

    This model comes pre-packaged with the ``IdMixin``, the ``TimestampMixin``, and the
    ``IsActiveMixin`` so inherited models shouldn't need to worry about providing
    primary UUID identifiers or ``created_at`` / ``updated_at`` timestamps or
    ``is_active`` boolean flags.
    """

    __abstract__ = True
