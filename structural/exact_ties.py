#!/usr/bin/env python3
"""Exact certification of the distinct-value counts that structural_checks.py, hp_counts.py,
chi_floor.py and fractional_points.py obtain numerically (11 and 32 significant digits).

Every index value used there is a finite sum of edge weights (ij)^a (i+j)^b e^(g q_ij) with rational
a, b and g in {0, 1}. Write k for the least common denominator of a and b. Each weight is then
r * N^(1/k) * e^(g q) with r rational and N a k-th-power-free positive integer (computed exactly below).
Two values are equal if and only if their coefficient maps (q, N) -> r agree:
  * for g = 0, because the k-th roots of distinct k-th-power-free positive integers are linearly
    independent over the rationals (Besicovitch 1940);
  * for g = 1, because the coefficients are algebraic and the exponents q distinct rationals, so by
    the Lindemann-Weierstrass theorem a vanishing sum needs every q-coefficient to vanish, and then
    Besicovitch applies to each of them.
So the counts below are exact: no rounding and no tolerance. They are compared with the committed
numerical counts. Trees are generated with networkx, and the tree counts are asserted against OEIS
A000055 (all trees) and A000602 (trees with maximum degree at most 4).

  cd structural && python3 exact_ties.py      -> exact_ties_out.txt      (a few minutes)
"""
import os, re, sys
from fractions import Fraction as F
from math import lcm
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
A000055 = {2: 1, 3: 1, 4: 2, 5: 3, 6: 6, 7: 11, 8: 23, 9: 47, 10: 106, 11: 235, 12: 551, 13: 1301,
           14: 3159, 15: 7741, 16: 19320, 17: 48629}
A000602 = {2: 1, 3: 1, 4: 2, 5: 3, 6: 5, 7: 9, 8: 18, 9: 35, 10: 75, 11: 159, 12: 355, 13: 802,
           14: 1858, 15: 4347, 16: 10359, 17: 24894}


def kth_free(M, k):
    """M = c^k * N with N k-th-power-free; returns (c, N)."""
    c, N, p = 1, 1, 2
    while p * p <= M or M > 1:
        if p * p > M:
            p = M
        e = 0
        while M % p == 0:
            M //= p; e += 1
        c *= p ** (e // k); N *= p ** (e % k)
        p += 1
    return c, N


def weight(i, j, a, b, g):
    """Exact representation (key, r) of (ij)^a (i+j)^b e^(g q_ij): value = r * N^(1/k) * e^(g q)."""
    k = lcm(a.denominator, b.denominator)
    xk = F(i * j) ** int(a * k) * F(i + j) ** int(b * k)            # x^k, rational
    P, Q = xk.numerator, xk.denominator
    c, N = kth_free(P * Q ** (k - 1), k)                              # x = c N^(1/k) / Q
    q = F(abs(i - j), i + j) if g else None
    return (q, N), F(c, Q)


def value_key(profile, a, b, g, cache):
    acc = {}
    for e in profile:
        if e not in cache:
            cache[e] = weight(e[0], e[1], a, b, g)
        key, r = cache[e]
        acc[key] = acc.get(key, 0) + r
    return frozenset((key, r) for key, r in acc.items() if r != 0)


def qhist(profile):
    return tuple(sorted(F(abs(i - j), i + j) for i, j in profile))


HALF, THIRD, SIXTH = F(1, 2), F(1, 3), F(1, 6)
TABLE = {"R": (-HALF, F(0), 0), "chi": (F(0), -HALF, 0), "GA": (HALF, F(-1), 0)}   # GA up to the factor 2
FRAC = [(F(0), HALF), (HALF, F(0)), (F(0), -HALF), (-HALF, F(0)), (HALF, F(-1)), (-HALF, F(1)),
        (THIRD, F(0)), (F(0), THIRD), (SIXTH, F(0))]                  # the points of fractional_points.py


def committed():
    """Numerical counts committed by the other scripts."""
    hp, chi, frac, prof = {}, {}, {}, {}
    for line in open(os.path.join(HERE, "hp_counts_out.txt")):
        m = re.match(r"n=(\d+) (all|mol) N=\d+ qhist=(\d+) GA_qmerges=\d+ R=(\d+) GA=(\d+)", line)
        if m:
            hp[(int(m[1]), m[2])] = dict(qhist=int(m[3]), R=int(m[4]), GA=int(m[5]))
    for line in open(os.path.join(HERE, "chi_floor_out.txt")):
        m = re.match(r"n=(\d+) profiles=(\d+) chi_distinct=(\d+)", line)
        if m:
            chi[int(m[1])] = int(m[3])
    for line in open(os.path.join(HERE, "fractional_points_out.txt")):
        m = re.match(r"\s*n=(\d+) profiles=(\d+) (.*)", line)
        if m:
            prof[int(m[1])] = int(m[2])
            for a, b, g, c in re.findall(r"\((-?[\d.]+),(-?[\d.]+),([01])\):(\d+)", m[3]):
                frac[(int(m[1]), float(a), float(b), int(g))] = int(c)
    return hp, chi, frac, prof


def main():
    hp, chi_ref, frac_ref, prof_ref = committed()
    out, bad = [], []
    first_ga_merge = {}
    for n in range(2, 18):
        trees = list(nx.nonisomorphic_trees(n)) if n > 2 else [nx.path_graph(2)]
        assert len(trees) == A000055[n], (n, len(trees))
        profs = [tuple(sorted(tuple(sorted((T.degree(u), T.degree(v)))) for u, v in T.edges())) for T in trees]
        for sub in ("all", "mol"):
            P = set(p for p in profs if sub == "all" or max(max(e) for e in p) <= 4)
            if sub == "mol":
                assert sum(1 for T in trees if max(d for _, d in T.degree()) <= 4) == A000602[n], n
            qh = {qhist(p) for p in P}
            cnt = {}
            for name, (a, b, g) in TABLE.items():
                cache = {}
                cnt[name] = len({value_key(p, a, b, g, cache) for p in P})
            # GA merges two distinct q-histograms iff it has fewer values than q-histograms (GA is on the ratio plane)
            merges = len(qh) - cnt["GA"]
            if merges > 0 and sub not in first_ga_merge:
                first_ga_merge[sub] = n
            line = f"n={n} {sub} profiles={len(P)} qhist={len(qh)} R={cnt['R']} chi={cnt['chi']} GA={cnt['GA']} GA_qmerges={merges}"
            ref = hp.get((n, sub))
            if ref:
                ok = ref["qhist"] == len(qh) and ref["R"] == cnt["R"] and ref["GA"] == cnt["GA"]
                line += f" | 32-digit counts {'CERTIFIED' if ok else 'DIFFER'}"
                if not ok: bad.append(line)
            if sub == "all" and n in chi_ref:
                ok = chi_ref[n] == cnt["chi"]
                line += f" | chi {'CERTIFIED' if ok else 'DIFFERS'}"
                if not ok: bad.append(line)
            out.append(line); print(line, flush=True)
        if 12 <= n <= 16:
            P = set(profs)
            assert prof_ref[n] == len(P), n
            parts = []
            for a, b in FRAC:
                for g in (0, 1):
                    cache = {}
                    c = len({value_key(p, a, b, g, cache) for p in P})
                    r = frac_ref[(n, round(float(a), 3), round(float(b), 3), g)]
                    parts.append(f"({a},{b},{g}):{c}{'' if c == r else '!=' + str(r)}")
                    if c != r: bad.append(f"n={n} fractional ({a},{b},{g}): exact {c}, committed {r}")
            if n == 16:
                cache = {}
                c = len({value_key(p, F(3, 10), F(1, 5), 0, cache) for p in P})
                parts.append(f"(3/10,1/5,0):{c}")
                if c != len(P): bad.append(f"n=16 LO(3/10,1/5,0): {c} values for {len(P)} profiles")
            line = f"n={n} all fractional points, exact: " + " ".join(parts)
            out.append(line); print(line, flush=True)
    out.append(f"GA merges two distinct q-histograms first at order {first_ga_merge.get('all', 'none <= 17')} (all trees), "
               f"{first_ga_merge.get('mol', 'none up to 17')} (max degree <= 4); orders 2-17 examined")
    out.append("RESULT: " + ("all numerical counts certified exactly" if not bad else f"{len(bad)} DIFFERENCES: " + "; ".join(bad)))
    print("\n".join(out[-2:]))
    open(os.path.join(HERE, "exact_ties_out.txt"), "w").write("\n".join(out) + "\n")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
