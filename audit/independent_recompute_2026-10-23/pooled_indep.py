import csv, sys, numpy as np
rows=list(csv.DictReader(open(sys.argv[1])))
P=[[tuple(map(int,x.split("-"))) for x in r["degree_pairs"].split()] for r in rows]
y=np.array([float(r["T_B_C"]) for r in rows]); z=np.array([float(r["n_C"]) for r in rows]); n=len(y)
pairs=sorted({p for Pm in P for p in Pm}); C=np.array([[Pm.count(p) for p in pairs] for Pm in P],float)
pi=np.array([p[0] for p in pairs],float); pj=np.array([p[1] for p in pairs],float)
def desc(T):
    a,b,g=T[:,0:1],T[:,1:2],T[:,2:3]
    return ((pi*pj)**a*(pi+pj)**b*np.exp(g*np.abs(pi-pj)/(pi+pj)))@C.T
def std(X):
    mu=X.mean(-1,keepdims=True); sd=X.std(-1,keepdims=True); return (X-mu)/np.where(sd>0,sd,1)
def press(X,zt,yt):
    Xs=std(X); zs=(zt-zt.mean())/zt.std(); m=len(yt)
    A=np.stack([np.ones_like(Xs),np.broadcast_to(zs,Xs.shape),Xs],-1)  # c x m x 3
    AtA=np.einsum('cmi,cmj->cij',A,A); det=np.linalg.det(AtA)
    ok=np.abs(det)>1e-8*m**3
    inv=np.linalg.inv(np.where(ok[:,None,None],AtA,np.eye(3)))
    h=np.einsum('cmi,cij,cmj->cm',A,inv,A); coef=np.einsum('cij,cmj,m->ci',inv,A,yt)
    res=yt-np.einsum('cmi,ci->cm',A,coef)
    r=np.sqrt(((res/(1-h))**2).mean(1)); rel=(X.max(1)-X.min(1))/np.abs(X).max(1)
    r[~ok|~np.isfinite(r)|(rel<1e-9)|np.any(1-h<1e-6,axis=1)]=np.inf; return r
def nested(X):
    p=np.empty(n)
    for i in range(n):
        m=np.arange(n)!=i; k=int(np.argmin(press(X[:,m],z[m],y[m])))
        xt=X[k,m]; mu,sd=xt.mean(),xt.std(); zm,zsd=z[m].mean(),z[m].std()
        A=np.column_stack([np.ones(n-1),(z[m]-zm)/zsd,(xt-mu)/sd]); c=np.linalg.lstsq(A,y[m],rcond=None)[0]
        p[i]=c[0]+c[1]*(z[i]-zm)/zsd+c[2]*(X[k,i]-mu)/sd
    return p
q2=lambda p,yy:1-((p-yy)**2).sum()/((yy-yy.mean())**2).sum()
G=[];L=[];out=[]
for s in range(50):
    rng=np.random.default_rng(s);B=2000
    rng.uniform(-2,2,(B,3)); rng.uniform(-2,2,(B,2))
    gm12=np.column_stack([np.round(rng.uniform(-12,12,(B,2)),3),np.zeros(B)])
    hy=np.round(np.column_stack([rng.uniform(-12,12,(B,2)),rng.uniform(-2,2,B)]),3)
    g=nested(desc(gm12)); l=nested(desc(hy)); G.append(g); L.append(l); out.append((s,q2(g,y),q2(l,y))); print(s,out[-1][1:],flush=True)
G,L=np.array(G),np.array(L); d=np.array([c-b for _,b,c in out])
rng=np.random.default_rng(20261005); st=[]
for _ in range(2000):
    idx=rng.integers(0,n,n); yy=y[idx]
    st.append(np.median((1-((L[:,idx]-yy)**2).sum(1)/((yy-yy.mean())**2).sum())-(1-((G[:,idx]-yy)**2).sum(1)/((yy-yy.mean())**2).sum())))
print("median GM12",np.median([b for _,b,_ in out]),"LOh",np.median([c for *_,c in out]),"d",np.median(d),"wins",(d>0).sum(),"CI",np.percentile(st,[2.5,97.5]))
np.savetxt(sys.argv[2],np.array(out),delimiter=",",fmt="%.10f")
