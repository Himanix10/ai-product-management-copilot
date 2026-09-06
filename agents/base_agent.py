from abc import ABC, abstractmethod
import logging
from typing import Dict, Any
import requests
from backend.config import config

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    def invoke_llm(self, system_prompt: str, user_prompt: str) -> str:
        if not config.OPENROUTER_API_KEYS:
            logger.warning("No OpenRouter API keys configured for agent %s", self.agent_name)
            return None

        models_to_try = list(dict.fromkeys([
            config.OPENROUTER_MODEL,
            "liquid/lfm-2.5-2.6b:free",
            "minimax/minimax-m3:free",
            "inclusionai/ling-3.0-flash-fin:free",
        ]))

        retryable_statuses = {401, 402, 403, 404, 429, 500, 502, 503, 504}

        for model_name in models_to_try:
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.2,
            }

            for key_index, api_key in enumerate(config.OPENROUTER_API_KEYS, start=1):
                try:
                    response = requests.post(
                        config.OPENROUTER_BASE_URL,
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json",
                            "HTTP-Referer": "http://localhost:8501",
                            "X-Title": config.APP_NAME,
                        },
                        json=payload,
                        timeout=30,
                    )
                    if response.status_code in retryable_statuses:
                        logger.warning(
                            "OpenRouter model %s with key %d failed with status %d; trying next candidate",
                            model_name, key_index, response.status_code
                        )
                        continue
                    response.raise_for_status()
                    content = response.json().get("choices", [{}])[0].get("message", {}).get("content")
                    if content:
                        return content.strip()
                except requests.RequestException:
                    logger.exception("OpenRouter request failed for model %s with key %d", model_name, key_index)

        logger.error("All configured OpenRouter models and API keys failed for agent %s", self.agent_name)
        return None

    @abstractmethod
    def execute(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        pass