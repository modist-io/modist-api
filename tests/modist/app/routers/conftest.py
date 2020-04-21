# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains fixtures and utilities for API router tests."""

from typing import List, Optional, Generator
from contextlib import contextmanager

import rapidjson as json
from fastapi.testclient import TestClient

from modist.app.main import app
from modist.models.user import User
from modist.app.services.security import OAuth2Scopes

from ....constants import TEST_USER_PASSWORD

DEFAULT_SESSION_SCOPES = [OAuth2Scopes.ME]


@contextmanager
def request_client(
    user: User = None, scopes: List[str] = DEFAULT_SESSION_SCOPES
) -> Generator[TestClient, None, None]:
    """Generate a Request's client to use for testing.

    :param User user: The user to automatically authenticate for the yielded session, \
        optional, defaults to None
    :param List[str] scopes: The scopes the user should be authenticated with, \
        optional, defaults to DEFAULT_SESSION_SCOPES
    :raises ValueError: If the given user fails to generate an access token
    :return: A generator that yields a testing Request's session
    :rtype: Generator[TestClient, None, None]
    """

    client = TestClient(app=app)

    if user:
        token_response = client.post(
            "/oauth2/token",
            data={
                "username": user.display_name,
                "password": TEST_USER_PASSWORD,
                "scope": scopes,
            },
        )
        access_token: Optional[str] = json.loads(token_response.text).get(
            "access_token", None
        )
        if not access_token:
            raise ValueError(f"Failed to build testing access token for user {user!r}")

        client.headers.update({"Authorization": f"Bearer {access_token!s}"})

    yield client
