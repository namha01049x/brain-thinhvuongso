import json
import time
import uuid
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.database import get_db
from app.engine.router import stream_chat_turn

router = APIRouter(tags=["Chat"])

@router.get("/api/chat/sessions")
def list_sessions():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM sessions ORDER BY updated_at DESC")
    sessions = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"sessions": sessions}

@router.get("/api/chat/messages")
def get_messages(session_id: str):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM messages WHERE session_id = ? ORDER BY created_at ASC", (session_id,))
    messages = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"messages": messages}

@router.websocket("/ws")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data_text = await websocket.receive_text()
            try:
                data = json.loads(data_text)
            except Exception:
                continue

            action = data.get("action")
            session_id = data.get("session_id") or str(uuid.uuid4())[:8]
            prompt = data.get("prompt", "").strip()
            provider = data.get("provider", "claude-code")

            if action == "ping":
                await websocket.send_text(json.dumps({"type": "pong"}))
                continue

            if not prompt:
                continue

            # Đảm bảo session tồn tại
            conn = get_db()
            with conn:
                cursor = conn.execute("SELECT id FROM sessions WHERE id = ?", (session_id,))
                if not cursor.fetchone():
                    now = time.time()
                    title = prompt[:30] + ("..." if len(prompt) > 30 else "")
                    conn.execute("INSERT INTO sessions (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
                                 (session_id, title, now, now))
                else:
                    conn.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (time.time(), session_id))
            conn.close()

            # Bắt đầu stream phản hồi AI
            async for chunk in stream_chat_turn(session_id, prompt, provider):
                await websocket.send_text(json.dumps(chunk))

    except WebSocketDisconnect:
        pass
