from typing import Dict, Any
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from agents.base_agent import BaseAgent

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

class IngestionAgent(BaseAgent):
    def __init__(self):
        super().__init__("IngestionAgent")
        self.sia = SentimentIntensityAnalyzer()

    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        raw_text = inputs.get("text", "")
        category = inputs.get("category", "General")

        cleaned_text = " ".join(raw_text.strip().split())

        llm_category = self.invoke_llm(
            "Classify feedback into exactly one of: Feature Request, Usability, Bug, or Integration. Return only the category name.",
            cleaned_text
        )
        final_category = llm_category if llm_category and llm_category in ["Feature Request", "Usability", "Bug", "Integration"] else category
        sentiment = self.sia.polarity_scores(cleaned_text)["compound"]

        return {
            "agent": self.agent_name,
            "cleaned_text": cleaned_text,
            "classified_category": final_category,
            "sentiment_score": round(sentiment, 2)
        }