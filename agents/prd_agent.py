from typing import Dict, Any
from agents.base_agent import BaseAgent
from backend.database.db import save_prd_db


class PRDAgent(BaseAgent):
    def __init__(self):
        super().__init__("PRDAgent")

    def execute(self, inputs: Dict[str, Any] = None) -> Dict[str, Any]:
        inputs = inputs or {}
        feature_name = inputs.get("feature_name", "Feature")
        target_user = inputs.get("target_user", "Enterprise Product Managers")
        problem = inputs.get("problem", "")
        requirements = inputs.get("requirements", "")

        prompt = f"""
Feature: {feature_name}
Target Persona: {target_user}
Problem: {problem}
Requirements: {requirements}

Draft a complete Markdown Product Requirement Document with Agile User Stories and Acceptance Criteria.
"""
        llm_prd = self.invoke_llm(
            "You are a Senior Product Manager. Write complete PRDs with user stories and acceptance criteria.",
            prompt
        )

        markdown = llm_prd if llm_prd else f"""# Product Requirement Document (PRD)

## Feature: {feature_name}
**Target Persona:** {target_user}

### Problem Statement
{problem}

### Agile User Stories
- **US-01:** As a {target_user}, I want {feature_name} so that I can resolve operational bottlenecks.
- **US-02:** As a team member, I want reliable validation so that errors are minimized.

### Functional Requirements
{requirements}

### Acceptance Criteria
- [ ] Task finishes under 2 seconds.
- [ ] Data persisted reliably in SQLite database.
- [ ] User receives clear completion telemetry.
"""
        save_prd_db(feature_name, target_user, problem, requirements, markdown)

        return {
            "agent": self.agent_name,
            "prd_markdown": markdown
        }