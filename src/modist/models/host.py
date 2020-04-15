# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Contains host related SQLAlchemy models."""

from uuid import UUID
from typing import List, Optional
from datetime import datetime

from sqlalchemy import (
    Text,
    Column,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import association_proxy

from ..db import Database
from ._types import SemverType
from .common import Social
from ._common import BaseModel
from ._mixins import TimestampMixin


class HostPublisherSocial(Database.Entity, TimestampMixin):
    """The ORM association model for m2m relationships between host publisher and social.

    This model is specifically not an subclass of the base model as we do not want
    the ``IdMixin`` applied to this association table. The proper primary key
    identification should be between the ``host_publisher_id`` and the ``social_id``.
    """

    __tablename__ = "host_publisher_social"
    __table_args__ = (PrimaryKeyConstraint("host_publisher_id", "social_id"),)

    host_publisher_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("host_publisher.id", ondelete="cascade"),
        nullable=False,
    )
    social_id: UUID = Column(
        postgresql.UUID(as_uuid=True), ForeignKey("social.id"), nullable=True
    )

    # NOTE: we only care about the backref to the ``host_publisher`` model as the
    # ``social``` model is a mutli-many leaf table
    social: Social = relationship("Social")
    host_publisher: "HostPublisher" = relationship(
        "HostPublisher", back_populates="host_publisher_socials"
    )


class HostPublisher(BaseModel):
    """The ORM model representation of a host publisher."""

    __tablename__ = "host_publisher"

    slug: str = Column(String(length=128), nullable=False, unique=True)
    name: str = Column(String(length=64), nullable=False)
    description: Optional[str] = Column(Text)
    banner_image: Optional[str] = Column(String(length=255))
    avatar_image: Optional[str] = Column(String(length=255))

    hosts: List["Host"] = relationship("Host", back_populates="publisher")
    host_publisher_socials: List[HostPublisherSocial] = relationship(
        "HostPublisherSocial", back_populates="host_publisher"
    )
    socials: List[Social] = association_proxy("host_publisher_socials", "social")


class Host(BaseModel):
    """The ORM model representation of a host."""

    __tablename__ = "host"

    slug: str = Column(String(length=128), nullable=False, unique=True)
    name: str = Column(String(length=64), nullable=False)
    description: Optional[str] = Column(Text)
    banner_image: Optional[str] = Column(String(length=255))
    avatar_image: Optional[str] = Column(String(length=255))
    host_publisher_id: UUID = Column(
        postgresql.UUID(as_uuid=True), ForeignKey("host_publisher.id"), nullable=False
    )

    publisher: HostPublisher = relationship("HostPublisher", back_populates="hosts")
    releases: List["HostRelease"] = relationship("HostRelease", back_populates="host")


class HostRelease(BaseModel):
    """The ORM model representation of a host release."""

    __tablename__ = "host_release"
    __table_args__ = (UniqueConstraint("host_id", "version"),)

    released_at: Optional[datetime] = Column(DateTime(timezone=True), default=None)
    version: str = Column(SemverType, nullable=False)
    description: Optional[str] = Column(Text)
    host_id: UUID = Column(
        postgresql.UUID(as_uuid=True), ForeignKey("host.id"), nullable=False
    )

    host: Host = relationship("Host", back_populates="releases")
