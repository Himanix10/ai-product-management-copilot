from backend.agents.base_agent import BaseAgent
from typing import Dict, Any

class RoadmapAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Roadmap Scheduling Agent",
            system_prompt="Schedule prioritized initiatives across quarterly roadmap milestones."
        )

    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        ranked = input_data.get("ranked_initiatives", [])
        schedule = []
        quarters = ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026"]
        for idx, init in enumerate(ranked):
            q = quarters[idx % len(quarters)]
            schedule.append({
                "roadmap_id": f"RM-00{idx+1}",
                "initiative_title": init["initiative_title"],
                "target_quarter": q,
                "rice_score": init["rice_score"],
                "status": "Planned"
            })
        return {"roadmap_schedule": schedule}