# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains utility methods for handling the environment context building."""

from attr._make import Attribute
from environ._environ_config import CNF_KEY


def build_environment_name(instance: object, attribute: Attribute) -> str:
    """Build the environment variable name given an instance and the attribute.

    Typically should be used by attribute validators to display what the expected
    environment variable name should be. You shouldn't try to implement your own
    environment variable loading logic as that is the main purpose of using a package
    like ``environ-config``.

    :param object instance: The config instance to utilize
    :param Attribute attribute: The attribute of the variable to use
    :return: The expected environment variable name
    :rtype: str
    """

    # if a custom name kwarg is given to the var, it will be stored in the
    # attribute metadata
    environment_name = attribute.metadata[CNF_KEY].name  # type: ignore

    # otherwise, we have to build it using the optional prefix from the instance
    if not isinstance(environment_name, str):
        try:
            environment_prefix = (
                instance._prefix.upper()  # type: ignore
                if isinstance(instance._prefix, str)  # type: ignore
                else ""
            )
        except AttributeError as exc:
            raise ValueError(
                "expected an instance of a 'environ.config' decorated class, "
                f"recieved {instance!r}"
            ) from exc

        environment_name = (
            f"{environment_prefix!s}_" if len(environment_prefix) > 0 else ""
        ) + attribute.name.upper()  # type: ignore

    return environment_name
