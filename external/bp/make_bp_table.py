#!/usr/bin/env python3
"""Rows of tab:bp (manuscript) from bp_results_summary.csv and bp_baselines.csv."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
S = {r["test"][0]: r for r in csv.DictReader(open(os.path.join(HERE, "bp_results_summary.csv")))}
Bm = {}
for r in csv.DictReader(open(os.path.join(HERE, "bp_baselines.csv"))):
    Bm[(r["test"][0], r["model"])] = float(r["Q2"])
import numpy as np
SEED = {}
for r in csv.DictReader(open(os.path.join(HERE, "bp_results_seeds.csv"))):
    SEED.setdefault(r["test"][0], []).append(float(r["Q2_LOh"]) - float(r["Q2_GM12"]))
rows = []
for t, lab, base in (("A", "decanes ($n = 34$)", ["mean", "classical best", "IRLA", "LO(0,0,1) fixed"]),
                     ("B", "C6--C10, with $n_C$ ($n = 101$)", ["size only", "size + classical best", "size + IRLA", "size + LO(0,0,1) fixed"])):
    s = S[t]
    cells = [lab] + [f"${Bm[(t, b)]:.3f}$" for b in base] + [f"${Bm[(t, 'ridge on degree-pair counts')]:.3f}$",
             f"${float(s['median_Q2_GM12']):.3f}$", f"${float(s['median_Q2_LOh']):.3f}$",
             f"${float(np.median(SEED[t])):+.3f}$", f"${s['LOh_better_of_50']}$"]
    rows.append(" & ".join(cells) + r"\\")
open(os.path.join(HERE, "bp_table_rows.tex"), "w").write("\n".join(rows) + "\n")
print("\n".join(rows))
