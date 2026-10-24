import csv, sys, math, numpy as np
rows=list(csv.DictReader(open(sys.argv[1])))
Pall=[[tuple(map(int,x.split("-"))) for x in r["degree_pairs"].split()] for r in rows]
yall=np.array([float(r["T_B_C"]) for r in rows]); zall=np.array([float(r["n_C"]) for r in rows])
LO=lambda P,a,b,g: sum((i*j)**a*(i+j)**b*math.exp(g*abs(i-j)/(i+j)) for i,j in P)
CL=[(0,1,0),(1,0,0),(0,2,0),(-1,0,0),(-.5,0,0),(0,-.5,0),(0,-1,0),(1,-1,0),(.5,-1,0),(-.5,1,0)]
DP=[(i,j) for i in range(1,5) for j in range(i,5)]
def q2(p,y): return 1-((p-y)**2).sum()/((y-y.mean())**2).sum()
def ols_pred(Xt,yt,Xn):
    A=np.column_stack([np.ones(len(yt)),Xt]); c=np.linalg.lstsq(A,yt,rcond=None)[0]; return np.r_[1,Xn]@c
def loo(fn,n):
    return np.array([fn(np.arange(n)!=i,i) for i in range(n)])
def inner_rmse(X,y):  # X: n x p design (without intercept)
    n=len(y); return math.sqrt(np.mean([(ols_pred(X[m],y[m],X[i])-y[i])**2 for i in range(n) for m in [np.arange(n)!=i]]))
def ridge_pred(F,y,Fn,lam):
    mu,sd=F.mean(0),F.std(0); k=sd>1e-12; Z=(F[:,k]-mu[k])/sd[k]; Zn=(Fn[k]-mu[k])/sd[k]
    w=np.linalg.solve(Z.T@Z+lam*np.eye(k.sum()),Z.T@(y-y.mean())); return y.mean()+Zn@w
LAM=np.logspace(-4,4,41)
def ridge_fold(F,y):
    def f(m,i):
        Ft,yt=F[m],y[m]; nt=len(yt)
        err=[np.sqrt(np.mean([(ridge_pred(Ft[np.arange(nt)!=j],yt[np.arange(nt)!=j],Ft[j],l)-yt[j])**2 for j in range(nt)])) for l in LAM]
        return ridge_pred(Ft,yt,F[i],LAM[int(np.argmin(err))])
    return f
for lab,sel in (("decane",[i for i,r in enumerate(rows) if r["n_C"]=="10"]),("pooled",list(range(len(rows))))):
    P=[Pall[i] for i in sel]; y=yall[sel]; z=zall[sel]; n=len(y)
    D=lambda t: np.array([LO(p,*t) for p in P])
    irla=np.array([2*sum(abs(i-j)/(i+j) for i,j in p) for p in P]); lo1=D((0,0,1)); C=[D(t) for t in CL]
    F=np.array([[p.count(d) for d in DP] for p in P],float)
    cov=(lambda x: x[:,None]) if lab=="decane" else (lambda x: np.column_stack([z,x]))
    out={}
    out["base"]=q2(loo(lambda m,i: y[m].mean(),n),y) if lab=="decane" else q2(loo(lambda m,i: ols_pred(z[m,None],y[m],z[i:i+1]),n),y)
    out["IRLA"]=q2(loo(lambda m,i: ols_pred(cov(irla)[m],y[m],cov(irla)[i]),n),y)
    out["LO1"]=q2(loo(lambda m,i: ols_pred(cov(lo1)[m],y[m],cov(lo1)[i]),n),y)
    def cls(m,i):
        k=int(np.argmin([inner_rmse(cov(c)[m],y[m]) for c in C])); return ols_pred(cov(C[k])[m],y[m],cov(C[k])[i])
    out["Class"]=q2(loo(cls,n),y)
    out["Ridge"]=q2(loo(ridge_fold(F,y),n),y)
    print(lab,n,{k:round(v,4) for k,v in out.items()},flush=True)
