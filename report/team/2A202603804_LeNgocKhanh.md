# Báo cáo cá nhân — LeNgocKhanh-2A202603804

## 1. Thông tin thành viên

- Họ tên: Lê Ngọc Khánh
- MSSV: 2A202603804
- Email: (tự điền)
- GitHub: lekhanh2k5-dotcom
- Vai trong nhóm (nhóm 3 người kiêm nhiệm): Người gắn nhãn 1; kiêm người viết code và kiểm số cho nhiệm vụ D (pilot) và E1–E2 (chỉ số, rủi ro).

## 2. Phần việc phụ trách

- **Issue #4 [C]:** gắn nhãn độc lập bộ 1 cho 20 ca lỗi; tổng hợp `report/team/bang_loi.md` (đồng thuận, quy tắc ca lệch, bảng khắc phục 5 ca).
- **Issue #5 [D]:** tính cỡ mẫu D1 trong `src/lab13.py`, trả lời D2, hoàn thiện `report/team/pilot_plan.yaml`.
- **Issue #6 [E1–E2]:** tính thử ba chỉ số trong `src/lab13.py`, viết `report/team/chi_so.md` (chỉ số đề xuất, event có `trace_id`, rủi ro kinh tế).

## 3. Đóng góp cụ thể

- **D1:** hàm `nhiem_vu_d1()` tính đủ năm câu bằng z chính xác: a) 1.251 mỗi nhóm; b) DE 2,48, 3.103 yêu cầu = 42 người mỗi nhóm, tổng 84 > 40; c) trần c/ICC = 1.000 < 1.251; d) trần 300, chỉ 6 cụm; e) mức chênh 6 điểm cần 859 mỗi nhóm và m ≥ 299 (DE 6,96). Tính thêm power 0,64 khi tác động thật chỉ 5 điểm và lịch pilot từ dữ liệu (khoảng 10 ngày làm việc ở bước 0,50, quyết định 2027-01-12).
- **pilot_plan.yaml:** chia theo nhân viên 20 + 20, phân tầng theo depot; scope theo hệ số A3 và tối đa 2 lần chạy theo B3; 4 luật dừng NẾU–TRONG–THÌ–KHÔNG THÌ (an toàn, chi phí, mức dùng, lỗi ngầm), ngưỡng đặt theo số hiện tại (mở lại 3,97%, chi phí 4.599 đ ở A4).
- **E1:** hàm `nhiem_vu_e1()` tính 82,83% (994/1.200), 27,12% (48/177), 4,25% (51/1.200), kèm số trong phạm vi pilot.
- **chi_so.md:** 2 chỉ số đề xuất, 10 event có `trace_id`, phần kiểm tra chéo chỉ số với event, 3 dòng rủi ro kinh tế lấy số từ A4 và B1/B4 (simulated).
- **Tích hợp:** giải xung đột `src/lab13.py` giữa phần B của Nam và phần D1, để file chạy liền A1 → B → D1 → E1.
- **Phát hiện và sửa:** ngưỡng luật dừng chi phí ban đầu 10.000 đ nằm trên mọi kịch bản B1 (tối đa 6.787 đ) nên không bao giờ kích hoạt; hạ xuống 6.000 đ có lý do bằng số.
- **C:** gắn 20 nhãn bộ 1 trong 8 phút, khoá bằng commit trước khi xem bộ 2; viết bảng khắc phục 5 ca, mỗi ca có cách phát hiện đo được và một vai trò phụ trách.

## 4. Bằng chứng

- PR #10 (D), PR #12 (E1–E2) trên repo nhóm.
- Commit: `ddc23d5` (D1 + pilot_plan), `b0233a5` và `f8395c5` (scope theo A3, B3), `b17cc57` (ngưỡng chi phí 6.000 đ), `f04a3e2` (E1 + chi_so), `4e889a4` và `621101b` (E2), `64f445a` (bộ nhãn 1 khoá lúc 15:02:06), `e83c83c` (bảng khắc phục).
- Kiểm tra đã chạy: `python lab13.py` in ba phép thử ĐẠT và chạy hết; `python -m unittest test_lab13 test_sensitivity` 22 test OK; `yaml.safe_load` đọc được `pilot_plan.yaml`; không còn dấu `?` ngoài chú thích; `grep -rni production report/team` không in gì.

## 5. Công cụ AI đã dùng

- **Claude Code (Claude Opus):** gợi ý code cho `nhiem_vu_d1`, `nhiem_vu_e1`, soạn nháp `pilot_plan.yaml`, `chi_so.md` và bảng khắc phục, giải xung đột merge.
- **Không dùng AI để gắn nhãn C:** 20 nhãn bộ 1 do tôi tự gắn, độc lập.
- **Cách tự kiểm tra:** mọi số do code của nhóm tính từ CSV; đối chiếu năm câu D1 và ba chỉ số E1 với số tham chiếu (lệch dưới 2%); tính tay câu e (20m ≥ 859 × (0,98 + 0,02m) → m ≥ 299); đối chiếu A4 tính độc lập (33.750 việc/tháng, 1.185 đ) với kết quả của Hiếu; rà checklist của RUBRIC C4, C5 trước khi gửi PR.
- **AI sai ở đâu:** bản nháp đặt ngưỡng chi phí 10.000 đ và giới hạn chạy lại trong hành động luật dừng chưa khớp với B3; tôi phát hiện khi đối chiếu với bảng độ nhạy và hồ sơ launch, rồi sửa.

## 6. Tự đánh giá

- Làm tốt: số D1 và E1 đúng đáp án, có lý do cho mọi ngưỡng, giữ D, E và hồ sơ launch nhất quán.
- Cần cải thiện: phần C phụ thuộc bộ nhãn 2, nên chốt sớm cách trao đổi bộ nhãn giữa hai người gắn nhãn ngay từ đầu buổi.
