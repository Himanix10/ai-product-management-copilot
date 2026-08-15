import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd

from backend.config import config


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)

        return cls._instance

    def get_connection(self):
        conn = sqlite3.connect(
            config.DATABASE_PATH,
            check_same_thread=False
        )

        conn.row_factory = sqlite3.Row

        return conn


def init_db():
    from create_db import build_database

    build_database()


# ============================================================
# FEEDBACK
# ============================================================

def fetch_customer_feedback_db(
    category: str = "All",
    search_query: str = ""
) -> pd.DataFrame:

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    query = """
        SELECT
            feedback_id AS ID,
            source AS Source,
            user_name AS User,
            feedback_text AS Feedback,
            theme AS Category,
            sentiment AS Sentiment,
            priority AS Priority,
            status AS Status,
            feature_request AS Feature_Request,
            rice_score AS RICE_Score
        FROM feedback
        WHERE 1 = 1
    """

    params = []

    if category and category != "All":
        query += " AND theme = ?"
        params.append(category)

    if search_query:
        query += """
            AND (
                feedback_text LIKE ?
                OR user_name LIKE ?
                OR theme LIKE ?
            )
        """

        search_term = f"%{search_query}%"

        params.extend(
            [
                search_term,
                search_term,
                search_term,
            ]
        )

    query += " ORDER BY feedback_timestamp DESC"

    try:
        return pd.read_sql_query(
            query,
            conn,
            params=params
        )
    finally:
        conn.close()


def insert_customer_feedback_db(
    source: str,
    user_type: str,
    feedback_text: str,
    category: str
):

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    try:
        feedback_id = f"FB-{uuid.uuid4().hex[:8].upper()}"

        conn.execute(
            """
            INSERT INTO feedback (
                user_id,
                feedback_id,
                user_name,
                feedback_timestamp,
                source,
                feedback_text,
                theme,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "streamlit-user",
                feedback_id,
                user_type,
                datetime.utcnow().isoformat(),
                source,
                feedback_text,
                category,
                "New",
            ),
        )

        conn.commit()

    finally:
        conn.close()


# ============================================================
# PAIN POINTS
# ============================================================

def fetch_pain_points_db(
    severity: str = "All",
    search_query: str = ""
) -> pd.DataFrame:

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    query = """
        SELECT
            cluster_id AS 'Cluster ID',
            theme_name AS 'Pain Point Area',
            category AS 'Category',
            description AS 'Impact Area',
            feedback_count AS 'Support Volume',
            priority_level AS 'Severity',
            status AS Status,
            owner AS Owner
        FROM pain_points
        WHERE 1 = 1
    """

    params = []

    if severity and severity != "All":
        query += " AND priority_level = ?"
        params.append(severity)

    if search_query:
        query += """
            AND (
                theme_name LIKE ?
                OR description LIKE ?
                OR category LIKE ?
            )
        """

        search_term = f"%{search_query}%"

        params.extend(
            [search_term, search_term, search_term]
        )

    query += " ORDER BY feedback_count DESC"

    try:
        return pd.read_sql_query(
            query,
            conn,
            params=params
        )
    finally:
        conn.close()


# ============================================================
# INITIATIVES
# ============================================================

def save_initiative_db(
    title: str,
    reach: float,
    impact: float,
    confidence: float,
    effort: float,
    rice_score: float,
    status: str = "Planned"
):

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    try:
        initiative_id = f"INIT-{uuid.uuid4().hex[:8].upper()}"

        conn.execute(
            """
            INSERT INTO initiatives (
                initiative_id,
                feature_name,
                reach,
                impact,
                confidence,
                effort,
                rice_score,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                initiative_id,
                title,
                reach,
                impact,
                confidence,
                effort,
                rice_score,
                status,
            ),
        )

        conn.commit()

    finally:
        conn.close()


def fetch_initiatives_db() -> pd.DataFrame:

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    query = """
        SELECT
            initiative_id AS ID,
            feature_name AS Title,
            theme AS Theme,
            reach AS Reach,
            impact AS Impact,
            confidence AS Confidence,
            effort AS Effort,
            rice_score AS 'RICE Score',
            priority_level AS Priority,
            status AS Status,
            target_quarter AS 'Target Quarter',
            owner AS Owner
        FROM initiatives
        ORDER BY rice_score DESC
    """

    try:
        return pd.read_sql_query(
            query,
            conn
        )
    finally:
        conn.close()


# ============================================================
# PRDs
# ============================================================

def save_prd_db(
    feature_name: str,
    target_persona: str,
    problem: str,
    requirements: str,
    markdown: str
):

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    try:
        prd_id = f"PRD-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.utcnow().isoformat()

        conn.execute(
            """
            INSERT INTO prds (
                prd_id,
                title,
                executive_summary,
                problem_statement,
                objectives,
                user_personas,
                user_stories,
                functional_requirements,
                non_functional_requirements,
                acceptance_criteria,
                success_metrics,
                risks,
                open_questions,
                priority,
                owner,
                estimated_effort,
                rice_score,
                status,
                created_at,
                updated_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """,
            (
                prd_id,
                feature_name,
                markdown[:500],
                problem,
                "",
                target_persona,
                "",
                requirements,
                "",
                "",
                "",
                "",
                "",
                "P1",
                "AI Product Manager",
                None,
                None,
                "Draft",
                now,
                now,
            ),
        )

        conn.commit()

    finally:
        conn.close()


def fetch_prds_db() -> pd.DataFrame:

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    try:
        return pd.read_sql_query(
            """
            SELECT
                prd_id AS ID,
                title AS Title,
                executive_summary AS Summary,
                problem_statement AS Problem,
                user_personas AS Personas,
                functional_requirements AS Requirements,
                priority AS Priority,
                owner AS Owner,
                status AS Status,
                created_at AS Created
            FROM prds
            ORDER BY created_at DESC
            """,
            conn
        )

    finally:
        conn.close()


# ============================================================
# ROADMAP
# ============================================================

def fetch_roadmap_db() -> pd.DataFrame:

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    try:
        return pd.read_sql_query(
            """
            SELECT
                roadmap_id AS ID,
                initiative_id AS Initiative_ID,
                title AS Initiative,
                theme AS Theme,
                quarter AS Quarter,
                target_release AS Release,
                owner AS Owner,
                engineering_team AS Team,
                priority AS Priority,
                status AS Status,
                progress_percentage AS Progress,
                milestone AS Milestone,
                risk_level AS Risk,
                business_goal AS Business_Goal,
                success_metric AS Success_Metric
            FROM roadmap
            ORDER BY
                quarter,
                progress_percentage DESC
            """,
            conn
        )

    finally:
        conn.close()


# ============================================================
# DASHBOARD ANALYTICS
# ============================================================

def get_feedback_monthly_counts():

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    try:
        query = """
            SELECT
                substr(feedback_timestamp, 1, 7) AS Month,
                COUNT(*) AS 'Feedback Volume'
            FROM feedback
            WHERE feedback_timestamp IS NOT NULL
            GROUP BY substr(feedback_timestamp, 1, 7)
            ORDER BY Month
        """

        return pd.read_sql_query(
            query,
            conn
        )

    finally:
        conn.close()


def get_pain_point_summary():

    db_mgr = DatabaseManager()
    conn = db_mgr.get_connection()

    try:
        query = """
            SELECT
                theme_name AS 'Pain Area',
                SUM(feedback_count) AS 'Support Volume'
            FROM pain_points
            GROUP BY theme_name
            ORDER BY 'Support Volume' DESC
            LIMIT 10
        """

        return pd.read_sql_query(
            query,
            conn
        )

    finally:
        conn.close()