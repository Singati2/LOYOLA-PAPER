"""Independent helpers for counterexample verification (written fresh, no repo code)."""
from fractions import Fraction
from collections import Counter
import math

def qf(i, j):
    """exact imbalance |i-j|/(i+j) as Fraction"""
    return Fraction(abs(i - j), i + j)

def profile_of_degrees(edges, deg):
    c = Counter()
    for u, v in edges:
        a, b = sorted((deg[u], deg[v]))
        c[(a, b)] += 1
    return tuple(sorted(c.items()))

def profile_of_graph(G):
    deg = dict(G.degree())
    return profile_of_degrees(G.edges(), deg)

def qhist(profile):
    c = Counter()
    for (i, j), m in profile:
        c[qf(i, j)] += m
    return tuple(sorted(c.items()))

def maxdeg(profile):
    return max(j for (i, j), m in profile)

def nvert(profile):
    s = sum(m * (Fraction(1, i) + Fraction(1, j)) for (i, j), m in profile)
    return s

def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

_fcache = {}
def fac(n):
    if n not in _fcache:
        _fcache[n] = factorize(n)
    return _fcache[n]

def radical_term(i, j, a, b, k):
    """(ij)^a (i+j)^b = coef * N^(1/k), N k-th-power-free; a,b Fractions with k*a, k*b integers.
    Returns (N, coef Fraction)."""
    exps = {}
    for p, e in fac(i * j).items():
        exps[p] = exps.get(p, 0) + a * e
    for p, e in fac(i + j).items():
        exps[p] = exps.get(p, 0) + b * e
    coef = Fraction(1)
    N = 1
    for p, e in exps.items():
        e = Fraction(e)
        fl = math.floor(e)
        fr = e - fl                      # in [0,1)
        assert (fr * k).denominator == 1
        coef *= Fraction(p) ** fl
        N *= p ** int(fr * k)
    return N, coef

def radical_key(profile, a, b, k, per_q=False):
    """Exact key of M_{a,b}=sum m_ij (ij)^a (i+j)^b in the Q-basis {N^(1/k)} (Besicovitch).
    If per_q: key of the per-imbalance-class coefficients c_q (what decides LO at algebraic gamma != 0)."""
    d = {}
    for (i, j), m in profile:
        N, c = radical_term(i, j, a, b, k)
        kk = (qf(i, j), N) if per_q else N
        d[kk] = d.get(kk, 0) + m * c
    return tuple(sorted((kk, v) for kk, v in d.items() if v != 0))

def lo_mp(profile, a, b, g, mp):
    s = mp.mpf(0)
    for (i, j), m in profile:
        s += m * mp.power(i * j, a) * mp.power(i + j, b) * mp.e ** (g * mp.mpf(abs(i - j)) / (i + j))
    return s

def count_distinct_mp(values, tol):
    vs = sorted(values)
    k = 1
    mingap = None
    for x, y in zip(vs, vs[1:]):
        d = y - x
        if d > tol:
            k += 1
            mingap = d if mingap is None or d < mingap else mingap
    return k, mingap

def ahu(adj, root, parent=None):
    ch = sorted(ahu(adj, c, root) for c in adj[root] if c != parent)
    return "(" + "".join(ch) + ")"

def tree_canon(adj):
    """canonical string of a tree (centre-rooted AHU)."""
    n = len(adj)
    if n == 1:
        return "()"
    deg = {v: len(adj[v]) for v in adj}
    leaves = [v for v in adj if deg[v] <= 1]
    rem = n
    while rem > 2:
        rem -= len(leaves)
        nl = []
        for v in leaves:
            for u in adj[v]:
                deg[u] -= 1
                if deg[u] == 1:
                    nl.append(u)
            deg[v] = 0
        leaves = nl
    return min(ahu(adj, c) for c in leaves) if len(leaves) == 1 else \
        "E" + "".join(sorted([ahu(adj, leaves[0], leaves[1]), ahu(adj, leaves[1], leaves[0])]))
