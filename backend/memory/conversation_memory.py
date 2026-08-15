import uuid
from datetime import datetime

from backend.database.db import DatabaseManager


class ConversationMemory:

    @staticmethod
    def get_history():

        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:

            rows = conn.execute(
                """
                SELECT
                    user_message,
                    assistant_response
                FROM chat_messages
                WHERE user_message IS NOT NULL
                ORDER BY created_at ASC
                """
            ).fetchall()

        finally:
            conn.close()

        history = []

        if not rows:

            return [
                {
                    "role": "assistant",
                    "content": (
                        "Hi! I am your AI Product Manager "
                        "Copilot powered by Google Gemini. "
                        "How can I assist you today?"
                    ),
                }
            ]

        for row in rows:

            if row["user_message"]:

                history.append(
                    {
                        "role": "user",
                        "content": row["user_message"],
                    }
                )

            if row["assistant_response"]:

                history.append(
                    {
                        "role": "assistant",
                        "content": row["assistant_response"],
                    }
                )

        return history

    @staticmethod
    def add_message(
        role: str,
        content: str
    ):

        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:

            if role == "user":

                conn.execute(
                    """
                    INSERT INTO chat_messages (
                        chat_id,
                        session_id,
                        user_id,
                        user_name,
                        timestamp,
                        user_message,
                        conversation_status,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(uuid.uuid4()),
                        "streamlit-session",
                        "streamlit-user",
                        "Product Manager",
                        datetime.utcnow().isoformat(),
                        content,
                        "active",
                        datetime.utcnow().isoformat(),
                    ),
                )

            elif role == "assistant":

                cursor = conn.execute(
                    """
                    SELECT chat_id
                    FROM chat_messages
                    WHERE assistant_response IS NULL
                    ORDER BY created_at DESC
                    LIMIT 1
                    """
                )

                row = cursor.fetchone()

                if row:

                    conn.execute(
                        """
                        UPDATE chat_messages
                        SET assistant_response = ?
                        WHERE chat_id = ?
                        """,
                        (
                            content,
                            row["chat_id"],
                        ),
                    )

                else:

                    conn.execute(
                        """
                        INSERT INTO chat_messages (
                            chat_id,
                            session_id,
                            user_id,
                            user_name,
                            timestamp,
                            assistant_response,
                            conversation_status,
                            created_at
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            str(uuid.uuid4()),
                            "streamlit-session",
                            "streamlit-user",
                            "Product Manager",
                            datetime.utcnow().isoformat(),
                            content,
                            "active",
                            datetime.utcnow().isoformat(),
                        ),
                    )

            conn.commit()

        finally:
            conn.close()

    @staticmethod
    def clear_memory():

        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:

            conn.execute(
                "DELETE FROM chat_messages"
            )

            conn.commit()

        finally:
            conn.close()