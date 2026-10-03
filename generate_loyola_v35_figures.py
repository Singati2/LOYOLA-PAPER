#!/usr/bin/env python3
"""Clean-room generator for the three manuscript figures + their canonical data CSVs.
Self-contained: octane data embedded; trees/decanes enumerated via networkx; no repo
layout or external raw files required. Usage:
  python3 generate_loyola_v29_figures.py [--output-dir DIR]
Writes: lo_sensitivity_prediction_correlations.csv, lo_sensitivity_degeneracy_order10_trees.csv,
lo_sensitivity_structure_sensitivity_decanes.csv (legacy normalized-dispersion
artifact, retired from the manuscript) and the TWO manuscript figures
figures/fig_lo_prediction_correlation_heatmap_v3.pdf,
figures/fig_lo_degeneracy_order10_trees_v2.pdf.
Requires numpy, networkx, matplotlib (requirements.txt)."""
import argparse, csv, math, os
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OCTANES=[('CCCCCCCC',125.6,-49.82,9.92,111.55,0.398),('CC(C)CCCCC',117.6,-51.50,9.48,109.84,0.378),
('CCC(C)CCCC',118.9,-50.82,9.52,111.26,0.371),('CCCC(C)CCC',117.7,-50.69,9.48,109.32,0.372),
('CC(C)(C)CCCC',106.8,-53.71,8.92,103.13,0.339),('CC(C)C(C)CCC',115.6,-51.13,9.27,108.02,0.348),
('CC(C)CC(C)CC',109.4,-52.44,9.03,106.98,0.344),('CC(C)CCC(C)C',109.1,-53.21,9.05,105.72,0.357),
('CCCC(C)(C)CC',111.9,-52.61,9.04,104.74,0.322),('CCC(C)C(C)CC',117.7,-50.91,9.32,106.59,0.340),
('CCC(CC)C(C)C',115.6,-50.48,9.21,106.06,0.330),('CCC(C)(CC)CC',118.3,-51.38,9.21,101.48,0.302),
('CCC(CC)CCC',118.5,-50.40,9.48,109.43,0.362),('CCC(C)C(C)(C)C',109.8,-52.61,8.88,101.31,0.300),
('CC(C)CC(C)(C)C',99.2,-53.57,8.40,101.81,0.305),('CCC(C)(C)C(C)C',114.8,-51.73,9.02,101.31,0.291),
('CC(C)C(C)C(C)C',113.5,-51.97,9.01,102.39,0.317),('CC(C)(C)C(C)(C)C',106.5,-53.99,8.41,93.06,0.247)]
PROPS=["T_B","dHf","dHvap","S","omega"]
PLAB=[r"$T_B$",r"$\Delta H_f$",r"$\Delta H_{vap}$",r"$S$",r"$\omega$"]
IDX=[("M1",(0,1,0)),("M2",(1,0,0)),("HM",(0,2,0)),("mM2",(-1,0,0)),("R",(-0.5,0,0)),
("chi",(0,-0.5,0)),("H/2",(0,-1,0)),("ISI",(1,-1,0)),("GA",(0.5,-1,0)),("AG",(-0.5,1,0)),
("LO(0,0,1)",(0,0,1)),("LO(0,0,2)",(0,0,2))]

def pairs(smi):
    adj={};prev=None;st=[];k=-1
    for ch in smi:
        if ch=='(':st.append(prev)
        elif ch==')':prev=st.pop()
        elif ch=='C':
            k+=1;adj[k]=set()
            if prev is not None:adj[k].add(prev);adj[prev].add(k)
            prev=k
    seen=set();out=[]
    for u in adj:
        for v in adj[u]:
            e=(min(u,v),max(u,v))
            if e in seen:continue
            seen.add(e);out.append((len(adj[u]),len(adj[v])))
    return out
def loP(P,a,b,g):return sum((i*j)**a*(i+j)**b*math.exp(g*abs(i-j)/(i+j)) for i,j in P)
def loG(G,a,b,g):return sum((G.degree(u)*G.degree(v))**a*(G.degree(u)+G.degree(v))**b
                            *math.exp(g*abs(G.degree(u)-G.degree(v))/(G.degree(u)+G.degree(v))) for u,v in G.edges())
def rs(x,y):
    xc=x-x.mean();yc=y-y.mean();s=np.linalg.norm(xc)*np.linalg.norm(yc)
    return 0.0 if s==0 else float(xc@yc/s)

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output-dir",default=os.path.dirname(os.path.abspath(__file__)))
    A=ap.parse_args();out=A.output_dir;figs=os.path.join(out,"figures");os.makedirs(figs,exist_ok=True)
    OP=[pairs(r[0]) for r in OCTANES];Y={p:np.array([r[1+i] for r in OCTANES]) for i,p in enumerate(PROPS)}
    # --- data 1: prediction correlations ---
    R=np.array([[rs(np.array([loP(P,*t) for P in OP]),Y[p]) for p in PROPS] for _,t in IDX])
    best=[int(np.argmax(np.abs(R[:,j]))) for j in range(5)]
    with open(os.path.join(out,"lo_sensitivity_prediction_correlations.csv"),"w",newline="") as f:
        w=csv.writer(f);w.writerow(["index"]+PROPS+["best_in"])
        for i,(nm,_) in enumerate(IDX):
            row=[nm]+[f"{R[i,j]:+.4f}"+("*" if best[j]==i else "") for j in range(5)]
            row.append("; ".join(PROPS[j] for j in range(5) if best[j]==i));w.writerow(row)
    # --- data 2+3: trees / decanes ---
    trees=list(nx.nonisomorphic_trees(10));NT=len(trees)
    deg={nm:len(set(round(loG(T,*t),9) for T in trees)) for nm,t in IDX}
    with open(os.path.join(out,"lo_sensitivity_degeneracy_order10_trees.csv"),"w",newline="") as f:
        w=csv.writer(f);w.writerow(["index","N_trees","distinct_values","degeneracy_pct"])
        for nm,_ in IDX:w.writerow([nm,NT,deg[nm],f"{100*(1-deg[nm]/NT):.2f}"])
    dec=[T for T in trees if max(d for _,d in T.degree())<=4]
    ss={};ab={}
    for nm,t in IDX:
        v=np.array([loG(T,*t) for T in dec]);ss[nm]=v.std(ddof=0)/v.mean();ab[nm]=(v.max()-v.min())/v.mean()
    with open(os.path.join(out,"lo_sensitivity_structure_sensitivity_decanes.csv"),"w",newline="") as f:
        w=csv.writer(f);w.writerow(["index","SS","Abr","SA"])
        for nm,_ in IDX:w.writerow([nm,f"{ss[nm]:.5f}",f"{ab[nm]:.5f}",f"{ss[nm]/ab[nm]:.5f}"])
    names=[nm for nm,_ in IDX]
    # --- fig 1: heatmap ---
    fig,ax=plt.subplots(figsize=(6.5,5.5))
    im=ax.imshow(R,cmap="RdBu_r",vmin=-1,vmax=1,aspect="auto")
    ax.set_xticks(range(5),PLAB);ax.set_yticks(range(12),names,fontsize=8)
    for i in range(12):
        for j in range(5):
            ax.text(j,i,f"{R[i,j]:+.3f}",ha="center",va="center",fontsize=6.5,
                    fontweight="bold" if best[j]==i else "normal",
                    color="white" if abs(R[i,j])>0.6 else "black")
    fig.colorbar(im,label="signed Pearson $r$");ax.set_title("Index-property correlations, 18 octane isomers",fontsize=10)
    fig.tight_layout();fig.savefig(os.path.join(figs,"fig_lo_prediction_correlation_heatmap_v3.pdf"),metadata={"CreationDate":None});plt.close(fig)
    # --- fig 2: degeneracy bars ---
    fig,ax=plt.subplots(figsize=(6.5,3.6))
    vals=[100*(1-deg[nm]/NT) for nm in names]
    ax.bar(range(12),vals,color=["#66aadd" if v>25.6 else "#2c7fb8" for v in vals])
    ax.axhline(100*(1-79/NT),ls="--",lw=1,color="gray")
    ax.text(-0.45,21.5,"BID floor 25.5%",fontsize=7,ha="left",color="gray")
    ax.set_xticks(range(12),names,rotation=45,ha="right",fontsize=8)
    ax.set_ylabel("degeneracy (%)");ax.set_title("Degeneracy on the 106 trees of order 10",fontsize=10)
    for i,v in enumerate(vals):ax.text(i,v+1,f"{v:.1f}",ha="center",fontsize=6.5)
    fig.tight_layout();fig.savefig(os.path.join(figs,"fig_lo_degeneracy_order10_trees_v2.pdf"),metadata={"CreationDate":None});plt.close(fig)
    # (retired) the sigma/mu proxy figure is no longer generated: those
    # quantities are legacy normalized-dispersion diagnostics, NOT the
    # published Furtula-Gutman-Dehmer structure sensitivity; the proxy CSV
    # above is retained only as an internal legacy artifact.
    print(f"wrote 3 CSVs -> {out} and 2 manuscript PDFs -> {figs}")

if __name__=="__main__":main()
