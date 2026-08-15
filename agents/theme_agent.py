from typing import Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from agents.base_agent import BaseAgent
from backend.tools.db_tools import DBTools

class ThemeAgent(BaseAgent):
    def __init__(self):
        super().__init__("ThemeAgent")

    def execute(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        feedback_df = DBTools.get_feedback_records()
        if not feedback_df.empty and len(feedback_df) >= 2:
            texts = feedback_df["Feedback"].tolist()
            vectorizer = TfidfVectorizer(stop_words="english", max_features=5)
            vectorizer.fit(texts)
            extracted_words = [word.capitalize() for word in vectorizer.get_feature_names_out()]
            extracted_themes = [f"{word} Optimization" for word in extracted_words[:3]]
        else:
            extracted_themes = ["Enterprise Scalability", "User Workflow Speed", "Ecosystem Integrations"]

        llm_themes = self.invoke_llm(
            "Extract 3 concise strategic enterprise themes from input keywords. Return only as a comma separated list.",
            f"Keywords: {', '.join(extracted_themes)}"
        )
        if llm_themes and "," in llm_themes:
            themes = [t.strip() for t in llm_themes.split(",") if t.strip()]
        else:
            themes = extracted_themes

        return {
            "agent": self.agent_name,
            "themes": themes
        }