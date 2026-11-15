import json
import time
from typing import Dict, Any, List, Optional
from app.core.database import get_db
from app.mcp import zalo, facebook

class MCPHub:
    """Cổng tập trung quản lý và phân quyền công cụ MCP."""

    @staticmethod
    def get_connection_perm(connector_id: str) -> str:
        """Lấy quyền hiện tại của kết nối từ cơ sở dữ liệu."""
        conn = get_db()
        cursor = conn.execute("SELECT perm FROM mcp_connections WHERE id = ?", (connector_id,))
        row = cursor.fetchone()
        conn.close()
        return row["perm"] if row else "readonly"

    @staticmethod
    def log_audit(connector: str, tool: str, args: dict, perm: str, status: str):
        """Ghi nhật ký kiểm toán vào SQLite."""
        try:
            conn = get_db()
            with conn:
                conn.execute("""
                INSERT INTO mcp_audit (connector, tool, args, perm, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (connector, tool, json.dumps(args), perm, status, time.time()))
            conn.close()
        except Exception as e:
            print(f"Error logging audit: {e}")

    @classmethod
    def call_tool(cls, connector: str, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Gọi thực thi tool có kiểm tra phân quyền 3 mức: readonly, safe, full."""
        perm = cls.get_connection_perm(connector)
        
        # 1. Phân quyền Zalo
        if connector == "zalo":
            if tool == "get_recent_chats":
                cls.log_audit(connector, tool, args, perm, "success")
                return {"success": True, "data": zalo.get_zalo_recent_chats(args.get("limit", 5))}
            elif tool == "send_message":
                if perm != "full":
                    cls.log_audit(connector, tool, args, perm, "denied")
                    return {"success": False, "error": f"Bị từ chối: Thao tác gửi tin nhắn cần quyền 'full' (Toàn quyền), quyền hiện tại là '{perm}'."}
                cls.log_audit(connector, tool, args, perm, "success")
                return {"success": True, "data": zalo.send_zalo_message(args.get("recipient", ""), args.get("message", ""))}

        # 2. Phân quyền Facebook
        elif connector == "facebook":
            if tool == "get_ads_report":
                cls.log_audit(connector, tool, args, perm, "success")
                return {"success": True, "data": facebook.get_facebook_ads_report(args.get("account", "phamquangdai"), args.get("period", "Tháng 8"))}
            elif tool == "get_page_posts":
                cls.log_audit(connector, tool, args, perm, "success")
                return {"success": True, "data": facebook.get_fanpage_posts(args.get("page_id", "phamquangdai"), args.get("limit", 3))}
            elif tool == "publish_post":
                if perm != "full":
                    cls.log_audit(connector, tool, args, perm, "denied")
                    return {"success": False, "error": f"Bị từ chối: Thao tác đăng bài lên Fanpage cần quyền 'full' (Toàn quyền), quyền hiện tại là '{perm}'."}
                cls.log_audit(connector, tool, args, perm, "success")
                return {"success": True, "data": facebook.publish_fanpage_post(args.get("page_id", "phamquangdai"), args.get("content", ""))}

        cls.log_audit(connector, tool, args, perm, "not_found")
        return {"success": False, "error": f"Tool '{tool}' không tồn tại trong connector '{connector}'."}

mcp_hub = MCPHub()
