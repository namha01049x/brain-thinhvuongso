from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.database import get_db

router = APIRouter(prefix="/api/mcp", tags=["MCP"])

class PermUpdatePayload(BaseModel):
    connector_id: str
    perm: str # 'readonly', 'safe', 'full'

@router.get("/connections")
def list_connections():
    conn = get_db()
    cursor = conn.execute("SELECT * FROM mcp_connections ORDER BY created_at ASC")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"connections": items}

@router.post("/perm")
def update_permission(payload: PermUpdatePayload):
    if payload.perm not in ["readonly", "safe", "full"]:
        raise HTTPException(status_code=400, detail="Quyền không hợp lệ")
    conn = get_db()
    with conn:
        conn.execute("UPDATE mcp_connections SET perm = ? WHERE id = ?", (payload.perm, payload.connector_id))
    conn.close()
    return {"status": "success", "connector_id": payload.connector_id, "perm": payload.perm}

@router.get("/audit")
def list_audit(limit: int = 20):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM mcp_audit ORDER BY created_at DESC LIMIT ?", (limit,))
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"audit_logs": logs}
