from typing import Dict, Any

from agents.base_agent import BaseAgent
from backend.tools.analytics_tools import AnalyticsTools


class AnalyticsAgent(BaseAgent):

    def __init__(self):
        super().__init__("AnalyticsAgent")

    def execute(
        self,
        inputs: Dict[str, Any] = None
    ) -> Dict[str, Any]:

        kpis = AnalyticsTools.get_workspace_kpis()

        return {
            "agent": self.agent_name,

            "feedback_count": kpis[
                "voc_feedback_volume"
            ],

            "active_pain_points": kpis[
                "active_pain_points"
            ],

            "scored_initiatives": kpis[
                "scored_initiatives"
            ],

            "approved_prds": kpis[
                "approved_prds"
            ],

            "active_roadmap_items": kpis[
                "active_roadmap_items"
            ],
        }