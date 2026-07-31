from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class Cluster(Base):
    __tablename__ = "clusters"

    id = Column(Integer, primary_key=True, index=True)
    cluster_name = Column(String, nullable=False, index=True)
    summary = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    themes = relationship("Theme", back_populates="cluster")
    priorities = relationship(
        "Priority",
        back_populates="cluster",
        cascade="all, delete-orphan",
    )
