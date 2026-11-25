# Báo cáo cá nhân — DoLyHoangNam-2A202603777

## 1. Thông tin thành viên

- Họ tên: Đỗ Lý Hoàng Nam
- MSSV: 2A202603777
- Email: dolyhoangnam13072005@gmail.com
- Vai trong nhóm (nhóm 3 người kiêm nhiệm): Người gắn nhãn 2 kiêm giữ hồ sơ, phụ trách phân tích độ nhạy (B1–B4) và kiểm tra chéo cỡ mẫu pilot (review D).

## 2. Phần việc phụ trách

- **Issue `#3` ([B1–B4]):** Phân tích độ nhạy 9 kịch bản, kiểm tra đổi một cặp và xếp hạng top 3 yếu tố ảnh hưởng mạnh nhất, tính chi phí cả hệ thống cho giới hạn 1–3 lần chạy, và đánh giá kịch bản xem lại 100% trong phạm vi `noi_dia + hang_nang`.
- **Issue `#8` ([C + review D]):** Gắn nhãn độc lập bộ 2 cho 20 ca lỗi theo 5 loại Google PAIR từ đề bài gốc; kiểm tra chéo phép tính cỡ mẫu D1 và rà soát 5 tiêu chí tách tác động D2 cho kế hoạch pilot (`#5`).
- **Issue `#7` ([E3]):** Tổng hợp hồ sơ launch v0 một trang (`ho_so_launch_v0.md`) và viết báo cáo nhóm ngắn (`group_report.md`), rà soát tính nhất quán số liệu, nhãn `simulated` và quy tắc Gate 2a.

## 3. Đóng góp cụ thể

- Viết hàm `chay_nhiem_vu_b(runs, reqs)` trong `src/lab13.py` (giữ nguyên phần A của `@Hie24` để tránh xung đột khi tích hợp).
- Hoàn thiện mục B1–B4 trong `report/team/bang_chi_phi.md` với đầy đủ số liệu `simulated`, đối xứng x2/÷2, phân tích giới hạn 2 lần chạy rẻ nhất toàn hệ thống (6.901.220 đ) và cảnh báo xem lại 100% (11.743 đ = 0,98× với 9 phút làm lại; 12.415 đ = 1,03× với 15,3 phút làm lại).
- Chốt bộ nhãn độc lập bộ 2 cho 20 ca lỗi (4 Do người dùng, 5 Hệ thống, 4 Ngữ cảnh, 4 Giới hạn hệ thống, 3 Ngầm) trước khi đối chiếu với bộ nhãn 1 của `@lekhanh2k5-dotcom`.
- Kiểm tra chéo 5 câu cỡ mẫu D1 (`1.251`, `DE = 2,48`, trần `1.000`, trần `300`, `m ≥ 299` cho MDE +6 điểm và `power = 0,642` nếu tác động thật chỉ +5 điểm) cùng tỉ lệ mở lại 7 ngày hiện tại (4,25% toàn mẫu; 3,97% trong phạm vi pilot).
- Soạn hoàn chỉnh `report/team/ho_so_launch_v0.md` (7 mục, đề xuất **Go có điều kiện** kèm 4 điều kiện có vai trò và ngày kiểm tra) và `report/team/group_report.md` (8 mục, ≤ 2 trang).

## 4. Bằng chứng

- Nhánh làm việc: `DoLyHoangNam_2A202603777` (liên kết các issue `#3`, `#7`, `#8`; sẽ đồng bộ `main` sau khi PR nền tảng `#1`–`#2` được merge).
- Các file đóng góp:
  - `src/lab13.py` (hàm `chay_nhiem_vu_b`)
  - `report/team/bang_chi_phi.md` (mục B1–B4)
  - `report/team/ho_so_launch_v0.md` (7 mục và đề xuất Gate 2a)
  - `report/team/group_report.md` (8 mục báo cáo nhóm)
- Output kiểm chứng đã chạy thực tế trên Python 3.10 (`.venv`) từ `logix_runs.csv` và `logix_requests.csv`.

## 5. Công cụ AI đã dùng

- **Công cụ:** Antigravity (trợ lý AI) hỗ trợ đọc cấu trúc repo, gợi ý cấu trúc code cho phần B1–B4, kiểm tra công thức cỡ mẫu `statsmodels` và rà soát tính nhất quán giữa các file báo cáo.
- **Cách tự kiểm tra:**
  - Chạy trực tiếp code Python trên hai file CSV gốc để lấy toàn bộ số liệu B1–B4, D1 và E1; kiểm tra quy tắc đối xứng (kịch bản giảm một nửa bằng đúng nửa mức tăng của kịch bản gấp đôi).
  - Kiểm chứng tay bất phương trình cỡ mẫu cụm câu D1e (`20m / (1 + 0,02(m-1)) ≥ 859 ⇒ m ≥ 299`).
  - Tự gắn nhãn 20 ca lỗi từ file đề bài `.docx` theo nguyên nhân gốc trước khi đối chiếu.
  - Quét toàn bộ thư mục `report/team/` để bảo đảm có đủ nhãn `simulated`, không ghi "cả đội" và không xuất hiện từ bị cấm theo quy tắc 5 của `README.md`.

## 6. Tự đánh giá

- Hoàn thành đúng phạm vi 3 issue được giao (`#3`, `#7`, `#8`), tôn trọng quy trình phối hợp nhánh riêng và giữ nguyên tính độc lập của lượt gắn nhãn bộ 2.
- Hiểu rõ bản chất chi phí mỗi việc thành công (tử số tính mọi lần chạy kể cả lỗi, mẫu số chỉ đếm `thanh_cong`), lý do giới hạn 2 lần chạy tối ưu tổng chi phí hệ thống hơn 1 lần chạy, và lý do phải minh bạch đánh đổi MDE +6 điểm (power 0,642 ở mức +5 điểm) trong hồ sơ Gate 2a.
- Điểm cần tiếp tục hoàn thiện cùng nhóm: đồng bộ lại số liệu chốt sau khi `#1`, `#2`, `#4`, `#5`, `#6` hợp nhất vào `main` và cập nhật kết quả duyệt chéo Gate 2a thực tế vào `group_report.md`.
