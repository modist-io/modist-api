# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Provides a default environment instance for usage throughout the platform.

Assuming the following environment:

>>> import os
>>> os.environ["SENTRY_ENABLED"] = "True"
>>> os.environ["SENTRY_DSN"] = "testing-dsn"

You can access the loaded variables using :class:`.envs.SentryEnv` instance attached
to the exported ``instance`` variable:

>>> from envrionment import instance as env
>>> env.sentry.is_enabled
True
>>> env.sentry.dsn
'testing-dsn'
"""

import os
from typing import Type, Union, TypeVar, Optional, cast

import environ

from .envs import BaseEnv
from .exceptions import MissingEnvValueError

__all__ = ["get_environment", "instance", "MissingEnvValueError"]

# generic environment type placeholder for typing signatures
Environment_T = TypeVar("Environment_T")


def get_environment(
    environment_class: Optional[Type[Environment_T]] = None,
    environment_dict: Union[dict, os._Environ] = os.environ,
) -> Environment_T:
    """Get the environment class instance of a given ``environment_class``.

    .. note:: If no ``environment_class`` is given, this method will default to the
        common :class:`.envs.BaseEnv` class. So calls to :func:`get_environment` will
        result in an instance of :class:`.envs.BaseEnv`.

    To get the default environment instance you can simply call this method.
    For example:

    >>> env = get_environment()
    >>> env.sentry.is_enabled
    True
    >>> env.sentry.dsn
    <SENTRY_DSN>

    You can also retreive a specific environment by calling this method with that
    specific ``environment_class``:

    >>> from environment.sentry import SentryEnvironment
    >>> sentry_env = get_environment(SentryEnvironment)
    >>> sentry_env.is_enabled
    True
    >>> sentry_env.dsn
    <SENTRY_DSN>

    :param Optional[Type[Environment_T]] environment_class: The ``environ.config``
        decorated class to build an instance of, optional, defaults to None
    :param Union[dict, os._Environ] environment_dict: The environment dictionary to use
        when building the ``environment_class`` instance, optional,
        defaults to ``os.environ``
    :return: An instance of an ``environ.config`` decorated class
    """

    def load_environment(environment_class: Type[Environment_T]) -> Environment_T:
        """Load an environment and raises :class:`~.exceptions.MissingEnvValueError` exceptions.

        :param Type[Environment_T] environment_class: The environment to load
        :raises MissingEnvValueError: If required environment variables are missing
        :return: An instance of the given ``environment_class``
        :rtype: Environment_T
        """

        try:
            return environ.to_config(environment_class, environ=environment_dict)
        except environ.exceptions.MissingEnvValueError as exc:
            # NOTE: this seems wrong and un-pythonic, but we left this here to allow for
            # future error reporting to accurately capture the state of when
            # (during runtime) environment variable loading failures occur

            raise exc

    if not environment_class:
        # NOTE: we are type-casting the hard-coded `BaseEnv` to match the
        # generic `Type[Environment_T]` as indicated by the method signature
        return load_environment(cast(Type[Environment_T], BaseEnv))

    return load_environment(environment_class)


# a module-level instance of the BaseEnv to simplify usage in the apps
instance: BaseEnv = get_environment(BaseEnv)
