#!/usr/bin/env python3
"""Expanded robustness of the matched-budget nested GM-vs-LO ablation:
seeds 0..99 x budgets {200, 500}, all five properties, plus a paired
same-alpha/beta control (LO candidates (a,b,g) vs the SAME candidates with
gamma zeroed) that isolates gamma from the independent-stream effect.

Candidate convention identical to ablation_gm_vs_lo.py / ablation_robustness.py:
rng = default_rng(seed); LO triples U(-2,2)^(budget x 3) rounded 3dp drawn
FIRST, then GM pairs U(-2,2)^(budget x 2) rounded 3dp, gamma=0.

Outputs (next to this script):
  expanded_robustness_v35.csv  (seed,budget,property,Q2_GM,Q2_LO,dQ2,
                                Q2_LOzero,dQ2_paired)
  expanded_robustness_summary_v35.csv (budget,property,n_seeds,
                                LO_better,LO_worse, paired_better,paired_worse,
                                dQ2_min,dQ2_median,dQ2_max)
Runtime ~2-4 minutes.
"""
import csv, math, os
import numpy as np
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from octane_data import OCTANES, alkane_pairs, lo_pairs, PROPS

HERE = os.path.dirname(os.path.abspath(__file__))
N = 18
OP = [alkane_pairs(r[0]) for r in OCTANES]
Y = {p: np.array([r[1+i] for r in OCTANES]) for i, p in enumerate(PROPS)}

def descriptor_matrix(triples):
    X = np.empty((len(triples), N))
    for k, (a, b, g) in enumerate(triples):
        X[k] = [lo_pairs(Pr, a, b, g) for Pr in OP]
    return X

def is_constant(x):
    return (x.max() - x.min()) <= 1e-9 * max(1.0, float(np.abs(x).max()))

def inner_loo_rmse_all(Xt, yt):
    C, n = Xt.shape
    m = n - 1
    Sx  = Xt.sum(axis=1, keepdims=True)
    Sxx = (Xt**2).sum(axis=1, keepdims=True)
    Sxy = (Xt * yt).sum(axis=1, keepdims=True)
    Sy  = yt.sum()
    Sx_j, Sxx_j, Sxy_j = Sx - Xt, Sxx - Xt**2, Sxy - Xt * yt
    Sy_j = Sy - yt
    denom = m * Sxx_j - Sx_j**2
    degen = denom <= 1e-12 * np.maximum(1.0, Sxx_j)
    slope = (m * Sxy_j - Sx_j * Sy_j) / np.where(degen, 1.0, denom)
    pred = Sy_j / m + slope * (Xt - Sx_j / m)
    pred = np.where(degen, Sy_j / m, pred)
    return np.sqrt(((pred - yt) ** 2).mean(axis=1))

def fit_predict(xt, yt, xnew):
    if is_constant(xt):
        return float(yt.mean())
    xm, ym = xt.mean(), yt.mean()
    b = ((xt - xm) * (yt - ym)).sum() / ((xt - xm) ** 2).sum()
    return float(ym + b * (xnew - xm))

def nested_q2(X, y):
    preds = np.empty(N)
    for i in range(N):
        mask = np.ones(N, bool); mask[i] = False
        Xt, yt = X[:, mask], y[mask]
        k = int(np.argmin(inner_loo_rmse_all(Xt, yt)))
        preds[i] = fit_predict(Xt[k], yt, X[k, i])
    return 1 - ((preds - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()

def main():
    rows = []
    for seed in range(100):
        for budget in (200, 500):
            rng = np.random.default_rng(seed)
            lo_t = np.round(rng.uniform(-2, 2, (budget, 3)), 3)
            gm_p = np.round(rng.uniform(-2, 2, (budget, 2)), 3)
            gm_t = np.column_stack([gm_p, np.zeros(budget)])
            lz_t = np.column_stack([lo_t[:, :2], np.zeros(budget)])  # paired control
            X_lo, X_gm, X_lz = (descriptor_matrix(t) for t in (lo_t, gm_t, lz_t))
            for p in PROPS:
                y = Y[p]
                q_gm, q_lo, q_lz = nested_q2(X_gm, y), nested_q2(X_lo, y), nested_q2(X_lz, y)
                rows.append([seed, budget, p, f"{q_gm:.10f}", f"{q_lo:.10f}",
                             f"{q_lo-q_gm:+.10f}", f"{q_lz:.10f}", f"{q_lo-q_lz:+.10f}"])
    with open(os.path.join(HERE, "expanded_robustness_v35.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seed", "budget", "property", "Q2_GM", "Q2_LO", "dQ2",
                    "Q2_LOzero", "dQ2_paired"])
        for r in rows: w.writerow(r)
    with open(os.path.join(HERE, "expanded_robustness_summary_v35.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["budget", "property", "n_seeds", "LO_better", "LO_worse",
                    "paired_better", "paired_worse", "dQ2_min", "dQ2_median", "dQ2_max"])
        for budget in (200, 500):
            for p in PROPS:
                d = [float(r[5]) for r in rows if r[1] == budget and r[2] == p]
                dp = [float(r[7]) for r in rows if r[1] == budget and r[2] == p]
                w.writerow([budget, p, len(d),
                            sum(1 for x in d if x > 0), sum(1 for x in d if x < 0),
                            sum(1 for x in dp if x > 0), sum(1 for x in dp if x < 0),
                            f"{min(d):+.10f}", f"{float(np.median(d)):+.10f}", f"{max(d):+.10f}"])
    print("wrote expanded_robustness_v35.csv (1000 rows) + summary")

if __name__ == "__main__":
    main()
