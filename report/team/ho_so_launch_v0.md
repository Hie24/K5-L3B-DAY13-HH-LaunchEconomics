# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Nhóm: HH · Lớp: L3B

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | Toàn mẫu: **4.472 đ** (`simulated`, gấp 16,3× hoá đơn 275 đ/yêu cầu). Phạm vi `noi_dia + hang_nang`: **3.414 đ** chưa cố định; cộng cố định 40 tr/tháng là **4.599 đ** ở 45.000 yc/tháng (33.750 việc TC) và **5.784 đ** ở nửa khối lượng (`simulated`). Đây là mốc A4 với tối đa 3 lần chạy. | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | 1) Số ca làm lại (+51,8% lên 6.787 đ khi ×2); 2) Tỉ lệ xem lại (+40,7% lên 6.292 đ khi ×2); 3) Lương nhân viên (+23,1% lên 5.506 đ khi +25%). Giá token ×2 chỉ +5,6% (`simulated`). | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Cả hệ thống (74 ca làm lại + 148 ca chuyển, cộng 12.000 đ/ca): **5.865 đ/yc = 0,49×**, chưa cố định; giới hạn 2 lần: **5.751 đ/yc**. Riêng phạm vi pilot, 2 lần tốn **4.053 đ/yc**, thấp hơn 3 lần (**4.131 đ/yc**), chưa cố định. Xem lại 100%: **11.743–12.415 đ/việc** chưa cố định; cộng cố định theo A4 thành **12.928–13.600 đ/việc** (`simulated`), vượt mốc 12.000 đ. | Giả lập | Giám đốc vận hành LogiX-VN |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Trong đợt chạy thử (không đối chứng): Chính **82,83%** (994/1.200); Dùng (bỏ qua `sua+bo`) **27,12%** (48/177); An toàn (mở lại 7 ngày) **4,25%** (51/1.200; phạm vi pilot **3,97%**). Tính bằng `nhiem_vu_e1()` trong `src/lab13.py`; `chi_so.md` có thêm 2 chỉ số đề xuất (tỉ lệ mở gợi ý, tỉ lệ hoàn sai qua kiểm tra mẫu) và 10 event có `trace_id`. | Xong, có bằng chứng | Trưởng nhóm CSKH |
| 5 · Bảng lỗi và cách khắc phục | 20 ca, 5 loại Google PAIR: hai cột nhãn trùng **20/20** theo số học, nhưng **chưa đủ bằng chứng** bộ 2 là lượt gắn độc lập (bộ 1 khoá ở commit `64f445a` lúc 15:02:06; bộ 2 commit `cc1a0a7` chờ Nam xác nhận ở issue #8). Bảng khắc phục 5 ca (ca 1, 20, 3, 19, 17) đã có, mỗi ca có cách phát hiện đo được và một vai trò; ca 20 chống hoàn trùng theo `refund_case_id`. Ca 7 (sổ cái 503 vẫn báo đã hoàn) và Ca 20 (hoàn trùng) phải được chặn trước pilot (`bang_loi.md`). | Chưa | Kỹ sư trưởng agent |
| 6 · Pilot plan | `pilot_plan.yaml`: **20 + 20 nhân viên**, ngẫu nhiên phân tầng theo depot, đối chứng đồng thời; trần 1.000 < 1.251 nên chọn **MDE +6 điểm**, n=859/nhóm, m≥299, DE=6,96; power chỉ **0,642** nếu tác động thật +5 điểm. Rollout 10%→25%→50% từ 2026-12-07; 4 luật dừng (an toàn, chi phí > 6.000 đ `simulated`, mức dùng, lỗi ngầm); rollback 30 phút; quyết định **2027-01-12**. | Xong, có bằng chứng | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | 1) Làm lại ×2 → +51,8% (6.787 đ); 2) Xem lại 100% kéo dài → 0,98×–1,03× (không tiết kiệm); 3) Khối lượng giảm nửa → cố định tăng từ +1.185 đ lên +2.370 đ/việc (`simulated`). | Giả lập | PM trợ lý hoàn phí |

Phạm vi đề xuất là `noi_dia` + `hang_nang`; `quoc_te` và `doi_tac` có cps tương ứng 1,88× và 0,85× mốc 12.000 đ (`simulated`), tỷ lệ thành công thấp và rủi ro điều khoản riêng nên được loại. Các mốc kiểm tra dưới đây khớp lịch trong `pilot_plan.yaml` (bắt đầu thứ Hai 2026-12-07); điều kiện 1–2 trước khi bắt đầu, điều kiện 3–4 theo tuần pilot.

- **Điều kiện 1 (Chặn lỗi nghiêm trọng):** Sửa khóa chống trùng (`idempotency_key`) và đối soát sổ cái 503 (Ca 7, Ca 20) — Phụ trách: **Kỹ sư trưởng agent** · Ngày kiểm tra: **2026-12-02** (trước ngày bắt đầu pilot).
- **Điều kiện 2 (Chấp nhận đánh đổi thống kê):** Ký duyệt đánh đổi MDE từ +5 lên +6 điểm (biết rõ power chỉ còn 0,642 nếu tác động thật là +5 điểm) và chốt `pilot_plan.yaml` — Phụ trách: **Giám đốc vận hành LogiX-VN** · Ngày kiểm tra: **2026-12-02**.
- **Điều kiện 3 (Đo thật thay cho `simulated`):** Bật đủ ≥ 6 event có `trace_id`, đo trực tiếp `phut_xem_lai` và `phut_lam_lai` sau tuần 1 để thay toàn bộ số `simulated` — Phụ trách: **PM trợ lý hoàn phí** · Ngày kiểm tra: **2026-12-11** (ngày làm việc cuối tuần 1).
- **Điều kiện 4 (Lộ trình giảm xem lại):** Áp dụng lộ trình giảm tỉ lệ xem lại theo bậc (không giữ 100% xem lại sau bước 0.25 vì chi phí đạt 0,98×–1,03×) — Phụ trách: **Trưởng nhóm CSKH** · Ngày kiểm tra: **2026-12-18** (ngày làm việc cuối tuần 2).

**Đề xuất: Go có điều kiện** cho kế hoạch pilot `noi_dia` + `hang_nang`, tối đa 2 lần chạy, sau khi đạt điều kiện 1–2; thực hiện tiếp các mốc điều kiện 3–4 và ra quyết định ngày 2027-01-12, ngân sách xem lại 100% phải gồm cố định.
