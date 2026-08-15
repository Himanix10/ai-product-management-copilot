from typing import Dict, Any
from agents.base_agent import BaseAgent
from backend.tools.db_tools import DBTools

class RoadmapAgent(BaseAgent):
    def __init__(self):
        super().__init__("RoadmapAgent")

    def execute(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        initiatives_df = DBTools.get_initiatives()
        schedule = []
        quarters = ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"]

        if not initiatives_df.empty:
            for idx, row in initiatives_df.iterrows():
                q = quarters[idx % len(quarters)]
                schedule.append({
                    "Quarter": q,
                    "Initiative": row["Title"],
                    "RICE Score": row["RICE Score"],
                    "Status": row["Status"]
                })
        else:
            schedule = [
                {"Quarter": "Q1 2026", "Initiative": "UI Redesign", "RICE Score": 5000.0, "Status": "Completed"},
                {"Quarter": "Q2 2026", "Initiative": "RICE Calculator", "RICE Score": 2700.0, "Status": "In Progress"},
                {"Quarter": "Q3 2026", "Initiative": "Jira Webhooks", "RICE Score": 1680.0, "Status": "Planned"}
            ]

        return {
            "agent": self.agent_name,
            "schedule": schedule
        }