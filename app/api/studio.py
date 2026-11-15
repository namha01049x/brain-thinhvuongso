from fastapi import APIRouter
from typing import Dict, Any, List

router = APIRouter(prefix="/api/studio", tags=["Studio"])

AGENTS = [
    {
        "id": "agent-core",
        "name": "Javis Executive Assistant",
        "role": "Tổng quản điều phối",
        "avatar": "⚡",
        "status": "active",
        "description": "Điều hành tổng thể các tác vụ hàng ngày, quản lý lịch trình, nhắc hẹn và điều phối các agent con.",
        "skills_count": 14,
        "model": "Claude 3.7 Sonnet"
    },
    {
        "id": "agent-marketing",
        "name": "Ads & Growth Specialist",
        "role": "Chuyên gia Tăng trưởng & Ads",
        "avatar": "📈",
        "status": "active",
        "description": "Theo dõi chiến dịch Meta Ads, Google Ads, tính toán CPA/ROI và tự động đề xuất tối ưu ngân sách.",
        "skills_count": 18,
        "model": "Claude 3.5 Sonnet"
    },
    {
        "id": "agent-content",
        "name": "Viral Content & Copywriter",
        "role": "Sáng tạo nội dung số",
        "avatar": "✍️",
        "status": "active",
        "description": "Soạn thảo kịch bản Reels/TikTok, bài viết Fanpage theo Thang giá trị và viết email marketing.",
        "skills_count": 12,
        "model": "GPT-4o"
    },
    {
        "id": "agent-coder",
        "name": "Fullstack Software Coder",
        "role": "Lập trình viên & Kỹ thuật",
        "avatar": "💻",
        "status": "active",
        "description": "Viết mã nguồn, debug, tạo checkpoint Git bóng và chạy thử nghiệm trong sandbox.",
        "skills_count": 15,
        "model": "Claude 3.7 Sonnet"
    },
    {
        "id": "agent-cskh",
        "name": "Zalo Care & Outreach Agent",
        "role": "Chăm sóc khách hàng Zalo",
        "avatar": "💬",
        "status": "active",
        "description": "Đọc tin nhắn, lọc khách tiềm năng và tự động soạn thảo tin nhắn trả lời chuẩn tone cá nhân.",
        "skills_count": 8,
        "model": "Gemini 2.0 Flash"
    },
    {
        "id": "agent-research",
        "name": "Deep Market Researcher",
        "role": "Nghiên cứu thị trường & Đọc tài liệu",
        "avatar": "🔬",
        "status": "active",
        "description": "Nghiên cứu đối thủ, tóm tắt tài liệu PDF dày và đúc kết thành các ghi chú Second Brain.",
        "skills_count": 10,
        "model": "DeepSeek R1"
    },
    {
        "id": "agent-curator",
        "name": "Knowledge & Brain Curator",
        "role": "Kiến trúc sư bộ não số",
        "avatar": "🧠",
        "status": "active",
        "description": "Phân loại ghi chú, liên kết Wikilinks, cập nhật MEMORY.md và bảo vệ tính toàn vẹn của tri thức.",
        "skills_count": 9,
        "model": "Claude 3.5 Haiku"
    }
]

SKILL_CATEGORIES = [
    {
        "category": "Marketing & Ads (18 skills)",
        "items": [
            {"id": "s1", "name": "Facebook Ads Metrics Inspector", "desc": "Đọc toàn bộ chỉ số CPA, CTR, CPM từ Meta Graph API"},
            {"id": "s2", "name": "Value Ladder Funnel Designer", "desc": "Thiết kế phễu thang giá trị 5 bậc cho sản phẩm số"},
            {"id": "s3", "name": "Ad Copy Variations Generator", "desc": "Sinh 5 biến thể tiêu đề quảng cáo theo góc nhìn nỗi đau"},
            {"id": "s4", "name": "Audience Targeting Research", "desc": "Tìm kiếm tệp đối tượng ngách tiềm năng cao"}
        ]
    },
    {
        "category": "Second Brain & Knowledge (15 skills)",
        "items": [
            {"id": "s5", "name": "Wikilinks 3D Connection Extractor", "desc": "Tự động phát hiện liên kết hai chiều giữa các note"},
            {"id": "s6", "name": "Memory Crystallization Engine", "desc": "Chắt lọc sự thật từ hội thoại đưa vào MEMORY.md"},
            {"id": "s7", "name": "Book Note Synthesizer", "desc": "Tóm tắt sách theo cấu trúc 1 câu + 3 ý chính + Hành động"},
            {"id": "s8", "name": "Git Snapshot & Shadow Rollback", "desc": "Tạo điểm phục hồi code và dữ liệu tức thì"}
        ]
    },
    {
        "category": "Social & Customer Outreach (14 skills)",
        "items": [
            {"id": "s9", "name": "Zalo Agent CLI Bridge", "desc": "Đọc/gửi tin nhắn Zalo cá nhân qua giao thức MCP"},
            {"id": "s10", "name": "Fanpage Post Scheduler", "desc": "Lên lịch đăng bài và kiểm soát tương tác bài viết"},
            {"id": "s11", "name": "Lead Qualification Scorer", "desc": "Đánh giá mức độ tiềm năng của khách hàng từ chat"}
        ]
    },
    {
        "category": "Coding & System Sandbox (16 skills)",
        "items": [
            {"id": "s12", "name": "Fuzzy Section File Editor", "desc": "Sửa chính xác một khối code mà không làm xáo trộn toàn file"},
            {"id": "s13", "name": "Sandboxed Shell Runner", "desc": "Thực thi lệnh bash trong container an toàn"},
            {"id": "s14", "name": "API Route Auto Generator", "desc": "Sinh nhanh router FastAPI chuẩn REST và Pydantic"}
        ]
    },
    {
        "category": "Voice & Multimedia (12 skills)",
        "items": [
            {"id": "s15", "name": "Vietnamese Phonetics TTS Optimizer", "desc": "Phiên âm từ tiếng Anh công nghệ sang ngữ âm tiếng Việt"},
            {"id": "s16", "name": "Groq Whisper STT Listener", "desc": "Nhận diện giọng nói siêu tốc dưới 500ms"},
            {"id": "s17", "name": "YouTube Transcript Extractor", "desc": "Tải phụ đề và bóc tách dàn ý video YouTube"}
        ]
    }
]

WORKFLOWS = [
    {
        "id": "wf-daily-ops",
        "name": "Quy trình Tổng hợp Báo cáo & Lên kế hoạch Ngày",
        "steps": [
            "1. Agent Ads đọc số liệu chi tiêu Facebook Ads ngày hôm qua",
            "2. Agent CSKH kiểm tra danh sách tin nhắn Zalo chưa trả lời",
            "3. Agent Core tạo bảng việc Kanban cho ngày hôm nay và gửi báo cáo tóm tắt"
        ],
        "trigger": "Mỗi ngày lúc 08:00 AM",
        "status": "running"
    }
]

@router.get("/overview")
def get_studio_overview():
    return {
        "stats": {
            "total_agents": len(AGENTS),
            "total_skills": 75,
            "total_workflows": len(WORKFLOWS)
        },
        "agents": AGENTS,
        "skills": SKILL_CATEGORIES,
        "workflows": WORKFLOWS
    }
