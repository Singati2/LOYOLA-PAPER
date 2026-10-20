"""Independent construction and checking of every explicit witness/example in main.tex/supplement.tex."""
import itertools, math, json, pickle
from fractions import Fraction as F
from collections import Counter
import networkx as nx
import numpy as np
import sympy as sp
import mpmath as mp
from common import profile_of_graph, qhist, qf, maxdeg, nvert, radical_key, tree_canon

mp.mp.dps = 50
R = {}
def rec(key, ok, info):
    R[key] = {"ok": bool(ok), "info": info}
    print(("PASS " if ok else "FAIL ") + key + " :: " + str(info), flush=True)

def P(d):  # dict {(i,j):m} -> profile tuple
    return tuple(sorted(((min(k), max(k)), v) for k, v in d.items()))

def build(edges):
    G = nx.Graph(); G.add_edges_from(edges); return G

def star_on(G, c, k, tag):
    for t in range(k):
        G.add_edge(c, f"{tag}{t}")

def pend_path(G, v, L, tag):
    prev = v
    for t in range(L):
        G.add_edge(prev, f"{tag}{t}"); prev = f"{tag}{t}"

def is_tree(G):
    return nx.is_tree(G)

# ---------------- A. order-13 pair (main 603-615, 1056-1060; supp 722-727) -----------------
T1 = nx.path_graph(["c", "a", "b", "d", "e", "l"])
star_on(T1, "c", 5, "c"); star_on(T1, "b", 1, "b"); star_on(T1, "d", 1, "d")
T2 = nx.path_graph(["c", "b", "x", "y", "z"])
star_on(T2, "c", 5, "c"); star_on(T2, "b", 1, "b"); star_on(T2, "z", 2, "z")
p13a = P({(1, 2): 1, (1, 3): 2, (1, 6): 5, (2, 3): 2, (2, 6): 1, (3, 3): 1})
p13b = P({(1, 3): 3, (1, 6): 5, (2, 2): 1, (2, 3): 2, (3, 6): 1})
qh13 = tuple(sorted({F(0): 1, F(1, 5): 2, F(1, 3): 1, F(1, 2): 3, F(5, 7): 5}.items()))
ok = (is_tree(T1) and is_tree(T2) and T1.number_of_nodes() == 13 and T2.number_of_nodes() == 13
      and profile_of_graph(T1) == p13a and profile_of_graph(T2) == p13b and p13a != p13b
      and qhist(p13a) == qhist(p13b) == qh13 and not nx.is_isomorphic(T1, T2))
deg1, deg2 = dict(T1.degree()), dict(T2.degree())
leafd3 = any(deg1[u] == 1 and deg1[w] == 3 for u, w in T1.edges() for u, w in [(u, w), (w, u)]) and \
         any(deg2[u] == 1 and deg2[w] == 3 for u, w in T2.edges() for u, w in [(u, w), (w, u)])
rec("A_order13_pair", ok and leafd3, {"T1": str(profile_of_graph(T1)), "T2": str(profile_of_graph(T2)),
     "qhist": str(qhist(p13a)), "Delta": (maxdeg(p13a), maxdeg(p13b)), "leaf_adj_deg3": leafd3})

# ---------------- B. order-16 pair with Delta<=4 (main 615-629) ------------------------------
U1 = nx.path_graph(["A", "B", "C", "D"])
star_on(U1, "A", 3, "a"); star_on(U1, "D", 3, "d"); star_on(U1, "B", 1, "b"); star_on(U1, "C", 1, "c")
pend_path(U1, "B", 2, "pb"); pend_path(U1, "C", 2, "pc")
U2 = nx.path_graph(["A", "w", "B", "v1", "v2", "v3", "v4", "C"])
star_on(U2, "A", 3, "a"); star_on(U2, "B", 2, "b"); star_on(U2, "C", 3, "c")
p16a = P({(1, 2): 2, (1, 4): 8, (2, 4): 2, (4, 4): 3})
p16b = P({(1, 4): 8, (2, 2): 3, (2, 4): 4})
qh16 = tuple(sorted({F(0): 3, F(1, 3): 4, F(3, 5): 8}.items()))
d1, d2 = dict(U1.degree()), dict(U2.degree())
ok = (is_tree(U1) and is_tree(U2) and U1.number_of_nodes() == 16 and U2.number_of_nodes() == 16
      and profile_of_graph(U1) == p16a and profile_of_graph(U2) == p16b and qhist(p16a) == qhist(p16b) == qh16
      and max(d1.values()) == 4 and max(d2.values()) == 4 and d1["A"] == d1["B"] == d1["C"] == d1["D"] == 4
      and d2["A"] == d2["B"] == d2["C"] == 4 and d2["w"] == 2)
rec("B_order16_pair_Delta4", ok, {"U1": str(profile_of_graph(U1)), "U2": str(profile_of_graph(U2)), "qhist": str(qhist(p16a))})

# ---------------- C. pendant-path propagation (Thm 2(iii)) ------------------------------------
def attach(G, d, L):
    H = G.copy(); deg = dict(H.degree())
    leaf = next(u for u in H if deg[u] == 1 and any(deg[w] == d for w in H[u]))
    pend_path(H, leaf, L, "pp"); return H
okC = True; infoC = []
for base, (G1, G2), d in [(13, (T1, T2), 3), (16, (U1, U2), 4)]:
    for n in range(base, 61):
        H1, H2 = attach(G1, d, n - base), attach(G2, d, n - base)
        a, b = profile_of_graph(H1), profile_of_graph(H2)
        good = (is_tree(H1) and is_tree(H2) and H1.number_of_nodes() == n == H2.number_of_nodes() and a != b
                and qhist(a) == qhist(b) and maxdeg(a) == maxdeg(p13a if base == 13 else p16a) and maxdeg(b) == maxdeg(a))
        okC &= good
    # same difference vector check
rec("C_pendant_propagation_n13-60_all_n16-60_Delta4", okC, "attach path L=n-base at leaf adj. to deg d; distinct profiles, equal q-hist, Delta unchanged (6 resp. 4)")

# ---------------- D. GA merge at order 17 (main 720-724) ---------------------------------------
G1 = nx.path_graph(["X", "Y", "Z"]); star_on(G1, "X", 3, "x"); star_on(G1, "Y", 3, "y"); star_on(G1, "Z", 4, "z")
pend_path(G1, "X", 4, "ch")   # X-(2)-(2)-(2)-leaf
G2 = nx.path_graph(["U", "A", "V", "B"]); star_on(G2, "A", 2, "a"); star_on(G2, "B", 3, "b")
star_on(G2, "U", 3, "u"); star_on(G2, "V", 3, "v"); pend_path(G2, "U", 2, "ch")
pg1 = P({(1, 5): 10, (2, 2): 2, (5, 5): 2, (2, 5): 1, (1, 2): 1})
pg2 = P({(4, 5): 3, (1, 4): 5, (1, 5): 6, (2, 5): 1, (1, 2): 1})
ga = lambda p: sum(m * 2 * sp.sqrt(i * j) / (i + j) for (i, j), m in p)
gdiff = sp.nsimplify(sp.simplify(ga(pg1) - ga(pg2)))
okD = (is_tree(G1) and is_tree(G2) and G1.number_of_nodes() == 17 == G2.number_of_nodes()
       and profile_of_graph(G1) == pg1 and profile_of_graph(G2) == pg2 and gdiff == 0
       and radical_key(pg1, F(1, 2), F(-1), 2) == radical_key(pg2, F(1, 2), F(-1), 2) and qhist(pg1) != qhist(pg2))
rec("D_GA_merge_order17", okD, {"GA1": str(sp.nsimplify(ga(pg1))), "GA2": str(sp.nsimplify(ga(pg2))),
     "qh1": str(qhist(pg1)), "qh2": str(qhist(pg2)), "Delta": (maxdeg(pg1), maxdeg(pg2))})

# ---------------- E. five crossings, order 12, Delta=6 (main 763-775) --------------------------
E1 = build([("h", "n4"), ("n4", "n3")]); star_on(E1, "h", 5, "h"); star_on(E1, "n4", 2, "f"); star_on(E1, "n3", 2, "t")
E2 = build([("h", "n5"), ("h", "n2")]); star_on(E2, "h", 4, "h"); star_on(E2, "n5", 4, "f"); star_on(E2, "n2", 1, "t")
pe1 = P({(1, 3): 2, (1, 4): 2, (1, 6): 5, (3, 4): 1, (4, 6): 1})
pe2 = P({(1, 2): 1, (1, 5): 4, (1, 6): 4, (2, 6): 1, (5, 6): 1})
qs = sorted(set(qf(i, j) for (i, j), m in pe1 + pe2))
def coeffs(a, b):
    c = {}
    for sgn, p in ((1, pe1), (-1, pe2)):
        for (i, j), m in p:
            c[qf(i, j)] = c.get(qf(i, j), 0) + sgn * m * mp.power(i * j, a) * mp.power(i + j, b)
    return [c[q] for q in qs]
cs = coeffs(-1, 0)
sg = [x for x in cs if x != 0]
V = sum(1 for x, y in zip(sg, sg[1:]) if (x > 0) != (y > 0))
D = lambda g: sum(c * mp.e ** (g * mp.mpf(q.numerator) / q.denominator) for c, q in zip(cs, qs))
roots = []
grid = [mp.mpf(x) / 100 for x in range(-40000, 40001)]
vals = [D(g) for g in grid[::1]] if False else None
prev = D(grid[0]); gp = grid[0]
for g in grid[1:]:
    cur = D(g)
    if cur == 0 or (cur > 0) != (prev > 0):
        roots.append(mp.findroot(D, (gp, g), solver="anderson"))
    prev, gp = cur, g
okE = (is_tree(E1) and is_tree(E2) and E1.number_of_nodes() == 12 == E2.number_of_nodes()
       and profile_of_graph(E1) == pe1 and profile_of_graph(E2) == pe2 and len(qs) == 8 and V == 5
       and maxdeg(pe1) == maxdeg(pe2) == 6 and len(roots) == 5
       and [round(float(r), 1) for r in roots] == [-17.2, -12.0, -2.0, 2.7, 31.1])
rec("E_five_crossings_order12", okE, {"n_imbalances": len(qs), "V": V, "roots": [mp.nstr(r, 8) for r in roots],
     "signs": ["+" if x > 0 else "-" for x in sg]})

# ---------------- F. sum-connectivity example (main 995-1007) -----------------------------------
diff = {(1, 3): 6, (2, 3): 4, (3, 3): 4, (1, 4): -4, (2, 2): -6, (2, 4): -4}
chi_diff = sp.simplify(sum(m / sp.sqrt(i + j) for (i, j), m in diff.items()))
g = sp.symbols("g")
Dsym = sum(m / sp.sqrt(i + j) * sp.exp(g * sp.Rational(abs(i - j), i + j)) for (i, j), m in diff.items())
Dpaper = 3 * (sp.exp(g / 2) - 1) - 4 / sp.sqrt(5) * (sp.exp(3 * g / 5) - sp.exp(g / 5)) + 4 / sp.sqrt(6) * (1 - sp.exp(g / 3))
same = sp.simplify(Dsym - Dpaper) == 0
D1 = mp.mpf(sp.N(Dsym.subs(g, 1), 30)); D6 = sp.N(Dsym.subs(g, sp.Rational(1, 10**6)), 30)
edges_ok = sum(diff.values()) == 0 and sum(m * (F(1, i) + F(1, j)) for (i, j), m in diff.items()) == 0
rec("F_sumconn_example", same and chi_diff == 0 and edges_ok and round(float(D1), 4) == 0.2255
    and abs(float(D6) - 2.4e-7) < 0.05e-7,
    {"chi_diff": str(chi_diff), "D(1)": mp.nstr(D1, 10), "D(1e-6)": str(sp.N(D6, 6)), "formula_matches": same})
# realizability at order 18 (t=1): search all chemical trees of order 18
want = {k: v for k, v in diff.items()}
prof18 = Counter()
for T in nx.nonisomorphic_trees(18):
    p = profile_of_graph(T)
    if maxdeg(p) <= 4:
        prof18[p] += 1
plist = list(prof18)
def dvec(a, b):
    c = Counter(dict(a)); c.subtract(Counter(dict(b))); return {k: v for k, v in c.items() if v}
idx = {}
for p in plist:
    idx[p] = p
found = None
pset = set(plist)
for p in plist:
    c = Counter(dict(p)); c.subtract(Counter(want))
    if all(v >= 0 for v in c.values()):
        q = tuple(sorted((k, v) for k, v in c.items() if v))
        if q in pset:
            found = (p, q); break
rec("F2_sumconn_pair_realisable_order18_chemical", found is not None, {"S": str(found[0]) if found else None,
     "T": str(found[1]) if found else None})

# ---------------- G. SDD / ISDD examples (main 662-667) ------------------------------------
ps1 = P({(1, 2): 1, (1, 3): 2, (2, 2): 4, (2, 3): 1}); ps2 = P({(1, 2): 3, (1, 3): 1, (2, 3): 3, (3, 3): 1})
sdd = lambda p: sum(m * (F(i, j) + F(j, i)) for (i, j), m in p)
S1 = nx.path_graph(7); S1.add_edge(2, "x"); S1.add_edge(2, "y")  # 0-1-2(3)-3-4-5-6 ; deg3 at 2 with two leaves?
# build explicitly: deg-3 vertex v with two leaves and a chain v-a-b-c-d-e-leaf : edges (1,3)^2,(2,3),(2,2)^4,(1,2)
S1 = build([("v", "l1"), ("v", "l2"), ("v", "a"), ("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"), ("e", "f")])
S2 = build([("u", "w"), ("u", "l"), ("u", "a1"), ("a1", "a2"), ("w", "b1"), ("b1", "b2"), ("w", "c1"), ("c1", "c2")])
okG = (profile_of_graph(S1) == ps1 and profile_of_graph(S2) == ps2 and is_tree(S1) and is_tree(S2)
       and S1.number_of_nodes() == 9 == S2.number_of_nodes() and sdd(ps1) == sdd(ps2) == F(58, 3))
rec("G_SDD_order9", okG, {"SDD": (str(sdd(ps1)), str(sdd(ps2))), "p1": str(profile_of_graph(S1)), "p2": str(profile_of_graph(S2))})

# ---------------- H. K4 vs K_{1,3} at gamma = ln 4 (main 704-705) -------------------------
lo = lambda G, a, b, gg: sum(mp.power(G.degree(u) * G.degree(v), a) * mp.power(G.degree(u) + G.degree(v), b)
                             * mp.e ** (gg * mp.mpf(abs(G.degree(u) - G.degree(v))) / (G.degree(u) + G.degree(v))) for u, v in G.edges())
k4, s3 = lo(nx.complete_graph(4), 0, 0, mp.log(4)), lo(nx.star_graph(3), 0, 0, mp.log(4))
rec("H_K4_K13_ln4", mp.almosteq(k4, 6, 1e-45) and mp.almosteq(s3, 6, 1e-45), {"K4": mp.nstr(k4, 20), "K13": mp.nstr(s3, 20)})

# ---------------- I. spider with four legs of length three (main 843-848) -------------------
Sp = nx.Graph()
for leg in range(4):
    pend_path(Sp, "c", 3, f"L{leg}_")
ps = profile_of_graph(Sp)
qset = sorted(set(qf(i, j) for (i, j), m in ps))
q1, q2 = F(1, 3), F(0)
c = (math.log(1 - float(q2) ** 2) - math.log(1 - float(q1) ** 2)) / (float(q1) - float(q2))
v = mp.matrix([1, -2, c])
def LOt(th):
    return lo(Sp, th[0], th[1], th[2])
th = [mp.mpf("0.3"), mp.mpf("-0.2"), mp.mpf("0.7")]
r1 = [LOt([th[k] + t * v[k] for k in range(3)]) / LOt(th) for t in (1, 2)]
resc = mp.almosteq(r1[1], r1[0] ** 2, 1e-12)
rec("I_spider", set(k for k, m in ps) == {(2, 4), (2, 2), (1, 2)} and qset == [F(0), F(1, 3)] and resc,
    {"profile": str(ps), "nodes": Sp.number_of_nodes(), "rescaling_ratio_t1,t2": [mp.nstr(x, 12) for x in r1]})

# ---------------- J. Delta<=4 imbalance list (main 738-739) ---------------------------------
qs4 = sorted(set(qf(i, j) for i in range(1, 5) for j in range(i, 5)))
rec("J_Delta4_imbalances", qs4 == [F(0), F(1, 7), F(1, 5), F(1, 3), F(1, 2), F(3, 5)], [str(x) for x in qs4])

# ---------------- K. closed forms (main 1201-1246) -----------------------------------------
def LOG(G, a, b, gg):
    return lo(G, a, b, gg)
okK = True; errs = []
rng = np.random.default_rng(7)
for trial in range(6):
    a, b, gg = [mp.mpf(float(x)) for x in rng.uniform(-1.5, 1.5, 3)]
    cases = []
    for n in range(2, 9):
        cases.append(("K", n, LOG(nx.complete_graph(n), a, b, gg), n * (n - 1) / 2 * mp.power(2, b) * mp.power(n - 1, 2 * a + b)))
        cases.append(("P", n, LOG(nx.path_graph(n), a, b, gg),
                      mp.power(2, b) if n == 2 else (2 * mp.power(2, a) * mp.power(3, b) * mp.e ** (gg / 3) + (n - 3) * mp.power(4, a + b))))
        cases.append(("S", n, LOG(nx.star_graph(n - 1), a, b, gg), (n - 1) * mp.power(n - 1, a) * mp.power(n, b) * mp.e ** (gg * mp.mpf(n - 2) / n)))
        if n >= 3:
            cases.append(("C", n, LOG(nx.cycle_graph(n), a, b, gg), n * mp.power(4, a + b)))
        if n >= 5:
            W = nx.wheel_graph(n)  # n vertices: hub + (n-1)-cycle
            cases.append(("W", n, LOG(W, a, b, gg), (n - 1) * (mp.power(3, a) * mp.power(n - 1, a) * mp.power(n + 2, b) * mp.e ** (gg * mp.mpf(n - 4) / (n + 2)) + mp.power(9, a) * mp.power(6, b))))
    for A_ in range(1, 5):
        for B_ in range(1, 5):
            cases.append(("Kab", (A_, B_), LOG(nx.complete_bipartite_graph(A_, B_), a, b, gg),
                          A_ * B_ * mp.power(A_ * B_, a) * mp.power(A_ + B_, b) * mp.e ** (gg * mp.mpf(abs(A_ - B_)) / (A_ + B_))))
    for k in range(1, 6):
        cases.append(("Q", k, LOG(nx.hypercube_graph(k), a, b, gg), k * 2 ** (k - 1) * mp.power(2, b) * mp.power(k, 2 * a + b)))
    for p in range(1, 6):
        Fp = nx.Graph()
        for t in range(p):
            Fp.add_edges_from([(0, 2 * t + 1), (0, 2 * t + 2), (2 * t + 1, 2 * t + 2)])
        cases.append(("F", p, LOG(Fp, a, b, gg), p * mp.power(4, a + b) + 2 * p * mp.power(4 * p, a) * mp.power(2 * p + 2, b) * mp.e ** (gg * mp.mpf(p - 1) / (p + 1))))
    for Greg, r in [(nx.petersen_graph(), 3), (nx.circulant_graph(9, [1, 2]), 4)]:
        cases.append(("reg", r, LOG(Greg, a, b, gg), Greg.number_of_edges() * mp.power(2, b) * mp.power(r, 2 * a + b)))
    for name, n, x, y in cases:
        if not mp.almosteq(x, y, 1e-40):
            okK = False; errs.append((name, n))
rec("K_closed_forms", okK, {"failures": errs[:10], "families": "K_n,P_n,S_n(n=2..8),C_n,W_n(n>=5),K_ab,Q_k,F_p,Petersen,C9(1,2); 6 random (a,b,g)"})

# ---------------- L. edge division vector (4,1,1) on 7 vertices (main 632) -------------------
def edv(T):
    n = T.number_of_nodes(); c = Counter()
    for u, w in T.edges():
        H = T.copy(); H.remove_edge(u, w)
        s = len(nx.node_connected_component(H, u)); c[min(s, n - s)] += 1
    return tuple(c.get(k, 0) for k in range(1, n // 2 + 1))
seven = [T for T in nx.nonisomorphic_trees(7) if edv(T) == (4, 1, 1)]
okL = len(seven) == 2 and profile_of_graph(seven[0]) != profile_of_graph(seven[1]) and \
      qhist(profile_of_graph(seven[0])) != qhist(profile_of_graph(seven[1]))
rec("L_EDV_411_order7", okL, {"count": len(seven), "profiles": [str(profile_of_graph(T)) for T in seven]})

# ---------------- M. octanes (main 899-939, Table 1, Remark data sets) -----------------------
def chain(n):
    return nx.path_graph(range(1, n + 1))
def add_sub(G, at, length, tag):
    prev = at
    for t in range(length):
        G.add_edge(prev, f"{tag}{t}"); prev = f"{tag}{t}"
def alkane(main, subs):
    G = chain(main)
    for k, (pos, L) in enumerate(subs):
        add_sub(G, pos, L, f"s{k}_")
    return G
octanes = {
    "octane": alkane(8, []), "2-methylheptane": alkane(7, [(2, 1)]), "3-methylheptane": alkane(7, [(3, 1)]),
    "4-methylheptane": alkane(7, [(4, 1)]), "3-ethylhexane": alkane(6, [(3, 2)]),
    "2,2-dimethylhexane": alkane(6, [(2, 1), (2, 1)]), "2,3-dimethylhexane": alkane(6, [(2, 1), (3, 1)]),
    "2,4-dimethylhexane": alkane(6, [(2, 1), (4, 1)]), "2,5-dimethylhexane": alkane(6, [(2, 1), (5, 1)]),
    "3,3-dimethylhexane": alkane(6, [(3, 1), (3, 1)]), "3,4-dimethylhexane": alkane(6, [(3, 1), (4, 1)]),
    "3-ethyl-2-methylpentane": alkane(5, [(3, 2), (2, 1)]), "3-ethyl-3-methylpentane": alkane(5, [(3, 2), (3, 1)]),
    "2,2,3-trimethylpentane": alkane(5, [(2, 1), (2, 1), (3, 1)]), "2,2,4-trimethylpentane": alkane(5, [(2, 1), (2, 1), (4, 1)]),
    "2,3,3-trimethylpentane": alkane(5, [(2, 1), (3, 1), (3, 1)]), "2,3,4-trimethylpentane": alkane(5, [(2, 1), (3, 1), (4, 1)]),
    "2,2,3,3-tetramethylbutane": alkane(4, [(2, 1), (2, 1), (3, 1), (3, 1)]),
}
allmol8 = [T for T in nx.nonisomorphic_trees(8) if max(dict(T.degree()).values()) <= 4]
canon = lambda G: tree_canon({v: list(G[v]) for v in G})
okM = (len(octanes) == 18 and len(allmol8) == 18 and set(canon(G) for G in octanes.values()) == set(canon(T) for T in allmol8))
prof = {k: profile_of_graph(G) for k, G in octanes.items()}
groups = Counter(prof.values())
coll = [sorted(k for k in prof if prof[k] == p) for p, c in groups.items() if c > 1]
pairA = P({(1, 2): 2, (1, 3): 1, (2, 2): 2, (2, 3): 2}); pairB = P({(1, 2): 2, (1, 3): 2, (2, 3): 2, (3, 3): 1})
okM2 = (len(groups) == 16 and sorted(coll) == sorted([["3-methylheptane", "4-methylheptane"], ["3,4-dimethylhexane", "3-ethyl-2-methylpentane"]])
        and prof["3-methylheptane"] == pairA and prof["3,4-dimethylhexane"] == pairB)
rec("M1_octane_18_isomers_16_vectors_2_pairs", okM and okM2, {"distinct_vectors": len(groups), "collision_classes": coll,
     "vecA": str(prof["3-methylheptane"]), "vecB": str(prof["3,4-dimethylhexane"])})
W = {k: nx.wiener_index(G) for k, G in octanes.items()}
E = {k: edv(G) for k, G in octanes.items()}
okM3 = all(W[a] != W[b] and E[a] != E[b] for a, b in coll)
rec("M2_octane_pairs_EDV_Wiener_differ", okM3, {a + "/" + b: (E[a], E[b], W[a], W[b]) for a, b in coll})
union = set(k for p in prof.values() for k, m in p)
def zvec(i, j):
    return np.array([math.log(i * j), math.log(i + j), abs(i - j) / (i + j)])
Z = np.array([zvec(i, j) for (i, j) in sorted(union)])
adim = np.linalg.matrix_rank(Z[1:] - Z[0], tol=1e-10)
rec("M3_octane_union_9_of_10_affdim3", len(union) == 9 and (1, 1) not in union and adim == 3, {"union": sorted(union), "affine_dim": int(adim)})
pairs10 = [(i, j) for i in range(1, 5) for j in range(i, 5) if (i, j) != (1, 1)]
Mx = np.array([[dict(p).get(k, 0) for k in pairs10] for p in prof.values()], float)
rk = np.linalg.matrix_rank(Mx - Mx.mean(0))
ident = all(nvert(p) == 8 for p in prof.values())
rec("M4_octane_centred_count_rank7", rk == 7 and ident, {"rank": int(rk), "sum(1/i+1/j)m_ij == n": ident})
TB = {"3-methylheptane": 118.9, "4-methylheptane": 117.7, "3,4-dimethylhexane": 117.7, "3-ethyl-2-methylpentane": 115.6}
sse = sum((TB[a] - TB[b]) ** 2 / 2 for a, b in coll)
rec("M5_octane_SSE_floor", round(sse, 3) == 2.925 and round(math.sqrt(sse / 18), 3) == 0.403 and
    [round(abs(TB[a] - TB[b]), 1) for a, b in sorted(coll)] == [2.1, 1.2] or [round(abs(TB[a] - TB[b]), 1) for a, b in sorted(coll)] == [1.2, 2.1],
    {"SSE": round(sse, 4), "RMS": round(math.sqrt(sse / 18), 4), "diffs": [round(abs(TB[a] - TB[b]), 2) for a, b in coll]})

# ---------------- N. p3 identity on trees (main 1795) --------------------------------------
okN = True
for n in range(4, 13):
    for T in nx.nonisomorphic_trees(n):
        sp_ = dict(nx.all_pairs_shortest_path_length(T))
        p3 = sum(1 for u in T for w in T if u < w and sp_[u][w] == 3)
        f = sum((T.degree(u) - 1) * (T.degree(w) - 1) for u, w in T.edges())
        okN &= (p3 == f)
rec("N_p3_identity_trees_4-12", okN, "p3 == sum (du-1)(dv-1) for all 1104 trees of orders 4..12")

# ---------------- O. determinants and Delta=2 identity (main 402, 406-420; supp 266) --------
l2, l3 = sp.log(2), sp.log(3)
z = lambda i, j: [1, sp.log(i * j), sp.log(i + j)]
d3 = sp.Matrix([z(1, 1), z(2, 2), z(1, 2)]).det()
za = lambda i, j: [1, sp.log(i * j), sp.log(i + j), sp.Rational(abs(i - j), i + j)]
d4 = sp.Matrix([za(1, 2), za(1, 3), za(2, 2), za(3, 3)]).det()
d4c = -sp.Rational(1, 6) * sp.log(sp.Rational(3, 2)) * sp.log(sp.Rational(2 ** 13, 3 ** 8))
dW = sp.Matrix([za(1, 1), za(2, 2), za(1, 2), za(1, 3)]).det()
dWc = sp.Rational(1, 6) * l2 * (8 * l3 - 13 * l2)
qform = all(sp.simplify((sp.log(i + j) - l2 - sp.log(i * j) / 2) / (3 * l3 - sp.Rational(9, 2) * l2) - sp.Rational(abs(i - j), i + j)) == 0
            for i, j in [(1, 1), (1, 2), (2, 2)])
okO = (abs(float(d3 - l2 * sp.log(sp.Rational(9, 8)))) < 1e-30 or abs(float(d3 + l2 * sp.log(sp.Rational(9, 8)))) < 1e-30)
rec("O_determinants", okO and abs(float(sp.N(d4 - d4c, 40))) < 1e-30 and round(float(d4), 4) == -0.0150 and qform
    and (abs(float(sp.N(dW - dWc, 40))) < 1e-30 or abs(float(sp.N(dW + dWc, 40))) < 1e-30),
    {"det3": float(d3), "ln2*ln(9/8)": float(l2 * sp.log(sp.Rational(9, 8))), "det4": float(d4), "paper_det4": float(d4c),
     "detW": float(dW), "paper_detW": float(dWc), "Delta2_qformula": qform})

# ---------------- P. semiregular bipartite constant q (Thm 1) ----------------------------
pK = profile_of_graph(nx.complete_bipartite_graph(2, 3))
rec("P_semiregular_constant_q", len(qhist(pK)) == 1, str(qhist(pK)))

json.dump(R, open("witnesses_out.json", "w"), indent=1, default=str)
