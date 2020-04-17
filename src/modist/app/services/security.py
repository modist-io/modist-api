# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains services related to authentication and security."""

from enum import Enum
from typing import List, Optional
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, Security, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import SecurityScopes, OAuth2PasswordBearer

from ...env import instance as env
from ..schemas.user import UserSchema
from ..schemas.security import JWTPayloadSchema


class OAuth2Scopes(object):
    """Aggregates the available scopes into an enum-like referenceable object.

    .. note:: We are specifically avoiding using an Enum in this case since we want
        to avoid the consistent usage of ``.value`` when utilizing scopes in routes
        and in service methods.

    """

    ME = "me"


oauth2_scopes = {OAuth2Scopes.ME: "Read information about the current user."}
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/oauth2/token", scopes=oauth2_scopes)
crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password matches a given hashed password with the current \
        cryptography context.

    :param str plain_password: The plaintext password to compare
    :param str hashed_password: The hashed password to compare
    :return: True if passwords match, otherwise False
    :rtype: bool
    """

    return crypt_context.verify(plain_password, hashed_password)


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password with the current cryptography context.

    :param str plain_password: The plaintext password to hash
    :return: The hashed password
    :rtype: str
    """

    return crypt_context.hash(plain_password)


def build_access_token(
    *,
    user: UserSchema,
    scopes: Optional[List[str]] = None,
    expires_delta: Optional[timedelta] = None,
) -> bytes:
    """Produce a JWT access token for a given user that is viable for a given time delta.

    :param UserSchema user: The user to build an access token for
    :param Optional[timedelta] expires_delta: The time delta that the generated JWT \
        token is open for, optional, defaults to None
    :return: The encoded JWT token in bytes
    :rtype: bytes
    """

    now = datetime.utcnow()
    expires_at: datetime = now + (
        expires_delta
        if expires_delta
        else timedelta(seconds=env.app.security.access_token_ttl)
    )
    payload = JWTPayloadSchema(
        sub=str(user.id),
        exp=datetime.timestamp(expires_at),
        iat=datetime.timestamp(now),
        scopes=scopes or [],
        display_name=user.display_name,
    )

    return jwt.encode(
        payload=payload.dict(),
        key=env.app.security.secret,
        algorithm=env.app.security.algorithm,
    )
