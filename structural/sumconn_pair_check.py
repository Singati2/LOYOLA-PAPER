#!/usr/bin/env python3
"""Check of Example ex:sumconn of main.tex from the trees themselves.

Among all chemical trees of order 18 (maximum degree <= 4), find the pairs whose degree-pair
profiles differ by 6(1,3) + 4(2,3) + 4(3,3) - 4(1,4) - 6(2,2) - 4(2,4) (the order-18 member
of the family in Example 2.2 of Rada, Rodriguez and Sigarreta 2022), confirm that their
sum-connectivity indices agree, and evaluate D(gamma) = LO(S;0,-1/2,gamma) - LO(T;0,-1/2,gamma)
from the profiles at 50 significant digits against the closed form in the example.

  python3 structural/sumconn_pair_check.py     (about 5 s)

Output: structural/sumconn_pair_check_out.txt (committed).  Exit 1 on any mismatch.
"""
import os, sys
from collections import Counter
import networkx as nx
from mpmath import mp, mpf, exp, power, sqrt, nstr
mp.dps = 50
DIFF = Counter({(1, 3): 6, (2, 3): 4, (3, 3): 4, (1, 4): -4, (2, 2): -6, (2, 4): -4})
H = mpf(1) / 2


def profile(G):
    d = dict(G.degree())
    return Counter(tuple(sorted((d[u], d[v]))) for u, v in G.edges())


def lo(p, a, b, g):
    return sum(c * power(i * j, a) * power(i + j, b) * exp(g * mpf(j - i) / (i + j)) for (i, j), c in p.items())


def closed_form(g):
    return 3 * (exp(g / 2) - 1) - 4 / sqrt(5) * (exp(3 * g / 5) - exp(g / 5)) + 4 / sqrt(6) * (1 - exp(g / 3))


def main():
    profs = {}
    for T in nx.nonisomorphic_trees(18):
        if max(dict(T.degree()).values()) <= 4:
            p = profile(T); profs[tuple(sorted(p.items()))] = p
    pairs = []
    for p in profs.values():
        q = Counter(p); q.subtract(DIFF)
        if min(q.values()) >= 0 and tuple(sorted((k, v) for k, v in q.items() if v)) in profs:
            pairs.append((p, +q))
    lines = [f"chemical trees of order 18: {len(profs)} profiles; pairs with the stated difference: {len(pairs)}"]
    ok = len(pairs) >= 1
    for S, T in pairs:
        chi = lo(S, 0, -H, 0) - lo(T, 0, -H, 0)
        lines.append(f"chi(S) - chi(T) = {nstr(chi, 3)}"); ok &= abs(chi) < mpf(10) ** -40
        for g in (mpf(1), mpf("1e-6"), mpf(-1)):
            d, f = lo(S, 0, -H, g) - lo(T, 0, -H, g), closed_form(g)
            lines.append(f"gamma = {nstr(g, 3)}: D from trees {nstr(d, 10)}, closed form {nstr(f, 10)}")
            ok &= abs(d - f) < mpf(10) ** -40
    d1, d6 = closed_form(mpf(1)), closed_form(mpf("1e-6"))
    ok &= nstr(d1, 4) == "0.2255" and nstr(d6, 2) == "2.4e-7"
    lines.append("RESULT: " + ("Example ex:sumconn confirmed (D(1) = 0.2255, D(1e-6) = 2.4e-7)" if ok else "MISMATCH"))
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sumconn_pair_check_out.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines)); sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
