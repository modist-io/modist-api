# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains all related user model factories."""

from factory import Faker
from factory.alchemy import SQLAlchemyModelFactory

from modist.models.user import User
from modist.app.services.security import hash_password

from ._common import SQLALCHEMY_SESSION
from ..constants import TEST_USER_PASSWORD


class UserFactory(SQLAlchemyModelFactory):
    """Build a testing user model instance."""

    class Meta:
        model = User
        sqlalchemy_session = SQLALCHEMY_SESSION
        sqlalchemy_session_persistence = "flush"

    verified_at = Faker("date_time")
    born_on = Faker("date")
    is_anonymous = Faker("boolean")
    email = Faker("email")
    password = hash_password(TEST_USER_PASSWORD)
    given_name = Faker("first_name")
    family_name = Faker("last_name")
    display_name = Faker("user_name")
    bio = Faker("paragraph")
