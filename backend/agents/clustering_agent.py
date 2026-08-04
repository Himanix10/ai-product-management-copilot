import os
from .base_agent import BaseAgent

class ClusteringAgent(BaseAgent):
    """
    The Clustering Agent takes the raw themes extracted by the Theme Agent
    and groups them into actionable Feature Initiatives or Epics.
    """
    def __init__(self):
        # Initialize the BaseAgent with a strategic PM role
        super().__init__(
            role="Product Manager - Feature Strategist",
            goal="Group recurring product themes into concrete, actionable Feature Initiatives or Epics."
        )

    def cluster_themes(self, themes_text: str) -> str:
        """
        Takes the text output from the Theme Agent and asks the LLM to 
        turn them into structured feature clusters.
        """
        print("Clustering Agent: Grouping themes into feature initiatives...")
        
        prompt = (
            "Analyze the following product themes. Group related themes together into 2 to 3 "
            "major 'Feature Initiatives' (Epics).\n"
            "For each Initiative, provide:\n"
            "1. Initiative Name (e.g., 'Core Platform Optimization')\n"
            "2. Description (What are we building and why?)\n"
            "3. Addressed Themes (Which themes from the input does this solve?)\n"
            "Format the output cleanly using Markdown."
        )
        
        # Call the LLM using the inherited run() method
        response = self.run(prompt=prompt, context=themes_text, temperature=0.4)
        return response

    def _generate_mock_response(self) -> str:
        """Overrides the BaseAgent mock to return a clustering-specific response."""
        return (
            "### MOCK AI RESPONSE: Feature Initiatives\n\n"
            "**Initiative 1: Core Performance & Stability Overhaul**\n"
            "- **Description:** A backend and frontend optimization sprint to resolve latency issues and app crashes, ensuring a smooth baseline experience.\n"
            "- **Addressed Themes:** Dashboard Performance, App Stability / Bugs\n\n"
            "**Initiative 2: UX Modernization & Accessibility**\n"
            "- **Description:** Updating the user interface to meet modern accessibility standards, including a highly requested dark mode.\n"
            "- **Addressed Themes:** UI / Display Preferences\n\n"
            "**Initiative 3: Power User Workflow Enhancements**\n"
            "- **Description:** Implementing keyboard shortcuts and fixing export bugs to speed up daily tasks for our most active users.\n"
            "- **Addressed Themes:** Workflow Efficiency\n"
        )