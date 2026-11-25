# Hồ sơ launch v0 · Trợ lý hoàn phí LogiX-VN · Gate 2a

Một trang. Cột trạng thái chỉ nhận: **Xong, có bằng chứng · Chưa · Giả lập**. Mục nào dựa trên cột `_simulated` ghi Giả lập. Người phụ trách là một vai trò, không ghi "cả đội". Gate 2a chỉ duyệt kế hoạch pilot: không viết như thể trợ lý đã được duyệt chạy chính thức (xem quy tắc 5 trong `README.md`).

Nhóm: HH · Lớp: L3B

| Mục | Con số chính | Trạng thái | Người phụ trách |
| --- | --- | --- | --- |
| 1 · Chi phí mỗi việc thành công | Toàn mẫu: **4.472 đ** (`simulated`, gấp 16,3× hoá đơn 275 đ/yêu cầu). Phạm vi `noi_dia + hang_nang`: **3.414 đ** chưa cố định; cộng cố định 40 tr/tháng là **4.599 đ** ở 45.000 yc/tháng (33.750 việc TC) và **5.784 đ** ở nửa khối lượng (`simulated`). | Giả lập | PM trợ lý hoàn phí |
| 2 · Ba yếu tố nhạy nhất | 1) Số ca làm lại (+51,8% lên 6.787 đ khi ×2); 2) Tỉ lệ xem lại (+40,7% lên 6.292 đ khi ×2); 3) Lương nhân viên (+23,1% lên 5.506 đ khi +25%). Giá token ×2 chỉ +5,6% (`simulated`). | Giả lập | PM trợ lý hoàn phí |
| 3 · So với nhân viên tự làm | Cả hệ thống (đã cộng 222 ca chuyển nhân viên × 12.000 đ): **5.865 đ/yc = 0,49×** (giới hạn 2 lần chạy rẻ nhất: **5.751 đ/yc = 0,48×**). **Số bất lợi:** `quoc_te` tốn 22.515 đ (1,88×), `doi_tac` 10.215 đ (0,85×) → loại khỏi pilot; nếu xem lại 100% (`noi_dia + hang_nang`): **11.743 đ = 0,98×** (9 phút làm lại) hoặc **12.415 đ = 1,03×** (15,3 phút/ca như dữ liệu) (`simulated`). | Giả lập | Giám đốc vận hành LogiX-VN |
| 4 · Chỉ số chính, chỉ số dùng, chỉ số an toàn | Trong đợt chạy thử (không đối chứng): Chính (đóng 24h & không mở lại 7 ngày) **82,83%** (994/1.200); Dùng (tỉ lệ bỏ qua `sua+bo`) **27,12%** (48/177); An toàn (mở lại 7 ngày) **4,25%** (51/1.200; phạm vi pilot **3,97%**). Cần đo thật thời gian xem lại/làm lại qua ≥ 6 event có `trace_id`. | Xong, có bằng chứng *(chờ đồng bộ chốt từ #6)* | Trưởng nhóm CSKH |
| 5 · Bảng lỗi và cách khắc phục | 20 ca lỗi theo 5 loại Google PAIR; bộ nhãn độc lập 2 đã chốt (4 Do người dùng, 5 Hệ thống, 4 Ngữ cảnh, 4 Giới hạn, 3 Ngầm). Lỗi nghiêm trọng cần chặn trước pilot: **Ca 7** (báo đã hoàn khi API sổ cái 503) và **Ca 20** (hoàn trùng 2 lần thiếu idempotency key). | Chưa *(chờ hợp nhất bộ nhãn 1 & bảng 5 ca từ #4)* | Kỹ sư trưởng agent |
| 6 · Pilot plan | Phạm vi: chỉ `noi_dia + hang_nang`. Chia ngẫu nhiên theo nhân viên (**20 + 20 cụm**, đối chứng đồng thời). **Đánh đổi:** 20 cụm/nhóm có trần hiệu dụng 1.000 < 1.251 (không đủ mẫu cho MDE +5 điểm), chấp nhận **MDE +6 điểm** (n=859/nhóm, m≥299 yc/nhân viên, DE=6,96; nếu tác động thật chỉ +5 điểm thì power còn **0,642**). Rollout 10%→25%→50%, ≥ 3 luật dừng và rollback 30 phút. | Chưa *(chờ chốt YAML từ #5)* | Giám đốc vận hành LogiX-VN |
| 7 · Rủi ro kinh tế | 1) Làm lại ×2 → +51,8% (6.787 đ); 2) Xem lại 100% kéo dài → 0,98×–1,03× (không tiết kiệm); 3) Khối lượng giảm nửa → cố định tăng từ +1.185 đ lên +2.370 đ/việc (`simulated`). | Giả lập | PM trợ lý hoàn phí |

**Đề xuất:** **Go có điều kiện** cho kế hoạch pilot phạm vi `noi_dia` + `hang_nang` (giới hạn tối đa 2 lần chạy), kèm các điều kiện bắt buộc trước khi khởi chạy:

- **Điều kiện 1 (Chặn lỗi nghiêm trọng):** Sửa khóa chống trùng (`idempotency_key`) và đối soát sổ cái 503 (Ca 7, Ca 20) — Phụ trách: **Kỹ sư trưởng agent** · Ngày kiểm tra: **2026-12-02** (trước ngày bắt đầu pilot).
- **Điều kiện 2 (Chấp nhận đánh đổi thống kê):** Ký duyệt đánh đổi MDE từ +5 lên +6 điểm (biết rõ power chỉ còn 0,642 nếu tác động thật là +5 điểm) và chốt `pilot_plan.yaml` — Phụ trách: **Giám đốc vận hành LogiX-VN** · Ngày kiểm tra: **2026-12-02**.
- **Điều kiện 3 (Đo thật thay cho `simulated`):** Bật đủ ≥ 6 event có `trace_id`, đo trực tiếp `phut_xem_lai` và `phut_lam_lai` sau tuần 1 để thay toàn bộ số `simulated` — Phụ trách: **PM trợ lý hoàn phí** · Ngày kiểm tra: **2026-12-09** (cuối tuần 1).
- **Điều kiện 4 (Lộ trình giảm xem lại):** Áp dụng lộ trình giảm tỉ lệ xem lại theo bậc (không giữ 100% xem lại sau bước 0.25 vì chi phí đạt 0,98×–1,03×) — Phụ trách: **Trưởng nhóm CSKH** · Ngày kiểm tra: **2026-12-16** (cuối tuần 2).
