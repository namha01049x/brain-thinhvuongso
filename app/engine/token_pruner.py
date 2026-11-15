import re
from typing import Dict, Any, List, Tuple
from app.core.config import settings
from app.vault.reader import get_note_content

# Từ khóa kích hoạt làn nặng (cần gọi tool thực thi)
HEAVY_KEYWORDS = [
    "ads", "quảng cáo", "facebook", "chi tiêu", "cpa", "ctr", "mua",
    "zalo", "nhắn tin", "gửi tin", "bạn bè", "cuộc trò chuyện",
    "sheet", "bảng tính", "excel", "dữ liệu",
    "kanban", "tác vụ", "việc cần làm", "todo", "giao việc",
    "sửa file", "tạo note", "ghi chú", "terminal", "lệnh máy", "code"
]

def classify_query_lane(query: str) -> str:
    """
    Phân loại lượt chat vào làn nhẹ (light) hay làn nặng (heavy).
    - Làn nhẹ: Hỏi đáp, trò chuyện, tóm tắt thông thường -> KHÔNG nạp Schema Tool -> Tiết kiệm 80% token.
    - Làn nặng: Thao tác thực tế (Ads, Zalo, File, Terminal, Kanban) -> Chỉ nạp đúng Tool cần thiết.
    """
    q_lower = query.lower()
    for kw in HEAVY_KEYWORDS:
        if kw in q_lower:
            return "heavy"
    return "light"

def build_pruned_system_prompt(lane: str, relevant_tools: List[str] = None) -> str:
    """Xây dựng System Prompt tối ưu hóa theo đúng ngân sách token."""
    # Đọc trí nhớ cốt lõi
    core_memory = get_note_content("memory/MEMORY.md") or "Người dùng: Doanh nhân số, Solopreneur."
    
    if lane == "light":
        return f"""Bạn là Javis - Trợ lý Trí tuệ Nhân tạo cá nhân của hệ điều hành Brain Thịnh Vượng Số.
Hồ sơ cốt lõi:
{core_memory}

Quy tắc:
- Trả lời ngắn gọn, súc tích, trực diện vào vấn đề.
- Sử dụng tiếng Việt chuẩn mực, hỗ trợ người dùng tối đa.
(Làn nhẹ: Không nạp công cụ không cần thiết để tiết kiệm token tối đa)."""

    # Làn nặng: Nạp hướng dẫn tool
    tools_desc = "\n".join([f"- {t}" for t in (relevant_tools or ["mcp_tools"])])
    return f"""Bạn là Javis - Trợ lý Trí tuệ Nhân tạo điều hành của hệ điều hành Brain Thịnh Vượng Số.
Hồ sơ cốt lõi:
{core_memory}

Bạn có toàn quyền sử dụng các công cụ đã được phân quyền qua Javis MCP Hub:
{tools_desc}

Quy tắc thực thi:
- Phân tích yêu cầu và gọi đúng tool cần thiết.
- Luôn báo cáo số liệu và kết quả minh bạch, rõ ràng."""
