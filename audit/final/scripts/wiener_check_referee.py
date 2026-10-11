import csv,re,numpy as np,itertools
def parse(inchi):
    parts=inchi.split('/')
    c=[p for p in parts if p.startswith('c')]
    n=int(re.search(r'C(\d+)',parts[1]).group(1)) if re.search(r'C(\d+)',parts[1]) else 1
    edges=[]
    if not c: return n,edges
    s=c[0][1:]
    toks=re.findall(r'\d+|[()\-,]',s)
    stack=[];prev=None
    for t in toks:
        if t.isdigit():
            a=int(t)
            if prev is not None: edges.append((prev,a))
            prev=a
        elif t=='(': stack.append(prev)
        elif t==')': prev=stack.pop()
        elif t==',': prev=stack[-1]
    return n,edges
def wiener(n,edges):
    D=np.full((n+1,n+1),99);
    for i in range(1,n+1): D[i,i]=0
    for a,b in edges: D[a,b]=D[b,a]=1
    for k in range(1,n+1): D=np.minimum(D,D[:,k:k+1]+D[k:k+1,:])
    return D[1:,1:].sum()/2
ids={}
for r in csv.DictReader(open('nist_alkanes_skeletons_audit.csv')):
    n,e=parse(r['skel'])
    if len(e)!=n-1: continue
    for i in r['ids'].split(';'):
        ids[i.strip()]=(n,wiener(n,e),e)
data=[r for r in csv.DictReader(open('bp_data.csv'))]
miss=[r['nist_id'] for r in data if r['nist_id'] not in ids]
print('missing',miss[:5],len(miss))
def loo(X,y):
    n=len(y);pr=[]
    for i in range(n):
        m=np.arange(n)!=i
        b=np.linalg.lstsq(X[m],y[m],rcond=None)[0]; pr.append(X[i]@b)
    pr=np.array(pr); return 1-((y-pr)**2).sum()/((y-y.mean())**2).sum()
d=[r for r in data if r['n_C']=='10' and r['nist_id'] in ids]
y=np.array([float(r['T_B_C']) for r in d]); W=np.array([ids[r['nist_id']][1] for r in d])
# check degree pairs consistent
print('decanes',len(d),'Q2 W',loo(np.c_[np.ones(len(y)),W],y))
# number of 3-path p3 / Wiener + p3 (2 desc)
d=[r for r in data if r['nist_id'] in ids]
y=np.array([float(r['T_B_C']) for r in d]); W=np.array([ids[r['nist_id']][1] for r in d]); nc=np.array([float(r['n_C']) for r in d])
print('pooled',len(d),'size only',loo(np.c_[np.ones(len(y)),nc],y),'size+W',loo(np.c_[np.ones(len(y)),nc,W],y),'size+logW', loo(np.c_[np.ones(len(y)),nc,np.log(W)],y))
def p3(n,edges):
    D=np.full((n+1,n+1),99)
    for i in range(1,n+1): D[i,i]=0
    for a,b in edges: D[a,b]=D[b,a]=1
    for k in range(1,n+1): D=np.minimum(D,D[:,k:k+1]+D[k:k+1,:])
    return (D[1:,1:]==3).sum()/2
d=[r for r in data if r['n_C']=='10' and r['nist_id'] in ids]
y=np.array([float(r['T_B_C']) for r in d]); W=np.array([ids[r['nist_id']][1] for r in d]); P=np.array([p3(ids[r['nist_id']][0],ids[r['nist_id']][2]) for r in d])
print('decane W+p3',loo(np.c_[np.ones(len(y)),W,P],y), 'p3', loo(np.c_[np.ones(len(y)),P],y))
