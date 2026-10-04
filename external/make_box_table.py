#!/usr/bin/env python3
"""Rows of tab:box (manuscript) from box_sensitivity_summary.csv, rounded once."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
TEX = {"T_B": r"$T_B$", "dHf": r"$\Delta H_f$", "dHvap": r"$\Delta H_{\mathrm{vap}}$", "S": r"$S$", "omega": r"$\omega$"}
R = {(r["dataset"], r["property"], int(r["L"])): r for r in csv.DictReader(open(os.path.join(HERE, "box_sensitivity_summary.csv")))}
out = []
for ds, props in (("octane", ["T_B", "dHf", "dHvap", "S", "omega"]), ("nonane", ["T_B", "dHvap"])):
    for p in props:
        a, b = R[(ds, p, 2)], R[(ds, p, 12)]
        cells = [("oct." if ds == "octane" else "non.") + " " + TEX[p],
                 f"${100*float(a['GM_edge_frac']):.0f}\\%$",
                 f"${float(a['median_Q2_GM']):.3f}$", f"${float(a['median_Q2_LO']):.3f}$", f"${a['LO_better']}$",
                 f"${100*float(b['GM_edge_frac']):.0f}\\%$",
                 f"${float(b['median_Q2_GM']):.3f}$", f"${float(b['median_Q2_LO']):.3f}$",
                 f"${float(b['median_Q2_LO_hybrid']):.3f}$", f"${b['LO_hybrid_better']}$"]
        out.append(" & ".join(cells) + r"\\")
open(os.path.join(HERE, "box_table_rows.tex"), "w").write("\n".join(out) + "\n")
print("\n".join(out))
