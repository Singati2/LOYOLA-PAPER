#!/usr/bin/env python3
"""Exploratory classical baseline (v40.29): Wiener's two-descriptor boiling-point model.

Wiener (J. Am. Chem. Soc. 69 (1947) 17-20) used the path number W and the polarity number p
(the number of pairs of carbon atoms three bonds apart, p3). This script rebuilds every decane
skeleton from its InChI connectivity layer (DATA/boiling_points_structures.csv), checks that the
rebuilt tree has the registered degree pairs, and reports the leave-one-out Q2 of ordinary least
squares on (1, W, p3) and on (1, W) for the 34 measured decanes. Nothing is tuned.
Output: wiener_baseline_out.txt.
"""
import csv, os, re
import numpy as np
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))


def tree(inchi):
    layer = [p for p in inchi.split("/") if p.startswith("c")][0][1:]
    G, stack, prev = nx.Graph(), [], None
    for t in re.findall(r"\d+|[()\-,]", layer):
        if t.isdigit():
            a = int(t); G.add_node(a)
            if prev is not None:
                G.add_edge(prev, a)
            prev = a
        elif t == "(":
            stack.append(prev)
        elif t == ")":
            prev = stack.pop()
        elif t == ",":
            prev = stack[-1]
    return G


def loo_q2(X, y):
    p = np.empty(len(y))
    for i in range(len(y)):
        m = np.arange(len(y)) != i
        p[i] = X[i] @ np.linalg.lstsq(X[m], y[m], rcond=None)[0]
    return 1 - ((y - p) ** 2).sum() / ((y - y.mean()) ** 2).sum()


bp = {r["nist_id"]: float(r["T_B_C"]) for r in csv.DictReader(open(os.path.join(HERE, "bp_data.csv")))}
rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "DATA", "boiling_points_structures.csv"))) if r["n_C"] == "10"]
W, P3, y, consistent = [], [], [], 0
for r in rows:
    G = tree(r["inchi_skeleton"])
    pairs = sorted(tuple(sorted((G.degree(a), G.degree(b)))) for a, b in G.edges())
    consistent += pairs == sorted(tuple(sorted(map(int, s.split("-")))) for s in r["degree_pairs"].split())
    d = dict(nx.all_pairs_shortest_path_length(G))
    W.append(sum(v for a in d for v in d[a].values()) / 2)
    P3.append(sum(1 for a in d for v in d[a].values() if v == 3) / 2)
    y.append(bp[r["nist_id"]])
W, P3, y = map(np.array, (W, P3, y))
one = np.ones(len(y))
assert consistent == len(rows), "rebuilt skeletons disagree with the registered degree pairs"
out = (f"decanes: {len(rows)}, rebuilt skeletons matching the registered degree pairs: {consistent}\n"
       f"Wiener W + p3, leave-one-out Q2 = {loo_q2(np.c_[one, W, P3], y):.4f}\n"
       f"W alone, leave-one-out Q2 = {loo_q2(np.c_[one, W], y):.4f}\n")
print(out, end="")
open(os.path.join(HERE, "wiener_baseline_out.txt"), "w").write(out)
