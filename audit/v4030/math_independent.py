#!/usr/bin/env python3
"""Independent recomputation of the main mathematical claims (v40.30 adversarial audit).

Written without the repository's checkers. Trees come from networkx.nonisomorphic_trees (the
Wright-Richmond-Odlyzko-McKay generator); completeness is checked against OEIS (A000055 for all
trees, A000602 for trees with maximum degree <= 4), and duplicates are excluded with a canonical
form written here (AHU encoding rooted at the centre). Histograms use exact fractions; values of
GA and LO use 40-digit mpmath.
  python3 audit/v4030/math_independent.py      -> audit/v4030/math_independent_out.txt
"""
import itertools, os, sys
from collections import Counter, defaultdict
from fractions import Fraction
import networkx as nx
import mpmath as mp

mp.mp.dps = 40
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def say(s): print(s, flush=True); OUT.append(s)

A000055 = [1, 1, 1, 1, 2, 3, 6, 11, 23, 47, 106, 235, 551, 1301, 3159, 7741, 19320, 48629]   # n = 0..17
A000602 = [1, 1, 1, 1, 2, 3, 5, 9, 18, 35, 75, 159, 355, 802, 1858, 4347, 10359, 24894]     # n = 0..17


def canon(T):
    """Canonical string of a free tree: AHU encoding from the centre (bicentre: min of both)."""
    c = nx.center(T)
    def enc(v, p):
        return "(" + "".join(sorted(enc(w, v) for w in T[v] if w != p)) + ")"
    if len(c) == 1:
        return enc(c[0], None)
    a, b = c
    return "".join(sorted([enc(a, b), enc(b, a)]))


def profile(T):
    d = dict(T.degree())
    return tuple(sorted(Counter(tuple(sorted((d[u], d[v]))) for u, v in T.edges()).items()))


def qhist(P):
    h = Counter()
    for (i, j), c in P:
        h[Fraction(j - i, i + j)] += c
    return tuple(sorted(h.items()))


# ---------------------------------------------------------------- M1 collision orders
first = {False: None, True: None}; witness = {}
for n in range(2, 18):
    trees = list(nx.nonisomorphic_trees(n))
    assert len(trees) == A000055[n], (n, len(trees))
    assert len({canon(T) for T in trees}) == len(trees), f"duplicate trees at n={n}"
    for chem in (False, True):
        TT = [T for T in trees if max(dict(T.degree()).values()) <= 4] if chem else trees
        if chem: assert len(TT) == A000602[n], (n, len(TT))
        byh = defaultdict(set)
        for T in TT:
            P = profile(T); byh[qhist(P)].add(P)
        coll = [ps for ps in byh.values() if len(ps) > 1]
        if coll and first[chem] is None:
            first[chem] = n; witness[chem] = sorted(coll[0])
say(f"M1 complete enumeration n=2..17 matches OEIS A000055 and A000602; canonical forms distinct")
say(f"M1 first order with two distinct profiles sharing a q-histogram: all trees {first[False]}, max degree <= 4 {first[True]}")
for chem in (False, True):
    say(f"   witness ({'max deg <= 4' if chem else 'all trees'}): " + " | ".join(str(dict(p)) for p in witness[chem]))
paper13 = [{(1, 2): 1, (1, 3): 2, (1, 6): 5, (2, 3): 2, (2, 6): 1, (3, 3): 1}, {(1, 3): 3, (1, 6): 5, (2, 2): 1, (2, 3): 2, (3, 6): 1}]
paper16 = [{(1, 2): 2, (1, 4): 8, (2, 4): 2, (4, 4): 3}, {(1, 4): 8, (2, 2): 3, (2, 4): 4}]
for nm, (A, B), n in (("order 13", paper13, 13), ("order 16", paper16, 16)):
    hA, hB = qhist(tuple(sorted(A.items()))), qhist(tuple(sorted(B.items())))
    realised = {profile(T) for T in nx.nonisomorphic_trees(n)}
    say(f"   paper's {nm} pair: equal histograms {hA == hB}; both realised by trees of order {n}: "
        f"{tuple(sorted(A.items())) in realised and tuple(sorted(B.items())) in realised}")

# ---------------------------------------------------------------- M2 GA first merge of distinct histograms
def GA(P): return sum(c * 2 * mp.sqrt(i * j) / (i + j) for (i, j), c in P)
ga_first = None
for n in range(2, 18):
    hs = {qhist(profile(T)): profile(T) for T in nx.nonisomorphic_trees(n)}
    vals = sorted((GA(P), h) for h, P in hs.items())
    hit = [(a, b) for a, b in zip(vals, vals[1:]) if abs(a[0] - b[0]) < mp.mpf(10) ** -30]
    if hit and ga_first is None:
        ga_first = (n, len(hit))
say(f"M2 GA: first order at which two distinct q-histograms receive equal GA (40 digits): {ga_first[0]} ({ga_first[1]} such adjacent pairs)")
p1 = {(1, 5): 10, (2, 2): 2, (5, 5): 2, (2, 5): 1, (1, 2): 1}; p2 = {(4, 5): 3, (1, 4): 5, (1, 5): 6, (2, 5): 1, (1, 2): 1}
say(f"   paper's order-17 GA example: GA difference {mp.nstr(GA(p1.items()) - GA(p2.items()), 5)}; histograms differ "
    f"{qhist(tuple(sorted(p1.items()))) != qhist(tuple(sorted(p2.items())))}")

# ---------------------------------------------------------------- M3 five crossings (Remark rem:crossings)
G = {(1, 3): 2, (1, 4): 2, (1, 6): 5, (3, 4): 1, (4, 6): 1}; H = {(1, 2): 1, (1, 5): 4, (1, 6): 4, (2, 6): 1, (5, 6): 1}
def D(g, a=-1, b=0):
    s = mp.mpf(0)
    for P, sg in ((G, 1), (H, -1)):
        for (i, j), c in P.items():
            s += sg * c * mp.mpf(i * j) ** a * mp.mpf(i + j) ** b * mp.e ** (g * mp.mpf(j - i) / (i + j))
    return s
cq = defaultdict(lambda: mp.mpf(0))
for P, sg in ((G, 1), (H, -1)):
    for (i, j), c in P.items(): cq[Fraction(j - i, i + j)] += sg * c * mp.mpf(i * j) ** -1
signs = [mp.sign(cq[q]) for q in sorted(cq) if cq[q] != 0]
V = sum(1 for x, y in zip(signs, signs[1:]) if x != y)
grid = [mp.mpf(-60) + k * mp.mpf("0.05") for k in range(int(120 / 0.05) + 1)]
roots = []
for a, b in zip(grid, grid[1:]):
    if mp.sign(D(a)) != mp.sign(D(b)):
        roots.append(mp.findroot(D, (a, b), solver="bisect"))
say(f"M3 crossing pair: orders {sum(G.values()) + 1}, {sum(H.values()) + 1}; distinct imbalances {len(cq)}; V = {V}; "
    f"sign changes of D on [-60, 60] at alpha=-1, beta=0: {len(roots)} at gamma = {[mp.nstr(r, 4) for r in roots]}")

# ---------------------------------------------------------------- M4 Lemma 3.1 determinants
L = mp.log
d3 = mp.det(mp.matrix([[1, 0, L(2)], [1, L(4), L(4)], [1, L(2), L(3)]]))
d4 = mp.det(mp.matrix([[1, L(2), L(3), mp.mpf(1) / 3], [1, L(3), L(4), mp.mpf(1) / 2], [1, L(4), L(4), 0], [1, L(9), L(6), 0]]))
say(f"M4 3x3 det {mp.nstr(d3, 12)} vs ln2*ln(9/8) {mp.nstr(L(2) * L(mp.mpf(9) / 8), 12)}; 4x4 det {mp.nstr(d4, 12)} vs "
    f"-(1/6)ln(3/2)ln(2^13/3^8) {mp.nstr(-L(mp.mpf(3) / 2) * L(mp.mpf(2) ** 13 / mp.mpf(3) ** 8) / 6, 12)}")
# Delta = 2 identity
say("M4 Delta=2: q = [ln(i+j)-ln2-ln(ij)/2]/(3ln3-4.5ln2) on (1,1),(1,2),(2,2): " + str(
    [mp.nstr((L(i + j) - L(2) - L(i * j) / 2) / (3 * L(3) - mp.mpf(9) / 2 * L(2)), 10) for i, j in ((1, 1), (1, 2), (2, 2))]))

# ---------------------------------------------------------------- M5 identifiability bound, Delta <= 6 and Delta = 7
def z(i, j): return [L(i * j), L(i + j), mp.mpf(j - i) / (i + j)]
def affdim(S):
    if len(S) == 1: return 0
    base = z(*S[0]); M = mp.matrix([[a - b for a, b in zip(z(*p), base)] for p in S[1:]])
    sv = mp.svd_r(M, compute_uv=False)
    return sum(1 for s in sv if s > mp.mpf(10) ** -25)
viol = {}
for D_ in (6, 7):
    P = [(i, j) for i in range(1, D_ + 1) for j in range(i, D_ + 1)]
    bad = []
    for k in range(2, 5):
        for S in itertools.combinations(P, k):
            r = len({Fraction(j - i, i + j) for i, j in S})
            if affdim(list(S)) < min(len(S) - 1, r, 3): bad.append(S)
    viol[D_] = bad
say(f"M5 subsets of at most four pairs violating A = min(|S|-1, r, 3): Delta=6: {len(viol[6])}; Delta=7: {viol[7]}")

# ---------------------------------------------------------------- M6 count ranks and octane collisions
sys.path.insert(0, os.path.dirname(os.path.dirname(HERE)))
def smiles_pairs(s):
    deg, edges, stack, prev = [], [], [], None
    for ch in s:
        if ch == "C":
            deg.append(0); cur = len(deg) - 1
            if prev is not None: edges.append((prev, cur)); deg[prev] += 1; deg[cur] += 1
            prev = cur
        elif ch == "(": stack.append(prev)
        elif ch == ")": prev = stack.pop()
    return [tuple(sorted((deg[a], deg[b]))) for a, b in edges]
from octane_data import OCTANES, NAMES
import csv, numpy as np
PAIRS = [(i, j) for i in range(1, 5) for j in range(i, 5)]
def vec(pp): c = Counter(pp); return [c[p] for p in PAIRS]
oct_v = [vec(smiles_pairs(r[0])) for r in OCTANES]
groups = defaultdict(list)
for nm, v in zip(NAMES, oct_v): groups[tuple(v)].append(nm)
say(f"M6 octanes: distinct count vectors {len(groups)}; shared: {[g for g in groups.values() if len(g) > 1]}")
bp = list(csv.DictReader(open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "external", "bp", "bp_data.csv"))))
def bpvec(r): return vec([tuple(int(t) for t in p.split("-")) for p in r["degree_pairs"].split()])
def crank(M): M = np.array(M, float); return int(np.linalg.matrix_rank(M - M.mean(0)))
say(f"M6 centred count-matrix ranks: octanes {crank(oct_v)}, decanes {crank([bpvec(r) for r in bp if r['n_C'] == '10'])}, "
    f"pooled {crank([bpvec(r) for r in bp])} (n = {len(bp)}); identity sum (1/i+1/j) m_ij = n holds for all: "
    f"{all(abs(sum((1/i + 1/j) * c for (i, j), c in zip(PAIRS, bpvec(r))) - int(r['n_C'])) < 1e-9 for r in bp)}")
y = {nm: r[1] for nm, r in zip(NAMES, OCTANES)}
sse = sum(sum((y[a] - np.mean([y[b] for b in g])) ** 2 for a in g) for g in groups.values())
say(f"M6 octane T_B within-class SSE {sse:.4f} (paper 2.925 = 117/40), RMSE {np.sqrt(sse / 18):.4f}")

# ---------------------------------------------------------------- M7 extremal trees and closed forms
ok = True
for n in range(4, 15):
    for g in (1, -1, 0.3):
        vals = [(sum(mp.e ** (g * mp.mpf(abs(T.degree(u) - T.degree(v))) / (T.degree(u) + T.degree(v))) for u, v in T.edges()), canon(T))
                for T in nx.nonisomorphic_trees(n)]
        lo, hi = min(vals)[0], max(vals)[0]
        pth, star = canon(nx.path_graph(n)), canon(nx.star_graph(n - 1))
        mins = [c for v, c in vals if abs(v - lo) < 1e-30]; maxs = [c for v, c in vals if abs(v - hi) < 1e-30]
        want_min, want_max = (pth, star) if g > 0 else (star, pth)
        ok &= mins == [want_min] and maxs == [want_max]
say(f"M7 extremal trees of LO(0,0,gamma), n = 4..14, gamma in {{1, -1, 0.3}}: path/star unique extremisers as stated: {ok}")
def LOg(Gr, a, b, g):
    return sum((mp.mpf(Gr.degree(u)) * Gr.degree(v)) ** a * mp.mpf(Gr.degree(u) + Gr.degree(v)) ** b *
               mp.e ** (g * mp.mpf(abs(Gr.degree(u) - Gr.degree(v))) / (Gr.degree(u) + Gr.degree(v))) for u, v in Gr.edges())
a, b, g = mp.mpf("0.37"), mp.mpf("-1.3"), mp.mpf("0.9"); err = 0
for n in range(5, 9):
    err = max(err, abs(LOg(nx.complete_graph(n), a, b, g) - n * (n - 1) / 2 * 2 ** b * (n - 1) ** (2 * a + b)))
    err = max(err, abs(LOg(nx.cycle_graph(n), a, b, g) - n * 4 ** (a + b)))
    err = max(err, abs(LOg(nx.path_graph(n), a, b, g) - (2 * 2 ** a * 3 ** b * mp.e ** (g / 3) + (n - 3) * 4 ** (a + b))))
    err = max(err, abs(LOg(nx.star_graph(n - 1), a, b, g) - (n - 1) * (n - 1) ** a * n ** b * mp.e ** (g * mp.mpf(n - 2) / n)))
    err = max(err, abs(LOg(nx.wheel_graph(n), a, b, g) - (n - 1) * (3 ** a * (n - 1) ** a * (n + 2) ** b * mp.e ** (g * mp.mpf(n - 4) / (n + 2)) + 9 ** a * 6 ** b)))
for k in range(1, 6):
    err = max(err, abs(LOg(nx.hypercube_graph(k), a, b, g) - k * 2 ** (k - 1) * 2 ** b * mp.mpf(k) ** (2 * a + b)))
for p in range(1, 6):
    F = nx.Graph(); [F.add_edges_from([(0, 2 * t + 1), (0, 2 * t + 2), (2 * t + 1, 2 * t + 2)]) for t in range(p)]
    err = max(err, abs(LOg(F, a, b, g) - (p * 4 ** (a + b) + 2 * p * (4 * p) ** a * (2 * p + 2) ** b * mp.e ** (g * mp.mpf(p - 1) / (p + 1)))))
for aa, bb in ((2, 3), (1, 4), (3, 3)):
    err = max(err, abs(LOg(nx.complete_bipartite_graph(aa, bb), a, b, g) - aa * bb * (aa * bb) ** a * (aa + bb) ** b * mp.e ** (g * mp.mpf(abs(aa - bb)) / (aa + bb))))
say(f"M7 closed forms (K_n, C_n, P_n, S_n, W_n, Q_k, F_p, K_ab) at (0.37, -1.3, 0.9): max abs error {mp.nstr(err, 3)}")
# Example 4.4
Dsc = lambda g: 3 * (mp.e ** (g / 2) - 1) - 4 / mp.sqrt(5) * (mp.e ** (3 * g / 5) - mp.e ** (g / 5)) + 4 / mp.sqrt(6) * (1 - mp.e ** (g / 3))
say(f"M7 Example 4.4: D(0) = {mp.nstr(Dsc(0), 3)}, D(1) = {mp.nstr(Dsc(1), 6)}, D(1e-6) = {mp.nstr(Dsc(mp.mpf('1e-6')), 4)}")
open(os.path.join(HERE, "math_independent_out.txt"), "w").write("\n".join(OUT) + "\n")
