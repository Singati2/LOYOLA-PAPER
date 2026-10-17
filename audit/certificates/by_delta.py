"""Independent enumeration: for each maximum-degree bound D, the first tree order n at which two
distinct degree-pair profiles of trees with max degree <= D share a q-histogram. Unlabeled trees
(networkx.nonisomorphic_trees), exact rational q. Writes a certificate of all colliding classes."""
import networkx as nx, sys, json
from fractions import Fraction
from collections import Counter, defaultdict
NMAX=int(sys.argv[1]); first={}; cert={}
for n in range(2,NMAX+1):
    byhist=defaultdict(lambda: defaultdict(set))   # D -> hist -> profiles
    for T in nx.nonisomorphic_trees(n):
        d=dict(T.degree()); D=max(d.values())
        pairs=Counter(tuple(sorted((d[u],d[v]))) for u,v in T.edges())
        prof=tuple(sorted(pairs.items()))
        h=Counter()
        for (i,j),c in pairs.items(): h[Fraction(j-i,i+j)]+=c
        byhist[D][tuple(sorted(h.items()))].add(prof)
    Ds=sorted(byhist)
    for bound in [3,4,5,6,7,8,None]:          # None = no bound (all trees)
        merged=defaultdict(set)
        for D in Ds:
            if bound is None or D<=bound:
                for h,s in byhist[D].items(): merged[h]|=s
        bad=[(h,sorted(s)) for h,s in merged.items() if len(s)>1]
        if bad and bound not in first:
            first[bound]=n
            cert[f"{'all trees' if bound is None else 'D<='+str(bound)}, n={n}"]=[{"q_histogram":[[str(q),c] for q,c in h],"profiles":[[list(p) for p in prof] for prof in s]} for h,s in bad]
    print(n, {str(b):first[b] for b in first}, flush=True)
json.dump(cert,open(f"first_collisions_upto{NMAX}.json","w"),indent=1)
print("first order by max-degree bound (None = all trees; bounds absent from the dict: no collision up to NMAX):",{str(b):first[b] for b in first})
