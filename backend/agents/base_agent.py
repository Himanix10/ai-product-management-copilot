import os
import requests
from typing import List, Dict, Any, Optional
from dotenv import dotenv_values

class BaseAgent:
    """
    The foundational agent class. All specialized agents (Theme, Clustering, Prioritization) 
    will inherit from this class. It handles standard LLM communication, system prompts, 
    and error handling.
    """
    def __init__(self, role: str, goal: str, model: str = "gemini-3.6-flash"):
        """
        Initialize the Base Agent.
        """
        # FORCED FILE READ: Bypass Windows terminal cache completely
        env_vars = dotenv_values(".env")
        api_key = env_vars.get("GEMINI_API_KEY", "")
        
        self.is_mock = False
        if not api_key or api_key == "your_actual_api_key_here":
            print("Warning: Valid GEMINI_API_KEY not found in .env file.")
            print("The agent will run in MOCK MODE and return simulated responses.")
            self.is_mock = True
        else:
            self.api_key = api_key
            
        self.role = role
        self.goal = goal
        self.model = model
        
        # The system prompt tells the LLM who it is and how to behave
        self.system_prompt = (
            f"You are an expert AI Product Manager Assistant.\n"
            f"Your specific role: {self.role}\n"
            f"Your core goal: {self.goal}\n"
            f"Always respond in a structured, objective, and professional PM tone. "
            f"Prioritize clarity, user impact, and data-driven reasoning."
        )

    def run(self, prompt: str, context: Optional[str] = None, temperature: float = 0.2) -> str:
        """
        Sends the prompt and context to the LLM via Direct REST API.
        """
        if getattr(self, 'is_mock', False):
            return self._generate_mock_response()
            
        # Combine the user prompt with the context if it exists
        full_prompt = prompt
        if context:
            full_prompt = f"Use the following data/context to complete the task:\n---\n{context}\n---\n\n{prompt}"
        
        # CHANGED v1beta TO v1 IN THE URL
        url = f"https://generativelanguage.googleapis.com/v1/models/{self.model}:generateContent?key={self.api_key}"
        
        # Construct the payload according to Gemini REST API specs
        payload = {
            "system_instruction": {
                "parts": [{"text": self.system_prompt}]
            },
            "contents": [
                {"role": "user", "parts": [{"text": full_prompt}]}
            ],
            "generationConfig": {
                "temperature": temperature
            }
        }
        
        try:
            # Send the request directly to Google's servers
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status() # Check for HTTP errors
            
            # Extract and return the text
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            error_details = response.text if 'response' in locals() else str(e)
            return f"Error communicating with Gemini REST API: {error_details}"

    def _generate_mock_response(self) -> str:
        """Returns a simulated LLM response for testing without an API key."""
        return (
            "### MOCK AI RESPONSE (No API Key Provided)\n\n"
            "**1. Dashboard Performance**\n"
            "- **Summary:** Users experience significant lag when loading more than 50 items.\n"
            "- **Mentions:** 2\n\n"
            "**2. UI / Display Preferences**\n"
            "- **Summary:** Users are requesting a dark mode because the bright background is harsh at night.\n"
            "- **Mentions:** 2\n\n"
            "**3. App Stability / Bugs**\n"
            "- **Summary:** iOS app crashes frequently; PDF export is failing.\n"
            "- **Mentions:** 4\n\n"
            "**4. Workflow Efficiency**\n"
            "- **Summary:** Users want shortcut keys to create tickets faster.\n"
            "- **Mentions:** 2\n"
        )