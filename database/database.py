import sqlite3
import os
from config import DATABASE_PATH


def get_db_connection():
    """Create and return a database connection."""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER,
            role TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    print("[OK] Database initialized successfully.")


def create_conversation(title="New Chat"):
    """Create a new conversation and return its ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO conversations (title) VALUES (?)", (title,))
    conn.commit()
    conv_id = cursor.lastrowid
    conn.close()
    return conv_id


def update_conversation_title(conv_id, title):
    """Update the title of a conversation."""
    conn = get_db_connection()
    conn.execute("UPDATE conversations SET title = ? WHERE id = ?", (title[:60], conv_id))
    conn.commit()
    conn.close()


def get_all_conversations():
    """Fetch all conversations ordered by creation date (newest first)."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT id, title, created_at FROM conversations ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_conversation_messages(conv_id):
    """Fetch all messages for a given conversation."""
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT role, message, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC",
        (conv_id,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def save_message(conv_id, role, message):
    """Save a message to the database."""
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO messages (conversation_id, role, message) VALUES (?, ?, ?)",
        (conv_id, role, message)
    )
    conn.commit()
    conn.close()


def delete_conversation(conv_id):
    """Delete a conversation and all its messages."""
    conn = get_db_connection()
    conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
    conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    conn.close()


def get_conversation_by_id(conv_id):
    """Fetch a single conversation by ID."""
    conn = get_db_connection()
    row = conn.execute(
        "SELECT id, title, created_at FROM conversations WHERE id = ?", (conv_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None
