"""Scratch, exploratory: nonane dHvap by provenance class. Writes nothing into the repo."""
import csv, os, sys, time
ROOT = __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__)))))
import numpy as np
EXT = os.path.join(ROOT, "external")
sys.path.insert(0, EXT); sys.path.insert(0, os.path.dirname(EXT))
import baselines as B
from octane_data import alkane_pairs
prov = {r["name"]: r for r in csv.DictReader(open(os.path.join(EXT,"nonane_provenance.csv"))) if r["property"]!="T_B"}
rows = [r for r in csv.DictReader(open(os.path.join(EXT,"nonane_data.csv"))) if r["dHvap_kcal"].strip()]
def cls(n):
    s = prov[n]["selection_rule"]; a = prov[n]["all_determinations"]
    if s.startswith("NIST average"): return "NIST_AVG"
    if "most recent calorimetric" in s: return "calorimetric"
    if "Labbauf" in a.split(":")[0]: return "Labbauf1961"
    return "WilhoitZwolinski1971(Reid1972)"
C = np.array([cls(r["name"]) for r in rows]); print({c: int((C==c).sum()) for c in set(C)})
P = [alkane_pairs(r["smiles"]) for r in rows]; y = np.array([float(r["dHvap_kcal"]) for r in rows])
def q2(p,y): return 1-((p-y)**2).sum()/((y-y.mean())**2).sum()
F = np.array([B.count_vector(p) for p in P])
pr = B.outer_loo(B.fold_ridge, F, y)[0]; res = y-pr
print("ridge-count LOO Q2 all n=%d: %.3f (repo baseline should match)" % (len(y), q2(pr,y)))
for c in sorted(set(C)):
    m = C==c; print(f"  {c:32s} n={m.sum():2d} mean|res| {np.abs(res[m]).mean():.3f} kcal/mol  max {np.abs(res[m]).max():.3f}")
meas = np.isin(C,["NIST_AVG","calorimetric"])
print("  measured (AVG+cal) n=%d mean|res| %.3f; compiled n=%d mean|res| %.3f" % (meas.sum(), np.abs(res[meas]).mean(), (~meas).sum(), np.abs(res[~meas]).mean()))
for r,c,e in zip(rows,C,res):
    if c in ("NIST_AVG","calorimetric"): print("   ", r["name"], c, f"resid {e:+.3f}")
def gmlo(Pc, yc, label):
    t=time.time(); d={b:[] for b in (200,500)}
    for s in range(100):
        for b in (200,500):
            gm_t, lo_t = B.candidate_triples(s,b)
            qg = q2(B.outer_loo(B.fold_select_ols, B.descriptor_matrix(Pc,gm_t), yc)[0], yc)
            ql = q2(B.outer_loo(B.fold_select_ols, B.descriptor_matrix(Pc,lo_t), yc)[0], yc)
            d[b].append(ql-qg)
    out = {b:(int((np.array(v)>0).sum()), float(np.median(v))) for b,v in d.items()}
    wins=[out[b][0] for b in (200,500)]; med=[out[b][1] for b in (200,500)]
    v = "REPLICATES" if min(wins)>=80 and min(med)>0 else ("DOES NOT REPLICATE" if min(wins)<=50 else "MIXED")
    print(f"{label}: n={len(yc)} B200 {out[200][0]}/100 med {out[200][1]:+.3f}; B500 {out[500][0]}/100 med {out[500][1]:+.3f}; rule -> {v}  ({time.time()-t:.0f}s)", flush=True)
m = C!="Labbauf1961"; gmlo([p for p,k in zip(P,m) if k], y[m], "Labbauf rows excluded")
m = C=="WilhoitZwolinski1971(Reid1972)"; gmlo([p for p,k in zip(P,m) if k], y[m], "Wilhoit-Zwolinski rows only")
