# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Contains host related SQLAlchemy models."""

from typing import Optional

from sqlalchemy import Text, Column, String

from ._common import BaseModel


class HostPublisher(BaseModel):
    """The ORM model representation of a host publisher."""

    __tablename__ = "host_publisher"

    slug: str = Column(String(length=128), nullable=False, unique=True)
    name: str = Column(String(length=64), nullable=False)
    description: Optional[str] = Column(Text)
    banner_image: Optional[str] = Column(String(length=255))
    avatar_image: Optional[str] = Column(String(length=255))
