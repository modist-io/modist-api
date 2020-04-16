# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Contains models related to mods."""

from uuid import UUID
from typing import List, Optional
from datetime import datetime

from semver import VersionInfo
from sqlalchemy import (
    Text,
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    PrimaryKeyConstraint,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy_utils import IPAddressType
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.associationproxy import association_proxy

from ..db import Database
from ._types import SemverType
from ._common import BaseModel
from ._mixins import IdMixin, TimestampMixin


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
    mod_releases: List["ModRelease"] = relationship("ModRelease", back_populates="mod")
    mod_tags: List["ModTag"] = relationship("ModTag", back_populates="mod")
    mod_bans: List["ModBan"] = relationship("ModBan", back_populates="mod")
    mod_rankings: List["ModRanking"] = relationship("ModRanking", back_populates="mod")
    mod_ratings: List["ModRating"] = relationship("ModRating", back_populates="mod")
    mod_posts: List["ModPost"] = relationship("ModPost", back_populates="mod")
    mod_images: List["ModImage"] = relationship("ModImage", back_populates="mod")

    tags = association_proxy("mod_tags", "tag")
    bans = association_proxy("mod_bans", "ban")
    rankings = association_proxy("mod_rankings", "ranking")
    ratings = association_proxy("mod_ratings", "rating")
    posts = association_proxy("mod_posts", "post")
    images = association_proxy("mod_images", "image")


class ModRelease(BaseModel):
    """The ORM representation of a mod release."""

    __tablename__ = "mod_release"

    version: VersionInfo = Column(SemverType, nullable=False)
    description: Optional[str] = Column(Text)
    size: int = Column(Integer, nullable=False)
    checksum: str = Column(String(length=64), nullable=False)
    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    host_release_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("host_release.id", ondelete="cascade"),
        nullable=False,
    )

    mod: Mod = relationship("Mod", back_populates="mod_releases")
    host_release = relationship("HostRelease", back_populates="mod_releases")
    artifacts: List["ModReleaseArtifact"] = relationship(
        "ModReleaseArtifact", back_populates="mod_release"
    )
    release_dependencies: List["ModReleaseDependency"] = relationship(
        "ModReleaseDependency", back_populates="release"
    )
    release_conflicts: List["ModReleaseConflict"] = relationship(
        "ModReleaseConflict", back_populates="release"
    )

    dependencies = association_proxy("release_dependencies", "dependency")
    conflicts = association_proxy("release_conflicts", "conflict")


class ModReleaseArtifact(BaseModel):
    """The ORM representation of a mod release artifact."""

    __tablename__ = "mod_release_artifact"

    name: str = Column(Text, nullable=False)
    path: str = Column(Text, nullable=False)
    size: int = Column(Integer, nullable=False)
    mimetype: str = Column(Text, nullable=False, default="application/octet-stream")
    checksum: str = Column(String(length=64), nullable=False)
    mod_release_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod_release.id", ondelete="cascade"),
        nullable=False,
    )

    mod_release: ModRelease = relationship("ModRelease", back_populates="artifacts")


class ModReleaseDependency(Database.Entity, TimestampMixin):
    """The ORM representation of a mod release dependency."""

    __tablename__ = "mod_release_dependency"
    __table_args__ = (PrimaryKeyConstraint("mod_release_id", "mod_id"),)

    mod_release_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod_release.id", ondelete="cascade"),
        nullable=False,
    )
    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    version_expression: str = Column(Text, nullable=False)

    release: "ModRelease" = relationship(
        "ModRelease", back_populates="release_dependencies"
    )
    dependency: "Mod" = relationship("Mod")


class ModReleaseConflict(Database.Entity, TimestampMixin):
    """The ORM representation of a mod release conflict."""

    __tablename__ = "mod_release_conflict"
    __table_args__ = (PrimaryKeyConstraint("mod_release_id", "mod_id"),)

    mod_release_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod_release.id", ondelete="cascade"),
        nullable=False,
    )
    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    version_expression: str = Column(Text, nullable=False)

    release: "ModRelease" = relationship(
        "ModRelease", back_populates="release_conflicts"
    )
    conflict: "Mod" = relationship("Mod")


class ModReleaseDownload(Database.Entity, IdMixin, TimestampMixin):
    """The ORM representation of a mod release download."""

    __tablename__ = "mod_release_download"

    downloaded_at: datetime = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )
    ip: str = Column(postgresql.INET, nullable=False)
    headers: dict = Column(
        postgresql.JSONB, nullable=False, default={}, server_default=text("'{}'::jsonb")
    )
    mod_release_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod_release.id", ondelete="set null"),
        nullable=True,
    )
    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="set null"),
        nullable=True,
    )


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


class ModBan(Database.Entity, TimestampMixin):
    """The ORM model for tying mods to bans."""

    __tablename__ = "mod_ban"
    __table_args__ = (PrimaryKeyConstraint("mod_id", "ban_id"),)

    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    ban_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("ban.id", ondelete="cascade"),
        nullable=False,
    )

    mod: Mod = relationship("Mod", back_populates="mod_bans")
    ban = relationship("Ban")


class ModRanking(Database.Entity, TimestampMixin):
    """The ORM model for tying mods to user produced rankings."""

    __tablename__ = "mod_ranking"
    __table_args__ = (
        PrimaryKeyConstraint("mod_id", "ranking_id"),
        UniqueConstraint("mod_id", "user_id"),
    )

    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    ranking_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("ranking.id", ondelete="cascade"),
        nullable=False,
    )
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )

    mod: Mod = relationship("Mod", back_populates="mod_rankings")
    ranking = relationship("Ranking")
    user = relationship("User")


class ModRating(Database.Entity, TimestampMixin):
    """The ORM model for tying mods to user produced ratings."""

    __tablename__ = "mod_rating"
    __table_args__ = (
        PrimaryKeyConstraint("mod_id", "rating_id", "user_id"),
        UniqueConstraint("mod_id", "user_id", "version"),
    )

    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    rating_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("rating.id", ondelete="cascade"),
        nullable=False,
    )
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )
    version: VersionInfo = Column(SemverType, nullable=False)

    mod: Mod = relationship("Mod", back_populates="mod_ratings")
    rating = relationship("Rating")
    user = relationship("User")


class ModPost(Database.Entity, TimestampMixin):
    """The ORM model for tying mods to author produced posts."""

    __tablename__ = "mod_post"
    __table_args__ = (PrimaryKeyConstraint("mod_id", "post_id"),)

    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    post_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("post.id", ondelete="cascade"),
        nullable=False,
    )

    mod: Mod = relationship("Mod", back_populates="mod_posts")
    post = relationship("Post")


class ModImage(Database.Entity, TimestampMixin):
    """The ORM model for tying models to images."""

    __tablename__ = "mod_image"
    __table_args__ = (PrimaryKeyConstraint("mod_id", "image_id"),)

    mod_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("mod.id", ondelete="cascade"),
        nullable=False,
    )
    image_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("image.id", ondelete="cascade"),
        nullable=False,
    )

    mod: Mod = relationship("Mod", back_populates="mod_images")
    image = relationship("Image")
