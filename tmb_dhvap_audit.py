#!/usr/bin/env python3
"""Sensitivity of the Table 4 dHvap column to the 2,2,3,3-tetramethylbutane value
(source trace in TMB_DHVAP_AUDIT.md).  Each variant is reported separately; none
replaces the benchmark value used in the paper.

  python3 tmb_dhvap_audit.py          (seconds)

Output: tmb_dhvap_audit.csv (committed).
"""
import csv, os
import numpy as np
import octane_data as od

HERE = os.path.dirname(os.path.abspath(__file__))
KJ = 4.184
INDICES = [("M1", (0, 1, 0)), ("M2", (1, 0, 0)), ("HM", (0, 2, 0)), ("mM2", (-1, 0, 0)), ("R", (-.5, 0, 0)),
           ("chi", (0, -.5, 0)), ("H/2", (0, -1, 0)), ("ISI", (1, -1, 0)), ("GA", (.5, -1, 0)), ("AG", (-.5, 1, 0)),
           ("LO(0,0,1)", (0, 0, 1)), ("LO(0,0,2)", (0, 0, 2))]
VARIANTS = [
    ("original", 8.410, "benchmark value (Milano octane set, DHVAP); source and reference state unstated"),
    ("excluded", None, "isomer removed (n = 17)"),
    ("hypothetical liquid estimate", (43.37 - 7.54) / KJ,
     "dsubH(298 K) 43.37 kJ/mol minus dfusH(373.9 K) 7.54 kJ/mol (Scott et al. 1952 via NIST); no heat-capacity correction"),
    ("NIST 298 K, solid to gas", 42.94 / KJ,
     "NIST dvapH 42.94 kJ/mol (Majer-Svoboda 1985); the compound is crystalline at 298 K, value equals dsubH (Circular 461: 10.24, footnote b)"),
]


def main():
    P = [od.alkane_pairs(r[0]) for r in od.OCTANES]
    y = np.array([r[3] for r in od.OCTANES]); it = od.NAMES.index("2,2,3,3-tetramethylbutane")
    X = {k: np.array([od.lo_pairs(p, *t) for p in P]) for k, t in INDICES}
    out = []
    for name, val, note in VARIANTS:
        m = np.ones(len(y), bool); yy = y.copy()
        if val is None:
            m[it] = False
        else:
            yy[it] = val
        r = {k: abs(np.corrcoef(X[k][m], yy[m])[0, 1]) for k, _ in INDICES}
        s = sorted(r.items(), key=lambda t: -t[1])
        out.append([name, "" if val is None else f"{val:.3f}", s[0][0], f"{s[0][1]:.4f}", s[1][0], f"{s[1][1]:.4f}",
                    f"{r['LO(0,0,1)']:.4f}", f"{min(r.values()):.4f}", note])
    with open(os.path.join(HERE, "tmb_dhvap_audit.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["variant", "tmb_dhvap_kcal", "top_index", "top_abs_r", "second_index", "second_abs_r",
                    "abs_r_LO001", "min_abs_r", "note"]); w.writerows(out)
    for o in out:
        print(o[:8])


if __name__ == "__main__":
    main()
