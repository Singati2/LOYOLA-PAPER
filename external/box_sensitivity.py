#!/usr/bin/env python3
"""Search-box sensitivity of the GM-vs-LO comparison (added after the expert
review found that the parent's selections lie on the U(-2,2) box boundary).

For every property (octanes: 5; nonanes: T_B, dHvap), seeds 0..49, budget 2000,
and half-widths L in {2, 12}: candidates U(-L,L)^3 (LO, drawn first) and
U(-L,L)^2 with gamma = 0 (GM), rounded to 3 dp; for L = 12 also a hybrid LO
control with (alpha, beta) in U(-12,12)^2 and gamma in U(-2,2), which avoids
diluting LO's search over a wide gamma range (drawn after GM from the same rng); fully nested LOO selection
exactly as in the main analysis. Records outer Q2 and the number of outer folds
whose selected candidate lies within 10% of the box boundary in any coordinate.
L = 12 is non-binding for both models on dHvap (dense-grid check: GM selections
interior in all folds at L = 12).

Output: box_sensitivity.csv, box_sensitivity_summary.csv
"""
import csv, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import baselines as B
from octane_data import OCTANES, PROPS, alkane_pairs

SEEDS, BUDGET, BOXES = range(50), 2000, (2, 12)


def cells():
    P8 = [alkane_pairs(r[0]) for r in OCTANES]
    for k, p in enumerate(PROPS):
        yield "octane", p, P8, np.array([r[1 + k] for r in OCTANES])
    rows = list(csv.DictReader(open(os.path.join(HERE, "nonane_data.csv"))))
    for p, col in (("T_B", "T_B_C"), ("dHvap", "dHvap_kcal")):
        keep = [r for r in rows if r[col].strip()]
        yield "nonane", p, [alkane_pairs(r["smiles"]) for r in keep], np.array([float(r[col]) for r in keep])


def q2(p, y):
    return 1 - ((p - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def main():
    out = []
    for ds, prop, P, y in cells():
        for L in BOXES:
            for seed in SEEDS:
                rng = np.random.default_rng(seed)
                lo = np.round(rng.uniform(-L, L, (BUDGET, 3)), 3)
                gm = np.column_stack([np.round(rng.uniform(-L, L, (BUDGET, 2)), 3), np.zeros(BUDGET)])
                pl, sl = B.outer_loo(B.fold_select_ols, B.descriptor_matrix(P, lo), y)
                pg, sg = B.outer_loo(B.fold_select_ols, B.descriptor_matrix(P, gm), y)
                el = sum(np.abs(lo[s]).max() >= 0.9 * L for s in sl)
                eg = sum(np.abs(gm[s][:2]).max() >= 0.9 * L for s in sg)
                if L == 12:
                    hy = np.round(np.column_stack([rng.uniform(-L, L, (BUDGET, 2)), rng.uniform(-2, 2, BUDGET)]), 3)
                    ph, _ = B.outer_loo(B.fold_select_ols, B.descriptor_matrix(P, hy), y)
                    qh = f"{q2(ph, y):+.10f}"
                else:
                    qh = ""
                out.append([ds, prop, len(y), L, seed, f"{q2(pg, y):+.10f}", f"{q2(pl, y):+.10f}", int(eg), int(el), qh])
            print(f"{ds} {prop} L={L} done", flush=True)
    with open(os.path.join(HERE, "box_sensitivity.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["dataset", "property", "n", "L", "seed", "Q2_GM", "Q2_LO", "GM_edge_folds", "LO_edge_folds", "Q2_LO_hybrid"])
        w.writerows(out)
    summ = []
    for ds, prop, P, y in cells():
        for L in BOXES:
            r = [x for x in out if x[0] == ds and x[1] == prop and x[3] == L]
            g = np.array([float(x[5]) for x in r]); l = np.array([float(x[6]) for x in r])
            h = np.array([float(x[9]) for x in r]) if L == 12 else None
            summ.append([ds, prop, len(y), L, len(r), f"{np.median(g):.10f}", f"{np.median(l):.10f}",   # v40.13: full precision; the table generator rounds once
                         f"{np.median(l - g):+.10f}", int((l > g).sum()),
                         f"{np.mean([x[7] for x in r]) / len(y):.10f}", f"{np.mean([x[8] for x in r]) / len(y):.10f}",
                         f"{np.median(h):.10f}" if h is not None else "", f"{np.median(h - g):+.10f}" if h is not None else "",
                         int((h > g).sum()) if h is not None else ""])
    with open(os.path.join(HERE, "box_sensitivity_summary.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "property", "n", "L", "n_seeds", "median_Q2_GM", "median_Q2_LO", "median_dQ2",
                    "LO_better", "GM_edge_frac", "LO_edge_frac",
                    "median_Q2_LO_hybrid", "median_dQ2_hybrid", "LO_hybrid_better"])
        w.writerows(summ)
    for s in summ: print(s)


if __name__ == "__main__":
    main()
