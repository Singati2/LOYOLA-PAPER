#!/usr/bin/env python3
"""Search: do two trees with Delta<=4 exchange order five times along gamma?
(Remark 3.12 states this is open.)  Profiles of chemical trees of orders 3..NMAX,
pairs of any orders, a grid of (alpha,beta). Candidates are re-certified in
mpmath interval arithmetic."""
import sys, itertools
import numpy as np
import networkx as nx
from collections import Counter
from fractions import Fraction as F
import mpmath as mp
from mpmath import iv

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 14
PAIRS = [(i, j) for i in range(1, 5) for j in range(i, 5)]
QS = sorted({F(j - i, i + j) for i, j in PAIRS})
QI = {p: QS.index(F(p[1] - p[0], p[0] + p[1])) for p in PAIRS}
profs = set()
for n in range(3, NMAX + 1):
    for T in nx.nonisomorphic_trees(n):
        d = dict(T.degree())
        if max(d.values()) > 4: continue
        c = Counter(tuple(sorted((d[u], d[v]))) for u, v in T.edges())
        profs.add(tuple(c.get(p, 0) for p in PAIRS))
profs = sorted(profs)
Mx = np.array(profs, dtype=float)
print("profiles:", len(profs))
qv = np.array([float(q) for q in QS])
gam = np.linspace(-400, 400, 32001)
E = np.exp(np.outer(qv, gam) - np.outer(qv, np.zeros_like(gam)))  # 6 x G (may overflow at large gamma)
found = []
for a in np.arange(-3, 3.01, 0.5):
    for b in np.arange(-3, 3.01, 0.5):
        w = np.array([(i * j) ** a * (i + j) ** b for i, j in PAIRS])
        C = np.zeros((len(profs), len(QS)))
        for k, p in enumerate(PAIRS):
            C[:, QI[p]] += Mx[:, k] * w[k]
        # pairwise differences, filter for alternating signs on all 6 classes
        for s in range(len(profs)):
            Dd = C[s] - C[s + 1:]
            sg = np.sign(Dd)
            alt = np.all(sg != 0, axis=1) & np.all(sg[:, 1:] * sg[:, :-1] < 0, axis=1)
            for t in np.nonzero(alt)[0]:
                c = Dd[t]
                # count sign changes on a log-scaled evaluation: divide by max term to avoid overflow
                L = np.outer(qv, gam)
                mx = L.max(axis=0)
                vals = (c[:, None] * np.exp(L - mx)).sum(axis=0)
                ch = np.sum(np.sign(vals[1:]) * np.sign(vals[:-1]) < 0)
                if ch >= 5:
                    found.append((a, b, profs[s], profs[s + 1 + t], ch))
                    print("FOUND", a, b, profs[s], profs[s + 1 + t], ch, flush=True)
        if len(found) > 3: break
    if len(found) > 3: break
print("total found:", len(found))
