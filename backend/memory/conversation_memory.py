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
                "SELECT user_message, assistant_response FROM chat_messages ORDER BY id ASC"
            ).fetchall()
        except Exception:
            rows = []
        finally:
            conn.close()

        history = []
        if not rows:
            return [{
                "role": "assistant",
                "content": "Hi! I am your AI Product Manager Copilot. How can I assist you today?"
            }]

        for row in rows:
            if row["user_message"]:
                history.append({"role": "user", "content": row["user_message"]})
            if row["assistant_response"]:
                history.append({"role": "assistant", "content": row["assistant_response"]})
        return history

    @staticmethod
    def add_message(role: str, content: str):
        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()
        try:
            if role == "user":
                conn.execute(
                    "INSERT INTO chat_messages (chat_id, user_message, created_at) VALUES (?, ?, ?)",
                    (str(uuid.uuid4()), content, datetime.utcnow().isoformat())
                )
            elif role == "assistant":
                cursor = conn.execute("SELECT id FROM chat_messages WHERE assistant_response IS NULL ORDER BY id DESC LIMIT 1")
                row = cursor.fetchone()
                if row:
                    conn.execute("UPDATE chat_messages SET assistant_response = ? WHERE id = ?", (content, row["id"]))
                else:
                    conn.execute(
                        "INSERT INTO chat_messages (chat_id, assistant_response, created_at) VALUES (?, ?, ?)",
                        (str(uuid.uuid4()), content, datetime.utcnow().isoformat())
                    )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def clear_memory():
        db_mgr = DatabaseManager()
        conn = db_mgr.get_connection()
        try:
            conn.execute("DELETE FROM chat_messages")
            conn.commit()
        finally:
            conn.close()