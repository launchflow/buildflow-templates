import datetime
import enum
from typing import List
import uuid
from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    # Autopoluated fields
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # User info
    google_id = Column(String, index=True, autoincrement=False)

    # Relationships
    chat_sessions: Mapped[List["ChatSession"]] = relationship(
        "ChatSession", back_populates="user"
    )


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    # Autopoluated fields
    id = Column(
        UUID(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    user: Mapped["User"] = relationship("User", back_populates="chat_sessions")
    chat_messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage", back_populates="chat_session"
    )


class ChatMessageUser(enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    message_content = Column(String, nullable=False)
    chat_user = Column(Enum(ChatMessageUser), nullable=False)
    chat_session_id = Column(
        UUID(as_uuid=True), ForeignKey("chat_sessions.id"), index=True
    )

    chat_session: Mapped["ChatSession"] = relationship(
        "ChatSession", back_populates="chat_messages"
    )
