from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class Theme(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True, index=True)

    feedback_id = Column(
        Integer,
        ForeignKey("feedbacks.id"),
        nullable=False,
        index=True,
    )
    cluster_id = Column(
        Integer,
        ForeignKey("clusters.id"),
        nullable=True,
        index=True,
    )

    theme_name = Column(String, nullable=False, index=True)
    sentiment = Column(String, index=True)
    confidence = Column(Float, index=True)

    pain_point = Column(String)
    intent = Column(String)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    feedback = relationship("Feedback", back_populates="themes")
    cluster = relationship("Cluster", back_populates="themes")
