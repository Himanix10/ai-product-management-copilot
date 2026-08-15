from abc import ABC, abstractmethod
from typing import Dict, Any
from google import genai
from backend.config import config

class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.client = genai.Client(api_key=config.GEMINI_API_KEY) if config.GEMINI_API_KEY else None

    def invoke_llm(self, system_prompt: str, user_prompt: str) -> str:
        if not self.client:
            return None
        try:
            prompt = f"{system_prompt}\n\nUser: {user_prompt}"
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt
            )
            if response and response.text:
                return response.text.strip()
            return None
        except Exception:
            return None

    @abstractmethod
    def execute(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        pass