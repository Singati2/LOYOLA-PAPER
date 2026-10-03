#!/usr/bin/env python3
"""EXPLORATORY, post hoc (added after review; not pre-registered).
Molecule-level uncertainty for the nested comparisons. For each dataset and
property, the outer leave-one-out predictions of GM and LO are computed for
every seed 0..99 at the given budget, and those of the ridge baseline once.
A paired bootstrap over molecules (B = 2000, rng seed 20261003) resamples the
molecules, recomputes Q^2 of every model on the resample, and takes the median
over seeds of dQ2(LO - GM); dQ2(LO - ridge) uses the median-over-seeds LO Q^2.
Reported: point value and 95% percentile interval.

Caveat: the bootstrap is conditional on the fitted outer predictions (model
selection is not repeated inside each resample), so it understates total
uncertainty; it captures which-molecules variability, which the seed sweep
does not.
Output: uncertainty_exploratory.csv
"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import baselines as B
from octane_data import OCTANES, PROPS, alkane_pairs

NB, RNG_SEED = 2000, 20261003


def datasets():
    P8 = [alkane_pairs(r[0]) for r in OCTANES]
    for k, p in enumerate(PROPS):
        yield "octane", p, P8, np.array([r[1 + k] for r in OCTANES])
    rows = list(csv.DictReader(open(os.path.join(HERE, "nonane_data.csv"))))
    for p, col in (("T_B", "T_B_C"), ("dHvap", "dHvap_kcal")):
        keep = [r for r in rows if r[col].strip()]
        yield "nonane", p, [alkane_pairs(r["smiles"]) for r in keep], np.array([float(r[col]) for r in keep])


def q2_rows(P, y):
    """Q^2 computed row-wise for prediction matrix P (models x n) against y[idx]."""
    return 1 - ((P - y) ** 2).sum(axis=1) / ((y - y.mean()) ** 2).sum()


def main():
    rng = np.random.default_rng(RNG_SEED)
    out = []
    for ds, prop, Pl, y in datasets():
        n = len(y)
        F = np.array([B.count_vector(P) for P in Pl], dtype=float)
        ridge_pred, _ = B.outer_loo(B.fold_ridge, F, y)
        for budget in (200, 500):
            G, L = [], []
            for seed in range(100):
                gm_t, lo_t = B.candidate_triples(seed, budget)
                G.append(B.outer_loo(B.fold_select_ols, B.descriptor_matrix(Pl, gm_t), y)[0])
                L.append(B.outer_loo(B.fold_select_ols, B.descriptor_matrix(Pl, lo_t), y)[0])
            G, L = np.array(G), np.array(L)
            def stats(idx):
                yy = y[idx]
                qg, ql = q2_rows(G[:, idx], yy), q2_rows(L[:, idx], yy)
                qr = q2_rows(ridge_pred[None, idx], yy)[0]
                return np.median(ql - qg), np.median(ql) - qr
            pt = stats(np.arange(n))
            boots = np.array([stats(rng.integers(0, n, n)) for _ in range(NB)])
            lo_gm = np.percentile(boots[:, 0], [2.5, 97.5]); lo_r = np.percentile(boots[:, 1], [2.5, 97.5])
            out.append([ds, prop, n, budget, f"{pt[0]:+.4f}", f"{lo_gm[0]:+.4f}", f"{lo_gm[1]:+.4f}",
                        f"{(boots[:,0] > 0).mean():.3f}", f"{pt[1]:+.4f}", f"{lo_r[0]:+.4f}", f"{lo_r[1]:+.4f}"])
            print(f"{ds:6s} {prop:6s} n={n:2d} B={budget}: dQ2(LO-GM) {pt[0]:+.3f} [{lo_gm[0]:+.3f},{lo_gm[1]:+.3f}]"
                  f"  P(>0)={(boots[:,0]>0).mean():.2f} | dQ2(LO-ridge) {pt[1]:+.3f} [{lo_r[0]:+.3f},{lo_r[1]:+.3f}]")
    with open(os.path.join(HERE, "uncertainty_exploratory.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "property", "n", "budget", "dQ2_LO_GM", "ci95_lo", "ci95_hi", "boot_frac_pos",
                    "dQ2_LO_ridge", "ci95_lo_ridge", "ci95_hi_ridge"])
        w.writerows(out)


if __name__ == "__main__":
    main()
