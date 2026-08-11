from backend.agents.base_agent import BaseAgent
from typing import Dict, Any

class PRDAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PRD Authoring Agent",
            system_prompt="Draft formal Product Requirement Documents for initiatives."
        )

    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        top_init = input_data.get("top_initiative", {})
        title = top_init.get("initiative_title", "New Feature Initiative")
        
        prd = {
            "prd_id": f"PRD-{top_init.get('priority_id', '501')}",
            "title": f"PRD: {title}",
            "status": "Approved",
            "target_quarter": "Q3 2026",
            "executive_summary": f"Functional specs to build and ship {title}.",
            "problem_statement": "Users experience friction and latency during peak usage.",
            "okrs": ["Decrease P95 latency below 2.0s", "Improve CSAT score by 15%"],
            "functional_requirements": [
                "FR-1: Implement database caching layer.",
                "FR-2: Standardize API error payloads."
            ],
            "acceptance_criteria": ["Given logged-in PM, dashboard loads under 2.0s."]
        }
        return {"prd_document": prd}