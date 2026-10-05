#!/usr/bin/env python3
"""EXPLORATORY (not pre-registered): fixed fractional parameter points.
(1) Discrimination: distinct values vs degree-pair profiles (the floor) for
    trees of order 12-16 (all) at fractional points with and without gamma.
(2) Prediction: nested-free leave-one-out Q2 of each FIXED point (no tuning),
    gamma = 1 versus the same (alpha, beta) with gamma = 0, on every dataset.
Writes fractional_points_out.txt."""
import csv, math, os, sys
from collections import Counter
import numpy as np, networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "external")); sys.path.insert(0, os.path.join(ROOT, "external", "bp"))
import baselines as B
from octane_data import OCTANES, PROPS, alkane_pairs
OUT = []
def log(*a):
    s = " ".join(map(str, a)); print(s, flush=True); OUT.append(s)
AB = [(0, .5), (.5, 0), (0, -.5), (-.5, 0), (.5, -1), (-.5, 1), (1/3, 0), (0, 1/3), (1/6, 0)]
def val(P, a, b, g): return sum((i*j)**a*(i+j)**b*math.exp(g*abs(i-j)/(i+j)) for i, j in P)
key = lambda x: float(f"{x:.11g}")
log("(1) distinct values / profiles, all trees")
for n in (12, 13, 14, 15, 16):
    Ps = [[tuple(sorted((T.degree(u), T.degree(v)))) for u, v in T.edges()] for T in nx.nonisomorphic_trees(n)]
    prof = len({tuple(sorted(Counter(P).items())) for P in Ps})
    row = [f"n={n} profiles={prof}"]
    for a, b in AB:
        for g in (0, 1):
            row.append(f"({a:.3g},{b:.3g},{g}):{len({key(val(P,a,b,g)) for P in Ps})}")
    log("  " + " ".join(row))
def loo_q2(x, y):
    p = np.array([B.fit_predict(np.delete(x, i), np.delete(y, i), x[i]) for i in range(len(y))])
    return B.scores(p, y)[0]
def loo_q2_size(x, z, y):
    import bp_tests as T
    p = np.array([T.fit_pred_size(np.delete(x, i), np.delete(z, i), np.delete(y, i), x[i], z[i]) for i in range(len(y))])
    return B.scores(p, y)[0]
sets = []
P8 = [alkane_pairs(r[0]) for r in OCTANES]
for k, p in enumerate(PROPS): sets.append((f"octane {p}", P8, np.array([r[1+k] for r in OCTANES]), None))
rows9 = list(csv.DictReader(open(os.path.join(ROOT, "external", "nonane_data.csv"))))
for p, col in (("T_B", "T_B_C"), ("dHvap", "dHvap_kcal")):
    kk = [r for r in rows9 if r[col].strip()]
    sets.append((f"nonane {p}", [alkane_pairs(r["smiles"]) for r in kk], np.array([float(r[col]) for r in kk]), None))
bp = list(csv.DictReader(open(os.path.join(ROOT, "external", "bp", "bp_data.csv"))))
pp = lambda r: [tuple(map(int, e.split("-"))) for e in r["degree_pairs"].split()]
dec = [r for r in bp if r["n_C"] == "10"]
sets.append(("decane T_B", [pp(r) for r in dec], np.array([float(r["T_B_C"]) for r in dec]), None))
sets.append(("pooled C6-C10 T_B (+n_C)", [pp(r) for r in bp], np.array([float(r["T_B_C"]) for r in bp]), np.array([float(r["n_C"]) for r in bp])))
log("(2) LOO Q2 of fixed points: gamma=0 -> gamma=1 (difference)")
wins = 0; tot = 0
for name, P, y, z in sets:
    cells = []
    for a, b in AB:
        q = []
        for g in (0, 1):
            x = np.array([val(Pi, a, b, g) for Pi in P])
            q.append(loo_q2_size(x, z, y) if z is not None else loo_q2(x, y))
        cells.append(f"({a:.3g},{b:.3g}):{q[0]:.3f}->{q[1]:.3f}({q[1]-q[0]:+.3f})"); wins += q[1] > q[0]; tot += 1
    log(f"  {name}: " + " ".join(cells))
log(f"gamma=1 better than gamma=0 at the same fractional (alpha,beta): {wins} of {tot} cases")
open(os.path.join(HERE, "fractional_points_out.txt"), "w").write("\n".join(OUT) + "\n")
