import sys, csv, math, numpy as np, networkx as nx
from collections import Counter
def parse(smi):
    deg=Counter(); edges=[]; stack=[]; prev=None; idx=0
    for ch in smi:
        if ch=='C':
            if prev is not None: edges.append((prev,idx))
            prev=idx; idx+=1
        elif ch=='(': stack.append(prev)
        elif ch==')': prev=stack.pop()
    for u,v in edges: deg[u]+=1; deg[v]+=1
    return [tuple(sorted((deg[u],deg[v]))) for u,v in edges]
def LO(P,a,b,g): return sum((i*j)**a*(i+j)**b*math.exp(g*abs(i-j)/(i+j)) for i,j in P)
IDX=[("M1",0,1,0,1),("M2",1,0,0,1),("HM",0,2,0,1),("mM2",-1,0,0,1),("R",-.5,0,0,1),("chi",0,-.5,0,1),("H/2",0,-1,0,1),("ISI",1,-1,0,1),("GA",.5,-1,0,2),("AG",-.5,1,0,.5),("LO001",0,0,1,1),("LO002",0,0,2,1)]
rows=list(csv.DictReader(open(sys.argv[1])))
P=[parse(r['smiles']) for r in rows]
props=['T_B_C','dHf_kcal_per_mol','dHvap_kcal_per_mol','S_cal_per_mol_K','omega']
Y={p:np.array([float(r[p]) for r in rows]) for p in props}
X={nm:np.array([c*LO(Pm,a,b,g) for Pm in P]) for nm,a,b,g,c in IDX}
print("Table 4 recomputed")
for nm in X: print(f"{nm:6s}"," ".join(f"{np.corrcoef(X[nm],Y[p])[0,1]:+.4f}" for p in props))
# collisions
prof=Counter(tuple(sorted(Counter(Pm).items())) for Pm in P); print("distinct profiles",len(prof))
for k,v in prof.items():
    if v>1: print("shared",k,[rows[i]['name'] for i,Pm in enumerate(P) if tuple(sorted(Counter(Pm).items()))==k])
# TMB variants
i=[r['name'] for r in rows].index('2,2,3,3-tetramethylbutane')
for lab,val in [("orig",None),("excl","x"),("hyp",(43.37-7.54)/4.184),("subl",42.94/4.184)]:
    y=Y['dHvap_kcal_per_mol'].copy(); m=np.ones(18,bool)
    if val=="x": m[i]=False
    elif val is not None: y[i]=val
    rs={nm:abs(np.corrcoef(X[nm][m],y[m])[0,1]) for nm in X}
    top=sorted(rs.items(),key=lambda t:-t[1])[:3]
    print(lab, None if val in (None,"x") else round(val,4), [(a,round(b,5)) for a,b in top])
# octane T_B within-class floor
cls={}
for k,Pm in enumerate(P): cls.setdefault(tuple(sorted(Counter(Pm).items())),[]).append(Y['T_B_C'][k])
ss=sum(((np.array(v)-np.mean(v))**2).sum() for v in cls.values()); print("floor SS",round(ss,4),"rms",round(math.sqrt(ss/18),4))
# order-10 trees degeneracy
T=list(nx.nonisomorphic_trees(10)); print("trees",len(T))
def pairs(G): return [tuple(sorted((G.degree(u),G.degree(v)))) for u,v in G.edges()]
TP=[pairs(G) for G in T]
print("profiles",len({tuple(sorted(Counter(p).items())) for p in TP}))
for nm,a,b,g,c in IDX:
    vals={float(f"{c*LO(p,a,b,g):.11g}") for p in TP}; print(nm,len(vals),round(100*(1-len(vals)/len(T)),2))
v=Counter(float(f"{LO(p,0,0,1):.11g}") for p in TP); print("trees sharing LO001 value",sum(c for c in v.values() if c>1))
