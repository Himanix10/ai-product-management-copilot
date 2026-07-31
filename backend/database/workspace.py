from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    documents = relationship(
        "UploadedDocument",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )
    feedbacks = relationship(
        "Feedback",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )
    chat_history = relationship(
        "ChatHistory",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )
