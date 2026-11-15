from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.vault.reader import get_all_notes, get_note_content
from app.vault.writer import save_note, delete_note
from app.vault.graph import generate_graph_data
from app.vault.git_engine import git_history

router = APIRouter(prefix="/api/vault", tags=["Vault"])

class NotePayload(BaseModel):
    path: str
    content: str
    commit_msg: Optional[str] = None

@router.get("/notes")
def list_notes():
    return {"notes": get_all_notes()}

@router.get("/note")
def read_note(path: str = Query(...)):
    content = get_note_content(path)
    if content is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy ghi chú")
    return {"path": path, "content": content}

@router.post("/note")
def write_note(payload: NotePayload):
    success = save_note(payload.path, payload.content, payload.commit_msg)
    if not success:
        raise HTTPException(status_code=500, detail="Lưu ghi chú thất bại")
    return {"status": "success", "path": payload.path}

@router.delete("/note")
def remove_note(path: str = Query(...)):
    success = delete_note(path)
    if not success:
        raise HTTPException(status_code=500, detail="Xóa ghi chú thất bại")
    return {"status": "success"}

@router.get("/graph")
def get_graph():
    return generate_graph_data()

@router.get("/history")
def get_history(limit: int = 10):
    return {"history": git_history(limit)}
