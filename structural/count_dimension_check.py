#!/usr/bin/env python3
"""Affine dimension of edge-degree-pair count vectors and the collision error floor (v40.28).

Remark rem:countdim of the manuscript: for a tree of order n >= 3 with maximum degree at most 4,
m_11 = 0, sum m_ij = n - 1 and sum (1/i + 1/j) m_ij = n (each vertex is counted once through its
incident edges). The nine remaining coordinates therefore have affine dimension at most 7 at fixed
n and at most 8 when n varies. This script checks the identities on every tree of orders 3-12 and on
the three data sets, and computes the exact rank of the centred count matrix of the 18 octanes, the
34 measured decanes and the 100 pooled alkanes (expected 7, 7, 8).

It also computes the in-sample error floor of Proposition prop:collision for the octane boiling
points: any function of the count vector predicts equal values within a collision class, so its sum
of squared errors is at least the within-class sum of squares (expected 2.925, RMSE 0.403 degC).

Exit 1 on any failure. Output: count_dimension_check_out.txt.
"""
import csv, os, sys
from fractions import Fraction
import networkx as nx
import sympy as sp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
from octane_data import OCTANES, alkane_pairs

PAIRS = [(i, j) for i in range(1, 5) for j in range(i, 5)]
lines, ok = [], True


def counts(edges_pairs):
    c = [0] * len(PAIRS)
    for i, j in edges_pairs:
        c[PAIRS.index((min(i, j), max(i, j)))] += 1
    return c


def identities(c, n):
    m11 = c[PAIRS.index((1, 1))]
    s1 = sum(c)
    s2 = sum(Fraction(1, i) * k + Fraction(1, j) * k for (i, j), k in zip(PAIRS, c))
    return m11 == 0 and s1 == n - 1 and s2 == n


def rank_centred(rows):
    M = sp.Matrix(rows)
    mean = sp.Matrix([[sp.Rational(sum(M[:, k]), M.rows) for k in range(M.cols)]])
    return (M - sp.ones(M.rows, 1) * mean).rank()


bad = 0
for n in range(3, 13):
    for T in nx.nonisomorphic_trees(n):
        if max(d for _, d in T.degree()) > 4:
            continue
        deg = dict(T.degree())
        if not identities(counts([(deg[u], deg[v]) for u, v in T.edges()]), n):
            bad += 1
lines.append(f"identities m11 = 0, sum m = n - 1, sum (1/i+1/j) m = n on all trees of orders 3-12 with Delta <= 4: "
             f"{'hold' if bad == 0 else f'FAIL in {bad} trees'}")
ok &= bad == 0

octane = [counts(alkane_pairs(r[0])) for r in OCTANES]
bp = list(csv.DictReader(open(os.path.join(ROOT, "external", "bp", "bp_data.csv"))))
bp_c = [counts([tuple(int(t) for t in p.split("-")) for p in r["degree_pairs"].split()]) for r in bp]
bp_n = [int(r["n_C"]) for r in bp]
dec = [c for c, n in zip(bp_c, bp_n) if n == 10]
for name, rows, ns in (("octanes", octane, [8] * len(octane)), ("measured decanes", dec, [10] * len(dec)),
                       ("pooled C6-C10", bp_c, bp_n)):
    idok = all(identities(c, n) for c, n in zip(rows, ns))
    r = rank_centred(rows)
    lines.append(f"{name}: {len(rows)} molecules, identities {'hold' if idok else 'FAIL'}, rank of centred count matrix {r}")
    ok &= idok

exp = {"octanes": 7, "measured decanes": 7, "pooled C6-C10": 8}
for name, e in exp.items():
    got = int([l for l in lines if l.startswith(name + ":")][0].rsplit(" ", 1)[1])
    ok &= got == e

groups = {}
for c, r in zip(octane, OCTANES):
    groups.setdefault(tuple(c), []).append(Fraction(str(r[1])))
sse = sum(sum((y - sum(g) / len(g)) ** 2 for y in g) for g in groups.values())
rmse = (float(sse) / len(OCTANES)) ** 0.5
lines.append(f"octane T_B collision floor: {len(groups)} classes, within-class SSE {float(sse):.3f} degC^2, RMSE {rmse:.3f} degC")
ok &= f"{float(sse):.3f}" == "2.925" and f"{rmse:.3f}" == "0.403"
lines.append("RESULT: " + ("affine dimension bounds attained (7, 7, 8); octane T_B floor SSE 2.925, RMSE 0.403" if ok else "FAILURE"))
out = "\n".join(lines) + "\n"
print(out, end="")
open(os.path.join(HERE, "count_dimension_check_out.txt"), "w").write(out)
sys.exit(0 if ok else 1)
