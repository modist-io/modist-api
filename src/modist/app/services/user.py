# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains service methods related to managing users."""

from uuid import UUID
from typing import List, Tuple, Optional
from datetime import datetime

import jwt
from fastapi import Depends, Security, HTTPException, status
from fastapi.security import SecurityScopes
from sqlalchemy.orm.exc import NoResultFound

from ...env import instance as env
from ..utils import get_db
from ...models.user import User
from ..schemas.user import UserSchema, UserMutationSchema
from ..services.security import (
    OAuth2Scopes,
    hash_password,
    oauth2_scheme,
    verify_password,
)


def get_user_by_id(user_id: UUID) -> Optional[UserSchema]:
    """Get a user by their ``id``.

    :param UUID user_id: The user's unique primary identifier
    :return: The discovered user if they exist
    :rtype: Optional[UserSchema]
    """

    with get_db().session() as session:
        user_model: Optional[User] = session.query(User).get(user_id)
        if not user_model:
            return None

        return UserSchema.from_model(user_model)


def get_user_by_email(user_email: str) -> Optional[UserSchema]:
    """Get a user by their ``email``.

    :param str user_email: The user's email address
    :return: The discovered user if a user with a matching ``email`` exists
    :rtype: Optional[UserSchema]
    """

    with get_db().session() as session:
        try:
            user_model: User = session.query(User).filter(
                User.email == user_email
            ).one()
        except NoResultFound:
            return None

        return UserSchema.from_model(user_model)


def get_user_by_display_name(user_display_name: str) -> Optional[UserSchema]:
    """Get a user by their ``display_name``.

    :param str user_display_name: The user's display name
    :return: The discovered user if a user with a matching ``display_name`` exists
    :rtype: Optional[UserSchema]
    """

    with get_db().session() as session:
        try:
            user_model: User = session.query(User).filter(
                User.display_name == user_display_name
            ).one()
        except NoResultFound:
            return None

        return UserSchema.from_model(user_model)


def get_user_by_login_identifier(user_login_identifier) -> Optional[UserSchema]:
    """Get a user by their login identifier.

    :param str user_login_identifier: The user's login identifier, either their \
        ``email`` or  ``display_name`` are valid inputs
    :return: The discovered user if they exist
    :rtype: Optional[UserSchema]
    """

    user = get_user_by_email(user_email=user_login_identifier)
    if not user:
        return get_user_by_display_name(user_display_name=user_login_identifier)

    return user


def get_users_hashed_password(user: UserSchema) -> Optional[str]:
    """Get a user's hashed password.

    Since we never include passwords in public schemas, one of the safer ways of dealing
    with referencing hashed passwords from user schemas is to simply have a quick query
    to only fetch the password when handling authentication. This reduces the number of
    times the hashed password needs to be sent over the network.

    :param UserSchema user: The user schema of the user whose password fetched
    :return: The discovered hashed password if it exists
    :rtype: Optional[str]
    """

    with get_db().session() as session:
        try:
            record: Tuple[str] = session.query(User.password).filter(
                User.id == user.id
            ).one()
        except NoResultFound:
            return None

        if len(record) <= 0:
            return None

        return record[0]


def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
) -> UserSchema:
    """Get the current authenticated user dependent on HTTP authorization.

    :param str token: The JWT token identifying the authenticated user, optional, \
        defaults to Depends(oauth2_scheme)
    :raises HTTPException: When the discovery of the authenticated user fails
    :return: The discovered active user for the current HTTP authorization
    :rtype: UserSchema
    """

    def _build_unauthorized_exception(detail: str) -> HTTPException:
        """Build the appropriate ``HTTPException`` if failures occur during fetching \
            the current user.

        :param str detail: The detail message included in the response
        :return: The appropriate ``HTTPException`` instance for the current context
        :rtype: HTTPException
        """
        authneticate_header: str = f"Bearer" + (
            f' scope="{security_scopes.scope_str!s}"' if security_scopes.scopes else ""
        )
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": authneticate_header},
        )

    try:
        jwt_payload = jwt.decode(
            jwt=token,
            key=env.app.security.secret,
            algorithms=[env.app.security.algorithm],
        )
        user_id: Optional[str] = jwt_payload.get("sub", None)
        if user_id is None:
            raise _build_unauthorized_exception(
                "Failed to discover user id from JWT payload"
            )

        user_scopes: List[str] = jwt_payload.get("scopes", [])

    except jwt.PyJWTError:  # type: ignore
        raise _build_unauthorized_exception("Failed to decode JWT payload")

    user = get_user_by_id(user_id=UUID(user_id))
    if user is None:
        raise _build_unauthorized_exception("Failed to get user by JWT identifier")

    for scope in security_scopes.scopes:
        if scope not in user_scopes:
            raise _build_unauthorized_exception(f"Missing necessary scope {scope!r}")

    return user


def get_current_active_user(
    current_user: UserSchema = Security(get_current_user, scopes=[OAuth2Scopes.ME]),
) -> UserSchema:
    """Get the current active user dependent on HTTP authorization.

    :param UserSchema current_user: The discovered current user, optional,defaults to \
        Depends(get_current_user)
    :raises HTTPException: When the user is flagged as inactive
    :return: The discovered active user for the current HTTP authorization
    :rtype: UserSchema
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {current_user.display_name!s} is not active",
        )

    return current_user


def get_current_verified_user(
    current_user: UserSchema = Security(
        get_current_active_user, scopes=[OAuth2Scopes.ME]
    ),
) -> UserSchema:
    """Get the current verified user dependent on HTTP authorization.

    :param UserSchema current_user: The discovered current active user, optional, \
        defaults to Depends(get_current_active_user)
    :raises HTTPException: When the user is not flagged as verified
    :return: The discovered verified user for the current HTTP authorization
    :rtype: UserSchema
    """

    if not current_user.verified_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {current_user.display_name!s} is not verified",
        )

    return current_user


def authenticate_user(user_identifier: str, user_password: str) -> Optional[UserSchema]:
    """Authenticate a given user.

    :param str user_identifier: The user login identifier, either their ``email`` or \
        ``display_name`` are valid inputs
    :param str user_password: The input user's password
    :return: The authenticated user if successfully authenticated
    :rtype: Optional[UserSchema]
    """

    user = get_user_by_login_identifier(user_login_identifier=user_identifier)
    if not user:
        return None

    hashed_password = get_users_hashed_password(user)
    if not hashed_password:
        return None

    if not verify_password(
        plain_password=user_password, hashed_password=hashed_password
    ):
        return None

    # mark user last authentication datetime
    with get_db().session() as session:
        session.query(User).filter(User.id == user.id).update(
            {User.authenticated_at: datetime.utcnow()}
        )

    return user


def create_user(user_data: UserMutationSchema) -> Optional[UserSchema]:
    """Create a new user.

    :param UserMutationSchema user_data: The new user's base data
    :return: The newly created user if successfully created
    :rtype: Optional[UserSchema]
    """

    with get_db().session() as session:
        user_model: User = User(
            email=user_data.email,
            password=hash_password(plain_password=user_data.password),
            display_name=user_data.display_name,
            is_anonymous=user_data.is_anonymous,
            born_on=user_data.born_on,
            given_name=user_data.given_name,
            family_name=user_data.family_name,
            bio=user_data.bio,
        )
        if user_data.preferences:
            user_model.preferences = user_data.preferences.dict()

        session.add(user_model)
        session.flush()

        return UserSchema.from_model(user_model)
