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


# ---------- Nhiệm vụ D1 · Cỡ mẫu pilot (issue #5, lekhanh2k5-dotcom) ----------
# TODO CP4: số cho sẵn của lab: baseline 0,70; mục tiêu +5 điểm; alpha 0,05; power 0,8; ICC 0,02.
BASE_P = 0.70
ICC = 0.02
SO_NHAN_VIEN = 40          # khoảng 40 nhân viên CSKH
YC_MOI_NGAY = 1500         # khoảng 1.500 yêu cầu / ngày cho cả công ty
PHAM_VI = ('noi_dia', 'hang_nang')


def co_mau_mot_nhom(p1, p2, alpha=0.05, power=0.80):
    """Cỡ mẫu mỗi nhóm khi so hai tỉ lệ (công thức 4 của lab), z chính xác, làm tròn lên."""
    from statistics import NormalDist
    za, zb = NormalDist().inv_cdf(1 - alpha / 2), NormalDist().inv_cdf(power)
    pb = (p1 + p2) / 2
    tu = (za * math.sqrt(2 * pb * (1 - pb)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(tu / (p2 - p1) ** 2)


def he_so_thiet_ke(m, icc=ICC):
    """DE = 1 + (m − 1) × ICC, m = số yêu cầu mỗi cụm."""
    return 1 + (m - 1) * icc


def m_toi_thieu(n_can, so_cum, icc=ICC):
    """m nhỏ nhất để c·m / DE(m) ≥ n_can; None nếu vượt giới hạn c / ICC (không m nào đủ)."""
    if n_can >= so_cum / icc:
        return None
    # c·m ≥ n·(1 − ICC + ICC·m)  →  m·(c − n·ICC) ≥ n·(1 − ICC)
    return math.ceil(n_can * (1 - icc) / (so_cum - n_can * icc))


def nhiem_vu_d1(reqs):
    """In năm câu D1, power khi chấp nhận mức chênh 6 điểm, và số liệu để đặt luật an toàn / ngày quyết định."""
    from statsmodels.stats.power import NormalIndPower
    from statsmodels.stats.proportion import proportion_effectsize

    n5 = co_mau_mot_nhom(BASE_P, BASE_P + 0.05)
    print('\nNhiệm vụ D1 · cỡ mẫu mỗi nhóm (baseline 0,70; alpha 0,05; power 0,8; ICC 0,02)')
    print(f'  a) Chia theo yêu cầu, mức chênh 5 điểm: {n5:,} yêu cầu mỗi nhóm')

    de75 = he_so_thiet_ke(75)
    n_b = math.ceil(n5 * de75)
    nv_b = math.ceil(n_b / 75)
    print(f'  b) Theo nhân viên, m = 75: DE = {de75:.2f}; {n_b:,} yêu cầu mỗi nhóm = {nv_b} nhân viên mỗi nhóm, '
          f'tổng {2 * nv_b} > {SO_NHAN_VIEN}: {"không đủ người" if 2 * nv_b > SO_NHAN_VIEN else "đủ"}')

    tran_20 = 20 / ICC
    print(f'  c) 20 nhân viên mỗi nhóm: cỡ mẫu hiệu dụng tối đa c/ICC = {tran_20:,.0f} '
          f'{"<" if tran_20 < n5 else "≥"} {n5:,}: {"không đạt" if tran_20 < n5 else "đạt"} mức chênh 5 điểm')

    tran_6 = 6 / ICC
    print(f'  d) 6 depot mỗi nhóm: cỡ mẫu hiệu dụng tối đa c/ICC = {tran_6:,.0f} < {n5:,}: không đạt, chỉ 6 cụm')

    n6 = co_mau_mot_nhom(BASE_P, BASE_P + 0.06)
    m6 = m_toi_thieu(n6, 20)
    print(f'  e) Mức chênh 6 điểm: {n6:,} mỗi nhóm; 20 nhân viên mỗi nhóm cần m ≥ {m6} yêu cầu mỗi người '
          f'(DE = {he_so_thiet_ke(m6):.2f}; hiệu dụng {20 * m6 / he_so_thiet_ke(m6):,.1f} ≥ {n6:,})')

    es5 = proportion_effectsize(BASE_P + 0.05, BASE_P)
    power5 = NormalIndPower().power(effect_size=es5, nobs1=n6, alpha=0.05, ratio=1.0)
    print(f'  Bất lợi khi chọn mức chênh 6 điểm: nếu tác động thật chỉ 5 điểm, power với n = {n6} chỉ còn {power5:.2f}')

    mo_lai = reqs.mo_lai_trong_7_ngay.astype(int)
    trong_pv = reqs.loai.isin(PHAM_VI)
    print(f'  Mở lại 7 ngày hiện tại: {mo_lai.mean():.2%} ({mo_lai.sum()}/{len(reqs)}); '
          f'phạm vi noi_dia + hang_nang: {mo_lai[trong_pv].mean():.2%} ({mo_lai[trong_pv].sum()}/{trong_pv.sum()})')

    ti_le_pv = trong_pv.mean()
    yc_pv_moi_nv_ngay = YC_MOI_NGAY / SO_NHAN_VIEN * ti_le_pv
    ngay_du_m = math.ceil(m6 / yc_pv_moi_nv_ngay)
    print(f'  Phạm vi chiếm {ti_le_pv:.1%} yêu cầu → mỗi nhân viên ≈ {yc_pv_moi_nv_ngay:.1f} yêu cầu trong phạm vi/ngày; '
          f'cần ≈ {ngay_du_m} ngày làm việc ở bước 0,50 để đạt m = {m6}')
    return {'n5': n5, 'de75': de75, 'n_b': n_b, 'nv_b': nv_b, 'tran_20': tran_20, 'tran_6': tran_6,
            'n6': n6, 'm6': m6, 'de6': he_so_thiet_ke(m6), 'power5': power5,
            'mo_lai': mo_lai.mean(), 'mo_lai_pv': mo_lai[trong_pv].mean(), 'ngay_du_m': ngay_du_m}


# ---------- Nhiệm vụ E1 · Tính thử ba chỉ số (issue #6, lekhanh2k5-dotcom) ----------
def _ti_le(mask, mau):
    """(tử, mẫu, tỉ lệ) để ghi đủ tử số / mẫu số trong chi_so.md."""
    tu, n = int(mask.sum()), int(len(mau))
    return tu, n, (tu / n if n else float('nan'))


def nhiem_vu_e1(reqs):
    """Ba chỉ số của đợt chạy thử (không có đối chứng: chỉ mô tả, không kết luận trợ lý gây ra thay đổi)."""
    r = reqs.copy()
    for cot in ('dong_trong_24h', 'mo_lai_trong_7_ngay', 'duoc_xem_lai'):
        r[cot] = r[cot].astype(int)
    pv = r[r.loai.isin(PHAM_VI)]
    ket = {}
    print('\nNhiệm vụ E1 · chỉ số trong đợt chạy thử (cả mẫu | phạm vi noi_dia + hang_nang)')
    for ten, ham in (
        ('chinh', lambda d: ((d.dong_trong_24h == 1) & (d.mo_lai_trong_7_ngay == 0), d)),
        ('dung_bo_qua', lambda d: (d[d.duoc_xem_lai == 1].quyet_dinh_xem_lai.isin(['sua', 'bo']),
                                   d[d.duoc_xem_lai == 1])),
        ('an_toan_mo_lai', lambda d: (d.mo_lai_trong_7_ngay == 1, d)),
        ('lam_lai', lambda d: (d.ket_qua == 'lam_lai', d)),
        ('chuyen_nhan_vien', lambda d: (d.ket_qua == 'chuyen_nhan_vien', d)),
        ('duoc_xem_lai', lambda d: (d.duoc_xem_lai == 1, d)),
    ):
        ca = _ti_le(*ham(r))
        p = _ti_le(*ham(pv))
        ket[ten] = {'ca_mau': ca, 'pham_vi': p}
        print(f'  {ten:17s} {ca[2]:7.2%} ({ca[0]}/{ca[1]})  |  {p[2]:7.2%} ({p[0]}/{p[1]})')
    return ket


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    ket_qua = mo_hinh(runs, reqs)
    for ten, gia_tri in ket_qua.items():
        print(f'{ten:12s} {gia_tri:>14,.0f}')
    # TODO CP1 · Nhiệm vụ A3: tính lại theo từng giá trị của cột loai.
    # TODO CP2 · Nhiệm vụ B: đổi từng yếu tố, ghi vào bảng độ nhạy.
    # CP4 · Nhiệm vụ D1: cỡ mẫu (issue #5).
    nhiem_vu_d1(reqs)
    # CP5 · Nhiệm vụ E1: tính thử ba chỉ số (issue #6).
    nhiem_vu_e1(reqs)
