#!/usr/bin/env python3
"""Fast regression checks: python3 external/test_regressions.py."""
import tempfile
import sys
import shutil
import unittest
from pathlib import Path

import numpy as np
import baselines as B
from verify_external import csv_equal
sys.path.insert(0, str(Path(__file__).resolve().parent / "bp"))
import bp_tests as BP
import build_bp_data as BD
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "structural"))
import structural_checks as SC


class RegressionTests(unittest.TestCase):
    def test_extreme_descriptor_scales(self):
        x = np.arange(1., 11.)
        y = 2 * x + 3
        with np.errstate(all="raise"):
            for scale in (1., 1e-200, 1e200):
                with self.subTest(scale=scale):
                    self.assertFalse(B.is_constant(scale * x))
                    self.assertAlmostEqual(B.fit_predict(scale * x, y, scale * 11), 25.)
                    self.assertLess(B.inner_loo_rmse_all((scale * x)[None, :], y)[0], 1e-12)
                    self.assertEqual(B.fit_predict(np.full(10, scale), y, scale), y.mean())

    def test_large_translation(self):
        x = np.arange(1., 11.)
        y = 2 * x + 3
        self.assertFalse(B.is_constant(x + 1e13))
        self.assertAlmostEqual(B.fit_predict(x + 1e13, y, 11 + 1e13), 25.)

    def test_size_adjusted_press_rank_loss(self):
        z = np.arange(6.) + 6
        y = np.array([0., 1., 2., 4., 3., 9.])
        for x in (np.array([0., 0., 0., 0., 0., 1.]),):
            pred = []
            for i in range(len(y)):
                m = np.arange(len(y)) != i
                pred.append(BP.fit_pred_size(x[m], z[m], y[m], x[i], z[i]))
            expected = np.sqrt(np.mean((y - pred) ** 2))
            self.assertAlmostEqual(BP.press_size(x[None, :], z, y)[0], expected)
        for x in (z.copy(), np.ones(6)):
            self.assertTrue(np.isinf(BP.press_size(x[None, :], z, y)[0]))

    def test_size_adjusted_extreme_scales(self):
        x = np.array([0., 1., 4., 2., 8., 3.])
        z = np.arange(6.) + 6
        y = np.array([0., 1., 2., 4., 3., 9.])
        score = BP.press_size(x[None, :], z, y)[0]
        prediction = BP.fit_pred_size(x, z, y, 5., 12.)
        for scale in (1e-200, 1e200):
            self.assertAlmostEqual(BP.press_size((x * scale)[None, :], z, y)[0], score)
            self.assertAlmostEqual(BP.fit_pred_size(x * scale, z, y, 5. * scale, 12.), prediction)

    def test_missing_grouped_archive_fails(self):
        original = BD.HERE
        with tempfile.TemporaryDirectory() as td:
            shutil.copytree(original, Path(td) / "bp")
            BD.HERE = str(Path(td) / "bp")
            (Path(BD.HERE) / "nist_raw" / "C500006531.html").unlink()
            try:
                with self.assertRaisesRegex(FileNotFoundError, "C500006531"):
                    BD.main()
            finally:
                BD.HERE = original

    def test_empty_structural_certificate_fails(self):
        original = SC.RES
        SC.RES = {}
        try:
            with self.assertRaisesRegex(AssertionError, "at least one"):
                SC.s3_certify()
        finally:
            SC.RES = original

    def equal(self, a, b):
        with tempfile.TemporaryDirectory() as td:
            pa, pb = Path(td) / "a.csv", Path(td) / "b.csv"
            pa.write_text(a); pb.write_text(b)
            return csv_equal(pa, pb)

    def test_known_results_tolerate_roundoff(self):
        self.assertTrue(self.equal("Q2\n0.1234567890\n", "Q2\n0.1234567891\n"))
        self.assertFalse(self.equal("Q2\n0.1234\n", "Q2\n0.1244\n"))

    def test_parameters_data_and_unknown_columns_are_exact(self):
        for col in ("seed", "budget", "alpha", "beta", "gamma", "selection",
                    "n", "T_B_C", "value_used", "conditions", "future_parameter"):
            with self.subTest(column=col):
                self.assertFalse(self.equal(f"{col}\n1.0000000000\n", f"{col}\n1.0000000001\n"))
        self.assertFalse(self.equal("Q2\n1\n", "Q2\n1.0000000001\n"))

    def test_nonfinite_values_cannot_use_tolerance(self):
        self.assertFalse(self.equal("Q2\ninf\n", "Q2\nInfinity\n"))
        self.assertFalse(self.equal("Q2\nnan\n", "Q2\nNaN\n"))
        self.assertTrue(self.equal("r_pred\nnan\n", "r_pred\nnan\n"))

    def test_malformed_csv_fails_closed(self):
        for contents in ("", "\n", "Q2,Q2\n1,1\n", "Q2,RMSE\n0.1\n"):
            with self.subTest(contents=contents):
                self.assertFalse(self.equal(contents, contents))
        self.assertFalse(self.equal("Q2\n0.1\n", "RMSE\n0.1\n"))
        self.assertFalse(self.equal("Q2\n0.1\n", "Q2\n0.1\n0.1\n"))


if __name__ == "__main__":
    unittest.main()
