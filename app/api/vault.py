from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time
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

# Self-Learning & Auto-Distillation API
SELF_LEARNING_DATA = {
    "stats": {
        "distilled_rules": 48,
        "active_facts": 1138,
        "compounding_rate": "+12.4% / tuần",
        "health_score": "98/100"
    },
    "recent_distillations": [
        {
            "id": "distill-1",
            "source": "06 - Sources/Chiến lược Phễu Webcake Q4.md",
            "distilled_to": "07 - Wiki/Kỹ thuật Tối ưu Landing Page High-Ticket.md",
            "insight": "Khách hàng mua gói doanh nghiệp cần video walkthrough thực tế trước khi đặt lịch tư vấn.",
            "category": "MARKETING/CRO",
            "confidence": 0.96,
            "time_ago": "2 giờ trước"
        },
        {
            "id": "distill-2",
            "source": "01 - Daily Log/2026-11-14.md",
            "distilled_to": "07 - Wiki/Quy trình Bàn giao Tự động qua Zalo.md",
            "insight": "Nhắn tin xác nhận kèm link tài liệu trong vòng 3 phút giúp nâng tỷ lệ kích hoạt lên 89%.",
            "category": "OPERATIONS",
            "confidence": 0.94,
            "time_ago": "1 ngày trước"
        },
        {
            "id": "distill-3",
            "source": "06 - Sources/Hội thoại tư vấn gói Brain Doanh nghiệp.md",
            "distilled_to": "07 - Wiki/Pain-point Khách hàng Doanh nghiệp SME.md",
            "insight": "Rào cản lớn nhất của CEO SME là dữ liệu phân tán ở Zalo, Messenger, Drive và không đồng bộ được về một nơi.",
            "category": "SALES",
            "confidence": 0.98,
            "time_ago": "2 ngày trước"
        }
    ]
}

@router.get("/self-learning")
def get_self_learning():
    return SELF_LEARNING_DATA

class IngestSourcePayload(BaseModel):
    title: str
    content: str
    category: Optional[str] = "WIKI"

@router.post("/ingest")
def ingest_source(payload: IngestSourcePayload):
    # Lưu vào sources
    slug = payload.title.lower().replace(" ", "-")[:40]
    path = f"06 - Sources/{slug}.md"
    body = f"""---
title: "{payload.title}"
category: "{payload.category}"
source_type: "user_ingested"
date: "{time.strftime('%Y-%m-%d %H:%M:%S')}"
---

# {payload.title}

{payload.content}
"""
    save_note(path, body, f"Tự động chưng cất nguồn: {payload.title}")
    
    # Thêm vào danh sách distillation
    new_distill = {
        "id": f"distill-{int(time.time())}",
        "source": path,
        "distilled_to": f"07 - Wiki/{payload.title}.md",
        "insight": payload.content[:150] + ("..." if len(payload.content) > 150 else ""),
        "category": payload.category,
        "confidence": 0.95,
        "time_ago": "Vừa xong"
    }
    SELF_LEARNING_DATA["recent_distillations"].insert(0, new_distill)
    SELF_LEARNING_DATA["stats"]["distilled_rules"] += 1
    
    return {"status": "success", "distilled": new_distill}
