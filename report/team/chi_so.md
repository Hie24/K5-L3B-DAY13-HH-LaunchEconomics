# Đặc tả chỉ số, event và rủi ro kinh tế · Nhiệm vụ E1, E2

Phụ trách: lekhanh2k5-dotcom (issue #6) · kiểm tra chéo: Hie24. Số E1 do `src/lab13.py` (hàm `nhiem_vu_e1`) tính trên
1.200 yêu cầu của đợt chạy thử; phạm vi pilot là `noi_dia` + `hang_nang` (982 yêu cầu).

## E1 · Đặc tả chỉ số

| Loại | Chỉ số | Công thức | Tính thử trên 1.200 yêu cầu |
| --- | --- | --- | --- |
| Chính (kết quả) | % yêu cầu đóng trong 24 giờ và không mở lại trong 7 ngày | `dong_trong_24h` bằng 1 và `mo_lai_trong_7_ngay` bằng 0, chia tổng số yêu cầu | **82,83%** (994/1.200); phạm vi pilot 92,26% (906/982) |
| Dùng | Tỉ lệ bỏ qua gợi ý | `quyet_dinh_xem_lai` là `sua` hoặc `bo`, chia số yêu cầu được xem lại | **27,12%** (48/177); phạm vi pilot 21,09% (27/128) |
| An toàn | Tỉ lệ lỗi lọt đến khách | `mo_lai_trong_7_ngay` bằng 1, chia tổng số yêu cầu | **4,25%** (51/1.200); phạm vi pilot 3,97% (39/982) |
| Dùng | Nhóm tự đề xuất: **tỉ lệ mở gợi ý** của nhân viên nhóm trợ lý | Số yêu cầu trong phạm vi có `agent_suggestion_shown` được nhân viên mở, chia số `refund_request_created` trong phạm vi giao cho nhóm trợ lý; tính hằng ngày theo `staff_id`; Trưởng nhóm CSKH theo dõi | Không cần tính |
| An toàn | Nhóm tự đề xuất: **tỉ lệ hoàn sai tiền qua kiểm tra mẫu** (bắt lỗi ngầm như ca 5, 17) | Số đơn trong `audit_sample_checked` có `so_tien_da_hoan` khác `so_tien_dung`, chia số đơn được kiểm; mẫu ngẫu nhiên 50 đơn/tuần mỗi nhóm; Kế toán trưởng theo dõi | Không cần tính |

Viết "chỉ số trong đợt chạy thử là …", không viết "trợ lý đã nâng chỉ số": đợt chạy thử không có nhóm đối chứng.

- Chỉ số chính trong đợt chạy thử là 82,83%. Con số này **không** so được với baseline 0,70 để kết luận về tác động, vì
  2 tuần chạy thử ở 6 depot không có nhóm đối chứng cùng thời gian; pilot ở `pilot_plan.yaml` mới tách được tác động.
- Hai con số bất lợi để theo dõi: 12,33% yêu cầu (148/1.200) chạy hết 3 lần vẫn lỗi và phải chuyển nhân viên (trong
  phạm vi còn 3,46%, 34/982), và 6,17% (74/1.200) phải làm lại (trong phạm vi 4,89%, 48/982).

## Danh sách event

Ít nhất sáu event, mỗi event có `trace_id` để nối với trace của agent.

| Event | Ai tạo | Thuộc tính chính | Thời điểm |
| --- | --- | --- | --- |
| `refund_request_created` | App khách / cổng CSKH | request_id, loai, so_tien_vnd, depot, staff_id, arm (tro_ly / doi_chung), trace_id | Khi khách gửi yêu cầu |
| `agent_run_completed` | Agent | run_id, attempt, tokens_in, tokens_out, tool_calls, status (ok / loi), trace_id | Sau **mỗi** lần chạy, kể cả lần lỗi |
| `agent_suggestion_shown` | Giao diện nhân viên | staff_id, so_tien_de_xuat, opened (true / false), trace_id | Khi gợi ý hiện ra và khi nhân viên mở |
| `staff_review_decision` | Nhân viên | quyet_dinh (giu / sua / bo), phut_xem_lai đo thật, trace_id | Khi bấm gửi, sửa hoặc bỏ |
| `staff_rework_completed` | Nhân viên | phut_lam_lai đo thật, ly_do, trace_id | Khi làm lại xong |
| `handoff_to_staff` | Agent | reason (het_3_lan / ngoai_pham_vi / thieu_du_lieu), tom_tat, trace_id | Khi chuyển nhân viên |
| `refund_ledger_write` | Dịch vụ sổ cái | idempotency_key, so_tien, ket_qua (ok / loi / trung), trace_id | Khi ghi hoàn tiền vào sổ cái |
| `ticket_closed` | Hệ thống ticket | closed_at, trace_id | Khi yêu cầu đóng |
| `ticket_reopened` | Khách | reopened_at, reason, trace_id | Khi khách mở lại (theo dõi 7 ngày) |
| `audit_sample_checked` | Kế toán | so_tien_da_hoan, so_tien_dung, trace_id | Hằng tuần, mẫu ngẫu nhiên |

**Kiểm tra chéo:** với mỗi chỉ số ở bảng E1, ghi event dùng để tính. Chỉ số nào không tính được từ danh sách event thì chưa đo được.

- **Chính:** `refund_request_created` (mẫu số, theo arm) + `ticket_closed` (đóng trong 24 giờ so với created_at) + `ticket_reopened` (không mở lại trong 7 ngày).
- **Dùng, bỏ qua gợi ý:** `staff_review_decision` (sua / bo trên tổng số quyết định xem lại).
- **An toàn, lỗi lọt đến khách:** `ticket_reopened` chia `refund_request_created`.
- **Dùng, tỉ lệ mở gợi ý (đề xuất):** `agent_suggestion_shown.opened` chia `refund_request_created` của nhóm trợ lý. Event này cũng dùng để phát hiện nhóm đối chứng dùng ké (spillover).
- **An toàn, hoàn sai qua kiểm tra mẫu (đề xuất):** `audit_sample_checked`. Đây là cách duy nhất thấy lỗi ngầm, vì lỗi ngầm không sinh `ticket_reopened`.
- **Chi phí mỗi việc thành công:** `agent_run_completed` (token và tool của mọi lần chạy, kể cả lỗi) + `staff_review_decision.phut_xem_lai` + `staff_rework_completed.phut_lam_lai` (thay phút **simulated** bằng phút đo thật), chia số yêu cầu thành công từ `ticket_closed` / `ticket_reopened`.
- **Luật dừng hoàn trùng** (`pilot_plan.yaml`): `refund_ledger_write` có `ket_qua = trung` hoặc hai bản ghi cùng request_id.

## E2 · Rủi ro kinh tế

Ít nhất hai dòng, số lấy từ bảng độ nhạy (`bang_chi_phi.md`).

| Rủi ro | Tác động đã tính | Dấu hiệu theo dõi | Hành động | Người phụ trách |
| --- | --- | --- | --- | --- |
| Khối lượng thấp hơn dự kiến làm chi phí cố định 40 triệu đ/tháng chia cho ít việc hơn | +1.185 đ mỗi việc thành công ở 45.000 yêu cầu/tháng (phạm vi 81,8%, thành công 91,65%: 33.750 việc/tháng); **+2.370 đ** nếu khối lượng còn một nửa. Khớp A4 của #2 (PR #11: 33.750 việc/tháng, 1.185,19 đ) | Số việc thành công trong phạm vi theo tuần dưới 50% kế hoạch (dưới khoảng 3.900 việc/tuần) | Không mở rộng pilot; xem lại hợp đồng chi phí cố định trước ngày quyết định 2027-01-12 | PM trợ lý hoàn phí |
| Số ca làm lại tăng gấp đôi | Chờ kịch bản "làm lại ×2" ở bảng B1 (#3, simulated) | Tỉ lệ làm lại theo tuần trong phạm vi vượt 7% (đợt chạy thử: 4,89%, 48/982) | Thu hẹp về `noi_dia`; rà 20 trace làm lại gần nhất trong 3 ngày làm việc | PM trợ lý hoàn phí |
| Phải xem lại 100% kéo dài | Chờ kịch bản B4 (#3, simulated) | % yêu cầu được xem lại còn trên 50% ở cuối bước rollout 0,25 (đợt chạy thử: 13,03% trong phạm vi) | Giảm xem lại theo bậc khi tỉ lệ bỏ qua gợi ý dưới 15% | Trưởng nhóm CSKH |
