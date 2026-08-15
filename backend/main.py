from backend.database.db import init_db
from backend.services import (
    get_feedback_service,
    add_feedback_service,
    execute_chat_service,
    execute_prd_service,
    execute_prioritization_service,
    get_analytics_metrics
)

def run_backend_service():
    init_db()

if __name__ == "__main__":
    run_backend_service()
    print("Backend database initialized and services ready.")