#!/usr/bin/env python3
"""Independent referee check: tree enumeration, profiles, q-histograms,
first collision orders, GA merges, Randic counts, count-vector rank,
extremal trees. Exact rational arithmetic for profiles/histograms;
high-precision mpmath for irrational index values (equalities confirmed
symbolically with sympy when found)."""
import sys, json, itertools
from fractions import Fraction as F
from collections import Counter, defaultdict
import networkx as nx
import mpmath as mp
import sympy as sp

mp.mp.dps = 60
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 17

def profile(T):
    d = dict(T.degree())
    c = Counter()
    for u, v in T.edges():
        a, b = sorted((d[u], d[v]))
        c[(a, b)] += 1
    return tuple(sorted(c.items()))

def qhist(prof):
    h = Counter()
    for (i, j), m in prof:
        h[F(j - i, i + j)] += m
    return tuple(sorted(h.items()))

def maxdeg(prof):
    return max(j for (i, j), m in prof)

def mpval(prof, f):
    return mp.fsum(m * f(i, j) for (i, j), m in prof)

def symval(prof, f):
    return sp.nsimplify(sum(m * f(sp.Integer(i), sp.Integer(j)) for (i, j), m in prof))

def count_distinct(vals, tol=mp.mpf(10) ** -45):
    vs = sorted(vals)
    k = 0
    last = None
    groups = []
    for v in vs:
        if last is None or abs(v - last) > tol * max(1, abs(v)):
            k += 1
            groups.append([v])
        else:
            groups[-1].append(v)
        last = v
    return k

GA = lambda i, j: 2 * mp.sqrt(i * j) / (i + j)
GAs = lambda i, j: 2 * sp.sqrt(i * j) / (i + j)
RAN = lambda i, j: 1 / mp.sqrt(i * j)
def M(a, b, g):
    return lambda i, j: mp.power(i * j, a) * mp.power(i + j, b) * mp.e ** (g * mp.mpf(j - i) / (i + j))

out = {}
for n in range(2, NMAX + 1):
    trees = list(nx.nonisomorphic_trees(n)) if n >= 2 else []
    for cls in ("all", "chem"):
        profs = []
        for T in trees:
            p = profile(T)
            if cls == "chem" and maxdeg(p) > 4:
                continue
            profs.append(p)
        N = len(profs)
        P = set(profs)
        H = defaultdict(set)
        for p in P:
            H[qhist(p)].add(p)
        nh = len(H)
        coll = [sorted(s) for s in H.values() if len(s) > 1]
        rec = dict(N=N, profiles=len(P), histograms=nh, n_hist_collisions=len(coll))
        if coll and n <= 16:
            rec["example"] = [str(x) for x in coll[0]]
        # Randic distinct values over profiles
        if n >= 12:
            rv = [mpval(p, RAN) for p in P]
            rec["randic_distinct"] = count_distinct(rv)
            # GA merges of distinct histograms
            gav = {}
            for h, s in H.items():
                p = next(iter(s))
                gav[h] = mpval(p, GA)
            items = sorted(gav.items(), key=lambda t: t[1])
            merges = []
            for (h1, v1), (h2, v2) in zip(items, items[1:]):
                if abs(v1 - v2) < mp.mpf(10) ** -45:
                    p1 = next(iter(H[h1])); p2 = next(iter(H[h2]))
                    diff = sp.simplify(sp.radsimp(symval(p1, GAs) - symval(p2, GAs)))
                    merges.append((str(p1), str(p2), str(diff)))
            rec["GA_hist_merges"] = len(merges)
            if merges:
                rec["GA_merge_examples"] = merges[:3]
            rec["GA_distinct"] = count_distinct(list(gav.values()))
        if n == 16 and cls == "all":
            for lab, (a, b, g) in {"(0,1/2,0)": (0, mp.mpf(1) / 2, 0), "(0,1/3,0)": (0, mp.mpf(1) / 3, 0),
                                   "(0,1/2,1)": (0, mp.mpf(1) / 2, 1), "(0,1/3,1)": (0, mp.mpf(1) / 3, 1),
                                   "(1/2,0,0)": (mp.mpf(1) / 2, 0, 0), "(1/2,0,1)": (mp.mpf(1) / 2, 0, 1),
                                   "(-1/2,0,0)": (-mp.mpf(1) / 2, 0, 0), "(-1/2,0,1)": (-mp.mpf(1) / 2, 0, 1),
                                   "(0.3,0.2,0)": (mp.mpf('0.3'), mp.mpf('0.2'), 0)}.items():
                rec["distinct_" + lab] = count_distinct([mpval(p, M(a, b, g)) for p in P])
        # extremal trees for pure gamma, gamma = +-1 (orders 4..12)
        if cls == "all" and 4 <= n <= 12:
            for g in (1, -1, mp.mpf('0.3')):
                vals = [(mpval(profile(T), M(0, 0, g)), T) for T in trees]
                vals.sort(key=lambda t: t[0])
                lo, hi = vals[0], vals[-1]
                path = nx.is_isomorphic(lo[1], nx.path_graph(n)) if g > 0 else nx.is_isomorphic(lo[1], nx.star_graph(n - 1))
                star = nx.is_isomorphic(hi[1], nx.star_graph(n - 1)) if g > 0 else nx.is_isomorphic(hi[1], nx.path_graph(n))
                uniq = (vals[1][0] - lo[0] > 1e-40) and (hi[0] - vals[-2][0] > 1e-40)
                rec.setdefault("extremal_ok", []).append(bool(path and star and uniq))
        out[f"{n}_{cls}"] = rec
    print(n, out[f"{n}_all"], out[f"{n}_chem"], flush=True)

json.dump(out, open(sys.argv[2] if len(sys.argv) > 2 else "ref_trees_out.json", "w"), indent=1, default=str)
