# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains schemas related to security routes and services."""

from typing import List

from pydantic import BaseModel


class JWTPayloadSchema(BaseModel):
    """Describes the JWT payload structure."""

    sub: str
    exp: int
    iat: int
    scopes: List[str]
    display_name: str


class TokenSchema(BaseModel):
    """Describes the OAuth2 token payload structure."""

    access_token: str
    token_type: str
