---
title: Kiến Trúc Bộ Não AI Doanh Nghiệp 4 Lớp
tags: [enterprise, architecture, second-brain, mcp, agents]
updated: 2026-11-15
department: Ban Lãnh Đạo & Toàn Công Ty
---

# Kiến Trúc Bộ Não AI Doanh Nghiệp 4 Lớp

> **Triết lý cốt lõi:** *"Một bộ não chung, mọi trợ lý cùng dùng. Tri thức, quy trình và số liệu không còn nằm rải rác trong đầu nhân sự và các thư mục tài liệu."*

---

## 4 Lớp Năng Lực Toàn Diện

### 1. Lớp Tri Thức (Second Brain Tập Trung)
- [[SOP - Quy Trinh Ban Hang Zalo 24-7]]
- [[Chinh Sach Bang Gia Doanh Nghiep 2026]]
- [[Quy Trinh Doi Soat Ads - POS - Sheets]]
- Tài liệu, quy trình, chính sách, hồ sơ khách hàng số hoá thành wiki liên kết tự động.
- Dữ liệu định dạng Markdown mở, tự host trên hạ tầng riêng của công ty, sao lưu 2 chiều GitHub.

### 2. Lớp Dữ Liệu Thật (MCP Connectors)
- Kết nối trực tiếp 15+ hệ thống: Pancake POS, KiotViet, Meta Ads, TikTok Ads, Google Sheets, Gmail, Calendar, Zalo...
- **Phân quyền do hệ thống thực thi:**
  - `Chỉ đọc (Read-only)`: Trợ lý xem số liệu, không thay đổi gì.
  - `Soạn nháp (Draft)`: Trợ lý chuẩn bị nội dung, người có thẩm quyền duyệt.
  - `Toàn quyền (Full)`: Trợ lý tự thực hiện với tác vụ tin cậy lặp lại.

### 3. Lớp Đội Trợ Lý Theo Phòng Ban (Department Agents)
- **Ban Lãnh Đạo:** Trợ lý tổng hợp báo cáo kinh doanh qua Telegram Bot, đối soát doanh thu chi phí.
- **Bán Hàng & CSKH:** Bot Zalo 24/7 trả lời theo giá và tồn kho thật, nhớ lịch sử từng khách, chuyển giao người thật khi vượt thẩm quyền.
- **Marketing & Nội Dung:** Viết 1 lần, đăng 6 kênh (Facebook, Instagram, Threads, TikTok, YouTube, Zalo), đúng 100% Brand Voice.
- **Vận Hành & Kế Toán:** 1 lệnh chạy chuỗi việc: kéo Meta Ads -> Google Sheets -> POS -> báo Telegram.

### 4. Lớp Kênh Làm Việc (Multi-Channel Interface)
- Web Cockpit điều hành thời gian thực.
- Telegram Bot điều hành & phê duyệt cho lãnh đạo.
- Zalo Agent giao tiếp trực tiếp với khách hàng.
- Desktop App chạy ngầm 24/7.
