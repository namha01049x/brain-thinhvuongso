from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter(prefix="/api/models", tags=["Models"])

# Dữ liệu các nhà cung cấp model tương tự Javis OS
PROVIDERS = [
    {
        "id": "anthropic-cli",
        "name": "Anthropic OAuth (Claude Code)",
        "badge": "MCP/SKILL",
        "is_main": True,
        "status": "connected",
        "email": "dai9zpp@gmail.com",
        "plan": "max",
        "mode": "subscription", # 'subscription' (không tốn tiền) hoặc 'api_key'
        "models": ["claude-3-7-sonnet", "claude-3-5-sonnet", "claude-3-opus", "claude-3-5-haiku"],
        "description": "Chạy qua Claude Code nên giữ nguyên lệnh máy, WebFetch, MCP native và nối phiên cũ."
    },
    {
        "id": "openai-oauth",
        "name": "OpenAI OAuth (ChatGPT / Codex)",
        "badge": "DEVICE CODE",
        "is_main": False,
        "status": "connected",
        "plan": "plus",
        "mode": "subscription",
        "models": ["gpt-4o", "gpt-4o-mini", "o1-preview", "o1-mini", "chatgpt-4o-latest"],
        "description": "Kết nối phiên ChatGPT Plus/Pro của bạn, hỗ trợ tạo ảnh, vision và chạy code."
    },
    {
        "id": "antigravity-cli",
        "name": "Google Antigravity CLI",
        "badge": "MCP/SKILL",
        "is_main": False,
        "status": "connected",
        "plan": "google (keyring máy)",
        "mode": "subscription",
        "models": ["gemini-2.0-flash", "gemini-1.5-pro", "gemini-1.5-flash", "claude-3.5-sonnet-via-agy"],
        "description": "Dùng gói Google của bạn không cần mua API key. Chọn đúng dàn model của Antigravity IDE."
    },
    {
        "id": "ollama-local",
        "name": "Ollama Local (Offline AI)",
        "badge": "LOCAL RUNTIME",
        "is_main": False,
        "status": "connected",
        "plan": "local",
        "mode": "offline",
        "models": ["deepseek-r1:8b", "llama3.3:70b", "qwen2.5:14b"],
        "description": "Chạy hoàn toàn trên máy tính cá nhân của bạn, không gửi bất kỳ byte dữ liệu nào ra ngoài."
    }
]

@router.get("/providers")
def get_providers():
    return {"providers": PROVIDERS}

class SwitchModePayload(BaseModel):
    provider_id: str
    mode: str

@router.post("/mode")
def set_provider_mode(payload: SwitchModePayload):
    for p in PROVIDERS:
        if p["id"] == payload.provider_id:
            p["mode"] = payload.mode
            return {"status": "success", "provider": p}
    return {"status": "error", "message": "Provider not found"}
