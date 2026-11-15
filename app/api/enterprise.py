"""
Enterprise API Router for Javis OS - Bộ Não Doanh Nghiệp
Hỗ trợ quản lý 4 lớp kiến trúc doanh nghiệp:
Lớp 1: Tri thức (Second Brain theo phòng ban)
Lớp 2: Dữ liệu thật (15+ kết nối POS, Ads, CRM qua MCP)
Lớp 3: Đội trợ lý chuyên trách theo phòng ban
Lớp 4: Kênh làm việc đa nền tảng (Web, Telegram, Zalo)
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

router = APIRouter(prefix="/api/enterprise", tags=["Enterprise"])

# 1. 4 Lớp kiến trúc doanh nghiệp
@router.get("/architecture")
async def get_enterprise_architecture():
    return {
        "title": "Kiến Trúc Bộ Não AI Doanh Nghiệp (4 Lớp)",
        "subtitle": "Một bộ não chung, mọi trợ lý cùng dùng, dữ liệu ở lại trong doanh nghiệp",
        "layers": [
            {
                "id": "layer-1",
                "layer_num": 1,
                "name": "Lớp Tri Thức (Second Brain)",
                "icon": "🧠",
                "tagline": "Tài liệu, quy trình, chính sách, hồ sơ khách hàng số hoá thành wiki liên kết",
                "details": [
                    "Wiki liên kết chéo tự động (Cross-linking Markdown)",
                    "Ghi nhớ vai trò, quyết định, bối cảnh nội bộ",
                    "Truy xuất nguồn chính xác 100% trong vài giây",
                    "Sao lưu 2 chiều lên kho riêng tư (GitHub/Gitea/Local)"
                ],
                "stats": "1,424 notes · 3,188 liên kết tri thức"
            },
            {
                "id": "layer-2",
                "layer_num": 2,
                "name": "Lớp Dữ Liệu Thật (MCP Connectors)",
                "icon": "🔌",
                "tagline": "Kết nối POS, Quảng cáo, CRM, Sheets, Email... trợ lý đọc số liệu thật, không đoán",
                "details": [
                    "Kết nối Pancake POS, KiotViet, Meta Ads, TikTok Ads",
                    "Tích hợp Google Sheets, Gmail, Calendar, Drive",
                    "Phân quyền 3 tầng nghiêm ngặt: Chỉ đọc / Soạn nháp / Toàn quyền",
                    "Server MCP chuẩn hóa, bảo mật không rò rỉ dữ liệu"
                ],
                "stats": "15+ cổng kết nối · Phân quyền do hệ thống thực thi"
            },
            {
                "id": "layer-3",
                "layer_num": 3,
                "name": "Lớp Đội Trợ Lý (Department Assistants)",
                "icon": "👥",
                "tagline": "Skills, Agents, Workflows theo từng phòng ban: tự động hóa, soạn nháp, chạy theo lịch",
                "details": [
                    "Ban Lãnh Đạo: Trợ lý tổng hợp kinh doanh, báo cáo tức thì",
                    "Bán Hàng & CSKH: Bot Zalo 24/7 tra cứu giá và nhớ lịch sử khách",
                    "Marketing: Soạn 1 lần, duyệt nháp, xuất bản 6 kênh mạng xã hội",
                    "Vận Hành & Kế Toán: 1 lệnh chạy chuỗi (Ads -> Sheets -> POS -> Telegram)"
                ],
                "stats": "7 trợ lý chuyên trách · 75 skills tác vụ"
            },
            {
                "id": "layer-4",
                "layer_num": 4,
                "name": "Lớp Kênh Làm Việc (Multi-Channel Access)",
                "icon": "📱",
                "tagline": "Nhân sự và lãnh đạo sử dụng ngay trên công cụ họ đã quen thuộc hàng ngày",
                "details": [
                    "Giao diện Web Cockpit trực quan trên máy tính",
                    "Bot Telegram / Zalo thông báo tức thì trên điện thoại",
                    "Voice Interaction (Vbee / Giọng nói AI Việt ngữ)",
                    "Ứng dụng Desktop chạy nền 24/7"
                ],
                "stats": "Đa nền tảng · Hoạt động liên tục 24/7"
            }
        ]
    }

# 2. Đội trợ lý theo phòng ban
@router.get("/departments")
async def get_enterprise_departments():
    return {
        "departments": [
            {
                "id": "executive",
                "name": "Ban Lãnh Đạo & Điều Hành",
                "icon": "👑",
                "lead_role": "CEO / Ban Giám Đốc",
                "assistant_name": "Javis Executive Advisor",
                "channel": "Telegram Bot & Web Cockpit",
                "description": "Hỏi bất cứ lúc nào, nhận câu trả lời tổng hợp từ tài liệu và số liệu kinh doanh thật, trích dẫn nguồn, kèm file báo cáo.",
                "capabilities": [
                    "Báo cáo doanh thu & chi phí quảng cáo realtime",
                    "Đối chiếu chỉ tiêu kinh doanh với kế hoạch quý/năm",
                    "Tra cứu nhanh quy chế, điều lệ, chính sách công ty",
                    "Phê duyệt đề xuất và ngân sách một chạm qua Telegram"
                ],
                "active_bots": 2,
                "permissions": "Toàn quyền truy cập báo cáo tổng hợp"
            },
            {
                "id": "sales_cskh",
                "name": "Bán Hàng & Chăm Sóc Khách Hàng",
                "icon": "💬",
                "lead_role": "Trưởng phòng Kinh Doanh & CSKH",
                "assistant_name": "Zalo Sales AI Assistant",
                "channel": "Zalo Cá Nhân / Zalo OA & Web",
                "description": "Bot Zalo chăm khách 24/7 bằng dữ liệu công ty: trả lời ngoài giờ, nhớ lịch sử từng khách, chuyển người thật khi vượt thẩm quyền.",
                "capabilities": [
                    "Tra cứu bảng giá, chính sách chiết khấu, tồn kho tức thì",
                    "Ghi nhớ lịch sử trao đổi, sở thích và phân loại khách hàng",
                    "Tự động gửi thông báo lịch hẹn, tái chăm sóc đơn chưa thanh toán",
                    "Chuyển tiếp hội thoại sang nhân viên tư vấn khi gặp case phức tạp"
                ],
                "active_bots": 3,
                "permissions": "Chỉ đọc bảng giá + Soạn nháp tin nhắn"
            },
            {
                "id": "marketing",
                "name": "Marketing & Sáng Tạo Nội Dung",
                "icon": "🚀",
                "lead_role": "Marketing Manager",
                "assistant_name": "Omni-Channel Content Engine",
                "channel": "Web Studio & Auto-Poster",
                "description": "Viết một lần, đăng 6 kênh (Facebook, Instagram, Threads, YouTube, TikTok, Zalo) đúng giọng thương hiệu, kèm ảnh/video theo Brand Kit.",
                "capabilities": [
                    "Giữ nhất quán 100% Brand Voice & định vị thương hiệu",
                    "Soạn nháp nội dung đa định dạng chờ Manager duyệt",
                    "Tự động biến 1 bài blog dài thành chuỗi bài đăng ngắn & kịch bản Reels/Shorts",
                    "Theo dõi hiệu quả chiến dịch Ads và cảnh báo CPA cao"
                ],
                "active_bots": 2,
                "permissions": "Soạn nháp nội dung + Đọc chỉ số Ads"
            },
            {
                "id": "operations_finance",
                "name": "Vận Hành & Tài Chính - Kế Toán",
                "icon": "⚡",
                "lead_role": "CFO / Trưởng phòng Vận Hành",
                "assistant_name": "Operations Pipeline Automator",
                "channel": "Automated Workflows & Sheets Sync",
                "description": "Một lệnh chạy cả chuỗi việc: kéo số liệu Meta Ads -> cập nhật Google Sheets -> tạo hoá đơn trên POS -> báo Telegram.",
                "capabilities": [
                    "Báo cáo định kỳ tự động mỗi 08:00 sáng và 18:00 chiều",
                    "Đối soát số liệu giữa Meta/TikTok Ads, POS và tài khoản ngân hàng",
                    "Tự động phát hiện chênh lệch đơn hàng và cảnh báo tồn kho ảo",
                    "Lập đề xuất chi tiêu và kiểm tra định mức ngân sách"
                ],
                "active_bots": 2,
                "permissions": "Toàn quyền thực thi chuỗi tác vụ tin cậy"
            }
        ]
    }

# 3. Bảng so sánh "Chatbot cá nhân" vs "Bộ não doanh nghiệp Javis OS"
@router.get("/comparison")
async def get_enterprise_comparison():
    return {
        "title": "Bảng So Sánh Giải Pháp AI Cho Doanh Nghiệp",
        "rows": [
            {
                "criteria": "Tri thức & Bí quyết công ty",
                "personal_ai": "Nằm rải rác trong đầu nhân sự, mất sạch khi nhân viên nghỉ việc",
                "javis_os": "Tập trung vào Second Brain, thuộc sở hữu vĩnh viễn của công ty",
                "highlight": True
            },
            {
                "criteria": "Số liệu kinh doanh",
                "personal_ai": "Phải copy/paste thủ công, dễ sai lệch, AI dễ bị ảo giác đoán bừa",
                "javis_os": "Kết nối trực tiếp hệ thống thật (POS, Ads, CRM, Sheets) qua MCP chuẩn hóa",
                "highlight": True
            },
            {
                "criteria": "Kiểm soát & Phân quyền",
                "personal_ai": "Không ai quản lý, nhân viên tự do dán dữ liệu mật ra ngoài",
                "javis_os": "Hệ thống thực thi phân quyền 3 tầng: Chỉ đọc / Soạn nháp / Toàn quyền",
                "highlight": True
            },
            {
                "criteria": "Nhà cung cấp mô hình AI",
                "personal_ai": "Bị phụ thuộc vào một nhà cung cấp duy nhất (Vendor Lock-in)",
                "javis_os": "Linh hoạt đổi giữa Claude, GPT-4, Gemini hoặc mô hình nội bộ (Ollama)",
                "highlight": False
            },
            {
                "criteria": "Lưu trữ dữ liệu",
                "personal_ai": "Lưu trên máy chủ đám mây công cộng của bên thứ ba",
                "javis_os": "Tự host trên hạ tầng máy chủ riêng của doanh nghiệp, định dạng Markdown mở",
                "highlight": True
            },
            {
                "criteria": "Chi phí & Quản lý",
                "personal_ai": "Nhiều tài khoản rời rạc, chi phí lãng phí và khó kiểm soát",
                "javis_os": "Quản lý tập trung 1 cổng, tối ưu token bằng bộ pruner tiết kiệm 40% chi phí",
                "highlight": False
            }
        ]
    }

# 4. Giải pháp chuyên sâu theo 6 ngành nghề
@router.get("/industries")
async def get_enterprise_industries():
    return {
        "industries": [
            {
                "id": "retail_ecommerce",
                "name": "Bán Lẻ & Thương Mại Điện Tử",
                "icon": "🛍️",
                "pain_point": "Cùng một câu hỏi về giá, size, tồn kho, vận chuyển lặp lại hàng trăm lần mỗi ngày kể cả ngoài giờ.",
                "solution": "Bot Zalo & Fanpage tích hợp Pancake POS tra cứu kho tức thì, chăm sóc giỏ hàng chưa chốt và trả lời 24/7 chuẩn chính sách.",
                "workflows": ["Auto check tồn kho Pancake", "Bám đuổi đơn huỷ/hoãn", "Báo cáo doanh thu ca tối"]
            },
            {
                "id": "education_training",
                "name": "Giáo Dục & Đào Tạo",
                "icon": "🎓",
                "pain_point": "Học phí, lịch khai giảng, lộ trình học, cam kết đầu ra được hỏi dồn dập qua nhiều kênh tư vấn.",
                "solution": "Second Brain số hoá toàn bộ đề cương, lộ trình đào tạo, tài liệu giải đáp thắc mắc tuyển sinh tự động kèm nguồn chứng minh.",
                "workflows": ["Tư vấn lộ trình học viên theo nhu cầu", "Nhắc lịch học & bài tập qua Zalo", "Tổng hợp phản hồi học viên"]
            },
            {
                "id": "b2b_consulting",
                "name": "Dịch Vụ B2B & Tư Vấn",
                "icon": "💼",
                "pain_point": "Kinh nghiệm thực chiến dự án, giải pháp, bài học triển khai mất đi khi chuyên gia/nhân sự chủ chốt nghỉ việc.",
                "solution": "Hệ thống Wiki tự động ghi nhớ hồ sơ dự án, cấu trúc giải pháp, tạo đề xuất (proposal) hợp đồng trong vài phút.",
                "workflows": ["Tạo bản đề xuất giải pháp (RFP/Pitch Deck)", "Tổng hợp hồ sơ năng lực công ty", "Checklist nghiệm thu dự án"]
            },
            {
                "id": "real_estate",
                "name": "Bất Động Sản & Dự Án",
                "icon": "🏢",
                "pain_point": "Bảng hàng, chính sách bán hàng thay đổi liên tục; môi giới nhớ sai hoặc gửi nhầm bảng giá cũ cho khách VIP.",
                "solution": "Kho tài liệu bất động sản tập trung cập nhật theo thời gian thực; trợ lý tự động đối chiếu căn trống và chính sách ưu đãi.",
                "workflows": ["Cập nhật bảng hàng theo thời gian thực", "Soạn kịch bản tư vấn theo từng dự án", "Gửi brochure dự án tự động"]
            },
            {
                "id": "spa_clinic",
                "name": "Spa, Thẩm Mỹ & Phòng Khám",
                "icon": "💆",
                "pain_point": "Khách quên lịch hẹn, hủy lịch đột xuất gây lãng phí khung giờ chuyên gia và giảm doanh thu.",
                "solution": "Bot tự động xác nhận lịch hẹn trước 24h và 2h qua Zalo, hướng dẫn chuẩn bị trước khi đến và chăm sóc hậu phẫu.",
                "workflows": ["Nhắc lịch hẹn khám/làm đẹp đa kênh", "Tự động gửi hướng dẫn chăm sóc sau liệu trình", "Khảo sát độ hài lòng (CSAT)"]
            },
            {
                "id": "fnb_chains",
                "name": "F&B & Chuỗi Cửa Hàng",
                "icon": "🍜",
                "pain_point": "Nhân viên mới luân chuyển liên tục, hỏi lặp lại SOP, mỗi chi nhánh làm một kiểu không đồng nhất chất lượng.",
                "solution": "Quy trình chế biến, công thức định lượng, checklist mở/đóng ca được số hóa vào Second Brain, nhân sự tra cứu qua điện thoại.",
                "workflows": ["Tra cứu định lượng & công thức món chuẩn", "Checklist kiểm tra vệ sinh an toàn thực phẩm", "Báo cáo doanh số từng chi nhánh"]
            }
        ]
    }

# 5. Cổng kết nối dữ liệu thật (15+ Connectors)
@router.get("/connectors")
async def get_enterprise_connectors():
    return {
        "connectors": [
            {"id": "pancake", "name": "Pancake POS", "category": "Bán hàng & Kho", "status": "connected", "permission": "full_access", "permission_label": "Toàn quyền", "desc": "Đồng bộ đơn hàng, kho tồn, khách hàng"},
            {"id": "kiotviet", "name": "KiotViet POS", "category": "Bán hàng & Kho", "status": "connected", "permission": "read_only", "permission_label": "Chỉ đọc", "desc": "Tra cứu số dư kho và giá bán lẻ"},
            {"id": "meta_ads", "name": "Meta Ads (Facebook Ads)", "category": "Quảng cáo", "status": "connected", "permission": "read_only", "permission_label": "Chỉ đọc", "desc": "Kéo chỉ số chi tiêu, reach, CPA, ROAS"},
            {"id": "tiktok_ads", "name": "TikTok Ads", "category": "Quảng cáo", "status": "ready", "permission": "read_only", "permission_label": "Chỉ đọc", "desc": "Theo dõi chi phí và chuyển đổi video ads"},
            {"id": "google_ads", "name": "Google Ads", "category": "Quảng cáo", "status": "ready", "permission": "read_only", "permission_label": "Chỉ đọc", "desc": "Giám sát hiệu quả tìm kiếm và ngân sách"},
            {"id": "google_sheets", "name": "Google Sheets Doanh Nghiệp", "category": "Dữ liệu & Báo cáo", "status": "connected", "permission": "full_access", "permission_label": "Toàn quyền", "desc": "Cập nhật bảng thu chi, KPI tự động"},
            {"id": "zalo_agent", "name": "Zalo Agent (Cá nhân & OA)", "category": "Giao tiếp & CSKH", "status": "connected", "permission": "draft", "permission_label": "Soạn nháp", "desc": "Chăm sóc khách hàng 24/7, gửi thông báo"},
            {"id": "telegram_bot", "name": "Telegram Bot Điều Hành", "category": "Giao tiếp & Báo cáo", "status": "connected", "permission": "full_access", "permission_label": "Toàn quyền", "desc": "Báo cáo cho ban giám đốc, duyệt lệnh"},
            {"id": "facebook_page", "name": "Facebook Fanpage Graph API", "category": "Marketing", "status": "connected", "permission": "draft", "permission_label": "Soạn nháp", "desc": "Đăng bài, bình luận, gửi tin nhắn"},
            {"id": "gmail", "name": "Gmail Workspace", "category": "Email", "status": "connected", "permission": "draft", "permission_label": "Soạn nháp", "desc": "Soạn email báo cáo, trả lời đối tác"},
            {"id": "google_calendar", "name": "Google Calendar", "category": "Lịch biểu", "status": "connected", "permission": "full_access", "permission_label": "Toàn quyền", "desc": "Tự động lên lịch họp và nhắc việc"},
            {"id": "botcake", "name": "Botcake Chatbot", "category": "CSKH", "status": "ready", "permission": "draft", "permission_label": "Soạn nháp", "desc": "Kịch bản tin nhắn tự động theo luồng"},
            {"id": "webcake", "name": "Webcake Landing Page", "category": "Marketing", "status": "connected", "permission": "full_access", "permission_label": "Toàn quyền", "desc": "Đồng bộ lead đăng ký từ landing page"}
        ]
    }

class WorkflowTriggerRequest(BaseModel):
    workflow_id: str
    params: Dict[str, Any] = {}

# 6. Giả lập / thực thi chuỗi tác vụ doanh nghiệp đa hệ thống
@router.post("/run-workflow")
async def run_enterprise_workflow(req: WorkflowTriggerRequest):
    if req.workflow_id == "daily_reconciliation":
        return {
            "status": "success",
            "workflow_name": "Đối soát đa hệ thống: Meta Ads → Google Sheets → Pancake POS → Telegram",
            "steps": [
                {"step": 1, "action": "Kéo dữ liệu Meta Ads chi tiêu hôm nay (25.440.355đ)", "status": "done"},
                {"step": 2, "action": "Kéo 91 đơn hàng thành công từ Pancake POS", "status": "done"},
                {"step": 3, "action": "Tính toán CPA trung bình: 279.564đ/đơn và ghi vào Google Sheets", "status": "done"},
                {"step": 4, "action": "Gửi thông báo tổng hợp báo cáo về nhóm Telegram Ban Lãnh Đạo", "status": "done"}
            ],
            "message": "Chuỗi tác vụ đối soát doanh nghiệp đã hoàn tất trong 1.8 giây."
        }
    return {
        "status": "success",
        "workflow_name": f"Tác vụ doanh nghiệp [{req.workflow_id}]",
        "message": "Đã thực thi thành công tác vụ phòng ban."
    }
