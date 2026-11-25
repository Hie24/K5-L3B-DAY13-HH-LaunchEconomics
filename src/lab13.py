"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Điền các chỗ ghi VIẾT Ở ĐÂY (đánh dấu TODO CP1…CP4). Dữ liệu trong hai file CSV là giả lập.
Bản gốc chưa sửa nằm ở lab13_starter.py.
"""
import math
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
# TODO CP1: viết ba hàm dưới đây cho tới khi kiem_tra_dap_an_biet_truoc() in ĐẠT.
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    raise NotImplementedError('VIẾT Ở ĐÂY')


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    raise NotImplementedError('VIẾT Ở ĐÂY')


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    raise NotImplementedError('VIẾT Ở ĐÂY')


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# TODO CP1: viết mo_hinh; CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    raise NotImplementedError('VIẾT Ở ĐÂY')


# ---------- Nhiệm vụ B · Bảng độ nhạy, giới hạn chạy lại và xem lại 100% ----------
def chay_nhiem_vu_b(runs, reqs):
    """Chạy B1–B4 dùng hàm mo_hinh (phụ thuộc PR nền tảng #1)."""
    goc = mo_hinh(runs, reqs)
    cps_goc = goc['cps']

    print('\n=== B1 · Bảng độ nhạy (9 kịch bản) [simulated] ===')
    kich_ban = [
        ('Giá token gấp đôi',          dict(gia_vao=52, gia_ra=260)),
        ('Giá token giảm một nửa',     dict(gia_vao=13, gia_ra=65)),
        ('Tỉ lệ xem lại gấp đôi',      dict(he_so_xem_lai=2.0)),
        ('Tỉ lệ xem lại giảm một nửa', dict(he_so_xem_lai=0.5)),
        ('Số ca làm lại gấp đôi',      dict(he_so_lam_lai=2.0)),
        ('Số ca làm lại giảm một nửa', dict(he_so_lam_lai=0.5)),
        ('Lương nhân viên tăng 25%',   dict(luong_phut=2500)),
        ('Chỉ cho chạy tối đa 2 lần',  dict(max_lan_chay=2)),
        ('Chỉ cho chạy 1 lần',         dict(max_lan_chay=1)),
    ]
    for ten, kw in kich_ban:
        cps = mo_hinh(runs, reqs, **kw)['cps']
        pct = (cps / cps_goc - 1) * 100
        print(f'{ten:28s} {cps:8,.0f} đ ({pct:+6.1f}%)')

    print('\n=== B2 · Đổi một cặp [simulated] ===')
    cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2.0)['cps']
    print(f'Token x2 + Xem lại x2: {cap:,.0f} đ ({(cap / cps_goc - 1) * 100:+.1f}%)')

    print('\n=== B3 · Chi phí cả hệ thống theo giới hạn chạy lại (1.200 yêu cầu) [simulated] ===')
    for k in (1, 2, 3):
        kq = mo_hinh(runs, reqs, max_lan_chay=k)
        khong_tc = len(reqs) - kq['thanh_cong']
        ca_he_thong = kq['tong'] + khong_tc * BASELINE
        print(f'k={k} | trợ lý={kq["tong"]:10,.0f} đ | không TC={khong_tc:3d} | '
              f'cả hệ thống={ca_he_thong:10,.0f} đ | cps={kq["cps"]:6,.0f} đ')

    print('\n=== B4 · Xem lại 100% (noi_dia + hang_nang) [simulated] ===')
    pv = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    runs_pv = runs[runs['request_id'].isin(pv['request_id'])]
    req_co_ok = runs_pv[runs_pv['status'] == 'ok']['request_id'].nunique()
    ca_lam_lai = (pv['ket_qua'] == 'lam_lai').sum()
    so_tc_pv = (pv['ket_qua'] == 'thanh_cong').sum()
    tok_tool_pv = (
        runs_pv['tokens_in'] / 1000 * GIA_VAO
        + runs_pv['tokens_out'] / 1000 * GIA_RA
        + runs_pv['tool_calls'] * GIA_TOOL
    ).sum()
    xem_lai_100 = req_co_ok * 5 * LUONG_PHUT
    lam_lai_9 = ca_lam_lai * 9 * LUONG_PHUT
    tong_9 = tok_tool_pv + xem_lai_100 + lam_lai_9
    cps_9 = tong_9 / so_tc_pv
    mean_ll = reqs.loc[reqs['ket_qua'] == 'lam_lai', 'phut_lam_lai_simulated'].mean()
    lam_lai_tt = ca_lam_lai * mean_ll * LUONG_PHUT
    tong_tt = tok_tool_pv + xem_lai_100 + lam_lai_tt
    cps_tt = tong_tt / so_tc_pv
    print(f'Mẫu số={so_tc_pv} việc TC | ok={req_co_ok} | lam_lai={ca_lam_lai} | tok+tool={tok_tool_pv:,.0f} đ')
    print(f'Làm lại 9 phút/ca:    tổng={tong_9:,.0f} đ | cps={cps_9:,.0f} đ ({cps_9 / BASELINE:.2f}x)')
    print(f'Làm lại {mean_ll:.1f} phút/ca: tổng={tong_tt:,.0f} đ | cps={cps_tt:,.0f} đ ({cps_tt / BASELINE:.2f}x)')


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    ket_qua = mo_hinh(runs, reqs)
    for ten, gia_tri in ket_qua.items():
        print(f'{ten:12s} {gia_tri:>14,.0f}')
    # TODO CP1 · Nhiệm vụ A3: tính lại theo từng giá trị của cột loai.
    # CP2 · Nhiệm vụ B: đổi từng yếu tố, ghi vào bảng độ nhạy.
    chay_nhiem_vu_b(runs, reqs)
    # TODO CP4 · Nhiệm vụ D: cỡ mẫu.
    #   from statsmodels.stats.proportion import proportion_effectsize
    #   from statsmodels.stats.power import NormalIndPower
