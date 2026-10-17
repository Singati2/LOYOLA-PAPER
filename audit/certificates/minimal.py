"""Independent check (not the repository's code): first tree order with two distinct degree-pair
profiles sharing a q-histogram, for all trees and for trees with max degree <= 4."""
import networkx as nx, sys
from fractions import Fraction
from collections import Counter, defaultdict
def first(nmax):
    out={}
    for n in range(2,nmax+1):
        byhist={"all":defaultdict(set),"chem":defaultdict(set)}
        for T in nx.nonisomorphic_trees(n):
            d=dict(T.degree())
            pairs=Counter(tuple(sorted((d[u],d[v]))) for u,v in T.edges())
            prof=tuple(sorted(pairs.items()))
            hist=Counter()
            for (i,j),c in pairs.items(): hist[Fraction(j-i,i+j)]+=c
            h=tuple(sorted(hist.items()))
            byhist["all"][h].add(prof)
            if max(d.values())<=4: byhist["chem"][h].add(prof)
        for k in ("all","chem"):
            bad=sum(1 for s in byhist[k].values() if len(s)>1)
            nprof=len(set().union(*byhist[k].values()))
            if bad and k not in out: out[k]=n
            print(n,k,"profiles",nprof,"histograms",len(byhist[k]),"classes with >1 profile",bad,flush=True)
    return out
print(first(int(sys.argv[1])))
