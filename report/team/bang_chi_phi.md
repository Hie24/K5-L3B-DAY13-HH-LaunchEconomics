# Bảng chi phí · Nhiệm vụ A và B

Số tính bằng `src/lab13.py`. Mọi con số tính từ cột `_simulated` ghi nhãn `simulated`. Mỗi câu trả lời không quá ba dòng, có ít nhất một con số.

## A1 · Ba phép thử đáp án biết trước

| Phép thử (p = 0,8) | Kết quả của nhóm |
| --- | --- |
| Số lần chạy trung bình, tối đa 2 lần | ... |
| Số lần chạy trung bình, chạy đến khi đúng | ... |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | ... |

## A2 · Mô hình chi phí từ trace

| Khoản | Số tiền (đ) | Nguồn | Nhãn |
| --- | ---: | --- | --- |
| Token | ... | `logix_runs.csv` | đo từ trace |
| Tool | ... | `logix_runs.csv` | đo từ trace |
| Trong đó, phần của lần chạy thứ 2 và 3 | ... | attempt lớn hơn 1 | đo từ trace |
| Xem lại | ... | `phut_xem_lai_simulated` | simulated |
| Làm lại | ... | `phut_lam_lai_simulated` | simulated |
| Tổng chi phí | ... | | |
| Số việc thành công | ... | `ket_qua` | |
| Chi phí mỗi việc thành công | ... | | |
| Hoá đơn token và tool chia cho số yêu cầu | ... | | |

- Chi phí mỗi việc thành công gấp bao nhiêu lần "hoá đơn chia số yêu cầu"? ...
- Khoản nào chiếm tỉ trọng lớn nhất trong tổng chi phí, bao nhiêu phần trăm? ...

## A3 · Tách theo loại yêu cầu

| Loại | Số yêu cầu | Tỉ lệ thành công | Số lần chạy mỗi yêu cầu | Chi phí mỗi việc thành công | So với 12.000 đ |
| --- | ---: | ---: | ---: | ---: | ---: |
| noi_dia | ... | ... | ... | ... | ... |
| hang_nang | ... | ... | ... | ... | ... |
| quoc_te | ... | ... | ... | ... | ... |
| doi_tac | ... | ... | ... | ... | ... |

- Loại nào không đáng để trợ lý xử lý? Với loại đó, cho chạy lại tới 3 lần có giúp không? ...

## A4 · Chi phí cố định (phạm vi noi_dia + hang_nang)

| Khối lượng | Việc thành công mỗi tháng | Chi phí cố định mỗi việc | Chi phí mỗi việc thành công + cố định | So với 12.000 đ |
| --- | ---: | ---: | ---: | ---: |
| 45.000 yêu cầu/tháng | ... | ... | ... | ... |
| Một nửa khối lượng | ... | ... | ... | ... |

- Chi phí cố định có đổi kết luận không? Ở khối lượng nào? ...

## B1 · Đổi từng yếu tố

Gốc (A2): **4.472 đ** (`simulated`). Quy tắc đối xứng đạt chuẩn: mỗi kịch bản giảm một nửa làm chi phí giảm đúng bằng một nửa mức tăng của kịch bản gấp đôi tương ứng (+5,6% vs −2,8%; +40,7% vs −20,3%; +51,8% vs −25,9%).

| Kịch bản | Cách tính | Chi phí mỗi việc thành công (`simulated`) | Thay đổi (%) |
| --- | --- | ---: | ---: |
| Giá token gấp đôi | 52 đ và 260 đ cho 1.000 token; giá tool giữ nguyên | 4.723 đ | +5,6% |
| Giá token giảm một nửa | 13 đ và 65 đ | 4.346 đ | −2,8% |
| Tỉ lệ xem lại gấp đôi | Tiền xem lại × 2 | 6.292 đ | +40,7% |
| Tỉ lệ xem lại giảm một nửa | Tiền xem lại ÷ 2 | 3.562 đ | −20,3% |
| Số ca làm lại gấp đôi | Tiền làm lại × 2 | 6.787 đ | +51,8% |
| Số ca làm lại giảm một nửa | Tiền làm lại ÷ 2 | 3.315 đ | −25,9% |
| Lương nhân viên tăng 25% | 2.500 đ mỗi phút | 5.506 đ | +23,1% |
| Chỉ cho chạy tối đa 2 lần | Bỏ lần chạy có attempt > 2; yêu cầu có so_lan_chay > 2 coi là chuyen_nhan_vien | 4.237 đ | −5,2% |
| Chỉ cho chạy 1 lần | Như trên với giới hạn 1 | 4.111 đ | −8,1% |

## B2 · Đổi một cặp và xếp hạng

- Giá token gấp đôi cùng lúc tỉ lệ xem lại gấp đôi: **6.543 đ (+46,3%)** (`simulated`), đúng bằng tổng hai tác động riêng (+5,6% + +40,7% = +46,3%) vì mô hình là tổng tuyến tính của các khoản chi phí trên cùng mẫu số 978 việc thành công.
- Xếp hạng ba yếu tố ảnh hưởng mạnh nhất: **1. Số ca làm lại (+51,8% khi gấp đôi)** · **2. Tỉ lệ xem lại (+40,7% khi gấp đôi)** · **3. Lương nhân viên (+23,1% khi tăng 25%)** (đều `simulated`).

## B3 · Giới hạn chạy lại có thật sự rẻ hơn

Chi phí cả hệ thống (1.200 yêu cầu) = Tổng chi phí trợ lý + 12.000 đ × Số yêu cầu không thành công (`simulated`).

| Giới hạn | Tổng chi phí trợ lý (`simulated`) | Số yêu cầu không thành công | Chi phí cả hệ thống (`simulated`) | Chi phí mỗi việc thành công (`simulated`) |
| --- | ---: | ---: | ---: | ---: |
| 1 lần | 3.621.781 đ | 319 | 7.449.781 đ | 4.111 đ |
| 2 lần | 4.093.220 đ | 234 | **6.901.220 đ** | 4.237 đ |
| 3 lần | 4.373.585 đ | 222 | 7.037.585 đ | 4.472 đ |

- Giới hạn **2 lần chạy** rẻ nhất cho công ty (**6.901.220 đ**, tương đương 5.751 đ/yêu cầu, `simulated`), **không trùng** với giới hạn cho chi phí mỗi việc thành công thấp nhất (1 lần: 4.111 đ). Tối ưu riêng chi phí mỗi việc thành công ở mức 1 lần sẽ đẩy thêm **85 yêu cầu** (319 vs 234) sang nhân viên, làm tổng chi phí cả hệ thống tăng thêm **548.561 đ**.

## B4 · Nếu phải xem lại tất cả

- Phạm vi `noi_dia` + `hang_nang` (982 yêu cầu, mẫu số **900** việc thành công, 948 yêu cầu chạy `ok`, 48 ca `lam_lai`, token + tool = 224.513 đ; không cộng trùng hai khoản): với 5 phút xem lại và 9 phút làm lại, tổng 10.568.513 đ → **11.743 đ = 0,98×** của 12.000 đ (`simulated`). Nếu dùng mức làm lại trung bình dữ liệu 15,3 phút/ca, chi phí lên **12.415 đ = 1,03×** (`simulated`, đắt hơn nhân viên tự làm; ngưỡng hoà vốn xem lại là ≤ 5,1 phút hoặc ≤ 4,8 phút).
- Xem lại 100% khiến tiền xem lại chiếm ~90% chi phí nên gần như không tiết kiệm được gì. Pilot bắt buộc phải học được mức giảm tỉ lệ xem lại an toàn (theo bậc) và liệu thời gian xem lại có thể rút ngắn dưới 4,8–5,1 phút/ca hay không.
