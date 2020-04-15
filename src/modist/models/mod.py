# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Contains models related to mods."""

from uuid import UUID
from typing import List, Optional

from sqlalchemy import (
    Text,
    Column,
    String,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import association_proxy

from ..db import Database
from ._common import BaseModel
from ._mixins import TimestampMixin


class Mod(BaseModel):
    """The ORM representation for a mod."""

    __tablename__ = "mod"
    __table_args__ = (UniqueConstraint("user_id", "slug"),)

    slug: str = Column(String(length=128), nullable=False, unique=True)
    name: str = Column(String(length=64), nullable=False)
    description: Optional[str] = Column(Text)
    banner_image: Optional[str] = Column(String(length=255))
    avatar_image: Optional[str] = Column(String(length=255))
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )
    host_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("host.id", ondelete="cascade"),
        nullable=False,
    )
    category_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("category.id", ondelete="set null"),
        nullable=True,
    )
    age_restriction_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("age_restriction.id", ondelete="set null"),
        nullable=True,
        default=None,
    )

    user = relationship("User", back_populates="mods")
    host = relationship("Host", back_populates="mods")
    category = relationship("Category", back_populates="mods")
    age_restriction = relationship("AgeRestriction")
    mod_tags: List["ModTag"] = relationship("ModTag", back_populates="mod")

    tags = association_proxy("mod_tags", "tag")


class ModTag(Database.Entity, TimestampMixin):
    """The ORM model for tying mods to tags."""

    __tablename__ = "mod_tag"
    __table_args__ = (PrimaryKeyConstraint("mod_id", "tag_id"),)

    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    tag_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("tag.id", ondelete="cascade"),
        nullable=False,
    )

    mod: Mod = relationship("Mod", back_populates="mod_tags")
    tag = relationship("Tag")
