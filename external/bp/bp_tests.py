#!/usr/bin/env python3
"""Pre-registered v40 boiling-point tests (../PREREG_v40.md).

Test A (external decane T_B): one-descriptor models, fully nested LOO.
Test B (pooled C6-C10 T_B, size-adjusted): T_B = a + b n_C + c x, fully nested
LOO; for GM/LO the candidate is chosen by inner-LOO RMSE of this model. The
descriptor is standardized with training-fold statistics before solving
(model-invariant; needed for conditioning in the wide search boxes).
Candidate streams per seed s (rng = default_rng(s)), 2000 per model, in order:
  LO2  ~ U(-2,2)^3;  GM2 ~ U(-2,2)^2 (gamma=0);
  GM12 ~ U(-12,12)^2 (gamma=0);  LOh ~ (U(-12,12)^2, U(-2,2)).
Seeds 0..49. Primary contrast dQ2 = Q2(LOh) - Q2(GM12) (median over seeds).
Decision: 'gamma adds value' iff LOh > GM12 in >= 40/50 seeds AND the 95%
molecule-bootstrap interval (2000 resamples, conditional on fitted outer
predictions, rng 20261005) of the median dQ2 excludes 0.
Outputs: bp_results_seeds.csv, bp_results_summary.csv, bp_baselines.csv.
"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
import baselines as B

SEEDS, BUD = range(50), 2000
CLASSICAL = [t for nm, t in B.FIXED_INDICES if not nm.startswith("LO(")]


def load():
    rows = list(csv.DictReader(open(os.path.join(HERE, "bp_data.csv"))))
    P = [[tuple(map(int, x.split("-"))) for x in r["degree_pairs"].split()] for r in rows]
    return rows, P, np.array([float(r["T_B_C"]) for r in rows]), np.array([int(r["n_C"]) for r in rows], float)


def streams(seed):
    rng = np.random.default_rng(seed)
    lo2 = np.round(rng.uniform(-2, 2, (BUD, 3)), 3)
    gm2 = np.column_stack([np.round(rng.uniform(-2, 2, (BUD, 2)), 3), np.zeros(BUD)])
    gm12 = np.column_stack([np.round(rng.uniform(-12, 12, (BUD, 2)), 3), np.zeros(BUD)])
    hy = np.round(np.column_stack([rng.uniform(-12, 12, (BUD, 2)), rng.uniform(-2, 2, BUD)]), 3)
    return {"LO2": lo2, "GM2": gm2, "GM12": gm12, "LOh": hy}


def q2(p, y):
    return 1 - ((p - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


# ---------- two-predictor (size + descriptor) machinery ----------
def _standardize(Xt):
    """Affine rescaling of each candidate descriptor by its training-fold mean
    and SD. OLS with an intercept is invariant to this, so the fitted model and
    its leave-one-out residuals are unchanged, but the normal equations stay
    well conditioned for descriptors spanning many orders of magnitude (wide
    search boxes give values from 1e-14 to 1e+24)."""
    Xt = B._rescale_extreme_rows(np.asarray(Xt, float))   # v40.11: keeps variances representable beyond 1e+-150 (never reached here)
    mu = Xt.mean(axis=1, keepdims=True); sd = Xt.std(axis=1, keepdims=True)
    sd = np.where(sd > 0, sd, 1.0)
    return (Xt - mu) / sd


def press_size(Xt, zt, yt):
    """Inner-LOO RMSE of y ~ 1 + z + x for every candidate row of Xt (C x n).

    The closed-form residual/(1-h) identity requires every deletion to keep
    the design of full rank; a candidate whose deletion makes a leverage
    reach 1 (its leave-one-out prediction is then undefined) is rejected
    (inf), consistently with the singular-design filter (v40.11; never
    triggered on the package data, where the result is bit-identical)."""
    Xt_raw = np.asarray(Xt, float)
    C, n = Xt_raw.shape
    Xt = _standardize(Xt_raw)
    A = np.stack([np.ones((C, n)), np.broadcast_to(zt, (C, n)), Xt], axis=2)      # C x n x 3
    S = np.einsum("cni,cnj->cij", A, A)
    ok = np.abs(np.linalg.det(S)) > 1e-9 * np.abs(S).max(axis=(1, 2)) ** 3
    S[~ok] = np.eye(3)
    Si = np.linalg.inv(S)
    beta = np.einsum("cij,cnj,n->ci", Si, A, yt)
    res = yt - np.einsum("cni,ci->cn", A, beta)
    h = np.einsum("cni,cij,cnj->cn", A, Si, A)
    regular = ok & np.all(np.abs(1 - h) > 1e-10, axis=1)   # deletion-induced rank loss -> rejected
    r = np.full(C, np.inf)
    r[regular] = np.sqrt(((res[regular] / (1 - h[regular])) ** 2).mean(axis=1))
    return r


def fit_pred_size(xt, zt, yt, xn, zn):
    xt = np.asarray(xt, float)
    scale = float(np.abs(xt).max())
    if scale > 0 and (scale < 1e-150 or scale > 1e150):   # v40.11: as in baselines.fit_predict
        xt, xn = xt / scale, xn / scale
    mu, sd = xt.mean(), xt.std()
    sd = sd if sd > 0 else 1.0
    A = np.column_stack([np.ones_like(zt), zt, (xt - mu) / sd])
    coef, *_ = np.linalg.lstsq(A, yt, rcond=None)
    return coef[0] + coef[1] * zn + coef[2] * (xn - mu) / sd


def nested_size(X, z, y):
    n = len(y); preds = np.empty(n)
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        r = press_size(X[:, m], z[m], y[m])
        if not np.isfinite(r).any():     # never reached (design determinant has ~7000x headroom); argmin over all-inf would silently pick 0
            raise RuntimeError(f"fold {i}: every candidate rejected by the singular-design guard")
        k = int(np.argmin(r))
        preds[i] = fit_pred_size(X[k, m], z[m], y[m], X[k, i], z[i])
    return preds


def size_only(z, y):
    """Leave-one-out predictions of y ~ 1 + z by ordinary least squares (the
    same solver as fit_pred_size, without a descriptor)."""
    n = len(y); preds = np.empty(n)
    for i in range(n):
        m = np.arange(n) != i
        A = np.column_stack([np.ones(m.sum()), z[m]])
        coef, *_ = np.linalg.lstsq(A, y[m], rcond=None)
        preds[i] = coef[0] + coef[1] * z[i]
    return preds


# ---------- tests ----------
def boot_ci(G, L, y, rng):
    n = len(y); stats = []
    for _ in range(2000):
        idx = rng.integers(0, n, n); yy = y[idx]
        qg = 1 - ((G[:, idx] - yy) ** 2).sum(1) / ((yy - yy.mean()) ** 2).sum()
        ql = 1 - ((L[:, idx] - yy) ** 2).sum(1) / ((yy - yy.mean()) ** 2).sum()
        stats.append(np.median(ql - qg))
    return np.percentile(stats, [2.5, 97.5])


def run_test(label, P, y, z=None):
    preds = {k: [] for k in ("LO2", "GM2", "GM12", "LOh")}
    seed_rows = []
    for s in SEEDS:
        st = streams(s); q = {}
        for k, T in st.items():
            X = B.descriptor_matrix(P, T)
            p = nested_size(X, z, y) if z is not None else B.outer_loo(B.fold_select_ols, X, y)[0]
            preds[k].append(p); q[k] = q2(p, y)
        seed_rows.append([label, s] + [f"{q[k]:+.10f}" for k in ("GM2", "LO2", "GM12", "LOh")])
    Gp, Lp = np.array(preds["GM12"]), np.array(preds["LOh"])
    d = np.array([q2(l, y) - q2(g, y) for g, l in zip(Gp, Lp)])
    ci = boot_ci(Gp, Lp, y, np.random.default_rng(20261005))
    wins = int((d > 0).sum())
    verdict = "gamma adds value" if (wins >= 40 and (ci[0] > 0 or ci[1] < 0) and np.median(d) > 0) else "no evidence that gamma adds value"
    med = lambda k: np.median([q2(p, y) for p in preds[k]])
    summ = [label, len(y), f"{med('GM2'):.10f}", f"{med('LO2'):.10f}", f"{med('GM12'):.10f}", f"{med('LOh'):.10f}",
            f"{np.median(d):+.10f}", wins, f"{ci[0]:+.10f}", f"{ci[1]:+.10f}", verdict]   # v40.13: full precision
    return seed_rows, summ


def baselines(label, P, y, z=None):
    out = []
    Xc = B.descriptor_matrix(P, CLASSICAL)
    ir = np.array([B.irla(p) for p in P])[None, :]
    lo1 = B.descriptor_matrix(P, [(0.0, 0.0, 1.0)])
    F = np.array([B.count_vector(p) for p in P], float)
    if z is None:
        out.append(("mean", B.outer_loo(B.fold_mean, None, y)[0]))
        out.append(("classical best", B.outer_loo(B.fold_select_ols, Xc, y)[0]))
        out.append(("IRLA", B.outer_loo(B.fold_select_ols, ir, y)[0]))
        out.append(("LO(0,0,1) fixed", B.outer_loo(B.fold_select_ols, lo1, y)[0]))
    else:
        out.append(("size only", size_only(z, y)))
        out.append(("size + classical best", nested_size(Xc, z, y)))
        out.append(("size + IRLA", nested_size(ir, z, y)))
        out.append(("size + LO(0,0,1) fixed", nested_size(lo1, z, y)))
    out.append(("ridge on degree-pair counts", B.outer_loo(B.fold_ridge, F, y)[0]))
    return [[label, nm, len(y), f"{q2(p, y):.10f}", f"{np.sqrt(((p - y) ** 2).mean()):.10f}"] for nm, p in out]   # v40.13: full precision


def main():
    rows, P, y, z = load()
    dec = [i for i, r in enumerate(rows) if r["n_C"] == "10"]
    Pd, yd = [P[i] for i in dec], y[dec]
    seeds, summ, base = [], [], []
    for label, args in (("A: decane T_B", (Pd, yd, None)), ("B: pooled C6-C10 T_B (size-adjusted)", (P, y, z))):
        sr, sm = run_test(label, *args); seeds += sr; summ.append(sm)
        base += baselines(label, *args)
        print(sm, flush=True)
    with open(os.path.join(HERE, "bp_results_seeds.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["test", "seed", "Q2_GM2", "Q2_LO2", "Q2_GM12", "Q2_LOh"]); w.writerows(seeds)
    with open(os.path.join(HERE, "bp_results_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["test", "n", "median_Q2_GM2", "median_Q2_LO2", "median_Q2_GM12", "median_Q2_LOh",
                    "median_dQ2_LOh_GM12", "LOh_better_of_50", "ci95_lo", "ci95_hi", "prereg_verdict"])
        w.writerows(summ)
    with open(os.path.join(HERE, "bp_baselines.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["test", "model", "n", "Q2", "RMSE"]); w.writerows(base)
    for b in base: print(b)


if __name__ == "__main__":
    main()
