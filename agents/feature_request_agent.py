from typing import Dict, Any
from agents.base_agent import BaseAgent

class FeatureRequestAgent(BaseAgent):
    def __init__(self):
        super().__init__("FeatureRequestAgent")

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        request_text = inputs.get("request", "").lower()
        demand = "High Demand" if ("bulk" in request_text or "export" in request_text or "jira" in request_text) else "Medium Demand"
        return {
            "agent": self.agent_name,
            "status": "Analyzed",
            "demand_level": demand
        }