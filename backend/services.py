from agents.ingestion_agent import IngestionAgent
from agents.chat_agent import ChatAgent
from agents.prd_agent import PRDAgent
from agents.prioritization_agent import PrioritizationAgent
from agents.analytics_agent import AnalyticsAgent
from backend.database.db import fetch_customer_feedback_db, insert_customer_feedback_db

def get_feedback_service(category="All", search=""):
    return fetch_customer_feedback_db(category=category, search_query=search)

def add_feedback_service(source, user_type, text, category):
    ingest_agent = IngestionAgent()
    cleaned = ingest_agent.execute({"text": text, "category": category, "source": source, "user_type": user_type})
    insert_customer_feedback_db(source, user_type, cleaned["cleaned_text"], cleaned["classified_category"])

def execute_chat_service(prompt: str):
    agent = ChatAgent()
    return agent.execute({"prompt": prompt})

def execute_prd_service(feature_name: str, target_user: str, problem: str, requirements: str):
    agent = PRDAgent()
    return agent.execute({"feature_name": feature_name, "target_user": target_user, "problem": problem, "requirements": requirements})

def execute_prioritization_service(reach: float, impact: float, confidence: float, effort: float, title: str = "Initiative"):
    agent = PrioritizationAgent()
    return agent.execute({"title": title, "reach": reach, "impact": impact, "confidence": confidence, "effort": effort})

def get_analytics_metrics():
    agent = AnalyticsAgent()
    return agent.execute({})