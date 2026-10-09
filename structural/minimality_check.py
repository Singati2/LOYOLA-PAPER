#!/usr/bin/env python3
"""Minimality certificate for Theorem 3.5(iii): exhaustive over ALL tree orders 2-16.

  python3 structural/minimality_check.py   (about one minute)

Output: structural/minimality_check_out.txt (committed).  Exit 1 if the first collision
orders are not 13 (all trees) and 16 (maximum degree at most 4).
"""
import os, sys
# Minimality certificate: for every order n, enumerate all non-isomorphic trees
# (networkx WROM generator; counts checked against OEIS A000055 and A000602) and test whether
# two distinct degree-pair profiles share a q-histogram (exact rationals).
import networkx as nx
from fractions import Fraction
from collections import Counter
A000055=[1,1,1,1,2,3,6,11,23,47,106,235,551,1301,3159,7741,19320]   # n=0..16
A000602=[1,1,1,1,2,3,5,9,18,35,75,159,355,802,1858,4347,10359]     # n=0..16 (alkanes, Delta<=4)
def first(chem):
    for n in range(2,17):
        trees=list(nx.nonisomorphic_trees(n))
        if chem: trees=[t for t in trees if max(d for _,d in t.degree())<=4]
        ref=(A000602 if chem else A000055)[n]
        assert len(trees)==ref,(n,len(trees),ref)
        prof2hist={}
        for t in trees:
            d=dict(t.degree())
            prof=tuple(sorted(Counter(tuple(sorted((d[u],d[v]))) for u,v in t.edges()).items()))
            hist=tuple(sorted(Counter(Fraction(abs(i-j),i+j) for (i,j),c in prof for _ in range(c)).items()))
            prof2hist[prof]=hist
        h=Counter(prof2hist.values())
        coll=[k for k,c in h.items() if c>1]
        print(("chem " if chem else "all  ")+f"n={n:2d} trees={len(trees):5d} profiles={len(prof2hist):5d} histograms={len(h):5d} colliding classes={len(coll)}")
LINES=[]
_print=print
def print(*a):
    LINES.append(" ".join(str(x) for x in a)); _print(*a)
first(False); first(True)
fa=min(int(l.split("n=")[1].split()[0]) for l in LINES if l.startswith("all") and not l.endswith("classes=0"))
fc=min(int(l.split("n=")[1].split()[0]) for l in LINES if l.startswith("chem") and not l.endswith("classes=0"))
print(f"RESULT: first order with distinct profiles sharing a q-histogram: {fa} (all trees), {fc} (maximum degree <= 4)")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "minimality_check_out.txt"), "w").write("\n".join(LINES) + "\n")
sys.exit(0 if (fa,fc)==(13,16) else 1)
