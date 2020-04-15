# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""
"""

from typing import Type, Union, Optional

from sqlalchemy import Column
from sqlalchemy.types import UnicodeText, TypeDecorator

try:
    from semver import VersionInfo
except ImportError:
    pass


class SemverType(TypeDecorator):
    """Custom SQLAlchemy type for Semver version details in Postgres.

    .. note:: This implementation is inspired from the integrations made by
        `sqlalchemy-utils <https://github.com/kvesteri/sqlalchemy-utils>`_ and follows
        their design for optinal imports and safe type resolution. That is why you see
        some uncommon checks against ``VersionInfo`` being defined in callables.

    """

    impl = UnicodeText

    @property
    def python_type(self) -> Type[VersionInfo]:
        """Define the resolved Python type of the SQLAlchemy column definition."""

        return VersionInfo

    def process_bind_param(
        self, value: Optional[Union[str, VersionInfo]], *args
    ) -> Optional[str]:
        """Cast the given Python data type into the SQLAlchemy column data type.

        .. note:: This value is optional in the case of nullable columns, and can
            potentially be a string in the case where ``VersionInfo`` is not importable.

        :param Optional[Union[str, VersionInfo]] value: The value to cast
        :return: The casted database data value
        :rtype: Optional[str]
        """

        if VersionInfo is not None and isinstance(value, VersionInfo):
            return str(value)

        if isinstance(value, str):
            return value

        return None

    def process_result_value(
        self, value: Optional[str], *args
    ) -> Optional[Union[str, VersionInfo]]:
        """Cast the given SQLAlchemy column data type into a desired Python data type.

        .. note:: This value is optional in the case of nullable columns.

        :param Optional[str] value: The database value to cast
        :return: The casted Python data value
        :rtype: Optional[Union[str, VersionInfo]]
        """

        if VersionInfo is None:
            return value

        if value is not None:
            return VersionInfo.parse(value)

        return None

    def _coerce(self, value: Optional[str]) -> Optional[Union[str, VersionInfo]]:
        """Coerce the given sample Python value into a desired Python data type.

        :param Optional[str] value: The Python value to cast
        :return: The casted desired Python data type value
        :rtype: Optional[Union[str, VersionInfo]]
        """

        if VersionInfo is None:
            return value

        if value is not None and not isinstance(value, VersionInfo):
            return VersionInfo.parse(value)

        return value
