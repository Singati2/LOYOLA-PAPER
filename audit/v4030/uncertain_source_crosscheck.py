#!/usr/bin/env python3
"""Independent cross-check of uncertain_source_sensitivity.py (different code path, different libraries).

Subsets are rebuilt with pandas from the ledger; correlations come from scipy.stats.pearsonr on
degree pairs from a SMILES parser written here; the decane ridge Q2 comes from the scikit-learn
pipeline of audit/permutation_pipeline_audit.py (StandardScaler + Ridge, penalty by inner LeaveOneOut
over the same 41-value grid). Needs requirements-extras-lock.txt (pandas, scikit-learn).
  python3 audit/v4030/uncertain_source_crosscheck.py   -> uncertain_source_crosscheck_out.txt
"""
import os, re, sys
from collections import Counter
import numpy as np, pandas as pd
from scipy.stats import pearsonr
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [ROOT, os.path.join(ROOT, "audit")]
from octane_data import OCTANES, NAMES, PROPS

led = pd.read_csv(os.path.join(ROOT, "audit", "final", "scripts", "claim_provenance_ledger.csv"))
SC = {"broad": {"A", "B", "A-AGG", "B?"}, "strict": {"A", "B"}}
OUT = []
def say(s): print(s, flush=True); OUT.append(s)

def pairs(smi):
    deg, edges, stack, prev = [], [], [], None
    for ch in smi:
        if ch == "C":
            deg.append(0); c = len(deg) - 1
            if prev is not None: edges.append((prev, c)); deg[prev] += 1; deg[c] += 1
            prev = c
        elif ch == "(": stack.append(prev)
        elif ch == ")": prev = stack.pop()
    return [(deg[a], deg[b]) for a, b in edges]
def lo(P, a, b, g): return sum((i * j) ** a * (i + j) ** b * np.exp(g * abs(i - j) / (i + j)) for i, j in P)
PP = [pairs(r[0]) for r in OCTANES]
check = {("dHf", "strict"): ("mM2", (-1, 0, 0), "AG", (-0.5, 1, 0)), ("dHvap", "strict"): ("LO(0,0,1)", (0, 0, 1), "LO(0,0,2)", (0, 0, 2)),
         ("dHvap", "broad"): ("LO(0,0,1)", (0, 0, 1), "LO(0,0,2)", (0, 0, 2))}
for (prop, sc), (n1, t1, n2, t2) in check.items():
    k = PROPS.index(prop); sub = led[(led.dataset == "octane") & (led.property == prop) & led.tier.isin(SC[sc])]
    keep = [nm in set(sub.molecule) for nm in NAMES]; y = np.array([r[1 + k] for r, kp in zip(OCTANES, keep) if kp])
    x1 = [lo(p, *t1) for p, kp in zip(PP, keep) if kp]; x2 = [lo(p, *t2) for p, kp in zip(PP, keep) if kp]
    say(f"octane {prop} {sc}: n={len(y)}; |r| {n1} {abs(pearsonr(x1, y)[0]):.3f}, {n2} {abs(pearsonr(x2, y)[0]):.3f}")
for prop in PROPS:
    for sc in SC:
        say(f"octane {prop} {sc}: n={int(((led.dataset == 'octane') & (led.property == prop) & led.tier.isin(SC[sc])).sum())}")
bp = pd.read_csv(os.path.join(ROOT, "external", "bp", "bp_data.csv")).merge(
    led[led.dataset == "bp"][["molecule", "tier"]], left_on="name", right_on="molecule", how="left")
PAIRS = [(i, j) for i in range(1, 5) for j in range(i, 5)]
def F(df): return np.array([[Counter(tuple(int(t) for t in p.split("-")) for p in s.split())[q] for q in PAIRS] for s in df.degree_pairs], float)
# nested ridge rebuilt here from scikit-learn parts (not the audited baselines.fold_ridge): outer LeaveOneOut;
# inside each training fold StandardScaler + Ridge with the penalty chosen by GridSearchCV over
# np.logspace(-4, 4, 41) with an inner LeaveOneOut (first value on ties). Compared per molecule and per
# fold with the audited pipeline (baselines.outer_loo(fold_ridge)).
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, LeaveOneOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
sys.path.insert(0, os.path.join(ROOT, "external")); import baselines as BL
GRID = np.logspace(-4, 4, 41)
assert np.array_equal(GRID, BL.LAMBDA_GRID), "grids differ"
rows_cmp = []
assert bp.tier.notna().all() and not bp.name.duplicated().any(), "provenance join: unmatched or duplicate compounds"
for sc in ("original", "strict", "pooled original", "pooled strict"):
    d = {"original": bp[bp.n_C == 10], "strict": bp[(bp.n_C == 10) & bp.tier.isin(SC["strict"])],
         "pooled original": bp, "pooled strict": bp[bp.tier.isin(SC["strict"])]}[sc]
    Fm, yv = F(d), d.T_B_C.to_numpy(); pr = np.empty(len(yv)); lam = []
    for tr, te in LeaveOneOut().split(Fm):
        g = GridSearchCV(Pipeline([("s", StandardScaler()), ("r", Ridge())]), {"r__alpha": GRID}, cv=LeaveOneOut(),
                         scoring="neg_mean_squared_error", n_jobs=-1).fit(Fm[tr], yv[tr])
        pr[te] = g.predict(Fm[te]); lam.append(int(np.argmin(np.abs(GRID - g.best_params_["r__alpha"]))))
    ref, sel = BL.outer_loo(BL.fold_ridge, Fm, yv)
    q_sk = 1 - ((pr - yv) ** 2).sum() / ((yv - yv.mean()) ** 2).sum(); q_ref = 1 - ((ref - yv) ** 2).sum() / ((yv - yv.mean()) ** 2).sum()
    same_lam = sum(int(a == b) for a, b in zip(lam, sel))
    say(f"nested ridge ({sc}): n={len(yv)}; Q2 scikit-learn {q_sk:.6f}, audited {q_ref:.6f}; max |prediction difference| "
        f"{np.abs(pr - ref).max():.2e} degC; same penalty chosen in {same_lam} of {len(yv)} folds")
    rows_cmp.append([sc, len(yv), f"{q_sk:.6f}", f"{q_ref:.6f}", f"{np.abs(pr - ref).max():.3e}", f"{same_lam}/{len(yv)}"])
pd.DataFrame(rows_cmp, columns=["scenario", "n", "Q2_sklearn", "Q2_audited", "max_abs_pred_diff_C", "same_penalty_folds"]).to_csv(
    os.path.join(HERE, "sensitivity_ridge_crosscheck.csv"), index=False)
import subprocess
_g = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
print(f"commit {_g('rev-parse', 'HEAD')}; modified tracked files: {len([l for l in _g('status', '--porcelain', '--untracked-files=no').splitlines() if l])}")
say(f"pooled strict n={int(bp.tier.isin(SC['strict']).sum())}, broad n={int(bp.tier.isin(SC['broad']).sum())}")
open(os.path.join(HERE, "uncertain_source_crosscheck_out.txt"), "w").write("\n".join(OUT) + "\n")
