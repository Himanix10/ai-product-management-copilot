from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    company = Column(String(100))
    role = Column(String(50))
    created_date = Column(DateTime, default=datetime.utcnow)

class CustomerFeedback(Base):
    __tablename__ = "customer_feedback"
    feedback_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    product_id = Column(Integer, default=1)
    feedback_text = Column(Text, nullable=False)
    sentiment = Column(String(20), default="Neutral")
    channel = Column(String(50), default="Zendesk")
    submission_date = Column(DateTime, default=datetime.utcnow)

class OpportunityPrioritization(Base):
    __tablename__ = "opportunity_prioritization"
    priority_id = Column(Integer, primary_key=True, index=True)
    cluster_id = Column(Integer)
    initiative_title = Column(String(200), nullable=False)
    reach = Column(Integer, default=1000)
    impact = Column(Float, default=2.0)
    confidence = Column(Float, default=0.8)
    effort = Column(Float, default=2.0)
    rice_score = Column(Float, default=0.0)

class ProductRequirementDocument(Base):
    __tablename__ = "product_requirement_documents"
    prd_id = Column(String(50), primary_key=True)
    priority_id = Column(Integer, ForeignKey("opportunity_prioritization.priority_id"), nullable=True)
    title = Column(String(200), nullable=False)
    executive_summary = Column(Text)
    problem_statement = Column(Text)
    status = Column(String(20), default="Draft")