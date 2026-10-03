#!/usr/bin/env python3
"""Fully nested LOO ablation: MODEL GM = LO(a,b,0) (200 (a,b) candidates) vs
MODEL LO = LO(a,b,g) (200 (a,b,g) candidates, same budget) on the 5 octane
properties. Candidates ~ U(-2,2) rounded to 3 dp, rng default_rng(12345),
LO triples drawn first (200x3), then GM pairs (200x2).

Outer fold i: leave molecule i out. Inner: on the 17 training molecules,
evaluate each candidate by inner LOO RMSE of simple linear regression
(descriptor -> property); pick minimal (ties: first); refit OLS on all 17;
predict molecule i. Degenerate (constant-on-training) descriptors predict the
training mean.

Outputs: ablation_perfold.csv, ablation_summary.csv (same directory).
"""
import csv, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- copied verbatim from verify_loyola_v32.py ----
OCTANES = [
('CCCCCCCC',125.6,-49.82,9.92,111.55,0.398),('CC(C)CCCCC',117.6,-51.50,9.48,109.84,0.378),
('CCC(C)CCCC',118.9,-50.82,9.52,111.26,0.371),('CCCC(C)CCC',117.7,-50.69,9.48,109.32,0.372),
('CC(C)(C)CCCC',106.8,-53.71,8.92,103.13,0.339),('CC(C)C(C)CCC',115.6,-51.13,9.27,108.02,0.348),
('CC(C)CC(C)CC',109.4,-52.44,9.03,106.98,0.344),('CC(C)CCC(C)C',109.1,-53.21,9.05,105.72,0.357),
('CCCC(C)(C)CC',111.9,-52.61,9.04,104.74,0.322),('CCC(C)C(C)CC',117.7,-50.91,9.32,106.59,0.340),
('CCC(CC)C(C)C',115.6,-50.48,9.21,106.06,0.330),('CCC(C)(CC)CC',118.3,-51.38,9.21,101.48,0.302),
('CCC(CC)CCC',118.5,-50.40,9.48,109.43,0.362),('CCC(C)C(C)(C)C',109.8,-52.61,8.88,101.31,0.300),
('CC(C)CC(C)(C)C',99.2,-53.57,8.40,101.81,0.305),('CCC(C)(C)C(C)C',114.8,-51.73,9.02,101.31,0.291),
('CC(C)C(C)C(C)C',113.5,-51.97,9.01,102.39,0.317),('CC(C)(C)C(C)(C)C',106.5,-53.99,8.41,93.06,0.247)]
PROPS = ["T_B","dHf","dHvap","S","omega"]

def alkane_pairs(smi):
    adj={};prev=None;stack=[];k=-1
    for ch in smi:
        if ch=='(':stack.append(prev)
        elif ch==')':prev=stack.pop()
        elif ch=='C':
            k+=1;adj[k]=set()
            if prev is not None:adj[k].add(prev);adj[prev].add(k)
            prev=k
    seen=set();out=[]
    for u in adj:
        for v in adj[u]:
            e=(min(u,v),max(u,v))
            if e in seen:continue
            seen.add(e);out.append((len(adj[u]),len(adj[v])))
    return out

def lo_pairs(P,a,b,g):return sum((i*j)**a*(i+j)**b*math.exp(g*abs(i-j)/(i+j)) for i,j in P)
# ---- end copied pieces ----

N = 18
OP = [alkane_pairs(r[0]) for r in OCTANES]
Y = {p: np.array([r[1+i] for r in OCTANES]) for i, p in enumerate(PROPS)}

# Candidate draws: LO triples first, then GM pairs (fixed, reproducible streams)
rng = np.random.default_rng(12345)
LO_TRIPLES = np.round(rng.uniform(-2, 2, size=(200, 3)), 3)
GM_PAIRS   = np.round(rng.uniform(-2, 2, size=(200, 2)), 3)
GM_TRIPLES = np.column_stack([GM_PAIRS, np.zeros(200)])  # g fixed at 0

def descriptor_matrix(triples):
    """(n_cand, 18) matrix of LO(G;a,b,g) values."""
    X = np.empty((len(triples), N))
    for k, (a, b, g) in enumerate(triples):
        X[k] = [lo_pairs(Pr, a, b, g) for Pr in OP]
    return X

X_LO = descriptor_matrix(LO_TRIPLES)
X_GM = descriptor_matrix(GM_TRIPLES)
assert np.all(np.isfinite(X_LO)) and np.all(np.isfinite(X_GM))

def is_constant(x):
    """Constant-on-subset guard (relative tolerance)."""
    return (x.max() - x.min()) <= 1e-9 * max(1.0, float(np.abs(x).max()))

def inner_loo_rmse_all(Xt, yt):
    """Vectorized inner-LOO RMSE for every candidate row of Xt on the training
    set (Xt: (C, n), yt: (n,)). Closed-form leave-one-out sums; degenerate
    (constant) leave-one-out subsets predict the subset mean."""
    C, n = Xt.shape
    m = n - 1
    Sx  = Xt.sum(axis=1, keepdims=True)          # (C,1)
    Sxx = (Xt**2).sum(axis=1, keepdims=True)
    Sxy = (Xt * yt).sum(axis=1, keepdims=True)
    Sy  = yt.sum()
    Sx_j  = Sx  - Xt                              # (C,n): sums excluding col j
    Sxx_j = Sxx - Xt**2
    Sxy_j = Sxy - Xt * yt
    Sy_j  = Sy  - yt                              # (n,) broadcast
    denom = m * Sxx_j - Sx_j**2                   # m^2 * var of subset
    scale = np.maximum(1.0, Sxx_j)
    degen = denom <= 1e-12 * scale
    safe = np.where(degen, 1.0, denom)
    slope = (m * Sxy_j - Sx_j * Sy_j) / safe
    pred = Sy_j / m + slope * (Xt - Sx_j / m)     # intercept + slope*x_j
    pred = np.where(degen, Sy_j / m, pred)
    return np.sqrt(((pred - yt) ** 2).mean(axis=1))

def fit_predict(xt, yt, xnew):
    """OLS on training set; degenerate descriptor -> training mean."""
    if is_constant(xt):
        return float(yt.mean())
    xm, ym = xt.mean(), yt.mean()
    b = ((xt - xm) * (yt - ym)).sum() / ((xt - xm) ** 2).sum()
    return float(ym + b * (xnew - xm))

def run_model(X, triples, y):
    """Nested LOO for one property/model. Returns preds (18,), sel (18,3)."""
    preds = np.empty(N)
    sel = np.empty((N, 3))
    for i in range(N):
        mask = np.ones(N, bool); mask[i] = False
        Xt, yt = X[:, mask], y[mask]
        rmse = inner_loo_rmse_all(Xt, yt)
        k = int(np.argmin(rmse))                  # ties -> first
        preds[i] = fit_predict(Xt[k], yt, X[k, i])
        sel[i] = triples[k]
    return preds, sel

def r_signed(x, y):
    xc = x - x.mean(); yc = y - y.mean()
    s = np.linalg.norm(xc) * np.linalg.norm(yc)
    return 0.0 if s == 0 else float(xc @ yc / s)

def metrics(pred, y):
    ss = ((y - y.mean()) ** 2).sum()
    q2 = 1 - ((y - pred) ** 2).sum() / ss
    rmse = float(np.sqrt(((pred - y) ** 2).mean()))
    mae = float(np.abs(pred - y).mean())
    return q2, rmse, mae, r_signed(pred, y)

def stab(v):
    return (float(v.mean()), float(v.std(ddof=0)), float(v.min()), float(v.max()))

perfold_rows, summary_rows = [], []
headline = []
for p in PROPS:
    y = Y[p]
    pred_gm, sel_gm = run_model(X_GM, GM_TRIPLES, y)
    pred_lo, sel_lo = run_model(X_LO, LO_TRIPLES, y)
    res = {}
    for model, pred, sel in [("GM", pred_gm, sel_gm), ("LO", pred_lo, sel_lo)]:
        q2, rmse, mae, rs = metrics(pred, y)
        res[model] = dict(q2=q2, rmse=rmse, mae=mae, rs=rs,
                          abserr=np.abs(pred - y), pred=pred, sel=sel)
        for i in range(N):
            perfold_rows.append([p, model, i, i,
                f"{sel[i,0]:.3f}", f"{sel[i,1]:.3f}", f"{sel[i,2]:.3f}",
                f"{pred[i]:.6f}", f"{y[i]:.4f}", f"{abs(pred[i]-y[i]):.6f}"])
    d = res["LO"]["abserr"] - res["GM"]["abserr"]     # LO minus GM
    tol = 1e-9
    nb = int((d < -tol).sum()); nw = int((d > tol).sum()); nt = N - nb - nw
    for model in ["GM", "LO"]:
        r = res[model]; sel = r["sel"]
        am, asd, amin, amax = stab(sel[:, 0])
        bm, bsd, bmin, bmax = stab(sel[:, 1])
        gm_, gsd, gmin, gmax = stab(sel[:, 2])
        gfrac = float((np.abs(sel[:, 2]) > 1.5).mean())
        row = [p, model, f"{r['q2']:.4f}", f"{r['rmse']:.4f}", f"{r['mae']:.4f}",
               f"{r['rs']:.4f}", f"{r['mae']:.4f}"]
        if model == "LO":
            row += [f"{d.mean():.6f}", f"{np.median(d):.6f}", nb, nw, nt]
        else:
            row += ["", "", "", "", ""]
        row += [f"{am:.3f}", f"{asd:.3f}", f"{amin:.3f}", f"{amax:.3f}",
                f"{bm:.3f}", f"{bsd:.3f}", f"{bmin:.3f}", f"{bmax:.3f}"]
        if model == "LO":
            row += [f"{gm_:.3f}", f"{gsd:.3f}", f"{gmin:.3f}", f"{gmax:.3f}", f"{gfrac:.3f}"]
        else:
            row += ["", "", "", "", ""]
        summary_rows.append(row)
    headline.append((p, res["GM"]["q2"], res["LO"]["q2"], d.mean(), np.median(d), nb, nw, nt))
    print(f"[{p}] GM Q2={res['GM']['q2']:+.4f} RMSE={res['GM']['rmse']:.4f} MAE={res['GM']['mae']:.4f} r={res['GM']['rs']:+.4f}")
    print(f"[{p}] LO Q2={res['LO']['q2']:+.4f} RMSE={res['LO']['rmse']:.4f} MAE={res['LO']['mae']:.4f} r={res['LO']['rs']:+.4f}")
    print(f"[{p}] paired |err| diff (LO-GM): mean={d.mean():+.4f} median={np.median(d):+.4f} LO better/worse/tied = {nb}/{nw}/{nt}")
    slo = res["LO"]["sel"]; sgm = res["GM"]["sel"]
    print(f"[{p}] GM sel a mean/sd={sgm[:,0].mean():+.3f}/{sgm[:,0].std():.3f}  b mean/sd={sgm[:,1].mean():+.3f}/{sgm[:,1].std():.3f}")
    print(f"[{p}] LO sel a mean/sd={slo[:,0].mean():+.3f}/{slo[:,0].std():.3f}  b mean/sd={slo[:,1].mean():+.3f}/{slo[:,1].std():.3f}  "
          f"g mean/sd={slo[:,2].mean():+.3f}/{slo[:,2].std():.3f}  frac|g|>1.5={float((np.abs(slo[:,2])>1.5).mean()):.3f}")
    print()

with open(os.path.join(HERE, "ablation_perfold.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["property","model","fold","heldout_index","sel_a","sel_b","sel_g",
                "pred","actual","abs_err"])
    w.writerows(perfold_rows)

with open(os.path.join(HERE, "ablation_summary.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["property","model","Q2","RMSE","MAE","r_signed","mean_abs_err",
                "paired_diff_mean_LOminusGM","paired_diff_median_LOminusGM",
                "n_LO_better","n_LO_worse","n_tied",
                "sel_a_mean","sel_a_sd","sel_a_min","sel_a_max",
                "sel_b_mean","sel_b_sd","sel_b_min","sel_b_max",
                "sel_g_mean","sel_g_sd","sel_g_min","sel_g_max","frac_absg_gt_1.5"])
    w.writerows(summary_rows)

print("HEADLINE (property: GM Q2 vs LO Q2, LO-GM mean|err|diff, better/worse/tied):")
for p, qg, ql, dm, dmed, nb, nw, nt in headline:
    print(f"  {p:6s}  GM {qg:+.4f}  LO {ql:+.4f}  dQ2={ql-qg:+.4f}  d|err| mean={dm:+.4f} med={dmed:+.4f}  {nb}/{nw}/{nt}")
