from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .db import Base


class Priority(Base):
    __tablename__ = "priorities"

    id = Column(Integer, primary_key=True, index=True)

    cluster_id = Column(
        Integer,
        ForeignKey("clusters.id"),
        nullable=False,
        index=True,
    )

    rice_score = Column(Float)
    ice_score = Column(Float)
    reach = Column(Integer)
    impact = Column(Float)
    confidence = Column(Float)
    effort = Column(Float)
    risk = Column(String)

    priority_level = Column(String, index=True)
    scoring_method = Column(String, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    cluster = relationship("Cluster", back_populates="priorities")
    prds = relationship(
        "PRD",
        back_populates="priority",
        cascade="all, delete-orphan",
    )
