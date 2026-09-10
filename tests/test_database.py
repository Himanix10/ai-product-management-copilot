from backend.database.db import init_db, fetch_customer_feedback_db

def test_db_initialization_and_seeding():
    init_db()
    df = fetch_customer_feedback_db()
    assert not df.empty