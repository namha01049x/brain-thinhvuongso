import time
import uuid
from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])

WEBHOOKS_LIST = [
    {
        "id": "wh-zalo-leads",
        "name": "Zalo OA Lead Inbound",
        "url": "/api/webhooks/incoming/zalo",
        "status": "active",
        "events": ["user_send_text", "user_submit_form"],
        "assistant": "Javis Vu | Customer Care",
        "last_trigger": "10 phút trước",
        "trigger_count": 142
    },
    {
        "id": "wh-webcake-form",
        "name": "Webcake Landing Form Submissions",
        "url": "/api/webhooks/incoming/webcake",
        "status": "active",
        "events": ["form_submission"],
        "assistant": "Bao - Conversion Specialist",
        "last_trigger": "32 phút trước",
        "trigger_count": 89
    },
    {
        "id": "wh-meta-cpa-alert",
        "name": "Meta Ads Anomaly Trigger",
        "url": "/api/webhooks/incoming/meta-cpa",
        "status": "active",
        "events": ["cpa_threshold_exceeded"],
        "assistant": "Bao - Conversion Specialist",
        "last_trigger": "2 giờ trước",
        "trigger_count": 12
    }
]

RECENT_LOGS = [
    {
        "id": "log-1",
        "webhook": "Zalo OA Lead Inbound",
        "timestamp": "Vừa xong",
        "status": "200 OK",
        "payload_snippet": '{"sender": "0912***345", "intent": "Tư vấn gói Second Brain"}'
    },
    {
        "id": "log-2",
        "webhook": "Webcake Landing Form Submissions",
        "timestamp": "32 phút trước",
        "status": "200 OK",
        "payload_snippet": '{"name": "Trần Văn Nam", "phone": "098***123", "package": "VIP"}'
    },
    {
        "id": "log-3",
        "webhook": "Meta Ads Anomaly Trigger",
        "timestamp": "2 giờ trước",
        "status": "200 OK",
        "payload_snippet": '{"campaign": "Scale Tháng 11", "cpa": "112,000 đ", "action": "alert"}'
    }
]

@router.get("/list")
def list_webhooks():
    return {
        "webhooks": WEBHOOKS_LIST,
        "recent_logs": RECENT_LOGS
    }

class TestWebhookPayload(BaseModel):
    webhook_id: str
    custom_payload: Optional[str] = None

@router.post("/test")
def test_webhook(payload: TestWebhookPayload):
    new_log = {
        "id": f"log-{uuid.uuid4().hex[:6]}",
        "webhook": payload.webhook_id,
        "timestamp": "Vừa xong (Test)",
        "status": "200 OK",
        "payload_snippet": payload.custom_payload or '{"event": "test_ping", "status": "success", "timestamp": ' + str(int(time.time())) + '}'
    }
    RECENT_LOGS.insert(0, new_log)
    return {"status": "success", "message": "Đã gửi test webhook thành công!", "log": new_log}

@router.post("/incoming/{source}")
async def handle_incoming(source: str, request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {"raw": "Non-JSON or empty payload"}
    
    log_entry = {
        "id": f"log-{uuid.uuid4().hex[:6]}",
        "webhook": f"Incoming/{source}",
        "timestamp": "Vừa xong",
        "status": "200 OK",
        "payload_snippet": str(body)[:120]
    }
    RECENT_LOGS.insert(0, log_entry)
    return {"received": True, "source": source}
