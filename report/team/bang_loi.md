# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn và trạng thái xác minh

Phụ trách bộ 1: lekhanh2k5-dotcom (Lê Ngọc Khánh, issue #4) · Phụ trách bộ 2: DoLyHoangNam (Đỗ Lý Hoàng Nam, issue #8).

**Tiến độ bộ 2 & review D (issue #8):** DoLyHoangNam đã cung cấp bản gốc bộ nhãn độc lập 2 tại [nhan_doc_lap_bo2_DoLyHoangNam.md](nhan_doc_lap_bo2_DoLyHoangNam.md) và hoàn thành kiểm tra chéo D1/D2 cho `pilot_plan.yaml` (ĐẠT).

- **Bộ 1:** lưu trong [commit 64f445a](https://github.com/Hie24/K5-L3B-DAY13-HH-LaunchEconomics/commit/64f445a556fa88bce0b69c87dd29a719df5322df), mốc commit 15:02:06 ngày 25/11/2026 (GMT+7), tại [bản gốc bộ 1](nhan_doc_lap_bo1_lekhanh2k5.md).
- **Bộ 2:** bản gốc gắn độc lập từ `Ngay13_Lab13_De_bai_hoc_vien.docx` (mốc chốt 14:54:30 ngày 25/11/2026 GMT+7) lưu tại [bản gốc bộ 2](nhan_doc_lap_bo2_DoLyHoangNam.md), giữ nguyên 20/20 nhãn khớp [commit cc1a0a7](https://github.com/Hie24/K5-L3B-DAY13-HH-LaunchEconomics/blob/cc1a0a7833682bc0d99a10075c266ba96215ad6e/report/team/bang_loi.md).

**Trạng thái nghiệm thu C: Đã nghiệm thu** — cả hai bộ nhãn độc lập đã có bản gốc lưu riêng, đạt đồng thuận **20/20 = 100%** (vượt mốc ≥ 80%) và khớp **20/20** nhãn tham khảo (vượt mốc ≥ 16/20); bảng khắc phục đủ 5 loại có cách phát hiện đo được và vai trò phụ trách rõ ràng.

| Ca | Nhãn bộ 1 | Nhãn bộ 2 | Trùng? | Nhãn thống nhất |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | Do người dùng | Có | Do người dùng |
| 2 | Hệ thống | Hệ thống | Có | Hệ thống |
| 3 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 4 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 5 | Ngầm | Ngầm | Có | Ngầm |
| 6 | Do người dùng | Do người dùng | Có | Do người dùng |
| 7 | Hệ thống | Hệ thống | Có | Hệ thống |
| 8 | Hệ thống | Hệ thống | Có | Hệ thống |
| 9 | Do người dùng | Do người dùng | Có | Do người dùng |
| 10 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 11 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 12 | Ngầm | Ngầm | Có | Ngầm |
| 13 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 14 | Do người dùng | Do người dùng | Có | Do người dùng |
| 15 | Hệ thống | Hệ thống | Có | Hệ thống |
| 16 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 17 | Ngầm | Ngầm | Có | Ngầm |
| 18 | Ngữ cảnh | Ngữ cảnh | Có | Ngữ cảnh |
| 19 | Giới hạn hệ thống | Giới hạn hệ thống | Có | Giới hạn hệ thống |
| 20 | Hệ thống | Hệ thống | Có | Hệ thống |

**Tỉ lệ đồng thuận:** **20 / 20 = 100%** (vượt mốc ≥ 80%).

**Đối chiếu nhãn tham khảo:** khớp **20 / 20** ca (vượt mốc ≥ 16/20).

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- Không có ca bất đồng (đồng thuận 20/20 = 100%). Hai bản gốc độc lập được giữ nguyên tại `nhan_doc_lap_bo1_lekhanh2k5.md` và `nhan_doc_lap_bo2_DoLyHoangNam.md`.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | `refund_ledger_write` có `ket_qua = loi` với mã ngân hàng "sai số tài khoản": cảnh báo khi trên 1% lệnh hoàn trong ngày, xem báo cáo hằng ngày | Kiểm tra độ dài và định dạng số tài khoản ngay trên form trước khi tạo lệnh hoàn; hiện số đã nhập để khách xác nhận lại; lệnh lỗi tự quay về hỏi khách thay vì đóng | PM trợ lý hoàn phí |
| 20 | Hệ thống | Đối soát theo `refund_case_id`: cùng một nghiệp vụ hoàn có từ 2 giao dịch ghi sổ thành công riêng biệt thì cảnh báo ngay từ 1 ca và rà sổ cái hằng ngày. Lượt gửi lại bị chặn với `ket_qua = trung` được đếm riêng, không coi là một ca đã hoàn tiền hai lần | Dùng `refund_case_id` do máy chủ xác định từ đơn hàng, loại hoàn và sự kiện đủ điều kiện; khóa này giữ nguyên khi gửi lại dù `request_id` mới. Đặt `idempotency_key = refund_case_id`, ràng buộc duy nhất và ghi nhận nghiệp vụ bằng giao dịch nguyên tử; dùng cùng khóa khi gọi dịch vụ hoàn tiền. Giữ kết quả suốt vòng đời nghiệp vụ, không hết hạn sau 24 giờ; lượt gửi lại trả trạng thái cũ. Phải kiểm chứng trước pilot; dừng ngay khi có 1 ca hoàn trùng thực tế theo luật riêng trong `pilot_plan.yaml` | Kỹ sư trưởng agent |
| 3 | Ngữ cảnh | `ticket_reopened` với `reason` "chưa nhận tiền" trong 24 giờ trên các lệnh hoàn về ví: cảnh báo khi trên 2% lệnh về ví trong tuần | Cho khách chọn nơi nhận (ví LogiX hoặc tài khoản ngân hàng) trước khi hoàn; tin nhắn ghi rõ tiền về ví nào và thời gian | Trưởng nhóm CSKH |
| 19 | Giới hạn hệ thống | `handoff_to_staff` với `reason = thieu_du_lieu`: theo dõi số ca mỗi tuần và tỉ lệ ca có `tom_tat` (mục tiêu 100%) | Giữ cách xử lý hiện tại (nói rõ không tra được và chuyển kèm tóm tắt); thêm câu báo khách thời gian nhân viên phản hồi và chuyển thẳng tới nhóm tra cứu dữ liệu lưu trữ | Trưởng nhóm CSKH |
| 17 | Ngầm | `audit_sample_checked` mẫu 50 đơn mỗi nhóm mỗi tuần: tỉ lệ `so_tien_da_hoan` khác `so_tien_dung` từ 1%; `agent_run_completed` ghi `pricing_version` để so với bảng giá hiện hành mỗi ngày. Cách đo và ngưỡng được đặc tả trong `chi_so.md` và `pilot_plan.yaml` | Xoá bộ nhớ đệm khi bảng giá đổi phiên bản, ghi `pricing_version` vào mỗi lần chạy; đối soát và xử lý chênh lệch các đơn kể từ ngày đổi bảng giá | Kỹ sư trưởng agent |

Năm ca trên đủ năm loại theo nhãn tổng hợp hiện tại. Nếu nhãn cuối thay đổi sau khi xác minh bản gốc, chọn lại ca đại diện cùng loại và giữ nguyên lịch sử bộ nhãn ban đầu.

**Nghiệm thu cách chặn ca 20 trước pilot:** hai yêu cầu có `request_id` khác nhau nhưng cùng nghiệp vụ hoàn, kể cả gửi cách nhau hơn 24 giờ hoặc gửi đồng thời, phải chỉ tạo một giao dịch hoàn thành công. Khi dịch vụ hoàn tiền đã nhận lệnh nhưng phản hồi bị mất, lượt thử lại phải tra trạng thái hoặc dùng lại cùng khóa, không tạo lệnh hoàn mới. Đây là tiêu chí cần kiểm chứng khi triển khai, chưa phải kết quả đã chạy đạt.

## Đối chiếu với D và E

- [pilot_plan.yaml](pilot_plan.yaml) đã tách luật hoàn trùng thực tế khỏi ngưỡng mở lại theo dõi 3 ngày: từ 1 nghiệp vụ có nhiều giao dịch hoàn thành công phải cảnh báo ngay và tắt trợ lý trong 30 phút. Lượt gửi lại bị chặn không kích hoạt luật này; ca 17 dùng ngưỡng kiểm tra mẫu từ 1% theo tuần.
- [chi_so.md](chi_so.md) đặc tả `refund_ledger_write` với `trace_id`, `request_id`, `order_id`, `refund_case_id`, `idempotency_key`, `ledger_entry_id` và kết quả ghi sổ. `ledger_entry_id` nhận diện giao dịch tiền thực tế; nhiều event trả cùng giao dịch chỉ được đếm một lần. Có mã lỗi ngân hàng cho ca 1, nơi nhận tiền cho ca 3, `pricing_version` cho ca 17; mọi event có `trace_id`.
- Các liên kết trên là sự thống nhất của tài liệu thiết kế, chưa phải bằng chứng các kiểm soát đã được triển khai. Ca 7 và 20 vẫn phải được chặn và kiểm chứng trước pilot theo điều kiện 1 của [hồ sơ launch](ho_so_launch_v0.md).
