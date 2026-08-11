from backend.database.db import init_db, fetch_customer_feedback_db, insert_customer_feedback_db

def run_backend_service():
    """Initializes the backend database engine directly for Streamlit integration."""
    init_db()

def get_feedback_service(category="All", search=""):
    return fetch_customer_feedback_db(category=category, search_query=search)

def add_feedback_service(source, user_type, text, category):
    insert_customer_feedback_db(source, user_type, text, category)
