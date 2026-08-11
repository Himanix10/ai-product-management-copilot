from backend.agents.base_agent import BaseAgent
from typing import Dict, Any

class ChatAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Copilot Assistant Agent",
            system_prompt="Process natural language product management requests."
        )

    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        query = input_data.get("query", "")
        return {
            "parsed_intent": "query_workspace",
            "original_query": query,
            "response": f"AI PM Copilot: Processed request '{query}'. Delegating task to workspace agents."
        }