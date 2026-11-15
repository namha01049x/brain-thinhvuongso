import sqlite3
import time
import uuid
from typing import List, Dict, Any, Optional
from app.core.database import get_db

# Khởi tạo bảng công việc theo timeline thời gian tương tự Javis OS (Ảnh 2)
def init_advanced_tasks():
    conn = get_db()
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS timeline_tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            time_str TEXT NOT NULL,
            date_group TEXT NOT NULL,
            schedule_type TEXT,
            assistant TEXT NOT NULL,
            assistant_avatar TEXT,
            owner_type TEXT NOT NULL DEFAULT 'javis', -- 'javis' hoặc 'mine'
            status TEXT NOT NULL DEFAULT 'upcoming', -- 'upcoming', 'today', 'done', 'recurring'
            created_at REAL NOT NULL
        );
        """)
        cursor = conn.execute("SELECT COUNT(*) FROM timeline_tasks")
        if cursor.fetchone()[0] == 0:
            now = time.time()
            sample_tasks = [
                ("t1", "Add the class recording to the Wiki", "05:30", "Tomorrow 6/11", "5:30 Sun, Mon, Wed, Fri weekly", "Javis Vu | Customer Care", "👨‍💼", "javis", "upcoming", now),
                ("t2", "Reminder: brainstorm the work plan", "08:00", "Tomorrow 6/11", "Remind only", "Javis Core", "⚡", "javis", "upcoming", now),
                ("t3", "Keep the unpaid-order follow-up campaign running", "09:00", "Tomorrow 6/11", "9:00 daily", "Javis Core", "⚡", "javis", "upcoming", now),
                ("t4", "JAVISER: morning reminder for Tue/Thu meetups", "09:00", "Tuesday, 10/11", "9:00 Tue, Thu weekly", "Javis Core", "⚡", "javis", "upcoming", now),
                ("t5", "JAVISER: send the Meet link at 19:30 Tue/Thu", "19:30", "Tuesday, 10/11", "19:30 Tue, Thu weekly", "Javis Core", "⚡", "javis", "upcoming", now),
                ("t6", "Review Facebook Ads CPA & scale budget", "14:00", "Today", "Daily review", "Bao - Conversion Specialist", "📈", "mine", "today", now),
                ("t7", "Record short reel on 5-step value ladder", "16:30", "Today", "Weekly content", "Pham Quang Dai", "👤", "mine", "today", now)
            ]
            conn.executemany("""
            INSERT INTO timeline_tasks (id, title, time_str, date_group, schedule_type, assistant, assistant_avatar, owner_type, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, sample_tasks)
    conn.close()

init_advanced_tasks()

def get_timeline_tasks(owner_type: Optional[str] = None, filter_status: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db()
    query = "SELECT * FROM timeline_tasks WHERE 1=1"
    params = []
    if owner_type and owner_type != "all":
        query += " AND owner_type = ?"
        params.append(owner_type)
    if filter_status and filter_status != "all":
        query += " AND status = ?"
        params.append(filter_status)
    query += " ORDER BY date_group ASC, time_str ASC"
    cursor = conn.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows

def toggle_task_done(task_id: str) -> bool:
    conn = get_db()
    with conn:
        conn.execute("UPDATE timeline_tasks SET status = CASE WHEN status = 'done' THEN 'upcoming' ELSE 'done' END WHERE id = ?", (task_id,))
    conn.close()
    return True

# Backward compatibility aliases
get_kanban_tasks = get_timeline_tasks

def create_kanban_task(title: str, description: str = "", priority: str = "medium", due_date: str = "") -> Dict[str, Any]:
    task_id = str(uuid.uuid4())[:8]
    now = time.time()
    conn = get_db()
    with conn:
        conn.execute("""
        INSERT INTO timeline_tasks (id, title, time_str, date_group, schedule_type, assistant, assistant_avatar, owner_type, status, created_at)
        VALUES (?, ?, '09:00', 'Today', 'Ad-hoc', 'Javis Core', '⚡', 'mine', 'today', ?)
        """, (task_id, title, now))
    conn.close()
    return {"id": task_id, "title": title, "status": "today"}

def update_task_status(task_id: str, status: str) -> bool:
    conn = get_db()
    with conn:
        conn.execute("UPDATE timeline_tasks SET status = ? WHERE id = ?", (status, task_id))
    conn.close()
    return True

def delete_kanban_task(task_id: str) -> bool:
    conn = get_db()
    with conn:
        conn.execute("DELETE FROM timeline_tasks WHERE id = ?", (task_id,))
    conn.close()
    return True
