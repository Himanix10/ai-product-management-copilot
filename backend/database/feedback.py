from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)

    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    document_id = Column(
        Integer,
        ForeignKey("uploaded_documents.id"),
        nullable=False,
        index=True,
    )

    title = Column(String)
    content = Column(Text, nullable=False)

    source = Column(String, index=True)
    customer = Column(String, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    workspace = relationship("Workspace", back_populates="feedbacks")
    document = relationship("UploadedDocument", back_populates="feedbacks")
    themes = relationship(
        "Theme",
        back_populates="feedback",
        cascade="all, delete-orphan",
    )
