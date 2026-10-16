#!/usr/bin/env python3
"""Independent recount of Table 2 (tab:firstfail) and its footnotes (v40.30 audit).
Trees from networkx.nonisomorphic_trees (complete against OEIS for n <= 17); profiles and q-histograms
exact; index values at 40 digits (mpmath), counted as distinct when they differ by more than 1e-30.
For each order 7..17 (all trees) and 7..17 (max degree <= 4): profiles, q-histograms, and distinct values
of LO(0,0,1), LO(0,0,2), R = M_{-1/2,0} and GA. Reports the first order "below floor" (values < profiles)
and the first order at which GA gives equal values to two different q-histograms ("merges").
  python3 audit/v4030/table2_independent.py   -> table2_independent_out.txt
"""
import os
from collections import Counter
from fractions import Fraction
import networkx as nx, mpmath as mp
mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
def profile(T):
    d = dict(T.degree()); return tuple(sorted(Counter(tuple(sorted((d[u], d[v]))) for u, v in T.edges()).items()))
def qh(P):
    h = Counter()
    for (i, j), c in P: h[Fraction(j - i, i + j)] += c
    return tuple(sorted(h.items()))
IDX = {"LO(0,0,1)": lambda i, j: mp.e ** (mp.mpf(j - i) / (i + j)), "LO(0,0,2)": lambda i, j: mp.e ** (2 * mp.mpf(j - i) / (i + j)),
       "R": lambda i, j: 1 / mp.sqrt(i * j), "GA": lambda i, j: 2 * mp.sqrt(i * j) / (i + j)}
def ndistinct(vals):
    vals = sorted(vals); k = 1
    for a, b in zip(vals, vals[1:]):
        if abs(b - a) > mp.mpf(10) ** -30: k += 1
    return k
out = []; first = {}
for n in range(7, 18):
    trees = list(nx.nonisomorphic_trees(n))
    for chem in (False, True):
        profs = {profile(T) for T in trees if not chem or max(dict(T.degree()).values()) <= 4}
        hists = {qh(P) for P in profs}
        row = {"profiles": len(profs), "histograms": len(hists)}
        for k, f in IDX.items():
            row[k] = ndistinct([sum(c * f(i, j) for (i, j), c in P) for P in profs])
            if row[k] < len(profs) and (k, chem) not in first: first[(k, chem)] = (n, row[k], len(profs))
        ga_by_hist = {}
        for P in profs: ga_by_hist.setdefault(qh(P), sum(c * IDX["GA"](i, j) for (i, j), c in P))
        if ndistinct(list(ga_by_hist.values())) < len(ga_by_hist) and ("GA merges", chem) not in first: first[("GA merges", chem)] = (n,)
        out.append(f"n={n:2} {'maxdeg<=4' if chem else 'all     '} " + " ".join(f"{k}={v}" for k, v in row.items()))
        print(out[-1], flush=True)
out.append("FIRST below floor / merges: " + "; ".join(f"{k} {'maxdeg<=4' if c else 'all'}: {v}" for (k, c), v in sorted(first.items(), key=str)))
print(out[-1])
open(os.path.join(HERE, "table2_independent_out.txt"), "w").write("\n".join(out) + "\n")
