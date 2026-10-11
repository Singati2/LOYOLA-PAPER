"""Scratch, exploratory. Reads the repo, writes nothing into it."""
import sys, os, math
ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))))
import numpy as np
REPO = ROOT
sys.path.insert(0, REPO)
import octane_data as od

IDX = [("M1",(0,1,0)),("M2",(1,0,0)),("HM",(0,2,0)),("mM2",(-1,0,0)),("R",(-.5,0,0)),("chi",(0,-.5,0)),
       ("H/2",(0,-1,0)),("ISI",(1,-1,0)),("GA",(.5,-1,0)),("AG",(-.5,1,0)),("LO(0,0,1)",(0,0,1)),("LO(0,0,2)",(0,0,2))]
P = [od.alkane_pairs(r[0]) for r in od.OCTANES]
X = {k: np.array([od.lo_pairs(p,*t) for p in P]) for k,t in IDX}
names = od.NAMES; print("PROPS", od.PROPS)
def col(prop): j = od.PROPS.index(prop); return np.array([r[1+j] for r in od.OCTANES], float)
def corr(y, mask=None):
    m = np.ones(len(y),bool) if mask is None else mask
    return {k: np.corrcoef(X[k][m], y[m])[0,1] for k,_ in IDX}
def show(label, r):
    s = sorted(r, key=lambda k: -abs(r[k]))
    print(f"{label:45s} top {s[0]} {abs(r[s[0]]):.3f}; 2nd {s[1]} {abs(r[s[1]]):.3f}; HM {r['HM']:+.3f} M1 {r['M1']:+.3f} LO001 {r['LO(0,0,1)']:+.3f}")
    return r

S = col("S"); r0 = show("S original", corr(S))
API_ALL = {"octane":110.82,"2-methylheptane":108.81,"3-methylheptane":110.32,"4-methylheptane":108.35,"3-ethylhexane":109.51,
 "2,2-dimethylhexane":103.06,"2,3-dimethylhexane":106.11,"2,4-dimethylhexane":106.51,"2,5-dimethylhexane":104.93,
 "3,3-dimethylhexane":104.70,"3,4-dimethylhexane":104.38,"3-ethyl-2-methylpentane":105.43,"3-ethyl-3-methylpentane":103.48,
 "2,2,3-trimethylpentane":101.62,"2,2,4-trimethylpentane":101.62,"2,3,3-trimethylpentane":103.14,"2,3,4-trimethylpentane":102.99,
 "2,2,3,3-tetramethylbutane":94.34}
SIX = ["4-methylheptane","2,2-dimethylhexane","3,4-dimethylhexane","3-ethyl-2-methylpentane","3-ethyl-3-methylpentane","2,3,3-trimethylpentane"]
assert set(API_ALL)==set(names)
y = S.copy()
for n in SIX: y[names.index(n)] = API_ALL[n]
r1 = show("S six -> API-44 1947 (repo v41 scenario)", corr(y))
print("   max |dr| six->API:", max(abs(abs(r1[k])-abs(r0[k])) for k in r0))
m = np.array([n not in SIX for n in names]); r2 = show("S six excluded (n=12)", corr(S, m))
print("   max |dr| excl:", max(abs(abs(r2[k])-abs(r0[k])) for k in r0))
yA = np.array([API_ALL[n] for n in names]); r3 = show("S all 18 from API-44 1947 Table 3p", corr(yA))
print("   max |dr| all1947:", max(abs(abs(r3[k])-abs(r0[k])) for k in r0))
print("   diff used - API (six):", {n: round(S[names.index(n)]-API_ALL[n],2) for n in SIX})
print("   diff used - API (all):", {n: round(S[names.index(n)]-API_ALL[n],2) for n in names})

# TMB dHvap: Circular 461 Table 3m ratios
T3m = {"octane":(125.66,9.915,8.360),"2-methylheptane":(117.64,9.483,8.03),"3-methylheptane":(118.92,9.520,8.14),
 "4-methylheptane":(117.71,9.482,8.100),"3-ethylhexane":(118.53,9.475,8.19),"2,2-dimethylhexane":(106.84,8.912,7.73),
 "2,3-dimethylhexane":(115.60,9.271,8.02),"2,4-dimethylhexane":(109.43,9.026,7.82),"2,5-dimethylhexane":(109.10,9.048,7.84),
 "3,3-dimethylhexane":(111.97,8.971,7.82),"3,4-dimethylhexane":(117.72,9.315,8.02),"3-ethyl-2-methylpentane":(115.65,9.207,7.96),
 "3-ethyl-3-methylpentane":(118.26,9.080,7.91),"2,2,3-trimethylpentane":(109.84,8.823,7.69),"2,2,4-trimethylpentane":(99.24,8.396,7.410),
 "2,3,3-trimethylpentane":(114.76,8.895,7.78),"2,3,4-trimethylpentane":(113.47,9.012,7.810)}
tb = np.array([v[0] for v in T3m.values()]); rat = np.array([v[1]/v[2] for v in T3m.values()])
print("ratio dH(25C)/dH(Tb): min %.3f max %.3f mean %.3f" % (rat.min(), rat.max(), rat.mean()))
b = np.polyfit(tb-25, rat, 1); pred = np.polyval(b, 106.30-25)
res = rat - np.polyval(b, tb-25); sd = res.std(ddof=2)
print("linear fit ratio vs (Tb-25): slope %.5f intercept %.4f resid sd %.4f" % (b[0], b[1], sd))
print("TMB extrapolated from 7.56 kcal/mol at Tb: %.3f (range from min/max ratio %.3f-%.3f; +/-2sd %.3f-%.3f)" %
      (7.56*pred, 7.56*rat.min(), 7.56*rat.max(), 7.56*(pred-2*sd), 7.56*(pred+2*sd)))
# branched-only (exclude n-octane & mono-methyl)
dH = col("dHvap"); it = names.index("2,2,3,3-tetramethylbutane")
for lab, v in [("original",8.41),("Table3m-ratio extrapolation",7.56*pred),("sub-fus",(43.37-7.54)/4.184),("NIST 298 solid",42.94/4.184)]:
    yy = dH.copy(); yy[it]=v; show(f"dHvap TMB={v:.3f} ({lab})", corr(yy))
show("dHvap TMB excluded", corr(dH, np.arange(18)!=it))

# omega TMB from Clausius-Clapeyron, KDB Tc/Pc (compiled), Tb NIST 379.6 K, dHvap 33.3 kJ/mol (377-390 K)
R=8.314462618
def omega(Tc,Pc_bar,Tb=379.6,dH=33300.):
    T=0.7*Tc; P=1.01325*math.exp(-dH/R*(1/T-1/Tb)); return -math.log10(P/Pc_bar)-1
print("omega TMB est (Tc 567.8, Pc 28.7): %.3f" % omega(567.8,28.7))
for Tc in (565.8,567.8,569.8):
    for Pc in (28.2,28.7,29.2):
        for dHv in (32300.,33300.,34300.):
            pass
vals=[omega(Tc,Pc,dH=d) for Tc in (565.8,567.8,569.8) for Pc in (28.2,28.7,29.2) for d in (32300.,33300.,34300.)]
print("omega TMB range over Tc+-2K, Pc+-0.5bar, dHvap+-1kJ: %.3f-%.3f" % (min(vals),max(vals)))
W = col("omega"); r0w=show("omega original", corr(W))
yy=W.copy(); yy[it]=0.251; show("omega TMB 0.251 only", corr(yy))
yy[names.index("2,2,4-trimethylpentane")]=0.303; show("omega both (repo v35)", corr(yy))
show("omega TMB excluded", corr(W, np.arange(18)!=it))

print("---- omega vs Milano benchmark (Ediz 2017 Table 1) ----")
MIL = {"octane":.39790,"2-methylheptane":.37792,"3-methylheptane":.37100,"4-methylheptane":.37150,"3-ethylhexane":.36247,
"2,2-dimethylhexane":.33943,"2,3-dimethylhexane":.34825,"2,4-dimethylhexane":.34422,"2,5-dimethylhexane":.35683,"3,3-dimethylhexane":.32260,
"3,4-dimethylhexane":.34035,"3-ethyl-2-methylpentane":.33243,"3-ethyl-3-methylpentane":.30690,"2,2,3-trimethylpentane":.30082,
"2,2,4-trimethylpentane":.30537,"2,3,3-trimethylpentane":.29318,"2,3,4-trimethylpentane":.31742,"2,2,3,3-tetramethylbutane":.25529}
for n in names: 
    d = W[names.index(n)]-MIL[n]
    if abs(d)>0.0006: print(f"   {n}: used {W[names.index(n)]:.3f} Milano {MIL[n]:.5f} diff {d:+.4f}")
yy=W.copy(); yy[it]=MIL["2,2,3,3-tetramethylbutane"]; ra=show("omega TMB 0.2553 (Milano)", corr(yy))
print("   max |dr|:", max(abs(abs(ra[k])-abs(r0w[k])) for k in r0w))
ym=np.array([MIL[n] for n in names]); rb=show("omega full Milano column", corr(ym))
print("   max |dr|:", max(abs(abs(rb[k])-abs(r0w[k])) for k in r0w))
