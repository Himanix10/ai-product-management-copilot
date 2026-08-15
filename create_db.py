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
}


def create_users_table(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'Product Manager'
        )
        """
    )


def seed_default_user(conn):
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        password_hash = bcrypt.hashpw(
            "password123".encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        cursor.execute(
            """
            INSERT INTO users
            (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            """,
            (
                "pradeepthi",
                "pradeepthi297@gmail.com",
                password_hash,
                "Product Manager",
            ),
        )


def table_exists(conn, table_name):
    cursor = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name = ?
        """,
        (table_name,),
    )

    return cursor.fetchone() is not None


def table_has_rows(conn, table_name):
    if not table_exists(conn, table_name):
        return False

    cursor = conn.execute(
        f"SELECT COUNT(*) FROM [{table_name}]"
    )

    return cursor.fetchone()[0] > 0


def load_excel_tables_if_missing(conn):
    """
    Load the expanded Excel database only when the corresponding
    SQLite table does not exist or is empty.

    IMPORTANT:
    We never replace populated application tables on every startup.
    """

    if not EXCEL_PATH.exists():
        print(f"Excel database not found: {EXCEL_PATH}")
        return

    excel = pd.ExcelFile(EXCEL_PATH)

    for sheet_name, table_name in SHEET_MAPPING.items():

        if sheet_name not in excel.sheet_names:
            print(
                f"Skipping missing sheet: {sheet_name}"
            )
            continue

        if table_has_rows(conn, table_name):
            print(
                f"Keeping existing table '{table_name}'. "
                f"No replacement performed."
            )
            continue

        df = pd.read_excel(
            excel,
            sheet_name=sheet_name
        )

        if df.empty:
            print(
                f"Sheet '{sheet_name}' is empty."
            )
            continue

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(
            f"Loaded {len(df):,} records "
            f"into '{table_name}'."
        )


def create_empty_fallback_tables(conn):
    """
    Creates minimal tables only when the Excel database
    is unavailable.
    """

    fallback_tables = {
        "feedback": """
            CREATE TABLE IF NOT EXISTS feedback (
                feedback_id TEXT PRIMARY KEY,
                source TEXT,
                user_name TEXT,
                feedback_text TEXT,
                theme TEXT
            )
        """,

        "pain_points": """
            CREATE TABLE IF NOT EXISTS pain_points (
                cluster_id TEXT PRIMARY KEY,
                theme_name TEXT,
                category TEXT,
                description TEXT,
                feedback_count INTEGER,
                priority_level TEXT
            )
        """,

        "initiatives": """
            CREATE TABLE IF NOT EXISTS initiatives (
                initiative_id TEXT PRIMARY KEY,
                feature_name TEXT,
                theme TEXT,
                reach REAL,
                impact REAL,
                confidence REAL,
                effort REAL,
                rice_score REAL,
                status TEXT
            )
        """,

        "prds": """
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
                created_at TEXT,
                updated_at TEXT
            )
        """,

        "roadmap": """
            CREATE TABLE IF NOT EXISTS roadmap (
                roadmap_id TEXT PRIMARY KEY,
                initiative_id TEXT,
                title TEXT,
                theme TEXT,
                quarter TEXT,
                target_release TEXT,
                start_date TEXT,
                end_date TEXT,
                owner TEXT,
                engineering_team TEXT,
                priority TEXT,
                status TEXT,
                progress_percentage INTEGER,
                dependencies TEXT,
                milestone TEXT,
                estimated_effort INTEGER,
                risk_level TEXT,
                business_goal TEXT,
                success_metric TEXT,
                notes TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        """,

        "chat_messages": """
            CREATE TABLE IF NOT EXISTS chat_messages (
                chat_id TEXT PRIMARY KEY,
                session_id TEXT,
                user_id TEXT,
                user_name TEXT,
                timestamp TEXT,
                user_message TEXT,
                assistant_response TEXT,
                detected_intent TEXT,
                agent_used TEXT,
                confidence_score REAL,
                execution_time_ms INTEGER,
                tokens_used INTEGER,
                feedback_reference TEXT,
                theme_reference TEXT,
                prd_reference TEXT,
                roadmap_reference TEXT,
                initiative_reference TEXT,
                conversation_status TEXT,
                satisfaction_rating INTEGER,
                created_at TEXT
            )
        """,
    }

    for query in fallback_tables.values():
        conn.execute(query)


def build_database():
    DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(str(DATABASE_PATH))

    try:
        create_users_table(conn)
        seed_default_user(conn)

        if EXCEL_PATH.exists():
            load_excel_tables_if_missing(conn)
        else:
            create_empty_fallback_tables(conn)

        conn.commit()

        print(
            "\nDatabase initialization completed successfully."
        )
        print(f"Database: {DATABASE_PATH}")

    finally:
        conn.close()


if __name__ == "__main__":
    build_database()