import os
from .base_agent import BaseAgent

class PrioritizationAgent(BaseAgent):
    """
    The Prioritization Agent takes the Feature Initiatives from the Clustering Agent
    and ranks them using the RICE scoring framework.
    """
    def __init__(self):
        # Initialize the BaseAgent with a strategic PM role
        super().__init__(
            role="Product Manager - Strategy & Prioritization",
            goal="Evaluate feature initiatives using the RICE framework and rank them by ROI."
        )

    def prioritize_features(self, clusters_text: str) -> str:
        """
        Takes the clustered initiatives and asks the LLM to score them.
        """
        print("Prioritization Agent: Calculating RICE scores for initiatives...")
        
        prompt = (
            "Analyze the following Feature Initiatives. For each initiative, estimate a RICE score:\n"
            "- Reach (1-100% of user base)\n"
            "- Impact (3 = massive, 2 = high, 1 = medium, 0.5 = low)\n"
            "- Confidence (100% = high, 80% = medium, 50% = low)\n"
            "- Effort (in person-months, e.g., 1, 2, 3)\n\n"
            "Calculate the final RICE score = (Reach * Impact * Confidence) / Effort.\n"
            "Format the output as a Markdown table ranked from highest score to lowest."
        )
        
        # Call the LLM
        response = self.run(prompt=prompt, context=clusters_text, temperature=0.2)
        return response

    def _generate_mock_response(self) -> str:
        """Overrides the BaseAgent mock to return a prioritization-specific response."""
        return (
            "### MOCK AI RESPONSE: Feature Prioritization (RICE Framework)\n\n"
            "| Rank | Initiative Name | Reach | Impact | Confidence | Effort | **RICE Score** |\n"
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n"
            "| **1** | Core Performance & Stability Overhaul | 100% | 3 | 100% | 2 | **150.0** |\n"
            "| **2** | UX Modernization & Accessibility | 80% | 2 | 80% | 1.5 | **85.3** |\n"
            "| **3** | Power User Workflow Enhancements | 30% | 2 | 100% | 1 | **60.0** |\n\n"
            "**Recommendation:** We should immediately allocate engineering resources to the **Core Performance & Stability Overhaul**, as it impacts all users and has the highest overall return on investment."
        )