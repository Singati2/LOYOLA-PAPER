#!/usr/bin/env python3
"""Independent re-implementation of the decane ridge permutation check (Section 6.4).

The paper's pipeline (external/baselines.py fold_ridge, structural/structural_checks.py S7)
is rebuilt from scikit-learn parts: Pipeline(StandardScaler, Ridge) with the penalty chosen
by GridSearchCV over the same 41-value grid with an inner LeaveOneOut on the training fold
only, inside an outer LeaveOneOut.  The same 200 permutations (rng default_rng(20261005),
permuting the boiling points only) are rerun.  Leakage checks: scaling and penalty selection
see only training molecules of each outer fold.

  python3 audit/permutation_pipeline_audit.py     (about 30-60 minutes; not part of the replay harness)

Output: audit/permutation_pipeline_audit_out.txt (committed).  Exit 1 if the observed Q2 or
any permutation summary differs from structural/structural_checks_out.txt by more than 1e-3.
"""
import csv, os, re, sys
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.model_selection import GridSearchCV, LeaveOneOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "external")); sys.path.insert(0, ROOT)
import baselines as B

GRID = np.logspace(-4, 4, 41)


def nested_q2(F, y):
    preds = np.empty(len(y))
    for tr, te in LeaveOneOut().split(F):
        gs = GridSearchCV(Pipeline([("s", StandardScaler()), ("r", Ridge())]), {"r__alpha": GRID},
                          cv=LeaveOneOut(), scoring="neg_mean_squared_error", n_jobs=-1)
        gs.fit(F[tr], y[tr]); preds[te] = gs.predict(F[te])
    return 1 - ((preds - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def main():
    rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "external", "bp", "bp_data.csv"))) if r["n_C"] == "10"]
    P = [[tuple(map(int, x.split("-"))) for x in r["degree_pairs"].split()] for r in rows]
    y = np.array([float(r["T_B_C"]) for r in rows])
    F = np.array([B.count_vector(p) for p in P], float)
    F = F[:, F.std(axis=0) > 1e-12]                     # the paper drops zero-variance columns inside each fit
    real = nested_q2(F, y)
    rng = np.random.default_rng(20261005); q = []
    for _ in range(200):
        yp = rng.permutation(y); q.append(nested_q2(F, yp))
    q = np.array(q); ge = int((q >= real).sum())
    ref = open(os.path.join(ROOT, "structural", "structural_checks_out.txt")).read()
    m = re.search(r"S7 decane ridge Q2 ([-\d.]+); permuted \(200\): median ([-\d.]+), 95th pct ([-\d.]+), max ([-\d.]+)", ref)
    want = [float(x) for x in m.groups()]
    got = [real, float(np.median(q)), float(np.percentile(q, 95)), float(q.max())]
    lines = [f"independent (scikit-learn) nested ridge on {len(y)} decanes: Q2 {got[0]:.4f}",
             f"200 permutations: median {got[1]:.4f}, 95th pct {got[2]:.4f}, max {got[3]:.4f}; >= observed: {ge}; p = {(ge + 1) / 201:.4f}",
             f"paper pipeline (structural_checks_out.txt S7): Q2 {want[0]:.4f}, median {want[1]:.4f}, 95th pct {want[2]:.4f}, max {want[3]:.4f}"]
    ok = all(abs(a - b) <= 1e-3 for a, b in zip(got, want))
    lines.append("RESULT: " + ("independent re-implementation reproduces the paper pipeline" if ok else "MISMATCH with the paper pipeline"))
    open(os.path.join(ROOT, "audit", "permutation_pipeline_audit_out.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
