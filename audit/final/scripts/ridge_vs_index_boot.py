"""EXPLORATORY (audit only): conditional molecule bootstrap of Q2(ridge) - median_seeds Q2(GM12 / LOh),
same construction as bp_tests.boot_ci (2000 resamples, rng 20261005); GM12/LOh predictions from
branch robustness-guards (corrected guards, which equal the v40.28 pipeline for GM12/LOh)."""
import sys, numpy as np
ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))))
sys.path.insert(0, __import__("os").path.join(ROOT, "external")); sys.path.insert(0, __import__("os").path.join(ROOT, "external", "bp"))
import baselines as B, bp_tests as T
d = np.load("gr_preds.npz")
rows, P, y, z = T.load()
dec = [i for i, r in enumerate(rows) if r["n_C"] == "10"]
for lab, idx in (("A", dec), ("B", list(range(len(y))))):
    yy = y[idx]; F = np.array([B.count_vector(P[i]) for i in idx], float)
    R = B.outer_loo(B.fold_ridge, F, yy)[0]
    q = lambda p, t: 1 - ((p - t) ** 2).sum(-1) / ((t - t.mean()) ** 2).sum()
    for k in ("GM12", "LOh"):
        M = np.array([d[f"{lab}|{k}|{s}|corrected"] for s in range(50)])
        pt = q(R, yy) - np.median(q(M, yy))
        rng = np.random.default_rng(20261005); st = []
        for _ in range(2000):
            b = rng.integers(0, len(yy), len(yy)); t = yy[b]
            st.append(q(R[b], t) - np.median(q(M[:, b], t)))
        lo, hi = np.percentile(st, [2.5, 97.5])
        print(f"Test {lab}: Q2 ridge {q(R, yy):.4f}; ridge - median {k} = {pt:+.4f}, 95% conditional bootstrap [{lo:+.4f}, {hi:+.4f}]")
