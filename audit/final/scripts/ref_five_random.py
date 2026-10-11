#!/usr/bin/env python3
"""Exploratory: small integer difference vectors on the nine Delta<=4 tree pairs,
(alpha,beta) on a grid; does D(gamma) ever have five real zeros?"""
import numpy as np
rng = np.random.default_rng(1)
PAIRS = [(1,2),(1,3),(1,4),(2,2),(2,3),(2,4),(3,3),(3,4),(4,4)]
q = np.array([(j-i)/(i+j) for i,j in PAIRS])
QS = np.unique(q)
cls = np.array([np.where(np.isclose(QS, x))[0][0] for x in q])
gam = np.linspace(-600, 600, 24001)
L = np.outer(QS, gam); mx = L.max(axis=0); Ex = np.exp(L - mx)
best = 0; hits = []
grid = [(a, b) for a in np.arange(-6, 6.01, 0.5) for b in np.arange(-6, 6.01, 0.5)]
W = np.array([[ (i*j)**a * (i+j)**b for i,j in PAIRS] for a,b in grid])
for trial in range(40000):
    dm = rng.integers(-6, 7, size=9)
    C = np.zeros((len(grid), len(QS)))
    for k in range(9):
        C[:, cls[k]] += W[:, k] * dm[k]
    sg = np.sign(C)
    ok = np.all(sg != 0, axis=1) & np.all(sg[:, 1:] * sg[:, :-1] < 0, axis=1)
    for g in np.nonzero(ok)[0]:
        v = C[g] @ Ex
        ch = int(np.sum(np.sign(v[1:]) * np.sign(v[:-1]) < 0))
        if ch > best: best = ch; print("best", ch, dm.tolist(), grid[g], flush=True)
        if ch >= 5: hits.append((dm.tolist(), grid[g]))
    if len(hits) > 5: break
print("hits:", hits[:5])
