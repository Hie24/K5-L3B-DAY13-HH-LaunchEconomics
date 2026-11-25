# Bảng chi phí · Nhiệm vụ A và B

Số tính bằng `src/lab13.py`. Mọi con số tính từ cột `_simulated` ghi nhãn `simulated`. Mỗi câu trả lời không quá ba dòng, có ít nhất một con số.

## A1 · Ba phép thử đáp án biết trước

| Phép thử (p = 0,8) | Kết quả của nhóm |
| --- | --- |
| Số lần chạy trung bình, tối đa 2 lần | 1,20 — ĐẠT |
| Số lần chạy trung bình, chạy đến khi đúng | 1,25 — ĐẠT |
| Hệ số chi phí mỗi việc thành công, tối đa 3 lần | 1,25 — ĐẠT |

Công thức: E[N] = (1 − (1 − p)^k) / p; P(thành công) = 1 − (1 − p)^k; hệ số chi phí = E[N] / P(thành công).
Khi chạy đến lúc đúng và p > 0: E[N] = 1/p, P(thành công) = 1; các lần thử được giả định độc lập.

## A2 · Mô hình chi phí từ trace

| Khoản | Giá trị (đ, trừ số việc) | Nguồn | Nhãn |
| --- | ---: | --- | --- |
| Token | 245.585,13 | `logix_runs.csv`: mọi lần chạy, kể cả lỗi | đo từ trace |
| Tool | 84.000,00 | 5.600 lượt × 15 đ | đo từ trace |
| Trong đó, phần của lần chạy thứ 2 và 3 | 93.804,49 | Token + tool của attempt > 1; đã nằm trong hai dòng trên | đo từ trace |
| Xem lại | 1.780.000,00 | 890 phút `phut_xem_lai_simulated` × 2.000 đ | simulated |
| Làm lại | 2.264.000,00 | 1.132 phút `phut_lam_lai_simulated` × 2.000 đ | simulated |
| Tổng chi phí | 4.373.585,13 | Token + tool + xem lại + làm lại; chưa cộng cố định | simulated |
| Số việc thành công | 978 | Số yêu cầu `ket_qua == 'thanh_cong'` | đếm từ dữ liệu giả lập |
| Chi phí mỗi việc thành công | 4.471,97 | Tổng chi phí / 978 | simulated |
| Hoá đơn token và tool chia cho số yêu cầu | 274,65 | (245.585,13 + 84.000,00) / 1.200 | đo từ trace |

- Chi phí mỗi việc thành công gấp **16,28 lần** hóa đơn mỗi yêu cầu (simulated); tử số tính cả 1.624 lần chạy, mẫu số chỉ 978 việc thành công.
- Khoản lớn nhất là **làm lại: 51,77%** tổng chi phí; xem lại chiếm 40,70%, cộng hai khoản lao động là 92,46% (simulated).

**So với nhân viên tự làm:** theo quy ước B3, cộng 12.000 đ cho mỗi yêu cầu không thành công, gồm 74 ca làm lại và 148 ca chuyển nhân viên.
Chi phí cả hệ thống = (4.373.585,13 + 222 × 12.000) / 1.200 = **5.864,65 đ/yêu cầu = 0,49× baseline** (simulated; chưa gồm cố định).
Con số 4.471,97 đ/việc thành công có mẫu số khác 12.000 đ/yêu cầu; không dùng riêng nó để kết luận tỷ lệ tiết kiệm.

**Tính tay đối chiếu:** run đầu `run_00001` tốn 4.759 × 26/1.000 + 492 × 130/1.000 + 5 × 15 = **262,694 đ** token + tool.
Khoản xem lại = 890 × 2.000 = **1.780.000 đ** (simulated); tổng 4.373.585,13 / 978 = **4.471,97 đ/việc** (simulated).

## A3 · Tách theo loại yêu cầu

| Loại | Số yêu cầu | Tỉ lệ thành công | Số lần chạy mỗi yêu cầu | Chi phí mỗi việc thành công (simulated) | Cps / 12.000 đ (simulated) |
| --- | ---: | ---: | ---: | ---: | ---: |
| noi_dia | 824 | 95,02% | 1,11 | 2.695,64 đ | 0,22× |
| hang_nang | 158 | 74,05% | 1,47 | 8.220,73 đ | 0,69× |
| quoc_te | 150 | 27,33% | 2,32 | 22.515,17 đ | 1,88× |
| doi_tac | 68 | 54,41% | 1,88 | 10.214,87 đ | 0,85× |

Tỷ lệ `status == 'ok'` trong các lần chạy thực sự quan sát tại từng attempt (khác tỷ lệ yêu cầu thành công cuối cùng):

| Loại | Attempt 1 | Attempt 2 | Attempt 3 |
| --- | ---: | ---: | ---: |
| noi_dia | 91,02% | 75,68% | 38,89% |
| hang_nang | 70,89% | 39,13% | 17,86% |
| quoc_te | 30,00% | 11,43% | 2,15% |
| doi_tac | 51,47% | 18,18% | 14,81% |

Để so trên cùng mẫu số yêu cầu, chi phí cả hệ thống từng loại đã cộng 12.000 đ cho mỗi yêu cầu không thành công (simulated; chưa gồm cố định):

| Loại | Chi phí cả hệ thống / yêu cầu (simulated) |
| --- | ---: |
| noi_dia | 3.158,60 đ |
| hang_nang | 9.201,43 đ |
| quoc_te | 14.874,15 đ |
| doi_tac | 11.028,68 đ |

- **Loại không đáng xử lý:** quoc_te tốn 22.515,17 đ/việc thành công và 14.874,15 đ/yêu cầu cả hệ thống (simulated), cao hơn baseline 12.000 đ; thành công chỉ 27,33% dù chạy 2,32 lần/yêu cầu.
- **Chạy lại tới 3 lần:** tỷ lệ ok quoc_te giảm từ 30,00% ở lần 1 còn 11,43% và 2,15% ở lần 2–3; việc chạy lại chưa khắc phục tốt nhóm lỗi này, không nên giả định các lần thử độc lập.
- **Phạm vi đề xuất:** chỉ noi_dia + hang_nang; doi_tac có 54,41% thành công và chi phí hệ thống 11.028,68 đ/yêu cầu (simulated), gần baseline và có điều khoản riêng nên chưa đưa vào pilot.

## A4 · Chi phí cố định (phạm vi noi_dia + hang_nang)

Khối lượng tháng là **tổng yêu cầu của mọi loại**; giữ cơ cấu mẫu: phạm vi có 982/1.200 yêu cầu và 900 việc thành công.
Do đó số việc thành công trong phạm vi mỗi tháng = khối lượng tổng × 900/1.200, không lấy 900/982.
Chi phí biến đổi trong phạm vi là **3.072.513,27 đ / 900 = 3.413,90 đ/việc thành công** (simulated).

| Khối lượng tổng | Việc thành công trong phạm vi mỗi tháng | Chi phí cố định mỗi việc | Chi phí mỗi việc thành công + cố định (simulated) | Cps có cố định / 12.000 đ (simulated) |
| --- | ---: | ---: | ---: | ---: |
| 45.000 yêu cầu/tháng | 33.750 | 1.185,19 đ | 4.599,09 đ | 0,38× |
| 22.500 yêu cầu/tháng | 16.875 | 2.370,37 đ | 5.784,27 đ | 0,48× |

Chi phí cố định giả định **40.000.000 đ/tháng**, phân bổ toàn bộ cho phạm vi pilot; chưa có bằng chứng về chi phí thật.

Để đánh giá kinh tế trên cùng mẫu số, cộng thêm chi phí nhân viên cho **82 yêu cầu chưa thành công trong 982 yêu cầu thuộc phạm vi**, rồi phân bổ cố định theo số yêu cầu trong phạm vi:

| Khối lượng tổng | Yêu cầu trong phạm vi / tháng | Chi phí hệ thống mỗi yêu cầu trong phạm vi, gồm nhân viên làm thay và cố định (simulated) |
| --- | ---: | ---: |
| 45.000 yêu cầu/tháng | 36.825 | 5.217,09 đ |
| 22.500 yêu cầu/tháng | 18.412,50 (kỳ vọng) | 6.303,31 đ |

Cách tính dòng đầu: (3.072.513,27 + 82 × 12.000) / 982 + 40.000.000 / 36.825 = **5.217,09 đ/yêu cầu** (simulated).
Các yêu cầu ngoài phạm vi chưa nằm trong hai dòng chi phí này; đây không phải chi phí bình quân toàn công ty.

- **Chi phí cố định có đổi kết luận không?** Ở 45.000 hoặc 22.500 yêu cầu tổng/tháng, chi phí hệ thống trong phạm vi lần lượt 5.217,09 và 6.303,31 đ/yêu cầu, còn dưới 12.000 đ (simulated); khối lượng giảm một nửa làm cố định mỗi việc tăng gấp đôi.

Nguồn công thức và số đối chiếu: [dữ liệu và công thức](../../docs/du_lieu_va_cong_thuc.md), [hướng dẫn chi tiết, mục A](../../docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md). Số trên được tính lại bằng `src/lab13.py`, giữ độ chính xác đầy đủ trong phép tính và làm tròn khi hiển thị.

Tái lập sau khi cài `src/requirements.txt` và kích hoạt môi trường Python:

```bash
cd src
python lab13.py
python -m unittest -v test_lab13.py
```

## B1 · Đổi từng yếu tố

| Kịch bản | Cách tính | Chi phí mỗi việc thành công | Thay đổi (%) |
| --- | --- | ---: | ---: |
| Giá token gấp đôi | 52 đ và 260 đ cho 1.000 token; giá tool giữ nguyên | ... | ... |
| Giá token giảm một nửa | 13 đ và 65 đ | ... | ... |
| Tỉ lệ xem lại gấp đôi | Tiền xem lại × 2 | ... | ... |
| Tỉ lệ xem lại giảm một nửa | Tiền xem lại ÷ 2 | ... | ... |
| Số ca làm lại gấp đôi | Tiền làm lại × 2 | ... | ... |
| Số ca làm lại giảm một nửa | Tiền làm lại ÷ 2 | ... | ... |
| Lương nhân viên tăng 25% | 2.500 đ mỗi phút | ... | ... |
| Chỉ cho chạy tối đa 2 lần | Bỏ lần chạy có attempt > 2; yêu cầu có so_lan_chay > 2 coi là chuyen_nhan_vien | ... | ... |
| Chỉ cho chạy 1 lần | Như trên với giới hạn 1 | ... | ... |

## B2 · Đổi một cặp và xếp hạng

- Giá token gấp đôi cùng lúc tỉ lệ xem lại gấp đôi: ...
- Xếp hạng ba yếu tố ảnh hưởng mạnh nhất: 1. ... · 2. ... · 3. ...

## B3 · Giới hạn chạy lại có thật sự rẻ hơn

| Giới hạn | Tổng chi phí trợ lý | Số yêu cầu không thành công | Chi phí cả hệ thống | Chi phí mỗi việc thành công |
| --- | ---: | ---: | ---: | ---: |
| 1 lần | ... | ... | ... | ... |
| 2 lần | ... | ... | ... | ... |
| 3 lần | ... | ... | ... | ... |

- Giới hạn nào rẻ nhất cho công ty? Có trùng với giới hạn cho chi phí mỗi việc thành công thấp nhất không? ...

## B4 · Nếu phải xem lại tất cả

- Chi phí mỗi việc thành công khi xem lại 100% (`noi_dia` + `hang_nang`), so với 12.000 đ: ...
- Kết quả này nói gì về thứ pilot cần học được? ...
