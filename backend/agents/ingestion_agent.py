from backend.agents.base_agent import BaseAgent
from typing import Dict, Any, List

def sanitize_feedback(text: str) -> str:
    return text.strip().replace("\n", " ")

class IngestionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="VOC Ingestion Agent",
            system_prompt="Standardize and clean raw customer feedback."
        )
        self.register_tool("sanitize_feedback", sanitize_feedback)

    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        raw_list: List[Dict[str, Any]] = input_data.get("raw_feedback", [])
        cleaned = []
        for idx, item in enumerate(raw_list, 1):
            text = self.execute_tool("sanitize_feedback", text=item.get("content", item.get("feedback_text", "")))
            cleaned.append({
                "feedback_id": item.get("id", idx),
                "user_persona": item.get("user_persona", "Enterprise User"),
                "feedback_text": text,
                "channel": item.get("channel", "Zendesk"),
                "timestamp": item.get("timestamp", "2026-08-01")
            })
        return {"processed_feedback": cleaned, "total_records": len(cleaned)}