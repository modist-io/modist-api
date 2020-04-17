# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains the main API application."""

from fastapi import FastAPI

from .. import __version__
from ..env import instance as env
from .routers import user, security

app = FastAPI(
    debug=env.app.debug,
    title="Modist",
    description=__version__.__description__,
    version=__version__.__version__,
)
app.include_router(security.router, prefix="/oauth2", tags=["Security"])
app.include_router(user.router, prefix="/users", tags=["Users"])
