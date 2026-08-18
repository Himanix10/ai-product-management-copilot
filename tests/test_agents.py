import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pytest
from agents.prioritization_agent import PrioritizationAgent
from agents.prd_agent import PRDAgent
from agents.orchestrator_agent import OrchestratorAgent
from agents.ingestion_agent import IngestionAgent
from agents.clustering_agent import ClusteringAgent
from agents.theme_agent import ThemeAgent
from agents.feature_request_agent import FeatureRequestAgent
from agents.analytics_agent import AnalyticsAgent
from agents.chat_agent import ChatAgent
from agents.roadmap_agent import RoadmapAgent

def test_prioritization_agent():
    agent = PrioritizationAgent()
    res = agent.execute({"title": "Sync", "reach": 1000, "impact": 2.0, "confidence": 0.8, "effort": 2.0})
    assert res["score"] == 800.0

def test_prioritization_agent_zero_effort():
    agent = PrioritizationAgent()
    with pytest.raises(ValueError):
        agent.execute({"reach": 1000, "impact": 2.0, "confidence": 0.8, "effort": 0})

def test_prd_agent():
    agent = PRDAgent()
    res = agent.execute({"feature_name": "Jira Sync", "target_user": "Dev Leads", "problem": "Manual sync", "requirements": "Webhooks"})
    assert "Jira Sync" in res["prd_markdown"]

def test_orchestrator_agent():
    agent = OrchestratorAgent()
    res = agent.execute({"prompt": "Draft PRD for Dark Mode"})
    assert res["workflow"] == "PRD Pipeline"

def test_ingestion_agent():
    agent = IngestionAgent()
    res = agent.execute({"text": "  Need bulk actions  ", "category": "Feature Request"})
    assert res["cleaned_text"] == "Need bulk actions"

def test_clustering_agent():
    agent = ClusteringAgent()
    res = agent.execute({})
    assert "clusters" in res

def test_theme_agent():
    agent = ThemeAgent()
    res = agent.execute({})
    assert "themes" in res

def test_feature_request_agent():
    agent = FeatureRequestAgent()
    res = agent.execute({"request": "Export bulk files"})
    assert res["demand_level"] == "High Demand"

def test_analytics_agent():
    agent = AnalyticsAgent()
    res = agent.execute({})
    assert "feedback_count" in res

def test_chat_agent():
    agent = ChatAgent()
    res = agent.execute({"prompt": "Summarize features"})
    assert "response" in res

def test_roadmap_agent():
    agent = RoadmapAgent()
    res = agent.execute({})
    assert "schedule" in res

if __name__ == "__main__":
    pytest.main(["-v", __file__])