#!/usr/bin/env python3
"""Clean-room generator for the three manuscript figures + their canonical data CSVs.
Octane data imported from octane_data.py; trees/decanes enumerated via networkx; no repo
layout or external raw files required. Usage:
  python3 generate_loyola_v35_figures.py [--output-dir DIR]
Writes: lo_sensitivity_prediction_correlations.csv, lo_sensitivity_degeneracy_order10_trees.csv,
lo_sensitivity_structure_sensitivity_decanes.csv (legacy normalized-dispersion
artifact, retired from the manuscript) and the TWO manuscript figures
figures/fig_lo_prediction_correlation_heatmap_v3.pdf,
figures/fig_lo_degeneracy_order10_trees_v2.pdf.
Requires numpy, networkx, matplotlib (requirements.txt)."""
import argparse, csv, math, os
import numpy as np
import networkx as nx
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from octane_data import OCTANES,PROPS  # single source of truth for the data
PLAB=[r"$T_B$",r"$\Delta H_f$",r"$\Delta H_{\mathrm{vap}}$",r"$S$",r"$\omega$"]
IDX=[("M1",(0,1,0)),("M2",(1,0,0)),("HM",(0,2,0)),("mM2",(-1,0,0)),("R",(-0.5,0,0)),
("chi",(0,-0.5,0)),("H/2",(0,-1,0)),("ISI",(1,-1,0)),("GA",(0.5,-1,0)),("AG",(-0.5,1,0)),
("LO(0,0,1)",(0,0,1)),("LO(0,0,2)",(0,0,2))]

from octane_data import alkane_pairs as pairs  # single validated parser
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
            row=[nm]+[f"{R[i,j]:+.10f}"+("*" if best[j]==i else "") for j in range(5)]
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
        for nm,_ in IDX:w.writerow([nm,f"{ss[nm]:.10f}",f"{ab[nm]:.10f}",f"{ss[nm]/ab[nm]:.10f}"])
    names=[nm for nm,_ in IDX]
    # display labels in the same notation as the manuscript tables
    TEXLAB={"M1":r"$M_1$","M2":r"$M_2$","HM":r"$HM$","mM2":r"${}^{m}M_2$",
            "R":r"$R$","chi":r"$\chi$","H/2":r"$H/2$","ISI":r"$ISI$",
            "GA":r"$GA$","AG":r"$AG$"}
    dlab=[TEXLAB.get(nm,"$"+nm+"$") for nm in names]
    # degree-pair-profile floor computed from the data, not hard-coded
    nprof=len(set(tuple(sorted(Counter(tuple(sorted((T.degree(u),T.degree(v)))) for u,v in T.edges()).items())) for T in trees))
    floor=100*(1-nprof/NT)
    # --- fig 1: heatmap ---
    fig,ax=plt.subplots(figsize=(6.5,5.5))
    im=ax.imshow(R,cmap="RdBu_r",vmin=-1,vmax=1,aspect="auto")
    ax.set_xticks(range(5),PLAB);ax.set_yticks(range(12),dlab,fontsize=8)
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
    ax.bar(range(12),vals,color=["#66aadd" if v>floor+1e-9 else "#2c7fb8" for v in vals])
    ax.axhline(floor,ls="--",lw=1,color="gray")
    ax.text(11.45,72,f"dashed line: degree-pair-profile floor {floor:.1f}%",fontsize=7,ha="right",color="dimgray")
    ax.set_xticks(range(12),dlab,rotation=45,ha="right",fontsize=8)
    ax.set_ylabel("degeneracy (%)");ax.set_title("Degeneracy on the 106 trees of order 10",fontsize=10)
    for i,v in enumerate(vals):ax.text(i,v+1,f"{v:.1f}",ha="center",fontsize=6.5)
    fig.tight_layout();fig.savefig(os.path.join(figs,"fig_lo_degeneracy_order10_trees_v2.pdf"),metadata={"CreationDate":None});plt.close(fig)
    # (retired) the sigma/mu proxy figure is no longer generated: those
    # quantities are legacy normalized-dispersion diagnostics, NOT the
    # published Furtula-Gutman-Dehmer structure sensitivity; the proxy CSV
    # above is retained only as an internal legacy artifact.
    print(f"wrote 3 CSVs -> {out} and 2 manuscript PDFs -> {figs}")

if __name__=="__main__":main()
