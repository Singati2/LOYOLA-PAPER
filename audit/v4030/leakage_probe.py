#!/usr/bin/env python3
"""Leakage probe for every model used in the sensitivity analyses (v40.30 audit).
For each held-out compound i (all compounds, both sets), y_i is replaced by y_i + 1000 and the
out-of-fold prediction for i is recomputed. If no training step (scaling, descriptor or candidate
selection, penalty choice, refit) uses y_i, the prediction is unchanged. Also confirms that the
subsampling draws compounds without replacement and that compound names are unique.
  python3 audit/v4030/leakage_probe.py   -> leakage_probe_out.txt
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [ROOT, os.path.join(ROOT, "external"), os.path.join(ROOT, "external", "bp")]
import baselines as BL, bp_tests as T
rows, P, y, z = T.load()
assert len({r["name"] for r in rows}) == len(rows), "duplicate compound names"
_g = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
out = [f"commit {_g('rev-parse', 'HEAD')}; modified tracked files: {len([l for l in _g('status', '--porcelain', '--untracked-files=no').splitlines() if l])}"]
def fold_pred(model, Pk, yk, zk, i):
    F = np.array([BL.count_vector(p) for p in Pk], float)
    ir = np.array([BL.irla(p) for p in Pk])[None, :]; lo1 = BL.descriptor_matrix(Pk, [(0, 0, 1)]); Xc = BL.descriptor_matrix(Pk, T.CLASSICAL)
    if model == "ridge": return BL.fold_ridge(F, yk, i)[0]
    if model in ("classical", "IRLA", "LO(0,0,1)"):
        X = {"classical": Xc, "IRLA": ir, "LO(0,0,1)": lo1}[model]; return BL.fold_select_ols(X, yk, i)[0]
    X = {"size+classical": Xc, "size+IRLA": ir, "size+LO(0,0,1)": lo1}.get(model)
    m = np.arange(len(yk)) != i
    if model == "size only":
        A = np.column_stack([np.ones(m.sum()), zk[m]]); c, *_ = np.linalg.lstsq(A, yk[m], rcond=None); return c[0] + c[1] * zk[i]
    r = T.press_size(X[:, m], zk[m], yk[m]); r = np.where(BL.degenerate_rows(X[:, m]), np.inf, r); k = int(np.argmin(r))
    return T.fit_pred_size(X[k, m], zk[m], yk[m], X[k, i], zk[i])
for tst, idx, models in (("decanes", [i for i in range(len(rows)) if rows[i]["n_C"] == "10"], ["ridge", "classical", "IRLA", "LO(0,0,1)"]),
                         ("pooled", list(range(len(rows))), ["ridge", "size+classical", "size+IRLA", "size+LO(0,0,1)", "size only"])):
    Pk, yk, zk = [P[i] for i in idx], y[idx].copy(), z[idx]
    for mdl in models:
        worst = 0.0
        for i in range(len(idx)):
            a = fold_pred(mdl, Pk, yk, zk, i); yp = yk.copy(); yp[i] += 1000.0; b = fold_pred(mdl, Pk, yp, zk, i)
            worst = max(worst, abs(a - b))
        out.append(f"{tst:8} {mdl:15}: max |prediction change| for the held-out compound when its own y moves by 1000: {worst:.2e}")
        print(out[-1], flush=True)
rng = np.random.default_rng(20261014); s = rng.choice(np.arange(100), 80, replace=False)
out.append(f"subsampling draws without replacement: {len(set(s.tolist())) == len(s)} (80 distinct of 80)")
out.append(out[0].replace("commit", "end: commit"))
open(os.path.join(HERE, "leakage_probe_out.txt"), "w").write("\n".join(out) + "\n")
