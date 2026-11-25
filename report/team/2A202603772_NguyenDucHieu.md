# Báo cáo cá nhân — Nguyễn Đức Hiếu — 2A202603772

## 1. Thông tin thành viên

- Họ tên: Nguyễn Đức Hiếu
- MSSV: 2A202603772
- Email: 11236106@st.neu.edu.vn
- Nhóm HH · Lớp L3B · GitHub: Hie24
- Vai trò: Nhóm trưởng, người viết code và kiểm số A1–A4, phụ trách tích hợp và kiểm tra cuối.

## 2. Phần việc phụ trách

- Issue #1, #2: mô hình chi phí từ trace, phân tích theo loại yêu cầu và chi phí cố định.
- Issue #9: chia việc qua GitHub, review PR, xử lý xung đột và rà hồ sơ trước khi nộp.

## 3. Đóng góp cụ thể

- Hoàn thiện A1–A4 trong `src/lab13.py` và phần A của `bang_chi_phi.md`; giữ nguyên dữ liệu gốc và giao diện `mo_hinh()` để nhóm dùng cho B.
- Tính chi phí trên mọi lần chạy, kể cả lỗi: 978 việc thành công, 4.471,97 đ/việc; trong phạm vi pilot, cộng cố định thành 4.599,09 đ/việc ở 45.000 yêu cầu/tháng (đều simulated).
- Tích hợp A/B, bổ sung kiểm tra, xử lý conflict PR #13; rà phần C và đồng bộ thiết kế chống hoàn trùng giữa bảng lỗi, event và luật dừng.

## 4. Bằng chứng

- [PR #11](https://github.com/Hie24/K5-L3B-DAY13-HH-LaunchEconomics/pull/11), commit `9634fa8`: code A1–A4, bảng chi phí và 14 test.
- [PR #13](https://github.com/Hie24/K5-L3B-DAY13-HH-LaunchEconomics/pull/13), commit `17b8e72`: tích hợp A/B; tổng 22/22 test đạt.
- [PR #17](https://github.com/Hie24/K5-L3B-DAY13-HH-LaunchEconomics/pull/17): sửa thiết kế khóa nghiệp vụ `refund_case_id`, phân biệt hoàn trùng thực tế với lượt gửi lại bị chặn, đồng bộ C/D/E.
- Kiểm tra `python lab13.py` chạy đủ A/B/D/E, ba phép thử A1 đạt 1,20 · 1,25 · 1,25; YAML đọc được và có 5 luật dừng.

## 5. Công cụ AI đã dùng

Sử dụng ChatGPT/Codex để hỗ trợ đọc đề, triển khai code, viết test và rà tài liệu. Kiểm chứng bằng chạy code trên CSV gốc, đối chiếu số trong hướng dẫn, kiểm tra fixture tính tay, `git diff --check` và xác nhận dữ liệu không bị sửa.

## 6. Tự đánh giá

Hoàn thành phần A1–A4 và tích hợp mã nhóm; hiểu việc phân biệt chi phí mỗi việc thành công với chi phí cả hệ thống, cũng như tác động của giờ nhân viên và khối lượng lên chi phí. Phần điều phối còn cần hoàn tất phiếu duyệt chéo có bằng chứng thực tế, xác nhận chạy trên máy thành viên khác và nộp LMS.
