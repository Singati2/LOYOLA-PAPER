import math, networkx as nx, itertools
LO=lambda G,a,b,g: sum((G.degree(u)*G.degree(v))**a*(G.degree(u)+G.degree(v))**b*math.exp(g*abs(G.degree(u)-G.degree(v))/(G.degree(u)+G.degree(v))) for u,v in G.edges())
T=[t for t in nx.nonisomorphic_trees(10) if max(dict(t.degree()).values())<=4]; print(len(T))
def cid(G):
    h=nx.weisfeiler_lehman_graph_hash(G)
    for k,t in enumerate(T):
        if hashes[k]==h and nx.is_isomorphic(G,t): return k
hashes=[nx.weisfeiler_lehman_graph_hash(t) for t in T]
nb=[]
for k,G in enumerate(T):
    S=set()
    for (u,v) in list(G.edges()):
        H=G.copy(); H.remove_edge(u,v); c1,c2=list(nx.connected_components(H))
        for x in c1:
            for y in c2:
                if {x,y}=={u,v}: continue
                K=H.copy(); K.add_edge(x,y)
                if max(dict(K.degree()).values())>4: continue
                j=cid(K)
                if j!=k: S.add(j)
    nb.append(S)
print("sizes",min(map(len,nb)),max(map(len,nb)))
for nm,(a,b,g,c) in {"M1":(0,1,0,1),"HM":(0,2,0,1),"R":(-.5,0,0,1),"GA":(.5,-1,0,2),"LO001":(0,0,1,1),"LO002":(0,0,2,1),"IRLA":None}.items():
    if nm=="IRLA": v=[2*sum(abs(G.degree(u)-G.degree(w))/(G.degree(u)+G.degree(w)) for u,w in G.edges()) for G in T]
    else: v=[c*LO(G,a,b,g) for G in T]
    ss=[sum(abs(v[j]-v[k])/v[k] for j in nb[k])/len(nb[k]) for k in range(len(T))]
    ab=[max(abs(v[j]-v[k])/v[k] for j in nb[k]) for k in range(len(T))]
    SS,AB=sum(ss)/len(T),sum(ab)/len(T); print(nm,round(SS,4),round(AB,4),round(SS/AB,4))
