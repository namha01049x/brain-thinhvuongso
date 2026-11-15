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

# Self-Learning & Auto-Distillation API (Tailored for MLM BRAIN 4.0)
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
            "source": "06 - Sources/Hội thoại thực chiến đối đầu khách so sánh hàng Shopee.md",
            "distilled_to": "07 - Wiki/Kịch bản hóa giải phá giá & cam kết đồng hành 1-1.md",
            "insight": "Khách chê đắt hơn Shopee không phải vì thiếu tiền mà vì chưa thấy giá trị của người bảo trợ đồng hành quét chỉ số Tanita và thực đơn cá nhân hóa mỗi tuần.",
            "category": "XỬ LÝ TỪ CHỐI / SHOPEE",
            "confidence": 0.98,
            "time_ago": "15 phút trước"
        },
        {
            "id": "distill-2",
            "source": "06 - Sources/Case Study F1 vượt qua gia đình cấm cản đa cấp.md",
            "distilled_to": "07 - Wiki/Quy tắc hạ nhiệt phòng thủ & mượn lực bên thứ 3.md",
            "insight": "Không tranh luận đúng sai với người thân; dùng kết quả vóc dáng và sự thay đổi thái độ sống tích cực làm bằng chứng thực chứng sau 21 ngày.",
            "category": "TÂM LÝ HỌC / GIA ĐÌNH",
            "confidence": 0.96,
            "time_ago": "2 giờ trước"
        },
        {
            "id": "distill-3",
            "source": "05 - Knowledge/Mo hinh CLB Dinh Duong 30 khach moi ngay.md",
            "distilled_to": "07 - Wiki/Quy trình vận hành 21 chủ đề dinh dưỡng chuẩn mực.md",
            "insight": "Duy trì văn hóa chào đón và khen ngợi thành viên mỗi sáng tại CLB giúp tỷ lệ tái ký gói tháng đạt trên 85% mà không cần chào mời.",
            "category": "VẬN HÀNH / CLB & FIT",
            "confidence": 0.97,
            "time_ago": "1 ngày trước"
        },
        {
            "id": "distill-4",
            "source": "06 - Sources/Ghi chép đào tạo Top Leader Eric Worre NMPRO.md",
            "distilled_to": "07 - Wiki/10 Nguyen tac danh du ProCode & Kỷ luật 2-a-Day.md",
            "insight": "Người nghiệp dư cố trở thành chuyên gia thuyết trình; Người chuyên nghiệp dùng công cụ bên thứ ba (Video 5 phút, Form chẩn đoán) để ai cũng nhân bản được.",
            "category": "NHÂN BẢN / PROCODE",
            "confidence": 0.99,
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
