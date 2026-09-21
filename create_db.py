import os
import sqlite3
from pathlib import Path
import bcrypt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "data" / "app.db"
EXCEL_PATH = BASE_DIR / "AI_PM_Copilot_Database_Expanded.xlsx"

SHEET_MAPPING = {
    "Users_Feedback": "feedback",
    "Theme_Clusters": "pain_points",
    "Priority_Initiatives": "initiatives",
    "PRDs": "prds",
    "Roadmap": "roadmap",
    "Chat_History": "chat_messages",
    "Product_Metrics": "product_metrics",
}


def build_database():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DATABASE_PATH))

    try:
        # Users Table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT DEFAULT 'Product Manager'
            )
        """)

        # Fallback Core Tables if Excel is not loaded
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                feedback_id TEXT UNIQUE,
                user_name TEXT,
                feedback_timestamp TEXT,
                source TEXT,
                feedback_text TEXT,
                theme TEXT,
                sentiment TEXT,
                priority TEXT,
                status TEXT,
                rice_score REAL DEFAULT 0.0
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS pain_points (
                cluster_id TEXT PRIMARY KEY,
                theme_name TEXT,
                category TEXT,
                description TEXT,
                feedback_count INTEGER,
                priority_level TEXT,
                status TEXT,
                owner TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS initiatives (
                initiative_id TEXT PRIMARY KEY,
                feature_name TEXT,
                theme TEXT,
                reach REAL,
                impact REAL,
                confidence REAL,
                effort REAL,
                rice_score REAL,
                priority_level TEXT,
                status TEXT,
                target_quarter TEXT,
                owner TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS prds (
                prd_id TEXT PRIMARY KEY,
                title TEXT,
                executive_summary TEXT,
                problem_statement TEXT,
                objectives TEXT,
                user_personas TEXT,
                user_stories TEXT,
                functional_requirements TEXT,
                non_functional_requirements TEXT,
                acceptance_criteria TEXT,
                success_metrics TEXT,
                risks TEXT,
                open_questions TEXT,
                priority TEXT,
                owner TEXT,
                estimated_effort INTEGER,
                rice_score REAL,
                status TEXT,
                markdown_content TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS roadmap (
                roadmap_id TEXT PRIMARY KEY,
                initiative_id TEXT,
                title TEXT,
                theme TEXT,
                quarter TEXT,
                target_release TEXT,
                owner TEXT,
                engineering_team TEXT,
                priority TEXT,
                status TEXT,
                progress_percentage INTEGER,
                milestone TEXT,
                risk_level TEXT,
                business_goal TEXT,
                success_metric TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                user_message TEXT,
                assistant_response TEXT,
                created_at TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS product_metrics (
                metric_id TEXT PRIMARY KEY,
                metric_name TEXT NOT NULL,
                category TEXT NOT NULL,
                metric_value REAL NOT NULL,
                target_value REAL,
                unit TEXT,
                reporting_period TEXT,
                trend TEXT,
                status TEXT,
                owner TEXT,
                related_feature TEXT,
                related_theme TEXT,
                last_updated TEXT
            )
        """)

        # Seed Default User
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            pw_hash = bcrypt.hashpw("password123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES (?, ?, ?, ?)
            """, ("pradeepthi", "pradeepthi297@gmail.com", pw_hash, "Product Manager"))

        # Ingest Excel Tables if present
        if EXCEL_PATH.exists():
            excel = pd.ExcelFile(EXCEL_PATH)
            for sheet_name, table_name in SHEET_MAPPING.items():
                if sheet_name in excel.sheet_names:
                    df = pd.read_excel(excel, sheet_name=sheet_name)
                    df.to_sql(table_name, conn, if_exists="replace", index=False)
                    print(f"Loaded {len(df):,} records into '{table_name}'.")

        conn.commit()
        print("\nDatabase initialization completed successfully.")
    finally:
        conn.close()


if __name__ == "__main__":
    build_database()