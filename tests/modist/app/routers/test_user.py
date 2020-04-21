# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

import pytest
import rapidjson as json
from sqlalchemy.orm import Session

from modist.models.user import User
from modist.app.schemas.user import UserSchema

from .conftest import request_client


@pytest.mark.db
def test_get_me_fails_for_unauthenticated_clients():
    with request_client() as client:
        resp = client.get("/users/me")
        assert resp.status_code == 401


@pytest.mark.db
def test_get_me_fails_for_access_tokens_missing_necessary_scopes(user_instance: User):
    with request_client(user_instance, scopes=[]) as client:
        resp = client.get("/users/me")
        assert resp.status_code == 401


@pytest.mark.db
def test_get_me(db_session: Session, user_instance: User):
    with request_client(user_instance) as client:
        resp = client.get("/users/me")
        assert resp.status_code == 200

        schema = UserSchema(**json.loads(resp.text))

        # NOTE: because the user instance retrieved from the client has been
        # authenticated, the ``authenticated_at`` field will be set to a specific
        # datetime while the original User model instance will not yet have the explicit
        # datetime set by the user authentication service. So we will always need to
        # refresh the model instance in order for the two schemas to be equivalent
        db_session.refresh(user_instance)

        # NOTE: because we are refreshing the model instance directly from the database,
        # SQLAlchemy will try to be clever and include the ``tzinfo`` for datetimes.
        # These must be nullified in order for the ISO-8601 datetimes returned in the
        # result schema to be equivalent
        for field_name in (
            "authenticated_at",
            "verified_at",
        ):
            setattr(
                user_instance,
                field_name,
                getattr(user_instance, field_name).replace(tzinfo=None),
            )

        assert UserSchema.from_model(user_instance) == schema
