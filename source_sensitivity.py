#!/usr/bin/env python3
"""Data-source sensitivity of the omega and S columns of tab:lo_octane.

omega: the acentric factors of 2,2,4-trimethylpentane (0.305 -> 0.303) and
2,2,3,3-tetramethylbutane (0.247 -> 0.251) are replaced by the compiled
KDB values (provenance CSV).

S: the four gas-phase entropies that could not be matched to a primary
source and differ from the standard octane QSPR dataset (arXiv:1701.02859,
Table 1) are replaced by the dataset values:
  octane 111.55 -> 111.70; 2,2-dimethylhexane 103.13 -> 103.40;
  2,2,4-trimethylpentane 101.81 -> 104.10; 2,3,3-trimethylpentane 102.06 -> 102.10
  (v40.5: base value corrected from the duplicated 101.31).
(The primary data are NOT changed; this is a disclosure-only sensitivity.)

Outputs (next to this script): omega_source_sensitivity_v35.csv,
entropy_source_sensitivity_v36.csv. Columns: index, r_original,
r_alternative (full precision), displayed values (3 dp), whether the
displayed value changes, and whether the column winner changes.
"""
import csv, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from octane_data import OCTANES, NAMES, PROPS, alkane_pairs, lo_pairs

IDX = [("M1", (0, 1, 0)), ("M2", (1, 0, 0)), ("HM", (0, 2, 0)), ("mM2", (-1, 0, 0)),
       ("R", (-0.5, 0, 0)), ("chi", (0, -0.5, 0)), ("H/2", (0, -1, 0)), ("ISI", (1, -1, 0)),
       ("GA", (0.5, -1, 0)), ("AG", (-0.5, 1, 0)), ("LO(0,0,1)", (0, 0, 1)), ("LO(0,0,2)", (0, 0, 2))]

OMEGA_ALT = {"2,2,4-trimethylpentane": 0.303, "2,2,3,3-tetramethylbutane": 0.251}
S_ALT = {"octane": 111.70, "2,2-dimethylhexane": 103.40,
         "2,2,4-trimethylpentane": 104.10, "2,3,3-trimethylpentane": 102.10}


def r_signed(x, y):
    xc = x - x.mean(); yc = y - y.mean()
    return float(xc @ yc / (np.linalg.norm(xc) * np.linalg.norm(yc)))


def sensitivity(prop, alt, fname, prefix):
    OP = [alkane_pairs(r[0]) for r in OCTANES]
    j = PROPS.index(prop)
    y0 = np.array([r[1 + j] for r in OCTANES]); y1 = y0.copy()
    for nm, v in alt.items():
        y1[NAMES.index(nm)] = v
    R0, R1 = {}, {}
    for nm, t in IDX:
        x = np.array([lo_pairs(P, *t) for P in OP])
        R0[nm] = r_signed(x, y0); R1[nm] = r_signed(x, y1)
    w0 = max(R0, key=lambda k: abs(R0[k])); w1 = max(R1, key=lambda k: abs(R1[k]))
    with open(os.path.join(HERE, fname), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["index", f"r_{prefix}_original", f"r_{prefix}_alternative",
                    "displayed_original", "displayed_alternative", "displayed_changes", "winner_changes"])
        for nm, _ in IDX:
            d0, d1 = f"{R0[nm]:+.3f}", f"{R1[nm]:+.3f}"
            w.writerow([nm, f"{R0[nm]:+.10f}", f"{R1[nm]:+.10f}", d0, d1, d0 != d1, w0 != w1])
    n = sum(f"{R0[k]:+.3f}" != f"{R1[k]:+.3f}" for k in R0)
    print(f"{prop}: {n}/12 displayed correlations change; winner {w0} -> {w1}; "
          f"max |shift| = {max(abs(R1[k]-R0[k]) for k in R0):.4f}")


if __name__ == "__main__":
    sensitivity("omega", OMEGA_ALT, "omega_source_sensitivity_v35.csv", "omega")
    sensitivity("S", S_ALT, "entropy_source_sensitivity_v36.csv", "S")
