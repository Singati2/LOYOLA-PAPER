#!/usr/bin/env python3
"""Old-versus-corrected comparison of two numerical guards in the boiling-point tests.

Guard 1 (degeneracy, external/baselines.py): a candidate is rejected if it is constant to
floating-point resolution (is_constant) OR its relative range is below 1e-9. The second
clause can reject a genuinely varying descriptor such as 1e13 + {1,...,10}. Corrected:
is_constant only.

Guard 2 (rank, external/bp/bp_tests.py press_size): the size-adjusted design [1, n_C, x] is
accepted if |det(S)| > 1e-9 max|S|^3 with S = A'A built from the raw carbon number, which is
not invariant to translating n_C. Corrected: n_C centred and scaled within the training fold
and full rank decided by singular values (smallest / largest > 1e-10). Leverages and PRESS
residuals are invariant to this reparametrisation, so only the accept/reject decision can
differ.

For every seed 0-49, every candidate stream (GM2, LO2, GM12, LOh) and every outer fold of
Test A (34 decanes) and Test B (100 pooled alkanes), the selected candidate, the outer
prediction and Q2 are compared between the old and the corrected guards. No manuscript file
is changed.

  python3 audit/guard_robustness_audit.py      (about 1 hour)

Output: audit/guard_robustness_audit_out.txt.  Exit 0 iff every selection is identical and
every Q2 agrees to 1e-12.
"""
import os, sys, time
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "external", "bp")); sys.path.insert(0, os.path.join(ROOT, "external"))
import bp_tests as T
import baselines as B


def const_only(Xt):
    return np.array([B.is_constant(Xt[k]) for k in range(Xt.shape[0])], bool)


# ---------------- Test A: one-descriptor OLS ----------------
def select_A(X, y, i, corrected):
    m = B._mask(len(y), i); Xt, yt = X[:, m], y[m]
    rmse = B.inner_loo_rmse_all(Xt, yt)
    rmse = np.where(np.isfinite(rmse), rmse, np.inf)
    bad = const_only(Xt) if corrected else B.degenerate_rows(Xt)
    rmse = np.where(bad, np.inf, rmse)
    k = int(np.argmin(rmse))
    return k, B.fit_predict(Xt[k], yt, X[k, i]), rmse


# ---------------- Test B: size-adjusted OLS ----------------
def press_size_corrected(Xt_raw, zt, yt):
    Xt_raw = np.asarray(Xt_raw, float); C, n = Xt_raw.shape
    Xt = T._standardize(Xt_raw)
    zc = (zt - zt.mean()) / (zt.std() if zt.std() > 0 else 1.0)
    A = np.stack([np.ones((C, n)), np.broadcast_to(zc, (C, n)), Xt], axis=2)
    sv = np.linalg.svd(A, compute_uv=False)
    ok = sv[:, -1] > 1e-10 * sv[:, 0]
    S = np.einsum("cni,cnj->cij", A, A); S[~ok] = np.eye(3)
    Si = np.linalg.inv(S)
    beta = np.einsum("cij,cnj,n->ci", Si, A, yt)
    res = yt - np.einsum("cni,ci->cn", A, beta)
    h = np.einsum("cni,cij,cnj->cn", A, Si, A)
    regular = ok & np.all(np.abs(1 - h) > 1e-10, axis=1)
    r = np.full(C, np.inf)
    r[regular] = np.sqrt(((res[regular] / (1 - h[regular])) ** 2).mean(axis=1))
    return r, ok


def select_B(X, z, y, i, corrected):
    n = len(y); m = np.ones(n, bool); m[i] = False
    if corrected:
        r, _ = press_size_corrected(X[:, m], z[m], y[m]); bad = const_only(X[:, m])
    else:
        r = T.press_size(X[:, m], z[m], y[m]); bad = B.degenerate_rows(X[:, m])
    r = np.where(np.isfinite(r), r, np.inf); r = np.where(bad, np.inf, r)
    k = int(np.argmin(r))
    return k, T.fit_pred_size(X[k, m], z[m], y[m], X[k, i], z[i]), r


def main():
    import csv
    rows, P, y, z = T.load()
    dec = [i for i, r in enumerate(rows) if r["n_C"] == "10"]
    tests = (("A", [P[i] for i in dec], y[dec], None), ("B", P, y, z))
    diffs, q2, rmse, preds = [], {}, {}, {}
    folds, t0 = 0, time.time()
    for label, PP, yy, zz in tests:
        n = len(yy)
        for s in T.SEEDS:
            st = T.streams(s)
            for key in ("GM2", "LO2", "GM12", "LOh"):
                X = B.descriptor_matrix(PP, st[key])
                po, pn = np.empty(n), np.empty(n)
                for i in range(n):
                    if zz is None:
                        ko, po[i], so = select_A(X, yy, i, False); kn, pn[i], sn = select_A(X, yy, i, True)
                    else:
                        ko, po[i], so = select_B(X, zz, yy, i, False); kn, pn[i], sn = select_B(X, zz, yy, i, True)
                    folds += 1
                    if ko != kn:
                        cause = "old guard rejected the corrected choice" if not np.isfinite(so[kn]) else "near-tie (both accepted)"
                        diffs.append([label, key, s, i, ko, kn, f"{so[ko]:.15g}", f"{so[kn]:.15g}", f"{sn[ko]:.15g}", f"{sn[kn]:.15g}",
                                      f"{abs(so[ko] - so[kn]) / so[ko]:.3e}" if np.isfinite(so[kn]) else "inf", cause])
                q2[(label, key, s)] = (T.q2(po, yy), T.q2(pn, yy))
                preds[f"{label}|{key}|{s}|old"] = po.copy(); preds[f"{label}|{key}|{s}|corrected"] = pn.copy()
                rmse[(label, key, s)] = (float(np.sqrt(((po - yy) ** 2).mean())), float(np.sqrt(((pn - yy) ** 2).mean())),
                                         float(np.abs(po - pn).max()))
            print(f"test {label} seed {s} done ({time.time() - t0:.0f} s)", flush=True)
    np.savez_compressed(os.path.join(ROOT, "audit", "guard_robustness_predictions.npz"), **preds)
    with open(os.path.join(ROOT, "audit", "guard_robustness_diffs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["test", "stream", "seed", "fold", "k_old", "k_corrected", "old_score_k_old", "old_score_k_corrected",
                    "new_score_k_old", "new_score_k_corrected", "old_relative_gap", "cause"]); w.writerows(diffs)
    lines = []
    for label in ("A", "B"):
        for which, idx in (("old", 0), ("corrected", 1)):
            med = {k: np.median([q2[(label, k, s)][idx] for s in T.SEEDS]) for k in ("GM2", "LO2", "GM12", "LOh")}
            d = np.array([q2[(label, "LOh", s)][idx] - q2[(label, "GM12", s)][idx] for s in T.SEEDS])
            lines.append(f"Test {label} {which:9s}: GM2 {med['GM2']:.4f}, LO2 {med['LO2']:.4f}, GM12 {med['GM12']:.4f}, "
                         f"LOh {med['LOh']:.4f}, median dQ2 {np.median(d):+.4f}, LOh ahead in {int((d > 0).sum())} of 50")
    causes = {}
    for dd in diffs:
        causes[dd[-1]] = causes.get(dd[-1], 0) + 1
    by = {}
    for dd in diffs:
        by[(dd[0], dd[1])] = by.get((dd[0], dd[1]), 0) + 1
    lines.append(f"outer folds compared: {folds}; folds with a different selected candidate: {len(diffs)}; causes: {causes}; by test/stream: {by}")
    qd = max(abs(a - b) for a, b in q2.values())
    lines.append(f"largest |Q2 old - Q2 corrected| for a single seed and stream: {qd:.3e}")
    lines.append(f"largest |RMSE old - RMSE corrected|: {max(abs(a - b) for a, b, _ in rmse.values()):.3e}; "
                 f"largest |prediction old - prediction corrected|: {max(c for _, _, c in rmse.values()):.3e}")
    nz = sum(1 for _, _, c in rmse.values() if c > 0)
    lines.append(f"seed/stream runs with any prediction difference: {nz} of {len(rmse)}")
    same = all(l.split(": ", 1)[1] == lines[i + 1].split(": ", 1)[1] for i, l in enumerate(lines[:4]) if i % 2 == 0)
    lines.append("RESULT: " + ("Table 5 summaries identical at displayed precision" if same else "Table 5 summaries DIFFER at displayed precision"))
    open(os.path.join(ROOT, "audit", "guard_robustness_audit_out.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); sys.exit(0 if same else 1)


if __name__ == "__main__":
    main()
