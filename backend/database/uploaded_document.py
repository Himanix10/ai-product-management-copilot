from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id = Column(Integer, primary_key=True, index=True)

    workspace_id = Column(
        Integer,
        ForeignKey("workspaces.id"),
        nullable=False,
        index=True,
    )

    file_name = Column(String, nullable=False, index=True)
    file_type = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    workspace = relationship("Workspace", back_populates="documents")
    feedbacks = relationship(
        "Feedback",
        back_populates="document",
        cascade="all, delete-orphan",
    )
