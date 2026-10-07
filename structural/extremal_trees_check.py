#!/usr/bin/env python3
"""Exhaustive check of the extremal-tree proposition for the pure-gamma points
(main paper, Section 4): among all trees of order n, the path P_n is the unique
minimiser and the star S_n the unique maximiser of LO(T;0,0,gamma) for gamma > 0,
with the roles exchanged for gamma < 0, and the two bounds
(n-3) + 2 e^{gamma/3} and (n-1) e^{gamma (n-2)/n} are attained.
Orders 4..MAX_N (all non-isomorphic trees, networkx), gamma in GAMMAS.
Output: structural/extremal_trees_check_out.txt (committed).  Runtime: seconds."""
import math, os
import networkx as nx

MAX_N = 12
GAMMAS = (0.3, 1.0, 2.0, -1.0)
HERE = os.path.dirname(os.path.abspath(__file__))


def lo(T, g):
    return sum(math.exp(g * abs(T.degree(u) - T.degree(v)) / (T.degree(u) + T.degree(v))) for u, v in T.edges())


def main():
    lines = []; bad = 0
    for n in range(4, MAX_N + 1):
        trees = list(nx.nonisomorphic_trees(n))
        for g in GAMMAS:
            vals = sorted((lo(T, g), sum(1 for v in T if T.degree(v) == 1), max(d for _, d in T.degree())) for T in trees)
            path = (n - 3) + 2 * math.exp(g / 3); star = (n - 1) * math.exp(g * (n - 2) / n)
            lo_end, hi_end = (vals[0], vals[-1]) if g > 0 else (vals[-1], vals[0])
            second_lo, second_hi = (vals[1], vals[-2]) if g > 0 else (vals[-2], vals[1])
            ok = (abs(lo_end[0] - path) < 1e-9 and lo_end[1] == 2 and abs(hi_end[0] - star) < 1e-9 and hi_end[2] == n - 1
                  and abs(second_lo[0] - path) > 1e-9 and abs(second_hi[0] - star) > 1e-9)
            bad += not ok
            lines.append(f"n={n:2d} gamma={g:+.1f} trees={len(trees):4d}: path unique min/star unique max (gamma>0; exchanged for gamma<0): {'OK' if ok else 'FAIL'}")
    lines.append(f"RESULT: {'extremal-tree proposition holds for all orders 4..%d' % MAX_N if bad == 0 else str(bad) + ' FAILURES'}")
    print("\n".join(lines)); open(os.path.join(HERE, "extremal_trees_check_out.txt"), "w").write("\n".join(lines) + "\n")
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
