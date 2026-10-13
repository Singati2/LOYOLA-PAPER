#!/usr/bin/env python3
"""Feature-side leakage probe (v40.30 audit). Evidence, not an exhaustive proof.
For every held-out compound i, its descriptor column (counts for ridge; candidate descriptors for
the single-index and size-adjusted models; n_C too for the size models) is replaced by extreme values
(x1000 and shifted by 1e6), and the model chosen inside fold i is recomputed: the ridge penalty
index, the selected descriptor (fold_select_ols), or the selected candidate (size-adjusted PRESS).
Unchanged choices show that no feature-dependent step of the selection (standardisation, rescaling,
degeneracy guard, penalty or candidate choice) uses the held-out compound's features. It checks the
chosen model only, not the fitted coefficients, and it cannot rule out leakage paths it does not
exercise; the descriptors themselves are computed per molecule from its structure alone.
  python3 audit/v4030/feature_leakage_probe.py   -> feature_leakage_probe_out.txt
"""
import os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path[:0] = [ROOT, os.path.join(ROOT, "external"), os.path.join(ROOT, "external", "bp")]
import baselines as BL, bp_tests as T
rows, P, y, z = T.load()
_g = lambda *a: subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()
STAMP = f"commit {_g('rev-parse', 'HEAD')}; modified tracked files: {len([l for l in _g('status', '--porcelain', '--untracked-files=no').splitlines() if l])}"
print(STAMP)  # freeze stamp: printed, not written, so the output file can be replayed on any commit
out = []
def corrupt(v): return v * 1000.0 + 1e6
for tst, idx in (("decanes", [i for i in range(len(rows)) if rows[i]["n_C"] == "10"]), ("pooled", list(range(len(rows))))):
    Pk, yk, zk = [P[i] for i in idx], y[idx], z[idx]; n = len(idx)
    F = np.array([BL.count_vector(p) for p in Pk], float)
    cands = {"classical": BL.descriptor_matrix(Pk, T.CLASSICAL), "IRLA": np.array([BL.irla(p) for p in Pk])[None, :],
             "LO(0,0,1)": BL.descriptor_matrix(Pk, [(0, 0, 1)])}
    ch = {"ridge": 0, **{f"ols {k}": 0 for k in cands}, **({f"size {k}": 0 for k in cands} if tst == "pooled" else {})}
    for i in range(n):
        F2 = F.copy(); F2[i] = corrupt(F2[i])
        ch["ridge"] += int(BL.fold_ridge(F, yk, i)[1] != BL.fold_ridge(F2, yk, i)[1])
        for k, X in cands.items():
            X2 = X.copy(); X2[:, i] = corrupt(X2[:, i])
            ch[f"ols {k}"] += int(BL.fold_select_ols(X, yk, i)[1] != BL.fold_select_ols(X2, yk, i)[1])
            if tst == "pooled":
                m = np.arange(n) != i
                pick = lambda XX, zz: int(np.argmin(np.where(BL.degenerate_rows(XX[:, m]), np.inf, T.press_size(XX[:, m], zz[m], yk[m]))))
                z2 = zk.copy(); z2[i] = corrupt(z2[i])
                ch[f"size {k}"] += int(pick(X, zk) != pick(X2, z2))
    for k, v in ch.items():
        out.append(f"{tst:8} {k:16}: folds whose chosen model changed when the held-out compound's features were corrupted: {v}/{n}")
        print(out[-1], flush=True)
print("end: " + STAMP)
open(os.path.join(HERE, "feature_leakage_probe_out.txt"), "w").write("\n".join(out) + "\n")
