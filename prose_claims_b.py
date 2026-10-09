#!/usr/bin/env python3
"""Machine-checkable registry of every number stated in the running prose of
main.tex (Sections 1-5, Reproducibility paragraph, Appendix A prose, plus the
two collision-pair property differences of Section 6.1) and supplement.tex
(Sections S5-S7) of the LOYOLA paper.

Every "expected" value is computed from the committed canonical outputs
(structural/*_out.txt, the CSV tables, formal/, octane_data.py) or by a short
recomputation (tree enumeration with networkx).  No expected value is read
from the tex.

Entry format:
  {"id": str, "file": "main" | "supp",
   "pattern": regex with exactly one named group (?P<v>...) matching once,
   "expected": None | number | str (a Python expression evaluated in this
               module's namespace; a str result is matched exactly, a number
               within "tol"),
   "tol": absolute tolerance,
   "note": source}

Usage:  python3 prose_claims_b.py (or prose_numbers_check.py, which runs every registry)
"""
import os, re, csv, math, sys, warnings
warnings.simplefilter('ignore')
from fractions import Fraction
import numpy as np
import networkx as nx

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

_CACHE = {}


def _cached(key, fn):
    if key not in _CACHE:
        _CACHE[key] = fn()
    return _CACHE[key]


def _read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


def _csv(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
         8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
         14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen"}


def word(n):
    return WORDS[int(n)]


def pct(k, N):
    """Degeneracy percentage 100(1 - k/N) rounded to one decimal."""
    return round(100.0 * (1.0 - k / N), 1)


# ---------------------------------------------------------------- structural_checks_out.txt
def _sc():
    return _cached("sc", lambda: _read("structural/structural_checks_out.txt"))


def s1(n, sub):
    """Row of the S1 table: N, prof, qh, R, GA, LO1, LO2, merge."""
    def build():
        d = {}
        for line in _sc().splitlines():
            t = line.split()
            if len(t) == 10 and t[0].isdigit() and t[1] in ("all", "mol"):
                d[(int(t[0]), t[1])] = dict(zip(["N", "prof", "qh", "R", "GA", "LO1", "LO2", "merge"], map(int, t[2:])))
        return d
    return _cached("s1", build)[(n, sub)]


def s1_orders(sub):
    return sorted(n for (n, s) in _cached("s1", lambda: (s1(7, "all"), _CACHE["s1"])[1]) if s == sub)


def s1_first_below(sub, key, ref="prof"):
    """First order at which column `key` is below column `ref` (the floor)."""
    for n in s1_orders(sub):
        r = s1(n, sub)
        if r[key] < r[ref]:
            return n
    return None


def s1_last_eq(sub, key="qh", ref="prof"):
    """Last order at which `key` equals `ref` before the first failure."""
    return s1_first_below(sub, key, ref) - 1


def s1_first_merge():
    for n in s1_orders("all"):
        if s1(n, "all")["merge"] > 0:
            return n
    return None


def s3():
    """S3 crossing witness and certificate."""
    def build():
        t = _sc()
        m = re.search(r"S3 order-(\d+) trees at \(alpha,beta\)=\((-?\d+),(-?\d+)\): max crossings (\d+), attained by (\d+) pair", t)
        o = dict(order=int(m[1]), alpha=int(m[2]), beta=int(m[3]), max_cross=int(m[4]), npairs=int(m[5]))
        m = re.search(r"crossings (\d+) V (\d+) maxdeg (\d+) (\d+) distinct imbalances (\d+)", t)
        o.update(cross=int(m[1]), V=int(m[2]), maxdeg=max(int(m[3]), int(m[4])), nimb=int(m[5]))
        m = re.search(r"Laguerre V = (\d+); sign changes of D in (\d+)-digit arithmetic = (\d+) at gamma = \[([^\]]*)\]", t)
        o.update(V_cert=int(m[1]), dps=int(m[2]), nsign=int(m[3]), roots=[float(x.strip("' ")) for x in m[4].split(",")])
        m = re.search(r"=> exactly (\d+) crossings: (\w+)", t)
        o.update(exact=int(m[1]), status=m[2])
        return o
    return _cached("s3", build)


def s4(D):
    """(number of violating pair sets, text of the violating sets) at Delta = D."""
    m = re.search(r"S4 Delta=%d: pair sets violating A = min\(\|S\|-1, r, 3\): (\d+) \[(.*)\]" % D, _sc())
    return int(m[1]), m[2]


def s4_max_ok():
    Ds = [int(x) for x in re.findall(r"S4 Delta=(\d+):", _sc())]
    return max(D for D in Ds if s4(D)[0] == 0)


def s4_first_fail():
    Ds = [int(x) for x in re.findall(r"S4 Delta=(\d+):", _sc())]
    return min(D for D in Ds if s4(D)[0] > 0)


def s4_fail_set():
    """The single violating set at Delta = 7 as a tuple of pairs."""
    n, txt = s4(s4_first_fail())
    assert n == 1
    pairs = re.findall(r"\((\d+), (\d+)\)", txt)
    return tuple((int(i), int(j)) for i, j in pairs)


def s4_fail_set_str():
    return ",".join("(%d,%d)" % p for p in s4_fail_set())


def s5(name):
    """(SS, Abr, ratio) for 'IRLA' or 'LO(0,0,g)'."""
    pat = re.escape(name) + r" SS=([\d.]+) Abr=([\d.]+) ratio=([\d.]+)"
    m = re.search(pat, _sc())
    return float(m[1]), float(m[2]), float(m[3])


def s5_gammas():
    return [float(g) for g in re.findall(r"LO\(0,0,([\d.]+)\) SS=", _sc())]


def s5_ratio_peak():
    return max(s5_gammas(), key=lambda g: s5("LO(0,0,%g)" % g)[2])


def sc_src():
    return _cached("sc_src", lambda: _read("structural/structural_checks.py"))


def sc_sigdigits():
    return int(re.search(r'f"\{x:\.(\d+)g\}"', sc_src())[1])


def sc_grid():
    body = sc_src()[sc_src().index("def s3_certify"):sc_src().index("def s4")]
    m = re.search(r"np\.linspace\((-?\d+), (-?\d+),", body)
    return int(m[1]), int(m[2])


def sc_s4_dps():
    body = sc_src()[sc_src().index("def s4"):sc_src().index("def s5")]
    return int(re.search(r"mp\.mp\.dps = (\d+)", body)[1])


def sc_s4_maxk():
    body = sc_src()[sc_src().index("def s4"):sc_src().index("def s5")]
    return int(re.search(r"range\(2, (\d+)\)", body)[1]) - 1


# ---------------------------------------------------------------- hp_counts / chi_floor / fractional
def hp_digits():
    return int(re.search(r"all counts reproduced at (\d+) significant digits", _read("structural/hp_counts_out.txt"))[1])


def chi_floor(n):
    m = re.search(r"n=%d profiles=(\d+) chi_distinct=(\d+)" % n, _read("structural/chi_floor_out.txt"))
    return int(m[1]), int(m[2])


def chi_first_below():
    for n in range(7, 13):
        p, c = chi_floor(n)
        if c < p:
            return n


def _frac():
    def build():
        t = _read("structural/fractional_points_out.txt")
        counts, profiles, pred = {}, {}, {}
        for line in t.splitlines():
            m = re.match(r"\s+n=(\d+) profiles=(\d+)", line)
            if m:
                n = int(m[1]); profiles[n] = int(m[2])
                for a, b, g, c in re.findall(r"\(([-\d.]+),([-\d.]+),(\d)\):(\d+)", line):
                    counts[(n, round(float(a), 3), round(float(b), 3), int(g))] = int(c)
            m = re.match(r"\s+([^:]+): \(", line)
            if m and "->" in line:
                name = m[1]
                for a, b, q0, q1 in re.findall(r"\(([-\d.]+),([-\d.]+)\):([-\d.]+)->([-\d.]+)", line):
                    pred[(name, round(float(a), 3), round(float(b), 3), 0)] = float(q0)
                    pred[(name, round(float(a), 3), round(float(b), 3), 1)] = float(q1)
        m = re.search(r"gamma=1 better than gamma=0 at the same fractional \(alpha,beta\): (\d+) of (\d+) cases", t)
        return dict(counts=counts, profiles=profiles, pred=pred, wins=(int(m[1]), int(m[2])))
    return _cached("frac", build)


def frac_count(n, a, b, g):
    return _frac()["counts"][(n, round(a, 3), round(b, 3), g)]


def frac_profiles(n):
    return _frac()["profiles"][n]


def frac_orders():
    return sorted(_frac()["profiles"])


def frac_npoints():
    return len({(a, b) for (n, a, b, g) in _frac()["counts"]})


def frac_wins():
    return _frac()["wins"]


def frac_pred_max(dataset):
    return max(v for (nm, a, b, g), v in _frac()["pred"].items() if nm == dataset)


def frac_ratio_plane_count(n):
    vals = {frac_count(n, a, b, g) for (a, b) in ((0.5, -1), (-0.5, 1)) for g in (0, 1)}
    assert len(vals) == 1
    return vals.pop()


# ---------------------------------------------------------------- multi_order_degeneracy.csv
def mod(n, gset):
    for r in _cached("mod", lambda: _csv("multi_order_degeneracy.csv")):
        if int(r["n"]) == n and r["graph_set"] == gset:
            return {k: int(v) for k, v in r.items() if k != "graph_set"}
    raise KeyError((n, gset))


def mod_orders():
    return sorted({int(r["n"]) for r in _cached("mod", lambda: _csv("multi_order_degeneracy.csv"))})


def mod_order_with_N(N):
    ns = {int(r["n"]) for r in _cached("mod", lambda: _csv("multi_order_degeneracy.csv")) if int(r["N_trees"]) == N}
    assert len(ns) == 1
    return ns.pop()


# ---------------------------------------------------------------- structure sensitivity CSVs
def fgd(index):
    for r in _cached("fgd", lambda: _csv("fgd_structure_sensitivity_decanes.csv")):
        if r["index"] == index:
            return float(r["SS_fgd"]), float(r["Abr_fgd"]), float(r["ratio"])
    raise KeyError(index)


def fgd_nindices():
    return len(_cached("fgd", lambda: _csv("fgd_structure_sensitivity_decanes.csv")))


def control():
    return _cached("ctl", lambda: _csv("fgd_published_control.csv"))


def control_count(kind=None):
    if kind is None:
        return len(control())
    return sum(1 for r in control() if r["agreement"] == kind)


def control_nindices():
    return len({r["index"] for r in control()})


# ---------------------------------------------------------------- octane data
def _oct():
    import octane_data as od
    return od


def oct_names():
    return list(_oct().NAMES)


def oct_prop(name, prop):
    od = _oct()
    return od.OCTANES[od.NAMES.index(name)][1 + od.PROPS.index(prop)]


def oct_pairs(i):
    od = _oct()
    return [tuple(sorted(p)) for p in od.alkane_pairs(od.OCTANES[i][0])]


def _profile(P):
    d = {}
    for p in P:
        d[p] = d.get(p, 0) + 1
    return tuple(sorted(d.items()))


def oct_n():
    return len(_oct().OCTANES)


def oct_nprofiles():
    return len({_profile(oct_pairs(i)) for i in range(oct_n())})


def oct_collisions():
    """List of name-pairs sharing a degree-pair profile, in dataset order."""
    groups = {}
    for i in range(oct_n()):
        groups.setdefault(_profile(oct_pairs(i)), []).append(oct_names()[i])
    return [g for g in groups.values() if len(g) > 1]


def oct_collision_str(k):
    return ", ".join(oct_collisions()[k])


def oct_collision_diff(k, prop):
    a, b = oct_collisions()[k]
    return abs(oct_prop(a, prop) - oct_prop(b, prop))


def oct_union_pairs():
    return sorted({p for i in range(oct_n()) for p in oct_pairs(i)})


def _z(i, j):
    return np.array([math.log(i * j), math.log(i + j), abs(i - j) / (i + j)])


def affine_dim(pairs):
    Z = np.array([_z(i, j) for i, j in pairs])
    return int(np.linalg.matrix_rank(Z[1:] - Z[0], tol=1e-9)) if len(Z) > 1 else 0


def oct_affine_dim():
    return affine_dim(oct_union_pairs())


def n_admissible(D):
    return D * (D + 1) // 2


INDICES = {"M1": (0, 1, 0), "M2": (1, 0, 0), "HM": (0, 2, 0), "mM2": (-1, 0, 0), "R": (-0.5, 0, 0),
           "chi": (0, -0.5, 0), "H/2": (0, -1, 0), "ISI": (1, -1, 0), "GA": (0.5, -1, 0), "AG": (-0.5, 1, 0),
           "LO(0,0,1)": (0, 0, 1), "LO(0,0,2)": (0, 0, 2)}


def oct_descriptor(name):
    od = _oct()
    a, b, g = INDICES[name]
    return np.array([od.lo_pairs(oct_pairs(i), a, b, g) for i in range(oct_n())])


def oct_S_change_maxdr(molecule, old_value):
    """Max |Delta r| over the 12 descriptors when `molecule`'s S is replaced by old_value."""
    od = _oct()
    S = np.array([r[1 + od.PROPS.index("S")] for r in od.OCTANES], float)
    S_alt = S.copy(); S_alt[od.NAMES.index(molecule)] = old_value
    return max(abs(np.corrcoef(oct_descriptor(k), S)[0, 1] - np.corrcoef(oct_descriptor(k), S_alt)[0, 1]) for k in INDICES)


def oct_S_margin(a="HM", b="M1"):
    od = _oct()
    S = np.array([r[1 + od.PROPS.index("S")] for r in od.OCTANES], float)
    return abs(abs(np.corrcoef(oct_descriptor(a), S)[0, 1]) - abs(np.corrcoef(oct_descriptor(b), S)[0, 1]))


def old_S_233():
    """Previous (duplicated) S value of 2,3,3-trimethylpentane, from the provenance record."""
    r = prov("2,3,3-trimethylpentane", "S")
    return float(re.search(r"was ([\d.]+)", r["paper_value"])[1])


# ---------------------------------------------------------------- sensitivity CSVs (Appendix A)
def sens_maxdr(rel):
    rows = _csv(rel)
    col_o = [c for c in rows[0] if c.startswith("r_") and c.endswith("_original")][0]
    col_a = col_o.replace("_original", "_alternative")
    return max(abs(abs(float(r[col_a])) - abs(float(r[col_o]))) for r in rows)


def sens_alt(rel, index):
    rows = _csv(rel)
    col_a = [c for c in rows[0] if c.startswith("r_") and c.endswith("_alternative")][0]
    return abs(float(next(r for r in rows if r["index"] == index)[col_a]))


def sens_nchanged(rel):
    return sum(1 for r in _csv(rel) if r["displayed_changes"] == "True")


def sens_overall_max():
    return max(sens_maxdr(f) for f in ("entropy_source_sensitivity_v36.csv", "entropy_api44_sensitivity_v41.csv",
                                        "omega_source_sensitivity_v35.csv"))


def prov(molecule, prop):
    for r in _cached("prov", lambda: _csv("octane_property_provenance_v35.csv")):
        if r["molecule"] == molecule and r["property"] == prop:
            return r
    raise KeyError((molecule, prop))


def prov_S_cannot_verify():
    return sum(1 for r in _cached("prov", lambda: _csv("octane_property_provenance_v35.csv"))
               if r["property"] == "S" and r["classification"] == "CANNOT VERIFY")


def prov_api44_diffs():
    out = []
    for r in _cached("prov", lambda: _csv("octane_property_provenance_v35.csv")):
        if r["property"] == "S" and r["classification"] == "CANNOT VERIFY":
            m = re.search(r"differing from the value used by ([+-][\d.]+)", r["note"])
            out.append(abs(float(m[1])))
    return out


def prov_octane_S_nist():
    return float(re.search(r"([\d.]+) cal", prov("octane", "S")["converted_value"])[1])


def prov_ediz_233():
    return float(re.search(r"([\d.]+) \(Ediz", prov("2,3,3-trimethylpentane", "S")["source_value"])[1])


def prov_tmb_dvap_kcal():
    kj = float(re.search(r"dvapH ([\d.]+) kJ/mol", prov("2,2,3,3-tetramethylbutane", "dHvap")["source_value"])[1])
    return kj / 4.184


def prov_omega_diffs():
    out = []
    for mol in ("2,2,4-trimethylpentane", "2,2,3,3-tetramethylbutane"):
        out.append(float(re.search(r"[Dd]iff ([\d.]+)", prov(mol, "omega")["note"])[1]))
    return out


def tmb_lo_better(budget):
    r = next(r for r in _csv("dhvap_tmb_exclusion_summary_v36.csv") if int(r["budget"]) == budget)
    return int(r["LO_better"])


def tmb_budgets():
    return sorted(int(r["budget"]) for r in _csv("dhvap_tmb_exclusion_summary_v36.csv"))


def tmb_nseeds():
    v = {int(r["n_seeds"]) for r in _csv("dhvap_tmb_exclusion_summary_v36.csv")}
    assert len(v) == 1
    return v.pop()


def expanded_lo_better(prop):
    v = {int(r["LO_better"]) for r in _csv("expanded_robustness_summary_v35.csv") if r["property"] == prop}
    assert len(v) == 1, v
    return v.pop()


# ---------------------------------------------------------------- external datasets
def nonane_count(col="T_B_C"):
    return sum(1 for r in _csv("external/nonane_data.csv") if r[col].strip())


def bp_count(nC=None):
    rows = _csv("external/bp/bp_data.csv")
    return len(rows) if nC is None else sum(1 for r in rows if int(r["n_C"]) == nC)


# ---------------------------------------------------------------- Lean
def lean_profile(name):
    t = _read("formal/LoyolaFormal/Profiles.lean")
    m = re.search(r"def %s : Multiset \(ℕ × ℕ\) :=\s*\(\[(.*?)\]" % name, t, re.S)
    pairs = [(int(i), int(j)) for i, j in re.findall(r"\((\d+),(\d+)\)", m[1])]
    return _profile(pairs)


def lean_par_len(name):
    t = _read("formal/LoyolaFormal/Profiles.lean")
    m = re.search(r"def %s : List ℕ := \[([^\]]*)\]" % name, t)
    return len(m[1].split(","))


def lean_order():
    n = {len(dict(lean_profile("P1")).items()) and sum(dict(lean_profile("P1")).values()) + 1,
         sum(dict(lean_profile("P2")).values()) + 1, lean_par_len("par1") + 1, lean_par_len("par2") + 1}
    assert len(n) == 1
    return n.pop()


def lean_version():
    return _read("formal/lean-toolchain").strip().split(":")[-1].lstrip("v")


def mathlib_version():
    t = _read("formal/lake-manifest.json")
    m = re.search(r'"name": "mathlib".*?"inputRev": "v?([^"]+)"', t, re.S)
    return m[1]


# ---------------------------------------------------------------- tree enumeration (short recomputations)
def trees(n, mol=False):
    """Profiles (sorted ((i,j),count) tuples) of all non-isomorphic trees of order n."""
    def build():
        out = []
        for T in nx.nonisomorphic_trees(n):
            d = dict(T.degree())
            if mol and max(d.values()) > 4:
                continue
            out.append(_profile([tuple(sorted((d[u], d[v]))) for u, v in T.edges()]))
        return out
    return _cached(("trees", n, mol), build)


def qhist(profile):
    d = {}
    for (i, j), c in profile:
        q = Fraction(abs(i - j), i + j)
        d[q] = d.get(q, 0) + c
    return tuple(sorted(d.items()))


def collide_classes(n, mol=False):
    """q-histogram classes containing more than one distinct profile."""
    cls = {}
    for P in set(trees(n, mol)):
        cls.setdefault(qhist(P), set()).add(P)
    return [sorted(v) for v in cls.values() if len(v) > 1]


def order13_pair():
    """The Lean pair (P1, P2), verified to be a colliding class among order-13 trees."""
    P1, P2 = lean_profile("P1"), lean_profile("P2")
    n = sum(c for _, c in P1) + 1
    assert any(set(c) == {P1, P2} for c in collide_classes(n)), "Lean pair is not a collision class"
    return dict(P1), dict(P2)


def order13_qhist(q):
    return dict(qhist(lean_profile("P1")))[Fraction(q)]


def mol16_pair():
    """The unique colliding profile pair among trees with Delta <= 4 at the first failing order."""
    n = s1_first_below("mol", "qh")
    cls = collide_classes(n, mol=True)
    assert len(cls) == 1 and len(cls[0]) == 2, cls
    A, B = cls[0]
    if (4, 4) not in dict(A):
        A, B = B, A
    return dict(A), dict(B)


def common_leaf_degree(A, B):
    return min(d for (i, d) in A if i == 1 and (1, d) in B and d >= 2)


def _key(x, digits=None):
    return float(("%%.%dg" % (digits or sc_sigdigits())) % x)


def _val(profile, a, b, g):
    return sum(c * (i * j) ** a * (i + j) ** b * math.exp(g * abs(i - j) / (i + j)) for (i, j), c in profile)


def ga17_pair():
    """Profiles of the GA merge of distinct q-histograms at the first merging order."""
    n = s1_first_merge()
    groups = {}
    for P in set(trees(n)):
        groups.setdefault(_key(2 * _val(P, 0.5, -1, 0)), set()).add(P)
    merged = [v for v in groups.values() if len({qhist(P) for P in v}) > 1]
    assert len(merged) == 1 and len(merged[0]) == 2, merged
    A, B = sorted(merged[0])
    if (5, 5) not in dict(A):
        A, B = B, A
    return dict(A), dict(B)


def ga17_maxdeg():
    A, B = ga17_pair()
    return max(j for P in (A, B) for (i, j) in P)


def distinct_count(n, a, b, g, mol=False):
    return len({_key(_val(P, a, b, g)) for P in trees(n, mol)})


def shared_count(n, a, b, g):
    """Number of trees of order n whose index value is shared with another tree."""
    vals = [_key(_val(P, a, b, g)) for P in trees(n)]
    cnt = {}
    for v in vals:
        cnt[v] = cnt.get(v, 0) + 1
    return sum(1 for v in vals if cnt[v] > 1)


def decane_nb_sizes():
    """(min, max) size of the single-edge-relocation similar-structure sets on the 75 decanes."""
    def build():
        T10 = [T for T in nx.nonisomorphic_trees(10) if max(d for _, d in T.degree()) <= 4]
        H = [nx.weisfeiler_lehman_graph_hash(T, iterations=10) for T in T10]
        hidx = {h: i for i, h in enumerate(H)}
        sizes = []
        for gi, T in enumerate(T10):
            nb = set()
            for e in list(T.edges()):
                T2 = T.copy(); T2.remove_edge(*e); A_, B_ = list(nx.connected_components(T2))
                for u in A_:
                    for v in B_:
                        if (u, v) == e or (v, u) == e or T2.degree(u) >= 4 or T2.degree(v) >= 4:
                            continue
                        T3 = T2.copy(); T3.add_edge(u, v)
                        j = hidx.get(nx.weisfeiler_lehman_graph_hash(T3, iterations=10))
                        if j is not None and j != gi:
                            nb.add(j)
            sizes.append(len(nb))
        return min(sizes), max(sizes)
    return _cached("decane_nb", build)


# ---------------------------------------------------------------- registry
def E(id_, file_, pattern, expected, tol, note):
    return {"id": id_, "file": file_, "pattern": pattern, "expected": expected, "tol": tol, "note": note}


def d3(setname, hw, what):
    """Dense-parent-grid diagnostic D3 of external/wide_box_diagnostics_out.txt: nested Q2 ('q2') or
    number of boundary folds ('bd') of the parent for dHvap on 'octane'/'nonane' at box half-width hw."""
    import re as _re
    t = open(os.path.join(ROOT, "external", "wide_box_diagnostics_out.txt")).read()
    m = _re.search(r"D3 %s dHvap dense parent grid half-width %d: nested Q2 ([\d.]+), folds on boundary (\d+)/(\d+)" % (setname, hw), t)
    return float(m.group(1)) if what == "q2" else int(m.group(2))


REGISTRY = []
_add = REGISTRY.append

# ----- Section 1 Introduction (main) -----
_add(E("intro_collide_from13", "main", r"from\s+\$(?P<v>\d+)\$,\s+and",
       "s1_first_below('all', 'qh')", 0, "structural_checks_out.txt S1: first n with qhist < profiles (all trees)"))  # 1 match
_add(E("intro_collide_from13_b", "main", r"from\s+\$(?P<v>\d+)\$,\s+and",
       "s1_first_below('all', 'qh')", 0, "S1 first qhist<profiles, all"))  # 1
_add(E("intro_collide_from16_mol", "main", r"from\s+\$(?P<v>\d+)\$\s+for",
       "s1_first_below('mol', 'qh')", 0, "S1 first qhist<profiles, mol"))  # 1

# ----- Section 3 Parameter geometry (main) -----
_add(E("rp_n13", "main", r"for every \$n \\ge (?P<v>\d+)\$ \(and every \$n \\ge 16\$ among trees", "s1_first_below('all', 'qh')", 0, "S1"))  # 1
_add(E("rp_n16", "main", r"for every \$n \\ge 13\$ \(and every \$n \\ge (?P<v>\d+)\$ among trees", "s1_first_below('mol', 'qh')", 0, "S1 mol"))  # 1
_add(E("rp_proof_order13", "main", r"two\s+order\-\$(?P<v>\d+)\$\s+profiles", "lean_order()", 0, "formal/LoyolaFormal/Profiles.lean P1/P2 (12 edges)"))  # 1
_add(E("rp_proof_d3", "main", r"dimension\s+\$(?P<v>\d+)\$,\s+while", "common_leaf_degree(*order13_pair())", 0,
       "smallest degree d>=2 with (1,d) in both Lean profiles P1,P2"))  # 1
_add(E("rp_proof_order16", "main", r"the\s+order\-\$(?P<v>\d+)\$\s+pair", "s1_first_below('mol', 'qh')", 0, "S1 mol first failure"))  # 1
_M16A = r"\\\{\(1,2\)\^\{%s\}, \(1,4\)\^\{%s\}, \(2,4\)\^\{%s\}, \(4,4\)\^\{%s\}\\\}"
_M16B = r"\\\{\(1,4\)\^\{%s\}, \(2,2\)\^\{%s\}, \(2,4\)\^\{%s\}\\\}"
for _k, (_pair, _slot) in enumerate([((1, 2), 0), ((1, 4), 1), ((2, 4), 2), ((4, 4), 3)]):
    _f = ["2", "8", "2", "3"]; _f[_slot] = r"(?P<v>\d+)"
    _add(E("rp_mol16_A_%d%d" % _pair, "main", _M16A % tuple(_f), "mol16_pair()[0][%r]" % (_pair,), 0,
           "enumeration: unique q-histogram collision among order-16 trees with Delta<=4 (profile containing (4,4))"))  # 1 each
for _k, (_pair, _slot) in enumerate([((1, 4), 0), ((2, 2), 1), ((2, 4), 2)]):
    _f = ["8", "3", "4"]; _f[_slot] = r"(?P<v>\d+)"
    _add(E("rp_mol16_B_%d%d" % _pair, "main", _M16B % tuple(_f), "mol16_pair()[1][%r]" % (_pair,), 0,
           "enumeration: order-16 Delta<=4 collision (profile containing (2,2))"))  # 1 each
_add(E("rp_proof_d4", "main", r"realises\s+\$\(2,(?P<v>\d+)\)\$,\s+\$\(2,2\)\$", "common_leaf_degree(*mol16_pair())", 0, "smallest common leaf-neighbour degree of the order-16 pair"))  # 1
_add(E("rp_enum_to17", "main", r"orders\s+\$2\$\-\-\$(?P<v>\d+)\$,\s+two", "max(s1_orders('all'))", 0, "S1 orders"))  # 1
_add(E("rp_coincide_12", "main", r"most\s+\$(?P<v>\d+)\$\s+with", "s1_last_eq('all')", 0, "S1: last n with qhist==profiles (all)"))  # 1
_add(E("rp_coincide_15", "main", r"of order at most\s+\$(?P<v>\d+)\$\.\s+With part", "s1_last_eq('mol')", 0, "S1: last n with qhist==profiles (mol)"))  # 1
_add(E("rp_orders13", "main", r"At orders \$(?P<v>\d+)\$--\$17\$ generic points", "s1_first_below('all', 'qh')", 0, "S1"))  # 1
_add(E("rp_orders17", "main", r"At orders \$13\$--\$(?P<v>\d+)\$ generic points", "max(s1_orders('all'))", 0, "S1"))  # 1
_add(E("rp_GA_merge17", "main", r"trees first at\s+order\s+\$(?P<v>\d+)\$,\s+for instance", "s1_first_merge()", 0, "S1 GA_qmerges column"))  # 1
_GA_A = r"\\\{\(1,5\)\^\{%s\}, \(2,2\)\^\{%s\}, \(5,5\)\^\{%s\}, \(2,5\), \(1,2\)\\\}"
_GA_B = r"\\\{\(4,5\)\^\{%s\}, \(1,4\)\^\{%s\}, \(1,5\)\^\{%s\}, \(2,5\), \(1,2\)\\\}"
for _pair, _slot in [((1, 5), 0), ((2, 2), 1), ((5, 5), 2)]:
    _f = ["10", "2", "2"]; _f[_slot] = r"(?P<v>\d+)"
    _add(E("rp_ga17_A_%d%d" % _pair, "main", _GA_A % tuple(_f), "ga17_pair()[0][%r]" % (_pair,), 0,
           "enumeration: the unique GA value merging two distinct q-histograms at order 17 (profile containing (5,5))"))  # 1 each
for _pair, _slot in [((4, 5), 0), ((1, 4), 1), ((1, 5), 2)]:
    _f = ["3", "5", "6"]; _f[_slot] = r"(?P<v>\d+)"
    _add(E("rp_ga17_B_%d%d" % _pair, "main", _GA_B % tuple(_f), "ga17_pair()[1][%r]" % (_pair,), 0, "enumeration: order-17 GA merge (other profile)"))  # 1 each
# crossings
_add(E("cr_order12", "main", r"order\s+\$(?P<v>\d+)\$\s+with", "s3()['order']", 0, "S3 header"))  # 1
_add(E("cr_maxdeg6", "main", r"have\s+\$\\Delta\s+=\s+(?P<v>\d+)\$,\s+eight distinct", "s3()['maxdeg']", 0, "S3 maxdeg"))  # 1
_add(E("cr_eight_imb", "main", r"=\s+6\$,\s+(?P<v>[a-z]+)\s+distinct\s+imbalances", "word(s3()['nimb'])", 0, "S3 distinct imbalances"))  # 1
_add(E("cr_V5", "main", r"\$V\s+=\s+(?P<v>\d+)\$,\s+and\s+at", "s3()['V']", 0, "S3 V"))  # 1
_add(E("cr_five_times", "main", r"Whether\s+(?P<v>[a-z]+)\s+crossings\s+are", "word(s3()['cross'])", 0, "S3 crossings"))  # 1
_add(E("cr_alpha", "main", r"\$\(\\alpha,\\beta\)\s+=\s+\((?P<v>-?\d+),0\)\$\s+they\s+cross", "s3()['alpha']", 0, "S3 header (alpha,beta)"))  # 1
_add(E("cr_beta", "main", r"=\s+\(\-1,(?P<v>-?\d+)\)\$\s+they\s+cross", "s3()['beta']", 0, "S3 header (alpha,beta)"))  # 1
# identifiability
_add(E("id_delta6", "main", r"admissible pairs with\s+\$\\Delta \\le (?P<v>\d+)\$ \(by exhaustive enumeration", "s4_max_ok()", 0, "S4 Delta=6: 0 violations"))  # 1
_add(E("id_delta7", "main", r"\$\\Delta\s+=\s+(?P<v>\d+)\$:\s+among", "s4_first_fail()", 0, "S4 Delta=7: 1 violation"))  # 1
_add(E("id_fail_set", "main", r"the only one violating equality is\s+\$\\\{(?P<v>[0-9(),]+)\\\}\$,\s+whose", "s4_fail_set_str()", 0, "S4 Delta=7 violating set"))  # 1
_add(E("id_degree_sum8", "main", r"whose\s+degree sums all equal \$(?P<v>\d+)\$", "(lambda s: s.pop() if len(s) == 1 else None)({i + j for i, j in s4_fail_set()})", 0, "sum of each pair in the S4 set"))  # 1
_add(E("id_nine_pairs", "main", r"union\s+contains\s+(?P<v>nine)\s+of\s+the", "word(len(oct_union_pairs()))", 0, "octane_data: union of realised degree pairs"))  # 1
_add(E("id_affdim3", "main", r"its affine\s+dimension is \$(?P<v>\d+)\$, so", "oct_affine_dim()", 0, "rank of z_ij differences over the octane pair union"))  # 1

# ----- Section 5 Discrimination (main) -----
_add(E("ceil_18", "main", r"Among the\s+\$(?P<v>\d+)\$ octane isomers exactly \$16\$ distinct count vectors", "oct_n()", 0, "octane_data"))  # 1
_add(E("ceil_16", "main", r"octane isomers exactly \$(?P<v>\d+)\$ distinct count vectors occur", "oct_nprofiles()", 0, "distinct degree-pair profiles of the 18 octanes"))  # 1
_add(E("ceil_pair1", "main", r"pairs \$\\\{\$(?P<v>[^$]+)\$\\\}\$ and\s+\$\\\{\$3,4-dimethylhexane", "oct_collision_str(0)", 0, "octane_data collision groups (dataset order)"))  # 1
_add(E("ceil_pair2", "main", r"and\s+\$\\\{\$(?P<v>[^$]+)\$\\\}\$ share their", "oct_collision_str(1)", 0, "octane_data collision groups"))  # 1
_add(E("ceil_proof_18", "main", r"The counts for the \$(?P<v>\d+)\$ octane\s+isomers are computed", "oct_n()", 0, "octane_data"))  # 1
_add(E("tabcoll_18", "main", r"collision pairs among the \$(?P<v>\d+)\$ octane", "oct_n()", 0, "octane_data (table caption)"))  # 1
_add(E("deg_106", "main", r"\$N\s+=\s+(?P<v>\d+)\$\s+trees", "mod(10, 'all_trees')['N_trees']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("deg_order10", "main", r"of\s+order\s+\$(?P<v>\d+)\$\s+the\s+pure\-\$\\gamma\$", "mod_order_with_N(106)", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("deg_N106", "main", r"the\s+\$(?P<v>\d+)\$\s+trees", "mod(10, 'all_trees')['N_trees']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("deg_255_pct", "main", r"attain \$(?P<v>[\d.]+)\\%\$\s+\(\$79\$ distinct values\)", "pct(mod(10,'all_trees')['LO001'], mod(10,'all_trees')['N_trees'])", 0.05, "100(1-79/106)"))  # 1
_add(E("deg_M1_830_pct", "main", r"while \$M_1\$\s+\(\$(?P<v>[\d.]+)\\%\$\) and\s+\$M_2\$", "pct(mod(10,'all_trees')['M1'], mod(10,'all_trees')['N_trees'])", 0.05, "100(1-18/106)"))  # 1
_add(E("deg_79", "main", r"attain \$25\.5\\%\$\s+\(\$(?P<v>\d+)\$ distinct values\), tied", "mod(10, 'all_trees')['LO001']", 0, "multi_order_degeneracy.csv LO001"))  # 1
_add(E("deg_106b", "main", r"The\s+\$(?P<v>\d+)\$\s+trees", "mod(10, 'all_trees')['N_trees']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("deg_79b", "main", r"trees\s+realise\s+only\s+\$(?P<v>\d+)\$\s+distinct\s+edge\-degree\-pair\s+count", "mod(10, 'all_trees')['distinct_BID_profiles']", 0, "multi_order_degeneracy.csv profiles"))  # 1
_add(E("deg_M2_67", "main", r"\$M_2\$\s+\(\$(?P<v>[\d.]+)\\%\$\)\s+are", "pct(mod(10,'all_trees')['M2'], mod(10,'all_trees')['N_trees'])", 0.05, "100(1-35/106)"))  # 1
_add(E("deg_orders7", "main", r"For orders \$(?P<v>\d+)\$ through \$12\$, on all trees", "min(mod_orders())", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("deg_orders12", "main", r"For orders \$7\$ through \$(?P<v>\d+)\$, on all trees", "max(mod_orders())", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("deg_chi_order10", "main", r"order\s+\$(?P<v>\d+)\$,\s+with", "chi_first_below()", 0, "chi_floor_out.txt"))  # 1
_add(E("deg_chi_77", "main", r"with\s+\$(?P<v>[+-]?[\d.]+)\$\s+values", "chi_floor(10)[1]", 0, "chi_floor_out.txt n=10"))  # 1
_add(E("deg_chi_79", "main", r"against\s+\$(?P<v>\d+)\$\s+profiles\.", "chi_floor(10)[0]", 0, "chi_floor_out.txt n=10"))  # 1
_add(E("deg_upto12", "main", r"profiles up to\s+order \$(?P<v>\d+)\$ \(order \$15\$ for", "s1_last_eq('all')", 0, "S1"))  # 1
_add(E("deg_upto15", "main", r"\(order \$(?P<v>\d+)\$ for \$\\Delta \\le 4\$\)\s+and not beyond", "s1_last_eq('mol')", 0, "S1 mol"))  # 1
_add(E("deg_order13", "main", r"At\s+order\s+\$(?P<v>\d+)\$\s+the\s+profiles", "s1_first_below('all', 'qh')", 0, "S1"))  # 1


def _profile_entries(file_, prefix):
    """Entries for the order-13 collision profiles and their shared q-histogram."""
    out = []
    A = [((1, 2), "1"), ((1, 3), "2"), ((1, 6), "5"), ((2, 3), "2"), ((2, 6), "1"), ((3, 3), "1")]
    B = [((1, 3), "3"), ((1, 6), "5"), ((2, 2), "1"), ((2, 3), "2"), ((3, 6), "1")]
    for which, lst in (("P1", A), ("P2", B)):
        for k, (pair, _) in enumerate(lst):
            parts = []
            for kk, (p, mult) in enumerate(lst):
                m = r"(?P<v>\d+)" if kk == k else mult
                parts.append(r"\(%d,%d\)\^\{%s\}" % (p[0], p[1], m))
            pat = r"\\\{" + ", ".join(parts) + r"\\\}"
            out.append(E("%s_%s_%d%d" % (prefix, which, pair[0], pair[1]), file_, pat,
                         "dict(lean_profile(%r))[%r]" % (which, pair), 0,
                         "formal/LoyolaFormal/Profiles.lean %s (verified as a q-histogram collision class among order-13 trees)" % which))
    Q = [("0", "0", "1"), (r"\\tfrac15", "1/5", "2"), (r"\\tfrac13", "1/3", "1"), (r"\\tfrac12", "1/2", "3"), (r"\\tfrac57", "5/7", "5")]
    for k, (sym, q, _) in enumerate(Q):
        parts = []
        for kk, (s2, q2, mult) in enumerate(Q):
            m = r"(?P<v>\d+)" if kk == k else mult
            parts.append(r"%s\^\{%s\}" % (s2, m))
        pat = r"\\\{" + ", ".join(parts) + r"\\\}"
        out.append(E("%s_qhist_%s" % (prefix, q.replace("/", "_")), file_, pat, "order13_qhist(%r)" % q, 0,
                     "q-histogram of Lean profile P1 (equals that of P2)"))
    return out


REGISTRY.extend(_profile_entries("main", "deg13"))  # 16 entries, 1 match each
_add(E("deg_first_14", "main", r"order\s+\$(?P<v>\d+)\$,\s+where", "s1_first_below('all', 'R')", 0, "S1"))  # 1
_add(E("deg_1090", "main", r"ure\-\$\\gamma\$\ points\ give\ \$(?P<v>[+-]?[\d.]+)\$\ values\.", "s1(14, 'all')['LO1']", 0, "S1 n=14 LO(0,0,1)"))  # 1
_add(E("deg_R_order13", "main", r"\$R\$ still\s+attains the floor at order \$(?P<v>\d+)\$ \(\$570\$ values\)", "s1_first_below('all', 'R') - 1", 0, "S1: order before R's first failure"))  # 1
_add(E("deg_R_570", "main", r"\$13\$\s+\(\$(?P<v>[+-]?[\d.]+)\$\s+values\)", "s1(13, 'all')['R']", 0, "S1 n=13 R"))  # 1
# Table 2 caption and cells
_add(E("ff_cap_11", "main", r"at\s+\$(?P<v>\d+)\$\s+significant", "sc_sigdigits()", 0, "structural_checks.py key() format"))  # 1
_add(E("ff_cap_below7", "main", r"below\s+\$(?P<v>\d+)\$\s+were", "min(s1_orders('all'))", 0, "S1"))  # 1
_add(E("ff_LO_all_n", "main", r"\\gamma\)\$ & \$(?P<v>\d+)\$ \(\$566/570\$\) & never", "s1_first_below('all', 'LO1')", 0, "S1"))  # 1
_add(E("ff_LO_all_v", "main", r"\\gamma\)\$ & \$13\$ \(\$(?P<v>\d+)/570\$\) & never", "s1(13, 'all')['LO1']", 0, "S1"))  # 1
_add(E("ff_LO_all_p", "main", r"\\gamma\)\$ & \$13\$ \(\$566/(?P<v>\d+)\$\) & never", "s1(13, 'all')['prof']", 0, "S1"))  # 1
_add(E("ff_LO_mol_n", "main", r"never\$\^\{a\}\$ & \$(?P<v>\d+)\$ \(\$809/810\$\) & never", "s1_first_below('mol', 'LO1')", 0, "S1 mol"))  # 1
_add(E("ff_LO_mol_v", "main", r"never\$\^\{a\}\$ & \$16\$ \(\$(?P<v>\d+)/810\$\) & never", "s1(16, 'mol')['LO1']", 0, "S1 mol"))  # 1
_add(E("ff_LO_mol_p", "main", r"never\$\^\{a\}\$ & \$16\$ \(\$809/(?P<v>\d+)\$\) & never", "s1(16, 'mol')['prof']", 0, "S1 mol"))  # 1
_add(E("ff_R_all_n", "main", r"\$R\$ & \$(?P<v>\d+)\$ \(\$1095/1100\$\)", "s1_first_below('all', 'R')", 0, "S1"))  # 1
_add(E("ff_R_all_v", "main", r"\$R\$ & \$14\$ \(\$(?P<v>\d+)/1100\$\)", "s1(14, 'all')['R']", 0, "S1"))  # 1
_add(E("ff_R_all_p", "main", r"\$R\$ & \$14\$ \(\$1095/(?P<v>\d+)\$\)", "s1(14, 'all')['prof']", 0, "S1"))  # 1
_add(E("ff_R_mol_n", "main", r"\$R\$ & \$14\$ \(\$1095/1100\$\) & n/a\$\^\{b\}\$ & \$(?P<v>\d+)\$ \(\$1191/1194\$\)", "s1_first_below('mol', 'R')", 0, "S1 mol: first order with R below the profile floor"))  # 1
_add(E("ff_R_mol_v", "main", r"n/a\$\^\{b\}\$ & \$17\$ \(\$(?P<v>\d+)/1194\$\)", "s1(17, 'mol')['R']", 0, "S1 mol n=17 R"))  # 1
_add(E("ff_R_mol_p", "main", r"n/a\$\^\{b\}\$ & \$17\$ \(\$1191/(?P<v>\d+)\$\)", "s1(17, 'mol')['prof']", 0, "S1 mol n=17 profiles"))  # 1
_add(E("ff_GA_mol_gt17", "main", r"\$\^\{d\}\$ & \$> (?P<v>\d+)\^\{e\}\$", "max(s1_orders('mol')) if all(s1(n, 'mol')['merge'] == 0 for n in s1_orders('mol')) else None", 0, "S1 mol: GA merges no q-histograms up to the largest order examined"))  # 1
_add(E("ff_GA_all_n", "main", r"\$GA\$ & \$(?P<v>\d+)\$ \(\$566/570\$\)\$\^\{d\}\$", "s1_first_below('all', 'GA')", 0, "S1"))  # 1
_add(E("ff_GA_all_v", "main", r"\$GA\$ & \$13\$ \(\$(?P<v>\d+)/570\$\)\$\^\{d\}\$", "s1(13, 'all')['GA']", 0, "S1"))  # 1
_add(E("ff_GA_all_p", "main", r"\$GA\$ & \$13\$ \(\$566/(?P<v>\d+)\$\)\$\^\{d\}\$", "s1(13, 'all')['prof']", 0, "S1"))  # 1
_add(E("ff_GA_merge17", "main", r"& \$(?P<v>\d+)\^\{e\}\$ & \$16\$", "s1_first_merge()", 0, "S1 GA_qmerges"))  # 1
_add(E("ff_GA_mol_n", "main", r"\$17\^\{e\}\$ & \$(?P<v>\d+)\$ \(\$809/810\$\)\$\^\{d\}\$", "s1_first_below('mol', 'GA')", 0, "S1 mol"))  # 1
_add(E("ff_GA_mol_v", "main", r"\$17\^\{e\}\$ & \$16\$ \(\$(?P<v>\d+)/810\$\)\$\^\{d\}\$", "s1(16, 'mol')['GA']", 0, "S1 mol"))  # 1
_add(E("ff_GA_mol_p", "main", r"\$17\^\{e\}\$ & \$16\$ \(\$809/(?P<v>\d+)\$\)\$\^\{d\}\$", "s1(16, 'mol')['prof']", 0, "S1 mol"))  # 1
_add(E("ff_fn_mol_upto17", "main", r"merges no \$q\$-histograms up to order \$(?P<v>\d+)\$, the largest examined", "max(s1_orders('mol'))", 0, "S1 mol orders"))  # 1
_add(E("ff_fn_below17", "main", r"merges no \$q\$-histograms below order \$(?P<v>\d+)\$, so", "s1_first_merge()", 0, "S1"))  # 1
_add(E("ff_fn_maxdeg5", "main", r"has maximum degree \$(?P<v>\d+)\$;", "ga17_maxdeg()", 0, "max degree in the order-17 GA witness profiles"))  # 1
# off the ratio plane
_add(E("off_order16", "main", r"order\s+\$(?P<v>\d+)\$\s+\(\$4069\$", "max(frac_orders())", 0, "fractional_points_out.txt"))  # 1
_add(E("off_4069_prof", "main", r"\s+\(\$(?P<v>\d+)\$ profiles\), \$LO\(0,\\tfrac12,0\)\$", "frac_profiles(16)", 0, "fractional_points_out.txt n=16"))  # 1
_add(E("off_3475", "main", r"only\ \$(?P<v>[+-]?[\d.]+)\$\ and\ \$3476\$\ distinct\ valu", "frac_count(16, 0, 0.5, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("off_3476", "main", r"and\s+\$(?P<v>[+-]?[\d.]+)\$\s+distinct", "frac_count(16, 0, 1/3, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("off_4069_sep", "main", r"all\s+\$(?P<v>\d+)\$\.\s+\$LO\(\\tfrac12,0,\\cdot\)\$",
       "frac_count(16, 0, 0.5, 1) if frac_count(16, 0, 0.5, 1) == frac_count(16, 0, 1/3, 1) == frac_profiles(16) else None", 0, "fractional_points_out.txt"))  # 1
_add(E("off_3940", "main", r"from\ \$(?P<v>[+-]?[\d.]+)\$\ to\ \$4067\$\ and\ the\ Randi\\", "frac_count(16, 0.5, 0, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("off_4067", "main", r"to\s+\$(?P<v>[+-]?[\d.]+)\$\s+and", "frac_count(16, 0.5, 0, 1)", 0, "fractional_points_out.txt"))  # 1
_add(E("off_4007", "main", r"from\ \$(?P<v>[+-]?[\d.]+)\$\ to\ \$4068\$\ as\ \$\\gamma\$\ go", "frac_count(16, -0.5, 0, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("off_4068", "main", r"\$4007\$\s+to\s+\$(?P<v>[+-]?[\d.]+)\$\s+as\s+\$\\gamma\$", "frac_count(16, -0.5, 0, 1)", 0, "fractional_points_out.txt"))  # 1
_add(E("off_3996", "main", r"unaffected\s+\(\$(?P<v>\d+)\$\s+in", "frac_ratio_plane_count(16)", 0, "fractional_points_out.txt (0.5,-1) and (-0.5,1), both gammas"))  # 1
_add(E("off_generic_4069", "main", r"all\s+\$(?P<v>\d+)\$\s+profiles", "distinct_count(16, 0.3, 0.2, 0)", 0, "enumeration of order-16 trees, 11 significant digits"))  # 1
_add(E("off_orders12", "main", r"orders\s+\$(?P<v>\d+)\$\-\-\$16\$\s+but", "min(frac_orders())", 0, "fractional_points_out.txt"))  # 1
_add(E("off_orders16", "main", r"orders\s+\$12\$\-\-\$(?P<v>\d+)\$\s+but", "max(frac_orders())", 0, "fractional_points_out.txt"))  # 1
# structure sensitivity (main)
_add(E("ss_75", "main", r"published protocol on the \$(?P<v>\d+)\$ decane isomer", "mod(10, 'molecular')['N_trees']", 0, "multi_order_degeneracy.csv n=10 molecular"))  # 1
_add(E("ss_eleven", "main", r"Das\~\\cite\{BarmanDas2026HSO\},\s+with\s+(?P<v>[a-z]+)\s+of\s+fourteen", "word(control_count('exact_at_4dp'))", 0, "fgd_published_control.csv"))  # 1
_add(E("ss_fourteen", "main", r"eleven\s+of\s+(?P<v>[a-z]+)\s+\$SS\$/\$Abr\$\s+values", "word(control_count())", 0, "fgd_published_control.csv rows"))  # 1
_add(E("ss_three", "main", r"the\s+other\s+(?P<v>[a-z]+)\s+agrees\s+within", "word(control_count('within_1_unit_4th_dp'))", 0, "fgd_published_control.csv"))  # 1


def _ss_common(file_, prefix):
    return [
        E(prefix + "_LO2_SS", file_, r"\(\$(?P<v>[\d.]+)\$ against \$0\.1256\$\)", "fgd('LO(0,0,2)')[0]", 0.00005, "fgd_structure_sensitivity_decanes.csv"),
        E(prefix + "_HM_SS", file_, r"\(\$0\.1257\$ against \$(?P<v>[\d.]+)\$\)", "fgd('HM')[0]", 0.00005, "fgd_structure_sensitivity_decanes.csv"),
        E(prefix + "_LO2_Abr", file_, r"abruptness(?: is markedly smaller)? \(\$(?P<v>[\d.]+)\$\s+against \$0\.313\$\)", "fgd('LO(0,0,2)')[1]", 0.0005, "fgd CSV"),
        E(prefix + "_HM_Abr", file_, r"abruptness(?: is markedly smaller)? \(\$0\.274\$\s+against \$(?P<v>[\d.]+)\$\)", "fgd('HM')[1]", 0.0005, "fgd CSV"),
        E(prefix + "_LO2_ratio", file_, r"points\s+\(\$(?P<v>[\d.]+)\$ and \$0\.4565\$\)", "fgd('LO(0,0,2)')[2]", 0.00005, "fgd CSV"),
        E(prefix + "_LO1_ratio", file_, r"points\s+\(\$0\.4579\$ and \$(?P<v>[\d.]+)\$\)", "fgd('LO(0,0,1)')[2]", 0.00005, "fgd CSV"),
        E(prefix + "_range_lo", file_, r"\$GA\$ and\s+\$R\$ \(\$(?P<v>[\d.]+)\$--\$0\.451\$", "min(fgd(k)[2] for k in ('H/2', 'GA', 'R'))", 0.0005, "fgd CSV ratios of H/2, GA, R"),
        E(prefix + "_range_hi", file_, r"\$GA\$ and\s+\$R\$ \(\$0\.448\$--\$(?P<v>[\d.]+)\$", "max(fgd(k)[2] for k in ('H/2', 'GA', 'R'))", 0.0005, "fgd CSV ratios of H/2, GA, R"),
        E(prefix + "_SS_g05", file_, r"\(\$(?P<v>[\d.]+)\$,\s+\$0\.062\$, \$0\.126\$, \$0\.319\$", "s5('LO(0,0,0.5)')[0]", 0.0005, "S5 lines"),
        E(prefix + "_SS_g1", file_, r"\(\$0\.031\$,\s+\$(?P<v>[\d.]+)\$, \$0\.126\$", "s5('LO(0,0,1)')[0]", 0.0005, "S5 lines"),
        E(prefix + "_SS_g2", file_, r"\$0\.062\$, \$(?P<v>[\d.]+)\$, \$0\.319\$", "s5('LO(0,0,2)')[0]", 0.0005, "S5 lines"),
        E(prefix + "_SS_g5", file_, r"\$0\.126\$, \$(?P<v>[\d.]+)\$ at\s+\$\\gamma = 0\.5, 1, 2, 5\$", "s5('LO(0,0,5)')[0]", 0.0005, "S5 lines"),
        E(prefix + "_peak_g2", file_, r"[Tt]he ratio\s+peaks near \$\\gamma = (?P<v>\d+)\$", "s5_ratio_peak()", 0, "argmax of ratio over the S5 gammas"),
        E(prefix + "_ratio_g5", file_, r"then\s+falls \(\$(?P<v>[\d.]+)\$ at \$\\gamma = 5\$\)", "s5('LO(0,0,5)')[2]", 0.0005, "S5 lines"),
        E(prefix + "_IRLA_SS", file_, r"\(\$SS = (?P<v>[\d.]+)\$, \$Abr = 0\.5066\$", "s5('IRLA')[0]", 0.00005, "S5 IRLA"),
        E(prefix + "_IRLA_Abr", file_, r"\$Abr = (?P<v>[\d.]+)\$, ratio", "s5('IRLA')[1]", 0.00005, "S5 IRLA"),
        E(prefix + "_IRLA_ratio", file_, r"\$Abr = 0\.5066\$, ratio\s+\$(?P<v>[\d.]+)\$\)", "s5('IRLA')[2]", 0.00005, "S5 IRLA"),
    ]


REGISTRY.extend(_ss_common("main", "ss"))  # 17 entries, 1 match each
_add(E("ss_cap_75", "main", r"ratio on the \$(?P<v>\d+)\$ decane isomers under", "mod(10, 'molecular')['N_trees']", 0, "multi_order_degeneracy.csv (table caption)"))  # 1

# ----- Section 6.1 collision-pair property differences (requested explicitly) -----
_add(E("s6_18", "main", r"the \$(?P<v>\d+)\$ isomers realise only \$16\$ distinct edge-degree-pair count", "oct_n()", 0, "octane_data"))  # 1
_add(E("s6_16", "main", r"the \$18\$ isomers realise only \$(?P<v>\d+)\$ distinct edge-degree-pair count", "oct_nprofiles()", 0, "octane_data"))  # 1
_add(E("s6_dTB_pair1", "main", r"to\s+\$(?P<v>[\d.]+)\\,\^\{\\circ\}\$C\s+in", "oct_collision_diff(0, 'T_B')", 0.005, "octane_data / bid_collision_table.csv: |T_B(3-MH) - T_B(4-MH)|"))  # 1
_add(E("s6_dTB_pair2", "main", r"and\s+\$(?P<v>[\d.]+)\\,\^\{\\circ\}\$C\s+within", "oct_collision_diff(1, 'T_B')", 0.005, "|T_B(3,4-DMH) - T_B(3E2MP)|"))  # 1

# ----- Reproducibility paragraph (main) -----

# ----- Appendix A prose (main) -----
_add(E("app_18", "supp", r"full\s+\$(?P<v>\d+)\$\-isomer\s+dataset", "oct_n()", 0, "octane_data"))  # 1
_add(E("app_dHvap_33DMH", "supp", r"values of 3,3-dimethylhexane \(\$(?P<v>[\d.]+)\$\),", "oct_prop('3,3-dimethylhexane', 'dHvap')", 0.0005, "octane_data"))  # 1
_add(E("app_dHvap_3E3MP", "supp", r"3-ethyl-3-methylpentane \(\$(?P<v>[\d.]+)\$\), 2,2,3-trimethylpentane", "oct_prop('3-ethyl-3-methylpentane', 'dHvap')", 0.0005, "octane_data"))  # 1
_add(E("app_dHvap_223TMP", "supp", r"2,2,3-trimethylpentane \(\$(?P<v>[\d.]+)\$\) and", "oct_prop('2,2,3-trimethylpentane', 'dHvap')", 0.0005, "octane_data"))  # 1
_add(E("app_dHvap_233TMP", "supp", r"2,3,3-trimethylpentane \(\$(?P<v>[\d.]+)\$\) are values consistent", "oct_prop('2,3,3-trimethylpentane', 'dHvap')", 0.0005, "octane_data"))  # 1
_add(E("app_S_233TMP", "supp", r"2,3,3-trimethylpentane \(\$(?P<v>[\d.]+)\$\) is a compiled-dataset", "oct_prop('2,3,3-trimethylpentane', 'S')", 0.0005, "octane_data"))  # 1
_add(E("app_six_S", "supp", r"The\s+remaining\s+(?P<v>[a-z]+)\s+\(4\-methylheptane,\s+2,2\-dimethylhexane,", "word(prov_S_cannot_verify())", 0, "octane_property_provenance_v35.csv: S rows CANNOT VERIFY"))  # 1
_add(E("app_api44_lo", "supp", r"values used by \$(?P<v>[\d.]+)\$--\$2\.2\$", "min(prov_api44_diffs())", 0.005, "provenance notes: API-44 differences"))  # 1
_add(E("app_api44_hi", "supp", r"values used by \$0\.07\$--\$(?P<v>[\d.]+)\$", "max(prov_api44_diffs())", 0.05, "provenance notes: API-44 differences (2.21 displayed as 2.2)"))  # 1
_add(E("app_api44_maxdr", "supp", r"correlations by at most \$(?P<v>[\d.]+)\$ in \$\|r\|\$ and puts", "sens_maxdr('entropy_api44_sensitivity_v41.csv')", 0.0005, "entropy_api44_sensitivity_v41.csv"))  # 1
_add(E("app_api44_M1_HM", "supp", r"ahead of\s+\$HM\$ by \$(?P<v>[\d.]+)\$", "sens_alt('entropy_api44_sensitivity_v41.csv', 'M1') - sens_alt('entropy_api44_sensitivity_v41.csv', 'HM')", 0.0005, "entropy_api44_sensitivity_v41.csv alternative |r|"))  # 1
_add(E("app_old_10131", "supp", r"The value \$(?P<v>[\d.]+)\$ found in our", "old_S_233()", 0.0005, "provenance paper_value 'was 101.31'"))  # 1
_add(E("app_used_10206", "supp", r"The value used, \$(?P<v>[\d.]+)\$, is that of", "oct_prop('2,3,3-trimethylpentane', 'S')", 0.0005, "octane_data"))  # 1
_add(E("app_ediz_10210", "supp", r"Ediz~\\cite\{Ediz2017Octane\} gives\s+\$(?P<v>[\d.]+)\$\)", "prov_ediz_233()", 0.0005, "provenance source_value (transcription of a published value)"))  # 1
_add(E("app_S_change_0006", "supp", r"most\s+\$(?P<v>[\d.]+)\$,\s+and", "oct_S_change_maxdr('2,3,3-trimethylpentane', old_S_233())", 0.0005, "recomputed: max |Delta r| over the 12 descriptors of Table 4, S with 101.31 vs 102.06 (ISI shifts by 0.0086; M2 0.0059 is the max of the other eleven)"))  # 1
_add(E("app_oct_S", "supp", r"\(octane \$(?P<v>[\d.]+)\$ vs \$111\.70\$", "oct_prop('octane', 'S')", 0.0005, "octane_data"))  # 1
_add(E("app_oct_S_ediz", "supp", r"\(octane \$111\.55\$ vs \$(?P<v>[\d.]+)\$;", None, 0, "Ediz 2017 compilation value; not in the repository"))  # 1
_add(E("app_22DMH_S", "supp", r"2,2-dimethylhexane \$(?P<v>[\d.]+)\$ vs \$103\.40\$", "oct_prop('2,2-dimethylhexane', 'S')", 0.0005, "octane_data"))  # 1
_add(E("app_22DMH_S_ediz", "supp", r"2,2-dimethylhexane \$103\.13\$ vs \$(?P<v>[\d.]+)\$;", None, 0, "Ediz 2017 value; not in the repository"))  # 1
_add(E("app_224TMP_S", "supp", r"2,2,4-trimethylpentane \$(?P<v>[\d.]+)\$\s+vs \$104\.10\$", "oct_prop('2,2,4-trimethylpentane', 'S')", 0.0005, "octane_data"))  # 1
_add(E("app_224TMP_S_ediz", "supp", r"2,2,4-trimethylpentane \$101\.81\$\s+vs \$(?P<v>[\d.]+)\$;", None, 0, "Ediz 2017 value; not in the repository"))  # 1
_add(E("app_233TMP_S_b", "supp", r"2,3,3-trimethylpentane \$(?P<v>[\d.]+)\$ vs \$102\.10\$\)", "oct_prop('2,3,3-trimethylpentane', 'S')", 0.0005, "octane_data"))  # 1
_add(E("app_233TMP_S_ediz", "supp", r"2,3,3-trimethylpentane \$102\.06\$ vs \$(?P<v>[\d.]+)\$\)", "prov_ediz_233()", 0.0005, "provenance source_value"))  # 1
_add(E("app_nist_11163", "supp", r"NIST WebBook \(\$(?P<v>[\d.]+)\$\)", "prov_octane_S_nist()", 0.0005, "provenance converted_value for octane S"))  # 1
_add(E("app_twelve", "supp", r"compilation values changes all (?P<v>[a-z]+) \$S\$ correlations, by up to", "word(sens_nchanged('entropy_source_sensitivity_v36.csv'))", 0, "entropy_source_sensitivity_v36.csv displayed_changes"))  # 1
_add(E("app_0043", "supp", r"by up to \$(?P<v>[\d.]+)\$\s+in \$\|r\|\$, and moves", "sens_maxdr('entropy_source_sensitivity_v36.csv')", 0.0005, "entropy_source_sensitivity_v36.csv"))  # 1
_add(E("app_HM_M1_0001", "supp", r"in \$\|r\|\$, and moves the margin between \$HM\$ and \$M_1\$ at the top from\s+\$[\d.]+\$ to \$(?P<v>[\d.]+)\$\.\s+\\item",
       "sens_alt('entropy_source_sensitivity_v36.csv', 'HM') - sens_alt('entropy_source_sensitivity_v36.csv', 'M1')", 0.0005,
       "entropy_source_sensitivity_v36.csv: |r_alt(HM)| - |r_alt(M1)| after substituting the compilation values"))  # 1
_add(E("app_tmb_841", "supp", r"The\s+benchmark value \$(?P<v>[\d.]+)\$ comes from", "oct_prop('2,2,3,3-tetramethylbutane', 'dHvap')", 0.0005, "octane_data"))  # 1
_add(E("app_tmb_103", "supp", r"\(\$(?P<v>[\d.]+)\$~kcal\\,mol\$\^\{-1\}\$\) at \$298\$~K as", "prov_tmb_dvap_kcal()", 0.005, "provenance source_value 42.94 kJ/mol / 4.184"))  # 1
_add(E("app_93", "supp", r"\(\$(?P<v>\d+)/100\$ and \$96/100\$ seeds", "tmb_lo_better(tmb_budgets()[0])", 0, "dhvap_tmb_exclusion_summary_v36.csv budget 200"))  # 1
_add(E("app_96", "supp", r"and \$(?P<v>\d+)/100\$ seeds instead", "tmb_lo_better(tmb_budgets()[1])", 0, "dhvap_tmb_exclusion_summary_v36.csv budget 500"))  # 1
_add(E("app_nseeds", "supp", r"\(\$93/(?P<v>\d+)\$ and", "tmb_nseeds()", 0, "dhvap_tmb_exclusion_summary_v36.csv n_seeds"))  # 1
_add(E("app_100of100", "supp", r"seeds instead of\s+\$(?P<v>\d+)/100\$\)", "expanded_lo_better('dHvap')", 0, "expanded_robustness_summary_v35.csv dHvap LO_better (both budgets)"))  # 1
_add(E("app_omega_lo", "supp", r"compilation by\s+\$(?P<v>[\d.]+)\$--\$0\.004\$", "min(prov_omega_diffs())", 0.0005, "provenance notes for 2,2,4-TMP and TMB omega"))  # 1
_add(E("app_omega_hi", "supp", r"by\s+\$0\.002\$\-\-\$(?P<v>[\d.]+)\$,\s+and", "max(prov_omega_diffs())", 0.0005, "provenance notes"))  # 1
_add(E("app_overall_0043", "supp", r"by\s+more than \$(?P<v>[\d.]+)\$\. The only bolded entry", "sens_overall_max()", 0.0005, "max |Delta|r|| over the three sensitivity CSVs"))  # 1
_add(E("app_margin_0001", "supp", r"where \$HM\$ leads \$M_1\$ by \$(?P<v>[\d.]+)\$ with the values used", "oct_S_margin('HM', 'M1')", 0.0005, "recomputed |r(HM,S)| - |r(M1,S)| on octane_data"))  # 1

# ----- Supplement S5 -----
_add(E("sup_106", "supp", r"On the \$(?P<v>\d+)\$ non-isomorphic\s+trees of order \$10\$ we use", "mod(10, 'all_trees')['N_trees']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_order10", "supp", r"trees of order \$(?P<v>\d+)\$ we use", "mod_order_with_N(106)", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_N106", "supp", r"values\}\\\},\\ N = (?P<v>\d+),", "mod(10, 'all_trees')['N_trees']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_45", "supp", r"set,\s+\$(?P<v>\d+)\$\s+of", "shared_count(10, 0, 0, 1)", 0, "enumeration: order-10 trees sharing their LO(0,0,1) value"))  # 1
_add(E("sup_45_106", "supp", r"the\s+\$(?P<v>\d+)\$\s+trees", "len(trees(10))", 0, "enumeration"))  # 1
_add(E("sup_425", "supp", r"trees\s+\(\$(?P<v>[\d.]+)\\%\$\)\s+share", "round(100.0 * shared_count(10, 0, 0, 1) / len(trees(10)), 1)", 0.05, "100*45/106"))  # 1
_add(E("sup_255", "supp", r"attain degeneracy \$(?P<v>[\d.]+)\\%\$ \(\$79\$ distinct values\),\s+among", "pct(mod(10,'all_trees')['LO001'], mod(10,'all_trees')['N_trees'])", 0.05, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_79", "supp", r"attain degeneracy \$25\.5\\%\$ \(\$(?P<v>\d+)\$ distinct values\),\s+among", "mod(10, 'all_trees')['LO001']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_106b", "supp", r"\$AG\$\.\s+The\s+\$(?P<v>\d+)\$\s+trees\s+realise", "mod(10, 'all_trees')['N_trees']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_79b", "supp", r"\$AG\$\.\s+The\s+\$106\$\s+trees\s+realise\s+only\s+\$(?P<v>\d+)\$\s+distinct\s+edge\-degree\-pair\s+count\s+vectors,\s+so\s+\$25\.5\\%\$", "mod(10, 'all_trees')['distinct_BID_profiles']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_255b", "supp", r"count vectors, so \$(?P<v>[\d.]+)\\%\$ is the minimum degeneracy", "pct(mod(10,'all_trees')['distinct_BID_profiles'], mod(10,'all_trees')['N_trees'])", 0.05, "floor"))  # 1
_add(E("sup_M1_83", "supp", r"\$LO\(0, 1, 0\)\$ \(\$(?P<v>[\d.]+)\\%\$\)", "pct(mod(10,'all_trees')['M1'], mod(10,'all_trees')['N_trees'])", 0.05, "multi_order_degeneracy.csv M1"))  # 1
_add(E("sup_M2_67", "supp", r"\$LO\(1, 0, 0\)\$ \(\$(?P<v>[\d.]+)\\%\$\)", "pct(mod(10,'all_trees')['M2'], mod(10,'all_trees')['N_trees'])", 0.05, "multi_order_degeneracy.csv M2"))  # 1
_add(E("sup_fig_106", "supp", r"on the \$(?P<v>\d+)\$ non-isomorphic trees of order \$10\$\. The dashed", "mod(10, 'all_trees')['N_trees']", 0, "figure caption"))  # 1
_add(E("sup_fig_order10", "supp", r"non-isomorphic trees of order \$(?P<v>\d+)\$\. The dashed", "mod_order_with_N(106)", 0, "figure caption"))  # 1
_add(E("sup_fig_255", "supp", r"floor, \$(?P<v>[\d.]+)\\% = 100\(1 - 79/106\)\$", "pct(mod(10,'all_trees')['distinct_BID_profiles'], mod(10,'all_trees')['N_trees'])", 0.05, "figure caption"))  # 1
_add(E("sup_fig_79", "supp", r"= 100\(1 - (?P<v>\d+)/106\)\$", "mod(10, 'all_trees')['distinct_BID_profiles']", 0, "figure caption"))  # 1
_add(E("sup_fig_106b", "supp", r"= 100\(1 - 79/(?P<v>\d+)\)\$", "mod(10, 'all_trees')['N_trees']", 0, "figure caption"))  # 1
_add(E("sup_fig_106c", "supp", r"79/106\)\$\.\s+The\s+\$(?P<v>\d+)\$\s+trees\s+realise", "mod(10, 'all_trees')['N_trees']", 0, "figure caption"))  # 1
_add(E("sup_fig_79b", "supp", r"79/106\)\$\.\s+The\s+\$106\$\s+trees\s+realise\s+only\s+\$(?P<v>\d+)\$\s+distinct\s+edge\-degree\-pair\s+count\s+vectors,\s+so\s+no", "mod(10, 'all_trees')['distinct_BID_profiles']", 0, "figure caption"))  # 1
_add(E("sup_orders7", "supp", r"orders\s+\$(?P<v>\d+)\$\s+through", "min(mod_orders())", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_orders12", "supp", r"through\s+\$(?P<v>\d+)\$\.\s+It", "max(mod_orders())", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_chi_10", "supp", r"order\s+\$(?P<v>\d+)\$\.\s+Floor", "chi_first_below()", 0, "chi_floor_out.txt"))  # 1
_add(E("sup_upto12", "supp", r"profiles up to\s+order \$(?P<v>\d+)\$ \(order \$15\$", "s1_last_eq('all')", 0, "S1"))  # 1
_add(E("sup_upto15", "supp", r"\(order\s+\$(?P<v>\d+)\$\s+for", "s1_last_eq('mol')", 0, "S1 mol"))  # 1
_add(E("sup_order13", "supp", r"order\s+\$(?P<v>\d+)\$\s+the", "s1_first_below('all', 'qh')", 0, "S1"))  # 1
REGISTRY.extend(_profile_entries("supp", "sup13"))  # 16 entries, 1 match each
_add(E("sup_566", "supp", r"points realise \$(?P<v>\d+)\$ distinct values against\s+\$570\$ profiles", "s1(13, 'all')['LO1']", 0, "S1"))  # 1
_add(E("sup_570", "supp", r"against\s+\$(?P<v>\d+)\$\s+profiles\.", "s1(13, 'all')['prof']", 0, "S1"))  # 1
_add(E("sup_mol16", "supp", r"failure occurs at order \$(?P<v>\d+)\$ \(\$809\$ values against \$810\$ profiles\)", "s1_first_below('mol', 'LO1')", 0, "S1 mol"))  # 1
_add(E("sup_809", "supp", r"at order \$16\$ \(\$(?P<v>\d+)\$ values against \$810\$ profiles\)", "s1(16, 'mol')['LO1']", 0, "S1 mol"))  # 1
_add(E("sup_810", "supp", r"\(\$809\$ values against \$(?P<v>\d+)\$ profiles\)", "s1(16, 'mol')['prof']", 0, "S1 mol"))  # 1
_add(E("sup_R13", "supp", r"index still attains the floor at order \$(?P<v>\d+)\$ \(\$570\$ values\)", "s1_first_below('all', 'R') - 1", 0, "S1"))  # 1
_add(E("sup_R570", "supp", r"at order \$13\$ \(\$(?P<v>\d+)\$ values\)\s+and falls below", "s1(13, 'all')['R']", 0, "S1"))  # 1
_add(E("sup_R14", "supp", r"falls below it at order \$(?P<v>\d+)\$ \(\$1095\$", "s1_first_below('all', 'R')", 0, "S1"))  # 1
_add(E("sup_1095", "supp", r"at order \$14\$ \(\$(?P<v>\d+)\$ values against \$1100\$", "s1(14, 'all')['R']", 0, "S1"))  # 1
_add(E("sup_1100", "supp", r"\(\$1095\$ values against \$(?P<v>\d+)\$\s+profiles, where", "s1(14, 'all')['prof']", 0, "S1"))  # 1
_add(E("sup_1090", "supp", r"where the pure-\$\\gamma\$ points give \$(?P<v>\d+)\$\)", "s1(14, 'all')['LO1']", 0, "S1"))  # 1
_add(E("sup_tab_n7", "supp", r"\$n\s+=\s+(?P<v>\d+)\$\-\-\$12\$\.\s+The", "min(mod_orders())", 0, "multi_order_degeneracy.csv (table caption)"))  # 1
_add(E("sup_tab_n12", "supp", r"=\s+7\$\-\-\$(?P<v>\d+)\$\.\s+The", "max(mod_orders())", 0, "multi_order_degeneracy.csv (table caption)"))  # 1
_add(E("sup_nine_points", "supp", r"evaluates the (?P<v>[a-z]+) fixed\s+points", "word(frac_npoints())", 0, "fractional_points_out.txt distinct (alpha,beta)"))  # 1
_add(E("sup_frac_12", "supp", r"orders\s+\$(?P<v>\d+)\$\-\-\$16\$,\s+where", "min(frac_orders())", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_frac_16", "supp", r"\(0,\\tfrac13\),\s+\(\\tfrac(?P<v>\d+),0\)\\bigr\\\}\s+\\end\{multline\*\}", "max(frac_orders())", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_eg_order16", "supp", r"orders\s+\$12\$\-\-\$(?P<v>\d+)\$,\s+where", "max(frac_orders())", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g1_0_05", "supp", r"are\s+\$(?P<v>\d+)\$,\s+\$4067\$,", "frac_count(16, 0, 0.5, 1)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g1_05_0", "supp", r"\$4069\$,\s+\$(?P<v>\d+)\$,\s+\$4069\$,", "frac_count(16, 0.5, 0, 1)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g1_0_m05", "supp", r"\$4067\$,\s+\$(?P<v>\d+)\$,\s+\$4068\$,", "frac_count(16, 0, -0.5, 1)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g1_m05_0", "supp", r"\$4069\$,\s+\$4067\$,\s+\$4069\$,\s+\$(?P<v>\d+)\$,\s+\$4069\$ and", "frac_count(16, -0.5, 0, 1)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g1_13_0", "supp", r"\$4068\$,\s+\$(?P<v>\d+)\$\s+and", "frac_count(16, 1/3, 0, 1)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g1_0_13", "supp", r"\$4069\$\s+and\s+\$(?P<v>\d+)\$\s+of\s+\$4069\$", "frac_count(16, 0, 1/3, 1)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_of_4069", "supp", r"and \$4069\$ of \$(?P<v>\d+)\$ for", "frac_profiles(16)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g0_0_05", "supp", r"give \$(?P<v>\d+)\$, \$3940\$, \$3476\$, \$4007\$", "frac_count(16, 0, 0.5, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g0_05_0", "supp", r"give \$3475\$, \$(?P<v>\d+)\$, \$3476\$", "frac_count(16, 0.5, 0, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g0_0_m05", "supp", r"\$3940\$, \$(?P<v>\d+)\$, \$4007\$", "frac_count(16, 0, -0.5, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g0_m05_0", "supp", r"\$3476\$,\s+\$(?P<v>\d+)\$,\s+\$4009\$", "frac_count(16, -0.5, 0, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g0_13_0", "supp", r"\$4007\$,\s+\$(?P<v>\d+)\$\s+and", "frac_count(16, 1/3, 0, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_g0_0_13", "supp", r"and\s+\$(?P<v>\d+)\$,\s+while", "frac_count(16, 0, 1/3, 0)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_3996", "supp", r"give\s+\$(?P<v>\d+)\$\s+for", "frac_ratio_plane_count(16)", 0, "fractional_points_out.txt"))  # 1
_add(E("sup_52", "supp", r"in \$(?P<v>\d+)\$ of \$81\$ point--dataset", "frac_wins()[0]", 0, "fractional_points_out.txt last line"))  # 1
_add(E("sup_81", "supp", r"in \$52\$ of \$(?P<v>\d+)\$ point--dataset", "frac_wins()[1]", 0, "fractional_points_out.txt last line"))  # 1
_add(E("sup_q2_021", "supp", r"stays at \$Q\^2 \\le (?P<v>[\d.]+)\$ on the\s+decanes", "math.ceil(frac_pred_max('decane T_B') * 100 - 1e-9) / 100", 0, "fractional_points_out.txt decane T_B (max 0.201 -> bound 0.21)"))  # 1

# ----- Supplement S6 -----
_add(E("sup_ss_75", "supp", r"published protocol on the \$(?P<v>\d+)\$ decane isomer trees", "mod(10, 'molecular')['N_trees']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_ss_75b", "supp", r"means over all\s+\$(?P<v>\d+)\$ trees\.", "mod(10, 'molecular')['N_trees']", 0, "multi_order_degeneracy.csv"))  # 1
_add(E("sup_ss_size7", "supp", r"nonempty \(sizes \$(?P<v>\d+)\$ to\s+\$43\$\)", "decane_nb_sizes()[0]", 0, "recomputed single-edge-relocation neighbour sets (WL hashing, as in structural_checks.py s5)"))  # 1
_add(E("sup_ss_size43", "supp", r"\(sizes \$7\$ to\s+\$(?P<v>\d+)\$\)", "decane_nb_sizes()[1]", 0, "recomputed neighbour sets"))  # 1
_add(E("sup_ss_seven", "supp", r"for the (?P<v>[a-z]+) indices common to both", "word(control_nindices())", 0, "fgd_published_control.csv distinct indices"))  # 1
_add(E("sup_ss_fourteen", "supp", r"These\s+give\s+(?P<v>[a-z]+)\s+tabulated\s+\$SS\$/\$Abr\$", "word(control_count())", 0, "fgd_published_control.csv rows"))  # 1
_add(E("sup_ss_eleven", "supp", r"of\s+which\s+(?P<v>[a-z]+)\s+agree\s+exactly", "word(control_count('exact_at_4dp'))", 0, "fgd_published_control.csv"))  # 1
_add(E("sup_ss_three", "supp", r"the\s+remaining\s+(?P<v>[a-z]+)\s+differ\s+by", "word(control_count('within_1_unit_4th_dp'))", 0, "fgd_published_control.csv"))  # 1
_add(E("sup_ss_twelve", "supp", r"our values for all (?P<v>[a-z]+) compared indices", "word(fgd_nindices())", 0, "fgd_structure_sensitivity_decanes.csv rows"))  # 1
REGISTRY.extend(_ss_common("supp", "sup_ss"))  # 17 entries, 1 match each

# ----- Supplement S7 -----
_add(E("lean_version", "supp", r"\(Lean v(?P<v>[\d.]+), Mathlib", "lean_version()", 0, "formal/lean-toolchain"))  # 1
_add(E("mathlib_version", "supp", r"Mathlib v(?P<v>[\d.]+)\)", "mathlib_version()", 0, "formal/lake-manifest.json inputRev"))  # 1
_add(E("lean_two_order13", "supp", r"two\s+order\-\$(?P<v>\d+)\$\s+trees", "lean_order()", 0, "Profiles.lean"))  # 1
_add(E("lean_order13_pair", "supp", r"3\s+\-\s+(?P<v>\d+)\\ln\s+2\)", "lean_order()", 0, "Profiles.lean"))  # 1
_add(E("lean_13_vertex", "supp", r"the\s+order\-\$(?P<v>\d+)\$\s+profile", "lean_par_len('par1') + 1", 0, "Profiles.lean par1 length + 1"))  # 1

_add(E("cr_root1r", "main", r"\$\\gamma\s+\\approx\s+(?P<v>-?\d+\.\d)\$,", "round(s3()['roots'][0], 1)", 0.05, "S3 certificate roots, 1 dp"))
_add(E("cr_root2r", "main", r"\\approx\s+-17\.2\$,\s+\$(?P<v>-?\d+\.\d)\$,", "round(s3()['roots'][1], 1)", 0.05, "S3 certificate roots, 1 dp"))
_add(E("cr_root3r", "main", r"\$-12\.0\$, \$(?P<v>-?\d+\.\d)\$, \$2\.7\$", "round(s3()['roots'][2], 1)", 0.05, "S3 certificate roots, 1 dp"))
_add(E("cr_root4r", "main", r"\$-2\.0\$, \$(?P<v>-?\d+\.\d)\$ and \$31\.1\$", "round(s3()['roots'][3], 1)", 0.05, "S3 certificate roots, 1 dp"))
_add(E("cr_root5r", "main", r"and\s+\$(?P<v>-?\d+\.\d)\$,\s+which\s+are", "round(s3()['roots'][4], 1)", 0.05, "S3 certificate roots, 1 dp"))
UNCHECKABLE = [e["id"] for e in REGISTRY if e["expected"] is None]
# app_oct_S_ediz, app_22DMH_S_ediz, app_224TMP_S_ediz: values of the Ediz (2017) compilation, cited, not held in the repository.


# ---------------------------------------------------------------- evaluation
def _norm(s):
    return re.sub(r"\s+", " ", s).strip()


# dense-grid box curve (Section 6.2), from external/wide_box_diagnostics_out.txt
_add(E("d3_oct_q2_2", "main", r"is\s+\$(?P<v>[\d.]+)\$, \$0\.9156\$, \$0\.9525\$ and \$0\.9383\$", "d3('octane', 2, 'q2')", 0, "D3 octane hw2"))
_add(E("d3_oct_q2_4", "main", r"\$0\.8873\$, \$(?P<v>[\d.]+)\$, \$0\.9525\$ and", "d3('octane', 4, 'q2')", 0, "D3 octane hw4"))
_add(E("d3_oct_q2_8", "main", r"\$0\.9156\$, \$(?P<v>[\d.]+)\$ and \$0\.9383\$", "d3('octane', 8, 'q2')", 0, "D3 octane hw8"))
_add(E("d3_oct_q2_12", "main", r"\$0\.9525\$ and \$(?P<v>[\d.]+)\$\s+at half-widths", "d3('octane', 12, 'q2')", 0, "D3 octane hw12"))
_add(E("d3_oct_bd_2", "main", r"boundary\s+in \$(?P<v>\d+)\$, \$18\$, \$18\$ and \$0\$ of the \$18\$ folds", "d3('octane', 2, 'bd')", 0, "D3 octane boundary folds hw2"))
_add(E("d3_oct_bd_4", "main", r"boundary\s+in \$18\$, \$(?P<v>\d+)\$, \$18\$ and \$0\$ of the \$18\$ folds", "d3('octane', 4, 'bd')", 0, "D3 octane boundary folds hw4"))
_add(E("d3_oct_bd_8", "main", r"boundary\s+in \$18\$, \$18\$, \$(?P<v>\d+)\$ and \$0\$ of the \$18\$ folds", "d3('octane', 8, 'bd')", 0, "D3 octane boundary folds hw8"))
_add(E("d3_oct_bd_12", "main", r"boundary\s+in \$18\$, \$18\$, \$18\$ and \$(?P<v>\d+)\$ of the \$18\$ folds", "d3('octane', 12, 'bd')", 0, "D3 octane boundary folds hw12"))
_add(E("d3_non_q2_2", "main", r"the values are \$(?P<v>[\d.]+)\$, \$0\.8779\$, \$0\.8997\$ and \$0\.8837\$", "d3('nonane', 2, 'q2')", 0, "D3 nonane hw2"))
_add(E("d3_non_q2_4", "main", r"\$0\.8532\$, \$(?P<v>[\d.]+)\$, \$0\.8997\$ and", "d3('nonane', 4, 'q2')", 0, "D3 nonane hw4"))
_add(E("d3_non_q2_8", "main", r"\$0\.8779\$, \$(?P<v>[\d.]+)\$ and \$0\.8837\$", "d3('nonane', 8, 'q2')", 0, "D3 nonane hw8"))
_add(E("d3_non_q2_12", "main", r"\$0\.8997\$ and \$(?P<v>[\d.]+)\$, with \$34\$", "d3('nonane', 12, 'q2')", 0, "D3 nonane hw12"))
_add(E("d3_non_bd_2", "main", r"with \$(?P<v>\d+)\$,\s+\$34\$, \$34\$ and \$0\$ boundary folds of \$34\$", "d3('nonane', 2, 'bd')", 0, "D3 nonane boundary folds hw2"))
_add(E("d3_non_bd_4", "main", r"with \$34\$,\s+\$(?P<v>\d+)\$, \$34\$ and \$0\$ boundary folds of \$34\$", "d3('nonane', 4, 'bd')", 0, "D3 nonane boundary folds hw4"))
_add(E("d3_non_bd_8", "main", r"with \$34\$,\s+\$34\$, \$(?P<v>\d+)\$ and \$0\$ boundary folds of \$34\$", "d3('nonane', 8, 'bd')", 0, "D3 nonane boundary folds hw8"))
_add(E("d3_non_bd_12", "main", r"with \$34\$,\s+\$34\$, \$34\$ and \$(?P<v>\d+)\$ boundary folds of \$34\$", "d3('nonane', 12, 'bd')", 0, "D3 nonane boundary folds hw12"))

def evaluate(root=None):
    global ROOT
    if root:
        ROOT = root
        if ROOT not in sys.path:
            sys.path.insert(0, ROOT)
    texts = {"main": _read("main.tex"), "supp": _read("supplement.tex")}
    results = []
    for e in REGISTRY:
        r = dict(id=e["id"], file=e["file"])
        hits = re.findall(e["pattern"], texts[e["file"]])
        r["n_matches"] = len(hits)
        if len(hits) != 1:
            r["status"] = "PATTERN_ERROR"; results.append(r); continue
        cap = hits[0] if isinstance(hits[0], str) else hits[0][0]
        r["tex"] = cap
        if e["expected"] is None:
            r["status"] = "UNCHECKABLE"; results.append(r); continue
        try:
            exp = eval(e["expected"], globals()) if isinstance(e["expected"], str) else e["expected"]
        except Exception as ex:  # noqa
            r["status"] = "EVAL_ERROR"; r["error"] = repr(ex); results.append(r); continue
        r["expected"] = exp
        if exp is None:
            r["status"] = "EVAL_NONE"
        elif isinstance(exp, str):
            r["status"] = "OK" if _norm(cap) == _norm(exp) else "MISMATCH"
        else:
            try:
                r["status"] = "OK" if abs(float(cap) - float(exp)) <= e["tol"] + 1e-12 else "MISMATCH"
            except ValueError:
                r["status"] = "MISMATCH"
        results.append(r)
    return results


def main():
    res = evaluate(sys.argv[1] if len(sys.argv) > 1 else None)
    from_ids = {e["id"] for e in REGISTRY}
    assert len(from_ids) == len(REGISTRY), "duplicate ids"
    counts = {}
    for r in res:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("entries:", len(REGISTRY), "|", counts)
    for r in res:
        if r["status"] != "OK":
            print(r)


if __name__ == "__main__":
    main()
