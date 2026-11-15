import sqlite3
import json
import time
from typing import List, Dict, Any, Optional
from app.core.config import settings

def get_db():
    conn = sqlite3.connect(settings.DB_PATH)
    conn.row_factory = sqlite3.Row
    # Tối ưu hóa SQLite cho hiệu năng cao: WAL mode + synchronous NORMAL
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = NORMAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db()
    with conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            tool_calls TEXT,
            created_at REAL NOT NULL,
            FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS kanban_tasks (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT NOT NULL DEFAULT 'todo', -- 'todo', 'in_progress', 'done'
            priority TEXT NOT NULL DEFAULT 'medium', -- 'low', 'medium', 'high'
            due_date TEXT,
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS mcp_connections (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'connected', -- 'connected', 'disabled'
            perm TEXT NOT NULL DEFAULT 'safe', -- 'readonly', 'safe', 'full'
            config_json TEXT,
            created_at REAL NOT NULL
        );

        CREATE TABLE IF NOT EXISTS mcp_audit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            connector TEXT NOT NULL,
            tool TEXT NOT NULL,
            args TEXT,
            perm TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at REAL NOT NULL
        );
        """)
        
        # Thêm kết nối mẫu mặc định nếu chưa có
        cursor = conn.execute("SELECT COUNT(*) FROM mcp_connections")
        if cursor.fetchone()[0] == 0:
            now = time.time()
            conn.executemany("""
            INSERT INTO mcp_connections (id, name, category, status, perm, config_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                ("zalo", "Zalo Agent MCP", "Tin nhắn & CSKH", "connected", "full", json.dumps({"account": "Trey Pham"}), now),
                ("facebook", "Facebook Fanpage Graph API", "Mạng xã hội & Ads", "connected", "full", json.dumps({"page_id": "phamquangdai"}), now),
                ("sheets", "Google Sheets MCP", "Dữ liệu & Báo cáo", "connected", "safe", json.dumps({}), now),
                ("terminal", "Local Terminal Sandbox", "Hệ thống", "connected", "safe", json.dumps({}), now)
            ])
    conn.close()
