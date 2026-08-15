from typing import Dict, Any
from agents.base_agent import BaseAgent
from agents.prioritization_agent import PrioritizationAgent
from agents.prd_agent import PRDAgent
from agents.roadmap_agent import RoadmapAgent
from agents.theme_agent import ThemeAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("OrchestratorAgent")
        self.prioritization_agent = PrioritizationAgent()
        self.prd_agent = PRDAgent()
        self.roadmap_agent = RoadmapAgent()
        self.theme_agent = ThemeAgent()

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        prompt = inputs.get("prompt", "").lower()
        llm_response = self.invoke_llm(
            "You are an Orchestrator Agent. Route task to: PRD, RICE, or DISCOVERY. Return only the category.",
            prompt
        )

        if "prd" in prompt or "spec" in prompt or (llm_response and "PRD" in llm_response.upper()):
            prd_res = self.prd_agent.execute({
                "feature_name": inputs.get("feature_name", "Requested Feature"),
                "target_user": "Enterprise Users",
                "problem": prompt,
                "requirements": "Generated via Orchestrator workflow"
            })
            return {
                "agent": self.agent_name,
                "workflow": "PRD Pipeline",
                "result": prd_res["prd_markdown"]
            }
        elif "rice" in prompt or "prioritize" in prompt or (llm_response and "RICE" in llm_response.upper()):
            rice_res = self.prioritization_agent.execute({
                "title": inputs.get("title", "Initiative"),
                "reach": inputs.get("reach", 1000),
                "impact": inputs.get("impact", 2.0),
                "confidence": inputs.get("confidence", 0.8),
                "effort": inputs.get("effort", 1.0)
            })
            return {
                "agent": self.agent_name,
                "workflow": "Prioritization Pipeline",
                "result": f"Score: {rice_res['score']}"
            }
        else:
            theme_res = self.theme_agent.execute(inputs)
            return {
                "agent": self.agent_name,
                "workflow": "Discovery Pipeline",
                "result": f"Discovered Themes: {', '.join(theme_res['themes'])}"
            }