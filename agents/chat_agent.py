from typing import Dict, Any
from agents.base_agent import BaseAgent
from backend.tools.retrieval_tools import RetrievalTools


class ChatAgent(BaseAgent):
    def __init__(self):
        super().__init__("ChatAgent")
        self.retrieval_tools = RetrievalTools()

    def execute(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        inputs = inputs or {}
        prompt = inputs.get("prompt", "")
        context = self.retrieval_tools.search_documents(prompt)
        llm_reply = self.invoke_llm(
            f"You are an AI Product Manager Copilot. Use workspace context:\n{context}",
            prompt
        )
        reply = llm_reply if llm_reply else f"AI Copilot Evaluated: '{prompt}'.\nTelemetry summary:\n{context}"
        return {
            "agent": self.agent_name,
            "response": reply
        }