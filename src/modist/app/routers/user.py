# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the application's user router and views."""

from typing import Optional

from fastapi import Depends, APIRouter

from ..schemas.user import UserSchema, UserMutationSchema
from ..services.user import create_user, get_current_active_user

router = APIRouter()


@router.get("/me", response_model=UserSchema)
def get_me(current_user: UserSchema = Depends(get_current_active_user)) -> UserSchema:
    """Fetch the current active user's data."""

    return current_user


@router.post("/", response_model=UserSchema)
def post_user(user_data: UserMutationSchema) -> Optional[UserSchema]:
    """Create a new user."""

    return create_user(user_data)
