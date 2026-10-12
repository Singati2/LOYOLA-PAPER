#!/usr/bin/env python3
"""Fast regression checks: python3 external/test_regressions.py."""
import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import baselines as B
from verify_external import csv_equal
sys.path.insert(0, str(Path(__file__).resolve().parent / "bp"))
import build_bp_data as BD
import bp_tests as BP
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
        """A candidate whose deletion makes the design rank-deficient (leverage 1)
        is rejected rather than scored by the residual/(1-h) identity, which is
        invalid there; an ordinary candidate keeps its closed-form score."""
        z = np.arange(6.) + 6
        y = np.array([0., 1., 2., 4., 3., 9.])
        x = np.array([0., 0., 0., 0., 0., 1.])
        self.assertTrue(np.isinf(BP.press_size(x[None, :], z, y)[0]))
        for x in (z.copy(), np.ones(6)):      # collinear with n_C or constant: rejected
            self.assertTrue(np.isinf(BP.press_size(x[None, :], z, y)[0]))
        x = np.array([0., 1., 4., 2., 8., 3.])
        pred = []
        for i in range(len(y)):
            m = np.arange(len(y)) != i
            pred.append(BP.fit_pred_size(x[m], z[m], y[m], x[i], z[i]))
        self.assertAlmostEqual(BP.press_size(x[None, :], z, y)[0], np.sqrt(np.mean((y - pred) ** 2)))

    def test_size_adjusted_extreme_scales(self):
        x = np.array([0., 1., 4., 2., 8., 3.])
        z = np.arange(6.) + 6
        y = np.array([0., 1., 2., 4., 3., 9.])
        score = BP.press_size(x[None, :], z, y)[0]
        prediction = BP.fit_pred_size(x, z, y, 5., 12.)
        for scale in (1e-200, 1e200):
            self.assertAlmostEqual(BP.press_size((x * scale)[None, :], z, y)[0], score)
            self.assertAlmostEqual(BP.fit_pred_size(x * scale, z, y, 5. * scale, 12.), prediction)

    def test_selection_translation_invariance(self):
        """OLS with an intercept is translation invariant; the selection guard must not reject a
        well-resolved candidate after a large constant is added (v40.29; formerly an expected failure)."""
        x = np.arange(1., 11.)
        y = 2 * x + 3
        p0 = B.fold_select_ols(x[None, :], y, 0)[0]
        for c in (1e6, 1e10, 1e12, 1e13):
            with self.subTest(offset=c):
                self.assertAlmostEqual(B.fold_select_ols((x + c)[None, :], y, 0)[0], p0, places=6)

    def test_rounding_noise_rejected(self):
        """A constant carrying rounding jitter of up to 512 ulps is degenerate at every magnitude,
        and a candidate with fewer than 1024 resolvable steps after a translation is degenerate too."""
        k = np.array([-512., 512., 0., 3., -7., 100., -300., 1., 64., -64.])
        for c in (1e-300, 1e-8, 1., 7., 1e8, 1e300):
            with self.subTest(c=c):
                self.assertTrue(B.degenerate_rows((c * (1 + k * np.finfo(float).eps / 2))[None, :])[0])
        self.assertTrue(B.degenerate_rows((np.arange(1., 11.) + 1e15)[None, :])[0])

    def test_small_relative_range_accepted(self):
        """Small relative range is not degeneracy when the values are resolved: 1 + 1e-10 s keeps
        about a million steps and was wrongly rejected by the v40.22 floor of 1e-9."""
        s = np.log(np.arange(2., 12.))
        for x in (1 + 1e-10 * s, 1e-200 * s, 1e200 * s, s + 1e10):
            self.assertFalse(B.degenerate_rows(x[None, :])[0])

    def test_press_size_near_collinear(self):
        """A candidate nearly collinear with n_C is either rejected or scored accurately: the
        inner-LOO RMSE agrees with a 60-digit reference to 1e-6 whenever it is finite (v40.29)."""
        import mpmath as mp
        mp.mp.dps = 60
        rng = np.random.default_rng(0)
        n = 20; z = np.arange(6, 6 + n) % 5 + 6.0; y = rng.normal(size=n) + z
        for e in (1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9):
            x = z + e * rng.normal(size=n)
            r = BP.press_size(x[None, :], z, y)[0]
            if not np.isfinite(r):
                continue
            X = [[1, zi, xi] for zi, xi in zip(z, x)]; s = 0
            for i in range(n):
                A = mp.matrix([X[k] for k in range(n) if k != i]); b = mp.matrix([y[k] for k in range(n) if k != i])
                beta = mp.lu_solve(A.T * A, A.T * b)
                s += (sum(beta[j] * X[i][j] for j in range(3)) - y[i]) ** 2
            with self.subTest(noise=e):
                self.assertAlmostEqual(r / float(mp.sqrt(s / n)), 1.0, places=6)

    def test_size_refit_translation(self):
        """The final size-adjusted refit is invariant to translating n_C and the new point together
        (v40.29; a shift of 1e8 formerly changed the prediction)."""
        z = np.arange(6.) + 6; x = z + 1e-3 * np.array([0., 1., 4., 2., 8., 3.]); y = np.array([0., 1., 2., 4., 3., 9.])
        p0 = BP.fit_pred_size(x, z, y, 12 + 1e-3, 12.)
        for c in (1e4, 1e8):
            with self.subTest(shift=c):
                self.assertAlmostEqual(BP.fit_pred_size(x, z + c, y, 12 + 1e-3, 12. + c), p0, places=5)

    def test_inchi_parser_rejects_repeats(self):
        """The alkane InChI parser rejects repeated atoms and bonds (v40.29)."""
        sys.path.insert(0, str(Path(__file__).resolve().parent / "bp"))
        import build_bp_data as BB
        with self.assertRaises(ValueError):
            BB.inchi_tree("InChI=1S/C3H8/c1-2-1-2-3", 3)
        self.assertEqual(BB.inchi_tree("InChI=1S/C6H14/c1-5(2)6(3)4", 6).number_of_edges(), 5)

    def test_press_probe_fails_closed(self):
        """The press_size probe passes on its committed output and fails on every disallowed
        diagnostic: rejection, band, selection change, leverage-1, non-finite QR, QR
        disagreement above 1e-8, non-finite deviation, or an unreproduced published output."""
        import re
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "audit" / "final" / "scripts"))
        import press_size_probe as PP
        out = (Path(PP.__file__).resolve().parent / "press_size_probe_out.txt").read_text()
        n = lambda pat: float(re.search(pat, out).group(1))
        S = {"calls": n(r"calls (\d+)"), "candidates": n(r"candidates (\d+)"), "rej_1e6": n(r"at 1e-6: (\d+)"),
             "rej_1e10": n(r"at 1e-10: (\d+);"), "band": n(r"1e-6\): (\d+)"), "argmin_changes": n(r"argmin: (\d+)"),
             "argmin_changes_if_1e10": n(r"\(at 1e-10: (\d+)\)"), "rank_reject_leverage": n(r"candidates: (\d+)$"),
             "max_rel_vs_qr": n(r"relative difference ([\d.e+-]+)"), "max_abs_vs_qr": n(r"max absolute ([\d.e+-]+)"),
             "nonfinite_qr": 0}
        rs, rb = "summary.csv: True" in out, "baselines.csv: True" in out
        self.assertEqual(PP.verdict(S, rs, rb), [])
        bad = [("rej_1e6", 1), ("rej_1e10", 1), ("band", 1), ("argmin_changes", 1), ("argmin_changes_if_1e10", 1),
               ("rank_reject_leverage", 1), ("nonfinite_qr", 1), ("max_rel_vs_qr", 2e-8), ("max_rel_vs_qr", float("nan")),
               ("max_abs_vs_qr", float("inf")), ("calls", 0)]
        for k, v in bad:
            self.assertTrue(PP.verdict(dict(S, **{k: v}), rs, rb), k)
        self.assertTrue(PP.verdict(S, False, rb)); self.assertTrue(PP.verdict(S, rs, False))

    def test_gamma_rule_one_sided(self):
        """The pre-registered rule needs the whole interval above zero; a wholly
        negative or zero-crossing interval never gives a gamma effect."""
        self.assertTrue(BP.gamma_adds_value(40, (0.001, 0.02), 0.01))
        self.assertFalse(BP.gamma_adds_value(40, (-0.02, -0.001), 0.01))
        self.assertFalse(BP.gamma_adds_value(40, (-0.001, 0.02), 0.01))
        self.assertFalse(BP.gamma_adds_value(39, (0.001, 0.02), 0.01))
        self.assertFalse(BP.gamma_adds_value(40, (0.001, 0.02), 0.0))

    def test_header_only_csv_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            a, b = Path(td) / "a.csv", Path(td) / "b.csv"
            a.write_text("x,y\n"); b.write_text("x,y\n")
            self.assertFalse(csv_equal(a, b))

    def test_nan_candidate_never_selected(self):
        X = np.array([[np.nan] * 6, [0., 1., 4., 2., 8., 3.]])
        y = np.array([0., 1., 2., 4., 3., 9.])
        orig = B.inner_loo_rmse_all
        try:
            B.inner_loo_rmse_all = lambda Xt, yt: np.array([np.nan, 1.0])
            pred, k = B.fold_select_ols(X, y, 0)
        finally:
            B.inner_loo_rmse_all = orig
        self.assertEqual(k, 1); self.assertTrue(np.isfinite(pred))

    def test_missing_grouped_archive_fails(self):
        """A missing archived NIST page must stop the boiling-point data build
        (skipping it silently admitted 3-ethyl-4-methylhexane: 101 molecules)."""
        original = BD.HERE
        with tempfile.TemporaryDirectory() as td:
            shutil.copytree(original, Path(td) / "bp")
            BD.HERE = str(Path(td) / "bp")
            (Path(BD.HERE) / "nist_raw" / "C500006531.html").unlink()
            try:
                with self.assertRaisesRegex(FileNotFoundError, "C500006531"), contextlib.redirect_stdout(io.StringIO()):
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
