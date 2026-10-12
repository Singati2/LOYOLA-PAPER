#!/usr/bin/env python3
"""Does the constancy test matter?  Every candidate triple actually drawn by
ablation_gm_vs_lo.py (rng 12345, budget 200) and by expanded_robustness_v35.py /
tmb_exclusion_sensitivity.py (seeds 0-99, budgets 200 and 500; LO triples and
gamma-zeroed GM pairs, and the paired LO-zero controls (LO's own alpha, beta with gamma = 0))
is evaluated on the 18 octanes; on every outer training
fold (18-molecule and 17-molecule sets) the descriptor is tested with
  old:  range <= 1e-9 * max(1, max|x|)          (v35-v40.6 core scripts)
  new:  range <= 16 eps * max(max|x|, tiny)      (external/baselines.py; v40.7)
and with the inner-LOO degeneracy flags of the scripts.  v40.30: the streams are taken from the
production generator external/baselines.candidate_triples (one fresh rng per seed and budget), and
the script fails unless the sampling lines of the three generators are still the ones mirrored here
(the former version drew budget 500 from the same rng after budget 200, so most budget-500 triples
were not the ones the experiments use, and it omitted the LO-zero controls).  Output:
constancy_test_check_out.txt (committed).  Runtime about one minute."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from octane_data import OCTANES, NAMES, alkane_pairs, lo_pairs

OP = [alkane_pairs(r[0]) for r in OCTANES]; N = len(OP)
sys.path.insert(0, os.path.join(HERE, "external"))
import baselines as B

# The generators must still draw exactly as candidate_triples does: fail closed if their sampling lines change.
SAMPLING = {
    "expanded_robustness_v35.py": ["rng = np.random.default_rng(seed)", "lo_t = np.round(rng.uniform(-2, 2, (budget, 3)), 3)",
                                   "gm_p = np.round(rng.uniform(-2, 2, (budget, 2)), 3)", "lz_t = np.column_stack([lo_t[:, :2], np.zeros(budget)])"],
    "tmb_exclusion_sensitivity.py": ["rng = np.random.default_rng(seed)", "lo_t = np.round(rng.uniform(-2, 2, (budget, 3)), 3)",
                                     "gm_p = np.round(rng.uniform(-2, 2, (budget, 2)), 3)", "lz_t = np.column_stack([lo_t[:, :2], np.zeros(budget)])"],
    "ablation_gm_vs_lo.py": ["rng = np.random.default_rng(12345)", "LO_TRIPLES = np.round(rng.uniform(-2, 2, size=(200, 3)), 3)",
                             "GM_PAIRS   = np.round(rng.uniform(-2, 2, size=(200, 2)), 3)"],
}
for fn, needles in SAMPLING.items():
    src = open(os.path.join(HERE, fn)).read()
    missing = [t for t in needles if t not in src]
    assert not missing, f"{fn}: sampling code changed, update this check: {missing}"
streams = []
for seed, budget in [(s, b) for s in range(100) for b in (200, 500)] + [(12345, 200)]:
    gm_t, lo_t = B.candidate_triples(seed, budget)
    streams += [lo_t, gm_t, np.column_stack([lo_t[:, :2], np.zeros(budget)])]
T = np.unique(np.vstack(streams), axis=0)
X = np.array([[lo_pairs(P, a, b, g) for P in OP] for a, b, g in T])
eps, tiny = np.finfo(float).eps, np.finfo(float).tiny
folds = [[k for k in range(N) if k != i] for i in range(N)]
idx = [k for k, nm in enumerate(NAMES) if nm != "2,2,3,3-tetramethylbutane"]   # v40.12: was tested on the SMILES string, so it excluded nothing
assert len(idx) == 17
folds += [[k for j, k in enumerate(idx) if j != i] for i in range(len(idx))]
old = new = cur = degen = 0; minrel = np.inf
for m in folds:
    Xt = X[:, m]; rg = Xt.max(1) - Xt.min(1); sc = np.abs(Xt).max(1)
    old += int((rg <= 1e-9 * np.maximum(1.0, sc)).sum())
    new += int((rg <= 16 * eps * np.maximum(sc, tiny)).sum())
    cur += int(B.degenerate_rows(Xt).sum())              # current guard of fold_select_ols (v40.29)
    minrel = min(minrel, float((rg / sc).min()))
    mm = Xt.shape[1]; Sx = Xt.sum(1, keepdims=True); Sxx = (Xt ** 2).sum(1, keepdims=True)
    Sx_j = Sx - Xt; Sxx_j = Sxx - Xt ** 2; denom = (mm - 1) * Sxx_j - Sx_j ** 2
    degen += int((denom <= 1e-12 * np.maximum(1.0, Sxx_j)).sum())
lines = [f"distinct candidate triples: {len(T)}",
         f"training folds examined: {len(folds)} (18 of 17 molecules, 17 of 16 molecules)",
         f"descriptors flagged constant, old test: {old}",
         f"descriptors flagged constant, new test: {new}",
         f"descriptors flagged degenerate, current resolution guard (1024 eps): {cur}",
         f"inner-LOO degeneracy flags (denom <= 1e-12 * max(1, Sxx)): {degen}",
         f"smallest relative range (max-min)/max|x| of any training-fold descriptor: {minrel:.3e}",
         "RESULT: " + ("the two constancy tests never disagree on these inputs; no fold is affected" if old == new == cur == degen == 0 else "DIFFERENCES FOUND")]
print("\n".join(lines)); open(os.path.join(HERE, "constancy_test_check_out.txt"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if old == new == cur == degen == 0 else 1)
