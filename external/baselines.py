#!/usr/bin/env python3
"""Pre-registered baseline comparison (PREREG_v37.md, Q2) for the LO paper.

For each property of a dataset (octanes now; nonanes via a CSV later), every
method below is evaluated by a fully nested outer leave-one-out: the outer fold
holds out one molecule and EVERY selection/tuning step (index choice, ridge
penalty, feature standardization, candidate choice) uses the outer training
fold only. Methods:

  mean        training-fold mean predictor
  fixed_best  best of the 12 fixed established indices (M1, M2, HM, mM2, R,
              chi, H/2, ISI, GA, AG, LO(0,0,1), LO(0,0,2)); index chosen inside
              the training fold by inner-LOO RMSE of one-descriptor OLS
  IRLA        IRLA(G) = 2 sum_uv q_uv, one-descriptor OLS (no selection)
  ridge       ridge on the edge-degree-pair count vector (pairs (i,j),
              1<=i<=j<=4); features standardized with training statistics
              (inside the inner folds too); lambda from a fixed log-grid
              1e-4..1e4 (41 values) chosen by inner LOO; intercept unpenalized
  GM, LO      random-search models exactly as in expanded_robustness_v35.py
              (rng = default_rng(seed); LO triples U(-2,2)^(B x 3) rounded 3dp
              drawn first, then GM pairs U(-2,2)^(B x 2) rounded 3dp, gamma=0),
              seeds 0..99, budgets 200 and 500, plus seed 12345 / budget 200.

Reported per method: outer Q2 = 1 - PRESS/SS_tot, RMSE = sqrt(PRESS/n), and
signed Pearson r between outer predictions and observations.

CLI:
  python3 external/baselines.py                    # octanes -> baselines_octane.csv
  python3 external/baselines.py --dataset nonane   # external/nonane_data.csv
  python3 external/baselines.py --dataset path/to/file.csv --props T_B dHvap
CSV datasets need a SMILES column (case-insensitive 'smiles'); property columns
are the numeric columns other than id/name/cas/smiles/notes (or --props).
Empty / NA / nan / MISSING cells are missing; each property is analysed on the
molecules where it is present, and only if >= --min-n values exist (default 25
for CSV datasets per the pre-registration, no minimum for the octanes).
"""
import argparse, csv, math, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from octane_data import OCTANES, PROPS as OCT_PROPS, alkane_pairs, lo_pairs  # noqa: E402

# --------------------------------------------------------------------------
# descriptors
# --------------------------------------------------------------------------
FIXED_INDICES = [  # name, (alpha, beta, gamma)
    ("M1", (0.0, 1.0, 0.0)), ("M2", (1.0, 0.0, 0.0)), ("HM", (0.0, 2.0, 0.0)),
    ("mM2", (-1.0, 0.0, 0.0)), ("R", (-0.5, 0.0, 0.0)), ("chi", (0.0, -0.5, 0.0)),
    ("H/2", (0.0, -1.0, 0.0)), ("ISI", (1.0, -1.0, 0.0)), ("GA", (0.5, -1.0, 0.0)),
    ("AG", (-0.5, 1.0, 0.0)), ("LO(0,0,1)", (0.0, 0.0, 1.0)),
    ("LO(0,0,2)", (0.0, 0.0, 2.0)),
]
DEG_PAIRS = [(i, j) for i in range(1, 5) for j in range(i, 5)]  # 10 types
LAMBDA_GRID = np.logspace(-4, 4, 41)
SEEDS = list(range(100))
BUDGETS = (200, 500)
REF_SEED, REF_BUDGET = 12345, 200


def descriptor_matrix(pairs_list, triples):
    """(C x n) matrix of LO values; identical arithmetic to the v35 script."""
    X = np.empty((len(triples), len(pairs_list)))
    for k, (a, b, g) in enumerate(triples):
        X[k] = [lo_pairs(P, a, b, g) for P in pairs_list]
    return X


def irla(P):
    return 2.0 * sum(abs(i - j) / (i + j) for i, j in P)


def count_vector(P):
    c = np.zeros(len(DEG_PAIRS))
    for i, j in P:
        c[DEG_PAIRS.index((min(i, j), max(i, j)))] += 1
    return c


def candidate_triples(seed, budget):
    """Exact v35 stream: LO triples first, then GM pairs (gamma = 0)."""
    rng = np.random.default_rng(seed)
    lo_t = np.round(rng.uniform(-2, 2, (budget, 3)), 3)
    gm_p = np.round(rng.uniform(-2, 2, (budget, 2)), 3)
    gm_t = np.column_stack([gm_p, np.zeros(budget)])
    return gm_t, lo_t


# --------------------------------------------------------------------------
# one-descriptor OLS machinery (copied verbatim in logic from v35)
# --------------------------------------------------------------------------
def is_constant(x):
    """The descriptor is constant on the training fold if its range is within
    floating-point resolution of its magnitude (16 machine epsilons, i.e. about
    3.6e-15 relative). This is invariant to rescaling and to translation as far
    as double precision can represent the values: x = 1e13 + {1,...,10} is
    correctly non-constant, while a constant vector carrying rounding noise is
    constant. (v40.3; the v40.2 relative threshold of 1e-12 wrongly flagged
    large-offset descriptors as constant.)"""
    x = np.asarray(x, float)
    scale = float(np.abs(x).max())
    if scale == 0:
        return True
    if scale < 1e-150 or scale > 1e150:
        # Avoid underflow in the tolerance and overflow in the range.
        x = x / scale
        return (x.max() - x.min()) <= 16 * np.finfo(float).eps
    return (x.max() - x.min()) <= 16 * np.finfo(float).eps * scale


def _rescale_extreme_rows(Xt):
    """Keep variance calculations representable without changing ordinary rows."""
    scale = np.abs(Xt).max(axis=1, keepdims=True)
    extreme = (scale > 0) & ((scale < 1e-150) | (scale > 1e150))
    return Xt / np.where(extreme, scale, 1.0)


def _standardize_rows(Xt):
    """Affine rescaling of each candidate row by its training-fold mean and SD;
    OLS with an intercept is invariant to it, so selections and predictions are
    unchanged, but the arithmetic no longer depends on the descriptor's units
    or offset (values span 1e-14..1e+24 in wide search boxes). The invariance
    holds up to double-precision representation of the inputs themselves."""
    Xt = _rescale_extreme_rows(Xt)
    mu = Xt.mean(axis=1, keepdims=True); sd = Xt.std(axis=1, keepdims=True)
    return (Xt - mu) / np.where(sd > 0, sd, 1.0)


def inner_loo_rmse_all(Xt, yt):
    """Inner leave-one-out RMSE of the one-descriptor OLS for every candidate
    row of Xt (C x n), computed on standardized rows (v40.2)."""
    Xt = _standardize_rows(np.asarray(Xt, float))
    C, n = Xt.shape
    m = n - 1
    Sx  = Xt.sum(axis=1, keepdims=True)
    Sxx = (Xt**2).sum(axis=1, keepdims=True)
    Sxy = (Xt * yt).sum(axis=1, keepdims=True)
    Sy  = yt.sum()
    Sx_j, Sxx_j, Sxy_j = Sx - Xt, Sxx - Xt**2, Sxy - Xt * yt
    Sy_j = Sy - yt
    denom = m * Sxx_j - Sx_j**2
    degen = denom <= 1e-12 * np.maximum(m * Sxx_j, np.finfo(float).tiny)
    slope = (m * Sxy_j - Sx_j * Sy_j) / np.where(degen, 1.0, denom)
    pred = Sy_j / m + slope * (Xt - Sx_j / m)
    pred = np.where(degen, Sy_j / m, pred)
    return np.sqrt(((pred - yt) ** 2).mean(axis=1))


def fit_predict(xt, yt, xnew):
    xt = np.asarray(xt, float)
    if is_constant(xt):
        return float(yt.mean())
    scale = float(np.abs(xt).max())
    if scale < 1e-150 or scale > 1e150:
        xt, xnew = xt / scale, xnew / scale
    mu, sd = xt.mean(), xt.std()
    xs, xn = (xt - mu) / sd, (xnew - mu) / sd
    ym = yt.mean()
    b = ((xs) * (yt - ym)).sum() / ((xs) ** 2).sum()
    return float(ym + b * xn)


def _mask(n, i):
    m = np.ones(n, bool); m[i] = False
    return m


def fold_mean(_F, y, i):
    m = _mask(len(y), i)
    return float(y[m].mean()), None


def fold_select_ols(X, y, i):
    """X: (C x n) candidate matrix. Inner-LOO selection, refit, predict."""
    m = _mask(len(y), i)
    Xt, yt = X[:, m], y[m]
    rmse = inner_loo_rmse_all(Xt, yt)
    if not np.isfinite(rmse).any():      # never reached on the package data; argmin over all-inf would silently pick 0
        raise RuntimeError(f"fold {i}: every candidate descriptor is degenerate on the training set")
    k = int(np.argmin(rmse))
    return fit_predict(Xt[k], yt, X[k, i]), k


def fold_ols(x, y, i):
    m = _mask(len(y), i)
    return fit_predict(x[m], y[m], x[i]), None


def ridge_fit_predict(Ft, yt, Fnew, lam):
    """Standardize with Ft statistics (ddof=0); zero-variance columns dropped;
    unpenalized intercept; closed form. Fnew: (k x p)."""
    mu = Ft.mean(axis=0); sd = Ft.std(axis=0)
    keep = sd > 1e-12
    Z = (Ft[:, keep] - mu[keep]) / sd[keep]
    Zn = (Fnew[:, keep] - mu[keep]) / sd[keep]
    ym = yt.mean()
    if Z.shape[1] == 0:
        return np.full(len(Fnew), ym)
    A = Z.T @ Z + lam * np.eye(Z.shape[1])
    w = np.linalg.solve(A, Z.T @ (yt - ym))
    return ym + Zn @ w


def ridge_inner_rmse(Ft, yt):
    """Inner-LOO RMSE for every lambda; each inner fold re-standardizes."""
    n = len(yt)
    err = np.zeros((len(LAMBDA_GRID), n))
    for j in range(n):
        mj = _mask(n, j)
        for li, lam in enumerate(LAMBDA_GRID):
            err[li, j] = ridge_fit_predict(Ft[mj], yt[mj], Ft[j:j + 1], lam)[0] - yt[j]
    return np.sqrt((err**2).mean(axis=1))


def fold_ridge(F, y, i):
    m = _mask(len(y), i)
    Ft, yt = F[m], y[m]
    rr = ridge_inner_rmse(Ft, yt)
    if not np.isfinite(rr).any():
        raise RuntimeError(f"fold {i}: ridge inner-LOO error not finite for any lambda")
    li = int(np.argmin(rr))
    return float(ridge_fit_predict(Ft, yt, F[i:i + 1], LAMBDA_GRID[li])[0]), li


def outer_loo(fold_fn, feats, y):
    n = len(y)
    preds = np.empty(n); sel = []
    for i in range(n):
        preds[i], s = fold_fn(feats, y, i)
        sel.append(s)
    return preds, sel


def scores(preds, y):
    press = ((preds - y) ** 2).sum()
    ss = ((y - y.mean()) ** 2).sum()
    r = float(np.corrcoef(preds, y)[0, 1]) if preds.std() > 0 else float("nan")
    return 1 - press / ss, math.sqrt(press / len(y)), r


# --------------------------------------------------------------------------
# datasets
# --------------------------------------------------------------------------
MISSING_TOKENS = {"", "na", "nan", "n/a", "missing", "none", "null", "-"}
NON_PROP_COLS = {"smiles", "id", "name", "iupac", "iupac_name", "cas", "notes",
                 "note", "source", "url"}


def load_octane():
    smiles = [r[0] for r in OCTANES]
    Y = {p: np.array([r[1 + k] for r in OCTANES], float) for k, p in enumerate(OCT_PROPS)}
    return {"name": "octane", "smiles": smiles, "Y": Y, "props": list(OCT_PROPS)}


def load_csv(path, props=None, name=None):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"{path}: empty")
    cols = list(rows[0].keys())
    scol = next((c for c in cols if c.strip().lower() == "smiles"), None)
    if scol is None:
        raise ValueError(f"{path}: no SMILES column")

    def val(s):
        s = (s or "").strip()
        return float("nan") if s.lower() in MISSING_TOKENS else float(s)

    if props is None:
        props = []
        for c in cols:
            if c.strip().lower() in NON_PROP_COLS or c == scol:
                continue
            try:
                [val(r[c]) for r in rows]
                props.append(c)
            except ValueError:
                pass  # non-numeric column (e.g. provenance text)
    Y = {p: np.array([val(r[p]) for r in rows], float) for p in props}
    return {"name": name or os.path.splitext(os.path.basename(path))[0],
            "smiles": [r[scol].strip() for r in rows], "Y": Y, "props": props}


# --------------------------------------------------------------------------
# main analysis
# --------------------------------------------------------------------------
def gm_lo_matrices(pairs_list, seeds=SEEDS, budgets=BUDGETS, extra=((REF_SEED, REF_BUDGET),)):
    out = {}
    for sb in [(s, b) for s in seeds for b in budgets] + list(extra):
        gm_t, lo_t = candidate_triples(*sb)
        out[sb] = (descriptor_matrix(pairs_list, gm_t), descriptor_matrix(pairs_list, lo_t))
    return out


def analyse(ds, min_n=None, seeds=SEEDS, budgets=BUDGETS, verbose=True):
    pairs_all = [alkane_pairs(s) for s in ds["smiles"]]
    t0 = time.time()
    mats = gm_lo_matrices(pairs_all, seeds, budgets)
    Xfix_all = descriptor_matrix(pairs_all, [t for _, t in FIXED_INDICES])
    irla_all = np.array([irla(P) for P in pairs_all])
    F_all = np.array([count_vector(P) for P in pairs_all])
    rows, skipped = [], []
    for p in ds["props"]:
        yfull = ds["Y"][p]
        ok = np.isfinite(yfull)
        n = int(ok.sum())
        if (min_n is not None and n < min_n) or n < 4:
            skipped.append((p, n)); continue
        y = yfull[ok]

        def base(method, preds, note=""):
            q, e, r = scores(preds, y)
            rows.append(dict(property=p, n=n, method=method, Q2=q, RMSE=e, r_pred=r,
                             selection=note))

        base("mean", outer_loo(fold_mean, None, y)[0])
        pr, sel = outer_loo(fold_select_ols, Xfix_all[:, ok], y)
        cnt = {}
        for k in sel:
            cnt[FIXED_INDICES[k][0]] = cnt.get(FIXED_INDICES[k][0], 0) + 1
        base("fixed_best", pr, ";".join(f"{k}:{v}" for k, v in sorted(cnt.items(), key=lambda t: -t[1])))
        base("IRLA", outer_loo(fold_ols, irla_all[ok], y)[0])
        pr, sel = outer_loo(fold_ridge, F_all[ok], y)
        lams = [LAMBDA_GRID[k] for k in sel]
        base("ridge_counts", pr, f"lambda median {np.median(lams):.3g} range [{min(lams):.3g},{max(lams):.3g}]")

        for mi, mname in enumerate(("GM", "LO")):
            res = {}
            for sb, XX in mats.items():
                pr_, _ = outer_loo(fold_select_ols, XX[mi][:, ok], y)
                res[sb] = scores(pr_, y)
            for b in budgets:
                v = np.array([res[(s, b)] for s in seeds])
                rows.append(dict(property=p, n=n, method=f"{mname}_b{b}",
                                 Q2=float(np.median(v[:, 0])), RMSE=float(np.median(v[:, 1])),
                                 r_pred=float(np.median(v[:, 2])),
                                 Q2_min=v[:, 0].min(), Q2_max=v[:, 0].max(),
                                 RMSE_min=v[:, 1].min(), RMSE_max=v[:, 1].max(),
                                 n_seeds=len(seeds),
                                 selection="Q2/RMSE/r_pred = median over seeds"))
            q, e, r = res[(REF_SEED, REF_BUDGET)]
            rows.append(dict(property=p, n=n, method=f"{mname}_s{REF_SEED}_b{REF_BUDGET}",
                             Q2=q, RMSE=e, r_pred=r, selection="Supplementary Table S3(a) configuration (seed 12345, budget 200)"))
            rows[-1]["_per_seed"] = res  # kept for tests; not written
        if verbose:
            print(f"  {p}: done ({time.time() - t0:.1f}s)", flush=True)
    return rows, skipped


CSV_COLS = ["property", "n", "method", "Q2", "RMSE", "r_pred", "n_seeds",
            "Q2_min", "Q2_max", "RMSE_min", "RMSE_max", "selection"]


def write_csv(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(CSV_COLS)
        for r in rows:
            out = []
            for c in CSV_COLS:
                v = r.get(c, "")
                out.append(f"{v:.10f}" if isinstance(v, (float, np.floating)) else v)
            w.writerow(out)


def print_table(rows):
    print(f"\n{'property':<8} {'method':<18} {'Q2':>9} {'RMSE':>9} {'r_pred':>8}   seed range Q2 / RMSE")
    last = None
    for r in rows:
        if r["property"] != last and last is not None:
            print()
        last = r["property"]
        extra = ""
        if "Q2_min" in r:
            extra = (f"   [{r['Q2_min']:+.4f},{r['Q2_max']:+.4f}] / "
                     f"[{r['RMSE_min']:.4f},{r['RMSE_max']:.4f}]")
        print(f"{r['property']:<8} {r['method']:<18} {r['Q2']:+9.4f} {r['RMSE']:9.4f} {r['r_pred']:+8.4f}{extra}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dataset", default="octane",
                    help="'octane', 'nonane' (external/nonane_data.csv) or a CSV path")
    ap.add_argument("--props", nargs="*", default=None)
    ap.add_argument("--min-n", type=int, default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    if a.dataset == "octane":
        ds = load_octane(); min_n = a.min_n
    else:
        path = os.path.join(HERE, "nonane_data.csv") if a.dataset == "nonane" else a.dataset
        ds = load_csv(path, a.props, name=a.dataset if a.dataset == "nonane" else None)
        min_n = 25 if a.min_n is None else a.min_n
    if a.props and a.dataset == "octane":
        ds["props"] = a.props
    t0 = time.time()
    print(f"dataset {ds['name']}: {len(ds['smiles'])} molecules, properties {ds['props']}")
    rows, skipped = analyse(ds, min_n=min_n)
    for p, n in skipped:
        print(f"  skipped {p}: only {n} non-missing values")
    out = a.out or os.path.join(HERE, f"baselines_{ds['name']}.csv")
    write_csv(rows, out)
    print_table(rows)
    print(f"\nwrote {out}  ({time.time() - t0:.1f}s)")


if __name__ == "__main__":
    main()
