#!/usr/bin/env python3
"""Independent interval checks of the finite rank claim and five-crossing witness.
Run: python audit/check_mathematics.py. Requires locked mpmath and networkx.
This checks these two claims only, not every theorem of the manuscript.
"""
import itertools
from collections import Counter, defaultdict
from fractions import Fraction
import mpmath as mp
import networkx as nx

mp.iv.dps = 50


def excludes_zero(x):
    return x.a > 0 or x.b < 0


def determinant(A):
    if len(A) == 1:
        return A[0][0]
    if len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1])
            - A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0])
            + A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))


def check_rank():
    for delta in (6, 7):
        pairs = [(i, j) for i in range(1, delta + 1) for j in range(i, delta + 1)]
        Z = {p: [mp.iv.log(p[0] * p[1]), mp.iv.log(sum(p)),
                 mp.iv.mpf(p[1] - p[0]) / sum(p)] for p in pairs}
        uncertified, count = [], 0
        for k in range(2, 5):
            for S in itertools.combinations(pairs, k):
                count += 1
                r = len({Fraction(j - i, j + i) for i, j in S})
                target = min(k - 1, r, 3)
                M = [[Z[p][c] - Z[S[0]][c] for c in range(3)] for p in S[1:]]
                certified = any(excludes_zero(determinant([[M[a][b] for b in cols] for a in rows]))
                                for rows in itertools.combinations(range(k - 1), target)
                                for cols in itertools.combinations(range(3), target))
                if not certified:
                    uncertified.append(S)
        expected = [] if delta == 6 else [((1, 7), (2, 6), (3, 5), (4, 4))]
        assert uncertified == expected, (delta, uncertified)
        # In the exception every i+j is 8, hence the log-sum coordinate is
        # constant and affine rank is at most 2. Other subsets have the
        # lower-rank minors just certified; the paper supplies the upper bound.
        print(f"Delta={delta}: {count} subsets; exceptions {uncertified}", flush=True)


def interval_fraction(x):
    return mp.iv.mpf(x.numerator) / x.denominator


def check_lemma1_witness():
    """Lemma 3.1 without the pair (1,1): the augmented vectors of (1,2), (1,3), (2,2), (3,3) are linearly independent
    (their 4x4 determinant is about -0.015), certified in 50-digit interval arithmetic (Laplace expansion along
    the first column, each 3x3 minor evaluated by determinant() on mp.iv intervals)."""
    rows = [[mp.iv.mpf(1), mp.iv.log(i * j), mp.iv.log(i + j), mp.iv.mpf(abs(i - j)) / (i + j)]
            for i, j in ((1, 2), (1, 3), (2, 2), (3, 3))]
    d = mp.iv.mpf(0)
    for r in range(4):
        minor = [row[1:] for k, row in enumerate(rows) if k != r]
        d += (-1) ** r * rows[r][0] * determinant(minor)
    assert d.b < mp.mpf("-0.014") and d.a > mp.mpf("-0.016"), f"Lemma 3.1 witness determinant {d}"
    print(f"Lemma 3.1 witness without (1,1): determinant {mp.nstr(mp.mpf(d.mid.a), 12)} != 0 certified")


def check_crossings():
    G = Counter({(1, 6): 5, (1, 3): 2, (1, 4): 2, (3, 4): 1, (4, 6): 1})
    H = Counter({(1, 5): 4, (1, 6): 4, (1, 2): 1, (2, 6): 1, (5, 6): 1})
    found = set()
    for T in nx.nonisomorphic_trees(12):
        d = dict(T.degree())
        profile = Counter(tuple(sorted((d[u], d[v]))) for u, v in T.edges())
        for name, witness in (("G", G), ("H", H)):
            if profile == witness:
                found.add(name)
    assert found == {"G", "H"}, found
    c = defaultdict(Fraction)
    for profile, sign in ((G, 1), (H, -1)):
        for (i, j), count in profile.items():
            c[Fraction(j - i, i + j)] += sign * Fraction(count, i * j)
    coefficients = sorted((q, v) for q, v in c.items() if v)
    V = sum((a > 0) != (b > 0) for (_, a), (_, b) in zip(coefficients, coefficients[1:]))
    assert V == 5

    def D(x):
        return sum(interval_fraction(v) * mp.iv.exp(mp.iv.mpf(x) * interval_fraction(q))
                   for q, v in coefficients)

    for a, b in (("-17.18", "-17.16"), ("-11.97", "-11.95"),
                 ("-2.04", "-2.02"), ("2.72", "2.74"), ("31.12", "31.14")):
        left, right = D(a), D(b)
        assert excludes_zero(left) and excludes_zero(right)
        assert (left.a > 0) != (right.a > 0)
        print(f"Opposite interval signs: [{a}, {b}]", flush=True)
    print("Five distinct crossings certified, conditional on the stated Laguerre bound.")


if __name__ == "__main__":
    check_rank()
    check_lemma1_witness()
    check_crossings()
    print("Mathematics interval checks PASS")
