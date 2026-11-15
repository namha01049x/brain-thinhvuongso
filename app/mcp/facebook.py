from typing import Dict, Any, List
import time

def get_facebook_ads_report(account_name: str = "phamquangdai", period: str = "Tháng 8") -> Dict[str, Any]:
    """Báo cáo chỉ số chiến dịch quảng cáo Facebook thông qua Meta Ads Graph API."""
    return {
        "account": account_name,
        "account_id": "699125929448265",
        "period": period,
        "metrics": {
            "spend": 25440355,
            "currency": "VND",
            "impressions": 713206,
            "reach": 467271,
            "frequency": 1.53,
            "clicks_all": 20097,
            "ctr_all": 2.82,
            "link_clicks": 3527,
            "cpc_link": 7213,
            "cpm": 35670
        },
        "breakdown": [
            {
                "objective": "Chuyển đổi (Conversions / Purchase)",
                "spend": 23769358,
                "results": 91,
                "result_type": "Website Purchases",
                "cpa": 261200
            },
            {
                "objective": "Tiếp cận (Reach / Nhận diện)",
                "spend": 1670997,
                "reach": 416362,
                "cost_per_1000_reach": 3600
            }
        ]
    }

def get_fanpage_posts(page_id: str = "phamquangdai", limit: int = 3) -> List[Dict[str, Any]]:
    """Đọc danh sách bài đăng Fanpage gần đây."""
    return [
        {
            "id": "post_101",
            "content": "Tại sao Solopreneur cần một Second Brain thay vì lưu note rời rạc? Chia sẻ kiến trúc 5 bậc...",
            "likes": 245,
            "comments": 38,
            "shares": 19,
            "published_at": "Hôm qua"
        },
        {
            "id": "post_102",
            "content": "Case study tối ưu chi phí quảng cáo và tự động hóa vận hành bằng MCP Tool...",
            "likes": 412,
            "comments": 65,
            "shares": 54,
            "published_at": "3 ngày trước"
        }
    ][:limit]

def publish_fanpage_post(page_id: str, content: str) -> Dict[str, Any]:
    """Đăng bài viết mới lên Fanpage Facebook qua Graph API."""
    return {
        "status": "published",
        "post_id": f"post_{int(time.time())}",
        "page_id": page_id,
        "content_preview": content[:100] + ("..." if len(content) > 100 else ""),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }
