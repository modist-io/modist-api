# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Contains miscellaneous common leaf models."""

import enum

from furl.furl import furl
from sqlalchemy import Enum, Column
from sqlalchemy_utils import URLType

from ._common import BaseModel


class SocialType(enum.Enum):
    """Enumeration of allowable social types."""

    GENERIC = "generic"
    TWITTER = "twitter"
    PATREON = "patreon"
    GITHUB = "github"


class Social(BaseModel):
    """The common social model for tying social related models to external URLs."""

    __tablename__ = "social"

    type: SocialType = Column(
        Enum(SocialType), nullable=False, default=SocialType.GENERIC
    )
    url: furl = Column(URLType, nullable=False)
