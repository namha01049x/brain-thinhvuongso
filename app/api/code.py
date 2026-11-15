import sys
import io
import traceback
import contextlib
import time
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/api/code", tags=["Code Studio"])

CODE_SNIPPETS = [
    {
        "id": "meta-cpa-audit",
        "title": "Facebook Ads CPA Anomaly Detector",
        "language": "python",
        "description": "Script kiểm tra chiến dịch quảng cáo và tính chi phí trên mỗi lượt mua hàng (CPA).",
        "code": """# Facebook Ads CPA Monitor
def check_cpa(spend: float, conversions: int, target_cpa: float = 85000):
    if conversions == 0:
        return {"status": "BURNING", "cpa": spend, "action": "TẮT CHIẾN DỊCH NGAY"}
    actual_cpa = spend / conversions
    status = "OK" if actual_cpa <= target_cpa else "OVER_BUDGET"
    return {
        "status": status,
        "spend": f"{spend:,.0f} đ",
        "conversions": conversions,
        "cpa": f"{actual_cpa:,.0f} đ",
        "target": f"{target_cpa:,.0f} đ"
    }

result = check_cpa(spend=1250000, conversions=18, target_cpa=75000)
print("=== KẾT QUẢ KIỂM TRA QUẢNG CÁO ===")
for k, v in result.items():
    print(f"{k.upper()}: {v}")
"""
    },
    {
        "id": "vault-distill",
        "title": "Second Brain Auto-Distillation Rule",
        "language": "python",
        "description": "Trích xuất quy tắc thực chiến từ một cuộc hội thoại và chuẩn bị note vào wiki.",
        "code": """# Knowledge Distillation Pipeline
raw_note = \"\"\"
Hôm nay thử nghiệm landing page dạng Scroll-storytelling.
Tỷ lệ ở lại trang tăng từ 35s lên 1m45s.
Tỷ lệ điền form chuyển đổi tăng từ 2.4% lên 5.8%.
Kết luận: Trải nghiệm mượt mà trực quan nâng cao niềm tin của khách hàng cao cấp.
\"\"\"

def distil_insight(text: str):
    return {
        "rule_title": "Tác động của Scroll-storytelling lên CR",
        "category": "MARKETING/CRO",
        "compound_score": 0.88,
        "key_takeaway": "Nâng thời gian đọc trang gấp 3x, tăng CR thêm +3.4%."
    }

print("Đã chưng cất thành công quy tắc:")
print(distil_insight(raw_note))
"""
    },
    {
        "id": "zalo-webhook-parser",
        "title": "Zalo OA Webhook Event Receiver",
        "language": "python",
        "description": "Phân tích payload tin nhắn đến từ người dùng Zalo và gắn nhãn ý định.",
        "code": """# Zalo Webhook Parser
event = {
    "event_name": "user_send_text",
    "sender": {"id": "zalo_8829104"},
    "message": {"text": "Tôi muốn tư vấn hệ thống quản trị Second Brain cho doanh nghiệp"}
}

def route_intent(msg: str):
    msg_lower = msg.lower()
    if "tư vấn" in msg_lower or "giá" in msg_lower:
        return "HIGH_INTENT_LEAD"
    return "GENERAL_INQUIRY"

intent = route_intent(event["message"]["text"])
print(f"Người gửi: {event['sender']['id']}")
print(f"Nội dung: {event['message']['text']}")
print(f"Phân loại Intent: {intent} -> Điều hướng tới trợ lý May May!")
"""
    }
]

class RunCodePayload(BaseModel):
    code: str
    language: Optional[str] = "python"

@router.get("/snippets")
def get_snippets():
    return {"snippets": CODE_SNIPPETS}

@router.post("/run")
def execute_code(payload: RunCodePayload):
    if payload.language != "python":
        return {"output": "Ngôn ngữ không được hỗ trợ để thực thi trực tiếp trên máy chủ.", "execution_time_ms": 0}

    # Bắt stdout và stderr
    stdout_buf = io.StringIO()
    start_time = time.time()
    
    # Safe namespace execution
    safe_globals = {
        "__builtins__": {
            "print": print,
            "len": len,
            "range": range,
            "int": int,
            "float": float,
            "str": str,
            "bool": bool,
            "dict": dict,
            "list": list,
            "set": set,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "round": round,
            "isinstance": isinstance,
            "enumerate": enumerate,
            "zip": zip,
        }
    }
    
    try:
        with contextlib.redirect_stdout(stdout_buf), contextlib.redirect_stderr(stdout_buf):
            exec(payload.code, safe_globals)
        output = stdout_buf.getvalue()
        if not output:
            output = "Mã nguồn đã thực thi thành công (Không có output in ra console)."
    except Exception as e:
        output = f"Lỗi thực thi (Runtime Error):\n{traceback.format_exc()}"
    
    duration = round((time.time() - start_time) * 1000, 2)
    return {
        "output": output,
        "execution_time_ms": duration,
        "status": "success"
    }
