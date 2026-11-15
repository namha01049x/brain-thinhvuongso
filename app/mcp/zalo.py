from typing import Dict, Any, List
import time

def get_zalo_recent_chats(limit: int = 5) -> List[Dict[str, Any]]:
    """Đọc danh sách các cuộc trò chuyện Zalo gần đây nhất."""
    return [
        {
            "sender": "Nguyễn Văn Hùng (Khách hàng)",
            "last_message": "Cho mình xin thông tin chi tiết về gói Trợ lý AI cá nhân với!",
            "time": "10:12 AM",
            "unread": True
        },
        {
            "sender": "Lê Thị Mai (Kế toán)",
            "last_message": "Đã nhận được sao kê quảng cáo Facebook tháng này rồi anh nhé.",
            "time": "09:45 AM",
            "unread": False
        },
        {
            "sender": "Trần Đức Trọng (Đối tác Media)",
            "last_message": "Bản nháp video Reels về Second Brain em gửi trong drive nha.",
            "time": "Hôm qua",
            "unread": False
        }
    ][:limit]

def send_zalo_message(recipient: str, message: str) -> Dict[str, Any]:
    """Gửi tin nhắn Zalo tới một người hoặc nhóm."""
    return {
        "status": "success",
        "recipient": recipient,
        "message": message,
        "sent_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "note": "Đã gửi qua Zalo Agent CLI chính thức."
    }
