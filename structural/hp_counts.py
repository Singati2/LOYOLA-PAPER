#!/usr/bin/env python3
"""High-precision cross-check of the distinct-value counts of structural_checks.py S1.

structural_checks.py counts distinct index values at 11 significant digits.
Here every value is recomputed in 40-digit arithmetic (mpmath) and counted at
32 significant digits, for R, GA, LO(0,0,1) and LO(0,0,2) on all trees and on
the molecular trees (max degree <= 4) of orders 7-17 (molecular: 7-17), and
compared with the committed S1 output.  For the pure-gamma points the count
must equal the number of distinct q-histograms exactly (Lindemann-Weierstrass;
ratio-plane theorem of the paper), which is checked as well.
Also cross-checks Table S4 (multi_order_degeneracy.csv, 9-decimal rounding)
at 32 significant digits (40-digit arithmetic).  Output: hp_counts_out.txt (committed).  Runtime
about one minute."""
import os, sys, time
from collections import Counter
from fractions import Fraction
import networkx as nx, mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
mp.mp.dps = 40
IDX = {"R": (-0.5, 0, 0), "GA": (0.5, -1, 0), "LO1": (0, 0, 1), "LO2": (0, 0, 2)}


def val(P, a, b, g):
    return sum(mp.power(i * j, a) * mp.power(i + j, b) * mp.exp(g * mp.mpf(abs(i - j)) / (i + j)) for i, j in P)


def main():
    ref = {}
    for line in open(os.path.join(HERE, "structural_checks_out.txt")):
        t = line.split()
        if len(t) == 10 and t[0].isdigit() and t[1] in ("all", "mol"):
            ref[(int(t[0]), t[1])] = dict(zip(["N", "prof", "qh", "R", "GA", "LO1", "LO2", "merge"], map(int, t[2:])))
    out, bad, t0 = [], 0, time.time()
    for n in range(7, 18):
        trees = list(nx.nonisomorphic_trees(n))
        for sub in ("all", "mol"):
            if sub == "mol" and n > 17:
                continue
            vals = {k: set() for k in IDX}; qh = set(); N = 0; ga = {}
            for T in trees:
                d = dict(T.degree())
                if sub == "mol" and max(d.values()) > 4:
                    continue
                N += 1; P = [tuple(sorted((d[u], d[v]))) for u, v in T.edges()]
                q = tuple(sorted(Counter(Fraction(j - i, i + j) for i, j in P).items())); qh.add(q)
                for k, (a, b, g) in IDX.items():
                    vals[k].add(mp.nstr(val(P, a, b, g), 32))
                ga.setdefault(mp.nstr(2 * val(P, .5, -1, 0), 32), set()).add(q)
            hp = {k: len(v) for k, v in vals.items()}; r = ref[(n, sub)]
            merge = sum(1 for s_ in ga.values() if len(s_) > 1)
            same = all(hp[k] == r[k] for k in IDX) and N == r["N"] and len(qh) == r["qh"] and merge == r["merge"]
            exact = hp["LO1"] == len(qh) == hp["LO2"]
            bad += (not same) + (not exact)
            out.append(f"n={n} {sub} N={N} qhist={len(qh)} GA_qmerges={merge} " + " ".join(f"{k}={hp[k]}" for k in IDX)
                       + f" | 11-digit counts {'REPRODUCED' if same else 'DIFFER'} | pure-gamma counts == q-histograms: {exact}")
            print(out[-1], flush=True)
    # Table S4: multi_order_degeneracy.csv (12 indices, orders 7-12, rounded to 9 decimals)
    import csv
    sys.path.insert(0, os.path.dirname(HERE))
    import multi_order_degeneracy as MO
    for row in csv.DictReader(open(os.path.join(os.path.dirname(HERE), "multi_order_degeneracy.csv"))):
        n = int(row["n"]); trees = list(nx.nonisomorphic_trees(n))
        if row["graph_set"] == "molecular":
            trees = [T for T in trees if max(d for _, d in T.degree()) <= 4]
        Ps = [[tuple(sorted((T.degree(u), T.degree(v)))) for u, v in T.edges()] for T in trees]
        qn = len({tuple(sorted(Counter(Fraction(j - i, i + j) for i, j in P).items())) for P in Ps})
        hp = {nm: len({mp.nstr(val(P, a, b, g), 32) for P in Ps}) for nm, (a, b, g) in MO.INDICES}
        same = all(hp[nm] == int(row[nm]) for nm, _ in MO.INDICES) and len(trees) == int(row["N_trees"])
        exact = hp["LO001"] == qn == hp["LO002"]
        bad += (not same) + (not exact)
        out.append(f"Table S4 n={n} {row['graph_set']}: 9-decimal counts {'REPRODUCED' if same else 'DIFFER'} at 32 digits; pure-gamma counts == q-histograms: {exact}")
        print(out[-1], flush=True)
    out.append(f"RESULT: {'all counts reproduced at 32 significant digits' if bad == 0 else str(bad) + ' MISMATCHES'}")
    print(out[-1] + f" ({time.time()-t0:.0f} s)")   # runtime on stdout only, so the committed output is reproducible
    open(os.path.join(HERE, "hp_counts_out.txt"), "w").write("\n".join(out) + "\n")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
