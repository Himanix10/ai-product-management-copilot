from datetime import datetime, timezone
from backend.database.db import DatabaseManager


class ConversationMemory:
    """Persistent SQLite conversation memory using ROWID for 100% schema resilience."""

    @staticmethod
    def _default_chat_id(user=None):
        if isinstance(user, dict):
            user_id = user.get("id")
            if user_id is not None:
                return f"user:{user_id}"
            email = user.get("email")
            if email:
                return f"email:{email.strip().lower()}"
        return "anonymous"

    @classmethod
    def get_chat_id(cls, user=None):
        return cls._default_chat_id(user)

    @classmethod
    def get_history(cls, user=None, limit=None):
        chat_id = cls.get_chat_id(user)
        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:
            rows = conn.execute(
                """
                SELECT
                    user_message,
                    assistant_response
                FROM chat_messages
                WHERE chat_id = ?
                ORDER BY ROWID ASC
                """,
                (chat_id,),
            ).fetchall()
        except Exception:
            rows = []
        finally:
            conn.close()

        history = []
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

        if limit and limit > 0:
            history = history[-limit:]

        return history

    @classmethod
    def add_message(cls, role: str, content: str, user=None):
        content = (content or "").strip()
        if not content:
            return

        if role not in {"user", "assistant"}:
            return

        chat_id = cls.get_chat_id(user)
        now = datetime.now(timezone.utc).isoformat()

        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:
            if role == "user":
                conn.execute(
                    """
                    INSERT INTO chat_messages
                    (
                        chat_id,
                        user_message,
                        assistant_response,
                        created_at
                    )
                    VALUES (?, ?, NULL, ?)
                    """,
                    (chat_id, content, now),
                )
            else:
                row = conn.execute(
                    """
                    SELECT ROWID as id
                    FROM chat_messages
                    WHERE chat_id = ?
                      AND assistant_response IS NULL
                    ORDER BY ROWID DESC
                    LIMIT 1
                    """,
                    (chat_id,),
                ).fetchone()

                if row:
                    conn.execute(
                        """
                        UPDATE chat_messages
                        SET assistant_response = ?
                        WHERE ROWID = ?
                        """,
                        (content, row["id"]),
                    )
                else:
                    conn.execute(
                        """
                        INSERT INTO chat_messages
                        (
                            chat_id,
                            user_message,
                            assistant_response,
                            created_at
                        )
                        VALUES (?, NULL, ?, ?)
                        """,
                        (chat_id, content, now),
                    )

            conn.commit()
        finally:
            conn.close()

    @classmethod
    def clear_memory(cls, user=None):
        chat_id = cls.get_chat_id(user)
        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()

        try:
            conn.execute(
                """
                DELETE FROM chat_messages
                WHERE chat_id = ?
                """,
                (chat_id,),
            )
            conn.commit()
        finally:
            conn.close()