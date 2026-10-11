#!/usr/bin/env python3
"""Exploratory sensitivities (v40.29) of the boiling-point sets: a repeated NIST row and wide NIST averages.

NIST (C1190836) lists 421.15 K from Marschner and Carmody (1951) twice, next to 421.65 K from the
same paper. The registered extraction rule takes the median of every listed non-compilation
determination, which gives 421.35 K (148.2 degC). Counting the repeated row once gives 421.5 K
(148.35 degC, stored to one decimal as 148.4). This script refits the ridge baseline on the decanes
and on the pooled set with both values. The registered value is kept; this is not a correction.
"""
import csv, os, re, sys
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "external"))
import baselines as B

rows = list(csv.DictReader(open(os.path.join(ROOT, "external", "bp", "bp_data.csv"))))
NAME = "Heptane, 2,2,6-trimethyl-"


def q2(p, y):
    return 1 - ((p - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def ridge_q2(sub, value=None):
    P = [[tuple(int(t) for t in p.split("-")) for p in r["degree_pairs"].split()] for r in sub]
    y = np.array([float(r["T_B_C"]) for r in sub])
    if value is not None:
        y[[k for k, r in enumerate(sub) if r["name"] == NAME][0]] = value
    F = np.array([B.count_vector(p) for p in P])
    return q2(B.outer_loo(B.fold_ridge, F, y)[0], y)


med_reg = np.median([421.15, 421.65, 421.15, 421.35, 422.08]) - 273.15
med_dedup = np.median([421.15, 421.65, 421.35, 422.08]) - 273.15
dec = [r for r in rows if r["n_C"] == "10"]
lines = [f"registered median {med_reg:.2f} degC; repeated row counted once {med_dedup:.2f} degC (stored 148.4)"]
for label, sub in (("decanes", dec), ("pooled C6-C10", rows)):
    a, b = ridge_q2(sub), ridge_q2(sub, 148.4)
    lines.append(f"{label}: ridge Q2 {a:.4f} as registered, {b:.4f} with 148.4 degC")
# quality variant (v40.29): drop molecules whose value is a NIST average quoting more than +-3 K
prov = list(csv.DictReader(open(os.path.join(ROOT, "external", "bp", "bp_provenance.csv"))))
wide = {r["nist_id"] for r in prov if r["status"] == "INCLUDED" and r["rule_or_reason"].startswith("AVG")
        and float(re.search(r"\u00b1 ([\d.]+)", r["all_determinations"]).group(1)) > 3}
lines.append("NIST averages quoting more than 3 K: " + ", ".join(sorted(r["name"] for r in rows if r["nist_id"] in wide)))
for label, sub in (("decanes", dec), ("pooled C6-C10", rows)):
    kept = [r for r in sub if r["nist_id"] not in wide]
    lines.append(f"{label}: ridge Q2 {ridge_q2(sub):.4f} as registered, {ridge_q2(kept):.4f} without them (n = {len(kept)})")
out = "\n".join(lines) + "\n"
print(out, end="")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bp_duplicate_sensitivity_out.txt"), "w").write(out)
