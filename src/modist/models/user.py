# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains user related SQLAlchemy models."""

from uuid import UUID
from typing import Optional
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
from sqlalchemy.ext.associationproxy import association_proxy

from ..db import Database
from ._common import BaseModel
from ._mixins import TimestampMixin


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
    avatar_image: Optional[str] = Column(String(length=255))
    status_emoji: Optional[str] = Column(String(length=255))
    status: Optional[str] = Column(String(length=128))
    preferences: dict = Column(
        postgresql.JSONB,
        nullable=False,
        default={},
        server_default=text("'{}'::jsonb"),
    )

    mods = relationship("Mod", back_populates="user")
    user_bans = relationship("Ban", back_populates="user")

    bans = association_proxy("user_bans", "ban")


class UserBan(Database.Entity, TimestampMixin):
    """The ORM model for tying users to bans."""

    __tablename__ = "user_ban"
    __table_args__ = (PrimaryKeyConstraint("user_id", "ban_id"),)

    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )
    ban_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("ban.id", ondelete="cascade"),
        nullable=False,
    )

    user: User = relationship("User", back_populates="user_bans")
    ban = relationship("Ban")
