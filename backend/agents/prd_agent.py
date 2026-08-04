import os
from .base_agent import BaseAgent

class PRDAgent(BaseAgent):
    """
    The PRD Agent takes the highest-priority feature initiative and 
    generates a comprehensive Product Requirements Document (PRD) for the engineering team.
    """
    def __init__(self):
        # Initialize the BaseAgent with an execution-focused PM role
        super().__init__(
            role="Product Manager - Execution & Technical Spec Writer",
            goal="Write detailed, highly structured Product Requirements Documents (PRDs) for engineering teams based on prioritized features."
        )

    def generate_prd(self, prioritized_features_text: str) -> str:
        """
        Takes the ranked list of features, identifies the #1 priority, 
        and asks the LLM to write a PRD for it.
        """
        print("PRD Agent: Drafting Product Requirements Document for the top feature...")
        
        prompt = (
            "Review the provided prioritized feature list. Identify the #1 ranked feature initiative. "
            "Write a standard Product Requirements Document (PRD) for this feature. "
            "Include the following sections:\n"
            "1. Title & Meta (Status, Target Release)\n"
            "2. Problem Statement (Why are we doing this?)\n"
            "3. Goals & Non-Goals\n"
            "4. User Stories\n"
            "5. Acceptance Criteria\n"
            "Format the output strictly in Markdown."
        )
        
        # Call the LLM
        response = self.run(prompt=prompt, context=prioritized_features_text, temperature=0.3)
        return response

    def _generate_mock_response(self) -> str:
        """Overrides the BaseAgent mock to return a simulated PRD."""
        return (
            "# PRD: Core Performance & Stability Overhaul\n\n"
            "**Status:** In Review | **Target Release:** Q4 Sprint 1 | **Priority:** P0 (Critical)\n\n"
            "## 1. Problem Statement\n"
            "Currently, users experience significant latency when loading more than 50 items on the dashboard. "
            "Additionally, mobile users are reporting frequent crashes on iOS. This severely degrades trust and workflow efficiency.\n\n"
            "## 2. Goals & Non-Goals\n"
            "**Goals:**\n"
            "- Reduce dashboard load time for 50+ items to under 1.5 seconds.\n"
            "- Eliminate the memory leak causing iOS app crashes.\n"
            "**Non-Goals:**\n"
            "- We are *not* redesigning the dashboard UI in this sprint.\n\n"
            "## 3. User Stories\n"
            "- *As a power user*, I want my dashboard to load instantly regardless of item count, so I can start working without waiting.\n"
            "- *As an iOS user*, I want the app to remain stable during heavy usage, so I don't lose unsaved data.\n\n"
            "## 4. Acceptance Criteria\n"
            "- [ ] Dashboard API response time is < 500ms for payloads up to 500 items.\n"
            "- [ ] Frontend implements virtualized scrolling/pagination for the dashboard.\n"
            "- [ ] iOS crash rate drops to < 0.1% over a 7-day period in TestFlight."
        )