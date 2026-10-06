#!/usr/bin/env python3
"""Does the constancy test matter?  Every candidate triple actually drawn by
ablation_gm_vs_lo.py (rng 12345, budget 200) and by expanded_robustness_v35.py /
tmb_exclusion_sensitivity.py (seeds 0-99, budgets 200 and 500; LO triples and
gamma-zeroed GM pairs) is evaluated on the 18 octanes; on every outer training
fold (18-molecule and 17-molecule sets) the descriptor is tested with
  old:  range <= 1e-9 * max(1, max|x|)          (v35-v40.6 core scripts)
  new:  range <= 16 eps * max(max|x|, tiny)      (external/baselines.py; v40.7)
and with the inner-LOO degeneracy flags of the scripts.  Output:
constancy_test_check_out.txt (committed).  Runtime about one minute."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from octane_data import OCTANES, alkane_pairs, lo_pairs

OP = [alkane_pairs(r[0]) for r in OCTANES]; N = len(OP)
streams = []
rng = np.random.default_rng(12345)
streams.append(np.round(rng.uniform(-2, 2, (200, 3)), 3))
streams.append(np.column_stack([np.round(rng.uniform(-2, 2, (200, 2)), 3), np.zeros(200)]))
for seed in range(100):
    rng = np.random.default_rng(seed)
    for budget in (200, 500):
        streams.append(np.round(rng.uniform(-2, 2, (budget, 3)), 3))
        streams.append(np.column_stack([np.round(rng.uniform(-2, 2, (budget, 2)), 3), np.zeros(budget)]))
T = np.unique(np.vstack(streams), axis=0)
X = np.array([[lo_pairs(P, a, b, g) for P in OP] for a, b, g in T])
eps, tiny = np.finfo(float).eps, np.finfo(float).tiny
folds = [[k for k in range(N) if k != i] for i in range(N)]
idx = [k for k, r in enumerate(OCTANES) if "tetramethylbutane" not in r[0]]
folds += [[k for j, k in enumerate(idx) if j != i] for i in range(len(idx))]
old = new = degen = 0; minrel = np.inf
for m in folds:
    Xt = X[:, m]; rg = Xt.max(1) - Xt.min(1); sc = np.abs(Xt).max(1)
    old += int((rg <= 1e-9 * np.maximum(1.0, sc)).sum())
    new += int((rg <= 16 * eps * np.maximum(sc, tiny)).sum())
    minrel = min(minrel, float((rg / sc).min()))
    mm = Xt.shape[1]; Sx = Xt.sum(1, keepdims=True); Sxx = (Xt ** 2).sum(1, keepdims=True)
    Sx_j = Sx - Xt; Sxx_j = Sxx - Xt ** 2; denom = (mm - 1) * Sxx_j - Sx_j ** 2
    degen += int((denom <= 1e-12 * np.maximum(1.0, Sxx_j)).sum())
lines = [f"distinct candidate triples: {len(T)}",
         f"training folds examined: {len(folds)} (18 of 17 molecules, 17 of 16 molecules)",
         f"descriptors flagged constant, old test: {old}",
         f"descriptors flagged constant, new test: {new}",
         f"inner-LOO degeneracy flags (denom <= 1e-12 * max(1, Sxx)): {degen}",
         f"smallest relative range (max-min)/max|x| of any training-fold descriptor: {minrel:.3e}",
         "RESULT: " + ("the two constancy tests never disagree on these inputs; no fold is affected" if old == new == degen == 0 else "DIFFERENCES FOUND")]
print("\n".join(lines)); open(os.path.join(HERE, "constancy_test_check_out.txt"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if old == new == degen == 0 else 1)
