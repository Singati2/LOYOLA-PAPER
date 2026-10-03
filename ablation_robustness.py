#!/usr/bin/env python3
"""Robustness of the matched-budget nested GM-vs-LO ablation to the random
candidate stream and budget: seeds {12345, 777, 2024} x budgets {200, 500}.
Same fully nested design as ablation_gm_vs_lo.py (LO triples drawn first,
then GM pairs, per seed). Writes ablation_robustness.csv next to this script.
Runtime ~3-5 minutes.
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

def nested_q2(prop, cands):
    y = Y[prop]
    X = np.array([[lo_pairs(P, *c) for P in OP] for c in cands])
    preds = np.empty(N)
    for i in range(N):
        m = np.ones(N, bool); m[i] = False
        best = (None, np.inf)
        for k in range(len(cands)):
            x = X[k][m]; yt = y[m]; errs = []
            for j in range(17):
                mm = np.ones(17, bool); mm[j] = False
                xt, ytt = x[mm], yt[mm]
                if xt.std() == 0:
                    pr = ytt.mean()
                else:
                    b = ((xt-xt.mean())*(ytt-ytt.mean())).sum()/((xt-xt.mean())**2).sum()
                    pr = (ytt.mean()-b*xt.mean())+b*x[j]
                errs.append((pr-yt[j])**2)
            r = math.sqrt(np.mean(errs))
            if r < best[1]-1e-15: best = (k, r)
        k = best[0]; x = X[k][m]; yt = y[m]
        if x.std() == 0:
            preds[i] = yt.mean()
        else:
            b = ((x-x.mean())*(yt-yt.mean())).sum()/((x-x.mean())**2).sum()
            preds[i] = (yt.mean()-b*x.mean())+b*X[k][i]
    return 1-((preds-y)**2).sum()/((y-y.mean())**2).sum()

def main():
    rows = []
    for seed in (12345, 777, 2024):
        for budget in (200, 500):
            rng = np.random.default_rng(seed)
            lo_c = [tuple(v) for v in np.round(rng.uniform(-2, 2, (budget, 3)), 3)]
            gm_c = [(a, b, 0.0) for a, b in np.round(rng.uniform(-2, 2, (budget, 2)), 3)]
            for p in PROPS:
                qg = nested_q2(p, gm_c); ql = nested_q2(p, lo_c)
                rows.append([seed, budget, p, f"{qg:.10f}", f"{ql:.10f}", f"{ql-qg:+.10f}"])
    with open(os.path.join(HERE, "ablation_robustness.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["seed", "budget", "property", "Q2_GM", "Q2_LO", "dQ2"])
        for r in rows: w.writerow(r)
    print("wrote ablation_robustness.csv,", len(rows), "rows")

if __name__ == "__main__":
    main()
