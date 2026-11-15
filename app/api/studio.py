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
        "category": "system",
        "title": "Executive Operations & Workflow Lead",
        "role": "Điều phối toàn bộ luồng tự động & standup hàng ngày",
        "avatar": "👩‍💼",
        "avatar_color": "#ea580c",
        "icon_symbol": "⬢",
        "status": "system",
        "auto_mode": False,
        "model": "Claude 3.5 Sonnet",
        "tasks_count": 10,
        "budget": "Không giới hạn",
        "bio": "Quản lý luồng công việc tự động, theo dõi timeline điều hành và phân luồng task tới từng trợ lý chuyên môn.",
        "assistant_documents": ["00 - System/Rules.md", "01 - Projects/Operations.md"],
        "system_prompt": "You lead executive operations and orchestrate multi-agent workflows. Ensure strict timeline adherence and escalate blockers to the CEO.",
        "skills": ["Workflow Orchestration", "Daily Standup", "Status Tracking"],
        "sample_chat": [
            {"role": "user", "text": "Báo cáo tiến độ vận hành sáng nay thế nào?"},
            {"role": "agent", "text": "Chào Sếp! Toàn bộ 9 cộng sự đang trực chiến. Đã có 3 task hoàn thành tự động từ Javis Vu (CSKH) và 1 bản tin thị trường từ Duy (Market Research). Không có điểm nghẽn nào."}
        ]
    },
    {
        "id": "javis-vu",
        "name": "Javis Vu | Customer Care",
        "category": "auto",
        "title": "Customer Care & Support Agent",
        "role": "Chăm sóc khách hàng tự động 24/7 qua Zalo & Fanpage",
        "avatar": "👨‍💼",
        "avatar_color": "#f97316",
        "icon_symbol": "●",
        "status": "auto",
        "auto_mode": True,
        "model": "GPT-4o mini",
        "tasks_count": 9,
        "budget": "$0.40 / ngày (~35k tokens)",
        "bio": "Chuyên xử lý chăm sóc khách hàng tự động qua Zalo và Fanpage, trả lời tin nhắn và tóm tắt biên bản đào tạo.",
        "assistant_documents": ["07 - Wiki/Chính sách CSKH.md", "07 - Wiki/Kịch bản phản hồi.md"],
        "system_prompt": "Bạn là Javis Vu, chuyên viên chăm sóc khách hàng 24/7. Bạn trả lời thân thiện, lịch sự, đúng chính sách và chuyển tiếp các ca khó cho nhân sự người thật.",
        "skills": ["Zalo Auto-reply", "Meeting Notes to Wiki", "Ticket Routing"],
        "sample_chat": [
            {"role": "user", "text": "Hôm nay có bao nhiêu khách cần hỗ trợ kỹ thuật?"},
            {"role": "agent", "text": "Dạ thưa Sếp, từ 00:00 đến nay có 18 lượt chat qua Zalo. Em đã tự động giải đáp 16 trường hợp theo Wiki CSKH, còn 2 ca hỏi về hợp đồng tùy biến em đã gắn tag [Cần Sếp Duyệt]."}
        ]
    },
    {
        "id": "ha-lam",
        "name": "Ha Lam | Assistant",
        "category": "auto",
        "title": "Executive AI Assistant",
        "role": "Trợ lý lịch trình, phân loại email và nhắc việc điều hành",
        "avatar": "👩‍💻",
        "avatar_color": "#10b981",
        "icon_symbol": "●",
        "status": "auto",
        "auto_mode": True,
        "model": "Gemini 1.5 Flash",
        "tasks_count": 6,
        "budget": "$0.30 / ngày (~30k tokens)",
        "bio": "Giám sát lịch trình, tóm tắt các cuộc họp quan trọng, nhắc việc điều hành và lọc email ưu tiên.",
        "assistant_documents": ["02 - Areas/Schedule.md", "00 - System/Briefs.md"],
        "system_prompt": "Bạn là Hà Lam, trợ lý điều hành. Bạn quản lý thời gian, lọc thư rác, tóm tắt nội dung họp và nhắc việc quan trọng.",
        "skills": ["Calendar Sync", "Email Summarizer", "Task Dispatcher"],
        "sample_chat": [
            {"role": "user", "text": "Lịch làm việc buổi chiều nay có gì đột xuất không?"},
            {"role": "agent", "text": "Dạ thưa Sếp, chiều nay 14:30 có lịch review phễu với Khang và Bao. Em đã chuẩn bị sẵn tài liệu phễu Webcake tại thư mục 01 - Projects để Sếp tiện mở."}
        ]
    },
    {
        "id": "an-marketing",
        "name": "An - Marketing Lead",
        "category": "others",
        "title": "Chief Marketing Strategist",
        "role": "Owns the marketing strategy, leads the 5 AI teammates",
        "avatar": "▲",
        "avatar_color": "#8b5cf6",
        "icon_symbol": "▲",
        "status": "online",
        "auto_mode": False,
        "model": "GPT-4o mini",
        "tasks_count": 8,
        "budget": "$0.80 / ngày (~60k tokens)",
        "bio": "Chỉ huy chiến lược Marketing tổng thể, điều phối 5 chuyên viên AI chuyên môn, kiểm soát toàn bộ kế hoạch từ phác thảo đến bàn giao.",
        "assistant_documents": ["01 - Projects/Marketing Strategy 2026.md", "07 - Wiki/Brand Standards.md"],
        "system_prompt": "You lead the AI marketing team and report to the owner. You own the plan from strategy to sign-off, pick the right coworker for each step and learn from reviews.",
        "skills": ["30 kĩ năng xuất sắc", "Campaign Orchestrator", "Content Quality Gate", "Funnel Review"],
        "sample_chat": [
            {"role": "user", "text": "30 bước review chiến dịch marketing Q4"},
            {"role": "agent", "text": "Đã nhận lệnh từ Sếp. Tôi đang kích hoạt quy trình 30 bước review chiến dịch Q4: 1. Thu thập dữ liệu ROI/ROAS từ Duy và Bao. 2. Đối chiếu mục tiêu doanh thu. 3. Rà soát chất lượng qua Tough Reviser. 4. Đề xuất 3 đòn bẩy tối ưu hóa."}
        ]
    },
    {
        "id": "bao-conversion",
        "name": "Bao - Conversion & Analytics",
        "category": "others",
        "title": "CRO & Performance Specialist",
        "role": "Builds landing page funnels, tracks ROAS & CPA anomalies",
        "avatar": "■",
        "avatar_color": "#3b82f6",
        "icon_symbol": "■",
        "status": "online",
        "auto_mode": False,
        "model": "Claude 3.5 Sonnet",
        "tasks_count": 5,
        "budget": "$0.60 / ngày (~40k tokens)",
        "bio": "Giám sát hiệu quả chiến dịch Facebook/Google Ads, phát hiện điểm đốt tiền bất thường và tối ưu tỷ lệ chuyển đổi landing page.",
        "assistant_documents": ["01 - Projects/Funnel Metrics.md", "07 - Wiki/Landing Page Checklist.md"],
        "system_prompt": "You build high-converting landing pages, audit sales funnels, and detect CPA anomalies on Meta & Google Ads.",
        "skills": ["Meta Ads Graph API", "CPA Anomaly Alert", "A/B Testing", "Webcake Exporter"],
        "sample_chat": [
            {"role": "user", "text": "Kiểm tra tỷ lệ chuyển đổi của landing page mới"},
            {"role": "agent", "text": "Tỷ lệ chuyển đổi trang Webcake hiện tại đạt 3.82% (tăng 0.6% so với tuần trước). Điểm nghẽn lớn nhất nằm ở form đăng ký tầng 2 trên mobile, tôi khuyến nghị rút gọn từ 4 trường xuống còn 2 trường (Tên + Số Zalo)."}
        ]
    },
    {
        "id": "duy-market",
        "name": "Duy - Market Research",
        "category": "others",
        "title": "Market & Prospect Intelligence",
        "role": "Researches prospects, competitors and market sentiment",
        "avatar": "●",
        "avatar_color": "#10b981",
        "icon_symbol": "●",
        "status": "online",
        "auto_mode": False,
        "model": "GPT-4o mini",
        "tasks_count": 4,
        "budget": "$0.50 / ngày (~40k tokens)",
        "bio": "Phân tích đối thủ cạnh tranh, đào sâu nỗi đau khách hàng tiềm năng và cập nhật xu hướng thị trường vào Second Brain.",
        "assistant_documents": ["03 - Resources/Competitor Intelligence.md"],
        "system_prompt": "You conduct deep market intelligence, track competitor pricing and campaigns, and summarize prospect ICP pains.",
        "skills": ["Market Mining", "Sentiment Analysis", "Competitor Matrix"],
        "sample_chat": [
            {"role": "user", "text": "Đối thủ A vừa ra mắt gói dịch vụ mới, có gì đáng chú ý?"},
            {"role": "agent", "text": "Tôi đã phân tích gói mới của Đối thủ A: Họ định giá 4.900.000đ nhưng thiếu tính năng tích hợp Second Brain và tự động hóa Zalo. Đây là khoảng trống hoàn hảo để ta đánh bật họ bằng thông điệp [Thuê cộng sự tự hành thay vì chỉ nhận tài liệu]."}
        ]
    },
    {
        "id": "tough-reviser",
        "name": "Tough Reviser",
        "category": "others",
        "title": "Brutal Content & Strategy Critic",
        "role": "Critiques blog posts, sales scripts & strategic memos",
        "avatar": "◆",
        "avatar_color": "#f59e0b",
        "icon_symbol": "◆",
        "status": "online",
        "auto_mode": False,
        "model": "Claude 3.5 Sonnet",
        "tasks_count": 3,
        "budget": "$0.50 / ngày (~35k tokens)",
        "bio": "Phản biện sắc bén, gọt giũa bài viết, loại bỏ sáo rỗng và các luận điểm yếu trước khi gửi cho khách hàng hoặc xuất bản.",
        "assistant_documents": ["07 - Wiki/Anti-hype Writing Rules.md"],
        "system_prompt": "You critique copy with brutal honesty. Point out logical holes, fluff, over-promising buzzwords, and force clarity.",
        "skills": ["Brutal Revision", "Logical Fallacy Check", "Readability Score"],
        "sample_chat": [
            {"role": "user", "text": "Soát lại bài post thông báo tính năng mới"},
            {"role": "agent", "text": "Bài viết này còn quá nhiều thuật ngữ kỹ thuật rườm rà. Đoạn mở đầu mất 3 câu vô nghĩa trước khi vào trọng tâm. Hãy bỏ ngay cụm từ \"giải pháp đột phá mang tính cách mạng\", thay bằng: \"Bạn không cần thêm khung chat, bạn cần một cộng sự tự làm việc\"."}
        ]
    },
    {
        "id": "ha-email",
        "name": "Ha - Email & Nurture",
        "category": "others",
        "title": "Lifecycle & Retention Architect",
        "role": "Designs email sequences, retention drips & newsletter broadcasts",
        "avatar": "✦",
        "avatar_color": "#ec4899",
        "icon_symbol": "✦",
        "status": "online",
        "auto_mode": False,
        "model": "GPT-4o mini",
        "tasks_count": 4,
        "budget": "$0.40 / ngày (~30k tokens)",
        "bio": "Thiết kế chuỗi email nuôi dưỡng khách hàng, kịch bản chăm sóc sau mua và newsletter hàng tuần chuẩn phong cách Thịnh Vượng Số.",
        "assistant_documents": ["01 - Projects/Email Drips.md"],
        "system_prompt": "You craft high-converting email sequences, nurture drips, and broadcast newsletters with compelling storytelling.",
        "skills": ["Email Sequence Engine", "Subject Line Scorer", "Unsubscribe Shield"],
        "sample_chat": [
            {"role": "user", "text": "Tạo kịch bản email chào mừng 3 ngày đầu cho học viên mới"},
            {"role": "agent", "text": "Dạ, tôi đã soạn xong chuỗi 3 email chào mừng: 1. Quyền truy cập Second Brain, 2. Kích hoạt cộng sự AI đầu tiên, 3. Thử thách thực chiến & hỗ trợ VIP."}
        ]
    },
    {
        "id": "khang-funnel",
        "name": "Khang - Funnel Strategy",
        "category": "others",
        "title": "Value Ladder & Offer Architect",
        "role": "Maps the path from visitor to high-ticket buyer",
        "avatar": "⬡",
        "avatar_color": "#06b6d4",
        "icon_symbol": "⬡",
        "status": "online",
        "auto_mode": False,
        "model": "Claude 3.5 Sonnet",
        "tasks_count": 5,
        "budget": "$0.60 / ngày (~45k tokens)",
        "bio": "Thiết kế cấu trúc thang giá trị (Value Ladder), bố cục phễu thu hút khách hàng tiềm năng và chuyển đổi sang gói cao cấp.",
        "assistant_documents": ["01 - Projects/Value Ladder.md", "07 - Wiki/Offer Framework.md"],
        "system_prompt": "You design frictionless customer journeys, tripwires, core offers, and high-ticket backends.",
        "skills": ["Value Ladder Design", "Offer Crafting", "Conversion Architecture"],
        "sample_chat": [
            {"role": "user", "text": "Đề xuất cấu trúc phễu bán hàng cho khóa đào tạo AI Operating System"},
            {"role": "agent", "text": "Tôi đề xuất phễu 3 nấc: 1. Nấc Mồi: Template Second Brain Obsidian, 2. Nấc Chuyển đổi: Bộ 10 Agent Prompt 199k, 3. Nấc Lõi: Coaching Thực chiến Cockpit JAVIS OS."}
        ]
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

# CHATBOT OMNICHANNEL & SLEEP-STATS APIS
OMNICHANNEL_CONVERSATIONS = [
    {
        "id": "conv-1",
        "customer_name": "Trần Hải Đăng",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=80&h=80&fit=crop",
        "channel": "Zalo OA",
        "channel_icon": "message-circle",
        "channel_color": "blue",
        "time": "02:14 sáng (Khi bạn ngủ)",
        "last_message": "Cho mình hỏi gói Setup Second Brain trọn gói cho doanh nghiệp bao gồm những gì?",
        "ai_reply": "Dạ em chào anh Đăng! Gói Setup Second Brain trọn gói bên em gồm 7 trụ cột: Vault Obsidian chuẩn PARA, Javis OS Cockpit điều hành, tích hợp Telegram/Zalo bot 24/7 và chuyển giao 1-1 ạ.",
        "status": "ai_replied",
        "status_label": "AI đã trả lời chuẩn xác"
    },
    {
        "id": "conv-2",
        "customer_name": "Mai Phương Linh",
        "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=80&h=80&fit=crop",
        "channel": "Messenger",
        "channel_icon": "send",
        "channel_color": "indigo",
        "time": "04:35 sáng (Khi bạn ngủ)",
        "last_message": "Mình muốn xin demo giao diện Javis OS và bảng báo giá chi tiết.",
        "ai_reply": "Dạ chị Linh, em xin gửi chị link video walkthrough 5 phút của Javis OS và bảng đối chiếu ROI. Anh Duy cũng sẽ liên hệ chị lúc 8:30 sáng nay ạ!",
        "status": "ai_replied",
        "status_label": "AI đã trả lời chuẩn xác"
    },
    {
        "id": "conv-3",
        "customer_name": "Lê Văn Tuấn (Giám đốc Công nghệ)",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&h=80&fit=crop",
        "channel": "Telegram",
        "channel_icon": "send",
        "channel_color": "sky",
        "time": "06:10 sáng",
        "last_message": "Công ty mình cần tích hợp bảo mật On-Premise và xuất hóa đơn VAT công ty thì chiết khấu thế nào?",
        "ai_reply": "[Bot chủ động im lặng - Câu hỏi nhạy cảm về đàm phán hợp đồng & chiết khấu riêng]",
        "status": "silence_hold",
        "status_label": "Bot giữ im lặng - Đang chờ bạn tiếp quản"
    },
    {
        "id": "conv-4",
        "customer_name": "Nguyễn Bích Ngọc",
        "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=80&h=80&fit=crop",
        "channel": "WhatsApp",
        "channel_icon": "phone-call",
        "channel_color": "emerald",
        "time": "06:55 sáng",
        "last_message": "I am interested in integrating our existing Slack workspace with your AI Brain.",
        "ai_reply": "Hello Ms. Ngoc! Javis OS supports seamless Slack integration via incoming Webhooks and Event Subscriptions. Let me share the quick setup doc.",
        "status": "ai_replied",
        "status_label": "AI đã trả lời chuẩn xác"
    },
    {
        "id": "conv-5",
        "customer_name": "Hoàng Nam",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=80&h=80&fit=crop",
        "channel": "Instagram",
        "channel_icon": "camera",
        "channel_color": "pink",
        "time": "Hôm qua 23:45",
        "last_message": "Chào bạn, mình thấy video trên Threads rất hay, muốn hỏi học phí kèm 1-1.",
        "ai_reply": "Cảm ơn bạn Hoàng Nam đã quan tâm! Em xin gửi thông tin chi tiết về chương trình Mentorship 30 ngày nhé ạ.",
        "status": "ai_replied",
        "status_label": "AI đã trả lời chuẩn xác"
    }
]

OMNICHANNEL_CHANNELS = [
    {"id": "whatsapp", "name": "WhatsApp", "connected": True, "messages": 184, "bot_active": True, "badge_color": "emerald"},
    {"id": "messenger", "name": "Messenger", "connected": True, "messages": 892, "bot_active": True, "badge_color": "blue"},
    {"id": "instagram", "name": "Instagram", "connected": True, "messages": 412, "bot_active": True, "badge_color": "pink"},
    {"id": "telegram", "name": "Telegram", "connected": True, "messages": 526, "bot_active": True, "badge_color": "sky"},
    {"id": "slack", "name": "Slack", "connected": True, "messages": 95, "bot_active": True, "badge_color": "purple"},
    {"id": "lark", "name": "Lark Suite", "connected": True, "messages": 64, "bot_active": True, "badge_color": "cyan"},
    {"id": "threads", "name": "Threads", "connected": True, "messages": 78, "bot_active": True, "badge_color": "zinc"},
    {"id": "zalo_personal", "name": "Zalo Cá Nhân", "connected": True, "messages": 1420, "bot_active": True, "badge_color": "blue"},
    {"id": "zalo_oa", "name": "Zalo OA", "connected": True, "messages": 678, "bot_active": True, "badge_color": "sky"}
]

@router.get("/chatbot-stats")
def get_chatbot_stats():
    return {
        "status": "success",
        "hero": {
            "total_ai_answers": "2.569",
            "growth_rate": "+42% so với chu kỳ trước",
            "ai_answered_percentage": 79,
            "hours_freed": 42.8,
            "answers_while_slept": 567,
            "sleep_window": "11:00 PM - 07:00 AM",
            "customers_served": 343,
            "customers_new": 20,
            "speed_ai": "32 s",
            "speed_hand": "4 m",
            "hand_replies": 683,
            "waiting_count": 0
        },
        "hourly_distribution": [
            {"hour": "00:00", "count": 48, "is_night": True},
            {"hour": "01:00", "count": 35, "is_night": True},
            {"hour": "02:00", "count": 28, "is_night": True},
            {"hour": "03:00", "count": 22, "is_night": True},
            {"hour": "04:00", "count": 34, "is_night": True},
            {"hour": "05:00", "count": 52, "is_night": True},
            {"hour": "06:00", "count": 78, "is_night": True},
            {"hour": "07:00", "count": 115, "is_night": False},
            {"hour": "08:00", "count": 142, "is_night": False},
            {"hour": "09:00", "count": 180, "is_night": False},
            {"hour": "10:00", "count": 195, "is_night": False},
            {"hour": "11:00", "count": 170, "is_night": False},
            {"hour": "12:00", "count": 140, "is_night": False},
            {"hour": "13:00", "count": 165, "is_night": False},
            {"hour": "14:00", "count": 210, "is_night": False},
            {"hour": "15:00", "count": 285, "is_night": False, "is_peak": True},
            {"hour": "16:00", "count": 310, "is_night": False, "is_peak": True},
            {"hour": "17:00", "count": 290, "is_night": False, "is_peak": True},
            {"hour": "18:00", "count": 240, "is_night": False, "is_peak": True},
            {"hour": "19:00", "count": 190, "is_night": False},
            {"hour": "20:00", "count": 175, "is_night": False},
            {"hour": "21:00", "count": 160, "is_night": False},
            {"hour": "22:00", "count": 125, "is_night": False},
            {"hour": "23:00", "count": 82, "is_night": True}
        ],
        "account_comparison": {
            "account_name": "Javis Vũ",
            "ai_percent": 79,
            "hand_percent": 21,
            "ai_messages": 2569,
            "hand_messages": 683
        }
    }

@router.get("/chatbot-conversations")
def get_chatbot_conversations():
    return {"status": "success", "conversations": OMNICHANNEL_CONVERSATIONS}

class TakeoverPayload(BaseModel):
    conversation_id: str
    action: str

@router.post("/chatbot-takeover")
def chatbot_takeover(payload: TakeoverPayload):
    for c in OMNICHANNEL_CONVERSATIONS:
        if c["id"] == payload.conversation_id:
            if payload.action == "takeover":
                c["status"] = "human_takeover"
                c["status_label"] = "Bạn đã tiếp quản bằng tay"
            elif payload.action == "toggle_silence":
                c["status"] = "silence_hold"
                c["status_label"] = "Bot giữ im lặng"
            elif payload.action == "ai_resume":
                c["status"] = "ai_replied"
                c["status_label"] = "AI đã tiếp tục trả lời"
            return {"status": "success", "conversation": c}
    return {"status": "error", "message": "Conversation not found"}

@router.get("/chatbot-channels")
def get_chatbot_channels():
    return {"status": "success", "channels": OMNICHANNEL_CHANNELS}


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



class SavePartnerPayload(BaseModel):
    id: str
    name: Optional[str] = None
    role: Optional[str] = None
    title: Optional[str] = None
    model: Optional[str] = None
    system_prompt: Optional[str] = None
    auto_mode: Optional[bool] = None
    budget: Optional[str] = None
    skills: Optional[List[str]] = None
    assistant_documents: Optional[List[str]] = None

@router.post("/partners/save")
def save_partner(payload: SavePartnerPayload):
    for p in PARTNERS_LIST:
        if p["id"] == payload.id:
            if payload.name is not None: p["name"] = payload.name
            if payload.role is not None: p["role"] = payload.role
            if payload.title is not None: p["title"] = payload.title
            if payload.model is not None: p["model"] = payload.model
            if payload.system_prompt is not None: p["system_prompt"] = payload.system_prompt
            if payload.auto_mode is not None: p["auto_mode"] = payload.auto_mode
            if payload.budget is not None: p["budget"] = payload.budget
            if payload.skills is not None: p["skills"] = payload.skills
            if payload.assistant_documents is not None: p["assistant_documents"] = payload.assistant_documents
            return {"status": "success", "partner": p}
    return {"status": "error", "message": "Partner not found"}

class PartnerChatPayload(BaseModel):
    partner_id: str
    message: str
    model: Optional[str] = None
    skill: Optional[str] = None

@router.post("/partners/chat")
def partner_chat(payload: PartnerChatPayload):
    partner = next((p for p in PARTNERS_LIST if p["id"] == payload.partner_id), None)
    if not partner:
        return {"status": "error", "message": "Partner not found"}
    
    used_model = payload.model or partner.get("model", "GPT-4o mini")
    skills_avail = partner.get("skills", ["General"])
    used_skill = payload.skill or (skills_avail[0] if skills_avail else "General")
    
    p_name = partner.get("name", "Cộng sự")
    p_role = partner.get("role", "")
    
    if "sample_chat" not in partner:
        partner["sample_chat"] = []
    
    partner["sample_chat"].append({"role": "user", "text": payload.message})
    
    docs_list = ", ".join(partner.get("assistant_documents", ["Toàn bộ Wiki"]))
    reply = f"[{p_name}] Model: {used_model} | Kỹ năng: {used_skill} \n\nĐã tiếp nhận: {payload.message} \n\nĐã kết nối tài liệu: {docs_list}. Vai trò: {p_role}."
    partner["sample_chat"].append({"role": "agent", "text": reply})
    return {
        "status": "success",
        "reply": reply,
        "model": used_model,
        "skill": used_skill,
        "sample_chat": partner["sample_chat"]
    }

class UploadAgentPayload(BaseModel):
    markdown_content: str

@router.post("/partners/upload")
def upload_agent(payload: UploadAgentPayload):
    lines = payload.markdown_content.splitlines()
    name = "New Agent"
    role = "Specialist Agent"
    system_prompt = payload.markdown_content
    for line in lines:
        if line.startswith("# "):
            name = line.replace("# ", "").strip()
            break
        elif "name:" in line.lower():
            name = line.split(":", 1)[1].strip().strip("'\"")
            break
    
    new_agent = {
        "id": "agent-" + str(uuid.uuid4())[:6],
        "name": name,
        "category": "others",
        "title": name,
        "role": role,
        "avatar": "🤖",
        "avatar_color": "#6366f1",
        "icon_symbol": "★",
        "status": "online",
        "auto_mode": False,
        "model": "GPT-4o mini",
        "tasks_count": 0,
        "budget": "$0.50 / ngày",
        "bio": "Cộng sự AI được nhập từ file Markdown Second Brain.",
        "assistant_documents": ["07 - Wiki/Guidelines.md"],
        "system_prompt": system_prompt,
        "skills": ["Custom Skills"],
        "sample_chat": []
    }
    PARTNERS_LIST.append(new_agent)
    return {"status": "success", "agent": new_agent}
