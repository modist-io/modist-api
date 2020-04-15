# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Contains host related SQLAlchemy models."""

from uuid import UUID
from typing import List, Optional

from sqlalchemy import Text, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql

from ._common import BaseModel


class HostPublisher(BaseModel):
    """The ORM model representation of a host publisher."""

    __tablename__ = "host_publisher"

    slug: str = Column(String(length=128), nullable=False, unique=True)
    name: str = Column(String(length=64), nullable=False)
    description: Optional[str] = Column(Text)
    banner_image: Optional[str] = Column(String(length=255))
    avatar_image: Optional[str] = Column(String(length=255))

    hosts: List["Host"] = relationship("Host", back_populates="publisher")


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
