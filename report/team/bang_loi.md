# Bảng lỗi và cách khắc phục · Nhiệm vụ C

20 ca lỗi nằm trong `docs/Ngay13_Lab13_De_bai_hoc_vien.docx`. Năm loại theo Google PAIR: **Do người dùng · Hệ thống · Ngữ cảnh · Giới hạn hệ thống · Ngầm**. Gắn nhãn theo nguyên nhân gốc, không theo chỗ cần sửa.

## Hai bộ nhãn độc lập

Người gắn nhãn 1: lekhanh2k5-dotcom (Lê Ngọc Khánh, issue #4) · Người gắn nhãn 2: DoLyHoangNam (Đỗ Lý Hoàng Nam, issue #8) (gắn trong 8 phút, không trao đổi)

Bằng chứng độc lập: bộ 1 được khoá trong commit `64f445a` lúc 15:02:06 ngày 25/11, trước khi xem bộ 2 (file `report/team/nhan_doc_lap_bo1_lekhanh2k5.md`). Bộ 2 được đẩy lên repo lúc 16:33 ngày 25/11 (nhánh `feat/issue-8-c-labels-2`, commit `cc1a0a7`); Nam xác nhận qua nhóm chat của nhóm (16:39 ngày 25/11, Khánh ghi nhận) rằng bộ 2 là lượt gắn nhãn độc lập của mình. Hai bộ ban đầu giữ nguyên; chỉ cột "Nhãn thống nhất" được điền sau khi so.

| Ca | Nhãn người 1 | Nhãn người 2 | Trùng? | Nhãn thống nhất |
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

**Tỉ lệ đồng thuận:** 20 / 20 = 100% (≥ 80%)

**Đối chiếu nhãn tham khảo (chỉ sau khi cả hai bộ đã khoá):** nhãn thống nhất khớp 20/20 ca (yêu cầu ≥ 16/20).

## Quy tắc phân biệt cho các ca không trùng

Mỗi ca không trùng một câu. Đồng thuận dưới 80% thì ghi định nghĩa đã viết lại.

- Không có ca lệch: hai bộ trùng cả 20 ca nên không cần quy tắc phân biệt hay viết lại định nghĩa.

## Bảng khắc phục cho 5 ca, mỗi loại một ca

Cách phát hiện phải đo được (event, ngưỡng, tần suất). Người phụ trách là một vai trò, không ghi "cả đội".

| Ca | Loại lỗi | Phát hiện bằng gì | Khắc phục thế nào | Ai phụ trách |
| --: | --- | --- | --- | --- |
| 1 | Do người dùng | `refund_ledger_write` có `ket_qua = loi` với mã ngân hàng "sai số tài khoản": cảnh báo khi trên 1% lệnh hoàn trong ngày, xem báo cáo hằng ngày | Kiểm tra độ dài và định dạng số tài khoản ngay trên form trước khi tạo lệnh hoàn; hiện số đã nhập để khách xác nhận lại; lệnh lỗi tự quay về hỏi khách thay vì đóng | PM trợ lý hoàn phí |
| 20 | Hệ thống | `refund_ledger_write` có hai bản ghi cùng `request_id` hoặc `ket_qua = trung`: cảnh báo ngay từ 1 ca; đối soát sổ cái hằng ngày | Ghi sổ cái bằng `idempotency_key = request_id`, chặn lệnh thứ hai trong 24 giờ; khách gửi lại thì trả trạng thái lệnh cũ. Phải xong trước ngày bắt đầu pilot (luật dừng an toàn trong `pilot_plan.yaml` dừng ngay từ 1 ca hoàn trùng) | Kỹ sư trưởng agent |
| 3 | Ngữ cảnh | `ticket_reopened` với `reason` "chưa nhận tiền" trong 24 giờ trên các lệnh hoàn về ví: cảnh báo khi trên 2% lệnh về ví trong tuần | Cho khách chọn nơi nhận (ví LogiX hoặc tài khoản ngân hàng) trước khi hoàn; tin nhắn ghi rõ tiền về ví nào và thời gian | Trưởng nhóm CSKH |
| 19 | Giới hạn hệ thống | `handoff_to_staff` với `reason = thieu_du_lieu`: theo dõi số ca mỗi tuần và tỉ lệ ca có `tom_tat` (mục tiêu 100%) | Giữ cách xử lý hiện tại (nói rõ không tra được và chuyển kèm tóm tắt); thêm câu báo khách thời gian nhân viên phản hồi và chuyển thẳng tới nhóm tra cứu dữ liệu lưu trữ | Trưởng nhóm CSKH |
| 17 | Ngầm | `audit_sample_checked` mẫu 50 đơn mỗi nhóm mỗi tuần: tỉ lệ `so_tien_da_hoan` khác `so_tien_dung` từ 1% (luật dừng lỗi ngầm trong `pilot_plan.yaml`); `agent_run_completed` ghi `pricing_version` để so với bảng giá hiện hành mỗi ngày | Xoá bộ nhớ đệm khi bảng giá đổi phiên bản, ghi `pricing_version` vào mỗi lần chạy; đối soát và hoàn bù các đơn lệch kể từ ngày đổi bảng giá | Kỹ sư trưởng agent |

Năm ca trên chọn theo nhãn bộ 1; nếu nhãn thống nhất của ca nào đổi loại sau khi so, thay bằng ca khác cùng loại đã thống nhất.
Ca 7 và ca 20 (báo đã hoàn khi sổ cái lỗi, hoàn trùng) phải chặn trước pilot, khớp điều kiện 1 của `ho_so_launch_v0.md`;
event và ngưỡng dùng chung với `chi_so.md` (#6) và luật dừng trong `pilot_plan.yaml` (#5).
