"""First tree order at which SDD = sum(i/j + j/i) or ISDD = sum ij/(i^2+j^2), in exact rationals,
gives equal values to trees with distinct degree-pair profiles (all trees / max degree <= 4)."""
import networkx as nx
from fractions import Fraction as F
from collections import Counter, defaultdict
w={"SDD":lambda i,j:F(i,j)+F(j,i),"ISDD":lambda i,j:F(i*j,i*i+j*j)}
first={}
for n in range(3,14):
    for name,f in w.items():
        for cls in ("all","chem"):
            vals=defaultdict(set)
            for T in nx.nonisomorphic_trees(n):
                d=dict(T.degree())
                if cls=="chem" and max(d.values())>4: continue
                prof=tuple(sorted(Counter(tuple(sorted((d[u],d[v]))) for u,v in T.edges()).items()))
                vals[sum(f(i,j)*c for (i,j),c in prof)].add(prof)
            bad=[s for s in vals.values() if len(s)>1]
            if bad and (name,cls) not in first:
                first[(name,cls)]=n; print(name,cls,"first order",n,"example",sorted(bad[0])[:2])
print(first)
