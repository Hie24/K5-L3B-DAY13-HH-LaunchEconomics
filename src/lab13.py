"""Lab 13 · Định giá agent và lập kế hoạch pilot (Gate 2a) — bài làm của nhóm (file nộp).
Chạy trong thư mục src/: python3 lab13.py   (cần pandas; Nhiệm vụ D cần thêm statsmodels)
Không cần khoá API. Nhiệm vụ A1–A4 và B1–B4 đã hoàn thiện; CP4 được nhóm bổ sung sau.
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


# ---------- Nhiệm vụ B · Bảng độ nhạy, giới hạn chạy lại và xem lại 100% ----------
def chay_nhiem_vu_b(runs, reqs):
    """In B1–B4 và trả số liệu chưa làm tròn để kiểm chứng, dùng lại trong hồ sơ."""
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
    bang_b1 = []
    for ten, kw in kich_ban:
        cps = mo_hinh(runs, reqs, **kw)['cps']
        pct = (cps / cps_goc - 1) * 100
        bang_b1.append(dict(kich_ban=ten, cps=cps, thay_doi_pct=pct))
        print(f'{ten:28s} {cps:8,.0f} đ ({pct:+6.1f}%)')

    print('\n=== B2 · Đổi một cặp [simulated] ===')
    cap = mo_hinh(runs, reqs, gia_vao=52, gia_ra=260, he_so_xem_lai=2.0)['cps']
    print(f'Token x2 + Xem lại x2: {cap:,.0f} đ ({(cap / cps_goc - 1) * 100:+.1f}%)')
    cac_yeu_to_tang = [dong for dong in bang_b1 if dong['kich_ban'] in (
        'Giá token gấp đôi', 'Tỉ lệ xem lại gấp đôi',
        'Số ca làm lại gấp đôi', 'Lương nhân viên tăng 25%',
    )]
    xep_hang = sorted(cac_yeu_to_tang, key=lambda dong: dong['thay_doi_pct'], reverse=True)[:3]
    print('Ba yếu tố nhạy nhất (kịch bản tăng của B1): ' + ' · '.join(
        f'{i}. {dong["kich_ban"]} ({dong["thay_doi_pct"]:+.1f}%)'
        for i, dong in enumerate(xep_hang, start=1)
    ))

    print(f'\n=== B3 · Chi phí cả hệ thống theo giới hạn chạy lại ({len(reqs)} yêu cầu) [simulated] ===')
    bang_b3 = []
    for k in (1, 2, 3):
        kq = mo_hinh(runs, reqs, max_lan_chay=k)
        khong_tc = len(reqs) - kq['thanh_cong']
        ca_he_thong = kq['tong'] + khong_tc * BASELINE
        bang_b3.append(dict(gioi_han=k, tong=kq['tong'], khong_thanh_cong=khong_tc,
                            ca_he_thong=ca_he_thong, cps=kq['cps']))
        print(f'k={k} | trợ lý={kq["tong"]:10,.0f} đ | không TC={khong_tc:3d} | '
              f'cả hệ thống={ca_he_thong:10,.0f} đ | cps={kq["cps"]:6,.0f} đ')

    pv = reqs[reqs['loai'].isin(['noi_dia', 'hang_nang'])]
    bang_b3_pilot = []
    print('Đối chiếu riêng phạm vi pilot (chưa gồm cố định) [simulated]:')
    for k in (1, 2, 3):
        kq_pilot = mo_hinh(runs, pv, max_lan_chay=k)
        he_thong_pilot = chi_phi_he_thong_moi_yeu_cau(kq_pilot, len(pv))
        bang_b3_pilot.append(dict(gioi_han=k, cps=kq_pilot['cps'],
                                 he_thong_moi_yc=he_thong_pilot))
        print(f'k={k}: cps={kq_pilot["cps"]:,.2f} đ; hệ thống={he_thong_pilot:,.2f} đ/yêu cầu')
    print('\n=== B4 · Xem lại 100% (noi_dia + hang_nang) [simulated] ===')
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
    hoa_von_9 = (BASELINE * so_tc_pv - tok_tool_pv - lam_lai_9) / (req_co_ok * LUONG_PHUT)
    hoa_von_tt = (BASELINE * so_tc_pv - tok_tool_pv - lam_lai_tt) / (req_co_ok * LUONG_PHUT)
    co_dinh_moi_viec = bang_chi_phi_co_dinh(runs, reqs).iloc[0]['co_dinh_moi_viec']
    print(f'Mẫu số={so_tc_pv} việc TC | ok={req_co_ok} | lam_lai={ca_lam_lai} | tok+tool={tok_tool_pv:,.0f} đ')
    print(f'Làm lại 9 phút/ca:    tổng={tong_9:,.0f} đ | cps={cps_9:,.0f} đ ({cps_9 / BASELINE:.2f}x)')
    print(f'Làm lại {mean_ll:.1f} phút/ca: tổng={tong_tt:,.0f} đ | cps={cps_tt:,.0f} đ ({cps_tt / BASELINE:.2f}x)')
    print(f'Hòa vốn thời gian xem lại (chưa cố định): {hoa_von_9:.2f} phút (làm lại 9 phút); '
          f'{hoa_von_tt:.2f} phút (làm lại theo dữ liệu) [simulated]')
    print(f'Cộng cố định ở {YEU_CAU_MOI_THANG:,} yêu cầu tổng/tháng: '
          f'{cps_9 + co_dinh_moi_viec:,.2f} đ/việc (9 phút); '
          f'{cps_tt + co_dinh_moi_viec:,.2f} đ/việc (theo dữ liệu) [simulated]')
    return dict(
        goc=goc, b1=bang_b1, b2=cap, xep_hang=xep_hang,
        b3=bang_b3, b3_pilot=bang_b3_pilot,
        b4=dict(so_yeu_cau=len(pv), co_ok=req_co_ok, lam_lai=int(ca_lam_lai),
                thanh_cong=int(so_tc_pv), token_tool=float(tok_tool_pv),
                tong_9=float(tong_9), cps_9=float(cps_9),
                phut_lam_lai_du_lieu=float(mean_ll), cps_du_lieu=float(cps_tt),
                hoa_von_9=float(hoa_von_9), hoa_von_du_lieu=float(hoa_von_tt),
                cps_9_co_dinh=float(cps_9 + co_dinh_moi_viec),
                cps_du_lieu_co_dinh=float(cps_tt + co_dinh_moi_viec)),
    )


if __name__ == '__main__':
    runs = pd.read_csv('logix_runs.csv')
    reqs = pd.read_csv('logix_requests.csv', keep_default_na=False)
    kiem_tra_dap_an_biet_truoc()
    in_bang_nhiem_vu_a(runs, reqs)
    chay_nhiem_vu_b(runs, reqs)
    # TODO CP4 · Nhiệm vụ D: cỡ mẫu.
    #   from statsmodels.stats.proportion import proportion_effectsize
    #   from statsmodels.stats.power import NormalIndPower
