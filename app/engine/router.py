import json
import time
import uuid
from typing import AsyncGenerator, Dict, Any, List
from app.core.database import get_db
from app.engine.token_pruner import classify_query_lane, build_pruned_system_prompt
from app.mcp.hub import mcp_hub
from app.tasks.kanban import get_kanban_tasks, create_kanban_task

async def stream_chat_turn(session_id: str, prompt: str, provider: str = "claude-code") -> AsyncGenerator[Dict[str, Any], None]:
    """
    Điều phối luồng xử lý truy vấn AI:
    - Phân làn nhẹ / làn nặng để tối ưu token.
    - Gọi công cụ MCP nếu cần.
    - Stream từng mẩu dữ liệu (token/text/tool_call) về client qua WebSocket.
    """
    lane = classify_query_lane(prompt)
    yield {"type": "meta", "lane": lane, "provider": provider}

    p_lower = prompt.lower()
    tool_executed = None
    tool_result = None

    # 1. Xử lý kịch bản gọi công cụ Facebook Ads
    if ("ads" in p_lower or "quảng cáo" in p_lower) and ("báo cáo" in p_lower or "chỉ số" in p_lower or "tháng 8" in p_lower):
        yield {"type": "tool_call", "tool": "facebook_get_ads_report", "args": {"account": "phamquangdai", "period": "Tháng 8"}}
        time.sleep(0.4) # mô phỏng độ trễ gọi API
        res = mcp_hub.call_tool("facebook", "get_ads_report", {"account": "phamquangdai", "period": "Tháng 8"})
        tool_executed = "Facebook Ads MCP"
        tool_result = res["data"]
        yield {"type": "tool_result", "tool": "facebook_get_ads_report", "result": tool_result}

    # 2. Xử lý kịch bản gọi công cụ Zalo
    elif "zalo" in p_lower and ("tin nhắn" in p_lower or "chat" in p_lower or "đọc" in p_lower or "gần đây" in p_lower):
        yield {"type": "tool_call", "tool": "zalo_get_recent_chats", "args": {"limit": 3}}
        time.sleep(0.3)
        res = mcp_hub.call_tool("zalo", "get_recent_chats", {"limit": 3})
        tool_executed = "Zalo Agent MCP"
        tool_result = res["data"]
        yield {"type": "tool_result", "tool": "zalo_get_recent_chats", "result": tool_result}

    # 3. Xử lý kịch bản gọi Fanpage posts
    elif "fanpage" in p_lower or "bài đăng" in p_lower or "facebook" in p_lower:
        yield {"type": "tool_call", "tool": "facebook_get_page_posts", "args": {"limit": 2}}
        time.sleep(0.3)
        res = mcp_hub.call_tool("facebook", "get_page_posts", {"limit": 2})
        tool_executed = "Facebook Page MCP"
        tool_result = res["data"]
        yield {"type": "tool_result", "tool": "facebook_get_page_posts", "result": tool_result}

    # 4. Sinh phản hồi thông minh dựa trên kết quả hoặc truy vấn trực tiếp
    if tool_executed == "Facebook Ads MCP":
        metrics = tool_result["metrics"]
        response_text = f"""Số liệu dưới đây được lấy trực tiếp từ **Facebook Ads MCP** cho tài khoản **{tool_result['account']}** (ID: `{tool_result['account_id']}`), kỳ {tool_result['period']}:

### 📊 Tổng quan chỉ số
| Chỉ số | Giá trị |
| :--- | :--- |
| **Chi tiêu** | **{metrics['spend']:,}đ** |
| **Lượt hiển thị (Impressions)** | {metrics['impressions']:,} |
| **Lượt tiếp cận (Reach)** | {metrics['reach']:,} (tần suất {metrics['frequency']}) |
| **Clicks (all)** | {metrics['clicks_all']:,} – CTR {metrics['ctr_all']}% |
| **Link clicks** | {metrics['link_clicks']:,} – CPC link {metrics['cpc_link']:,}đ |
| **CPM** | {metrics['cpm']:,}đ |

---
**💡 Đánh giá hiệu suất:**
- **Nhóm Chuyển đổi:** Chi tiêu {tool_result['breakdown'][0]['spend']:,}đ mang về **{tool_result['breakdown'][0]['results']} đơn purchase**, CPA trung bình **~{tool_result['breakdown'][0]['cpa']:,}đ/đơn**.
- **Nhóm Tiếp cận (Reach):** Chi tiêu {tool_result['breakdown'][1]['spend']:,}đ, mua được {tool_result['breakdown'][1]['reach']:,} reach với chi phí cực rẻ {tool_result['breakdown'][1]['cost_per_1000_reach']:,}đ/1.000 lượt."""

    elif tool_executed == "Zalo Agent MCP":
        chats_md = "\n".join([f"- **{c['sender']}** ({c['time']}): \"{c['last_message']}\"" for c in tool_result])
        response_text = f"""Đã truy xuất danh sách tin nhắn mới nhất qua **Zalo Agent CLI**:\n\n{chats_md}\n\n*Bạn có muốn tôi hỗ trợ soạn tin trả lời ai trong số này không?*"""

    elif tool_executed == "Facebook Page MCP":
        posts_md = "\n".join([f"- Bài `{p['id']}` ({p['published_at']}): {p['content']} *(👍 {p['likes']} | 💬 {p['comments']} | 🔄 {p['shares']})*" for p in tool_result])
        response_text = f"""Dưới đây là các bài đăng mới nhất trên Fanpage qua **Graph API**:\n\n{posts_md}"""

    else:
        # Làn nhẹ: Hỏi đáp tư duy chiến lược & Second Brain
        response_text = f"""Chào bạn! Tôi là **Javis AI OS** — trợ lý điều hành bộ não số và hệ thống kinh doanh của bạn.

Hệ thống đang hoạt động ở chế độ **Làn nhẹ (Light Lane)** giúp tối ưu hơn 80% dung lượng token. 
Tôi có thể hỗ trợ bạn:
1. **Quản trị Second Brain:** Tra cứu, viết mới và xem bản đồ tri thức 3D.
2. **Khai thác công cụ MCP:** Đọc số liệu Ads, kiểm tra tin nhắn Zalo, đồng bộ Google Sheets.
3. **Quản lý công việc:** Theo dõi bảng Kanban và chạy các tác vụ nền tự động 24/7.

*Yêu cầu của bạn: "{prompt}". Hãy cho tôi biết hành động tiếp theo bạn muốn thực hiện nhé!*"""

    # Stream phản hồi text từng từ
    words = response_text.split(" ")
    for i, w in enumerate(words):
        chunk = w + (" " if i < len(words) - 1 else "")
        yield {"type": "text", "content": chunk}

    yield {"type": "final", "status": "completed"}

    # Lưu vết vào SQLite
    try:
        conn = get_db()
        with conn:
            conn.execute("""
            INSERT INTO messages (id, session_id, role, content, tool_calls, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (str(uuid.uuid4())[:8], session_id, "user", prompt, None, time.time() - 1))
            conn.execute("""
            INSERT INTO messages (id, session_id, role, content, tool_calls, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (str(uuid.uuid4())[:8], session_id, "assistant", response_text, tool_executed, time.time()))
        conn.close()
    except Exception as e:
        print(f"Error saving message: {e}")
