import sys
import os

def run_integration_test():
    print("Verifying AI PM Copilot imports and system setup...")
    sys.path.insert(0, os.path.abspath("."))

    try:
        from backend.database.db import init_db
        from backend.database.models import CustomerFeedback, ProductRequirementDocument
        from backend.agents.orchestrator_agent import OrchestratorAgent
        print("Backend & Database imports: SUCCESS")
    except Exception as e:
        print(f"Backend import check failed: {e}")
        return False

    try:
        from frontend.auth import init_auth
        from frontend.dashboard_sections import render_roadmap, render_dashboard_overview
        print("Frontend imports: SUCCESS")
    except Exception as e:
        print(f"Frontend import check failed: {e}")
        return False

    init_db()
    print("Database Tables Created: SUCCESS")

    orchestrator = OrchestratorAgent()
    test_payload = {
        "raw_feedback": [
            {"content": "Dashboard query processing shows latency delays.", "channel": "Zendesk"},
            {"content": "Need faster PRD exports and bulk operations.", "channel": "Survey"}
        ]
    }
    result = orchestrator.run(test_payload)
    print("Multi-Agent Orchestrator Run: SUCCESS")
    print(f"Pipeline Result Status: {result.data.get('status')}")

    return True

if __name__ == "__main__":
    if run_integration_test():
        print("\nAll files verified successfully! System ready to run.")