"""Independent re-implementation of Test A (decane T_B) contrast LOh vs GM12.
Reads external/bp/bp_data.csv only; own descriptor, own nested LOO, own bootstrap."""
import csv, sys, numpy as np
path = sys.argv[1]
rows = [r for r in csv.DictReader(open(path)) if r["n_C"] == "10"]
P = [[tuple(map(int, x.split("-"))) for x in r["degree_pairs"].split()] for r in rows]
y = np.array([float(r["T_B_C"]) for r in rows]); n = len(y)
pairs = sorted({p for Pm in P for p in Pm})
C = np.array([[sum(1 for q in Pm if q == p) for p in pairs] for Pm in P], float)  # n x K counts
pi = np.array([p[0] for p in pairs], float); pj = np.array([p[1] for p in pairs], float)
def desc(T):
    a, b, g = T[:, 0:1], T[:, 1:2], T[:, 2:3]
    W = (pi * pj) ** a * (pi + pj) ** b * np.exp(g * np.abs(pi - pj) / (pi + pj))  # cand x K
    return W @ C.T  # cand x n
def inner_press_rmse(X, yt):
    # exact LOO residual of y = a + b x via leverage, per candidate row
    mu = X.mean(1, keepdims=True); sd = X.std(1, keepdims=True); Z = (X - mu) / np.where(sd > 0, sd, 1)
    m = X.shape[1]; Szz = (Z ** 2).sum(1, keepdims=True)
    b = (Z * (yt - yt.mean())).sum(1, keepdims=True) / np.where(Szz > 0, Szz, 1)
    res = yt - yt.mean() - b * Z
    h = 1.0 / m + Z ** 2 / np.where(Szz > 0, Szz, 1)
    r = np.sqrt(((res / (1 - h)) ** 2).mean(1))
    rel = (X.max(1) - X.min(1)) / np.abs(X).max(1)
    r[~np.isfinite(r) | (rel < 1e-9)] = np.inf
    return r
def nested(X):
    p = np.empty(n)
    for i in range(n):
        m = np.arange(n) != i
        k = int(np.argmin(inner_press_rmse(X[:, m], y[m])))
        xt = X[k, m]; A = np.column_stack([np.ones(n - 1), xt])
        co = np.linalg.lstsq(A, y[m], rcond=None)[0]
        p[i] = co[0] + co[1] * X[k, i]
    return p
def q2(p, yy): return 1 - ((p - yy) ** 2).sum() / ((yy - yy.mean()) ** 2).sum()
G, L, out = [], [], []
for s in range(50):
    rng = np.random.default_rng(s); B = 2000
    lo2 = np.round(rng.uniform(-2, 2, (B, 3)), 3)
    gm2 = np.column_stack([np.round(rng.uniform(-2, 2, (B, 2)), 3), np.zeros(B)])
    gm12 = np.column_stack([np.round(rng.uniform(-12, 12, (B, 2)), 3), np.zeros(B)])
    hy = np.round(np.column_stack([rng.uniform(-12, 12, (B, 2)), rng.uniform(-2, 2, B)]), 3)
    g = nested(desc(gm12)); l = nested(desc(hy)); G.append(g); L.append(l)
    out.append((s, q2(g, y), q2(l, y)))
    print(s, round(q2(g, y), 6), round(q2(l, y), 6), flush=True)
G, L = np.array(G), np.array(L)
d = np.array([b - a for _, a, b in out])
rng = np.random.default_rng(20261005); st = []
for _ in range(2000):
    idx = rng.integers(0, n, n); yy = y[idx]
    qg = 1 - ((G[:, idx] - yy) ** 2).sum(1) / ((yy - yy.mean()) ** 2).sum()
    ql = 1 - ((L[:, idx] - yy) ** 2).sum(1) / ((yy - yy.mean()) ** 2).sum()
    st.append(np.median(ql - qg))
print("n", n, "median GM12", np.median([a for _, a, _ in out]), "median LOh", np.median([b for _, _, b in out]))
print("median dQ2", np.median(d), "wins", int((d > 0).sum()), "CI", np.percentile(st, [2.5, 97.5]))
np.savetxt(sys.argv[2], np.array(out), delimiter=",", header="seed,Q2_GM12,Q2_LOh", fmt="%.10f")
