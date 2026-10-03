#!/usr/bin/env python3
"""Faithful Furtula-Gutman-Dehmer (2013) structure sensitivity on the 75
decane molecular trees (n=10, Delta<=4).

S(G) = { Phi in Psi : Phi isomorphic to G - e + f for some single edge
relocation, Phi not isomorphic to G, Phi in Psi }, i.e. graph edit
distance 2 within the molecular class. Per graph:
SS(TI,G) = mean over S(G) of |TI(Omega)-TI(G)|/TI(G);
Abr(TI,G) = max of the same. Class values = means over the 75 trees.
Writes fgd_structure_sensitivity_decanes.csv next to this script.
"""
import csv, math, os
import networkx as nx
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = {"M1":(0,1,0),"M2":(1,0,0),"HM":(0,2,0),"mM2":(-1,0,0),"R":(-0.5,0,0),
"chi":(0,-0.5,0),"H/2":(0,-1,0),"ISI":(1,-1,0),"GA":(0.5,-1,0),"AG":(-0.5,1,0),
"LO(0,0,1)":(0,0,1),"LO(0,0,2)":(0,0,2)}

def logr(G,a,b,g):
    return sum((G.degree(u)*G.degree(v))**a*(G.degree(u)+G.degree(v))**b
               *math.exp(g*abs(G.degree(u)-G.degree(v))/(G.degree(u)+G.degree(v)))
               for u,v in G.edges())

def main():
    trees=[T for T in nx.nonisomorphic_trees(10) if max(d for _,d in T.degree())<=4]
    assert len(trees)==75
    H=[nx.weisfeiler_lehman_graph_hash(T,iterations=10) for T in trees]
    assert len(set(H))==75, "WL hash collision within the class"
    hidx={h:i for i,h in enumerate(H)}
    neighbors=[set() for _ in trees]
    for gi,T in enumerate(trees):
        for e in list(T.edges()):
            T2=T.copy();T2.remove_edge(*e)
            comps=list(nx.connected_components(T2));A,B=comps[0],comps[1]
            for u in A:
                for v in B:
                    if (u,v)==e or (v,u)==e:continue
                    if T2.degree(u)>=4 or T2.degree(v)>=4:continue
                    T3=T2.copy();T3.add_edge(u,v)
                    j=hidx.get(nx.weisfeiler_lehman_graph_hash(T3,iterations=10))
                    if j is not None and j!=gi:neighbors[gi].add(j)
    assert all(neighbors[i] for i in range(75)), "empty similar-structure set"
    assert all(i in neighbors[j] for i in range(75) for j in neighbors[i]), "asymmetric neighbors"
    rows=[]
    for nm,t in IDX.items():
        vals=np.array([logr(T,*t) for T in trees])
        ss_g=[];ab_g=[]
        for i in range(75):
            d=[abs(vals[j]-vals[i])/vals[i] for j in neighbors[i]]
            ss_g.append(np.mean(d));ab_g.append(max(d))
        SS=float(np.mean(ss_g));AB=float(np.mean(ab_g))
        assert AB>=SS
        rows.append((nm,SS,AB,SS/AB))
    with open(os.path.join(HERE,"fgd_structure_sensitivity_decanes.csv"),"w",newline="") as f:
        w=csv.writer(f);w.writerow(["index","SS_fgd","Abr_fgd","ratio"])
        for nm,ss,ab,r in rows:w.writerow([nm,f"{ss:.5f}",f"{ab:.5f}",f"{r:.5f}"])
    print("wrote fgd_structure_sensitivity_decanes.csv;",
          "max SS:",max(rows,key=lambda r:r[1])[0])

if __name__=="__main__":
    main()
