# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains user related SQLAlchemy models."""

from uuid import UUID
from typing import List, Optional
from datetime import date, datetime

from sqlalchemy import (
    Date,
    Text,
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from sqlalchemy.dialects import postgresql

from ._common import BaseModel


class User(BaseModel):
    """The ORM model representation of a user."""

    __tablename__ = "user"

    verified_at: Optional[datetime] = Column(DateTime(timezone=True), default=None)
    authenticated_at: Optional[datetime] = Column(DateTime(timezone=True), default=None)
    born_on: Optional[date] = Column(Date, default=None)
    is_anonymous: bool = Column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    email: str = Column(EmailType(length=255), nullable=False, unique=True)
    given_name: Optional[str] = Column(String(length=64))
    family_name: Optional[str] = Column(String(length=64))
    display_name: str = Column(String(length=64), nullable=False, unique=True)
    bio: Optional[str] = Column(Text)
    avatar_image: Optional[str] = Column(String(length=64))
    status_emoji: Optional[str] = Column(String(length=64))
    status: Optional[str] = Column(String(length=128))
    preferences: dict = Column(
        postgresql.JSONB,
        nullable=False,
        default={},
        server_default=text("'{}'::jsonb"),
    )
