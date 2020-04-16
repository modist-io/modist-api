# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Modist Team <admin@modist.io>
# ISC License <https://choosealicense.com/licenses/isc>

"""Contains user related SQLAlchemy models."""

import enum
from uuid import UUID
from typing import List, Optional
from datetime import date, datetime

from sqlalchemy import (
    Date,
    Enum,
    Text,
    Column,
    String,
    Boolean,
    Integer,
    Numeric,
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
from ._mixins import IsActiveMixin, TimestampMixin


class RatingType(enum.Enum):
    """Enumeration of allowable rating types."""

    MOD = "mod"


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
    sent_messages: List["Message"] = relationship("Message", back_populates="user")
    received_user_messages: List["UserMessage"] = relationship(
        "UserMessage", back_populates="user"
    )
    received_user_notifications: List["UserNotification"] = relationship(
        "UserNotification", back_populates="user"
    )
    user_socials: List["UserSocial"] = relationship("UserSocial", back_populates="user")

    bans = association_proxy("user_bans", "ban")
    received_messages = association_proxy("received_user_messages", "message")
    notifications = association_proxy("recieved_user_notifications", "notification")
    socials = association_proxy("user_socials", "social")


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


class Message(BaseModel):
    """The user message model for authored messages.

    .. note:: Although this model seems like it should be present in ``.common``, this
        is not a leaf table. Because of it's dependency on the user author relationship,
        this model is part of the user namespace.

    """

    __tablename__ = "message"

    sent_at: Optional[datetime] = Column(DateTime)
    received_at: Optional[datetime] = Column(DateTime)
    read_at: Optional[datetime] = Column(DateTime)
    content: str = Column(Text, nullable=False)
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )

    user: User = relationship("User", back_populates="sent_messages")


class Post(BaseModel):
    """The user post model for posted content."""

    __tablename__ = "post"

    published_at: datetime = Column(DateTime(timezone=True), nullable=True)
    title: str = Column(String(length=255), nullable=False)
    content: str = Column(Text, nullable=False)
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )

    user: User = relationship("User")


class Ranking(BaseModel):
    """The common ranking model for ranking generic content."""

    __tablename__ = "ranking"

    rank: int = Column(Integer, nullable=False)
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )

    user: User = relationship("User")


class Comment(Database.Entity, TimestampMixin, IsActiveMixin):
    """The common comment model for commenting on generic content."""

    __tablename__ = "comment"

    id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        server_default=text("uuid_generate_v4()"),
        primary_key=True,
    )
    parent_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("comment.id", ondelete="cascade"),
        nullable=True,
        default=None,
    )
    content: str = Column(Text, nullable=False)
    depth: int = Column(Integer, nullable=False, default=0, server_default="0")
    lineage: List[UUID] = Column(
        postgresql.ARRAY(postgresql.UUID(as_uuid=True)),
        nullable=False,
        default=[],
        server_default="{}",
    )
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )

    parent = relationship("Comment")
    user: User = relationship("User")
    comment_rankings: List["CommentRanking"] = relationship(
        "CommentRanking", back_populates="comment"
    )

    rankings = association_proxy("comment_rankings", "ranking")


class Rating(BaseModel):
    """The common content model for rating generic content."""

    __tablename__ = "rating"

    type: RatingType = Column(Enum(RatingType), nullable=False, default=RatingType.MOD)
    rating: float = Column(Numeric(precision=3, scale=2), nullable=False)
    content: str = Column(Text, nullable=False)
    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )

    user: User = relationship("User")


class UserMessage(Database.Entity, TimestampMixin):
    """The ORM association model for m2m realtionships between users and messages."""

    __tablename__ = "user_message"
    __table_args__ = (PrimaryKeyConstraint("user_id", "message_id"),)

    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )
    message_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("message.id", ondelete="cascade"),
        nullable=False,
    )

    user: User = relationship("User", back_populates="received_user_messages")
    message: Message = relationship("Message")


class UserNotification(Database.Entity, TimestampMixin):
    """The ORM association model for m2m relationships between users and notifys."""

    __tablename__ = "user_notification"
    __table_args__ = (PrimaryKeyConstraint("user_id", "notification_id"),)

    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )
    notification_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("notification.id", ondelete="cascade"),
        nullable=False,
    )

    user: User = relationship("User", back_populates="received_user_notifications")
    notification = relationship("Notification")


class UserSocial(Database.Entity, TimestampMixin):
    """The ORM association model for m2m relationships between user and social.

    This model is specifically not an subclass of the base model as we do not want
    the ``IdMixin`` applied to this association table. The proper primary key
    identification should be between the ``user_id`` and the ``social_id``.
    """

    __tablename__ = "user_social"
    __table_args__ = (PrimaryKeyConstraint("user_id", "social_id"),)

    user_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="cascade"),
        nullable=False,
    )
    social_id: UUID = Column(
        postgresql.UUID(as_uuid=True), ForeignKey("social.id"), nullable=True
    )

    # NOTE: we only care about the backref to the ``user`` model as the
    # ``social``` model is a mutli-many leaf table
    social = relationship("Social")
    user: User = relationship("User", back_populates="user_socials")


class CommentRanking(Database.Entity, TimestampMixin):
    """The ORM association model for m2m relationships between comments and rankings."""

    __tablename__ = "comment_ranking"
    __table_args__ = (PrimaryKeyConstraint("comment_id", "ranking_id"),)

    comment_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("comment.id", ondelete="cascade"),
        nullable=False,
    )
    ranking_id: UUID = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("ranking.id", ondelete="cascade"),
        nullable=False,
    )

    comment: Comment = relationship("Comment", back_populates="comment_rankings")
    ranking = relationship("Ranking")
