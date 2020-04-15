# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Contains miscellaneous common leaf models."""

import enum
from uuid import UUID
from typing import List, Optional
from datetime import datetime

from furl.furl import furl
from sqlalchemy import (
    Enum,
    Text,
    Column,
    String,
    Boolean,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import URLType
from sqlalchemy.dialects import postgresql

from ..db import Database
from ._common import BaseModel
from ._mixins import IsActiveMixin, TimestampMixin


class SocialType(enum.Enum):
    """Enumeration of allowable social types."""

    GENERIC = "generic"
    TWITTER = "twitter"
    PATREON = "patreon"
    GITHUB = "github"


class CategoryType(enum.Enum):
    """Enumeration of allowable category types."""

    MOD = "mod"


class Social(BaseModel):
    """The common social model for tying social related models to external URLs."""

    __tablename__ = "social"
    __table_args__ = (UniqueConstraint("type", "url"),)

    type: SocialType = Column(
        Enum(SocialType), nullable=False, default=SocialType.GENERIC
    )
    url: furl = Column(URLType, nullable=False)


class Category(Database.Entity, TimestampMixin, IsActiveMixin):
    """The ORM representation for a generic category.

    .. note:: This table is self-related on ``parent_id`` and should have the
        ``refresh_depth_and_lineage`` trigger associated to inserts and updates so the
        logic for dealing with updating ``depth`` and ``lineage`` fields lives within
        the database rather than some one-off script in the model. You should only ever
        be concerned with updating the ``parent_id``, and ``depth`` and ``lineage``
        should refresh themselves.

    .. note:: Because this table is self-relational and needs both ``parent`` and
        ``children`` relationships, we must avoid defining the ``id`` column with
        inheritance. Without a direct column definition for ``remote_side`` in the
        below relationships, we cannot resolve the mapping for the self-relation.
        For this reason we define the model manually without using the abstracted
        ``BaseModel`` class.

    """

    __tablename__ = "category"
    __table_args__ = (UniqueConstraint("parent_id", "name", "type"),)

    id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        server_default=text("uuid_generate_v4()"),
        primary_key=True,
    )
    parent_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("category.id", ondelete="cascade"),
        nullable=True,
        default=None,
    )
    type: CategoryType = Column(
        Enum(CategoryType), nullable=False, default=CategoryType.MOD
    )
    name: str = Column(String(64), nullable=False)
    description: str = Column(Text)
    depth: int = Column(Integer, nullable=False, default=0, server_default="0")
    lineage: List[UUID] = Column(
        postgresql.ARRAY(postgresql.UUID(as_uuid=True)),
        nullable=False,
        default=[],
        server_default="{}",
    )

    mods = relationship("Mod", back_populates="category")


class AgeRestriction(BaseModel):
    """The common age restriciton model for flagging age restricted content."""

    __tablename__ = "age_restriction"

    name: str = Column(String(length=64), nullable=False)
    description: str = Column(Text, nullable=False)
    avatar_image: str = Column(String(length=255))
    minimum_age: int = Column(Integer, nullable=False)


class Tag(BaseModel):
    """The common tag model for content tags."""

    __tablename__ = "tag"

    name: str = Column(String(length=64), nullable=False)
    description: Optional[str] = Column(Text)


class Ban(BaseModel):
    """The common ban model for registering content bans."""

    __tablename__ = "ban"

    is_permanent: bool = Column(Boolean, default=False, server_default="false")
    released_at: datetime = Column(DateTime)
    reason: str = Column(Text, nullable=False)


class Notification(BaseModel):
    """The common notification model for distributing notifications to users."""

    __tablename__ = "notification"

    title: str = Column(String(length=64), nullable=False)
    content: str = Column(Text, nullable=False)
    priority: int = Column(Integer, default=0)
