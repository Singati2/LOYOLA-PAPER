#!/usr/bin/env python3
"""Sum-connectivity index chi = LO(0,-1/2,0): distinct values vs degree-pair
profiles for all trees of orders 7-12 (values distinct at 11 significant
digits, as in all counts of the paper). Writes chi_floor_out.txt."""
import math, os
from collections import Counter
import networkx as nx
HERE = os.path.dirname(os.path.abspath(__file__)); out = []
for n in range(7, 13):
    Ps = [[tuple(sorted((T.degree(u), T.degree(v)))) for u, v in T.edges()] for T in nx.nonisomorphic_trees(n)]
    prof = len({tuple(sorted(Counter(P).items())) for P in Ps})
    chi = len({float(f"{sum((i + j) ** -0.5 for i, j in P):.11g}") for P in Ps})
    out.append(f"n={n} profiles={prof} chi_distinct={chi}"); print(out[-1])
open(os.path.join(HERE, "chi_floor_out.txt"), "w").write("\n".join(out) + "\n")
