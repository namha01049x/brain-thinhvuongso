import sqlite3
import time
import uuid
from typing import List, Dict, Any, Optional
from app.core.database import get_db

def get_kanban_tasks() -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.execute("SELECT * FROM kanban_tasks ORDER BY created_at DESC")
    tasks = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tasks

def create_kanban_task(title: str, description: str = "", priority: str = "medium", due_date: str = "") -> Dict[str, Any]:
    task_id = str(uuid.uuid4())[:8]
    now = time.time()
    conn = get_db()
    with conn:
        conn.execute("""
        INSERT INTO kanban_tasks (id, title, description, status, priority, due_date, created_at, updated_at)
        VALUES (?, ?, ?, 'todo', ?, ?, ?, ?)
        """, (task_id, title, description, priority, due_date, now, now))
    conn.close()
    return {"id": task_id, "title": title, "status": "todo", "priority": priority}

def update_task_status(task_id: str, status: str) -> bool:
    now = time.time()
    conn = get_db()
    with conn:
        conn.execute("UPDATE kanban_tasks SET status = ?, updated_at = ? WHERE id = ?", (status, now, task_id))
    conn.close()
    return True

def delete_kanban_task(task_id: str) -> bool:
    conn = get_db()
    with conn:
        conn.execute("DELETE FROM kanban_tasks WHERE id = ?", (task_id,))
    conn.close()
    return True
