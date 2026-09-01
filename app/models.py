# app/models.py
#
# WHY THIS FILE EXISTS:
# Step 1 of this project used a plain Python list to store tasks —
# that data disappeared every time the app restarted. Real applications
# need PERSISTENT storage. We use SQLite here because:
#   1. It ships built into Python (no extra server to install)
#   2. It's a real SQL database — same concepts as PostgreSQL/MySQL
#   3. It's perfect for learning before moving to a "real" DB server
#      in a future step (e.g., when we add Docker Compose with Postgres)
#
# WHERE THIS IS USED IN COMPANIES:
# Small internal tools, prototypes, and even some production services
# use SQLite. Larger companies use PostgreSQL/MySQL, but the SQL
# concepts (CREATE TABLE, INSERT, SELECT) are identical.

import sqlite3
from app.config import Config


def get_connection():
    """
    Opens a new connection to the SQLite database file.
    check_same_thread=False allows Flask's multiple worker threads
    to use this connection safely for our simple use case.
    """
    conn = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # lets us access columns by name
    return conn


def init_db():
    """
    Creates the 'tasks' table if it doesn't already exist.
    This function is safe to call every time the app starts —
    'IF NOT EXISTS' prevents errors on repeated runs.
    """
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


def get_all_tasks():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_task_by_id(task_id: int):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_task(title: str):
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, 0)", (title,)
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return get_task_by_id(task_id)


def update_task(task_id: int, done: bool):
    conn = get_connection()
    conn.execute("UPDATE tasks SET done = ? WHERE id = ?", (int(done), task_id))
    conn.commit()
    conn.close()
    return get_task_by_id(task_id)


def delete_task(task_id: int):
    conn = get_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
