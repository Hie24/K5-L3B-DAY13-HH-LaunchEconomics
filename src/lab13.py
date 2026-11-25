"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Nhiệm vụ A1–A4 đã hoàn thiện; CP2 và CP4 được nhóm bổ sung sau.
Dữ liệu trong hai file CSV là giả lập; chi phí có dùng phút nhân viên mang nhãn simulated.
Bản gốc chưa sửa nằm ở lab13_starter.py.

Công thức và cách đối chiếu: docs/du_lieu_va_cong_thuc.md và
docs/Lab13_Huong_dan_chi_tiet_buoi_chieu.md, mục A.
"""
import math
import pandas as pd

# Bảng giá GIẢ ĐỊNH của lab (không phải giá thật của nhà cung cấp nào)
GIA_VAO = 26        # đồng cho 1.000 token đầu vào
GIA_RA = 130        # đồng cho 1.000 token đầu ra
GIA_TOOL = 15       # đồng cho 1 lần gọi tool
LUONG_PHUT = 2000   # đồng cho 1 phút của nhân viên (đã gồm bảo hiểm, văn phòng)
BASELINE = 12000    # đồng cho 1 yêu cầu khi nhân viên tự làm (6 phút)
CHI_PHI_CO_DINH = 40000000  # đồng/tháng, giả định của lab
YEU_CAU_MOI_THANG = 45000  # tất cả loại yêu cầu, trước khi lọc phạm vi pilot
PHAM_VI_PILOT = ('noi_dia', 'hang_nang')


def _kiem_tra_gioi_han(k):
    if k is not None and (isinstance(k, bool) or not isinstance(k, int) or k < 1):
        raise ValueError('Giới hạn số lần chạy phải là số nguyên dương hoặc None.')


def _kiem_tra_xac_suat(p, k):
    if not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError('Xác suất p phải nằm trong [0, 1].')
    _kiem_tra_gioi_han(k)


# ---------- Nhiệm vụ A1 · Kinh tế của việc chạy lại ----------
def so_lan_chay_ky_vong(p, k=None):
    """Số lần chạy trung bình cho 1 yêu cầu khi mỗi lần đúng với xác suất p.
    k = số lần chạy tối đa; k=None nghĩa là chạy lại đến khi đúng."""
    _kiem_tra_xac_suat(p, k)
    if p == 0:
        return math.inf if k is None else float(k)
    return 1 / p if k is None else (1 - (1 - p) ** k) / p


def ti_le_thanh_cong(p, k=None):
    """Xác suất yêu cầu thành công sau tối đa k lần chạy."""
    _kiem_tra_xac_suat(p, k)
    if p == 0:
        return 0.0
    return 1.0 if k is None else 1 - (1 - p) ** k


def he_so_chi_phi_moi_viec_thanh_cong(p, k=None):
    """Chi phí mỗi việc thành công, tính bằng bội số của giá một lần chạy."""
    thanh_cong = ti_le_thanh_cong(p, k)
    return so_lan_chay_ky_vong(p, k) / thanh_cong if thanh_cong else math.inf


def kiem_tra_dap_an_biet_truoc():
    """Ba phép thử bắt buộc đạt 100% trước khi tính trên dữ liệu."""
    assert abs(so_lan_chay_ky_vong(0.8, 2) - 1.20) < 1e-9, 'p=0,8, tối đa 2 lần → 1,20 lần chạy'
    assert abs(so_lan_chay_ky_vong(0.8) - 1.25) < 1e-9, 'p=0,8, chạy đến khi đúng → 1,25 lần chạy'
    assert abs(he_so_chi_phi_moi_viec_thanh_cong(0.8, 3) - 1.25) < 1e-9, 'p=0,8, tối đa 3 lần → 1,25 lần giá một lần chạy'
    print('Ba phép thử đáp án biết trước: ĐẠT')
    print(f'Tối đa 2 lần: {so_lan_chay_ky_vong(0.8, 2):.2f}; '
          f'chạy đến khi đúng: {so_lan_chay_ky_vong(0.8):.2f}; '
          f'hệ số chi phí tối đa 3 lần: {he_so_chi_phi_moi_viec_thanh_cong(0.8, 3):.2f}')


# ---------- Nhiệm vụ A2 · Mô hình chi phí từ trace ----------
# CP2 gọi lại hàm này với tham số giá và hệ số đã đổi.
def mo_hinh(runs, reqs, gia_vao=26, gia_ra=130, gia_tool=15, luong_phut=2000,
            he_so_xem_lai=1.0, he_so_lam_lai=1.0, max_lan_chay=None):
    """Trả về dict gồm: token, tool, xem_lai, lam_lai, tong, thanh_cong, cps (chi phí mỗi việc thành công).
    - token, tool: cộng trên MỌI lần chạy trong runs, kể cả lần lỗi.
    - xem_lai, lam_lai: số phút (cột *_simulated) × LUONG_PHUT. Đây là số GIẢ LẬP, phải ghi nhãn simulated khi báo cáo.
    - thanh_cong: số yêu cầu có ket_qua == 'thanh_cong'.
    - Các tham số giá/hệ số/max_lan_chay dùng cho Nhiệm vụ B (độ nhạy, giới hạn số lần chạy); giữ mặc định ở A2.
    """
    _kiem_tra_gioi_han(max_lan_chay)
    reqs = reqs.copy()
    runs = runs.loc[runs['request_id'].isin(reqs['request_id'])]
    if max_lan_chay is not None:
        runs = runs.loc[runs['attempt'] <= max_lan_chay]
        vuot_gioi_han = reqs['so_lan_chay'] > max_lan_chay
        reqs.loc[vuot_gioi_han, 'ket_qua'] = 'chuyen_nhan_vien'
        reqs.loc[vuot_gioi_han, ['phut_xem_lai_simulated', 'phut_lam_lai_simulated']] = 0

    tien_token = runs['tokens_in'] / 1000 * gia_vao + runs['tokens_out'] / 1000 * gia_ra
    tien_tool = runs['tool_calls'] * gia_tool
    token, tool = float(tien_token.sum()), float(tien_tool.sum())
    xem_lai = float(reqs['phut_xem_lai_simulated'].sum()) * luong_phut * he_so_xem_lai
    lam_lai = float(reqs['phut_lam_lai_simulated'].sum()) * luong_phut * he_so_lam_lai
    tong = token + tool + xem_lai + lam_lai
    thanh_cong = int(reqs['ket_qua'].eq('thanh_cong').sum())
    return dict(
        token=token, tool=tool,
        chay_lai=float((tien_token + tien_tool).loc[runs['attempt'] > 1].sum()),
        xem_lai=xem_lai, lam_lai=lam_lai, tong=tong, thanh_cong=thanh_cong,
        cps=tong / thanh_cong if thanh_cong else math.inf,
        hoa_don_moi_yc=(token + tool) / len(reqs) if len(reqs) else 0.0,
    )


def chi_phi_he_thong_moi_yeu_cau(ket_qua, so_yeu_cau):
    """Theo quy ước B3: cộng 12.000 đ cho mỗi yêu cầu không thành công.

    Bao gồm cả lam_lai và chuyen_nhan_vien; chưa cộng chi phí cố định.
    """
    if so_yeu_cau < 1:
        raise ValueError('Cần ít nhất một yêu cầu để tính chi phí mỗi yêu cầu.')
    khong_thanh_cong = so_yeu_cau - ket_qua['thanh_cong']
    return (ket_qua['tong'] + khong_thanh_cong * BASELINE) / so_yeu_cau


# ---------- Nhiệm vụ A3 · Chi phí theo loại yêu cầu ----------
def bang_chi_phi_theo_loai(runs, reqs):
    """Tỷ lệ so với baseline của cps chỉ là tham chiếu, khác mẫu số.

    Khi so kinh tế, dùng thêm chi_phi_he_thong_moi_yc, đã cộng nhân viên làm thay.
    """
    cac_dong = []
    for loai, nhom in reqs.groupby('loai', sort=False):
        ket_qua = mo_hinh(runs, nhom)
        so_yeu_cau = len(nhom)
        so_lan_chay = int(runs['request_id'].isin(nhom['request_id']).sum())
        cac_dong.append(dict(
            loai=loai, so_yeu_cau=so_yeu_cau,
            ti_le_thanh_cong=ket_qua['thanh_cong'] / so_yeu_cau,
            lan_chay_moi_yc=so_lan_chay / so_yeu_cau,
            cps=ket_qua['cps'], so_voi_baseline=ket_qua['cps'] / BASELINE,
            chi_phi_he_thong_moi_yc=chi_phi_he_thong_moi_yeu_cau(ket_qua, so_yeu_cau),
        ))
    return pd.DataFrame(cac_dong).set_index('loai').sort_index()


def ti_le_ok_theo_lan_chay(runs, reqs):
    """Tỷ lệ ok trong số lần chạy thực sự quan sát ở từng attempt, từng loại."""
    noi = runs.merge(reqs[['request_id', 'loai']], on='request_id', validate='many_to_one')
    noi['ok'] = noi['status'].eq('ok')
    return noi.pivot_table(index='loai', columns='attempt', values='ok', aggfunc='mean')


# ---------- Nhiệm vụ A4 · Phân bổ chi phí cố định trong phạm vi pilot ----------
def bang_chi_phi_co_dinh(runs, reqs, chi_phi_co_dinh=CHI_PHI_CO_DINH,
                        yeu_cau_moi_thang=YEU_CAU_MOI_THANG):
    """Giữ cơ cấu mẫu khi ngoại suy tổng khối lượng và một nửa khối lượng.

    reqs là toàn bộ mẫu, không lọc trước: 45.000 yc/tháng bao gồm cả loại ngoài pilot.
    Các chi phí mỗi việc ở bảng này có phần simulated.
    """
    pham_vi = reqs.loc[reqs['loai'].isin(PHAM_VI_PILOT)]
    ket_qua = mo_hinh(runs, pham_vi)
    if not len(reqs) or not len(pham_vi) or not ket_qua['thanh_cong']:
        raise ValueError('Cần mẫu có ít nhất một việc thành công trong phạm vi pilot.')
    if not math.isfinite(yeu_cau_moi_thang) or yeu_cau_moi_thang <= 0:
        raise ValueError('Khối lượng yêu cầu mỗi tháng phải dương và hữu hạn.')
    if not math.isfinite(chi_phi_co_dinh) or chi_phi_co_dinh < 0:
        raise ValueError('Chi phí cố định phải không âm và hữu hạn.')
    chi_phi_he_thong = chi_phi_he_thong_moi_yeu_cau(ket_qua, len(pham_vi))
    cac_dong = []
    for khoi_luong in (yeu_cau_moi_thang, yeu_cau_moi_thang / 2):
        thanh_cong_thang = khoi_luong * ket_qua['thanh_cong'] / len(reqs)
        yeu_cau_trong_pham_vi = khoi_luong * len(pham_vi) / len(reqs)
        co_dinh_moi_viec = chi_phi_co_dinh / thanh_cong_thang
        cps_co_dinh = ket_qua['cps'] + co_dinh_moi_viec
        cac_dong.append(dict(
            yeu_cau_moi_thang=khoi_luong, thanh_cong_moi_thang=thanh_cong_thang,
            co_dinh_moi_viec=co_dinh_moi_viec, cps_cong_co_dinh=cps_co_dinh,
            so_voi_baseline=cps_co_dinh / BASELINE,
            he_thong_moi_yc_trong_pham_vi=(
                chi_phi_he_thong + chi_phi_co_dinh / yeu_cau_trong_pham_vi
            ),
        ))
    return pd.DataFrame(cac_dong)


def in_bang_nhiem_vu_a(runs, reqs):
    """In số liệu A2–A4 để điền báo cáo; tiền làm tròn khi hiển thị."""
    ket_qua = mo_hinh(runs, reqs)
    print('\nA2 · Mô hình chi phí từ trace (chưa gồm cố định)')
    for ten, gia_tri in ket_qua.items():
        nhan = ' [simulated]' if ten in ('xem_lai', 'lam_lai', 'tong', 'cps') else ''
        hien_thi = f'{gia_tri:,.0f}' if ten == 'thanh_cong' else f'{gia_tri:,.2f}'
        print(f'{ten:18s} {hien_thi:>14s}{nhan}')
    print(f'Cps / hóa đơn mỗi yêu cầu: {ket_qua["cps"] / ket_qua["hoa_don_moi_yc"]:.2f} lần [simulated]')
    cac_khoan = {ten: ket_qua[ten] for ten in ('token', 'tool', 'xem_lai', 'lam_lai')}
    lon_nhat = max(cac_khoan, key=cac_khoan.get)
    print(f'Khoản lớn nhất: {lon_nhat}, {cac_khoan[lon_nhat] / ket_qua["tong"]:.2%} [simulated]')
    print(f'Yêu cầu không thành công: {len(reqs) - ket_qua["thanh_cong"]}')
    chi_phi_he_thong = chi_phi_he_thong_moi_yeu_cau(ket_qua, len(reqs))
    print(f'Cả hệ thống: {chi_phi_he_thong:,.2f} đ/yêu cầu '
          f'= {chi_phi_he_thong / BASELINE:.2f}x baseline [simulated; chưa gồm cố định]')

    print('\nA3 · Chi phí theo loại (cps, so_voi_baseline, chi_phi_he_thong_moi_yc: simulated)')
    print(bang_chi_phi_theo_loai(runs, reqs).to_string(formatters={
        'ti_le_thanh_cong': '{:.2%}'.format, 'lan_chay_moi_yc': '{:.2f}'.format,
        'cps': '{:,.2f}'.format, 'so_voi_baseline': '{:.2f}x'.format,
        'chi_phi_he_thong_moi_yc': '{:,.2f}'.format,
    }))
    print('\nA3 · Tỷ lệ ok theo attempt (mẫu số là số lần chạy tại attempt đó)')
    bang_ok = ti_le_ok_theo_lan_chay(runs, reqs)
    print(bang_ok.to_string(formatters={cot: '{:.2%}'.format for cot in bang_ok.columns}))

    pham_vi = reqs.loc[reqs['loai'].isin(PHAM_VI_PILOT)]
    ket_qua_pilot = mo_hinh(runs, pham_vi)
    print(f'\nA4 · Phạm vi noi_dia + hang_nang: {len(pham_vi)} yêu cầu, '
          f'{ket_qua_pilot["thanh_cong"]} thành công trên {len(reqs)} yêu cầu toàn mẫu')
    print(f'Chi phí biến đổi trong phạm vi: {ket_qua_pilot["tong"]:,.2f} đ; '
          f'cps chưa cố định: {ket_qua_pilot["cps"]:,.2f} đ [simulated]')
    print('Chi phí cố định 40 triệu đ/tháng; mọi chi phí tổng hợp bên dưới: simulated.')
    bang_co_dinh = bang_chi_phi_co_dinh(runs, reqs)
    print(bang_co_dinh.to_string(index=False, formatters={
        cot: ('{:.2f}x'.format if cot == 'so_voi_baseline' else '{:,.2f}'.format)
        for cot in bang_co_dinh.columns
    }))


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


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    in_bang_nhiem_vu_a(runs, reqs)
    # TODO CP2 · Nhiệm vụ B: đổi từng yếu tố, ghi vào bảng độ nhạy.
    # CP4 · Nhiệm vụ D1: cỡ mẫu (issue #5).
    nhiem_vu_d1(reqs)
