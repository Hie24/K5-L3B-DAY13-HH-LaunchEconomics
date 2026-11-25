"""Kiểm tra tích hợp A/B sau khi xử lý conflict PR #13."""
from contextlib import redirect_stdout
import io
import os
from pathlib import Path
import subprocess
import sys
import unittest

import pandas as pd

from lab13 import chay_nhiem_vu_b


class SensitivityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = Path(__file__).resolve().parent
        cls.runs = pd.read_csv(cls.folder / 'logix_runs.csv')
        cls.reqs = pd.read_csv(cls.folder / 'logix_requests.csv', keep_default_na=False)
        with redirect_stdout(io.StringIO()):
            cls.result = chay_nhiem_vu_b(cls.runs, cls.reqs)

    def test_nine_scenarios_match_reference(self):
        expected = (4723, 4346, 6292, 3562, 6787, 3315, 5506, 4237, 4111)
        self.assertEqual(len(self.result['b1']), 9)
        for row, cps in zip(self.result['b1'], expected):
            with self.subTest(scenario=row['kich_ban']):
                self.assertAlmostEqual(row['cps'], cps, delta=0.6)

    def test_symmetric_changes_and_additive_pair(self):
        rows = self.result['b1']
        baseline = self.result['goc']['cps']
        for up, down in ((0, 1), (2, 3), (4, 5)):
            self.assertAlmostEqual(rows[up]['cps'] - baseline,
                                   2 * (baseline - rows[down]['cps']))
        self.assertAlmostEqual(self.result['b2'], rows[0]['cps'] + rows[2]['cps'] - baseline)
        self.assertEqual([row['kich_ban'] for row in self.result['xep_hang']], [
            'Số ca làm lại gấp đôi', 'Tỉ lệ xem lại gấp đôi', 'Lương nhân viên tăng 25%',
        ])

    def test_system_cost_optimum_differs_from_cost_per_success_optimum(self):
        rows = self.result['b3']
        self.assertEqual([row['khong_thanh_cong'] for row in rows], [319, 234, 222])
        for row, total in zip(rows, (7449781, 6901220, 7037585)):
            self.assertAlmostEqual(row['ca_he_thong'], total, delta=0.6)
        self.assertEqual(min(rows, key=lambda row: row['ca_he_thong'])['gioi_han'], 2)
        self.assertEqual(min(rows, key=lambda row: row['cps'])['gioi_han'], 1)

    def test_pilot_scope_also_favors_two_attempts(self):
        rows = self.result['b3_pilot']
        for row, cost in zip(rows, (4649.47, 4053.35, 4130.87)):
            self.assertAlmostEqual(row['he_thong_moi_yc'], cost, delta=0.01)
        self.assertEqual(min(rows, key=lambda row: row['he_thong_moi_yc'])['gioi_han'], 2)

    def test_full_review_replaces_existing_labor_costs(self):
        result = self.result['b4']
        self.assertEqual((result['so_yeu_cau'], result['co_ok'], result['lam_lai'],
                          result['thanh_cong']), (982, 948, 48, 900))
        self.assertAlmostEqual(result['tong_9'], 10568513.274)
        self.assertAlmostEqual(result['cps_9'], 11742.79, delta=0.01)
        self.assertAlmostEqual(result['phut_lam_lai_du_lieu'], 1132 / 74)
        self.assertAlmostEqual(result['cps_du_lieu'], 12414.50, delta=0.01)
        self.assertAlmostEqual(result['hoa_von_9'], 5.12, delta=0.01)
        self.assertAlmostEqual(result['hoa_von_du_lieu'], 4.80, delta=0.01)
        self.assertAlmostEqual(result['cps_9_co_dinh'], 12927.98, delta=0.01)
        self.assertAlmostEqual(result['cps_du_lieu_co_dinh'], 13599.69, delta=0.01)

    def test_multiple_ok_runs_do_not_double_count_a_reviewed_request(self):
        scope_ids = self.reqs.loc[self.reqs['loai'].isin(['noi_dia', 'hang_nang']), 'request_id']
        extra = self.runs.loc[self.runs['request_id'].isin(scope_ids)
                              & self.runs['status'].eq('ok')].iloc[[0]].copy()
        extra['attempt'] = 2
        extra_cost = float((extra['tokens_in'] * 26 / 1000
                            + extra['tokens_out'] * 130 / 1000
                            + extra['tool_calls'] * 15).sum())
        with redirect_stdout(io.StringIO()):
            changed = chay_nhiem_vu_b(pd.concat([self.runs, extra], ignore_index=True), self.reqs)
        self.assertEqual(changed['b4']['co_ok'], 948)
        self.assertAlmostEqual(changed['b4']['tong_9'] - self.result['b4']['tong_9'], extra_cost)

    def test_repeated_analysis_does_not_mutate_inputs(self):
        before_runs, before_reqs = self.runs.copy(deep=True), self.reqs.copy(deep=True)
        with redirect_stdout(io.StringIO()):
            chay_nhiem_vu_b(self.runs, self.reqs)
        pd.testing.assert_frame_equal(self.runs, before_runs)
        pd.testing.assert_frame_equal(self.reqs, before_reqs)

    def test_main_entrypoint_runs_both_a_and_b(self):
        completed = subprocess.run(
            [sys.executable, '-B', 'lab13.py'], cwd=self.folder,
            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'},
            capture_output=True, text=True, encoding='utf-8', check=True,
        )
        for marker in ('Ba phép thử đáp án biết trước: ĐẠT', 'A2 ·', 'A3 ·', 'A4 ·',
                       '=== B1', '=== B2', '=== B3', '=== B4', 'Ba yếu tố nhạy nhất'):
            with self.subTest(marker=marker):
                self.assertIn(marker, completed.stdout)
        self.assertNotIn('NotImplementedError', completed.stderr)


if __name__ == '__main__':
    unittest.main()
