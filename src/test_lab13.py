"""Kiểm tra A1–A4: cd src && python -m unittest -v test_lab13.py.

Fixture nhỏ tính tay; số đối chiếu toàn mẫu lấy từ hướng dẫn chi tiết mục A.
"""
import math
from pathlib import Path
import unittest

import pandas as pd

from lab13 import (
    bang_chi_phi_co_dinh,
    bang_chi_phi_theo_loai,
    chi_phi_he_thong_moi_yeu_cau,
    he_so_chi_phi_moi_viec_thanh_cong,
    kiem_tra_dap_an_biet_truoc,
    mo_hinh,
    so_lan_chay_ky_vong,
    ti_le_ok_theo_lan_chay,
    ti_le_thanh_cong,
)


class RetryTests(unittest.TestCase):
    def test_three_required_answers(self):
        kiem_tra_dap_an_biet_truoc()

    def test_zero_and_certain_success(self):
        self.assertEqual(so_lan_chay_ky_vong(0, 3), 3)
        self.assertEqual(ti_le_thanh_cong(0, 3), 0)
        self.assertEqual(ti_le_thanh_cong(0), 0)
        self.assertTrue(math.isinf(so_lan_chay_ky_vong(0)))
        self.assertTrue(math.isinf(he_so_chi_phi_moi_viec_thanh_cong(0, 3)))
        self.assertEqual(so_lan_chay_ky_vong(1, 3), 1)
        self.assertEqual(ti_le_thanh_cong(1, 3), 1)

    def test_invalid_probability_and_limit(self):
        for p in (-0.1, 1.1, math.nan, math.inf):
            with self.subTest(p=p), self.assertRaises(ValueError):
                so_lan_chay_ky_vong(p, 2)
        for k in (0, -1, 1.5, True):
            with self.subTest(k=k), self.assertRaises(ValueError):
                ti_le_thanh_cong(0.8, k)


class CostModelTests(unittest.TestCase):
    def setUp(self):
        self.runs = pd.DataFrame([
            ('A', 1, 1000, 100, 1, 'loi'),
            ('A', 2, 500, 50, 2, 'ok'),
            ('B', 1, 1000, 0, 1, 'ok'),
            ('C', 1, 0, 100, 1, 'loi'),
            ('C', 2, 0, 100, 1, 'loi'),
            ('C', 3, 0, 100, 1, 'loi'),
            # Không thuộc requests: tuyệt đối không tính vào phạm vi này.
            ('OUTSIDE', 1, 100000, 100000, 100, 'ok'),
        ], columns=['request_id', 'attempt', 'tokens_in', 'tokens_out', 'tool_calls', 'status'])
        self.reqs = pd.DataFrame([
            ('A', 'noi_dia', 2, 'thanh_cong', 2, 0),
            ('B', 'hang_nang', 1, 'lam_lai', 1, 3),
            ('C', 'quoc_te', 3, 'chuyen_nhan_vien', 0, 0),
        ], columns=['request_id', 'loai', 'so_lan_chay', 'ket_qua',
                    'phut_xem_lai_simulated', 'phut_lam_lai_simulated'])

    def test_failed_runs_and_human_time_are_charged(self):
        result = mo_hinh(self.runs, self.reqs)
        # Token A=58,5; B=26; C=39. Tool A=45; B=15; C=45.
        for name, expected in dict(token=123.5, tool=105, chay_lai=105.5,
                                   xem_lai=6000, lam_lai=6000, tong=12228.5,
                                   thanh_cong=1, cps=12228.5).items():
            with self.subTest(name=name):
                self.assertAlmostEqual(result[name], expected)
        self.assertAlmostEqual(result['hoa_don_moi_yc'], 228.5 / 3)

    def test_filter_requests_before_summing_runs(self):
        result = mo_hinh(self.runs, self.reqs.loc[self.reqs['request_id'] == 'A'])
        self.assertAlmostEqual(result['tong'], 4103.5)
        self.assertAlmostEqual(result['chay_lai'], 49.5)
        self.assertEqual(result['thanh_cong'], 1)

    def test_cutoff_reclassifies_and_removes_human_time(self):
        once = mo_hinh(self.runs, self.reqs, max_lan_chay=1)
        self.assertAlmostEqual(once['tong'], 8123)
        self.assertEqual(once['xem_lai'], 2000)
        self.assertEqual(once['lam_lai'], 6000)
        self.assertEqual(once['thanh_cong'], 0)
        self.assertTrue(math.isinf(once['cps']))
        twice = mo_hinh(self.runs, self.reqs, max_lan_chay=2)
        self.assertAlmostEqual(twice['tong'], 12200.5)
        self.assertEqual(twice['thanh_cong'], 1)

    def test_model_does_not_mutate_inputs(self):
        before_runs, before_reqs = self.runs.copy(deep=True), self.reqs.copy(deep=True)
        mo_hinh(self.runs, self.reqs, max_lan_chay=1)
        mo_hinh(self.runs, self.reqs, max_lan_chay=2)
        pd.testing.assert_frame_equal(self.runs, before_runs)
        pd.testing.assert_frame_equal(self.reqs, before_reqs)

    def test_cutoff_clears_rework_time_for_a_request_requiring_two_runs(self):
        # B vẫn phải thử lần 2 trước khi nhân viên bắt lỗi và làm lại.
        self.reqs.loc[self.reqs['request_id'] == 'B', 'so_lan_chay'] = 2
        second_run = pd.DataFrame([('B', 2, 1000, 0, 1, 'ok')], columns=self.runs.columns)
        runs = pd.concat([self.runs, second_run], ignore_index=True)
        result = mo_hinh(runs, self.reqs, max_lan_chay=1)
        self.assertEqual(result['xem_lai'], 0)
        self.assertEqual(result['lam_lai'], 0)
        self.assertAlmostEqual(result['tong'], 123)

    def test_price_and_human_time_parameters_for_task_b(self):
        result = mo_hinh(self.runs, self.reqs, gia_vao=52, gia_ra=260, gia_tool=30,
                        luong_phut=2500, he_so_xem_lai=2, he_so_lam_lai=0.5)
        self.assertAlmostEqual(result['tong'], 247 + 210 + 15000 + 3750)

    def test_system_cost_pays_for_both_kinds_of_unsuccessful_requests(self):
        result = mo_hinh(self.runs, self.reqs)
        self.assertAlmostEqual(chi_phi_he_thong_moi_yeu_cau(result, 3), 12076.166666666666)

    def test_empty_scope_and_no_success_are_explicit(self):
        result = mo_hinh(self.runs, self.reqs.iloc[:0])
        self.assertEqual(result['tong'], 0)
        self.assertEqual(result['thanh_cong'], 0)
        self.assertEqual(result['hoa_don_moi_yc'], 0)
        self.assertTrue(math.isinf(result['cps']))


class FullDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = Path(__file__).resolve().parent
        cls.runs = pd.read_csv(folder / 'logix_runs.csv')
        cls.reqs = pd.read_csv(folder / 'logix_requests.csv', keep_default_na=False)

    def test_a2_against_reference(self):
        result = mo_hinh(self.runs, self.reqs)
        self.assertEqual((len(self.runs), len(self.reqs), result['thanh_cong']), (1624, 1200, 978))
        for name, expected in dict(token=245585.13, tool=84000, chay_lai=93804.49,
                                   xem_lai=1780000, lam_lai=2264000,
                                   tong=4373585.13, cps=4471.97).items():
            with self.subTest(name=name):
                self.assertAlmostEqual(result[name], expected, delta=0.01)

    def test_a3_costs_and_retry_rates(self):
        table = bang_chi_phi_theo_loai(self.runs, self.reqs)
        for kind, count, cps in [('noi_dia', 824, 2695.64), ('hang_nang', 158, 8220.73),
                                  ('quoc_te', 150, 22515.17), ('doi_tac', 68, 10214.87)]:
            with self.subTest(kind=kind):
                self.assertEqual(table.loc[kind, 'so_yeu_cau'], count)
                self.assertAlmostEqual(table.loc[kind, 'cps'], cps, delta=0.01)
        rates = ti_le_ok_theo_lan_chay(self.runs, self.reqs)
        for attempt, expected in [(1, 0.30), (2, 0.1143), (3, 0.0215)]:
            with self.subTest(attempt=attempt):
                self.assertAlmostEqual(rates.loc['quoc_te', attempt], expected, delta=0.0001)

    def test_a4_uses_full_sample_denominator_and_half_volume(self):
        table = bang_chi_phi_co_dinh(self.runs, self.reqs)
        full, half = table.iloc[0], table.iloc[1]
        # 45.000 là tất cả loại yêu cầu: mẫu số 1.200, không phải 982 trong phạm vi.
        self.assertEqual(full['thanh_cong_moi_thang'], 33750)
        self.assertEqual(half['thanh_cong_moi_thang'], 16875)
        self.assertAlmostEqual(full['cps_cong_co_dinh'], 4599.09, delta=0.01)
        self.assertAlmostEqual(half['cps_cong_co_dinh'], 5784.27, delta=0.01)
        self.assertAlmostEqual(half['co_dinh_moi_viec'], full['co_dinh_moi_viec'] * 2)
        self.assertAlmostEqual(full['he_thong_moi_yc_trong_pham_vi'], 5217.09, delta=0.01)
        self.assertAlmostEqual(half['he_thong_moi_yc_trong_pham_vi'], 6303.31, delta=0.01)


if __name__ == '__main__':
    unittest.main()
