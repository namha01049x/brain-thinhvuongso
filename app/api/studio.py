from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import time
import uuid

router = APIRouter(prefix="/api/studio", tags=["Studio & Skills & Capabilities"])

# Danh sách kỹ năng chính xác theo Javis OS thực tế (Ảnh 1)
SKILLS_LIST = [
    {
        "id": "html-to-webcake",
        "name": "HTML to Webcake",
        "tag": "system",
        "category": "Marketing",
        "enabled": True,
        "description": "Turn an HTML page into a .pke file the Webcake builder can open, keeping the original colours, type sizes, images and layout.",
        "badges": ["Marketing", "html-to-webcake"]
    },
    {
        "id": "ingest-source",
        "name": "Ingest Source",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Digest one raw source into the Second Brain and distil it into wiki knowledge that compounds.",
        "badges": ["AI", "ingest-source"]
    },
    {
        "id": "javis-builder",
        "name": "Javis Builder",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Create or edit a Javis capability: agent, skill, workflow, loop, plugin. Ships file templates and the rules against duplicates.",
        "badges": ["AI", "javis-builder"]
    },
    {
        "id": "lint-wiki",
        "name": "Lint Wiki",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Audit the health of the Second Brain wiki and hand back a list of problems. Never mass-edits on its own.",
        "badges": ["AI", "lint-wiki"]
    },
    {
        "id": "notes",
        "name": "Notes",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Save the current message verbatim into sources/ (images included), then distil it up to the wiki if it earns a place.",
        "badges": ["AI", "notes"]
    },
    {
        "id": "query-wiki",
        "name": "Query Wiki",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Mine the knowledge held in the Second Brain: synthesis, comparison, hypotheses. Every answer carries citations.",
        "badges": ["AI", "query-wiki"]
    },
    {
        "id": "facebook-ads-mcp",
        "name": "Facebook Ads & CPA Optimizer",
        "tag": "system",
        "category": "Marketing",
        "enabled": True,
        "description": "Query Meta Ads Graph API, calculate real-time CPA, link clicks, ROAS and detect burning adsets.",
        "badges": ["Marketing", "meta-ads"]
    },
    {
        "id": "zalo-agent-cli",
        "name": "Zalo Agent CLI Bridge",
        "tag": "system",
        "category": "Social",
        "enabled": True,
        "description": "Read and dispatch Zalo direct messages via safe authenticated local command line bridge.",
        "badges": ["Social", "zalo-cli"]
    }
]

# Danh sách AI Partners / Trợ lý chuyên gia
PARTNERS_LIST = [
    {
        "id": "may-may",
        "name": "May May",
        "title": "Executive Operations & Workflow Lead",
        "avatar": "👩‍💼",
        "status": "online",
        "tasks_count": 10,
        "bio": "Quản lý luồng công việc tự động, theo dõi timeline điều hành và phân luồng task tới từng trợ lý chuyên môn.",
        "capabilities": ["Workflow Orchestration", "Daily Standup", "Status Tracking"]
    },
    {
        "id": "javis-vu",
        "name": "Javis Vu",
        "title": "Customer Care & Support Agent",
        "avatar": "👨‍💼",
        "status": "online",
        "tasks_count": 9,
        "bio": "Chuyên xử lý chăm sóc khách hàng tự động qua Zalo và Fanpage, trả lời tin nhắn và tóm tắt biên bản đào tạo.",
        "capabilities": ["Zalo Auto-reply", "Meeting Notes to Wiki", "Ticket Routing"]
    },
    {
        "id": "bao-conversion",
        "name": "Bao - Conversion Specialist",
        "title": "Funnel Optimization & Performance Ads",
        "avatar": "📈",
        "status": "online",
        "tasks_count": 5,
        "bio": "Giám sát hiệu quả chiến dịch Facebook Ads, tính toán CPA theo thời gian thực và đề xuất tối ưu tỷ lệ chuyển đổi.",
        "capabilities": ["Meta Ads Graph API", "CPA Anomaly Alert", "A/B Test Advisory"]
    },
    {
        "id": "mai-brand",
        "name": "Mai - Brand Content Specialist",
        "title": "Brand Voice & Content Generation",
        "avatar": "🎨",
        "status": "idle",
        "tasks_count": 4,
        "bio": "Viết bài chuẩn nhận diện thương hiệu Thịnh Vượng Số, kịch bản video ngắn và nội dung truyền thông đa kênh.",
        "capabilities": ["Brand Compliance", "Social Copywriting", "Script Generation"]
    },
    {
        "id": "tough-reader",
        "name": "Tough Reader",
        "title": "Deep Research & Knowledge Ingestion",
        "avatar": "📚",
        "status": "online",
        "tasks_count": 3,
        "bio": "Đọc sâu tài liệu dài, sách, nghiên cứu thị trường và trích xuất tinh hoa chưng cất vào Second Brain Wiki.",
        "capabilities": ["Long-form Synthesis", "Wiki Distillation", "Citation Verification"]
    },
    {
        "id": "khang-funnel",
        "name": "Khang - Funnel Architect",
        "title": "Funnel Strategy & Webcake Landing Page",
        "avatar": "🏗️",
        "status": "idle",
        "tasks_count": 2,
        "bio": "Thiết kế cấu trúc phễu bán hàng bậc thang giá trị (Value Ladder) và xuất bản landing page Webcake siêu tốc.",
        "capabilities": ["HTML to Webcake", "Value Ladder Design", "Offer Crafting"]
    }
]

# Danh sách Plugins hệ sinh thái Javis
PLUGINS_LIST = [
    {
        "id": "plugin-webcake",
        "name": "Webcake Page Exporter",
        "version": "1.2.0",
        "author": "Javis Foundation",
        "installed": True,
        "enabled": True,
        "description": "Tự động xuất trang web HTML sang định dạng .pke tương thích trực tiếp với trình dựng Webcake."
    },
    {
        "id": "plugin-zalo",
        "name": "Zalo Messaging Hub",
        "version": "2.0.4",
        "author": "Javis Community",
        "installed": True,
        "enabled": True,
        "description": "Kết nối nhắn tin Zalo OA và cá nhân qua token OAuth bảo mật cục bộ."
    },
    {
        "id": "plugin-meta-ads",
        "name": "Meta Ads & CPA Monitor",
        "version": "1.0.8",
        "author": "Javis Foundation",
        "installed": True,
        "enabled": True,
        "description": "Trích xuất chỉ số quảng cáo Meta Graph API, tự động cảnh báo nhóm quảng cáo đốt tiền."
    },
    {
        "id": "plugin-git-sync",
        "name": "Vault Git Auto-Sync",
        "version": "3.1.0",
        "author": "Core Engine",
        "installed": True,
        "enabled": True,
        "description": "Tự động commit và push mọi thay đổi trong Second Brain vào kho Git cục bộ/từ xa."
    },
    {
        "id": "plugin-ocr-vision",
        "name": "OCR Document & Receipt Scanner",
        "version": "0.9.5",
        "author": "Javis Labs",
        "installed": False,
        "enabled": False,
        "description": "Trích xuất văn bản từ hóa đơn, ảnh chụp màn hình và tài liệu scan trực tiếp vào thư mục Sources."
    }
]

# Chatbot configuration
CHATBOT_CONFIG = {
    "bot_name": "Javis Assistant",
    "welcome_message": "Xin chào! Tôi là trợ lý ảo Javis OS từ Brain Thịnh Vượng Số. Tôi có thể giúp gì cho bạn hôm nay?",
    "system_prompt": "Bạn là trợ lý AI thông minh đại diện cho doanh nghiệp. Hãy trả lời ngắn gọn, lịch sự và giải đáp chính xác thắc mắc của khách hàng dựa trên dữ liệu Second Brain.",
    "temperature": 0.7,
    "model": "claude-3-5-sonnet",
    "theme_color": "#ea580c",
    "allowed_domains": ["localhost", "127.0.0.1", "thinhvuongso.com"]
}

@router.get("/skills")
def list_skills():
    ai_count = sum(1 for s in SKILLS_LIST if s["category"] == "AI")
    mkt_count = sum(1 for s in SKILLS_LIST if s["category"] == "Marketing")
    return {
        "skills": SKILLS_LIST,
        "counts": {
            "all": len(SKILLS_LIST),
            "ai": ai_count,
            "marketing": mkt_count,
            "social": 1
        }
    }

class ToggleSkillPayload(BaseModel):
    skill_id: str
    enabled: bool

@router.post("/toggle-skill")
def toggle_skill(payload: ToggleSkillPayload):
    for s in SKILLS_LIST:
        if s["id"] == payload.skill_id:
            s["enabled"] = payload.enabled
            return {"status": "success", "skill": s}
    return {"status": "error", "message": "Skill not found"}

class AddSkillPayload(BaseModel):
    name: str
    category: str
    description: str

@router.post("/skills")
def add_custom_skill(payload: AddSkillPayload):
    new_skill = {
        "id": str(uuid.uuid4())[:8],
        "name": payload.name,
        "tag": "custom",
        "category": payload.category,
        "enabled": True,
        "description": payload.description,
        "badges": [payload.category, "custom-user"]
    }
    SKILLS_LIST.append(new_skill)
    return {"status": "success", "skill": new_skill}

@router.get("/partners")
def list_partners():
    return {"partners": PARTNERS_LIST}

@router.get("/plugins")
def list_plugins():
    return {"plugins": PLUGINS_LIST}

class TogglePluginPayload(BaseModel):
    plugin_id: str
    enabled: bool

@router.post("/toggle-plugin")
def toggle_plugin(payload: TogglePluginPayload):
    for p in PLUGINS_LIST:
        if p["id"] == payload.plugin_id:
            p["enabled"] = payload.enabled
            return {"status": "success", "plugin": p}
    return {"status": "error", "message": "Plugin not found"}

@router.get("/chatbot-config")
def get_chatbot_config():
    return {"config": CHATBOT_CONFIG}

class UpdateChatbotConfigPayload(BaseModel):
    bot_name: Optional[str] = None
    welcome_message: Optional[str] = None
    system_prompt: Optional[str] = None
    temperature: Optional[float] = None
    model: Optional[str] = None
    theme_color: Optional[str] = None

@router.post("/chatbot-config")
def update_chatbot_config(payload: UpdateChatbotConfigPayload):
    if payload.bot_name is not None: CHATBOT_CONFIG["bot_name"] = payload.bot_name
    if payload.welcome_message is not None: CHATBOT_CONFIG["welcome_message"] = payload.welcome_message
    if payload.system_prompt is not None: CHATBOT_CONFIG["system_prompt"] = payload.system_prompt
    if payload.temperature is not None: CHATBOT_CONFIG["temperature"] = payload.temperature
    if payload.model is not None: CHATBOT_CONFIG["model"] = payload.model
    if payload.theme_color is not None: CHATBOT_CONFIG["theme_color"] = payload.theme_color
    return {"status": "success", "config": CHATBOT_CONFIG}

# Autonomous Goals ("Làm cả khi bạn ngủ")
AUTONOMOUS_GOALS = [
    {
        "id": "goal-1",
        "title": "Nghiên cứu thị trường Solopreneur & Viết dàn ý Landing Page High-Ticket",
        "status": "completed",
        "lead_agent": "Tough Reader & Mai Content",
        "created_at": "Hôm qua lúc 23:30",
        "completed_at": "Hôm nay lúc 04:15 (Tự động hoàn thành khi bạn ngủ)",
        "deliverable": "vault_data/Wiki/Dan Y Landing Page Solopreneur 2026.md",
        "steps": [
            {"step": 1, "name": "Giao mục tiêu", "status": "done"},
            {"step": 2, "name": "AI tự viết dàn bài & kế hoạch", "status": "done"},
            {"step": 3, "name": "Chọn người làm (Tough Reader + Mai)", "status": "done"},
            {"step": 4, "name": "Tự động xuất bản & báo cáo Telegram", "status": "done"}
        ]
    }
]

class DispatchGoalPayload(BaseModel):
    goal_title: str
    target_agent: Optional[str] = "Auto-assign"

@router.post("/dispatch-goal")
def dispatch_autonomous_goal(payload: DispatchGoalPayload):
    new_goal = {
        "id": f"goal-{uuid.uuid4().hex[:6]}",
        "title": payload.goal_title,
        "status": "running",
        "lead_agent": payload.target_agent if payload.target_agent != "Auto-assign" else "May May & Javis Core",
        "created_at": "Vừa kích hoạt",
        "completed_at": "Dự kiến 06:00 sáng mai",
        "deliverable": "vault_data/Wiki/Ket-Qua-Chay-Ngam.md",
        "steps": [
            {"step": 1, "name": "Đã tiếp nhận mục tiêu", "status": "done"},
            {"step": 2, "name": "AI đang phân tích dàn ý nhiệm vụ...", "status": "running"},
            {"step": 3, "name": "Ủy quyền cộng sự chuyên môn", "status": "pending"},
            {"step": 4, "name": "Báo cáo khi hoàn thành", "status": "pending"}
        ]
    }
    AUTONOMOUS_GOALS.insert(0, new_goal)
    return {"status": "success", "goal": new_goal}

@router.get("/goals")
def list_goals():
    return {"goals": AUTONOMOUS_GOALS}

# System Permissions ("Bạn đặt giới hạn")
SYSTEM_PERMISSION_STATE = {
    "current_level": "draft",  # 'readonly', 'draft', 'full'
    "levels": [
        {
            "id": "readonly",
            "name": "Đọc và gợi ý",
            "tag": "chỉ xem dữ liệu",
            "desc": "AI chỉ có quyền đọc tài liệu và đưa ra phân tích, không được ghi đè hay gửi tin nhắn.",
            "active": False
        },
        {
            "id": "draft",
            "name": "Viết bản nháp",
            "tag": "cần duyệt trước",
            "desc": "AI được tạo bản nháp note, email, bài đăng nhưng phải qua bước bạn bấm phê duyệt.",
            "active": True
        },
        {
            "id": "full",
            "name": "Toàn quyền",
            "tag": "công cụ thật",
            "desc": "AI được phép tự động gọi API, gửi tin nhắn Zalo/Telegram và cập nhật Git không cần hỏi lại.",
            "active": False
        }
    ]
}

@router.get("/system-permission")
def get_permission():
    return SYSTEM_PERMISSION_STATE

class SetPermissionPayload(BaseModel):
    level: str  # 'readonly', 'draft', 'full'

@router.post("/system-permission")
def set_permission(payload: SetPermissionPayload):
    if payload.level in ["readonly", "draft", "full"]:
        SYSTEM_PERMISSION_STATE["current_level"] = payload.level
        for lvl in SYSTEM_PERMISSION_STATE["levels"]:
            lvl["active"] = (lvl["id"] == payload.level)
        return {"status": "success", "level": payload.level}
    raise HTTPException(status_code=400, detail="Mức quyền không hợp lệ")

# Git Workflow & Pull Requests ("Từ ý tưởng đến pull request")
@router.get("/git-workflow")
def get_git_workflow():
    return {
        "current_branch": "main",
        "active_pr": {
            "branch": "javis/fix-header",
            "title": "Tối ưu thanh điều hướng Cockpit & thêm chế độ ban đêm",
            "status": "merged",
            "checks": [
                {"name": "Lint Markdown & Syntax", "status": "passed"},
                {"name": "Audit Token Pruner", "status": "passed"},
                {"name": "Build Static Site", "status": "passed"}
            ],
            "merged_to": "main",
            "live_domain": "javisos.com"
        }
    }

# Recurring Loops ("Vòng lặp và nhắc hẹn")
RECURRING_LOOPS = [
    {
        "id": "loop-1",
        "name": "Báo cáo đầu ngày CEO",
        "schedule": "Mỗi ngày - 07:00",
        "cron": "0 7 * * *",
        "assistant": "May May",
        "action": "Tổng hợp chỉ số Ads, số dư quỹ và danh sách việc cần giải quyết",
        "status": "active"
    },
    {
        "id": "loop-2",
        "name": "Kiểm tra CPA Anomaly & Đốt tiền",
        "schedule": "Mỗi 30 phút",
        "cron": "*/30 * * * *",
        "assistant": "Bao - Conversion Specialist",
        "action": "Quét Meta Graph API, tự động cảnh báo nếu CPA vượt quá 85k",
        "status": "active"
    },
    {
        "id": "loop-3",
        "name": "Chưng cất tri thức sang Wiki",
        "schedule": "23:00 Hàng ngày",
        "cron": "0 23 * * *",
        "assistant": "Tough Reader",
        "action": "Đọc toàn bộ tin nhắn ngày và tạo commit vào Wiki",
        "status": "active"
    }
]

@router.get("/recurring-loops")
def get_recurring_loops():
    return {"loops": RECURRING_LOOPS}

