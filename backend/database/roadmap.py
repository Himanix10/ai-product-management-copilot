from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)

    prd_id = Column(
        Integer,
        ForeignKey("prds.id"),
        nullable=False,
        index=True,
    )

    title = Column(String, nullable=False)
    quarter = Column(String, index=True)
    sprint = Column(String, index=True)
    milestone = Column(String)
    release_version = Column(String, index=True)
    status = Column(String, index=True)
    notes = Column(Text)

    version = Column(Integer, default=1)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    prd = relationship("PRD", back_populates="roadmaps")
