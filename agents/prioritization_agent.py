from backend.agents.base_agent import BaseAgent
from typing import Dict, Any

def calculate_rice(reach: int, impact: float, confidence: float, effort: float) -> float:
    if effort <= 0:
        return 0.0
    return round((reach * impact * confidence) / effort, 2)

class PrioritizationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="RICE Scoring Agent",
            system_prompt="Score feature initiatives using RICE methodology."
        )
        self.register_tool("calculate_rice", calculate_rice)

    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        opportunities = input_data.get("opportunity_areas", [])
        ranked = []
        for opp in opportunities:
            reach = opp["support_volume"] * 100
            impact = 3.0 if "Performance" in opp["opportunity_title"] else 2.0
            confidence = 0.85
            effort = 2.0
            score = self.execute_tool("calculate_rice", reach=reach, impact=impact, confidence=confidence, effort=effort)
            ranked.append({
                "priority_id": 500 + opp["cluster_id"],
                "initiative_title": opp["opportunity_title"],
                "reach": reach,
                "impact": impact,
                "confidence": confidence,
                "effort": effort,
                "rice_score": score
            })
        ranked.sort(key=lambda x: x["rice_score"], reverse=True)
        return {"ranked_initiatives": ranked, "top_initiative": ranked[0] if ranked else None}