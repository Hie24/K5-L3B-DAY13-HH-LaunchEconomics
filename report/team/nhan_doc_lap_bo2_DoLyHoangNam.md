# Nhãn độc lập bộ 2 & Kiểm tra chéo D — DoLyHoangNam (issue #8)

Gắn độc lập 20 ca lỗi trực tiếp từ `docs/Ngay13_Lab13_De_bai_hoc_vien.docx` theo **nguyên nhân gốc**, không trao đổi, không xem bộ 1 (`nhan_doc_lap_bo1_lekhanh2k5.md`) và không đọc bảng tham khảo trước khi chốt.

- **Người gắn nhãn bộ 2:** Đỗ Lý Hoàng Nam (`DoLyHoangNam`, MSSV `2A202603777`)
- **Mốc chốt độc lập:** `2026-11-25 14:54:30 GMT+7` (trước khi đối chiếu với bộ 1 và tài liệu hướng dẫn chi tiết)

## 1. Bộ nhãn độc lập 2 (20 ca theo 5 loại Google PAIR)

| Ca | Nhãn bộ 2 | Lý do theo nguyên nhân gốc |
| --: | --- | --- |
| 1 | Do người dùng | Khách nhập thiếu 2 chữ số số tài khoản nhận hoàn tiền |
| 2 | Hệ thống | Trợ lý gọi tool tra bảng giá sai tham số (hàng thường thay vì hàng nặng) |
| 3 | Ngữ cảnh | Hoàn về ví LogiX đúng thiết kế nhưng lệch kỳ vọng tài khoản ngân hàng của khách |
| 4 | Giới hạn hệ thống | LogiX không có dữ liệu chặng do hãng nước ngoài giao |
| 5 | Ngầm | 14 đơn có mã giảm giá bị hoàn thừa, không khách nào báo, không cảnh báo, kiểm tra mẫu mới thấy |
| 6 | Do người dùng | Khách chọn nhầm mục "Hoàn phí giao trễ" thay vì hàng bị vỡ |
| 7 | Hệ thống | API sổ cái trả lỗi 503 nhưng trợ lý vẫn báo khách "đã hoàn tiền thành công" |
| 8 | Hệ thống | Trợ lý bịa "Điều 7.2" không có trong chính sách hiện hành (lộ ra ngay trên câu trả lời) |
| 9 | Do người dùng | Khách nhập mã đơn sàn TMĐT thay vì mã vận đơn (không gợi ý là phần cần khắc phục) |
| 10 | Ngữ cảnh | Từ chối đúng điều khoản bất khả kháng nhưng lệch ngữ cảnh cam kết giao 24h trên app |
| 11 | Giới hạn hệ thống | Trợ lý không xử lý được đầu vào âm thanh (tin nhắn thoại 40 giây) |
| 12 | Ngầm | Tool depot D05 trả thiếu trường làm tiền token gấp 3 suốt 3 tuần không ai thấy |
| 13 | Giới hạn hệ thống | Hoàn phí bảo hiểm hàng hoá đối tác nằm ngoài phạm vi trợ lý |
| 14 | Do người dùng | Khách bấm nhầm nút "Xác nhận đã nhận tiền" |
| 15 | Hệ thống | Trợ lý tính sai chính sách (hoàn 100% thay vì 50%), nhân viên bắt được khi xem lại |
| 16 | Ngữ cảnh | Gửi thông báo Zalo đúng thiết kế "gửi ngay" nhưng sai bối cảnh thời gian (2:14 sáng) |
| 17 | Ngầm | Bộ nhớ đệm bảng giá cũ gây lệch 1.000–2.000 đ trên 212 đơn trong 9 ngày không ai mở lại |
| 18 | Ngữ cảnh | Tính đúng số tiền nhưng thiếu cách tính khiến khách hiểu nhầm là hoàn thiếu |
| 19 | Giới hạn hệ thống | Đơn từ 14 tháng trước, vượt giới hạn truy cập dữ liệu 12 tháng |
| 20 | Hệ thống | Thiếu khoá chống trùng (`idempotency_key`) khiến hoàn tiền hai lần cho cùng một đơn |

**Phân bố bộ 2:** Do người dùng (**4**: `1, 6, 9, 14`) · Hệ thống (**5**: `2, 7, 8, 15, 20`) · Ngữ cảnh (**4**: `3, 10, 16, 18`) · Giới hạn hệ thống (**4**: `4, 11, 13, 19`) · Ngầm (**3**: `5, 12, 17`).

## 2. Xác nhận kiểm tra chéo D1/D2 (Issue #5 — `pilot_plan.yaml`)

Đã kiểm chứng độc lập phép tính cỡ mẫu D1 và cấu hình `report/team/pilot_plan.yaml`:
- `yaml.safe_load`: **OK**, 0 dấu `?` ngoài chú thích, 0 từ bị cấm.
- **D1:** a) `1.251` (`statsmodels`: `1.250`); b) `m = 75` → `DE = 2,48`, `n = 3.103`/nhóm → `42` nhân viên/nhóm (`84 > 40`, không đủ); c) `20` nhân viên/nhóm → trần `c / ICC = 1.000 < 1.251`; d) `6` depot/nhóm → trần `300`; e) MDE +6 điểm (`n = 859`/nhóm) → `20m / (1 + 0,02(m - 1)) ≥ 859 ⇒ m ≥ 299` (`DE = 6,96`), power còn **0,642** nếu tác động thật là +5 điểm.
- **D2 & D3:** Đủ 5 tiêu chí tách tác động, 4 luật dừng đủ 4 vế `NẾU – TRONG – THÌ – KHÔNG THÌ`, ngưỡng mở lại phù hợp baseline hiện tại (`3,97%` trong phạm vi `noi_dia + hang_nang`), khớp giới hạn tối đa 2 lần chạy theo B3 (`6.901.220 đ`, `simulated`).
- **Kết luận review D:** **ĐẠT**.
