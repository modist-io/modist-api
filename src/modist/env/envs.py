# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the environment groups and contexts to use throughout the application."""

from enum import Enum

from environ import var, group, config, bool_var


class Environment(Enum):
    """The valid environment names to be respected throughout the Modist platform."""

    TEST = "test"
    DEBUG = "debug"
    PRODUCTION = "production"


@config(prefix="DATABASE")
class DatabaseEnv(object):
    """The environment variables to define and control the database."""

    url: str = var()
    echo: bool = bool_var(default=False)


@config(prefix="APP")
class AppEnv(object):
    """The environment variables to define and control the application."""

    @config(prefix="SECURITY")
    class SecurityEnv(object):
        """The environment variables related to application security."""

        secret: str = var()
        algorithm: str = var(default="HS256")
        access_token_ttl: int = var(default=86400, converter=int)

    security: SecurityEnv = group(SecurityEnv)
    debug: bool = bool_var(default=False)


@config(prefix="")
class BaseEnv(object):
    """The environment variables required for the Modist platform.

    .. note:: Includes all other required environment classes for the Modist platform.
    """

    env: Environment = var(default=Environment.DEBUG, converter=Environment)
    database: DatabaseEnv = group(DatabaseEnv)
    app: AppEnv = group(AppEnv)
