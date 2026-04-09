"""
Simple chat storage for conversation context
"""

import json
import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class ChatStorage:
    """Simple chat storage for conversation context."""

    def __init__(self, storage_dir: str = "chat_logs"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.db_path = self.storage_dir / "conversations.db"
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    channel TEXT NOT NULL,
                    thread_ts TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_thread ON messages (channel, thread_ts)"
            )

    def store_message(
        self,
        channel: str,
        thread_ts: str,
        user_id: str,
        message: str,
        role: str = "user"
    ) -> None:
        """Store a message in the database."""
        try:
            timestamp = datetime.now().isoformat()

            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT INTO messages (channel, thread_ts, user_id, role, message, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (channel, thread_ts, user_id, role, message, timestamp))

            logger.debug(f"Stored {role} message for thread {thread_ts}")

        except Exception as e:
            logger.error(f"Error storing message: {e}")

    def get_thread_context(
        self,
        channel: str,
        thread_ts: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get recent messages from a thread for context."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("""
                    SELECT * FROM messages
                    WHERE channel = ? AND thread_ts = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (channel, thread_ts, limit))

                messages = []
                for row in cursor.fetchall():
                    messages.append({
                        "user_id": row["user_id"],
                        "role": row["role"],
                        "message": row["message"],
                        "timestamp": row["timestamp"]
                    })

                # Return in chronological order (oldest first)
                return list(reversed(messages))

        except Exception as e:
            logger.error(f"Error getting thread context: {e}")
            return []