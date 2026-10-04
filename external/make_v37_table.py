#!/usr/bin/env python3
"""Build the manuscript's external-validation/baseline table (tab:external)
from the result CSVs (rounded once, 3 dp), and the classical-only fixed-index
baseline (computed here, nested LOO). Writes v37_table_rows.tex and
v37_classical_fixed.csv. No number in the table is typed by hand."""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import baselines as B
from octane_data import OCTANES, PROPS, alkane_pairs

CLASSICAL = [x for x in B.FIXED_INDICES if not x[0].startswith("LO(")]
TEX = {"T_B": r"$T_B$", "dHf": r"$\Delta H_f$", "dHvap": r"$\Delta H_{\mathrm{vap}}$",
       "S": r"$S$", "omega": r"$\omega$"}


def fixed_lo1_q2(P, y):
    x = B.descriptor_matrix(P, [(0.0, 0.0, 1.0)])[0]
    preds = np.array([B.fit_predict(np.delete(x, i), np.delete(y, i), x[i]) for i in range(len(y))])
    return B.scores(preds, y)[0]


def classical_q2(P, y):
    X = B.descriptor_matrix(P, [t for _, t in CLASSICAL])
    preds, _ = B.outer_loo(B.fold_select_ols, X, y)
    return B.scores(preds, y)[0]


def f3(x):
    return f"{x:+.3f}".replace("+", "+") if x < 0 else f"{x:.3f}"


def main():
    base = {}
    for ds, fn in (("octane", "baselines_octane.csv"), ("nonane", "baselines_nonane.csv")):
        for r in csv.DictReader(open(os.path.join(HERE, fn))):
            prop = {"T_B_C": "T_B", "dHvap_kcal": "dHvap"}.get(r["property"], r["property"])
            base[(ds, prop, r["method"])] = float(r["Q2"])
    # LO-better counts
    cnt = {}
    for r in csv.DictReader(open(os.path.join(os.path.dirname(HERE), "expanded_robustness_summary_v35.csv"))):
        cnt[("octane", r["property"], int(r["budget"]))] = int(r["LO_better"])
    for r in csv.DictReader(open(os.path.join(HERE, "nonane_validation_summary.csv"))):
        if r["analysis"] == "primary":
            cnt[("nonane", r["property"], int(r["budget"]))] = int(r["LO_better"])
    # classical-only fixed baseline
    cls = {}; lo1 = {}
    P8 = [alkane_pairs(r[0]) for r in OCTANES]
    for k, p in enumerate(PROPS):
        cls[("octane", p)] = classical_q2(P8, np.array([r[1 + k] for r in OCTANES]))
        lo1[("octane", p)] = fixed_lo1_q2(P8, np.array([r[1 + k] for r in OCTANES]))
    rows9 = list(csv.DictReader(open(os.path.join(HERE, "nonane_data.csv"))))
    for p, col in (("T_B", "T_B_C"), ("dHvap", "dHvap_kcal")):
        keep = [r for r in rows9 if r[col].strip()]
        cls[("nonane", p)] = classical_q2([alkane_pairs(r["smiles"]) for r in keep],
                                          np.array([float(r[col]) for r in keep]))
        lo1[("nonane", p)] = fixed_lo1_q2([alkane_pairs(r["smiles"]) for r in keep],
                                          np.array([float(r[col]) for r in keep]))
    with open(os.path.join(HERE, "v37_classical_fixed.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["dataset", "property", "Q2_classical_fixed_best"])
        for (ds, p), v in cls.items():
            w.writerow([ds, p, f"{v:.10f}"])
    lines = []
    order = [("octane", p) for p in PROPS] + [("nonane", "T_B"), ("nonane", "dHvap")]
    for ds, p in order:
        q = lambda m: base[(ds, p, m)]
        cells = [("oct." if ds == "octane" else "non.") + " " + TEX[p],
                 f"${q('mean'):+.3f}$", f"${cls[(ds, p)]:.3f}$", f"${q('IRLA'):.3f}$",
                 f"${q('ridge_counts'):.3f}$", f"${lo1[(ds, p)]:.3f}$",
                 f"${q('GM_b200'):.3f}$", f"${q('LO_b200'):.3f}$",
                 f"${cnt[(ds, p, 200)]}/{cnt[(ds, p, 500)]}$"]
        lines.append(" & ".join(cells) + r"\\")
    open(os.path.join(HERE, "v37_table_rows.tex"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
