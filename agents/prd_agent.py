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
        custom_criteria = inputs.get("acceptance_criteria", "")

        criteria_prompt = f"\nCustom Acceptance Constraints:\n{custom_criteria}" if custom_criteria else ""

        prompt = f"""
Feature Name: {feature_name}
Target User Persona: {target_user}
Problem Statement: {problem}
Functional Scope: {requirements}{criteria_prompt}

Generate a complete, industry-standard Product Requirement Document (PRD) in clean Markdown.
Ensure explicit Agile User Stories and testable Acceptance Criteria:

1. Executive Summary
2. Problem Statement & Business Objectives
3. Target User Personas
4. Detailed Agile User Stories (Format: "As a [persona], I want [capability] so that [benefit]")
5. Functional Specifications & Scope
6. Non-Functional Requirements (P95 latency, SLA, concurrency)
7. Acceptance Criteria (Checklist format: "- [ ] Given/When/Then or testable benchmark")
8. Success Metrics (KPIs, adoption targets)
9. Risks, Dependencies & Open Questions
"""

        system_prompt = (
            "You are a Senior Principal Product Manager. Draft executive-ready PRDs "
            "with actionable user stories and testable acceptance criteria."
        )

        llm_prd = self.invoke_llm(system_prompt, prompt)

        markdown = llm_prd if llm_prd else self._fallback_prd(
            feature_name, target_user, problem, requirements, custom_criteria
        )

        default_ac = (
            custom_criteria
            if custom_criteria
            else "- [ ] System response latency finishes in under 2.0 seconds.\n"
                 "- [ ] All inputs are validated before SQLite database persistence.\n"
                 "- [ ] User receives immediate affirmative status confirmation.\n"
                 "- [ ] Zero database constraint errors occur during execution."
        )

        save_prd_db(
            feature_name=feature_name,
            target_persona=target_user,
            problem=problem,
            requirements=requirements,
            markdown=markdown,
            acceptance_criteria=default_ac
        )

        return {
            "agent": self.agent_name,
            "prd_markdown": markdown,
            "acceptance_criteria": default_ac
        }

    @staticmethod
    def _fallback_prd(feature_name, target_user, problem, requirements, custom_criteria=""):
        ac_section = (
            custom_criteria
            if custom_criteria
            else "- [ ] System response latency finishes in under 2.0 seconds.\n"
                 "- [ ] All inputs are validated before SQLite database persistence.\n"
                 "- [ ] User receives immediate affirmative status confirmation.\n"
                 "- [ ] Zero database constraint errors occur during execution."
        )

        return f"""# Product Requirement Document (PRD)

## Feature: {feature_name}
**Target Persona:** {target_user}

### 1. Executive Summary
This initiative formalizes requirements and acceptance benchmarks for **{feature_name}** to eliminate user friction.

### 2. Problem Statement
{problem}

### 3. User Personas
* **Primary Persona:** {target_user}

### 4. Agile User Stories
* **US-01:** As a {target_user}, I want {feature_name} so that I can eliminate operational bottlenecks.
* **US-02:** As a Team Lead, I want automated validation checks so that manual errors are minimized.
* **US-03:** As an Administrator, I want clear controls and audit visibility.

### 5. Functional Requirements
{requirements}

### 6. Non-Functional Requirements
* **Latency:** P95 response time under 2.0 seconds.
* **Reliability:** 99.9% uptime with persistent SQLite database storage.

### 7. Acceptance Criteria
{ac_section}

### 8. Success Metrics (KPIs)
* Feature adoption rate >= 75% within 30 days of release.
* Support ticket volume reduced by >= 25%.
"""