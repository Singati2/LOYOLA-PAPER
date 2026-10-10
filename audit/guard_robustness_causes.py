#!/usr/bin/env python3
"""Cause-by-cause analysis of the folds where the old and corrected guards select different
candidates (run after audit/guard_robustness_audit.py).

For every differing fold:
  * guard 1 only (degeneracy corrected, rank guard old) and guard 2 only (rank guard corrected,
    degeneracy old) are rerun, to attribute the change;
  * a stable reference decides which of the two candidates is genuinely better: the inner
    leave-one-out RMSE is recomputed by explicit refits with numpy.linalg.lstsq (QR/SVD based,
    no normal equations) on the standardised design.
Then the Table 5 quantities, the 95% molecule-bootstrap intervals (bp_tests.boot_ci, rng
20261005) and the pre-registered decisions are recomputed from the old and from the corrected
predictions.

  python3 audit/guard_robustness_causes.py

Output: audit/guard_robustness_causes_out.txt and audit/guard_robustness_causes.csv.
"""
import csv, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "audit"))
import guard_robustness_audit as G
T, B = G.T, G.B


def ref_inner_rmse(x, z, y):
    """Inner-LOO RMSE of y ~ 1 (+ z) + x by explicit lstsq refits on the standardised design."""
    n = len(y); err = np.empty(n)
    for j in range(n):
        m = np.ones(n, bool); m[j] = False
        xs = (x - x[m].mean()) / (x[m].std() or 1.0)
        cols = [np.ones(n), xs] if z is None else [np.ones(n), (z - z[m].mean()) / (z[m].std() or 1.0), xs]
        A = np.column_stack(cols)
        coef, _, rank, _ = np.linalg.lstsq(A[m], y[m], rcond=None)
        err[j] = A[j] @ coef - y[j]
    return float(np.sqrt((err ** 2).mean()))


def select_variant(X, z, y, i, rank_corrected, degeneracy_corrected):
    n = len(y); m = np.ones(n, bool); m[i] = False; Xt = X[:, m]
    if z is None:
        r = B.inner_loo_rmse_all(Xt, y[m])
    else:
        r = G.press_size_corrected(Xt, z[m], y[m])[0] if rank_corrected else T.press_size(Xt, z[m], y[m])
    r = np.where(np.isfinite(r), r, np.inf)
    bad = G.const_only(Xt) if degeneracy_corrected else B.degenerate_rows(Xt)
    return int(np.argmin(np.where(bad, np.inf, r)))


def main():
    rows, P, y, z = T.load()
    dec = [i for i, r in enumerate(rows) if r["n_C"] == "10"]
    data = {"A": ([P[i] for i in dec], y[dec], None), "B": (P, y, z)}
    diffs = list(csv.DictReader(open(os.path.join(ROOT, "audit", "guard_robustness_diffs.csv"))))
    out, cache = [], {}
    for d in diffs:
        label, key, s, i = d["test"], d["stream"], int(d["seed"]), int(d["fold"])
        PP, yy, zz = data[label]
        if (label, key, s) not in cache:
            cache = {(label, key, s): B.descriptor_matrix(PP, T.streams(s)[key])}
        X = cache[(label, key, s)]
        ko, kc = int(d["k_old"]), int(d["k_corrected"])
        k1 = select_variant(X, zz, yy, i, False, True)
        k2 = select_variant(X, zz, yy, i, True, False)
        cause = ("guard 1 (degeneracy)" if k1 == kc and k2 == ko else "guard 2 (rank)" if k2 == kc and k1 == ko
                 else "both" if k1 == kc and k2 == kc else "neither guard alone: score rounding")
        m = np.ones(len(yy), bool); m[i] = False
        zt = None if zz is None else zz[m]
        ro = ref_inner_rmse(X[ko, m], zt, yy[m]); rc = ref_inner_rmse(X[kc, m], zt, yy[m])
        better = "tie" if abs(ro - rc) <= 1e-12 * max(ro, rc) else ("corrected" if rc < ro else "old")
        out.append([label, key, s, i, ko, kc, cause, f"{ro:.15g}", f"{rc:.15g}", f"{abs(ro - rc) / max(ro, rc):.3e}", better])
    with open(os.path.join(ROOT, "audit", "guard_robustness_causes.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["test", "stream", "seed", "fold", "k_old", "k_corrected", "cause", "ref_rmse_old_choice",
                    "ref_rmse_corrected_choice", "ref_relative_gap", "reference_prefers"]); w.writerows(out)
    lines = [f"differing folds: {len(out)}"]
    for field, idx in (("cause", 6), ("reference prefers", 10)):
        c = {}
        for o in out:
            c[o[idx]] = c.get(o[idx], 0) + 1
        lines.append(f"{field}: {c}")
    gaps = [float(o[9]) for o in out]
    if gaps:
        lines.append(f"reference relative RMSE gap between the two choices: median {np.median(gaps):.2e}, max {max(gaps):.2e}")
    pr = np.load(os.path.join(ROOT, "audit", "guard_robustness_predictions.npz"))
    for label in ("A", "B"):
        _, yy, _ = data[label]
        for which in ("old", "corrected"):
            g = np.array([pr[f"{label}|GM12|{s}|{which}"] for s in T.SEEDS]); l = np.array([pr[f"{label}|LOh|{s}|{which}"] for s in T.SEEDS])
            q = {k: np.median([T.q2(pr[f"{label}|{k}|{s}|{which}"], yy) for s in T.SEEDS]) for k in ("GM2", "LO2", "GM12", "LOh")}
            dq = np.array([T.q2(a, yy) - T.q2(b, yy) for a, b in zip(l, g)])
            ci = T.boot_ci(g, l, yy, np.random.default_rng(20261005))
            wins = int((dq > 0).sum())
            verdict = "gamma adds value" if (wins >= 40 and (ci[0] > 0 or ci[1] < 0) and np.median(dq) > 0) else "no evidence that gamma adds value"
            lines.append(f"Test {label} {which:9s}: GM {q['GM12']:.3f}, LO_h {q['LOh']:.3f}, median dQ2 {np.median(dq):+.3f}, "
                         f"LO_h ahead {wins}/50, 95% CI [{ci[0]:+.3f}, {ci[1]:+.3f}], narrow box GM {q['GM2']:.3f} / LO {q['LO2']:.3f}; {verdict}")
    open(os.path.join(ROOT, "audit", "guard_robustness_causes_out.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
