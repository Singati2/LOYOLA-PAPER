#!/usr/bin/env python3
"""EXPLORATORY (not pre-registered; added after an external review asked
whether an octane-trained model transfers). For each seed 0..99 and budget
200/500, the GM and LO candidate with the smallest leave-one-out RMSE on all 18
octanes is selected (same candidate stream as the main analysis) and FROZEN.
On the nonanes:
  (a) parameter transfer: theta frozen, the one-descriptor OLS refitted by
      leave-one-out on the nonanes -> Q2_transfer_refit;
  (b) unchanged model: theta AND the octane OLS coefficients frozen, applied
      to the nonanes -> Q2_transfer_frozen (expected to suffer from the size
      shift between C8 and C9: the descriptor and property levels differ).
Outputs transfer_exploratory.csv (per seed) and transfer_exploratory_summary.csv.
"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import baselines as B
from octane_data import OCTANES, PROPS, alkane_pairs

P8 = [alkane_pairs(r[0]) for r in OCTANES]
ROWS9 = list(csv.DictReader(open(os.path.join(HERE, "nonane_data.csv"))))
PAIRS = (("T_B", "T_B_C"), ("dHvap", "dHvap_kcal"))


def q2(pred, y):
    return 1 - ((pred - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def loo_refit_q2(x, y):
    preds = np.array([B.fit_predict(np.delete(x, i), np.delete(y, i), x[i]) for i in range(len(y))])
    return q2(preds, y)


def main():
    out = []
    for prop, col in PAIRS:
        y8 = np.array([r[1 + PROPS.index(prop)] for r in OCTANES])
        keep = [r for r in ROWS9 if r[col].strip()]
        P9 = [alkane_pairs(r["smiles"]) for r in keep]
        y9 = np.array([float(r[col]) for r in keep])
        for seed in range(100):
            for b in (200, 500):
                gm_t, lo_t = B.candidate_triples(seed, b)
                for model, T in (("GM", gm_t), ("LO", lo_t)):
                    X8 = B.descriptor_matrix(P8, T)
                    k = int(np.argmin(B.inner_loo_rmse_all(X8, y8)))
                    x8 = X8[k]; th = T[k]
                    x9 = B.descriptor_matrix(P9, [th])[0]
                    slope, icpt = np.polyfit(x8, y8, 1)
                    out.append([prop, model, seed, b, *[f"{v:.3f}" for v in th],
                                f"{loo_refit_q2(x9, y9):+.10f}", f"{q2(slope * x9 + icpt, y9):+.10f}"])
    with open(os.path.join(HERE, "transfer_exploratory.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["property", "model", "seed", "budget", "alpha", "beta", "gamma",
                                       "Q2_transfer_refit", "Q2_transfer_frozen"]); w.writerows(out)
    summ = []
    for prop, _ in PAIRS:
        for b in (200, 500):
            g = {m: np.array([[float(r[7]), float(r[8])] for r in out if r[0] == prop and r[1] == m and r[3] == b]) for m in ("GM", "LO")}
            better = int((g["LO"][:, 0] > g["GM"][:, 0]).sum())
            summ.append([prop, b, f"{np.median(g['GM'][:,0]):+.4f}", f"{np.median(g['LO'][:,0]):+.4f}", better,
                         f"{np.median(g['GM'][:,1]):+.4f}", f"{np.median(g['LO'][:,1]):+.4f}"])
            print(f"{prop:6s} B={b}: refit Q2 median GM {summ[-1][2]} LO {summ[-1][3]} (LO better {better}/100) | frozen Q2 median GM {summ[-1][5]} LO {summ[-1][6]}")
    with open(os.path.join(HERE, "transfer_exploratory_summary.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["property", "budget", "median_Q2_refit_GM", "median_Q2_refit_LO", "LO_better_refit",
                                       "median_Q2_frozen_GM", "median_Q2_frozen_LO"]); w.writerows(summ)


if __name__ == "__main__":
    main()
