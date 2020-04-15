# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Contains models related to mods."""

from uuid import UUID
from typing import Optional

from sqlalchemy import Text, Column, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from ._common import BaseModel


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
