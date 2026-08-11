from backend.database.db import get_db_session
from agents.prd_agent import PRDAgent

def generate_prd_direct(workspace_id: int, feature_title: str) -> dict:
    """Runs PRD generation logic directly without going through FastAPI."""
    db = get_db_session()
    try:
        agent = PRDAgent()
        # Execute agent workflow directly
        prd_result = agent.run(workspace_id=workspace_id, title=feature_title)
        
        # Save to SQLite database directly
        # db.add(...)
        # db.commit()
        
        return {"status": "success", "data": prd_result}
    finally:
        db.close()
