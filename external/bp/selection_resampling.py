#!/usr/bin/env python3
"""Selection-aware resampling for the two pre-registered boiling-point tests
(exploratory, added after the results; not part of PREREG_v40.md).

The bootstrap interval of bp_tests.py resamples molecules from FIXED outer
predictions, so it omits refitting and parameter-selection uncertainty.  Here
each replicate r draws a subsample of round(0.8 n) molecules without
replacement (rng default_rng(20261008 + r)) and a fresh candidate stream
(bp_tests.streams(r)), and reruns the WHOLE fully nested leave-one-out
procedure for GM12 and LOh on the subsample: selection, refit and prediction.
The statistic is dQ2 = Q2(LOh) - Q2(GM12) on that subsample.

  python3 external/bp/selection_resampling.py [R_A] [R_B]   (defaults 500, 200: the run reported in the paper)

Outputs: selection_resampling.csv (one row per replicate) and
selection_resampling_summary.csv.
"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bp_tests as T
B = T.B


def one(P, y, z, idx, seed):
    st = T.streams(seed); Ps = [P[i] for i in idx]; ys = y[idx]; zs = None if z is None else z[idx]
    q = {}
    for k in ("GM12", "LOh"):
        X = B.descriptor_matrix(Ps, st[k])
        p = T.nested_size(X, zs, ys) if zs is not None else B.outer_loo(B.fold_select_ols, X, ys)[0]
        q[k] = T.q2(p, ys)
    return q["GM12"], q["LOh"]


def main():
    RA = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    RB = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rows, P, y, z = T.load()
    dec = [i for i, r in enumerate(rows) if r["n_C"] == "10"]
    tests = (("A: decane T_B", [P[i] for i in dec], y[dec], None, RA),
             ("B: pooled C6-C10 T_B (size-adjusted)", P, y, z, RB))
    out, summ = [], []
    for label, PP, yy, zz, R in tests:
        n = len(yy); m = int(round(0.8 * n)); d = []
        for r in range(R):
            idx = np.sort(np.random.default_rng(20261008 + r).choice(n, m, replace=False))
            g, l = one(PP, yy, zz, idx, r)
            out.append([label, r, m, f"{g:.10f}", f"{l:.10f}", f"{l - g:+.10f}"]); d.append(l - g)
        d = np.array(d)
        s = [label, R, m, f"{np.median(d):+.4f}", f"{np.percentile(d, 2.5):+.4f}", f"{np.percentile(d, 97.5):+.4f}", int((d > 0).sum())]
        summ.append(s); print(s, flush=True)
    with open(os.path.join(HERE, "selection_resampling.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["test", "replicate", "n_sub", "Q2_GM12", "Q2_LOh", "dQ2"]); w.writerows(out)
    with open(os.path.join(HERE, "selection_resampling_summary.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["test", "replicates", "n_sub", "median_dQ2", "p2.5", "p97.5", "LOh_better"]); w.writerows(summ)


if __name__ == "__main__":
    main()
