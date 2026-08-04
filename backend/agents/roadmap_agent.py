import os
from .base_agent import BaseAgent

class RoadmapAgent(BaseAgent):
    """
    The Roadmap Agent takes the prioritized list of features and sequences them 
    into a logical timeline (Sprints or Quarters) based on their RICE scores and effort.
    """
    def __init__(self):
        # Initialize the BaseAgent with a planning-focused PM role
        super().__init__(
            role="Product Manager - Release Planner",
            goal="Sequence prioritized features into a realistic, structured execution roadmap."
        )

    def generate_roadmap(self, prioritized_features_text: str) -> str:
        """
        Takes the ranked list of features and asks the LLM to draft a release roadmap.
        """
        print("Roadmap Agent: Sequencing features into a Sprint Roadmap...")
        
        prompt = (
            "Review the provided prioritized feature list and their RICE scores. "
            "Create a structured execution roadmap dividing these features into Sprints (e.g., Sprint 1, Sprint 2). "
            "Assume a standard 2-week sprint cycle. High-priority, high-effort items may span multiple sprints. "
            "For each sprint, output:\n"
            "- Sprint Name / Dates\n"
            "- Primary Goal\n"
            "- Features to be developed\n"
            "Format the output cleanly using Markdown."
        )
        
        # Call the LLM
        response = self.run(prompt=prompt, context=prioritized_features_text, temperature=0.3)
        return response

    def _generate_mock_response(self) -> str:
        """Overrides the BaseAgent mock to return a simulated Roadmap."""
        return (
            "# Product Execution Roadmap\n\n"
            "### Sprint 1: Stability First\n"
            "**Primary Goal:** Fix critical performance and crash issues to restore user trust.\n"
            "- [x] Core Performance & Stability Overhaul (Part 1: iOS Memory Leak Fix)\n"
            "- [x] Core Performance & Stability Overhaul (Part 2: Dashboard Pagination)\n\n"
            "### Sprint 2: Modernization & Quick Wins\n"
            "**Primary Goal:** Deliver highly requested UI improvements and fix workflow bugs.\n"
            "- [ ] UX Modernization & Accessibility (Dark Mode implementation)\n"
            "- [ ] Power User Workflow Enhancements (Shortcut keys)\n\n"
            "### Sprint 3: Polish & Tech Debt\n"
            "**Primary Goal:** Wrap up remaining UX features and address backend tech debt.\n"
            "- [ ] UX Modernization & Accessibility (Contrast and screen reader support)\n"
            "- [ ] PDF Export Bug Resolution\n"
        )