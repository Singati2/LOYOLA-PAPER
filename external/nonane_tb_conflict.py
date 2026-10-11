#!/usr/bin/env python3
"""Sensitivity of the nonane T_B analysis to 3-ethyl-4-methylhexane (exploratory, v40.28).

The registered nonane data use 140.4 degC (413.55 K, Fenske et al. 1947, CAS page). The later
boiling-point audit (PREREG_v40.md, D5) found a second NIST entry, 407.15 K (Lukes and
Langthaler 1957, C500006531), 6.4 K lower, and excluded the molecule from Test B. This script
reruns the registered nonane T_B comparison (GM vs LO, seeds 0-99, budgets 200 and 500, as in
nonane_validation.py) and the ridge baseline with the value (a) as registered, (b) excluded and
(c) replaced by 134.0 degC. Case (a) must reproduce the committed summaries; a mismatch stops
the run. Output: nonane_tb_conflict_out.txt.
"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import baselines as B
from octane_data import alkane_pairs

SEEDS, BUDGETS = range(100), (200, 500)
NAME = "3-ethyl-4-methylhexane"


def q2(p, y):
    return 1 - ((p - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def analyse(P, y):
    d = {b: [] for b in BUDGETS}
    for s in SEEDS:
        for b in BUDGETS:
            gm_t, lo_t = B.candidate_triples(s, b)
            qg = q2(B.outer_loo(B.fold_select_ols, B.descriptor_matrix(P, gm_t), y)[0], y)
            ql = q2(B.outer_loo(B.fold_select_ols, B.descriptor_matrix(P, lo_t), y)[0], y)
            d[b].append(ql - qg)
    F = np.array([B.count_vector(p) for p in P])
    ridge = q2(B.outer_loo(B.fold_ridge, F, y)[0], y)
    return {b: (int((np.array(v) > 0).sum()), float(np.median(v))) for b, v in d.items()}, ridge


def main():
    rows = [r for r in csv.DictReader(open(os.path.join(HERE, "nonane_data.csv"))) if r["T_B_C"].strip()]
    P = [alkane_pairs(r["smiles"]) for r in rows]
    y = np.array([float(r["T_B_C"]) for r in rows])
    i = [k for k, r in enumerate(rows) if r["name"] == NAME][0]
    assert y[i] == 140.4, y[i]
    keep = np.arange(len(y)) != i
    y_alt = y.copy(); y_alt[i] = 134.0
    cases = [("as registered (140.4 degC)", P, y),
             ("excluded", [p for k, p in enumerate(P) if keep[k]], y[keep]),
             ("second NIST entry (134.0 degC)", P, y_alt)]
    summ = {(r["budget"]): r for r in csv.DictReader(open(os.path.join(HERE, "nonane_validation_summary.csv")))
            if r["property"] == "T_B" and r["analysis"] == "primary"}
    ridge_ref = [float(r["Q2"]) for r in csv.DictReader(open(os.path.join(HERE, "baselines_nonane.csv")))
                 if r["property"] == "T_B_C" and r["method"] == "ridge_counts"][0]
    lines, verdicts = [], []
    for k, (label, Pc, yc) in enumerate(cases):
        v, ridge = analyse(Pc, yc)
        wins = [v[b][0] for b in BUDGETS]; med = [v[b][1] for b in BUDGETS]
        verdicts.append("REPLICATES" if min(wins) >= 80 and min(med) > 0 else
                        "DOES NOT REPLICATE" if min(wins) <= 50 else "MIXED")
        if k == 0:
            for b in BUDGETS:
                ref = summ[str(b)]
                if v[b][0] != int(ref["LO_better"]) or f"{v[b][1]:+.4f}" != ref["median_dQ2"]:
                    raise SystemExit(f"case (a) does not reproduce nonane_validation_summary.csv at B={b}: {v[b]} vs {ref}")
            if abs(ridge - ridge_ref) > 1e-9:
                raise SystemExit(f"case (a) ridge {ridge} != committed {ridge_ref}")
        lines.append(f"{label}: n={len(yc)}; " + "; ".join(
            f"B={b}: LO better {v[b][0]}/100, median dQ2 {v[b][1]:+.3f}" for b in BUDGETS) + f"; ridge Q2 {ridge:.3f}; verdict {verdicts[-1]}")
    lines.append("RESULT: verdict " + ("MIXED in all three cases, as registered" if set(verdicts) == {"MIXED"}
                                      else "differs between cases: " + ", ".join(verdicts)))
    out = "\n".join(lines) + "\n"
    print(out, end="")
    open(os.path.join(HERE, "nonane_tb_conflict_out.txt"), "w").write(out)


if __name__ == "__main__":
    main()
