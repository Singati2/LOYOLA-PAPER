#!/usr/bin/env python3
"""Inclusion sensitivity for 2,2,3,3-tetramethylbutane (TMB) in the
vaporization-enthalpy experiment.

TMB is a solid at 298 K (triple point 373.97 K). Its tabulated benchmark
value (8.41 kcal/mol) is a 298 K liquid-reference value taken from the
standard octane benchmark compilation; it does not equal either standard
vaporization enthalpy listed by NIST (42.94, 42.91 kJ/mol). Because the
physical reference state of that cell cannot be matched to a primary
determination, the full nested GM-vs-LO comparison for dHvap is repeated
with TMB excluded (17 isomers), over the same seeds 0..99 and budgets
{200, 500}, with the same candidate convention as expanded_robustness_v35.py
(rng = default_rng(seed); LO triples U(-2,2) rounded 3 dp drawn first,
then GM pairs; paired control = LO candidates with gamma zeroed).

Outputs (next to this script):
  dhvap_tmb_exclusion_v36.csv          seed,budget,Q2_GM,Q2_LO,dQ2,Q2_LOzero,dQ2_paired
  dhvap_tmb_exclusion_summary_v36.csv  budget,n_seeds,LO_better,LO_worse,
                                       paired_better,paired_worse,dQ2_min,dQ2_median,dQ2_max
"""
import csv, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from octane_data import OCTANES, NAMES, alkane_pairs, lo_pairs, PROPS

HERE = os.path.dirname(os.path.abspath(__file__))
KEEP = [i for i, nm in enumerate(NAMES) if nm != "2,2,3,3-tetramethylbutane"]
assert len(KEEP) == 17
OP = [alkane_pairs(OCTANES[i][0]) for i in KEEP]
Y = np.array([OCTANES[i][1 + PROPS.index("dHvap")] for i in KEEP])
N = len(KEEP)


def descriptor_matrix(triples):
    return np.array([[lo_pairs(P, a, b, g) for P in OP] for a, b, g in triples])


def is_constant(x):
    """Constant at double precision: range within 16 ulp of the largest
    magnitude (same resolution-based test as external/baselines.py)."""
    x = np.asarray(x, float)
    scale = max(float(np.abs(x).max()), np.finfo(float).tiny)
    return (x.max() - x.min()) <= 16 * np.finfo(float).eps * scale


def inner_loo_rmse_all(Xt, yt):
    # Degeneracy threshold (denom <= 1e-12 * max(1, Sxx)) is inert on these data:
    # no training-fold descriptor of any candidate stream has relative range
    # below 2.4e-4 (constancy_test_check.py, output committed).
    m = Xt.shape[1] - 1
    Sx = Xt.sum(axis=1, keepdims=True); Sxx = (Xt**2).sum(axis=1, keepdims=True)
    Sxy = (Xt * yt).sum(axis=1, keepdims=True); Sy = yt.sum()
    Sx_j, Sxx_j, Sxy_j, Sy_j = Sx - Xt, Sxx - Xt**2, Sxy - Xt * yt, Sy - yt
    denom = m * Sxx_j - Sx_j**2
    degen = denom <= 1e-12 * np.maximum(1.0, Sxx_j)
    slope = (m * Sxy_j - Sx_j * Sy_j) / np.where(degen, 1.0, denom)
    pred = np.where(degen, Sy_j / m, Sy_j / m + slope * (Xt - Sx_j / m))
    return np.sqrt(((pred - yt) ** 2).mean(axis=1))


def fit_predict(xt, yt, xnew):
    if is_constant(xt):
        return float(yt.mean())
    xm, ym = xt.mean(), yt.mean()
    return float(ym + ((xt - xm) * (yt - ym)).sum() / ((xt - xm) ** 2).sum() * (xnew - xm))


def nested_q2(X, y):
    preds = np.empty(N)
    for i in range(N):
        mask = np.ones(N, bool); mask[i] = False
        k = int(np.argmin(inner_loo_rmse_all(X[:, mask], y[mask])))
        preds[i] = fit_predict(X[k, mask], y[mask], X[k, i])
    return 1 - ((preds - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def main():
    rows = []
    for seed in range(100):
        for budget in (200, 500):
            rng = np.random.default_rng(seed)
            lo_t = np.round(rng.uniform(-2, 2, (budget, 3)), 3)
            gm_p = np.round(rng.uniform(-2, 2, (budget, 2)), 3)
            gm_t = np.column_stack([gm_p, np.zeros(budget)])
            lz_t = np.column_stack([lo_t[:, :2], np.zeros(budget)])
            q_lo, q_gm, q_lz = (nested_q2(descriptor_matrix(t), Y) for t in (lo_t, gm_t, lz_t))
            rows.append((seed, budget, q_gm, q_lo, q_lo - q_gm, q_lz, q_lo - q_lz))
    with open(os.path.join(HERE, "dhvap_tmb_exclusion_v36.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["seed", "budget", "Q2_GM", "Q2_LO", "dQ2", "Q2_LOzero", "dQ2_paired"])
        for r in rows:
            w.writerow([r[0], r[1]] + [f"{v:+.10f}" for v in r[2:]])
    with open(os.path.join(HERE, "dhvap_tmb_exclusion_summary_v36.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["budget", "n_seeds", "LO_better", "LO_worse", "paired_better",
                    "paired_worse", "dQ2_min", "dQ2_median", "dQ2_max"])
        for budget in (200, 500):
            d = np.array([r[4] for r in rows if r[1] == budget])
            dp = np.array([r[6] for r in rows if r[1] == budget])
            w.writerow([budget, len(d), int((d > 0).sum()), int((d <= 0).sum()),
                        int((dp > 0).sum()), int((dp <= 0).sum()),
                        f"{d.min():+.10f}", f"{np.median(d):+.10f}", f"{d.max():+.10f}"])
    print("wrote dhvap_tmb_exclusion_v36.csv and dhvap_tmb_exclusion_summary_v36.csv")


if __name__ == "__main__":
    main()
