"""Define all our models for our storage layer.

These models construct the tables in our database.
"""

import datetime
from typing import List
import uuid

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String
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
    journals: Mapped[List["Journal"]] = relationship("Journal", back_populates="user")


class Journal(Base):
    __tablename__ = "journals"

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

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)

    # Journal Info
    title = Column(String, nullable=False)
    entry = Column(String, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="journals")
