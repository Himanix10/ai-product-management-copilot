import sqlite3
import hashlib
import pandas as pd
import streamlit as st

DATABASE_FILE = "app.db"

@st.cache_resource
def get_db_connection():
    """Create persistent SQLite connection cached by Streamlit."""
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables and seed initial records."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'Product Manager'
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            user_type TEXT NOT NULL,
            feedback_text TEXT NOT NULL,
            category TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        pwd_hash = hashlib.sha256("password123".encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                       ("admin", "user@enterprise.com", pwd_hash))

        seed_data = [
            ("Zendesk", "Enterprise Lead", "Need faster PRD exports and bulk actions", "Feature Request"),
            ("Survey", "Product Mgr", "UI navigation is crisp and modern", "Usability"),
            ("CRM", "Tech Lead", "Add REST API webhooks for Jira synchronization", "Integration"),
            ("Email", "SaaS Founder", "Dashboard queries experience latency delays", "Bug")
        ]
        cursor.executemany("INSERT INTO feedback (source, user_type, feedback_text, category) VALUES (?, ?, ?, ?)", seed_data)
        conn.commit()

@st.cache_data(ttl=30)
def fetch_customer_feedback_db(category: str = "All", search_query: str = "") -> pd.DataFrame:
    conn = get_db_connection()
    query = "SELECT id AS ID, source AS Source, user_type AS User, feedback_text AS Feedback, category AS Category FROM feedback WHERE 1=1"
    params = []
    
    if category != "All":
        query += " AND category = ?"
        params.append(category)
        
    if search_query:
        query += " AND feedback_text LIKE ?"
        params.append(f"%{search_query}%")
        
    return pd.read_sql_query(query, conn, params=params)

def insert_customer_feedback_db(source: str, user_type: str, feedback_text: str, category: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedback (source, user_type, feedback_text, category) VALUES (?, ?, ?, ?)",
                   (source, user_type, feedback_text, category))
    conn.commit()
    st.cache_data.clear()
