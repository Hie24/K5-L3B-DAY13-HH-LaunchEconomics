# Báo cáo nhóm

Báo cáo ngắn, tối đa 2 trang. Số liệu chi tiết nằm trong các file hồ sơ; ở đây chỉ dẫn lại con số chính.

## 1. Thông tin nhóm

- Tên nhóm: HH
- Lớp: L3B
- Thành viên: 3 thành viên (`@Hie24`, `@DoLyHoangNam`, `@lekhanh2k5-dotcom`) — chi tiết vai trò và đóng góp xem [TEAM.md](../../TEAM.md).

## 2. Mục tiêu và cách tiếp cận

Nhóm xây dựng bộ **Hồ sơ launch v0** cho trợ lý hoàn phí **LogiX-VN** nhằm phục vụ thẩm định kế hoạch pilot tại cổng **Gate 2a** trên bộ dữ liệu giả lập gồm 1.200 yêu cầu và 1.624 lần chạy. Bốn câu hỏi trọng tâm: (1) chi phí thật mỗi việc thành công và độ nhạy so với nhân viên tự làm (12.000 đ/yêu cầu), (2) phân loại 20 ca lỗi theo Google PAIR và biện pháp phát hiện/khắc phục, (3) thiết kế pilot có đối chứng đủ cỡ mẫu và luật dừng rõ ràng, và (4) hệ thống chỉ số, event có `trace_id`, rủi ro kinh tế.

## 3. Giải pháp

- **Nhiệm vụ A (Mô hình chi phí):** Xây dựng 3 hàm A1 đạt 3 phép thử nền tảng (`1,20 · 1,25 · 1,25`), mô hình `mo_hinh()` cộng chi phí mọi lần chạy kể cả lần lỗi trên mẫu số `ket_qua == 'thanh_cong'`, tách theo 4 loại yêu cầu và phân bổ chi phí cố định 40 triệu đ/tháng → [src/lab13.py](../../src/lab13.py), [bang_chi_phi.md](bang_chi_phi.md).
- **Nhiệm vụ B (Độ nhạy & Giới hạn):** Chạy 9 kịch bản độ nhạy, kiểm tra tính tuyến tính khi đổi 1 cặp, tính chi phí cả hệ thống (cộng 12.000 đ/ca không thành công) cho giới hạn 1–3 lần chạy và đánh giá kịch bản xem lại 100% trên `noi_dia + hang_nang` → [src/lab13.py](../../src/lab13.py), [bang_chi_phi.md](bang_chi_phi.md).
- **Nhiệm vụ C (Bảng lỗi, chờ #4):** Cần hợp nhất hai bộ nhãn độc lập 20 ca theo nguyên nhân gốc, tính đồng thuận và hoàn thiện bảng khắc phục 5 loại → [bang_loi.md](bang_loi.md).
- **Nhiệm vụ D (Kế hoạch pilot, chờ #5):** Phương án dùng công thức hai tỉ lệ và hệ số thiết kế cụm (`ICC = 0,02`); cần chốt năm kiểm tra tách tác động, mã D1 và YAML có luật dừng 4 vế → [pilot_plan.yaml](pilot_plan.yaml).
- **Nhiệm vụ E:** Hồ sơ v0 đã tổng hợp số A/B; đặc tả ba chỉ số, event và rủi ro đang chờ #6 chốt → [chi_so.md](chi_so.md), [ho_so_launch_v0.md](ho_so_launch_v0.md).

## 4. Kết quả

- **Kinh tế (A, B — `simulated`):** Chi phí mỗi việc thành công toàn mẫu là **4.472 đ** (gấp 16,3× hoá đơn 275 đ/yc); chi phí cả hệ thống là **5.865 đ/yc (0,49×)**, tối ưu ở giới hạn **2 lần chạy** với **6.901.220 đ** (5.751 đ/yc). Ba yếu tố nhạy nhất: số ca làm lại (+51,8%), tỉ lệ xem lại (+40,7%), lương nhân viên (+23,1%). Loại `quoc_te` (1,88×) và `doi_tac` (0,85×) bị loại khỏi phạm vi pilot; với `noi_dia + hang_nang`, chi phí gồm cố định là **4.599 đ** ở 45.000 yc/tháng (**5.784 đ** ở nửa khối lượng). Tuy nhiên, nếu xem lại 100%, chi phí tăng lên **11.743 đ (0,98×)** (9 phút làm lại) hoặc **12.415 đ (1,03×)** (15,3 phút/ca như dữ liệu).
- **Chỉ số đợt chạy thử (E1, chưa đối chứng):** Đóng trong 24h & không mở lại 7 ngày **82,83%** (994/1.200); tỉ lệ bỏ qua gợi ý **27,12%** (48/177); tỉ lệ mở lại 7 ngày **4,25%** (51/1.200; phạm vi pilot 3,97%).
- **Thiết kế pilot (D, đề xuất chờ chốt YAML):** Chia ngẫu nhiên 20 + 20 nhân viên, đề nghị đánh đổi MDE +6 điểm (`n = 859`/nhóm, `m ≥ 299` yc/nhân viên, `DE = 6,96`; power còn **0,642** nếu tác động thật là +5 điểm); chưa coi là đã được ký duyệt.
- **Đề xuất trong [ho_so_launch_v0.md](ho_so_launch_v0.md):** **Go có điều kiện** cho pilot phạm vi `noi_dia + hang_nang` (tối đa 2 lần chạy), kèm 4 điều kiện cụ thể có vai trò và ngày kiểm tra.
- **Kết quả duyệt chéo Gate 2a:** *Chờ cập nhật sau phiên duyệt chéo tại lớp (chỉ ghi khi có phiếu chấm thực tế từ nhóm hội đồng).*

## 5. Khó khăn và cách xử lý

- **Nhóm 3 người làm đề 4 vai:** Nhóm phân công 9 issue cân bằng (mỗi người 3 issue, 140 phút ước lượng), giữ đúng nguyên tắc 2 người gắn nhãn độc lập ở Nhiệm vụ C và làm trên nhánh riêng để tránh xung đột file chung `src/lab13.py`.
- **Giới hạn cụm của LogiX-VN (40 nhân viên, 12 depot):** Không cách chia cụm nào đủ cỡ mẫu cho MDE +5 điểm (`c/ICC = 1.000 < 1.251`), nên nhóm minh bạch đánh đổi MDE +6 điểm và công khai power 0,642 trong hồ sơ.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp và bằng chứng của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

- **Phụ thuộc dữ liệu giả lập:** Các cột thời gian xem lại và làm lại đang là `simulated` (chiếm 92,5% tổng chi phí); cần thu thập số đo thật từ event `staff_review_decision` và `staff_rework_completed` ngay tuần 1 của pilot.
- **Đợt chạy thử thiếu nhóm đối chứng:** Con số 82,83% chưa đủ kết luận nhân quả; cần triển khai pilot phân nhóm ngẫu nhiên 20 + 20 nhân viên có kiểm soát spillover theo tài khoản.
- **Rủi ro chi phí nếu xem lại 100%:** Cần xây dựng cơ chế giảm tỉ lệ xem lại theo bậc dựa trên độ tin cậy và kết quả kiểm tra mẫu hằng tuần.
- **Chi phí cố định khi xem lại 100%:** Các số B4 11.743–12.415 đ/việc chưa gồm cố định. Cộng phân bổ A4 ở 45.000 yêu cầu tổng/tháng thành **12.928–13.600 đ/việc** (`simulated`); cần ngân sách tuần pilot và kiểm soát chi phí.
- **Hồ sơ còn chờ tích hợp:** #4–#6, thông tin thật trong TEAM.md, báo cáo cá nhân còn thiếu và phiếu duyệt chéo phải được hoàn thiện trước khi nộp toàn bộ lab. Không suy ra các phần này đã xong từ việc A/B chạy đạt.

## 8. Tài liệu tham khảo

- Erol và cộng sự, *Cost-of-Pass: An Economic Framework for Evaluating Language Models*, https://arxiv.org/abs/2504.13359
- Google PAIR, *People + AI Guidebook*, chương "Errors + Graceful Failure", https://pair.withgoogle.com
- Tài liệu `statsmodels` (`NormalIndPower`, `proportion_effectsize`) và tài liệu đề bài Lab 13 trong thư mục `docs/`.
