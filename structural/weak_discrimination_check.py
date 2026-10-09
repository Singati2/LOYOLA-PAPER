#!/usr/bin/env python3
"""Exhaustive check of the weak-discrimination theorem (Theorem thm:weakdisc of main.tex).

For every chemical tree (maximum degree <= 4) of orders 4-18 and every connected graph with
maximum degree <= 4 on 3-7 vertices (networkx graph atlas), the degree-pair profiles are
collected and LO is evaluated at 50 significant digits.  'merges' = number of distinct
profiles minus number of distinct values at that order.  The theorem predicts 0 merges at
every point with 2*alpha + beta not an integer and gamma != 0.

  python3 structural/weak_discrimination_check.py     (about 15 s)

Output: structural/weak_discrimination_check_out.txt (committed).  Exit 1 if a point with
non-integer 2*alpha + beta merges two profiles.
"""
import os, sys
from collections import Counter
import networkx as nx
from mpmath import mp, mpf, exp, power
mp.dps = 50
H = mpf(1) / 2; T = mpf(1) / 3; Q = mpf(1) / 4
POINTS = [("(0,1/2,1)", (0, H, 1), False), ("(0,-1/2,1)", (0, -H, 1), False), ("(0,1/3,1)", (0, T, 1), False),
          ("(1/4,0,1)", (Q, 0, 1), False), ("(0,1/2,2)", (0, H, 2), False), ("(1/3,0,-1)", (T, 0, -1), False),
          ("(0,1,1)", (0, 1, 1), True), ("(1/2,0,1)", (H, 0, 1), True), ("(-1/2,0,1)", (-H, 0, 1), True),
          ("(0,-1,1)", (0, -1, 1), True), ("(1,-1,1)", (1, -1, 1), True), ("(0,0,1)", (0, 0, 1), True),
          ("(0,1/2,0)", (0, H, 0), True), ("(0,-1/2,0)", (0, -H, 0), True)]


def profile(G):
    d = dict(G.degree())
    return tuple(sorted(Counter(tuple(sorted((d[u], d[v]))) for u, v in G.edges()).items()))


def merges(profs):
    out = []
    for name, (a, b, g), _ in POINTS:
        vals = {mp.nstr(sum(c * power(i * j, a) * power(i + j, b) * exp(g * mpf(j - i) / (i + j)) for (i, j), c in p), 40) for p in profs}
        out.append(len(profs) - len(vals))
    return out


def main():
    lines = ["columns: " + " ".join(n for n, _, _ in POINTS) + "   (last eight: 2*alpha+beta integer, or gamma = 0)"]
    bad = 0
    for n in range(4, 19):
        profs = {profile(T_) for T_ in nx.nonisomorphic_trees(n) if max(dict(T_.degree()).values()) <= 4}
        m = merges(profs); lines.append(f"chemical trees n={n:2d} profiles={len(profs):5d} merges " + " ".join(map(str, m)))
        bad += sum(x for x, (_, _, integer) in zip(m, POINTS) if not integer)
    by_n = {}
    for G in nx.graph_atlas_g():
        if 3 <= G.number_of_nodes() <= 7 and nx.is_connected(G) and max(dict(G.degree()).values()) <= 4:
            by_n.setdefault(G.number_of_nodes(), set()).add(profile(G))
    for n in sorted(by_n):
        m = merges(by_n[n]); lines.append(f"connected graphs n={n} profiles={len(by_n[n]):5d} merges " + " ".join(map(str, m)))
        bad += sum(x for x, (_, _, integer) in zip(m, POINTS) if not integer)
    lines.append("RESULT: " + ("no merge at any point with non-integer 2*alpha+beta" if bad == 0 else f"{bad} MERGES at non-integer points"))
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "weak_discrimination_check_out.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
