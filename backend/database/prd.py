from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database.db import Base


class PRD(Base):
    __tablename__ = "prds"

    id = Column(Integer, primary_key=True, index=True)

    priority_id = Column(
        Integer,
        ForeignKey("priorities.id"),
        nullable=False,
        index=True,
    )

    title = Column(String, nullable=False, index=True)
    executive_summary = Column(Text)
    problem_statement = Column(Text)
    objectives = Column(Text)
    user_personas = Column(Text)
    user_stories = Column(Text)
    functional_requirements = Column(Text)
    non_functional_requirements = Column(Text)
    acceptance_criteria = Column(Text)
    success_metrics = Column(Text)
    risks = Column(Text)
    open_questions = Column(Text)

    version = Column(Integer, default=1, index=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        index=True,
    )

    priority = relationship("Priority", back_populates="prds")
    roadmaps = relationship(
        "Roadmap",
        back_populates="prd",
        cascade="all, delete-orphan",
    )
