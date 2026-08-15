from typing import Dict, Any

from agents.base_agent import BaseAgent
from backend.database.db import save_prd_db


class PRDAgent(BaseAgent):

    def __init__(self):
        super().__init__("PRDAgent")

    def execute(
        self,
        inputs: Dict[str, Any]
    ) -> Dict[str, Any]:

        feature_name = inputs.get(
            "feature_name",
            "Feature"
        )

        target_user = inputs.get(
            "target_user",
            "Product Managers"
        )

        problem = inputs.get(
            "problem",
            ""
        )

        requirements = inputs.get(
            "requirements",
            ""
        )

        prompt = f"""
Feature:
{feature_name}

Target Persona:
{target_user}

Problem:
{problem}

Requirements:
{requirements}
"""

        llm_prd = self.invoke_llm(
            """
You are an expert Product Manager.

Create a complete Product Requirements Document.

Include:

1. Executive Summary
2. Problem Statement
3. Objectives
4. User Personas
5. User Stories
6. Functional Requirements
7. Non-Functional Requirements
8. Acceptance Criteria
9. Success Metrics
10. Risks
11. Open Questions
12. Priority
13. Estimated Effort

Return the PRD in clean Markdown.
""",
            prompt
        )

        markdown = (
            llm_prd
            if llm_prd
            else self._fallback_prd(
                feature_name,
                target_user,
                problem,
                requirements
            )
        )

        # Save into the EXPANDED PRD schema.
        save_prd_db(
            feature_name=feature_name,
            target_persona=target_user,
            problem=problem,
            requirements=requirements,
            markdown=markdown,
        )

        return {
            "agent": self.agent_name,
            "prd_markdown": markdown,
        }

    @staticmethod
    def _fallback_prd(
        feature_name,
        target_user,
        problem,
        requirements
    ):

        return f"""
# Product Requirement Document

## Feature

{feature_name}

## Executive Summary

This initiative addresses customer needs related to
{feature_name}.

## Problem Statement

{problem}

## Objectives

- Improve customer experience
- Reduce operational friction
- Improve product adoption
- Provide measurable product outcomes

## User Personas

{target_user}

## User Stories

- As a user, I want the feature to be reliable.
- As a product manager, I want measurable outcomes.
- As an administrator, I want clear controls and visibility.

## Functional Requirements

{requirements}

## Non-Functional Requirements

- Response time should remain below 2 seconds
- System should be reliable
- Data should be persisted in SQLite
- Access should be authenticated

## Acceptance Criteria

- Feature works as specified
- Data is persisted successfully
- User receives clear feedback
- No database schema errors occur

## Success Metrics

- Increased adoption
- Reduced customer friction
- Improved task completion rate

## Risks

- Integration complexity
- Data quality issues
- Engineering capacity

## Open Questions

- What additional integrations are required?
- What is the target release quarter?

## Priority

P1

## Estimated Effort

Medium
"""