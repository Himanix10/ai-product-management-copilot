from backend.agents.base_agent import BaseAgent
from typing import Dict, Any
from collections import Counter

class ThemeAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Pain Point Discovery Agent",
            system_prompt="Extract customer pain points and problem clusters from feedback."
        )

    def _process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        feedback_list = input_data.get("processed_feedback", [])
        pain_points = []
        for item in feedback_list:
            text = item.get("feedback_text", "").lower()
            if any(k in text for k in ["slow", "loading", "delay", "latency"]):
                pain_points.append("Performance & Speed")
            elif any(k in text for k in ["export", "prd", "download", "csv"]):
                pain_points.append("PRD Automation")
            elif any(k in text for k in ["ui", "ux", "navigate", "layout"]):
                pain_points.append("UI / UX Refresh")
            elif any(k in text for k in ["api", "webhook", "jira", "sync"]):
                pain_points.append("Integrations")
            else:
                pain_points.append("General Usability")

        counts = Counter(pain_points)
        summary = [{"pain_point": k, "count": v} for k, v in counts.items()]
        return {"pain_point_clusters": summary, "top_pain_point": counts.most_common(1)[0][0] if counts else "General Usability"}