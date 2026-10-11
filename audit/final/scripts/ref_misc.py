#!/usr/bin/env python3
"""Independent referee checks: count-vector identities and ranks, octane
collision floor, five-crossing certificate (interval arithmetic), Example 4.4,
Lemma 3.1 determinants, Delta=7 remark, Remark 3.9 example."""
import sys, csv, itertools, re
ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))))
from fractions import Fraction as F
from collections import Counter
import networkx as nx
import mpmath as mp
from mpmath import iv

sys.path.insert(0, ROOT)
PAIRS = [(i, j) for i in range(1, 5) for j in range(i, 5)]   # 10 pairs, Delta<=4

def rank_exact(rows):
    """Rank of a list of rational vectors (Gaussian elimination in Fractions)."""
    M = [[F(x) for x in r] for r in rows]
    rk, col = 0, 0
    ncol = len(M[0]) if M else 0
    while rk < len(M) and col < ncol:
        piv = next((r for r in range(rk, len(M)) if M[r][col] != 0), None)
        if piv is None:
            col += 1; continue
        M[rk], M[piv] = M[piv], M[rk]
        for r in range(len(M)):
            if r != rk and M[r][col] != 0:
                f = M[r][col] / M[rk][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[rk])]
        rk += 1; col += 1
    return rk

def affine_rank(vecs):
    vecs = list(vecs)
    v0 = vecs[0]
    return rank_exact([[a - b for a, b in zip(v, v0)] for v in vecs[1:]]) if len(vecs) > 1 else 0

def countvec(T):
    d = dict(T.degree()); c = Counter()
    for u, v in T.edges():
        c[tuple(sorted((d[u], d[v])))] += 1
    return c

# ---------- 1. countdim on all Delta<=4 trees, n = 3..17 ----------
print("== Remark countdim: identities and affine dimension of Delta<=4 tree count vectors ==")
allvecs = []
for n in range(3, 18):
    vecs = set(); ok = True
    for T in nx.nonisomorphic_trees(n):
        c = countvec(T)
        if max(j for (i, j) in c) > 4:
            continue
        v = tuple(c.get(p, 0) for p in PAIRS)
        if c.get((1, 1), 0) != 0: ok = False
        if sum(v) != n - 1: ok = False
        if sum((F(1, i) + F(1, j)) * c.get((i, j), 0) for (i, j) in PAIRS) != n: ok = False
        vecs.add(v[1:])  # drop m11
    allvecs.extend(vecs)
    print(f"n={n:2d} distinct={len(vecs):5d} identities_ok={ok} affine_dim={affine_rank(vecs)}")
print("pooled n=3..17 affine dim:", affine_rank(set(allvecs)))

# ---------- 2. data sets: octanes, decanes, pooled ----------
def smiles_graph(s):
    G = nx.Graph(); stack = []; prev = None; idx = 0
    for ch in s:
        if ch == 'C':
            G.add_node(idx)
            if prev is not None: G.add_edge(prev, idx)
            prev = idx; idx += 1
        elif ch == '(':
            stack.append(prev)
        elif ch == ')':
            prev = stack.pop()
        else:
            raise ValueError(s)
    return G
from octane_data import OCTANES, NAMES
oct_vecs = []
classes = {}
for (smi, tb, *_), name in zip(OCTANES, NAMES):
    G = smiles_graph(smi); assert nx.is_tree(G) and G.number_of_nodes() == 8
    c = countvec(G); v = tuple(c.get(p, 0) for p in PAIRS)
    oct_vecs.append(v[1:]); classes.setdefault(v, []).append((name, F(str(tb))))
print("\n== Octanes ==")
print("distinct count vectors:", len(classes), " centred rank:", affine_rank(oct_vecs))
union = sorted({p for v in classes for p, m in zip(PAIRS, v) if m})
print("union of pairs:", union, len(union))
sse = F(0)
for v, mem in classes.items():
    if len(mem) > 1:
        mean = sum(t for _, t in mem) / len(mem)
        ss = sum((t - mean) ** 2 for _, t in mem)
        sse += ss
        print("  collision class", dict(zip(PAIRS, v)), [(n_, float(t)) for n_, t in mem], "SS=", ss)
print("within-class SSE =", sse, float(sse), " RMSE =", mp.sqrt(mp.mpf(sse.numerator) / sse.denominator / 18))
# affine dimension of z_ij over octane union
mp.mp.dps = 50
def z(i, j): return [mp.log(i * j), mp.log(i + j), mp.mpf(j - i) / (i + j)]
Z = [z(*p) for p in union]
A = mp.matrix([[a - b for a, b in zip(r, Z[0])] for r in Z[1:]])
sv = mp.svd_r(A, compute_uv=False)
print("singular values of centred z over octane union:", [mp.nstr(s, 5) for s in sv])

rows = list(csv.DictReader(open(__import__('os').path.join(ROOT,'external','bp','bp_data.csv'))))
def vec_from(dp):
    c = Counter(tuple(sorted(map(int, t.split('-')))) for t in dp.split())
    return c
dec = []; pooled = []; bad = 0
for r in rows:
    c = vec_from(r['degree_pairs']); n = int(r['n_C'])
    v = tuple(c.get(p, 0) for p in PAIRS)
    if sum(v) != n - 1 or sum((F(1, i) + F(1, j)) * m for (i, j), m in zip(PAIRS, v)) != n: bad += 1
    pooled.append(v[1:])
    if n == 10: dec.append(v[1:])
print("\n== bp_data.csv ==  rows:", len(rows), " identity violations:", bad)
print("decanes:", len(dec), " centred rank:", affine_rank(dec))
print("pooled:", len(pooled), " centred rank:", affine_rank(pooled))
print("carbon counts:", Counter(int(r['n_C']) for r in rows))

# ---------- 3. five-crossing certificate ----------
print("\n== Remark 3.12 five crossings at (alpha,beta)=(-1,0) ==")
T1 = {(1, 3): 2, (1, 4): 2, (1, 6): 5, (3, 4): 1, (4, 6): 1}
T2 = {(1, 2): 1, (1, 5): 4, (1, 6): 4, (2, 6): 1, (5, 6): 1}
for T in (T1, T2):
    assert sum(T.values()) == 11 and sum((F(1, i) + F(1, j)) * m for (i, j), m in T.items()) == 12
coef = Counter()
for T, s in ((T1, 1), (T2, -1)):
    for (i, j), m in T.items():
        coef[F(j - i, i + j)] += s * m * F(1, i * j)
cs = sorted(coef.items())
print("coefficients by q:", [(str(q), str(c)) for q, c in cs])
signs = [c > 0 for q, c in cs if c != 0]
V = sum(a != b for a, b in zip(signs, signs[1:])); print("sign changes V =", V, " distinct q =", len(cs))
iv.dps = 50
def Div(g):
    return iv.fsum([iv.mpf(c.numerator) / c.denominator * iv.exp(g * iv.mpf(q.numerator) / q.denominator) for q, c in cs])
def Dmp(g):
    return mp.fsum([mp.mpf(c.numerator) / c.denominator * mp.exp(g * mp.mpf(q.numerator) / q.denominator) for q, c in cs])
def bis(a, b):
    fa = Dmp(a)
    for _ in range(120):
        c = (a + b) / 2; fc = Dmp(c)
        if fa * fc <= 0: b = c
        else: a, fa = c, fc
    return (a + b) / 2
grid = [mp.mpf(x) / 10 for x in range(-400, 400)]
roots = []
for a, b in zip(grid, grid[1:]):
    if Dmp(a) * Dmp(b) < 0:
        r = bis(a, b)
        roots.append(r)
print("approx roots:", [mp.nstr(r, 6) for r in roots])
# rigorous sign certification at bracket endpoints
cert = []
for r in roots:
    lo, hi = r - mp.mpf('1e-6'), r + mp.mpf('1e-6')
    a, b = Div(iv.mpf(lo)), Div(iv.mpf(hi))
    cert.append((a.b < 0 and b.a > 0) or (a.a > 0 and b.b < 0))
print("interval sign change certified at each root:", cert, " total =", sum(cert))
print("sign at -inf: first coef", cs[0][1], " +inf: last coef", cs[-1][1])

# ---------- 4. Example 4.4 ----------
print("\n== Example 4.4 ==")
def Dex(g):
    g = mp.mpf(g)
    return 3 * (mp.exp(g / 2) - 1) - 4 / mp.sqrt(5) * (mp.exp(3 * g / 5) - mp.exp(g / 5)) + 4 / mp.sqrt(6) * (1 - mp.exp(g / 3))
print("D(0)=", Dex(0), " D(1)=", mp.nstr(Dex(1), 6), " D(1e-6)=", mp.nstr(Dex(mp.mpf('1e-6')), 6))
dm = {(1, 3): 6, (2, 3): 4, (3, 3): 4, (1, 4): -4, (2, 2): -6, (2, 4): -4}
def Dgen(g):
    return mp.fsum(m * mp.power(i + j, -0.5) * mp.exp(g * mp.mpf(j - i) / (i + j)) for (i, j), m in dm.items())
print("from count difference: D(1)=", mp.nstr(Dgen(1), 8), " D(1e-6)=", mp.nstr(Dgen(mp.mpf('1e-6')), 6))
print("  sum m diff", sum(dm.values()), " sum (1/i+1/j) m diff", sum((F(1, i) + F(1, j)) * m for (i, j), m in dm.items()))

# ---------- 5. Lemma 3.1 determinants ----------
print("\n== Lemma 3.1 ==")
def aug(i, j): return [1, mp.log(i * j), mp.log(i + j), mp.mpf(j - i) / (i + j)]
print("det3 (1,1),(2,2),(1,2):", mp.det(mp.matrix([aug(1,1)[:3], aug(2,2)[:3], aug(1,2)[:3]])), " ln2 ln(9/8)=", mp.log(2) * mp.log(mp.mpf(9) / 8))
d4 = mp.det(mp.matrix([aug(1,2), aug(1,3), aug(2,2), aug(3,3)]))
print("det4 (1,2),(1,3),(2,2),(3,3):", mp.nstr(d4, 10), " claimed:", mp.nstr(-mp.log(mp.mpf(3)/2) * mp.log(mp.mpf(2)**13 / 3**8) / 6, 10))
print("det W:", mp.nstr(mp.det(mp.matrix([aug(1,1), aug(2,2), aug(1,2), aug(1,3)])), 10), mp.nstr(mp.log(2)*(8*mp.log(3)-13*mp.log(2))/6, 10))
qd2 = lambda i, j: (mp.log(i + j) - mp.log(2) - mp.log(i * j) / 2) / (3 * mp.log(3) - mp.mpf(9) / 2 * mp.log(2))
print("Delta=2 q formula:", [mp.nstr(qd2(*p), 8) for p in [(1,1),(1,2),(2,2)]])

# ---------- 6. Remark 3.14: A(S) = min(|S|-1, r, 3) for subsets of P_Delta ----------
print("\n== Remark 3.14 (equality in Prop 3.13(ii)) ==")
mp.mp.dps = 40
def Aset(S):
    Z = [z(*p) for p in S]
    if len(Z) == 1: return 0
    A = mp.matrix([[a - b for a, b in zip(r, Z[0])] for r in Z[1:]])
    sv = mp.svd_r(A, compute_uv=False)
    return sum(1 for s in sv if s > mp.mpf(10) ** -25), min(sv)
for Dl in range(2, 9):
    P = [(i, j) for i in range(1, Dl + 1) for j in range(i, Dl + 1)]
    viol = []; minsv = mp.inf
    for k in range(2, 5):
        for S in itertools.combinations(P, k):
            r = len({F(j - i, i + j) for i, j in S})
            bound = min(k - 1, r, 3)
            Ar, ms = Aset(S)
            if Ar == bound: minsv = min(minsv, ms) if Ar == min(k-1, 3) else minsv
            if Ar < bound: viol.append(S)
    print(f"Delta={Dl}: subsets<=4 violating equality: {viol[:6]}{' ...' if len(viol)>6 else ''} (count {len(viol)})")

# ---------- 7. Remark 3.9 example ----------
print("\n== Remark 3.9 ==  LO(K4;0,0,ln4)=6, LO(K13;0,0,ln4)=", 3 * mp.exp(mp.log(4) / 2))
# ---------- 8. Remark 3.7: parent on Pi at gamma=0 bases ----------
print("bases (1-q^2)/4 distinct for distinct q in [0,1): q -> (1-q^2)/4 is strictly decreasing on [0,1)")
