from typing import Dict, Any
from agents.base_agent import BaseAgent
from backend.tools.scoring_tools import ScoringTools
from backend.tools.db_tools import DBTools

class PrioritizationAgent(BaseAgent):
    def __init__(self):
        super().__init__("PrioritizationAgent")

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        title = inputs.get("title", "Initiative")
        reach = float(inputs.get("reach", 0))
        impact = float(inputs.get("impact", 0))
        confidence = float(inputs.get("confidence", 0))
        effort = float(inputs.get("effort", 1))

        score = ScoringTools.calculate_rice(reach, impact, confidence, effort)
        DBTools.add_initiative(title, reach, impact, confidence, effort, score)

        return {
            "agent": self.agent_name,
            "title": title,
            "score": score
        }