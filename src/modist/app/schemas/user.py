# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains schemas related to user routes and services."""

import re
from uuid import UUID
from typing import Optional
from datetime import date, datetime

from pydantic import EmailStr, BaseModel, validator, validate_email

from ...models.user import User

DISPLAY_NAME_PATTERN = re.compile(r"^[a-zA-Z0-9]+(?:[-_.]*[a-zA-Z0-9])+$")


class UserPreferencesSchema(BaseModel):
    """Describes the available user preferences."""

    show_nsfw: bool = False


class UserMutationSchema(BaseModel):
    """Describes the mutation structure for as user."""

    email: EmailStr
    display_name: str
    password: str
    is_anonymous: Optional[bool]
    born_on: Optional[date]
    given_name: Optional[str]
    family_name: Optional[str]
    bio: Optional[str]
    preferences: Optional[UserPreferencesSchema]

    @validator("display_name")
    def _validate_display_name(cls, display_name: str) -> str:  # noqa
        """Validate that the given display name matches the defined regex pattern.

        :param str display_name: The user's display name
        :raises ValueError: If the given display name does not match the pattern
        :return: The user's display name
        :rtype: str
        """

        if not DISPLAY_NAME_PATTERN.match(display_name):
            raise ValueError(f"invalid display name")
        return display_name


class UserSchema(BaseModel):
    """Describes a user."""

    id: UUID
    email: EmailStr
    display_name: str
    is_active: bool
    is_anonymous: bool
    verified_at: Optional[datetime]
    authenticated_at: Optional[datetime]
    born_on: Optional[date]
    given_name: Optional[str]
    family_name: Optional[str]
    bio: Optional[str]
    preferences: UserPreferencesSchema

    @classmethod
    def from_model(cls, model: User) -> "UserSchema":
        """Create an instance of the schema from the related user model.

        :param User user: The user model representation of the user
        """

        return cls(
            id=str(model.id),
            email=model.email,
            display_name=model.display_name,
            is_active=model.is_active,
            is_anonymous=model.is_anonymous,
            verified_at=model.verified_at,
            authenticated_at=model.authenticated_at,
            born_on=model.born_on,
            given_name=model.given_name,
            family_name=model.family_name,
            bio=model.bio,
            preferences=model.preferences,
        )
