# Team

## Thông tin nhóm

- Tên nhóm: HH
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY13-HH-LaunchEconomics` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/Hie24/K5-L3B-DAY13-HH-LaunchEconomics · nhánh `main` · commit chốt: (ghi lúc nộp)
- Nhóm có 3 thành viên nên kiêm nhiệm bốn vai (phân công theo issue #1–#9).

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Đức Hiếu | 2A202603772 | 11236106@st.neu.edu.vn | Hie24 | Nhóm trưởng; người viết code A1–A4 (#1, #2); tích hợp, duyệt chéo Gate 2a, nộp bài (#9) |
|   2 | Đỗ Lý Hoàng Nam | 2A202603777 | dolyhoangnam13072005@gmail.com | DoLyHoangNam | Người gắn nhãn 2 kiêm giữ hồ sơ; độ nhạy B1–B4 (#3), hồ sơ launch và báo cáo nhóm (#7), review D (#8) |
|   3 | Lê Ngọc Khánh | 2A202603804 | lekhanh2k5@gmail.com | lekhanh2k5-dotcom | Người gắn nhãn 1; viết code và kiểm số D (#5), E1–E2 (#6); tổng hợp bảng lỗi C (#4) |

Bốn vai của lab:

- **Người viết code:** viết và chạy `src/lab13.py`.
- **Người kiểm số:** tính tay một con số để đối chiếu, điền bảng.
- **Người gắn nhãn 1:** đọc đề, theo dõi điều kiện "Xong khi"; gắn nhãn 20 ca độc lập ở CP3.
- **Người gắn nhãn 2, kiêm giữ hồ sơ:** điền `report/team/ho_so_launch_v0.md` từ đầu buổi; gắn nhãn 20 ca độc lập ở CP3.

Đổi người viết code sau giờ giải lao, để ít nhất hai người trong nhóm tự tay tính được chi phí.

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

## NguyenDucHieu-2A202603772

### Phần việc phụ trách

- #1, #2: mô hình chi phí A1–A4, phân tích theo loại yêu cầu, chi phí cố định và bảng chi phí phần A.
- #9: phân công issue, review PR, tích hợp mã và kiểm tra hồ sơ trước khi nộp.

### Đóng góp cụ thể

- Viết ba hàm A1 và `mo_hinh()` có tham số giá, hệ số lao động và giới hạn lần chạy; bổ sung bảng A3–A4 và phép tính tay đối chiếu.
- Kết quả: 978 việc thành công; 4.471,97 đ/việc toàn mẫu; phạm vi pilot cộng cố định 4.599,09 đ/việc ở 45.000 yêu cầu/tháng (simulated).
- Xử lý conflict A/B, bổ sung test tích hợp (22/22 đạt), đồng bộ thiết kế chống hoàn trùng trong C/D/E và rà thiếu sót hồ sơ.
- Điều phối còn chờ: phiếu duyệt chéo thực tế, xác nhận chạy trên máy thành viên khác và nộp LMS.

### Bằng chứng

- PR #11 (`9634fa8`), PR #13 (`17b8e72`), PR #17 (`db47e2d`, `eb579f6`).
- Báo cáo cá nhân: [2A202603772_NguyenDucHieu.md](report/team/2A202603772_NguyenDucHieu.md).

## LeNgocKhanh-2A202603804

### Phần việc phụ trách

- #4 [C] gắn nhãn độc lập bộ 1 và tổng hợp `report/team/bang_loi.md`.
- #5 [D] cỡ mẫu D1 trong `src/lab13.py` và `report/team/pilot_plan.yaml`.
- #6 [E1–E2] ba chỉ số trong `src/lab13.py` và `report/team/chi_so.md`.

### Đóng góp cụ thể

- D1 năm câu (1.251 · DE 2,48, 84 > 40 · trần 1.000 · trần 300 · m ≥ 299, DE 6,96), power 0,64; pilot 20 + 20 nhân viên, 5 luật dừng sau cập nhật PR #17, quyết định 2027-01-12.
- E1: 82,83% · 27,12% · 4,25%; 2 chỉ số đề xuất, 10 event có `trace_id`, 3 dòng rủi ro kinh tế.
- C: lưu bộ nhãn 1 tại commit `64f445a`; tổng hợp bảng 20 ca và bảng khắc phục 5 loại. Hai cột nhãn trùng 20/20; hồ sơ bộ 2 được bổ sung trong PR #19.
- Giải xung đột `src/lab13.py` (B và D1), hạ ngưỡng luật dừng chi phí từ 10.000 đ xuống 6.000 đ có lý do bằng số.

### Bằng chứng

- PR #10, #12, #15; commit `64f445a` (bộ nhãn 1 lúc 15:02:06), `ddc23d5` (D1), `f04a3e2` (E1).
- Báo cáo cá nhân: `report/team/2A202603804_LeNgocKhanh.md`.

## DoLyHoangNam-2A202603777

### Phần việc phụ trách

- #3 [B1–B4] Phân tích độ nhạy 9 kịch bản, giới hạn chạy lại và kịch bản xem lại 100% (`src/lab13.py`, `report/team/bang_chi_phi.md`).
- #7 [E3] Tổng hợp hồ sơ launch v0 một trang (`report/team/ho_so_launch_v0.md`) và báo cáo nhóm (`report/team/group_report.md`).
- #8 [C + review D] Gắn nhãn độc lập bộ 2 (20 ca lỗi) và kiểm tra chéo cỡ mẫu D1/D2 cho `pilot_plan.yaml`.

### Đóng góp cụ thể

- Viết `chay_nhiem_vu_b()` và điền mục B1–B4 trong `bang_chi_phi.md`: đối xứng x2/÷2, top 3 yếu tố nhạy nhất (làm lại +51,8%, xem lại +40,7%, lương +23,1%), giới hạn 2 lần chạy rẻ nhất toàn hệ thống (6.901.220 đ), và cảnh báo xem lại 100% (11.743–12.415 đ chưa cố định; 12.928–13.600 đ có cố định, `simulated`).
- Hoàn thiện hồ sơ `ho_so_launch_v0.md` (7 mục, đề xuất **Go có điều kiện** kèm 4 điều kiện có vai trò và mốc ngày khớp `pilot_plan.yaml`) và `group_report.md` (8 mục).
- Lưu bản gốc bộ nhãn độc lập 2 tại `report/team/nhan_doc_lap_bo2_DoLyHoangNam.md` (20/20 đồng thuận với bộ 1, khớp tham khảo 20/20) và kiểm tra chéo đạt toàn bộ D1/D2 của `pilot_plan.yaml`.

### Bằng chứng

- PR #13 (nhánh `DoLyHoangNam_2A202603777`), PR #14, cùng bản gốc `report/team/nhan_doc_lap_bo2_DoLyHoangNam.md`.
- Báo cáo cá nhân: `report/team/2A202603777_DoLyHoangNam.md`.
