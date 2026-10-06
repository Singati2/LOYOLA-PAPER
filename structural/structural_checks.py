#!/usr/bin/env python3
"""Scripted checks for structural and auxiliary claims of the manuscript that
are not covered by verify_loyola_v35.py or external/verify_external.py.
Run from anywhere; writes structural_checks_out.txt next to this file.

S1  tree orders 7-17 (all trees) and 7-16 (Delta<=4): distinct degree-pair
    profiles, q-histograms, and distinct values of R, GA, LO(0,0,1),
    LO(0,0,2); number of GA values merging distinct q-histograms.
S2  the order-17 GA witness (exact, sympy).
S3  gamma-crossings at (alpha,beta) = (-1,0): exhaustive over order-12 trees;
    the maximum number of crossings and the witness pair(s).
S4  Prop. identrank(ii) equality for all pair sets with Delta <= 6 (60-digit
    SVD; subsets of size <= 4 suffice) and the Delta = 7 failures.
S5  structure sensitivity of IRLA and of LO(0,0,gamma) for gamma = 0.5,1,2,3,5,10
    on the 75 decanes (published single-edge-relocation protocol).
S6  leave-one-out Q2 of fixed M(4.5,-9) and LO(0,0,1) for octane dHvap.
S7  permutation check of ridge on degree-pair counts, decane T_B (200
    permutations, rng 20261005).
"""
import csv, itertools, math, os, sys
from collections import Counter, defaultdict
from fractions import Fraction
import numpy as np
import networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT); sys.path.insert(0, os.path.join(ROOT, "external"))
OUT = []


def log(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


def val(P, a, b, g):
    return sum((i * j) ** a * (i + j) ** b * math.exp(g * abs(i - j) / (i + j)) for i, j in P)


def key(x):
    return float(f"{x:.11g}")


RES = {}


def s1():
    log("S1 tree orders: n subset N profiles qhist R GA LO(0,0,1) LO(0,0,2) GA_qmerges")
    for n in range(7, 18):
        for sub in ("all", "mol"):
            if sub == "mol" and n > 16:
                continue
            prof, qh = set(), set(); vals = {k: set() for k in ("R", "GA", "LO1", "LO2")}; ga = {}; N = 0
            for T in nx.nonisomorphic_trees(n):
                d = dict(T.degree())
                if sub == "mol" and max(d.values()) > 4:
                    continue
                N += 1
                P = [tuple(sorted((d[u], d[v]))) for u, v in T.edges()]
                prof.add(tuple(sorted(Counter(P).items())))
                q = tuple(sorted(Counter(Fraction(j - i, i + j) for i, j in P).items())); qh.add(q)
                vals["R"].add(key(val(P, -.5, 0, 0))); vals["LO1"].add(key(val(P, 0, 0, 1)))
                vals["LO2"].add(key(val(P, 0, 0, 2))); g = key(2 * val(P, .5, -1, 0)); vals["GA"].add(g)
                ga.setdefault(g, set()).add(q)
            RES[(n, sub)] = dict(prof=len(prof), qh=len(qh), R=len(vals["R"]), GA=len(vals["GA"]), LO1=len(vals["LO1"]),
                                 LO2=len(vals["LO2"]), merge=sum(1 for s_ in ga.values() if len(s_) > 1))
            log(f"  {n} {sub} {N} {len(prof)} {len(qh)} {len(vals['R'])} {len(vals['GA'])} "
                f"{len(vals['LO1'])} {len(vals['LO2'])} {sum(1 for s in ga.values() if len(s) > 1)}")


def s2():
    import sympy as sp
    A = {(1, 5): 10, (2, 2): 2, (5, 5): 2, (2, 5): 1, (1, 2): 1}
    Bp = {(4, 5): 3, (1, 4): 5, (1, 5): 6, (2, 5): 1, (1, 2): 1}
    ga = lambda P: sum(c * 2 * sp.sqrt(i * j) / (i + j) for (i, j), c in P.items())
    hq = lambda P: Counter({Fraction(abs(i - j), i + j): 0 for (i, j) in P}) and \
        {k: sum(c for (i, j), c in P.items() if Fraction(abs(i - j), i + j) == k) for k in {Fraction(abs(i - j), i + j) for (i, j) in P}}
    difference = sp.simplify(ga(A) - ga(Bp))
    assert difference == 0 and hq(A) != hq(Bp), "S2 GA collision witness failed"   # v40.11: fail closed
    log("S2 GA witness: GA(A)-GA(B) =", difference, "| q-histograms equal:", hq(A) == hq(Bp),
        "| edges", sum(A.values()), sum(Bp.values()))


def s3():
    a, b = -1.0, 0.0; trees = []
    for T in nx.nonisomorphic_trees(12):
        d = dict(T.degree()); P = [tuple(sorted((d[u], d[v]))) for u, v in T.edges()]
        c = defaultdict(float)
        for i, j in P:
            c[Fraction(j - i, i + j)] += (i * j) ** a * (i + j) ** b
        trees.append((max(d.values()), dict(c), sorted(P)))
    qs = sorted({q for t in trees for q in t[1]}); qv = np.array([float(q) for q in qs])
    A = np.array([[t[1].get(q, 0.0) for q in qs] for t in trees])
    g = np.unique(np.concatenate([np.linspace(-60, 60, 240001), np.sign(np.linspace(-1, 1, 4001)) * np.logspace(-3, 3.5, 4001)]))
    best = []; maxz = 0
    for i in range(len(trees)):
        Dc = A[i] - A[i + 1:]; nz = np.abs(Dc) > 1e-12
        for k in np.nonzero(nz.any(1))[0]:
            c = Dc[k][nz[k]]; V = int(np.sum(np.sign(c[1:]) != np.sign(c[:-1])))
            if V < 4:
                continue
            E = np.outer(g, qv[nz[k]]); E -= E.max(1, keepdims=True)
            s = np.sign((c * np.exp(E)).sum(1)); s = s[s != 0]; zc = int(np.sum(s[1:] != s[:-1]))
            j = i + 1 + k
            if zc > maxz:
                maxz, best = zc, []
            if zc == maxz:
                best.append((zc, V, trees[i][0], trees[j][0], len(set(trees[i][1]) | set(trees[j][1])), trees[i][2], trees[j][2]))
    RES["s3_best"] = best
    log(f"S3 order-12 trees at (alpha,beta)=(-1,0): max crossings {maxz}, attained by {len(best)} pair(s)")
    for o in best:
        log("   crossings", o[0], "V", o[1], "maxdeg", o[2], o[3], "distinct imbalances", o[4])
        log("   G", Counter(o[5]), "| H", Counter(o[6]))


def s3_certify():
    """Exact certificate for the S3 witness pair(s): at (alpha,beta)=(-1,0) the
    coefficients c_k of D(gamma) = sum_k c_k exp(gamma q_k) are rational, so the
    Laguerre bound V is exact arithmetic; D is then evaluated in 50-digit
    arithmetic on a 24001-point grid over [-60, 60] plus a log-spaced tail
    and its sign changes counted.  Sign changes give at least that many
    zeros, V gives at most V, so equality certifies the exact number of
    crossings (the grid only has to bracket them); the certificate also
    requires every bracket sign to be far above the working precision."""
    import mpmath as mp
    mp.mp.dps = 50
    g = np.unique(np.concatenate([np.linspace(-60, 60, 24001), np.sign(np.linspace(-1, 1, 4001)) * np.logspace(-3, 3.5, 4001)]))
    witnesses = RES.get("s3_best", [])
    if not witnesses:
        raise AssertionError("S3 certificate requires at least one crossing witness")   # v40.11: fail closed
    for o in witnesses:
        c = defaultdict(Fraction)
        for P, sgn in ((o[5], 1), (o[6], -1)):
            for i, j in P:
                c[Fraction(j - i, i + j)] += sgn * Fraction(1, i * j)
        c = {q: v for q, v in c.items() if v != 0}; qs = sorted(c); cf = [c[q] for q in qs]
        V = sum(1 for x, y in zip(cf, cf[1:]) if (x > 0) != (y > 0))
        D = lambda x: sum(mp.mpf(v.numerator) / v.denominator * mp.exp(mp.mpf(x) * q.numerator / q.denominator) for q, v in c.items())
        sg = [mp.sign(D(x)) for x in g]
        br = [(g[k], g[k + 1]) for k in range(len(g) - 1) if sg[k] * sg[k + 1] < 0]
        roots = []
        for a, b in br:
            a, b = mp.mpf(a), mp.mpf(b)
            for _ in range(120):
                m = (a + b) / 2
                if mp.sign(D(m)) == mp.sign(D(a)): a = m
                else: b = m
            roots.append(mp.nstr((a + b) / 2, 8))
        rel = min(abs(D(x)) / sum(abs(mp.mpf(v.numerator) / v.denominator * mp.exp(mp.mpf(x) * q.numerator / q.denominator)) for q, v in c.items()) for a, b in br for x in (a, b))
        log(f"S3 certificate: exponents {[str(q) for q in qs]} coefficients {[str(x) for x in cf]}")
        log(f"   Laguerre V = {V}; sign changes of D in 50-digit arithmetic = {len(br)} at gamma = {roots}; "
            f"min relative |D| at brackets {mp.nstr(rel, 3)}; zero grid signs {sum(1 for x in sg if x == 0)}")
        ok = len(br) == V and all(x != 0 for x in sg) and rel > mp.mpf(10) ** (-40)
        log(f"   => exactly {len(br)} crossings: {'CERTIFIED' if ok else 'NOT certified (lower bound only)'}")
        if not ok:
            raise AssertionError("S3 witness failed crossing certification")


def s4():
    import mpmath as mp
    mp.mp.dps = 60

    def Aff(S):
        Z = [[mp.log(i * j), mp.log(i + j), mp.mpf(abs(i - j)) / (i + j)] for i, j in S]
        M = mp.matrix([[Z[k][c] - Z[0][c] for c in range(3)] for k in range(1, len(Z))])
        return sum(1 for x in mp.svd_r(M, compute_uv=False) if abs(x) > mp.mpf(10) ** -40)
    for D in (6, 7):
        P = [(i, j) for i in range(1, D + 1) for j in range(i, D + 1)]; bad = []
        for k in range(2, 5):
            for S in itertools.combinations(P, k):
                r = len({Fraction(j - i, i + j) for i, j in S})
                if Aff(S) < min(k - 1, r, 3):
                    bad.append(S)
        log(f"S4 Delta={D}: pair sets violating A = min(|S|-1, r, 3): {len(bad)} {bad[:3]}")
        expected = [] if D == 6 else [((1, 7), (2, 6), (3, 5), (4, 4))]
        assert bad == expected, f"S4 Delta={D} rank exceptions changed: {bad}"   # v40.11: the manuscript states exactly this exception set


def s5():
    trees = [T for T in nx.nonisomorphic_trees(10) if max(d for _, d in T.degree()) <= 4]
    H = [nx.weisfeiler_lehman_graph_hash(T, iterations=10) for T in trees]; hidx = {h: i for i, h in enumerate(H)}
    nb = [set() for _ in trees]
    for gi, T in enumerate(trees):
        for e in list(T.edges()):
            T2 = T.copy(); T2.remove_edge(*e); A_, B_ = list(nx.connected_components(T2))
            for u in A_:
                for v in B_:
                    if (u, v) == e or (v, u) == e or T2.degree(u) >= 4 or T2.degree(v) >= 4:
                        continue
                    T3 = T2.copy(); T3.add_edge(u, v); j = hidx.get(nx.weisfeiler_lehman_graph_hash(T3, iterations=10))
                    if j is not None and j != gi:
                        nb[gi].add(j)

    def ssab(f):
        v = np.array([f(T) for T in trees]); ss = []; ab = []
        for i in range(75):
            d = [abs(v[j] - v[i]) / v[i] for j in nb[i]]; ss.append(np.mean(d)); ab.append(max(d))
        return np.mean(ss), np.mean(ab)
    q = lambda T: [abs(T.degree(u) - T.degree(v)) / (T.degree(u) + T.degree(v)) for u, v in T.edges()]
    s, a = ssab(lambda T: 2 * sum(q(T))); log(f"S5 IRLA SS={s:.4f} Abr={a:.4f} ratio={s/a:.4f}")
    for g in (0.5, 1, 2, 3, 5, 10):
        s, a = ssab(lambda T: sum(math.exp(g * x) for x in q(T))); log(f"   LO(0,0,{g}) SS={s:.4f} Abr={a:.4f} ratio={s/a:.4f}")


def s6():
    import baselines as B
    from octane_data import OCTANES, PROPS, alkane_pairs
    P = [alkane_pairs(r[0]) for r in OCTANES]; y = np.array([r[1 + PROPS.index("dHvap")] for r in OCTANES])
    for t in [(4.5, -9.0, 0.0), (0.0, 0.0, 1.0)]:
        x = B.descriptor_matrix(P, [t])[0]
        pr = np.array([B.fit_predict(np.delete(x, i), np.delete(y, i), x[i]) for i in range(18)])
        log(f"S6 octane dHvap LOO Q2 of fixed {t}: {B.scores(pr, y)[0]:.4f}")


def s7():
    import baselines as B
    rows = [r for r in csv.DictReader(open(os.path.join(ROOT, "external", "bp", "bp_data.csv"))) if r["n_C"] == "10"]
    P = [[tuple(map(int, e.split("-"))) for e in r["degree_pairs"].split()] for r in rows]
    y = np.array([float(r["T_B_C"]) for r in rows]); F = np.array([B.count_vector(p) for p in P], float)
    real = B.scores(B.outer_loo(B.fold_ridge, F, y)[0], y)[0]
    rng = np.random.default_rng(20261005); q = []
    for _ in range(200):
        yp = rng.permutation(y); q.append(B.scores(B.outer_loo(B.fold_ridge, F, yp)[0], yp)[0])
    log(f"S7 decane ridge Q2 {real:.4f}; permuted (200): median {np.median(q):.4f}, 95th pct {np.percentile(q, 95):.4f}, max {max(q):.4f}")


def first(sub, key, ref="prof", nmax=17):
    for n in range(7, nmax + 1):
        r = RES.get((n, sub))
        if r and r[key] < r[ref]:
            return n, r[key], r[ref]
    return None


def check_tab_firstfail():
    """Every entry of Table tab:firstfail in ../main.tex must follow from S1."""
    tex = open(os.path.join(ROOT, "main.tex")).read()
    i = tex.index(r"\label{tab:firstfail}"); blk = tex[tex.index(r"\midrule", i):tex.index(r"\bottomrule", i)]
    lo_a, lo_m = first("all", "LO1"), first("mol", "LO1", nmax=16)
    r_a, r_m = first("all", "R"), first("mol", "R", nmax=16)
    ga_a, ga_m = first("all", "GA"), first("mol", "GA", nmax=16)
    ga_merge = next(n for n in range(7, 18) if RES[(n, "all")]["merge"] > 0)
    assert all(RES[(n, "all")]["LO1"] == RES[(n, "all")]["qh"] for n in range(7, 18)), "LO1 != q-histograms"
    want = {
        "LO row": f"$LO(0,0,\\gamma)$ & ${lo_a[0]}$ (${lo_a[1]}/{lo_a[2]}$) & never$^{{a}}$ & ${lo_m[0]}$ (${lo_m[1]}/{lo_m[2]}$) & never$^{{a}}$",
        "R row": f"$R$ & ${r_a[0]}$ (${r_a[1]}/{r_a[2]}$) & n/a$^{{b}}$ & $> 16^{{c}}$ & n/a$^{{b}}$" if r_m is None else "R mol fails <=16",
        "GA row": f"$GA$ & ${ga_a[0]}$ (${ga_a[1]}/{ga_a[2]}$)$^{{d}}$ & ${ga_merge}^{{e}}$ & ${ga_m[0]}$ (${ga_m[1]}/{ga_m[2]}$)$^{{d}}$",
    }
    for k, w in want.items():
        log(f"TAB firstfail {k}: {'OK' if w in blk else 'MISMATCH, expected: ' + w}")
        if w not in blk:
            raise SystemExit(1)


if __name__ == "__main__":
    for f in (s2, s4, s6, s7, s5, s3, s3_certify, s1, check_tab_firstfail):
        f()
    open(os.path.join(HERE, "structural_checks_out.txt"), "w").write("\n".join(OUT) + "\n")
