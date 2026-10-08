#!/usr/bin/env python3
"""Diagnostics quoted in the changelog, now scripted (v40.2):
D1  Test-B solver: press_size vs a stable lstsq reference on 5 seeds x 600
    wide-box candidates (rejections, max relative error, argmin agreement).
D2  one-descriptor path: at every selected candidate of 3 seeds x 2 streams
    (400 wide-box candidates each) over all outer folds of all 8 datasets,
    inner RMSE and held-out prediction vs a stable reference.
D3  dense parent grids for octane/nonane dHvap at half-widths 2, 4, 8, 12:
    nested Q2 and the number of outer folds whose selection lies within one
    grid step of the box boundary (shows the box of half-width 2 binds).
Writes wide_box_diagnostics_out.txt."""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(HERE, "bp"))
import baselines as B
import bp_tests as T
from octane_data import OCTANES, PROPS, alkane_pairs
OUT = []
def log(*a):
    s = " ".join(map(str, a)); print(s, flush=True); OUT.append(s)
def stable_rmse(x, y):
    n = len(y); e = []
    for i in range(n):
        m = np.ones(n, bool); m[i] = False; sd = x[m].std() or 1.0
        A = np.column_stack([np.ones(m.sum()), (x[m] - x[m].mean()) / sd]); c, *_ = np.linalg.lstsq(A, y[m], rcond=None)
        e.append(c[0] + c[1] * (x[i] - x[m].mean()) / sd - y[i])
    return np.sqrt(np.mean(np.square(e)))
def stable_pred(xt, yt, xn):
    sd = xt.std() or 1.0; A = np.column_stack([np.ones(len(xt)), (xt - xt.mean()) / sd]); c, *_ = np.linalg.lstsq(A, yt, rcond=None)
    return c[0] + c[1] * (xn - xt.mean()) / sd
def stable_size(x, z, y):
    n = len(y); e = []
    for i in range(n):
        m = np.ones(n, bool); m[i] = False; sd = x[m].std() or 1.0
        A = np.column_stack([np.ones(m.sum()), z[m], (x[m] - x[m].mean()) / sd]); c, *_ = np.linalg.lstsq(A, y[m], rcond=None)
        e.append(c[0] + c[1] * z[i] + c[2] * (x[i] - x[m].mean()) / sd - y[i])
    return np.sqrt(np.mean(np.square(e)))
def datasets():
    P8 = [alkane_pairs(r[0]) for r in OCTANES]
    for k, p in enumerate(PROPS): yield f"octane {p}", P8, np.array([r[1 + k] for r in OCTANES])
    rows = list(csv.DictReader(open(os.path.join(HERE, "nonane_data.csv"))))
    for p, col in (("T_B", "T_B_C"), ("dHvap", "dHvap_kcal")):
        kk = [r for r in rows if r[col].strip()]; yield f"nonane {p}", [alkane_pairs(r["smiles"]) for r in kk], np.array([float(r[col]) for r in kk])
    bp = [r for r in csv.DictReader(open(os.path.join(HERE, "bp", "bp_data.csv"))) if r["n_C"] == "10"]
    yield "decane T_B", [[tuple(map(int, e.split("-"))) for e in r["degree_pairs"].split()] for r in bp], np.array([float(r["T_B_C"]) for r in bp])
def d1():
    rows, P, y, z = T.load(); rej = 0; worst = 0; agree = 0
    for seed in range(5):
        rng = np.random.default_rng(seed)
        for T_ in (np.column_stack([np.round(rng.uniform(-12, 12, (300, 2)), 3), np.zeros(300)]), np.round(np.column_stack([rng.uniform(-12, 12, (300, 2)), rng.uniform(-2, 2, 300)]), 3)):
            X = B.descriptor_matrix(P, T_); fast = T.press_size(X, z, y); rej += int(np.isinf(fast).sum())
            ref = np.array([stable_size(X[k], z, y) for k in range(300)])
            worst = max(worst, float(np.max(np.abs(fast - ref) / ref))); agree += int(np.argmin(fast)) == int(np.argmin(ref))
    log(f"D1 Test-B solver: rejected {rej} of 3000 candidates, max rel error {worst:.2e}, argmin agreement {agree}/10")
def d2():
    wr = wp = 0; tot = 0
    for name, P, y in datasets():
        for seed in range(3):
            rng = np.random.default_rng(seed)
            for T_ in (np.column_stack([np.round(rng.uniform(-12, 12, (400, 2)), 3), np.zeros(400)]), np.round(np.column_stack([rng.uniform(-12, 12, (400, 2)), rng.uniform(-2, 2, 400)]), 3)):
                X = B.descriptor_matrix(P, T_)
                for i in range(len(y)):
                    m = np.ones(len(y), bool); m[i] = False
                    fa = B.inner_loo_rmse_all(X[:, m], y[m]); k = int(np.argmin(fa)); tot += 1
                    sr = stable_rmse(X[k, m], y[m]); wr = max(wr, abs(fa[k] - sr) / sr)
                    pf = B.fit_predict(X[k, m], y[m], X[k, i]); ps = stable_pred(X[k, m], y[m], X[k, i]); wp = max(wp, abs(pf - ps) / max(1e-9, abs(ps)))
    log(f"D2 one-descriptor path: {tot} selected candidates checked; max rel error of inner RMSE {wr:.2e}, of prediction {wp:.2e}")
def d3():
    P8 = [alkane_pairs(r[0]) for r in OCTANES]; y8 = np.array([r[1 + PROPS.index("dHvap")] for r in OCTANES])
    rows = list(csv.DictReader(open(os.path.join(HERE, "nonane_data.csv")))); kk = [r for r in rows if r["dHvap_kcal"].strip()]
    P9 = [alkane_pairs(r["smiles"]) for r in kk]; y9 = np.array([float(r["dHvap_kcal"]) for r in kk])
    for name, P, y in (("octane dHvap", P8, y8), ("nonane dHvap", P9, y9)):
        for L, step in ((2, 0.05), (4, 0.1), (8, 0.2), (12, 0.25)):
            K = int(round(L / step)); g = np.arange(-K, K + 1) * step   # v40.22: exact grid (0.0 is exactly representable)
            assert all(abs(x / step - round(x / step)) < 1e-12 for x in g) and 0.0 in g, "grid hygiene: every value a multiple of the step, zero exact"
            T_ = [(a, b, 0.0) for a in g for b in g]
            preds, sel = B.outer_loo(B.fold_select_ols, B.descriptor_matrix(P, T_), y)
            edge = sum(1 for s in sel if max(abs(T_[s][0]), abs(T_[s][1])) >= L - step - 1e-9)   # v40.22: within one grid step
            log(f"D3 {name} dense parent grid half-width {L}: nested Q2 {B.scores(preds, y)[0]:.4f}, folds on boundary {edge}/{len(y)}")
if __name__ == "__main__":
    d1(); d3(); d2()
    open(os.path.join(HERE, "wide_box_diagnostics_out.txt"), "w").write("\n".join(OUT) + "\n")
