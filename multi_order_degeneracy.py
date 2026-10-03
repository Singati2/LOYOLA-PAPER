#!/usr/bin/env python3
"""Multi-order degeneracy audit for 12 vertex-degree-based indices on trees.

For each n in 7..12, enumerate all nonisomorphic trees and the molecular
subset (max degree <= 4). For each set report: N trees, the number of
distinct BID edge-degree-pair profiles (theoretical discrimination floor
for ALL vertex-degree-based / bond-incident-degree indices), and the number
of distinct values (rounded to 9 decimals) attained by each of 12 indices
parameterized as logr(G, a, b, g) = sum_{uv in E} (du dv)^a (du+dv)^b
* exp(g |du-dv| / (du+dv)).

Output: multi_order_degeneracy.csv
"""
import csv
import math
import os
from collections import Counter

import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))

INDICES = [
    ("M1", (0, 1, 0)),
    ("M2", (1, 0, 0)),
    ("HM", (0, 2, 0)),
    ("mM2", (-1, 0, 0)),
    ("R", (-0.5, 0, 0)),
    ("chi", (0, -0.5, 0)),
    ("H2", (0, -1, 0)),
    ("ISI", (1, -1, 0)),
    ("GA", (0.5, -1, 0)),
    ("AG", (-0.5, 1, 0)),
    ("LO001", (0, 0, 1)),
    ("LO002", (0, 0, 2)),
]


def logr(G, a, b, g):
    return sum((G.degree(u) * G.degree(v)) ** a * (G.degree(u) + G.degree(v)) ** b
               * math.exp(g * abs(G.degree(u) - G.degree(v)) / (G.degree(u) + G.degree(v)))
               for u, v in G.edges())


def bid_profile(G):
    """Sorted multiset of sorted edge degree pairs."""
    return tuple(sorted(Counter(tuple(sorted((G.degree(u), G.degree(v))))
                                for u, v in G.edges()).items()))


def audit(trees):
    row = {"N_trees": len(trees),
           "distinct_BID_profiles": len(set(bid_profile(T) for T in trees))}
    for name, (a, b, g) in INDICES:
        row[name] = len(set(round(logr(T, a, b, g), 9) for T in trees))
    return row


def main():
    fieldnames = ["n", "graph_set", "N_trees", "distinct_BID_profiles"] + [nm for nm, _ in INDICES]
    out_path = os.path.join(HERE, "multi_order_degeneracy.csv")
    rows = []
    for n in range(7, 13):
        all_trees = list(nx.nonisomorphic_trees(n))
        molecular = [T for T in all_trees if max(d for _, d in T.degree()) <= 4]
        for set_name, trees in [("all_trees", all_trees), ("molecular", molecular)]:
            r = {"n": n, "graph_set": set_name}
            r.update(audit(trees))
            rows.append(r)
    with open(out_path, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # Report + sanity checks.
    print(f"wrote {out_path}")
    ok_floor = True
    for r in rows:
        floor = r["distinct_BID_profiles"]
        for nm, _ in INDICES:
            if r[nm] > floor:
                ok_floor = False
                print(f"FLOOR VIOLATION: n={r['n']} {r['graph_set']} {nm}: "
                      f"{r[nm]} > {floor}")
        lo1 = "FLOOR" if r["LO001"] == floor else f"BELOW({r['LO001']})"
        lo2 = "FLOOR" if r["LO002"] == floor else f"BELOW({r['LO002']})"
        print(f"n={r['n']:2d} {r['graph_set']:9s} N={r['N_trees']:3d} "
              f"BID_floor={floor:3d} LO001={lo1} LO002={lo2}")
    print("sanity: no index exceeds BID floor" if ok_floor
          else "sanity FAILED: some index exceeds BID floor")


if __name__ == "__main__":
    main()
