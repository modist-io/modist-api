# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the application's security router and views."""

from datetime import datetime, timedelta

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ...env import instance as env
from ..services.user import authenticate_user
from ..schemas.security import TokenSchema
from ..services.security import build_access_token

router = APIRouter()


@router.post("/token", response_model=TokenSchema)
def access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenSchema:
    """Build an access token for a user's given form credentials."""

    user = authenticate_user(
        user_identifier=form_data.username, user_password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login credentials",
            headers={"WWW-Authorization": "Bearer"},
        )
    return TokenSchema(
        access_token=build_access_token(
            user=user,
            scopes=form_data.scopes,
            expires_delta=timedelta(seconds=env.app.security.access_token_ttl),
        ),
        token_type="bearer",
    )
