import math, networkx as nx
from collections import Counter
from fractions import Fraction as Fr
LO=lambda P,a,b,g: sum((i*j)**a*(i+j)**b*math.exp(g*abs(i-j)/(i+j)) for i,j in P)
def stats(n):
    rows={"all":[], "mol":[]}
    for T in nx.nonisomorphic_trees(n):
        d=dict(T.degree()); P=[tuple(sorted((d[u],d[v]))) for u,v in T.edges()]
        rows["all"].append(P)
        if max(d.values())<=4: rows["mol"].append(P)
    for k,L in rows.items():
        prof={tuple(sorted(Counter(P).items())) for P in L}
        qh={tuple(sorted(Counter(Fr(j-i,i+j) for i,j in P).items())) for P in L}
        cnt=lambda a,b,g,c=1: len({float(f"{c*LO(P,a,b,g):.11g}") for P in L})
        # GA merges distinct q-histograms?
        ga={}
        for P in L:
            v=float(f"{2*LO(P,.5,-1,0):.11g}"); ga.setdefault(v,set()).add(tuple(sorted(Counter(Fr(j-i,i+j) for i,j in P).items())))
        merge=any(len(s)>1 for s in ga.values())
        print(n,k,"N",len(L),"profiles",len(prof),"qhist",len(qh),"M1",cnt(0,1,0),"M2",cnt(1,0,0),"R",cnt(-.5,0,0),"LO1",cnt(0,0,1),"LO2",cnt(0,0,2),"GA",cnt(.5,-1,0,2),"GAmerge",merge,flush=True)
for n in range(7,18): stats(n)
