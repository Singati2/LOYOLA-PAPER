"""Adversarial tests of the degeneracy guard: v40.22 (old) vs resolution guard (new).
High-precision references by mpmath (80 digits) on the exact stored doubles."""
import sys, numpy as np, mpmath as mp
ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))))
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__))); sys.path.insert(1, __import__("os").path.join(ROOT, "external")); sys.path.insert(2, ROOT)
import baselines_old as O, baselines as N
mp.mp.dps = 80
eps = np.finfo(float).eps
rs = np.random.default_rng(1)

def mp_loo(x, y):
    """Exact (80-digit) LOO predictions of y ~ 1 + x on the stored doubles; constant fold -> mean."""
    X = [mp.mpf(float(v)) for v in x]; Y = [mp.mpf(float(v)) for v in y]; n = len(X); out = []
    for i in range(n):
        xs = [X[j] for j in range(n) if j != i]; ys = [Y[j] for j in range(n) if j != i]; m = n - 1
        mx = sum(xs) / m; my = sum(ys) / m
        sxx = sum((a - mx) ** 2 for a in xs)
        if sxx == 0: out.append(my); continue
        b = sum((a - mx) * (c - my) for a, c in zip(xs, ys)) / sxx
        out.append(my + b * (X[i] - mx))
    return out

def mp_inner_rmse(x, y):
    p = mp_loo(x, y); return mp.sqrt(sum((a - mp.mpf(float(b))) ** 2 for a, b in zip(p, y)) / len(y))

def guards(x):
    X = np.asarray(x, float)[None, :]
    old = bool(O.is_constant(X[0]) or (X.max() - X.min()) <= 1e-9 * max(abs(X).max(), np.finfo(float).tiny))
    new = bool(N.degenerate_rows(X)[0])
    lv = (X.max() - X.min()) / (eps * abs(X).max()) if abs(X).max() > 0 else 0.0
    return old, new, lv

def accuracy(x, y):
    """Relative errors of double inner-LOO RMSE (new code path) and LOO prediction vs mpmath."""
    ref = mp_inner_rmse(x, y)
    got = N.inner_loo_rmse_all(np.asarray(x)[None, :], y)[0]
    e1 = float(abs(mp.mpf(got) - ref) / max(ref, mp.mpf(1e-300)))
    pref = mp_loo(x, y)
    pd = [N.fit_predict(np.delete(x, i), np.delete(y, i), x[i]) for i in range(len(y))]
    e2 = max(float(abs(mp.mpf(a) - b) / max(abs(b), 1)) for a, b in zip(pd, pref))
    return e1, e2

rows = []
def rec(case, x, y, want):
    o, n, lv = guards(x)
    e1, e2 = accuracy(x, y)
    rows.append((case, lv, o, n, want, e1, e2))

n = 18
s = np.log(np.arange(2., 2. + n)) + 0.3 * rs.standard_normal(n)   # a "real" descriptor signal
y = 3.0 * s + 0.2 * rs.standard_normal(n)

# 1. true constants with rounding jitter (k ulps of c)
for c in (1e-300, 1e-200, 1e-8, 1.0, 7.0, 1e8, 1e200, 1e300):
    for J in (1, 4, 16, 64, 512):
        k = rs.integers(-J, J + 1, n).astype(float); k[0], k[1] = -J, J
        x = c * (1 + k * eps / 2)       # within J half-ulps: jitter around a true constant
        rec(f"jitter c={c:g} J={J}ulp", x, y, "reject")
# 1b. computed constant: same number formed by summing terms in different orders
for m in (7, 9, 15, 50, 200):
    terms = rs.uniform(0.1, 10, m)
    x = np.array([sum(rs.permutation(terms)) for _ in range(n)])
    rec(f"permuted-sum constant m={m}", x, y, "reject")
# 1c. LO at a tiny exponent (the old D3 point 3.6e-15): sub-resolution signal
sys.path.insert(0, ROOT); from octane_data import OCTANES, alkane_pairs, lo_pairs, PROPS
P = [alkane_pairs(r[0]) for r in OCTANES]; yo = np.array([r[1 + PROPS.index("dHvap")] for r in OCTANES])
for a in (3.6e-15, 1e-13, 1e-12, 1e-11, 1e-10, 1e-9, 1e-6, 1e-3):
    x = np.array([lo_pairs(p, a, a, 0.0) for p in P])
    rec(f"octane LO({a:g},{a:g},0)", x, yo, "reject" if a <= 1e-13 else "accept?")
# 2. tiny-but-real variation around a constant offset
for d in (1e-6, 1e-9, 1e-10, 1e-12, 1e-13, 1e-14):
    x = 1.0 + d * s
    rec(f"1 + {d:g}*s", x, y, "accept" if d >= 1e-12 else "reject?")
for sc in (1e-200, 1e-15, 1e15, 1e200):
    rec(f"{sc:g}*s (pure scale)", sc * s, y, "accept")
# 3. huge offsets on exactly representable integers and on a real-valued signal
xi = np.arange(1., n + 1); yi = 2 * xi + 3 + 0.1 * rs.standard_normal(n)
for c in (0, 1e6, 1e10, 1e12, 1e13, 1e14, 1e15, 1e16):
    rec(f"ints + {c:g}", xi + c, yi, "accept" if c <= 1e13 else "boundary")
for c in (1e6, 1e10, 1e12, 1e13):
    rec(f"s + {c:g}", s + c, y, "accept")
# 4. near-collinear with the intercept: one leverage point
for d in (1e-6, 1e-10, 1e-13, 1e-15):
    x = np.ones(n); x[-1] += d
    rec(f"ones, last +{d:g}", x, y, "accept" if d >= 1e-12 else "reject")

print(f"{'case':<32}{'levels':>11} {'old':>6} {'new':>6}  want      relerr_rmse relerr_pred")
for c, lv, o, nn, w, e1, e2 in rows:
    print(f"{c:<32}{lv:11.3g} {'REJ' if o else 'acc':>6} {'REJ' if nn else 'acc':>6}  {w:<9} {e1:10.2e} {e2:10.2e}")

# translation invariance of fold_select_ols (the expected-failure test, extended)
print("\nfold_select_ols(x + c) - fold_select_ols(x), x = 1..10, y = 2x + 3, fold 0:")
x = np.arange(1., 11.); yy = 2 * x + 3
for c in (1e10, 1e12, 1e13, 1e14, 2e14, 1e15):
    for name, M in (("old", O), ("new", N)):
        try:
            p = M.fold_select_ols((x + c)[None, :], yy, 0)[0]; r = f"{p - 25 + 20:.3e}"   # pred - truth(5)
            r = f"{M.fold_select_ols((x + c)[None, :], yy, 0)[0] - M.fold_select_ols(x[None, :], yy, 0)[0]:+.2e}"
        except RuntimeError as e:
            r = "RuntimeError (all degenerate)"
        print(f"  c={c:g} {name}: {r}")
# impossibility witness
a = 7.0 + np.arange(10) * np.spacing(7.0); b = (a - 7.0) / np.spacing(7.0)
print("\nimpossibility: (7 + k ulp(7) - 7)/ulp(7) == k exactly:", np.array_equal(b, np.arange(10.)))
