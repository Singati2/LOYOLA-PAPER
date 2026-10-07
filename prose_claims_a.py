#!/usr/bin/env python3
r"""Machine-checkable registry of every numeral stated in the running prose
(table captions included, tabular cells excluded) of

  main.tex       : abstract; Section 6 "A concise QSPR diagnostic"
                   (sec:sensitivity, sec:octanes, sec:ablation, sec:external,
                   sec:bp); Conclusion (sec:conclusion); Appendix A.1
                   (app:quality)
  supplement.tex : S1 (sec:s-prov), S3 (sec:s-ablation), S4 (sec:s-external)

Every `expected` value is DERIVED BY CODE from the canonical committed
artefacts of the repository (CSV files under the repo root, external/,
external/bp/, structural/*_out.txt, octane_data.py, analysis-script protocol
constants parsed by regex) -- never from the tex.  Entries whose number has no
machine-readable source carry expected=None and are listed in UNCHECKABLE.

Summary at the time of writing (main.tex 2292 lines / supplement.tex 928 lines,
2026-10-05 23:10 versions; re-run to refresh):
  entries           : 414  (main 235, supp 179)
  checkable         : 401  (expected derived from canonical files)
  matching          : 398
  flagged           :   3  -- aq_change006 (stated 0.006, computed max |r| shift
                              0.0086 driven by ISI; 0.006 only without ISI) and
                              the two *_AUDIT_alt entries (the HM/M1 margin of
                              0.001 holds for the original S data, not after the
                              compilation substitution the sentence describes:
                              0.007 then)
  uncheckable       :  13  (298 K condition constants, 95% confidence level,
                              10% edge definition, '1 K' precision remark,
                              'two days earlier')
  pattern problems  :   0  (every pattern matches its tex file exactly once)

Each entry: {"id", "file" ("main"|"supp"), "pattern" (one named group v),
"expected" (expression string evaluated in this module's namespace, a plain
value, or None), "tol" (absolute tolerance), "note" (provenance)}.

Running `python3 prose_claims_a.py` performs the self-check (or use
prose_numbers_check.py, which runs every registry):
each pattern must match its tex file exactly once (re.findall count == 1),
and the captured value is compared with the evaluated expectation.
"""
import os, re, csv, math
import numpy as np

# --------------------------------------------------------------------------
# repository location and canonical-file readers
# --------------------------------------------------------------------------
REPO = os.path.dirname(os.path.abspath(__file__))

try:
    import octane_data                                       # repo module
except ImportError:                                          # pragma: no cover
    import sys as _sys                                       # only to locate the repo module
    _sys.path.insert(0, REPO)
    import octane_data
from octane_data import OCTANES, NAMES, PROPS, alkane_pairs, lo_pairs


def P(*parts):
    return os.path.join(REPO, *parts)


def rows(*parts):
    with open(P(*parts), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def text(*parts):
    with open(P(*parts), encoding="utf-8") as f:
        return f.read()


def fnum(s):
    """Float of a tex/csv numeral ('+0.069', '-0.000', '10\\,000', '99.05')."""
    return float(str(s).replace("\\,", "").replace(",", "").replace("$", ""))


def rnd(x, d):
    """Round half away from zero at d decimals (display rounding of the paper)."""
    q = 10 ** d
    return math.copysign(math.floor(abs(x) * q + 0.5) / q, x)


WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
         7: "seven", 8: "eight", 9: "nine", 10: "ten", 11: "eleven",
         12: "twelve", 13: "thirteen", 14: "fourteen", 100: "one hundred"}


def word(n, cap=False):
    w = WORDS[int(n)]
    return w[0].upper() + w[1:] if cap else w


# --------------------------------------------------------------------------
# octane data (octane_data.py) and Table 4 correlations
# --------------------------------------------------------------------------
RED = {"M1": (0, 1, 0), "M2": (1, 0, 0), "HM": (0, 2, 0), "mM2": (-1, 0, 0),
       "R": (-0.5, 0, 0), "chi": (0, -0.5, 0), "H/2": (0, -1, 0),
       "ISI": (1, -1, 0), "GA": (0.5, -1, 0), "AG": (-0.5, 1, 0),
       "LO(0,0,1)": (0, 0, 1), "LO(0,0,2)": (0, 0, 2)}
CLASSICAL = [k for k in RED if not k.startswith("LO(")]          # ten reductions
BOLD = [("mM2", "T_B"), ("mM2", "dHf"), ("LO(0,0,1)", "dHvap"), ("HM", "S"), ("M2", "omega")]
OP = [alkane_pairs(r[0]) for r in OCTANES]
Y = {p: np.array([r[1 + i] for r in OCTANES], float) for i, p in enumerate(PROPS)}
N_OCT = len(OCTANES)
IDX = {n: i for i, n in enumerate(NAMES)}


def r_signed(x, y):
    xc = x - x.mean(); yc = y - y.mean(); s = np.linalg.norm(xc) * np.linalg.norm(yc)
    return 0.0 if s == 0 else float(xc @ yc / s)


def absr(x, y):
    return abs(r_signed(x, y))


def col(t, pl=None):
    a, b, g = t
    return np.array([lo_pairs(Pr, a, b, g) for Pr in (OP if pl is None else pl)])


def irla(P_):
    return sum(2.0 * abs(i - j) / (i + j) for i, j in P_)


def r_tab4(nm, prop, y=None):
    return r_signed(col(RED[nm]), Y[prop] if y is None else y)


def top_two_margin(prop, y=None):
    v = sorted((absr(col(RED[nm]), Y[prop] if y is None else y) for nm in RED), reverse=True)
    return v[0] - v[1]


def margins_all():
    return [top_two_margin(p) for p in PROPS]


def deletion_influence_max():
    mx = 0.0
    for nm, p in BOLD:
        x = col(RED[nm]); y = Y[p]; base = absr(x, y)
        d = max(abs(absr(np.delete(x, i), np.delete(y, i)) - base) for i in range(N_OCT))
        mx = max(mx, d)
    return mx


def boot_hw(x, y, B=10000, seed=0):
    rng = np.random.default_rng(seed); v = []
    for _ in range(B):
        idx = rng.integers(0, len(y), len(y)); v.append(absr(x[idx], y[idx]))
    lo_, hi = np.percentile(v, [2.5, 97.5]); return (hi - lo_) / 2


_BOOT_HW = {}


def boot_hws():
    if not _BOOT_HW:
        for nm, p in BOLD:
            _BOOT_HW[(nm, p)] = boot_hw(col(RED[nm]), Y[p])
    return _BOOT_HW


def y_with(prop, subs):
    """Property vector with molecule->value substitutions applied."""
    y = Y[prop].copy()
    for name, val in subs.items():
        y[IDX[name]] = val
    return y


def max_abs_r_change(prop, subs):
    y2 = y_with(prop, subs)
    return max(abs(absr(col(RED[nm]), y2) - absr(col(RED[nm]), Y[prop])) for nm in RED)


def s_margin(subs=None):
    """|r_HM| - |r_M1| on S (top-two margin between HM and M1)."""
    y = Y["S"] if not subs else y_with("S", subs)
    return abs(absr(col(RED["HM"]), y) - absr(col(RED["M1"]), y))


# alternative compilation values (parsed from the verifier's S_ALT / OMEGA_ALT
# dictionaries, which are the committed machine record of the alternative
# compilation used by entropy_source_sensitivity_v36.csv / omega_source_...)
_VER = text("verify_loyola_v35.py")


def _parse_alt(name):
    m = re.search(name + r"\s*=\s*\{([^}]*)\}", _VER)
    return {k: float(v) for k, v in re.findall(r'"([^"]+)"\s*:\s*([-\d.]+)', m.group(1))}


S_ALT = _parse_alt("S_ALT")
OMEGA_ALT = _parse_alt("OMEGA_ALT")
S_DIFFS = [abs(S_ALT[k] - OCTANES[IDX[k]][4]) for k in S_ALT]
OMEGA_DIFFS = [abs(OMEGA_ALT[k] - OCTANES[IDX[k]][5]) for k in OMEGA_ALT]
BOOT_B = int(re.search(r"def boot_hw\(x,y,B=(\d+)", _VER).group(1))

# v36 dHvap corrections recorded in the octane_data.py module docstring
DHVAP_CORR = [(float(a), float(b)) for a, b in
              re.findall(r"dH_vap\s+([\d.]+)\s*->\s*([\d.]+)", octane_data.__doc__)]
DHVAP_CORR_DIFFS = [abs(a - b) for a, b in DHVAP_CORR]

# S2 local-tuning pools (recipe of verify_loyola_v35.py section [E]: one
# default_rng(42) stream, 50 perturbations in (-0.3,0.3) per anchor, order M2,
# HM, mM2, LO(0,0,1), LO(0,0,2))
_POOLS = {}


def pools():
    if not _POOLS:
        rng = np.random.default_rng(42)
        for anm, (a0, b0, g0) in [("M2", (1., 0., 0.)), ("HM", (0., 2., 0.)), ("mM2", (-1., 0., 0.)),
                                  ("LO(0,0,1)", (0., 0., 1.)), ("LO(0,0,2)", (0., 0., 2.))]:
            perts = []
            for _ in range(50):
                da, db, dg = (round(float(rng.uniform(-0.3, 0.3)), 2) for _ in range(3))
                perts.append((round(a0 + da, 2), round(b0 + db, 2), round(g0 + dg, 2)))
            _POOLS[anm] = perts
    return _POOLS


def tuning_margin_dhvap():
    """max over the four S2 anchors of the best in-sample |r| within the 50-triple
    pool minus the best fixed benchmark |r| for dHvap, both at display rounding."""
    y = Y["dHvap"]; best_fixed = rnd(max(absr(col(RED[nm]), y) for nm in RED), 3)
    best_tuned = max(rnd(max(absr(col(t), y) for t in pools()[a]), 3) for a in ("M2", "HM", "mM2", "LO(0,0,1)"))
    return best_tuned - best_fixed


# --------------------------------------------------------------------------
# redundancy / PCA / collisions (descriptor_correlations.csv, pca_spectrum.csv,
# bid_collision_table.csv)
# --------------------------------------------------------------------------
def corr_matrix():
    rs = rows("descriptor_correlations.csv")
    names = [r[""] for r in rs]
    M = np.array([[float(r[n]) for n in names] for r in rs])
    return names, M


def n_pairs_ge(thr):
    names, M = corr_matrix(); n = len(names)
    return sum(1 for i in range(n) for j in range(i + 1, n) if abs(M[i, j]) >= thr)


def corr_between(a, b):
    names, M = corr_matrix(); return M[names.index(a), names.index(b)]


def max_abs_corr_with_classical(lo):
    names, M = corr_matrix(); i = names.index(lo)
    return max(abs(M[i, names.index(c)]) for c in ["M1", "M2", "HM", "mM2", "R", "chi", "H2", "ISI", "GA", "AG"])


def pca_cumvar(k):
    return float([r for r in rows("pca_spectrum.csv") if int(r["component"]) == k][0]["cumvar"])


def pca_participation_ratio():
    lam = np.array([float(r["eigenvalue"]) for r in rows("pca_spectrum.csv")])
    return lam.sum() ** 2 / (lam ** 2).sum()


def n_distinct_profiles():
    return len({tuple(sorted(p)) for p in OP})


def n_collision_pairs():
    from collections import Counter
    c = Counter(tuple(sorted(p)) for p in OP)
    return sum(1 for v in c.values() if v == 2)


def collision_tb_diff(k):
    """T_B difference within the k-th (0/1) collision pair of bid_collision_table.csv."""
    rs = rows("bid_collision_table.csv")
    pairs = sorted({r["profile_id"] for r in rs if r["collides_with"]})
    pid = pairs[k]
    t = [float(r["T_B"]) for r in rs if r["profile_id"] == pid]
    return abs(t[0] - t[1])


# --------------------------------------------------------------------------
# provenance (octane_property_provenance_v35.csv)
# --------------------------------------------------------------------------
PROV = rows("octane_property_provenance_v35.csv")


def prov_count(cls=None, prop=None):
    return sum(1 for r in PROV if (cls is None or r["classification"] == cls)
               and (prop is None or r["property"] == prop))


def prov_row(mol, prop):
    return [r for r in PROV if r["molecule"] == mol and r["property"] == prop][0]


def prov_num(mol, prop, field, pattern):
    return float(re.search(pattern, prov_row(mol, prop)[field]).group(1))


TMB = "2,2,3,3-tetramethylbutane"
TMB_DHVAP_KJ = [prov_num(TMB, "dHvap", "source_value", r"dvapH ([\d.]+) kJ/mol \(Majer"),
                prov_num(TMB, "dHvap", "source_value", r"([\d.]+) kJ/mol \(Osborne")]
TMB_TRIPLE_K = prov_num(TMB, "dHvap", "source_value", r"triple point ([\d.]+) K")
OCTANE_S_NIST = prov_num("octane", "S", "converted_value", r"([\d.]+) cal")
EDIZ_233 = prov_num("2,3,3-trimethylpentane", "S", "source_value", r"([\d.]+) \(Ediz")
KDB_TMB_OMEGA = prov_num(TMB, "omega", "source_value", r"([\d.]+) \(KDB")
KDB_224_OMEGA = prov_num("2,2,4-trimethylpentane", "omega", "source_value", r"([\d.]+) \(KDB")

# --------------------------------------------------------------------------
# sensitivity CSVs
# --------------------------------------------------------------------------
def sens(fname, col_o, col_a):
    rs = rows(fname)
    return {r["index"]: (float(r[col_o]), float(r[col_a])) for r in rs}


S_SENS = sens("entropy_source_sensitivity_v36.csv", "r_S_original", "r_S_alternative")
W_SENS = sens("omega_source_sensitivity_v35.csv", "r_omega_original", "r_omega_alternative")


def max_abs_change(d):
    return max(abs(abs(a) - abs(o)) for o, a in d.values())


# 1947 API Research Project 44 gas-phase entropies of the six NIST-absent
# isomers: recorded in the provenance notes ("lists S(gas, 25 C) = X"); the
# committed sensitivity file entropy_api44_sensitivity_v41.csv is used for the
# correlation effects when present, otherwise they are recomputed here.
API44 = {r["molecule"]: float(re.search(r"lists S\(gas, 25 C\) = ([\d.]+)", r["note"]).group(1))
         for r in PROV if r["property"] == "S" and r["classification"] == "CANNOT VERIFY"}
API44_DIFFS = [abs(API44[k] - OCTANES[IDX[k]][4]) for k in API44]
if os.path.exists(P("entropy_api44_sensitivity_v41.csv")):
    A_SENS = sens("entropy_api44_sensitivity_v41.csv", "r_S_original", "r_S_alternative")
else:                                                        # pragma: no cover
    A_SENS = {nm: (r_tab4(nm, "S"), r_signed(col(RED[nm]), y_with("S", API44))) for nm in RED}


def api44_m1_minus_hm():
    return abs(A_SENS["M1"][1]) - abs(A_SENS["HM"][1])


def s_margin_alt_csv():
    return abs(abs(S_SENS["HM"][1]) - abs(S_SENS["M1"][1]))


# --------------------------------------------------------------------------
# matched-budget ablation (ablation_*.csv, expanded_robustness_*.csv,
# dhvap_tmb_exclusion_summary_v36.csv)
# --------------------------------------------------------------------------
EXP = rows("expanded_robustness_summary_v35.csv")
EXP_RAW = rows("expanded_robustness_v35.csv")
TMBX = rows("dhvap_tmb_exclusion_summary_v36.csv")
ABL = rows("ablation_summary.csv")
ABLF = rows("ablation_perfold.csv")
ABLR = rows("ablation_robustness.csv")


def exp(budget, prop, field):
    return fnum([r for r in EXP if r["budget"] == str(budget) and r["property"] == prop][0][field])


def tmbx(budget, field):
    return fnum([r for r in TMBX if r["budget"] == str(budget)][0][field])


def abl(prop, model, field):
    return fnum([r for r in ABL if r["property"] == prop and r["model"] == model][0][field])


def ablr(prop, field):
    return fnum([r for r in ABLR if r["property"] == prop][0][field])


def perfold_triples(prop, model):
    return [(float(r["sel_a"]), float(r["sel_b"]), float(r["sel_g"])) for r in ABLF
            if r["property"] == prop and r["model"] == model]


def perfold_mode(prop, model):
    from collections import Counter
    return Counter(perfold_triples(prop, model)).most_common(1)[0]


def perfold_max_abs_gamma():
    return max(abs(float(r["sel_g"])) for r in ABLF if r["model"] == "LO")


BUDGETS = sorted({int(r["budget"]) for r in EXP})
SEEDS_EXP = sorted({int(r["seed"]) for r in EXP_RAW})

# --------------------------------------------------------------------------
# box sensitivity (external/box_sensitivity_summary.csv, box_sensitivity.csv)
# --------------------------------------------------------------------------
BOX = rows("external", "box_sensitivity_summary.csv")
BOX_RAW = rows("external", "box_sensitivity.csv")
BOX_SRC = text("external", "box_sensitivity.py")


def box(ds, prop, L, field):
    return fnum([r for r in BOX if r["dataset"] == ds and r["property"] == prop and r["L"] == str(L)][0][field])


BOX_L = sorted({int(r["L"]) for r in BOX})
BOX_SEEDS = sorted({int(r["seed"]) for r in BOX_RAW})
BOX_BUDGET = int(re.search(r"SEEDS, BUDGET, BOXES = range\(\d+\), (\d+),", BOX_SRC).group(1))
BOX_NSEEDS = int(re.search(r"SEEDS, BUDGET, BOXES = range\((\d+)\)", BOX_SRC).group(1))


def box_interior_pct_floor():
    """100*(1 - max parent edge fraction in the wide box), floored to the ten."""
    return math.floor(100 * (1 - max(float(r["GM_edge_frac"]) for r in BOX if r["L"] == "12")) / 10) * 10


# --------------------------------------------------------------------------
# nonane replication (external/*)
# --------------------------------------------------------------------------
NONV = rows("external", "nonane_validation_summary.csv")
NON_DATA = rows("external", "nonane_data.csv")
NON_PROV = rows("external", "nonane_provenance.csv")
BASE_O = rows("external", "baselines_octane.csv")
BASE_N = rows("external", "baselines_nonane.csv")
TRANS = rows("external", "transfer_exploratory_summary.csv")
UNC = rows("external", "uncertainty_exploratory.csv")
NONV_SRC = text("external", "nonane_validation.py")
UNC_SRC = text("external", "uncertainty_exploratory.py")


def nonv(prop, analysis_prefix, budget, field):
    return fnum([r for r in NONV if r["property"] == prop and r["analysis"].startswith(analysis_prefix)
                 and r["budget"] == str(budget)][0][field])


def base(which, prop, method, field="Q2"):
    rs = BASE_O if which == "oct" else BASE_N
    return fnum([r for r in rs if r["property"] == prop and r["method"] == method][0][field])


def trans(prop, budget, field):
    return fnum([r for r in TRANS if r["property"] == prop and r["budget"] == str(budget)][0][field])


def unc(ds, prop, budget, field):
    return fnum([r for r in UNC if r["dataset"] == ds and r["property"] == prop and r["budget"] == str(budget)][0][field])


def non_count(prop):
    return sum(1 for r in NON_DATA if r[prop].strip())


def non_dhvap_rule_count(kind):
    sel = [r["selection_rule"] for r in NON_PROV if r["property"] == "dHvap"]
    if kind == "calorimetric":
        return sum(1 for s in sel if "calorimetric (method C)" in s)
    if kind == "avg":
        return sum(1 for s in sel if s.startswith("NIST average"))
    if kind == "compilation":
        return sum(1 for s in sel if s.startswith("only one NIST"))


def tmp_tb_row():
    return [r for r in NON_PROV if r["name"] == "2,3,3,4-tetramethylpentane" and r["property"] == "T_B"][0]


def tmp_determinations():
    return [float(v) for v in re.findall(r"([\d.]+) K \(", tmp_tb_row()["all_determinations"])]


def corr_lo1_irla(which):
    if which == "oct":
        pl = OP
    else:
        pl = [alkane_pairs(r["smiles"]) for r in NON_DATA]
    return r_signed(np.array([lo_pairs(p, 0, 0, 1) for p in pl]), np.array([irla(p) for p in pl]))


N_BASELINES = len({r["method"] for r in BASE_N} - {m for m in {r["method"] for r in BASE_N} if m.startswith(("GM", "LO"))})
NONV_SEEDS = int(re.search(r"SEEDS, BUDGETS = range\((\d+)\)", NONV_SRC).group(1))
NONV_THRESH = int(re.search(r"min\(better\) >= (\d+)", NONV_SRC).group(1))
UNC_NB = int(re.search(r"NB, RNG_SEED = (\d+),", UNC_SRC).group(1))


def narrow_box_q2_range(kind):
    """kind='q2only': classical best + GM (b200) on both sets; kind='linear': IRLA,
    ridge, LO(0,0,1), LO (b200) on both sets; returns (min, max)."""
    if kind == "q2only":
        v = [base("oct", "dHvap", "fixed_best"), base("oct", "dHvap", "GM_b200"),
             base("non", "dHvap_kcal", "fixed_best"), base("non", "dHvap_kcal", "GM_b200")]
        # on the octanes the fixed-best for dHvap is LO(0,0,1); the classical best is
        # read from the ten reductions via the external table value 'fixed_best' only
        # when LO(0,0,1) is not admitted -- recompute from the octane classical set:
        v[0] = CLASSICAL_BEST_OCT_DHVAP
        v[2] = CLASSICAL_BEST_NON_DHVAP
    else:
        v = [base("oct", "dHvap", m) for m in ("IRLA", "ridge_counts", "fixed_best", "LO_b200")] + \
            [base("non", "dHvap_kcal", m) for m in ("IRLA", "ridge_counts", "fixed_best", "LO_b200")]
    return min(v), max(v)


# classical-best Q2 for dHvap: the external table's 'Class.' column.  For the
# octanes baselines_octane.csv 'fixed_best' admits LO(0,0,1) (selection
# "LO(0,0,1):18"), so the classical-only value is recomputed here by the same
# nested rule (best of the ten reductions by inner-LOO RMSE in each fold, OLS).
def _loo_pred(x, y):
    n = len(x); pr = np.empty(n)
    for i in range(n):
        m = np.ones(n, bool); m[i] = False; xi, yi = x[m], y[m]
        b = ((xi - xi.mean()) * (yi - yi.mean())).sum() / ((xi - xi.mean()) ** 2).sum()
        pr[i] = yi.mean() - b * xi.mean() + b * x[i]
    return pr


def _nested_classical_q2(pl, y):
    X = {nm: np.array([lo_pairs(p, *RED[nm]) for p in pl]) for nm in CLASSICAL}
    n = len(y); pred = np.empty(n)
    for i in range(n):
        m = np.ones(n, bool); m[i] = False
        best = min(CLASSICAL, key=lambda nm: np.sqrt(((_loo_pred(X[nm][m], y[m]) - y[m]) ** 2).mean()))
        xi, yi = X[best][m], y[m]
        b = ((xi - xi.mean()) * (yi - yi.mean())).sum() / ((xi - xi.mean()) ** 2).sum()
        pred[i] = yi.mean() - b * xi.mean() + b * X[best][i]
    return 1 - ((pred - y) ** 2).sum() / ((y - y.mean()) ** 2).sum()


CLASSICAL_BEST_OCT_DHVAP = _nested_classical_q2(OP, Y["dHvap"])
_non_ok = [r for r in NON_DATA if r["dHvap_kcal"].strip()]
CLASSICAL_BEST_NON_DHVAP = _nested_classical_q2([alkane_pairs(r["smiles"]) for r in _non_ok],
                                                np.array([float(r["dHvap_kcal"]) for r in _non_ok]))

# --------------------------------------------------------------------------
# boiling points (external/bp/*)
# --------------------------------------------------------------------------
BPS = rows("external", "bp", "bp_results_summary.csv")
BPB = rows("external", "bp", "bp_baselines.csv")
BPP = rows("external", "bp", "bp_provenance.csv")
BPD = rows("external", "bp", "bp_data.csv")
CAL = rows("external", "bp", "calorimetric_dHvap298_alkanes.csv")
COV = rows("external", "bp", "coverage_bias.csv")
BPT_SRC = text("external", "bp", "bp_tests.py")
CHANGELOG = text("V35_TO_V36_SCIENTIFIC_CHANGELOG.md")


def bps(test_prefix, field):
    return fnum([r for r in BPS if r["test"].startswith(test_prefix)][0][field])


def bpb(test_prefix, model, field="Q2"):
    return fnum([r for r in BPB if r["test"].startswith(test_prefix) and r["model"] == model][0][field])


def bp_single_index_range():
    v = [bpb("A", m) for m in ("classical best", "IRLA", "LO(0,0,1) fixed")] + \
        [bps("A", f) for f in ("median_Q2_GM2", "median_Q2_LO2", "median_Q2_GM12", "median_Q2_LOh")]
    return min(v), max(v)


def bpp_count(nC=None, status=None, rule_sub=None):
    return sum(1 for r in BPP if (nC is None or r["n_C"] == str(nC)) and (status is None or r["status"] == status)
               and (rule_sub is None or rule_sub in r["rule_or_reason"]))


def bpp_spread_threshold():
    return float(re.search(r"> (\d+) K", [r for r in BPP if "spread" in r["rule_or_reason"] and r["status"] == "EXCLUDED"][0]["rule_or_reason"]).group(1))


def bpp_excluded_nonane_spread():
    return float(re.search(r"spread ([\d.]+) K", [r for r in BPP if r["n_C"] == "9" and r["status"] == "EXCLUDED"][0]["rule_or_reason"]).group(1))


def nist_to_iupac(name):
    """'Hexane, 2,4-dimethyl-' -> '2,4-dimethylhexane'; 'Octane' -> 'octane';
    grouped NIST records ('A / B') use their first name."""
    name = name.split(" / ")[0].strip()
    if "," not in name:
        return name.lower()
    parent, subs = name.split(",", 1)
    return (subs.strip().rstrip("-") + parent.strip()).lower()


def bp_vs_octane_table():
    """(max |T_B difference|, list of (name, bp_value, table_value)) over the 18 octanes."""
    out = []
    for r in BPD:
        if r["n_C"] == "8":
            nm = nist_to_iupac(r["name"])
            out.append((nm, float(r["T_B_C"]), OCTANES[IDX[nm]][1]))
    assert len(out) == 18
    return max(abs(a - b) for _, a, b in out), {nm: (a, b) for nm, a, b in out}


def heptane_shift():
    """3-methylhexane: pooled mean of two NIST averages vs first page alone (deg C, half-up 0.1)."""
    r = [r for r in BPP if r["rule_or_reason"].startswith("mean of 2 NIST averages")][0]
    first_K = float(re.findall(r"([\d.]+) ± ", r["all_determinations"])[0])
    return abs(rnd(first_K - 273.15, 1) - float(r["T_B_C"]))


def cal_count(kind):
    if kind == "outside_c8_c9":
        return sum(1 for r in CAL if r["n"] not in ("8", "9"))
    if kind == "decanes":
        return sum(1 for r in CAL if r["n"] == "10")


def changelog_n101(field):
    m = re.search(r"n=101: ([\d.]+), ([\d.]+),\s*([-+\d.]+), (\d+)/50, \[([-+\d.]+),([-+\d.]+)\]", CHANGELOG)
    return {"gm": fnum(m.group(1)), "lo": fnum(m.group(2)), "dq2": fnum(m.group(3)),
            "wins": int(m.group(4)), "lo_ci": fnum(m.group(5)), "hi_ci": fnum(m.group(6))}[field]


BP_SEEDS = int(re.search(r"SEEDS, BUD = range\((\d+)\), (\d+)", BPT_SRC).group(1))
BP_BUDGET = int(re.search(r"SEEDS, BUD = range\((\d+)\), (\d+)", BPT_SRC).group(2))
BP_WINS = int(re.search(r"wins >= (\d+)", BPT_SRC).group(1))
BP_NBOOT = int(re.search(r"for _ in range\((\d+)\):", BPT_SRC).group(1))
BP_HW_PARENT = int(re.search(r"GM12 ~ U\(-(\d+),\s*\d+\)\^2", BPT_SRC).group(1))
BP_HW_GAMMA = int(re.search(r"LOh ~ \(U\(-\d+,\d+\)\^2, U\(-(\d+),\s*\d+\)\)", BPT_SRC).group(1))
N_DEG_PAIRS = len([(i, j) for i in range(1, 5) for j in range(i, 5)])   # degree-pair types, max degree 4

# --------------------------------------------------------------------------
# structural outputs (structural/structural_checks_out.txt)
# --------------------------------------------------------------------------
STRUCT = text("structural", "structural_checks_out.txt")


def struct_table():
    """S1 tree-order table: {(n, subset): (N, profiles, qhist)}."""
    out = {}
    for m in re.finditer(r"^\s+(\d+) (all|mol) (\d+) (\d+) (\d+) ", STRUCT, re.M):
        out[(int(m.group(1)), m.group(2))] = (int(m.group(3)), int(m.group(4)), int(m.group(5)))
    return out


def last_order_profiles_eq_qhist(subset):
    t = struct_table(); ns = sorted(n for n, s in t if s == subset)
    good = [n for n in ns if t[(n, subset)][1] == t[(n, subset)][2]]
    first_bad = min((n for n in ns if t[(n, subset)][1] != t[(n, subset)][2]), default=None)
    return max(n for n in good if first_bad is None or n < first_bad)


def first_order_profiles_ne_qhist(subset):
    t = struct_table()
    return min(n for n, s in t if s == subset and t[(n, s)][1] != t[(n, s)][2])


def struct_max_order():
    return max(n for n, s in struct_table())


def struct_num(pattern):
    return float(re.search(pattern, STRUCT).group(1))


HP = text("structural", "hp_counts_out.txt")


def hp_num(pattern):
    return float(re.search(pattern, HP).group(1))


N_DECANES = struct_table()[(10, "mol")][0]

# --------------------------------------------------------------------------
# the registry
# --------------------------------------------------------------------------
def E(id_, file_, pattern, expected, tol, note):
    return {"id": id_, "file": file_, "pattern": pattern, "expected": expected, "tol": tol, "note": note}


def non_tb_rule(prefix):
    """Number of nonane T_B rows of nonane_provenance.csv whose selection_rule starts with prefix."""
    with open(P("external", "nonane_provenance.csv"), newline="") as f:
        return sum(1 for r in csv.DictReader(f) if r["property"] == "T_B" and r["selection_rule"].startswith(prefix))


def api44_margin_m1_over_hm():
    """|r_alt(M1)| - |r_alt(HM)| on S after substituting the 1947 API-44 entropies."""
    r = {x["index"]: float(x["r_S_alternative"]) for x in rows("entropy_api44_sensitivity_v41.csv")}
    return abs(r["M1"]) - abs(r["HM"])


def tuning_dout(anchor, prop):
    """Nested gain LOO_50 - LOO_0 of Table S2 (rows of section E of
    verify_loyola_v35_results.csv, displayed at 3 decimals; the prose quotes
    some of these to 4 decimals, hence the wider tolerances)."""
    r = {x["item"]: float(x["computed"]) for x in rows("verify_loyola_v35_results.csv") if x["section"] == "E"}
    return r[f"{anchor}/{prop}/LOO50"] - r[f"{anchor}/{prop}/LOO0"]


def sweep_positive():
    import re as _re
    t = open(P("tuning_pool_seed_sweep_out.txt")).read()
    return int(_re.search(r"positive in (\d+) of 100 seeds", t).group(1))


REGISTRY = [
    E("s2_sweep97", "supp", r"positive\s+in\s+\$(?P<v>\d+)\$\s+of\s+\$100\$", "sweep_positive()", 0, "tuning_pool_seed_sweep_out.txt"),
    E("s2_dout_m2_omega", "supp", r"\$S\$,\s+\$LO\((?P<v>-?[\d.]+),\s+0,", "tuning_dout('M2', 'omega')", 0.0011, "verify_loyola_v35_results.csv E rows (3 dp)"),
    E("s2_dout_hm_s", "supp", r"\$\-0\.0003\$,\s+\$(?P<v>-?[\d.]+)\$\s+and", "tuning_dout('HM', 'S')", 0.0015, "verify_loyola_v35_results.csv E rows (3 dp): HM on S"),
    E("s2_dout_lo1_dhvap", "supp", r"\$S\$,\s+\$LO\(0,\s+(?P<v>-?[\d.]+),\s+1\)\$", "tuning_dout('LO(0,0,1)', 'dHvap')", 0.0011, "verify_loyola_v35_results.csv E rows (3 dp)"),
    # ======================= main.tex : abstract =======================

    # ======================= main.tex : sec:sensitivity intro =======================
    E("s6_n_oct", "main", r"reduces to on the \$(?P<v>\d+)\$ octane isomers, following", "N_OCT", 0, "octane_data.OCTANES"),
    E("s6_n_non", "main", r"The\s+\$(?P<v>\d+)\$\s+nonane", "len(NON_DATA)", 0, "external/nonane_data.csv rows"),
    E("s6_tuning_margin", "main", r"except by a \$(?P<v>[\d.]+)\$ in-sample", "tuning_margin_dhvap()", 0.0005,
      "S2 recipe (default_rng(42) pools): best tuned in-sample |r| on dHvap minus best fixed |r|, at display rounding"),

    # ======================= main.tex : sec:octanes =======================
    E("oct_n18_a", "main", r"properties\s+of\s+the\s+\$(?P<v>\d+)\$\s+octane\s+isomers\.\s+The",
      "N_OCT", 0, "octane_data.OCTANES"),
    E("oct_90values", "main", r"All\s+\$(?P<v>\d+)\$\s+molecule\-level", "len(PROV)", 0, "octane_property_provenance_v35.csv rows"),
    E("oct_298_a", "main", r"Three caveats remain\. The \$(?P<v>\d+)\$\\,K vaporization", None, 0, "UNCHECKABLE: thermodynamic reference temperature (condition constant)"),
    E("oct_298_b", "main", r"2,2,3,3-tetramethylbutane, a solid at \$(?P<v>\d+)\$\\,K \(triple point", None, 0, "UNCHECKABLE: condition constant"),
    E("oct_triple374", "main", r"\(triple point\s+\$(?P<v>\d+)\$\\,K\), is the benchmark-compilation value", "rnd(TMB_TRIPLE_K,0)", 0,
      "provenance TMB dHvap source_value 'triple point 373.97 K'"),
    E("oct_tmb_841", "main", r"is the benchmark-compilation value \$(?P<v>[\d.]+)\$\\,kcal", "OCTANES[IDX[TMB]][3]", 0, "octane_data TMB dHvap"),
    E("oct_tmb_3519", "main", r"\$8\.41\$\\,kcal\\,mol\$\^\{\-1\}\$\s+\(\$(?P<v>[\d.]+)\$\\,kJ\\,mol\$\^\{\-1\}\$\)\.\s+This", "OCTANES[IDX[TMB]][3]*4.184", 0.005, "8.41 kcal x 4.184"),
    E("oct_tmb_4294", "main", r"enthalpies\s+\(\$(?P<v>[\d.]+)\$\s+and", "TMB_DHVAP_KJ[0]", 0, "provenance TMB dHvap source_value (Majer & Svoboda)"),
    E("oct_tmb_4291", "main", r"\(\$42\.94\$ and \$(?P<v>[\d.]+)\$\\,kJ", "TMB_DHVAP_KJ[1]", 0, "provenance TMB dHvap source_value (Osborne & Ginnings)"),
    E("oct_tmb_1026", "main", r"about\s+\$(?P<v>[\d.]+)\$\\,kcal\\,mol\$\^\{-1\}\$\), so its physical", "TMB_DHVAP_KJ[0]/4.184", 0.005, "42.94/4.184 (42.91/4.184 also rounds to the same)"),
    E("oct_six_S", "main", r"is\s+unresolved\.\s+(?P<v>Six)\s+gas\-phase\s+entropies",
      "word(prov_count('CANNOT VERIFY','S'), True)", 0, "provenance: S rows CANNOT VERIFY"),
    E("oct_api44_22", "main", r"to\s+\$(?P<v>[\d.]+)\$\s+units\.", "max(API44_DIFFS)", 0.05,
      "provenance notes: API-44 S values vs values used (3,4-dimethylhexane 106.59 vs 104.38)"),
    E("oct_four_S", "main", r"and (?P<v>four) entropies\s+differ\s+from a widely used compilation", "word(len(S_ALT))", 0, "S_ALT (4 alternative entropies)"),
    E("oct_twelve_S", "main", r"changes all (?P<v>twelve) \$S\$ correlations \(by up to", "word(len(S_SENS))", 0, "entropy_source_sensitivity_v36.csv rows"),
    E("oct_S_change043", "main", r"\(by up to \$(?P<v>[\d.]+)\$ in \$\|r\|\$\)\s+and moves the margin between \$HM\$", "max_abs_change(S_SENS)", 0.0005, "entropy_source_sensitivity_v36.csv max ||r_alt|-|r_orig||"),
    E("oct_S_margin001", "main", r"top\s+from\s+\$(?P<v>[\d.]+)\$\s+to\s+\$0\.007\$\.", "s_margin()", 0.0005,
      "|r_HM|-|r_M1| on S with the ORIGINAL data (0.00103); reading as 'the top-two margin on the original data'"),
    E("oct_S_margin007_alt", "main", r"to\s+\$(?P<v>[\d.]+)\$\.\s+Margins", "s_margin_alt_csv()", 0.0005,
      "AUDIT: literal reading (margin AFTER substituting the compilation values) = |−0.9612|−|−0.9541| = 0.0071 from entropy_source_sensitivity_v36.csv; the sentence's 0.001 holds only for the original data"),
    E("oct_M2_omega_orig", "main", r"\(e\.g\.\\ \$M_2\$ from \$(?P<v>-?[\d.]+)\$ to \$-0\.986\$\)", "W_SENS['M2'][0]", 0.0005, "omega_source_sensitivity_v35.csv M2 original"),
    E("oct_M2_omega_alt", "main", r"from \$-0\.988\$ to \$(?P<v>-?[\d.]+)\$\)\s+and leave the \$\\omega\$", "W_SENS['M2'][1]", 0.0005, "omega_source_sensitivity_v35.csv M2 alternative"),
    E("tab4cap_n18", "main", r"properties of the \$(?P<v>\d+)\$ octane isomers\. Bold flags", "N_OCT", 0, "octane_data"),
    E("tab4cap_margin_lo", "main", r"are\s+\$(?P<v>[\d.]+)\$\-\-\$0\.032\$,\s+and", "min(margins_all())", 0.0005, "top-two |r| margins per property (min), octane_data"),
    E("tab4cap_margin_hi", "main", r"are\s+\$0\.001\$\-\-\$(?P<v>[\d.]+)\$,\s+and", "max(margins_all())", 0.0005, "top-two |r| margins per property (max)"),
    E("oct_r984", "main", r"\(\$\|r\| = (?P<v>[\d.]+)\$, with\s+\$LO\(0, 0, 2\)\$ second at", "abs(r_tab4('LO(0,0,1)','dHvap'))", 0.0005, "octane_data correlation"),
    E("oct_r981", "main", r"at\s+\$(?P<v>[\d.]+)\$\),\s+and", "abs(r_tab4('LO(0,0,2)','dHvap'))", 0.0005, "octane_data correlation"),
    E("oct_del027", "main", r"most\s+\$(?P<v>[\d.]+)\$\s+\(bootstrap", "deletion_influence_max()", 0.0005, "deletion influence over bolded cells (verify [C] recipe)"),
    E("oct_n18_b", "main", r"twelve highly correlated sample\s+correlations on \$(?P<v>\d+)\$ molecules", "N_OCT", 0, "octane_data"),
    E("oct_collin982", "main", r"\(maximum \$\|r\|\$ with a reduction equal to\s+\$(?P<v>[\d.]+)\$ for \$LO\(0, 0, 1\)\$", "max_abs_corr_with_classical('LO001')", 0.0005, "descriptor_correlations.csv"),
    E("oct_collin993", "main", r"and \$(?P<v>[\d.]+)\$ for \$LO\(0, 0, 2\)\$\)\.", "max_abs_corr_with_classical('LO002')", 0.0005, "descriptor_correlations.csv"),
    E("oct_fourteen", "main", r"than\s+tests\.\s+(?P<v>Fourteen)\s+of\s+the", "word(n_pairs_ge(0.99), True)", 0, "descriptor_correlations.csv pairs with |r|>=0.99"),
    E("oct_pca9905", "main", r"carry\s+\$(?P<v>[\d.]+)\\%\$ of the variance \(Supplementary Section~S1\)", "100*pca_cumvar(2)", 0.005, "pca_spectrum.csv cumvar component 2"),
    E("oct_n18_c", "main", r"the \$(?P<v>\d+)\$ isomers realise only \$16\$", "N_OCT", 0, "octane_data"),
    E("oct_16profiles", "main", r"the \$18\$ isomers realise only \$(?P<v>\d+)\$ distinct edge-degree-pair", "n_distinct_profiles()", 0, "distinct degree-pair multisets of the 18 octanes"),
    E("oct_two_pairs", "main", r"\\centering\s+\\caption\{The\s+(?P<v>two)\s+degree\-pair\s+collision", "word(n_collision_pairs())", 0, "profiles shared by exactly two octanes"),
    E("oct_tb12", "main", r"to\s+\$(?P<v>[\d.]+)\\,\^\{\\circ\}\$C\s+in", "collision_tb_diff(0)", 0.05, "bid_collision_table.csv P03 pair T_B difference"),
    E("oct_tb21", "main", r"first pair and\s+\$(?P<v>[\d.]+)\\,\^\{\\circ\}\$C within the second", "collision_tb_diff(1)", 0.05, "bid_collision_table.csv P09 pair T_B difference"),

    # ======================= main.tex : sec:ablation =======================
    E("abl_onehundred", "main", r"seed\s+over\s+(?P<v>one hundred)\s+candidate\s+streams\.", "word(int(exp(200,'dHvap','n_seeds')))", 0, "expanded_robustness_summary_v35.csv n_seeds"),
    E("abl_100of100_a", "main", r"was\s+\$(?P<v>\d+)/100\$\s+at", "exp(200,'dHvap','LO_better')", 0, "expanded_robustness_summary_v35.csv dHvap b200 LO_better"),
    E("abl_100of100_b", "main", r"was\s+\$100/(?P<v>\d+)\$\s+at", "exp(200,'dHvap','n_seeds')", 0, "n_seeds"),
    E("abl_b200", "main", r"budgets\s+\$(?P<v>\d+)\$\s+and", "BUDGETS[0]", 0, "budgets in expanded_robustness_summary_v35.csv"),
    E("abl_b500", "main", r"and\s+\$(?P<v>\d+)\$,\s+with", "BUDGETS[1]", 0, "budgets"),
    E("abl_med069", "main", r"\$\\Delta\s+Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\s+and\s+\$\+0\.068\$,", "exp(200,'dHvap','dQ2_median')", 0.0005, "dQ2_median b200"),
    E("abl_med068", "main", r"and\s+\$(?P<v>[+-]?[\d.]+)\$,\s+whereas", "exp(500,'dHvap','dQ2_median')", 0.0005, "dQ2_median b500"),
    E("abl_tmb93", "main", r"to\s+\$(?P<v>\d+)/100\$\s+and", "tmbx(200,'LO_better')", 0, "dhvap_tmb_exclusion_summary_v36.csv"),
    E("abl_tmb96", "main", r"and\s+\$(?P<v>\d+)/100\$\s+\(Supplementary", "tmbx(500,'LO_better')", 0, "dhvap_tmb_exclusion_summary_v36.csv"),
    E("abl_n18_fixed", "main", r"of\s+\$(?P<v>\d+)\$\s+molecules\.", "N_OCT", 0, "octane_data"),
    E("abl_three_triples", "main", r"search chose (?P<v>three) distinct triples over the \$18\$", "word(len(set(perfold_triples('dHf','LO'))))", 0, "ablation_perfold.csv dHf LO distinct triples"),
    E("abl_18folds_a", "main", r"distinct triples over the \$(?P<v>\d+)\$\s+folds, whereas", "len(perfold_triples('dHf','LO'))", 0, "ablation_perfold.csv folds"),
    E("abl_alpha1021", "main", r"the parent chose\s+\$\(\\alpha,\\beta\) = \((?P<v>[\d.]+), -1\.993\)\$, on the boundary of the box, in \$16\$", "perfold_mode('dHvap','GM')[0][0]", 0.0005, "ablation_perfold.csv dHvap GM modal alpha"),
    E("abl_beta1993", "main", r"= \(1\.021, (?P<v>-?[\d.]+)\)\$, on the boundary of the box, in \$16\$", "perfold_mode('dHvap','GM')[0][1]", 0.0005, "modal beta"),
    E("abl_16of18_a", "main", r"on the boundary of the box, in \$(?P<v>\d+)\$\s+of the \$18\$ folds", "perfold_mode('dHvap','GM')[1]", 0, "count of modal pair"),
    E("abl_16of18_b", "main", r"in \$16\$\s+of the \$(?P<v>\d+)\$ folds\.", "len(perfold_triples('dHvap','GM'))", 0, "folds"),
    E("abl_2000", "main", r"with\s+\$(?P<v>\d+)\$\s+candidates", "BOX_BUDGET", 0, "box_sensitivity.py BUDGET"),
    E("abl_seeds49", "main", r"candidates per model, seeds \$0\$--\$(?P<v>\d+)\$, and boxes of half-width", "max(BOX_SEEDS)", 0, "box_sensitivity.csv seeds"),
    E("abl_hw2", "main", r"boxes of half-width \$(?P<v>\d+)\$\s+and \$12\$ for both models", "BOX_L[0]", 0, "box_sensitivity_summary.csv L"),
    E("abl_hw12", "main", r"half-width \$2\$\s+and \$(?P<v>\d+)\$ for both models", "BOX_L[1]", 0, "L"),
    E("abl_interior90", "main", r"interior in more than\s+\$(?P<v>\d+)\\%\$ of folds for every property", "box_interior_pct_floor()", 0,
      "100*(1-max GM_edge_frac at L=12) = 90.5, floored to a multiple of 10"),
    E("abl_hyb004", "main", r"gives median \$\\Delta Q\^2 = (?P<v>[+-]?[\d.]+)\$ on the octanes\s+\(\$28\$ of \$50\$ seeds\)", "box('octane','dHvap',12,'median_dQ2_hybrid')", 0.0005, "box_sensitivity_summary.csv"),
    E("abl_hyb28", "main", r"on the octanes\s+\(\$(?P<v>\d+)\$ of \$50\$ seeds\) and \$-0\.002\$", "box('octane','dHvap',12,'LO_hybrid_better')", 0, "LO_hybrid_better"),
    E("abl_hyb50a", "main", r"\(\$28\$ of \$(?P<v>\d+)\$ seeds\) and", "box('octane','dHvap',12,'n_seeds')", 0, "n_seeds"),
    E("abl_hyb002", "main", r"seeds\) and \$(?P<v>[+-]?[\d.]+)\$ on the nonanes \(\$24\$ of \$50\$\)", "box('nonane','dHvap',12,'median_dQ2_hybrid')", 0.0005, "box_sensitivity_summary.csv"),
    E("abl_hyb24", "main", r"nonanes\s+\(\$(?P<v>\d+)\$\s+of", "box('nonane','dHvap',12,'LO_hybrid_better')", 0, "LO_hybrid_better"),
    E("abl_wide011", "main", r"gives\s+\$(?P<v>[+-]?[\d.]+)\$\s+and", "box('octane','dHvap',12,'median_dQ2')", 0.0005, "median_dQ2 L=12 octane dHvap"),
    E("abl_wide016", "main", r"and\s+\$(?P<v>[+-]?[\d.]+)\$,\s+while", "box('nonane','dHvap',12,'median_dQ2')", 0.0005, "median_dQ2 L=12 nonane dHvap"),
    E("abl_S38", "main", r"ahead for octane \$S\$ \(\$(?P<v>\d+)\$ of \$50\$\s+seeds\)", "box('octane','S',12,'LO_hybrid_better')", 0, "LO_hybrid_better"),
    E("abl_TB31", "main", r"\$T_B\$\s+\(\$(?P<v>\d+)\$\s+of", "box('nonane','T_B',12,'LO_hybrid_better')", 0, "LO_hybrid_better"),
    E("abl_gm887", "main", r"\(\$(?P<v>[\d.]+) \\to 0\.942\$ on the octanes\)", "box('octane','dHvap',2,'median_Q2_GM')", 0.0005, "median_Q2_GM L=2"),
    E("abl_gm942", "main", r"\(\$0\.887 \\to (?P<v>[\d.]+)\$ on the octanes\)", "box('octane','dHvap',12,'median_Q2_GM')", 0.0005, "median_Q2_GM L=12"),
    E("abl_lo957", "main", r"less efficient there \(\$(?P<v>[\d.]+)\s+\\to 0\.946\$ for the hybrid control\)", "box('octane','dHvap',2,'median_Q2_LO')", 0.0005, "median_Q2_LO L=2"),
    E("abl_loh946", "main", r"\\to (?P<v>[\d.]+)\$ for the hybrid control\)", "box('octane','dHvap',12,'median_Q2_LO_hybrid')", 0.0005, "median_Q2_LO_hybrid L=12"),
    E("abl_a45", "main", r"\$\(\\alpha,\\beta\) \\approx \((?P<v>[\d.]+), -9\)\$ \(\$Q\^2 = 0\.957\$", r"struct_num(r'fixed \(([\d.]+), -9\.0, 0\.0\)')", 0, "structural_checks_out.txt S6 fixed point"),
    E("abl_b9", "main", r"\\approx \(4\.5, (?P<v>-?\d+)\)\$ \(\$Q\^2", r"struct_num(r'fixed \(4\.5, (-[\d.]+), 0\.0\)')", 0, "structural_checks_out.txt S6"),
    E("abl_q957", "main", r"\(\$Q\^2 = (?P<v>[\d.]+)\$ and \$0\.948\$ against", r"struct_num(r'fixed \(0\.0, 0\.0, 1\.0\): ([\d.]+)')", 0.0005, "structural_checks_out.txt S6 LOO Q2 of LO(0,0,1)"),
    E("abl_q948", "main", r"= 0\.957\$ and \$(?P<v>[\d.]+)\$ against\s+\$0\.949\$", "base('oct','dHvap','IRLA')", 0.0005, "baselines_octane.csv IRLA dHvap"),
    E("abl_q949", "main", r"against\s+\$(?P<v>[\d.]+)\$ there, on the octanes\)", r"struct_num(r'fixed \(4\.5, -9\.0, 0\.0\): ([\d.]+)')", 0.0005, "structural_checks_out.txt S6"),
    E("tab5cap_n18", "main", r"\$n\s+=\s+(?P<v>\d+)\$\.\s+Non\.:", "N_OCT", 0, "octane_data"),
    E("tab5cap_edge10", "main", r"lies within \$(?P<v>\d+)\\%\$ of the boundary", None, 0, "UNCHECKABLE: edge-share definition constant of box_sensitivity.py (not exposed as a literal 10)"),
    E("tab5cap_seeds49", "main", r"over\s+seeds\s+\$0\$\-\-\$(?P<v>\d+)\$\s+at\s+\$2000\$", "max(BOX_SEEDS)", 0, "box_sensitivity.csv"),
    E("tab5cap_2000", "main", r"\$0\$\-\-\$49\$\s+at\s+\$(?P<v>\d+)\$\s+candidates\s+per", "BOX_BUDGET", 0, "box_sensitivity.py"),
    E("tab5cap_of50", "main", r"the number of seeds \(of \$(?P<v>\d+)\$\) in which LO\s+beats GM \(half-width \$2\$\)", "BOX_NSEEDS", 0, "box_sensitivity.py"),
    E("tab5cap_hw2", "main", r"beats GM \(half-width \$(?P<v>\d+)\$\) or LO\$_h\$", "BOX_L[0]", 0, "L"),
    E("tab5cap_hw12", "main", r"or LO\$_h\$ beats GM \(half-width \$(?P<v>\d+)\$\)", "BOX_L[1]", 0, "L"),

    # ======================= main.tex : sec:external =======================
    E("ext_n35", "main", r"the\s+\$(?P<v>\d+)\$\s+constitutional", "len(NON_DATA)", 0, "nonane_data.csv"),
    E("ext_tb35", "main", r"were\s+\$(?P<v>\d+)\$\s+values:", "non_count('T_B_C')", 0,
      "nonane_data.csv non-blank T_B (NOTE: README_nonane_data.md says only 20 of the 35 are NIST averages; 5 single determinations, 10 'most recent' picks)"),
    E("ext_tb_avg20", "main", r"values:\s+\$(?P<v>\d+)\$\s+NIST", "non_tb_rule('NIST average')", 0, "nonane_provenance.csv T_B rows whose selection_rule starts 'NIST average'"),
    E("ext_tb_single5", "main", r"NIST averages, \$(?P<v>\d+)\$ single determinations", "non_tb_rule('single NIST')", 0, "nonane_provenance.csv T_B rows 'single NIST Tboil determination'"),
    E("ext_tb_d1_10", "main", r"single determinations and \$(?P<v>\d+)\$ most recent\s+determinations", "non_tb_rule('no NIST AVG')", 0, "nonane_provenance.csv T_B rows 'no NIST AVG; most recent primary experimental determination'"),
    E("ext_dhvap34", "main", r"enthalpies\s+were\s+\$(?P<v>\d+)\$\s+values\s+from", "non_count('dHvap_kcal')", 0, "nonane_data.csv non-blank dHvap"),
    E("ext_cal4", "main", r"Only\s+\$(?P<v>\d+)\$\s+of", "non_dhvap_rule_count('calorimetric')", 0, "nonane_provenance.csv selection_rule"),
    E("ext_cal_of34", "main", r"the\s+\$(?P<v>\d+)\$\s+vaporization", "non_count('dHvap_kcal')", 0, "nonane_data.csv"),
    E("ext_comp29", "main", r"and \$(?P<v>\d+)\$ come from two\s+compilations", "non_dhvap_rule_count('compilation')", 0, "nonane_provenance.csv 'only one NIST entry' rows"),
    E("ext_95", "main", r"in\s+\$(?P<v>\d+)/100\$\s+and", "nonv('dHvap','primary',200,'LO_better')", 0, "nonane_validation_summary.csv"),
    E("ext_98", "main", r"and\s+\$(?P<v>\d+)/100\$\s+seeds", "nonv('dHvap','primary',500,'LO_better')", 0, "nonane_validation_summary.csv"),
    E("ext_med048", "main", r"\$\\Delta\s+Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\s+and\s+\$\+0\.053\$\.", "nonv('dHvap','primary',200,'median_dQ2')", 0.0005, "median_dQ2"),
    E("ext_med053", "main", r"and\s+\$(?P<v>[+-]?[\d.]+)\$\.\s+For", "nonv('dHvap','primary',500,'median_dQ2')", 0.0005, "median_dQ2"),
    E("ext_tb58", "main", r"\\emph\{mixed\}\s+\(\$(?P<v>\d+)/100\$\s+and", "nonv('T_B','primary',200,'LO_better')", 0, "nonane_validation_summary.csv"),
    E("ext_tb63", "main", r"\(\$58/100\$ and \$(?P<v>\d+)/100\$\)\. The pre-registered protocol", "nonv('T_B','primary',500,'LO_better')", 0, "nonane_validation_summary.csv"),
    E("ext_hyb002", "main", r"Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\s+under", "box('nonane','dHvap',12,'median_dQ2_hybrid')", 0.0005, "box_sensitivity_summary.csv"),
    E("ext_lo1_957", "main", r"model\s+\(\$(?P<v>[\d.]+)\$\s+and", "base('oct','dHvap','fixed_best')", 0.0005, "baselines_octane.csv fixed_best dHvap (= LO(0,0,1) in all folds)"),
    E("ext_lo1_903", "main", r"\(\$0\.957\$ and \$(?P<v>[\d.]+)\$ against\s+medians \$0\.953\$ and \$0\.900\$\)\. It is", "base('non','dHvap_kcal','fixed_best')", 0.0005, "baselines_nonane.csv fixed_best dHvap (= LO(0,0,1):34)"),
    E("ext_lo_953", "main", r"medians \$(?P<v>[\d.]+)\$ and \$0\.900\$\)\. It is closely related to \$IRLA\$:", "base('oct','dHvap','LO_b200')", 0.0005, "baselines_octane.csv LO_b200"),
    E("ext_lo_900", "main", r"medians \$0\.953\$ and \$(?P<v>[\d.]+)\$\)\. It is closely related to \$IRLA\$:", "base('non','dHvap_kcal','LO_b200')", 0.0005, "baselines_nonane.csv LO_b200"),
    E("ext_corr996_oct", "main", r"two\s+is\s+\$(?P<v>[\d.]+)\$\s+on\s+both", "corr_lo1_irla('oct')", 0.0005, "corr(LO(0,0,1), IRLA) on the octanes (octane_data)"),
    E("ext_corr996_non", "main", r"two\s+is\s+\$(?P<v>[\d.]+)\$\s+on\s+both", "corr_lo1_irla('non')", 0.0005, "corr(LO(0,0,1), IRLA) on the nonanes (nonane_data.csv smiles)"),
    E("ext_irla_003", "main", r"comes within \$(?P<v>[\d.]+)\$ of the median Loyola model on the nonanes \(\$0\.897\$", "base('non','dHvap_kcal','LO_b200')-base('non','dHvap_kcal','IRLA')", 0.0005, "baselines_nonane.csv LO_b200 - IRLA"),
    E("ext_irla_897", "main", r"nonanes\s+\(\$(?P<v>[\d.]+)\$\s+against", "base('non','dHvap_kcal','IRLA')", 0.0005, "baselines_nonane.csv IRLA"),
    E("ext_lo_900b", "main", r"against\s+\$(?P<v>[\d.]+)\$\)\.\s+What", "base('non','dHvap_kcal','LO_b200')", 0.0005, "baselines_nonane.csv LO_b200"),
    E("ext_ridge927", "main", r"\(\$Q\^2\s+=\s+(?P<v>[\d.]+)\$\s+for", "base('non','dHvap_kcal','ridge_counts')", 0.0005, "baselines_nonane.csv ridge"),
    E("ext_ridge682", "main", r"H_\{\\mathrm\{vap\}\}\$,\s+\$(?P<v>[\d.]+)\$\s+for", "base('non','T_B_C','ridge_counts')", 0.0005, "baselines_nonane.csv ridge"),
    E("ext_95pct", "main", r"and its \$(?P<v>\d+)\\%\$ interval for LO minus GM on nonane", None, 0, "UNCHECKABLE: confidence level (protocol constant)"),
    E("ext_ci_lo", "main", r"\$\[(?P<v>-?[\d.]+), \+0\.113\]\$ at budget \$200\$, includes", "unc('nonane','dHvap',200,'ci95_lo')", 0.0005, "uncertainty_exploratory.csv"),
    E("ext_ci_hi", "main", r"\$\[-0\.006, (?P<v>[+-]?[\d.]+)\]\$ at budget \$200\$", "unc('nonane','dHvap',200,'ci95_hi')", 0.0005, "uncertainty_exploratory.csv"),
    E("ext_ci_b200", "main", r"\+0\.113\]\$ at budget \$(?P<v>\d+)\$, includes\s+zero", "BUDGETS[0]", 0, "budget"),
    E("tab6cap_n18", "main", r"on the octanes \(oct\., \$n = (?P<v>\d+)\$\) and\s+the nonane replication set", "N_OCT", 0, "octane_data"),
    E("tab6cap_n35", "main", r"\(non\., \$n = (?P<v>\d+)\$ for \$T_B\$, \$34\$ for", "non_count('T_B_C')", 0, "nonane_data.csv"),
    E("tab6cap_n34", "main", r"for \$T_B\$, \$(?P<v>\d+)\$ for\s+\$\\Delta H_\{\\mathrm\{vap\}\}\$\)\. Mean:", "non_count('dHvap_kcal')", 0, "nonane_data.csv"),
    E("tab6cap_ten", "main", r"Class\.: best of the\s+(?P<v>ten) classical indices, selected inside each fold", "word(len(CLASSICAL))", 0, "ten exact reductions"),
    E("tab6cap_seeds99", "main", r"over seeds \$0\$--\$(?P<v>\d+)\$ at budget \$200\$ in the box of half-width \$2\$", "max(SEEDS_EXP)", 0, "expanded_robustness_v35.csv seeds"),
    E("tab6cap_b200", "main", r"at budget \$(?P<v>\d+)\$ in the box of half-width \$2\$\s+\(see Table", "BUDGETS[0]", 0, "budget"),
    E("tab6cap_b200b", "main", r"LO beat GM at budgets \$(?P<v>\d+)\$/\$500\$\.", "BUDGETS[0]", 0, "budget"),
    E("tab6cap_b500", "main", r"at budgets \$200\$/\$(?P<v>\d+)\$\.", "BUDGETS[1]", 0, "budget"),

    # ======================= main.tex : sec:bp =======================
    E("bp_298", "main", r"standard-state \$(?P<v>\d+)\$\\,K determination \(NIST averaged", None, 0, "UNCHECKABLE: condition constant"),
    E("bp_cal25", "main", r"NIST lists only \$(?P<v>\d+)\$\s+acyclic alkane skeletons outside", "cal_count('outside_c8_c9')", 0, "calorimetric_dHvap298_alkanes.csv rows with n not in {8,9}"),
    E("bp_cal_one", "main", r"\$C_9\$,\s+and\s+(?P<v>one)\s+of\s+the", "word(cal_count('decanes'))", 0, "calorimetric_dHvap298_alkanes.csv n=10 rows"),
    E("bp_75decanes_a", "main", r"of\s+the\s+\$(?P<v>\d+)\$\s+decanes,\s+with", "bpp_count(10)", 0, "bp_provenance.csv decane rows (= 75 molecular trees of order 10)"),
    E("bp_two_days", "main", r"archived (?P<v>two) days earlier", None, 0, "UNCHECKABLE: calendar statement (git/PREREG dates)"),
    E("bp_3K_a", "main", r"within\s+\$(?P<v>\d+)\$\\,K,\s+and", "bpp_spread_threshold()", 0, "bp_provenance.csv exclusion reasons 'spread X K > 3 K'"),
    E("bp_34non", "main", r"and\s+\$(?P<v>\d+)\$\s+of", "bpp_count(9,'INCLUDED')", 0, "bp_provenance.csv"),
    E("bp_35non", "main", r"the\s+\$(?P<v>\d+)\$\s+nonanes,", "bpp_count(9)", 0, "bp_provenance.csv nonane rows"),
    E("bp_64K", "main", r"by\s+\$(?P<v>[\d.]+)\$\\,K\.\s+It", "bpp_excluded_nonane_spread()", 0.05, "bp_provenance.csv excluded nonane spread"),
    E("bp_34dec", "main", r"gives\s+\$(?P<v>\d+)\$\s+of", "bpp_count(10,'INCLUDED')", 0, "bp_provenance.csv"),
    E("bp_75decanes_b", "main", r"of\s+the\s+\$(?P<v>\d+)\$\s+decanes,\s+because", "bpp_count(10)", 0, "bp_provenance.csv"),
    E("bp_31nobp", "main", r"because\s+\$(?P<v>\d+)\$\s+of", "bpp_count(10,'EXCLUDED','no NIST boiling point')", 0, "bp_provenance.csv"),
    E("bp_10spread", "main", r"and \$(?P<v>\d+)\$ have determinations more than \$3\$\\,K apart", "bpp_count(10,'EXCLUDED','spread')", 0, "bp_provenance.csv"),
    E("bp_3K_b", "main", r"than\s+\$(?P<v>\d+)\$\\,K\s+apart\.", "bpp_spread_threshold()", 0, "bp_provenance.csv"),
    E("bp_14single", "main", r"For\s+\$(?P<v>\d+)\$\s+of", "bpp_count(10,'INCLUDED','median of 1 non-compilation')", 0, "bp_provenance.csv"),
    E("bp_34dec_b", "main", r"the\s+\$(?P<v>\d+)\$\s+included", "bpp_count(10,'INCLUDED')", 0, "bp_provenance.csv"),
    E("bp_oct_diff05", "main", r"to\s+\$(?P<v>[\d.]+)\\,\^\{\\circ\}\$C,\s+for", "bp_vs_octane_table()[0]", 0.05, "bp_data.csv C8 vs octane_data T_B, max |diff|"),
    E("bp_24dmh_1089", "main", r"at\s+\$(?P<v>[\d.]+)\$\s+against", "bp_vs_octane_table()[1]['2,4-dimethylhexane'][0]", 0.05, "bp_data.csv"),
    E("bp_24dmh_1094", "main", r"against \$(?P<v>[\d.]+)\\,\^\{\\circ\}\$C, a documented\s+source variation", "OCTANES[IDX['2,4-dimethylhexane']][1]", 0.05, "octane_data"),
    E("bp_p010", "main", r"\$p\s+\\ge\s+(?P<v>[\d.]+)\$\s+in", "math.floor(100*min(float(r['perm_p_two_sided']) for r in COV))/100", 0.005, "coverage_bias.csv min p (0.1033) floored to 2 dp"),
    E("bp_cov34", "main", r"with\s+\$(?P<v>\d+)\$\s+and", "int(COV[0]['n_included'])", 0, "coverage_bias.csv"),
    E("bp_cov41", "main", r"with \$34\$ and \$(?P<v>\d+)\$\s+molecules such tests", "int(COV[0]['n_excluded'])", 0, "coverage_bias.csv"),
    E("bp_pool100", "main", r"Test~B pools all\s+\$(?P<v>\d+)\$ molecules and adds the carbon number", "len(BPD)", 0, "bp_data.csv"),
    E("bp_box12", "main", r"over \$\(\\alpha,\\beta\) \\in \(-12,(?P<v>\d+)\)\^2\$ and the Loyola model", "BP_HW_PARENT", 0, "bp_tests.py docstring U(-12,12)"),
    E("bp_gamma2", "main", r"\\in\s+\(\-12,12\)\^(?P<v>\d+)\$\s+and", "BP_HW_GAMMA", 0, "bp_tests.py docstring gamma ~ U(-2,2)"),
    E("bp_2000", "main", r"\(\-2,2\)\$,\s+at\s+\$(?P<v>\d+)\$\s+candidates\s+and", "BP_BUDGET", 0, "bp_tests.py BUD"),
    E("bp_seeds49", "main", r"seeds\s+\$0\$\-\-\$(?P<v>\d+)\$\.\s+The", "BP_SEEDS-1", 0, "bp_tests.py SEEDS = range(50)"),
    E("bp_wins40", "main", r"required at least \$(?P<v>\d+)\$ wins in \$50\$ seeds", "BP_WINS", 0, "bp_tests.py decision rule"),
    E("bp_of50", "main", r"wins in \$(?P<v>\d+)\$ seeds and a molecule-bootstrap", "BP_SEEDS", 0, "bp_tests.py"),
    E("tab7cap_seeds49", "main", r"LO: medians over seeds \$0\$--\$(?P<v>\d+)\$ in the non-truncating boxes", "BP_SEEDS-1", 0, "bp_tests.py"),
    E("tab7cap_of50", "main", r"seeds \(of \$(?P<v>\d+)\$\) in\s+which LO beats GM\.\}", "BP_SEEDS", 0, "bp_tests.py"),
    E("bp_A_dq2", "main", r"Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$,\s+LO", "bps('A','median_dQ2_LOh_GM12')", 0.0005, "bp_results_summary.csv"),
    E("bp_A_15", "main", r"ahead\s+in\s+\$(?P<v>\d+)\$\s+of\s+\$50\$", "bps('A','LOh_better_of_50')", 0, "bp_results_summary.csv"),
    E("bp_A_of50", "main", r"of\s+\$(?P<v>\d+)\$\s+seeds,", "BP_SEEDS", 0, "bp_tests.py"),
    E("bp_A_95", "main", r"seeds, and the \$(?P<v>\d+)\\%\$ interval is \$\[-0\.156", None, 0, "UNCHECKABLE: confidence level"),
    E("bp_A_ci_lo", "main", r"is\s+\$\[(?P<v>-?[\d.]+),\s+\+0\.001\]\$\.", "bps('A','ci95_lo')", 0.0005, "bp_results_summary.csv"),
    E("bp_A_ci_hi", "main", r"is\s+\$\[\-0\.156,\s+(?P<v>[+-]?[\d.]+)\]\$\.\s+In", "bps('A','ci95_hi')", 0.0005, "bp_results_summary.csv"),
    E("bp_B_dq2", "main", r"are\s+\$(?P<v>[+-]?[\d.]+)\$,\s+\$25\$", "bps('B','median_dQ2_LOh_GM12')", 0.0005, "bp_results_summary.csv"),
    E("bp_B_25", "main", r"are\s+\$\-0\.000\$,\s+\$(?P<v>\d+)\$\s+of\s+\$50\$", "bps('B','LOh_better_of_50')", 0, "bp_results_summary.csv"),
    E("bp_B_of50", "main", r"of\s+\$(?P<v>\d+)\$\s+and", "BP_SEEDS", 0, "bp_tests.py"),
    E("bp_B_ci_lo", "main", r"and\s+\$\[(?P<v>-?[\d.]+),\s+\+0\.002\]\$\.", "bps('B','ci95_lo')", 0.0005, "bp_results_summary.csv"),
    E("bp_B_ci_hi", "main", r"and\s+\$\[\-0\.003,\s+(?P<v>[+-]?[\d.]+)\]\$\.\s+In", "bps('B','ci95_hi')", 0.0005, "bp_results_summary.csv"),
    E("bp_hw2", "main", r"In the original box of half-width \$(?P<v>\d+)\$, reported as the pre-registration", "BOX_L[0]", 0, "narrow box half-width (box_sensitivity_summary L)"),
    E("bp_gm2_469", "main", r"level on the decanes \(medians \$(?P<v>[\d.]+)\$\s+and \$0\.465\$\)", "bps('A','median_Q2_GM2')", 0.0005, "bp_results_summary.csv"),
    E("bp_lo2_465", "main", r"and\s+\$(?P<v>[\d.]+)\$\)\.\s+The", "bps('A','median_Q2_LO2')", 0.0005, "bp_results_summary.csv"),
    E("bp_lo2_980", "main", r"marginally ahead on the pooled set\s+\(\$(?P<v>[\d.]+)\$ against \$0\.976\$\)", "bps('B','median_Q2_LO2')", 0.0005, "bp_results_summary.csv"),
    E("bp_gm2_976", "main", r"against\s+\$(?P<v>[\d.]+)\$\)\.\s+Therefore", "bps('B','median_Q2_GM2')", 0.0005, "bp_results_summary.csv"),
    E("bp_loh_406", "main", r"hybrid control \(\$(?P<v>[\d.]+)\$ against\s+\$0\.465\$ in the narrow box\)", "bps('A','median_Q2_LOh')", 0.0005, "bp_results_summary.csv"),
    E("bp_lo2_465b", "main", r"\(\$0\.406\$ against\s+\$(?P<v>[\d.]+)\$ in the narrow box\)", "bps('A','median_Q2_LO2')", 0.0005, "bp_results_summary.csv"),
    E("bp_hept02", "main", r"by\s+\$(?P<v>[\d.]+)\\,\^\{\\circ\}\$C\.\s+On", "heptane_shift()", 0.05, "bp_provenance.csv 3-methylhexane: first-page AVG 365.0 K (91.9 C) vs pooled 91.7 C"),
    E("bp_101", "main", r"uncorrected cohort of \$(?P<v>\d+)\$ molecules the same test", "len(BPD)+bpp_count(9,'EXCLUDED')", 0, "bp_data rows + the nonane excluded by D5"),
    E("bp_101_dq2", "main", r"the same test\s+gave \$(?P<v>[+-]?[\d.]+)\$, \$24\$ of \$50\$, \$\[-0\.003, \+0\.002\]\$, so the correction", "changelog_n101('dq2')", 0.0005, "V35_TO_V36_SCIENTIFIC_CHANGELOG.md n=101 record (git-history result; not recomputable from committed CSVs)"),
    E("bp_101_24", "main", r"gave \$-0\.000\$, \$(?P<v>\d+)\$ of \$50\$, \$\[-0\.003", "changelog_n101('wins')", 0, "changelog n=101 record"),
    E("bp_101_of50", "main", r"gave \$-0\.000\$, \$24\$ of \$(?P<v>\d+)\$,", "BP_SEEDS", 0, "bp_tests.py"),
    E("bp_101_ci_lo", "main", r"\$24\$ of \$50\$, \$\[(?P<v>-?[\d.]+), \+0\.002\]\$, so the correction", "changelog_n101('lo_ci')", 0.0005, "changelog n=101 record"),
    E("bp_101_ci_hi", "main", r"\$24\$ of \$50\$, \$\[-0\.003, (?P<v>[+-]?[\d.]+)\]\$, so the correction", "changelog_n101('hi_ci')", 0.0005, "changelog n=101 record"),
    E("bp_ten_counts", "main", r"Ridge regression on the (?P<v>ten) degree-pair counts\s+reaches", "word(N_DEG_PAIRS)", 0, "degree-pair types (i<=j<=4) = baselines.py DEG_PAIRS"),
    E("bp_ridge860", "main", r"reaches \$Q\^2 = (?P<v>[\d.]+)\$ on the decanes, where every single index stays", "bpb('A','ridge on degree-pair counts')", 0.0005, "bp_baselines.csv"),
    E("bp_single_lo", "main", r"stays\s+between \$(?P<v>[\d.]+)\$ and \$0\.51\$", "bp_single_index_range()[0]", 0.005, "min over single-index decane models (bp_baselines + bp_results_summary)"),
    E("bp_single_hi", "main", r"between \$0\.15\$ and \$(?P<v>[\d.]+)\$, and \$0\.991\$", "bp_single_index_range()[1]", 0.005, "max over single-index decane models (GM12 0.5137)"),
    E("bp_ridge991", "main", r"and\s+\$(?P<v>[\d.]+)\$\s+on", "bpb('B','ridge on degree-pair counts')", 0.0005, "bp_baselines.csv"),
    E("bp_perm200", "main", r"\(\$(?P<v>\d+)\$ random permutations of the boiling points\)", r"struct_num(r'permuted \((\d+)\): median')", 0, "structural_checks_out.txt S7"),
    E("bp_perm_med", "main", r"gives it a median \$Q\^2\$ of \$(?P<v>-?[\d.]+)\$, so the gap", r"struct_num(r'permuted \(\d+\): median (-?[\d.]+)')", 0.005, "structural_checks_out.txt S7 (median -0.0882)"),

    # ======================= main.tex : conclusion =======================

    # ======================= main.tex : app:quality =======================
    E("aq_six_word", "supp", r"The\s+remaining\s+(?P<v>six)\s+\(4\-methylheptane,\s+2,2\-dimethylhexane,", "word(len(API44))", 0, "provenance S CANNOT VERIFY rows"),
    E("aq_api44_007", "supp", r"differ from the values used by \$(?P<v>[\d.]+)\$--\$2\.2\$\\,cal", "min(API44_DIFFS)", 0.005, "provenance API-44 S diffs (2,2-dimethylhexane 103.13 vs 103.06)"),
    E("aq_api44_22", "supp", r"by \$0\.07\$--\$(?P<v>[\d.]+)\$\\,cal\\,mol\$\^\{-1\}\$\\,K\$\^\{-1\}\$,\s+as that edition", "max(API44_DIFFS)", 0.05, "provenance API-44 S diffs (max 2.21)"),
    E("aq_api44_018", "supp", r"Substituting the 1947 values changes the\s+\$S\$ correlations by at most \$(?P<v>[\d.]+)\$ in \$\|r\|\$", "max_abs_change(A_SENS)", 0.0005, "entropy_api44_sensitivity_v41.csv max ||r_alt|-|r_orig|| (HM 0.0180)"),
    E("aq_api44_004", "supp", r"and puts \$M_1\$ ahead of\s+\$HM\$ by \$(?P<v>[\d.]+)\$\.", "api44_m1_minus_hm()", 0.0005, "entropy_api44_sensitivity_v41.csv |r_M1|-|r_HM| alternative (0.0037)"),
    E("aq_10131", "supp", r"The value \$(?P<v>[\d.]+)\$ found in our\s+earlier compilation", "OCTANES[IDX['2,2,3-trimethylpentane']][4]", 0.005, "octane_data 2,2,3-TMP S (the duplicated entry)"),
    E("aq_10206", "supp", r"The value used, \$(?P<v>[\d.]+)\$, is that of the compiled\s+\$18\$-octane", "OCTANES[IDX['2,3,3-trimethylpentane']][4]", 0.005, "octane_data 2,3,3-TMP S"),
    E("aq_18oct", "supp", r"is that of the compiled\s+\$(?P<v>\d+)\$-octane dataset", "N_OCT", 0, "octane_data"),
    E("aq_10210", "supp", r"gives\s+\$(?P<v>[\d.]+)\$\)\.\s+This", "EDIZ_233", 0.005, "provenance 2,3,3-TMP S source_value '(Ediz 2017)'"),
    E("aq_change006", "supp", r"most\s+\$(?P<v>[\d.]+)\$,\s+and", "max_abs_r_change('S', {'2,3,3-trimethylpentane': OCTANES[IDX['2,2,3-trimethylpentane']][4]})", 0.0005,
      "max ||r|| change over the 12 indices when 2,3,3-TMP S is reverted to 101.31 "
      "(computed 0.0086, from ISI 0.6012->0.5925; the largest change among the other eleven indices is M2 0.0059, "
      "so the stated 0.006 holds only if ISI is left out)"),
    E("aq_oct_11155", "supp", r"\(octane \$(?P<v>[\d.]+)\$ vs \$111\.70\$;", "OCTANES[IDX['octane']][4]", 0.005, "octane_data"),
    E("aq_oct_11170", "supp", r"\(octane \$111\.55\$ vs \$(?P<v>[\d.]+)\$;", "S_ALT['octane']", 0.005, "S_ALT (verify_loyola_v35.py)"),
    E("aq_22dmh_10313", "supp", r"2,2-dimethylhexane \$(?P<v>[\d.]+)\$ vs \$103\.40\$;", "OCTANES[IDX['2,2-dimethylhexane']][4]", 0.005, "octane_data"),
    E("aq_22dmh_10340", "supp", r"2,2-dimethylhexane \$103\.13\$ vs \$(?P<v>[\d.]+)\$;", "S_ALT['2,2-dimethylhexane']", 0.005, "S_ALT"),
    E("aq_224_10181", "supp", r"2,2,4-trimethylpentane \$(?P<v>[\d.]+)\$\s+vs \$104\.10\$;", "OCTANES[IDX['2,2,4-trimethylpentane']][4]", 0.005, "octane_data"),
    E("aq_224_10410", "supp", r"\$101\.81\$\s+vs \$(?P<v>[\d.]+)\$;", "S_ALT['2,2,4-trimethylpentane']", 0.005, "S_ALT"),
    E("aq_233_10206", "supp", r"2,3,3\-trimethylpentane\s+\$(?P<v>[\d.]+)\$\s+vs", "OCTANES[IDX['2,3,3-trimethylpentane']][4]", 0.005, "octane_data"),
    E("aq_233_10210", "supp", r"vs\s+\$(?P<v>[\d.]+)\$\)\.\s+For", "S_ALT['2,3,3-trimethylpentane']", 0.005, "S_ALT"),
    E("aq_nist_11163", "supp", r"agrees with the NIST WebBook \(\$(?P<v>[\d.]+)\$\)\. Substituting", "OCTANE_S_NIST", 0.005, "provenance octane S converted_value"),
    E("aq_S_change043", "supp", r"changes all twelve \$S\$ correlations, by up to \$(?P<v>[\d.]+)\$\s+in \$\|r\|\$, and moves", "max_abs_change(S_SENS)", 0.0005, "entropy_source_sensitivity_v36.csv"),
    E("aq_S_margin001", "supp", r"and moves the margin between \$HM\$ and \$M_1\$ at the top from\s+\$(?P<v>[\d.]+)\$ to \$[\d.]+\$\.\s+\\item", "s_margin()", 0.0005, "original-data HM/M1 margin on S (see oct_S_margin001)"),
    E("aq_S_margin007_alt", "supp", r"and moves the margin between \$HM\$ and \$M_1\$ at the top from\s+\$[\d.]+\$ to \$(?P<v>[\d.]+)\$\.\s+\\item", "s_margin_alt_csv()", 0.0005,
      "AUDIT: literal reading (margin after substitution) is 0.0071 per entropy_source_sensitivity_v36.csv"),
    E("aq_tmb_841", "supp", r"benchmark-compilation value \(\$(?P<v>[\d.]+)\$\) whose reference state is unresolved", "OCTANES[IDX[TMB]][3]", 0.005, "octane_data"),
    E("aq_298", "supp", r"The compound is a solid at \$(?P<v>\d+)\$~K, and NIST lists", None, 0, "UNCHECKABLE: condition constant"),
    E("aq_103", "supp", r"vaporization enthalpies near \$(?P<v>[\d.]+)\$~kcal", "TMB_DHVAP_KJ[0]/4.184", 0.05, "42.94/4.184 = 10.26 -> 10.3"),
    E("aq_93", "supp", r"persists\s+\(\$(?P<v>\d+)/100\$ and \$96/100\$ seeds instead of \$100/100\$\)", "tmbx(200,'LO_better')", 0, "dhvap_tmb_exclusion_summary_v36.csv"),
    E("aq_96", "supp", r"\(\$93/100\$ and \$(?P<v>\d+)/100\$ seeds instead of", "tmbx(500,'LO_better')", 0, "dhvap_tmb_exclusion_summary_v36.csv"),
    E("aq_100a", "supp", r"seeds instead of \$(?P<v>\d+)/100\$\)", "exp(200,'dHvap','LO_better')", 0, "expanded_robustness_summary_v35.csv"),
    E("aq_100b", "supp", r"instead of \$100/(?P<v>\d+)\$\)", "exp(200,'dHvap','n_seeds')", 0, "n_seeds"),
    E("aq_omega_002", "supp", r"differ from an alternative compilation by\s+\$(?P<v>[\d.]+)\$--\$0\.004\$", "min(OMEGA_DIFFS)", 0.0005, "|0.305-0.303| (OMEGA_ALT vs octane_data)"),
    E("aq_omega_004", "supp", r"by\s+\$0\.002\$\-\-\$(?P<v>[\d.]+)\$,\s+and", "max(OMEGA_DIFFS)", 0.0005, "|0.247-0.251|"),
    E("aq_final043", "supp", r"than\s+\$(?P<v>[\d.]+)\$\.\s+The", "max_abs_change(S_SENS)", 0.0005, "entropy_source_sensitivity_v36.csv (largest of all items)"),
    E("aq_final_margin001", "supp", r"where \$HM\$ leads \$M_1\$ by \$(?P<v>[\d.]+)\$ with the values used", "s_margin()", 0.0005, "octane_data: |r(HM,S)|-|r(M1,S)|"),
    E("aq_final_api44_004", "supp", r"substitution of item~\(i\) reverses that order by \$(?P<v>[\d.]+)\$", "api44_margin_m1_over_hm()", 0.0005, "entropy_api44_sensitivity_v41.csv: |r_alt(M1)|-|r_alt(HM)|"),

    # ======================= supplement.tex : S1 =======================
    E("s1_n18", "supp", r"of\s+the\s+\$(?P<v>\d+)\$\s+octane\s+isomers\.", "N_OCT", 0, "octane_data"),
    E("s1_298a", "supp", r"kcal\\,mol\$\^\{-1\}\$ \(the latter at \$(?P<v>\d+)\$~K\)", None, 0, "UNCHECKABLE: condition constant"),
    E("s1_90", "supp", r"All \$(?P<v>\d+)\$\s+molecule-level values\s+were traced", "len(PROV)", 0, "provenance rows"),
    E("s1_cls3", "supp", r"values,\s+\$(?P<v>\d+)\$\s+match", "prov_count('VERIFIED EXACT')", 0, "provenance classification counts"),
    E("s1_cls29", "supp", r"and\s+\$(?P<v>\d+)\$\s+match", "prov_count('VERIFIED AFTER UNIT CONVERSION')", 0, "provenance"),
    E("s1_cls37", "supp", r"further\s+\$(?P<v>\d+)\$\s+agree", "prov_count('AGREEMENT WITHIN TOLERANCE')", 0, "provenance"),
    E("s1_cls13", "supp", r"\$(?P<v>\d+)\$ lie within explained variation", "prov_count('SOURCE VARIATION / EXPLAINED')", 0, "provenance"),
    E("s1_cls7", "supp", r"revisions\.\s+\$(?P<v>\d+)\$\s+could", "prov_count('CANNOT VERIFY')", 0, "provenance"),
    E("s1_cls1_word", "supp", r"under\s+leave\-(?P<v>one)\-out\s+\(both", "word(prov_count('CONFLICT'))", 0, "provenance CONFLICT count"),
    E("s1_six", "supp", r"authoritative\s+value,\s+(?P<v>six)\s+of\s+these", "word(prov_count('CANNOT VERIFY','S'))", 0, "provenance S CANNOT VERIFY"),
    E("s1_api44_007", "supp", r"by\s+\$(?P<v>[\d.]+)\$\-\-\$2\.2\$\s+units,", "min(API44_DIFFS)", 0.005, "provenance API-44 S diffs"),
    E("s1_api44_22", "supp", r"differing by \$0\.07\$--\$(?P<v>[\d.]+)\$ units, as they do for isomers", "max(API44_DIFFS)", 0.05, "provenance API-44 S diffs"),
    E("s1_298b", "supp", r"\$(?P<v>\d+)\$\\,K vaporization enthalpy of 2,2,3,3-tetramethylbutane\. This\s+compound", None, 0, "UNCHECKABLE: condition constant"),
    E("s1_298c", "supp", r"compound is a solid at \$(?P<v>\d+)\$\\,K \(triple point", None, 0, "UNCHECKABLE: condition constant"),
    E("s1_374", "supp", r"point\s+\$(?P<v>\d+)\$\\,K\),\s+and", "rnd(TMB_TRIPLE_K,0)", 0, "provenance TMB triple point 373.97 K"),
    E("s1_4294", "supp", r"of\s+\$(?P<v>[\d.]+)\$\s+and", "TMB_DHVAP_KJ[0]", 0, "provenance"),
    E("s1_4291", "supp", r"and\s+\$(?P<v>[\d.]+)\$\\,kJ\\,mol\$\^\{\-1\}\$\s+\(about", "TMB_DHVAP_KJ[1]", 0, "provenance"),
    E("s1_1026", "supp", r"\(about\s+\$(?P<v>[\d.]+)\$\\,kcal\\,mol\$\^\{\-1\}\$\)\s+together", "TMB_DHVAP_KJ[0]/4.184", 0.005, "42.94/4.184"),
    E("s1_841", "supp", r"here,\s+\$(?P<v>[\d.]+)\$\\,kcal\\,mol\$\^\{\-1\}\$\s+\(\$35\.19\$\\,kJ\\,mol\$\^\{\-1\}\$\),", "OCTANES[IDX[TMB]][3]", 0.005, "octane_data"),
    E("s1_3519", "supp", r"\$8\.41\$\\,kcal\\,mol\$\^\{\-1\}\$\s+\(\$(?P<v>[\d.]+)\$\\,kJ\\,mol\$\^\{\-1\}\$\),\s+is", "OCTANES[IDX[TMB]][3]*4.184", 0.005, "8.41 x 4.184"),
    E("s1_tmb_omega247", "supp", r"2,2,3,3-tetramethylbutane \(\$(?P<v>[\d.]+)\$ vs\.\\ compiled \$0\.251\$\)", "OCTANES[IDX[TMB]][5]", 0.0005, "octane_data"),
    E("s1_tmb_omega251", "supp", r"compiled\s+\$(?P<v>[\d.]+)\$\),\s+while", "KDB_TMB_OMEGA", 0.0005, "provenance TMB omega source_value (KDB 0.2510)"),
    E("s1_224_omega305", "supp", r"2,2,4-trimethylpentane \(\$(?P<v>[\d.]+)\$ vs\.\\ compiled\s+\$0\.303\$\)", "OCTANES[IDX['2,2,4-trimethylpentane']][5]", 0.0005, "octane_data"),
    E("s1_224_omega303", "supp", r"vs\.\\ compiled\s+\$(?P<v>[\d.]+)\$\) agrees only within tolerance", "KDB_224_OMEGA", 0.0005, "provenance 2,2,4-TMP omega source_value (KDB 0.3030)"),
    E("s1_M2_988", "supp", r"moves\s+from\s+\$(?P<v>-?[\d.]+)\$\s+to\s+\$\-0\.986\$\)\.", "W_SENS['M2'][0]", 0.0005, "omega_source_sensitivity_v35.csv"),
    E("s1_M2_986", "supp", r"to\s+\$(?P<v>-?[\d.]+)\$\)\.\s+It", "W_SENS['M2'][1]", 0.0005, "omega_source_sensitivity_v35.csv"),
    E("s1_dhvap_005", "supp", r"by\s+\$(?P<v>[\d.]+)\$\-\-\$0\.13\$\\,kcal\\,mol\$\^\{\-1\}\$\s+circulate", "min(DHVAP_CORR_DIFFS)", 0.005, "octane_data.py docstring v36 corrections (8.88->8.83)"),
    E("s1_dhvap_013", "supp", r"by\s+\$0\.05\$--\$(?P<v>[\d.]+)\$\\,kcal", "max(DHVAP_CORR_DIFFS)", 0.005, "octane_data.py docstring v36 corrections (9.21->9.08)"),
    E("s1_897", "supp", r"determinations\s+\(\$(?P<v>[\d.]+)\$,\s+\$9\.08\$\),", "OCTANES[IDX['3,3-dimethylhexane']][3]", 0.005, "octane_data"),
    E("s1_908", "supp", r"\(\$8\.97\$,\s+\$(?P<v>[\d.]+)\$\),\s+and", "OCTANES[IDX['3-ethyl-3-methylpentane']][3]", 0.005, "octane_data"),
    E("s1_883", "supp", r"are\s+\$(?P<v>[\d.]+)\$,\s+which", "OCTANES[IDX['2,2,3-trimethylpentane']][3]", 0.005, "octane_data"),
    E("s1_890", "supp", r"and\s+\$(?P<v>[\d.]+)\$,\s+which", "OCTANES[IDX['2,3,3-trimethylpentane']][3]", 0.005, "octane_data"),
    E("s1_S_004", "supp", r"octane QSPR compilation by\s+\$(?P<v>[\d.]+)\$--\$2\.29\$ units", "min(S_DIFFS)", 0.005, "S_ALT vs octane_data (102.10-102.06)"),
    E("s1_S_229", "supp", r"\$0\.04\$--\$(?P<v>[\d.]+)\$ units", "max(S_DIFFS)", 0.005, "S_ALT vs octane_data (104.10-101.81)"),
    E("s1_10206", "supp", r"value\s+\$(?P<v>[\d.]+)\$\s+being", "OCTANES[IDX['2,3,3-trimethylpentane']][4]", 0.005, "octane_data"),
    E("s1_043", "supp", r"by\s+up\s+to\s+\$(?P<v>[\d.]+)\$\s+in\s+\$\|r\|\$,\s+but", "max_abs_change(S_SENS)", 0.0005, "entropy_source_sensitivity_v36.csv"),
    E("s1_984", "supp", r"\(\$\|r\| = (?P<v>[\d.]+)\$, with\s+\$LO\(0, 0, 2\)\$ second at \$0\.981\$\)\. At the\s+exact", "abs(r_tab4('LO(0,0,1)','dHvap'))", 0.0005, "octane_data"),
    E("s1_981", "supp", r"second at \$(?P<v>[\d.]+)\$\)\. At the\s+exact-reduction", "abs(r_tab4('LO(0,0,2)','dHvap'))", 0.0005, "octane_data"),
    E("s1_B10000a", "supp", r"\(\$B = (?P<v>10\\,000)\$,\s+resampling the \$18\$ isomers jointly", "BOOT_B", 0, "verify_loyola_v35.py boot_hw default B / section [D] B"),
    E("s1_18resample", "supp", r"resampling the \$(?P<v>\d+)\$ isomers jointly", "N_OCT", 0, "octane_data"),
    E("s1_hw016", "supp", r"range\s+from\s+\$(?P<v>[\d.]+)\$\s+to\s+\$0\.096\$", "min(boot_hws().values())", 0.0005, "percentile-bootstrap half-widths of the five bolded cells (B=10000, seed 0)"),
    E("s1_hw096", "supp", r"to\s+\$(?P<v>[\d.]+)\$\s+across", "max(boot_hws().values())", 0.0005, "idem (max)"),
    E("s1_B10000b", "supp", r"\$B = (?P<v>10\\,000)\$, \\texttt\{default\\_rng\(0\)\}\)\. The value", "BOOT_B", 0, "verify_loyola_v35.py boot_hw"),
    E("s1_del027", "supp", r"most\s+\$(?P<v>[\d.]+)\$,\s+which", "deletion_influence_max()", 0.0005, "deletion influence"),
    E("s1_n18_red", "supp", r"descriptors on the \$(?P<v>\d+)\$ isomers, fourteen descriptor pairs", "N_OCT", 0, "octane_data"),
    E("s1_fourteen", "supp", r"isomers, (?P<v>fourteen) descriptor pairs have", "word(n_pairs_ge(0.99))", 0, "descriptor_correlations.csv"),
    E("s1_r9997", "supp", r"\$r\s+=\s+(?P<v>[\d.]+)\$\.\s+A", "corr_between('R','H2')", 0.00005, "descriptor_correlations.csv R vs H2"),
    E("s1_18x12_a", "supp", r"standardised\s+\$(?P<v>\d+)\s+\\times\s+12\$", "N_OCT", 0, "octane_data"),
    E("s1_18x12_b", "supp", r"\$18 \\times (?P<v>\d+)\$\s+descriptor matrix", "len(RED)", 0, "twelve descriptors"),
    E("s1_pc1_903", "supp", r"places \$(?P<v>[\d.]+)\\%\$ of the variance on the first\s+component", "100*pca_cumvar(1)", 0.05, "pca_spectrum.csv component 1"),
    E("s1_pc2_9905", "supp", r"and\s+\$(?P<v>[\d.]+)\\%\$\s+on", "100*pca_cumvar(2)", 0.005, "pca_spectrum.csv"),
    E("s1_effrank", "supp", r"is\s+\$(?P<v>[\d.]+)\$,\s+so", "pca_participation_ratio()", 0.05, "participation ratio of pca_spectrum.csv eigenvalues"),
    E("s1_figcap18", "supp", r"five octane physicochemical properties on the \$(?P<v>\d+)\$ isomers\.\}", "N_OCT", 0, "octane_data"),

    # ======================= supplement.tex : S3 =======================
    E("s3_200cand", "supp", r"\$(?P<v>\d+)\$ candidate parameter vectors are drawn once from\s+\$\\mathrm\{Uniform\}\(-2,2\)\$", "BUDGETS[0]", 0, "budget 200 (ablation_robustness.csv budget)"),
    E("s3_rng12345", "supp", r"\\texttt\{default\\_rng\((?P<v>\d+)\)\}\s+for Table~\\ref\{tab:ablation\}", "int(ABLR[0]['seed'])", 0, "ablation_robustness.csv seed"),
    E("s3_17train_a", "supp", r"On\s+the\s+\$(?P<v>\d+)\$\s+training\s+isomers", "N_OCT-1", 0, "18-1"),
    E("s3_17train_b", "supp", r"the\s+regression is refit on all \$(?P<v>\d+)\$, and the held-out", "N_OCT-1", 0, "18-1"),
    E("s3cap_seed", "supp", r"candidate stream\} \(seed \$(?P<v>\d+)\$, budget\s+\$200\$\)", "int(ABLR[0]['seed'])", 0, "ablation_robustness.csv"),
    E("s3cap_b200", "supp", r"budget\s+\$(?P<v>\d+)\$\),\s+where", "int(ABLR[0]['budget'])", 0, "ablation_robustness.csv"),
    E("s3cap_of18", "supp", r"counts outer folds\s+\(of \$(?P<v>\d+)\$\) in which the Loyola model", "N_OCT", 0, "octane_data"),
    E("s3cap_100seed", "supp", r"of\s+\$(?P<v>\d+)\$\s+seeds\)\.", "len(SEEDS_EXP)", 0, "expanded_robustness_v35.csv"),
    E("s3cap_seeds99", "supp", r"seeds\s+\$0\$\-\-\$(?P<v>\d+)\$,\s+the", "max(SEEDS_EXP)", 0, "expanded_robustness_v35.csv"),
    E("s3cap_B200", "supp", r"\$B\s+=\s+(?P<v>\d+)\$\s+and", "BUDGETS[0]", 0, "budgets"),
    E("s3cap_B500", "supp", r"\$B\s+=\s+(?P<v>\d+)\$\.\s+All", "BUDGETS[1]", 0, "budgets"),
    E("s3_tb136", "supp", r"Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$,\s+and", "ablr('T_B','dQ2')", 0.0005, "ablation_robustness.csv seed 12345"),
    E("s3_dhvap086", "supp", r"Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\)\s+and", "ablr('dHvap','dQ2')", 0.0005, "ablation_robustness.csv"),
    E("s3_three_props", "supp", r"it\s+on\s+(?P<v>three)\s+\(\$\\Delta\s+H_f\$,", "word(sum(1 for p in PROPS if ablr(p,'dQ2')<0))", 0, "ablation_robustness.csv negative dQ2 count"),
    E("s3_18folds_same", "supp", r"selected the same\s+\$\(\\alpha,\\beta\)\$ in all \$(?P<v>\d+)\$ folds there", "perfold_mode('dHf','GM')[1]", 0, "ablation_perfold.csv dHf GM modal count"),
    E("s3_sd12", "supp", r"deviation above \$(?P<v>[\d.]+)\$ in both \$\\alpha\$ and \$\\beta\$\)", "math.floor(10*min(abl('dHf','LO','sel_a_sd'),abl('dHf','LO','sel_b_sd')))/10", 0.05, "ablation_summary.csv dHf LO sel_a_sd=1.228, sel_b_sd=1.328, floored to 1 dp"),
    E("s3_gamma048", "supp", r"\(maximum\s+\$\|\\gamma\| = (?P<v>[\d.]+)\$\)", "perfold_max_abs_gamma()", 0.005, "ablation_perfold.csv max |sel_g| over LO rows"),
    E("s3_alpha1021", "supp", r"the parent chose \$\(\\alpha,\\beta\) =\s+\((?P<v>[\d.]+), -1\.993\)\$, on the boundary of the box, in \$16\$ of the \$18\$\s+folds", "perfold_mode('dHvap','GM')[0][0]", 0.0005, "ablation_perfold.csv"),
    E("s3_beta1993", "supp", r"\(1\.021, (?P<v>-?[\d.]+)\)\$, on the boundary of the box, in \$16\$ of the \$18\$\s+folds", "perfold_mode('dHvap','GM')[0][1]", 0.0005, "ablation_perfold.csv"),
    E("s3_16of18a", "supp", r"box,\s+in\s+\$(?P<v>\d+)\$\s+of\s+the", "perfold_mode('dHvap','GM')[1]", 0, "ablation_perfold.csv"),
    E("s3_16of18b", "supp", r"the\s+\$(?P<v>\d+)\$\s+folds,", "len(perfold_triples('dHvap','GM'))", 0, "ablation_perfold.csv"),
    E("s3_triple_a", "supp", r"the identical\s+triple \$\((?P<v>-?[\d.]+), \+0\.271, \+0\.239\)\$", "perfold_mode('dHvap','LO')[0][0]", 0.0005, "ablation_perfold.csv dHvap LO triple (-0.270, 0.271, 0.239)"),
    E("s3_triple_b", "supp", r"triple \$\(-0\.270, (?P<v>[+-]?[\d.]+), \+0\.239\)\$", "perfold_mode('dHvap','LO')[0][1]", 0.005, "ablation_perfold.csv"),
    E("s3_triple_g", "supp", r"triple \$\(-0\.270, \+0\.271, (?P<v>[+-]?[\d.]+)\)\$", "perfold_mode('dHvap','LO')[0][2]", 0.005, "ablation_perfold.csv"),
    E("s3_n18", "supp", r"With\s+\$n = (?P<v>\d+)\$ molecules these \$Q\^2\$ differences", "N_OCT", 0, "octane_data"),
    E("s3_onehundred", "supp", r"repeated for (?P<v>one hundred) seeds \(\$0\$--\$99\$\) at both\s+budgets", "word(len(SEEDS_EXP))", 0, "expanded_robustness_v35.csv"),
    E("s3_seeds99", "supp", r"one hundred seeds \(\$0\$--\$(?P<v>\d+)\$\) at both\s+budgets", "max(SEEDS_EXP)", 0, "expanded_robustness_v35.csv"),
    E("s3_b200", "supp", r"budgets\s+\(\$(?P<v>\d+)\$\s+and", "BUDGETS[0]", 0, "budgets"),
    E("s3_b500", "supp", r"and\s+\$(?P<v>\d+)\$\s+candidates", "BUDGETS[1]", 0, "budgets"),
    E("s3_1000conf", "supp", r"makes\s+\$(?P<v>\d+)\$\s+configurations", "len(EXP_RAW)", 0, "expanded_robustness_v35.csv rows (100 seeds x 2 budgets x 5 properties)"),
    E("s3_100a", "supp", r"in every seed of this sweep \(\$(?P<v>\d+)/100\$ at\s+both budgets, and \$100/100\$ in the paired control", "min(exp(200,'dHvap','LO_better'),exp(500,'dHvap','LO_better'))", 0, "expanded_robustness_summary_v35.csv"),
    E("s3_100paired", "supp", r"sweep\s+\(\$100/(?P<v>\d+)\$\s+at", "min(exp(200,'dHvap','paired_better'),exp(500,'dHvap','paired_better'))", 0, "paired_better"),
    E("s3_med069", "supp", r"\$\\Delta\s+Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\s+and\s+\$\+0\.068\$,", "exp(200,'dHvap','dQ2_median')", 0.0005, "dQ2_median"),
    E("s3_med068", "supp", r"\+0\.069\$\s+and\s+\$(?P<v>[+-]?[\d.]+)\$,\s+with\s+range", "exp(500,'dHvap','dQ2_median')", 0.0005, "dQ2_median"),
    E("s3_range024", "supp", r"with\s+range\s+\$(?P<v>[+-]?[\d.]+)\$\s+to\s+\$\+0\.102\$\.", "min(exp(200,'dHvap','dQ2_min'),exp(500,'dHvap','dQ2_min'))", 0.0005, "dQ2_min over both budgets"),
    E("s3_range102", "supp", r"to\s+\$(?P<v>[+-]?[\d.]+)\$\.\s+It", "max(exp(200,'dHvap','dQ2_max'),exp(500,'dHvap','dQ2_max'))", 0.0005, "dQ2_max over both budgets"),
    E("s3_dhf86", "supp", r"H_f\$\s+\(\$(?P<v>\d+)/100\$\s+and", "exp(200,'dHf','LO_worse')", 0, "LO_worse"),
    E("s3_dhf76", "supp", r"and\s+\$(?P<v>\d+)/100\$\s+seeds\),", "exp(500,'dHf','LO_worse')", 0, "LO_worse"),
    E("s3_tb53", "supp", r"\$200\$\s+\(\$(?P<v>\d+)/100\$\)\s+but", "exp(200,'T_B','LO_better')", 0, "LO_better"),
    E("s3_tb64", "supp", r"\$500\$\s+\(\$(?P<v>\d+)/100\$\)\.\s+\$S\$", "exp(500,'T_B','LO_better')", 0, "LO_better"),
    E("s3_n18_fixed", "supp", r"of\s+\$(?P<v>\d+)\$\s+molecules,", "N_OCT", 0, "octane_data"),
    E("s3_100of100c", "supp", r"particular,\s+\$(?P<v>\d+)/100\$\s+does", "exp(200,'dHvap','LO_better')", 0, "LO_better"),
    E("s3_17mol", "supp", r"excluded\s+\(\$(?P<v>\d+)\$\s+molecules,", "N_OCT-1", 0, "18-1"),
    E("s3_tmb93", "supp", r"\$\\Delta\s+H_\{\\mathrm\{vap\}\}\$\s+in\s+\$(?P<v>\d+)/100\$\s+seeds\s+at\s+budget", "tmbx(200,'LO_better')", 0, "dhvap_tmb_exclusion_summary_v36.csv"),
    E("s3_tmb96", "supp", r"and\s+\$(?P<v>\d+)/100\$\s+at", "tmbx(500,'LO_better')", 0, "dhvap_tmb_exclusion_summary_v36.csv"),
    E("s3_tmbp95", "supp", r"control\s+\$(?P<v>\d+)/100\$\s+and", "tmbx(200,'paired_better')", 0, "paired_better"),
    E("s3_tmbp96", "supp", r"and\s+\$(?P<v>\d+)/100\$\)\.\s+The", "tmbx(500,'paired_better')", 0, "paired_better"),
    E("s3_tmbmed046", "supp", r"\$\\Delta\s+Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\s+and\s+\$\+0\.051\$,", "tmbx(200,'dQ2_median')", 0.0005, "dQ2_median"),
    E("s3_tmbmed051", "supp", r"\+0\.046\$\s+and\s+\$(?P<v>[+-]?[\d.]+)\$,\s+with\s+range", "tmbx(500,'dQ2_median')", 0.0005, "dQ2_median"),
    E("s3_tmbrange048", "supp", r"with\s+range\s+\$(?P<v>[+-]?[\d.]+)\$\s+to\s+\$\+0\.098\$\.", "min(tmbx(200,'dQ2_min'),tmbx(500,'dQ2_min'))", 0.0005, "dQ2_min over both budgets"),
    E("s3_tmbrange098", "supp", r"to\s+\$(?P<v>[+-]?[\d.]+)\$\.\s+The", "max(tmbx(200,'dQ2_max'),tmbx(500,'dQ2_max'))", 0.0005, "dQ2_max over both budgets"),

    # ======================= supplement.tex : S4 =======================
    E("s4_18", "supp", r"its size \(\$(?P<v>\d+)\$ molecules\) and\s+its restriction", "N_OCT", 0, "octane_data"),
    E("s4_35", "supp", r"the\s+\$(?P<v>\d+)\$\s+constitutional", "len(NON_DATA)", 0, "nonane_data.csv"),
    E("s4_tb35", "supp", r"points\s+\(\$(?P<v>\d+)\$\s+values\)", "non_count('T_B_C')", 0, "nonane_data.csv"),
    E("s4_dhvap34", "supp", r"enthalpies\s+\(\$(?P<v>\d+)\$\s+values,", "non_count('dHvap_kcal')", 0, "nonane_data.csv"),
    E("s4_1K", "supp", r"quoted only to \$(?P<v>\d+)\$\\,K\)", None, 0, "UNCHECKABLE: precision statement (README_nonane_data.md D3: 13 of 20 NIST AVG values are integer-K)"),
    E("s4_cal4", "supp", r"only \$(?P<v>\d+)\$ of \$34\$ are calorimetric\s+determinations and one is a NIST average", "non_dhvap_rule_count('calorimetric')", 0, "nonane_provenance.csv"),
    E("s4_of34", "supp", r"only \$4\$ of \$(?P<v>\d+)\$ are calorimetric", "non_count('dHvap_kcal')", 0, "nonane_data.csv"),
    E("s4_one_avg", "supp", r"determinations\s+and\s+(?P<v>one)\s+is\s+a", "word(non_dhvap_rule_count('avg'))", 0, "nonane_provenance.csv"),
    E("s4_29", "supp", r"other\s+\$(?P<v>\d+)\$\s+come", "non_dhvap_rule_count('compilation')", 0, "nonane_provenance.csv"),
    E("s4_35all", "supp", r"which covers all \$(?P<v>\d+)\$ nonanes and \$75\$ decanes", "len(NON_DATA)", 0, "nonane_data.csv (35 molecular trees of order 9)"),
    E("s4_75dec", "supp", r"nonanes and \$(?P<v>\d+)\$ decanes and is not a set", "N_DECANES", 0, "structural_checks_out.txt S1 (10 mol: 75)"),
    E("s4_80", "supp", r"at least \$(?P<v>\d+)\$ of \$100\$ seeds at both budgets\s+with positive median", "NONV_THRESH", 0, "nonane_validation.py decision rule"),
    E("s4_of100", "supp", r"at least \$80\$ of \$(?P<v>\d+)\$ seeds at both budgets", "NONV_SEEDS", 0, "nonane_validation.py SEEDS"),
    E("s4_four_baselines", "supp", r"(?P<v>Four) baselines were added", "word(N_BASELINES, True)", 0, "baselines_nonane.csv non-GM/LO methods (mean, fixed_best, IRLA, ridge_counts)"),
    E("s4_ten", "supp", r"of\s+the\s+(?P<v>ten)\s+classical\s+indices", "word(len(CLASSICAL))", 0, "ten reductions"),
    E("s4_95", "supp", r"GM\s+in\s+\$(?P<v>\d+)/100\$\s+and\s+\$98/100\$", "nonv('dHvap','primary',200,'LO_better')", 0, "nonane_validation_summary.csv"),
    E("s4_98", "supp", r"\$95/100\$\s+and\s+\$(?P<v>\d+)/100\$\s+seeds,\s+with", "nonv('dHvap','primary',500,'LO_better')", 0, "nonane_validation_summary.csv"),
    E("s4_med048", "supp", r"\$\\Delta\s+Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\s+and\s+\$\+0\.053\$\.", "nonv('dHvap','primary',200,'median_dQ2')", 0.0005, "median_dQ2"),
    E("s4_med053", "supp", r"and\s+\$(?P<v>[+-]?[\d.]+)\$\.\s+For", "nonv('dHvap','primary',500,'median_dQ2')", 0.0005, "median_dQ2"),
    E("s4_tb58", "supp", r"\\emph\{mixed\}\s+\(\$(?P<v>\d+)/100\$\s+and", "nonv('T_B','primary',200,'LO_better')", 0, "nonane_validation_summary.csv"),
    E("s4_tb63", "supp", r"and\s+\$(?P<v>\d+)/100\$\)\.\s+It", "nonv('T_B','primary',500,'LO_better')", 0, "nonane_validation_summary.csv"),
    E("s4_413", "supp", r"2,3,3,4-tetramethylpentane, \$(?P<v>\d+) \\pm 6\$~K", r"float(re.match(r'([\d.]+)', tmp_tb_row()['original_value']).group(1))", 0, "nonane_provenance.csv TMP T_B original_value '413. ± 6.'"),
    E("s4_pm6", "supp", r"\$413 \\pm (?P<v>\d+)\$~K, by the median of all", r"float(re.search(r'± ([\d.]+)', tmp_tb_row()['original_value']).group(1))", 0, "nonane_provenance.csv"),
    E("s4_eight", "supp", r"by the median of all (?P<v>eight)\s+listed determinations", "word(len(tmp_determinations()))", 0, "nonane_provenance.csv all_determinations count"),
    E("s4_41462", "supp", r"outlier,\s+\$(?P<v>[\d.]+)\$\~K\.\s+LO", "float(np.median(tmp_determinations()))", 0.005, "median of the 8 TMP determinations"),
    E("s4_d4_60", "supp", r"better\s+in\s+\$(?P<v>\d+)/100\$\s+and\s+\$66/100\$", "nonv('T_B','D4',200,'LO_better')", 0, "nonane_validation_summary.csv D4"),
    E("s4_d4_66", "supp", r"\$60/100\$\s+and\s+\$(?P<v>\d+)/100\$\s+seeds,\s+with", "nonv('T_B','D4',500,'LO_better')", 0, "D4"),
    E("s4_d4_041", "supp", r"\$\\Delta\s+Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\s+and\s+\$\+0\.052\$\.", "nonv('T_B','D4',200,'median_dQ2')", 0.0005, "D4"),
    E("s4_d4_052", "supp", r"\+0\.041\$\s+and\s+\$(?P<v>[+-]?[\d.]+)\$\.\s+The\s+pre\-registered", "nonv('T_B','D4',500,'median_dQ2')", 0.0005, "D4"),
    E("s4_hyb002", "supp", r"Q\^2\s+=\s+(?P<v>[+-]?[\d.]+)\$\s+under", "box('nonane','dHvap',12,'median_dQ2_hybrid')", 0.0005, "box_sensitivity_summary.csv"),
    E("s4_q2_853", "supp", r"GM\) reach\s+\$Q\^2 = (?P<v>[\d.]+)\$--\$0\.888\$", "narrow_box_q2_range('q2only')[0]", 0.0005, "min over {classical best, GM b200} x {oct, non} dHvap (nonane GM 0.8529)"),
    E("s4_q2_888", "supp", r"=\s+0\.853\$\-\-\$(?P<v>[\d.]+)\$\.\s+Models", "narrow_box_q2_range('q2only')[1]", 0.0005, "max (octane GM b200 0.8876)"),
    E("s4_q2_897", "supp", r"LO\) reach\s+\$Q\^2 = (?P<v>[\d.]+)\$--\$0\.957\$", "narrow_box_q2_range('linear')[0]", 0.0005, "min over {IRLA, ridge, LO(0,0,1), LO b200} x {oct, non} (nonane IRLA 0.8969)"),
    E("s4_q2_957", "supp", r"\$Q\^2 = 0\.897\$--\$(?P<v>[\d.]+)\$\. This split", "narrow_box_q2_range('linear')[1]", 0.0005, "max (octane LO(0,0,1) 0.9572)"),
    E("s4_wide942", "supp", r"the box of half-width \$12\$ the parent alone reaches \$(?P<v>[\d.]+)\$ and \$0\.892\$", "box('octane','dHvap',12,'median_Q2_GM')", 0.0005, "box_sensitivity_summary.csv"),
    E("s4_wide892", "supp", r"parent alone reaches \$0\.942\$ and \$(?P<v>[\d.]+)\$", "box('nonane','dHvap',12,'median_Q2_GM')", 0.0005, "box_sensitivity_summary.csv"),
    E("s4_lo1_957", "supp", r"sets\s+\(\$(?P<v>[\d.]+)\$\s+and", "base('oct','dHvap','fixed_best')", 0.0005, "baselines_octane.csv"),
    E("s4_lo1_903", "supp", r"\(\$0\.957\$\s+and\s+\$(?P<v>[\d.]+)\$\s+against\s+medians", "base('non','dHvap_kcal','fixed_best')", 0.0005, "baselines_nonane.csv"),
    E("s4_lo_953", "supp", r"medians\s+\$(?P<v>[\d.]+)\$\s+and", "base('oct','dHvap','LO_b200')", 0.0005, "baselines_octane.csv"),
    E("s4_lo_900", "supp", r"\$0\.953\$\s+and\s+\$(?P<v>[\d.]+)\$\)\.\s+It\s+is", "base('non','dHvap_kcal','LO_b200')", 0.0005, "baselines_nonane.csv"),
    E("s4_corr996_oct", "supp", r"is\s+\$(?P<v>[\d.]+)\$\.\s+The", "corr_lo1_irla('oct')", 0.0005, "corr on octanes"),
    E("s4_corr996_non", "supp", r"is\s+\$(?P<v>[\d.]+)\$\.\s+The", "corr_lo1_irla('non')", 0.0005, "corr on nonanes"),
    E("s4_ridge927", "supp", r"\(\$Q\^2\s+=\s+(?P<v>[\d.]+)\$\s+for", "base('non','dHvap_kcal','ridge_counts')", 0.0005, "baselines_nonane.csv"),
    E("s4_ridge682", "supp", r"H_\{\\mathrm\{vap\}\}\$,\s+\$(?P<v>[\d.]+)\$\s+for", "base('non','T_B_C','ridge_counts')", 0.0005, "baselines_nonane.csv"),
    E("s4_irla003", "supp", r"within\s+\$(?P<v>[\d.]+)\$\s+of", "base('non','dHvap_kcal','LO_b200')-base('non','dHvap_kcal','IRLA')", 0.0005, "baselines_nonane.csv"),
    E("s4_irla897", "supp", r"nonanes\s+\(\$(?P<v>[\d.]+)\$\s+against", "base('non','dHvap_kcal','IRLA')", 0.0005, "baselines_nonane.csv"),
    E("s4_lo900b", "supp", r"against\s+\$(?P<v>[\d.]+)\$\)\.\s+For", "base('non','dHvap_kcal','LO_b200')", 0.0005, "baselines_nonane.csv"),
    E("s4_18frozen", "supp", r"selected on all\s+\$(?P<v>\d+)\$ octanes were frozen", "N_OCT", 0, "octane_data"),
    E("s4_tr100", "supp", r"\$\\Delta\s+H_\{\\mathrm\{vap\}\}\$\s+in\s+\$(?P<v>\d+)/100\$\s+seeds\s+at\s+both", "min(trans('dHvap',200,'LO_better_refit'),trans('dHvap',500,'LO_better_refit'))", 0, "transfer_exploratory_summary.csv"),
    E("s4_tr910", "supp", r"\$Q\^2\s+=\s+(?P<v>[\d.]+)\$\s+and", "trans('dHvap',200,'median_Q2_refit_LO')", 0.0005, "transfer_exploratory_summary.csv"),
    E("s4_tr916", "supp", r"= 0\.910\$ and \$(?P<v>[\d.]+)\$ against \$0\.864\$", "trans('dHvap',500,'median_Q2_refit_LO')", 0.0005, "transfer_exploratory_summary.csv"),
    E("s4_tr864", "supp", r"against \$(?P<v>[\d.]+)\$ and \$0\.865\$\)", "trans('dHvap',200,'median_Q2_refit_GM')", 0.0005, "transfer_exploratory_summary.csv"),
    E("s4_tr865", "supp", r"\$0\.864\$\s+and\s+\$(?P<v>[\d.]+)\$\)\.\s+It\s+beat", "trans('dHvap',500,'median_Q2_refit_GM')", 0.0005, "transfer_exploratory_summary.csv"),
    E("s4_tr65", "supp", r"\$T_B\$\s+in\s+\$(?P<v>\d+)/100\$\s+and\s+\$82/100\$\.", "trans('T_B',200,'LO_better_refit')", 0, "transfer_exploratory_summary.csv"),
    E("s4_tr82", "supp", r"in \$65/100\$ and \$(?P<v>\d+)/100\$\. With the octane", "trans('T_B',500,'LO_better_refit')", 0, "transfer_exploratory_summary.csv"),
    E("s4_frozen_m222", "supp", r"\$Q\^2\$\s+between\s+\$(?P<v>-?[\d.]+)\$\s+and\s+\$\-0\.72\$", "min(trans(p,b,'median_Q2_frozen_LO') for p in ('T_B','dHvap') for b in (200,500))", 0.005, "transfer_exploratory_summary.csv frozen LO min"),
    E("s4_frozen_m072", "supp", r"and \$(?P<v>-?[\d.]+)\$ for LO against \$0\.06\$", "max(trans(p,b,'median_Q2_frozen_LO') for p in ('T_B','dHvap') for b in (200,500))", 0.005, "frozen LO max"),
    E("s4_frozen_006", "supp", r"for LO against \$(?P<v>[\d.]+)\$ to \$0\.44\$ for GM\)", "min(trans(p,b,'median_Q2_frozen_GM') for p in ('T_B','dHvap') for b in (200,500))", 0.005, "frozen GM min"),
    E("s4_frozen_044", "supp", r"to \$(?P<v>[\d.]+)\$ for GM\)", "max(trans(p,b,'median_Q2_frozen_GM') for p in ('T_B','dHvap') for b in (200,500))", 0.005, "frozen GM max"),
    E("s4_2000res", "supp", r"bootstrap over molecules \(\$(?P<v>\d+)\$ resamples\)", "UNC_NB", 0, "uncertainty_exploratory.py NB"),
    E("s4_95pct", "supp", r"The \$(?P<v>\d+)\\%\$ intervals", None, 0, "UNCHECKABLE: confidence level"),
    E("s4_ci_oct_lo", "supp", r"are\s+\$\[(?P<v>[+-]?[\d.]+),\s+\+0\.111\]\$", "unc('octane','dHvap',200,'ci95_lo')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_oct_hi", "supp", r"are\s+\$\[\+0\.014,\s+(?P<v>[+-]?[\d.]+)\]\$\s+on", "unc('octane','dHvap',200,'ci95_hi')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_non_lo", "supp", r"but\s+\$\[(?P<v>-?[\d.]+), \+0\.113\]\$ on the nonanes at budget \$200\$", "unc('nonane','dHvap',200,'ci95_lo')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_non_hi", "supp", r"\$\[-0\.006, (?P<v>[+-]?[\d.]+)\]\$ on the nonanes at budget \$200\$", "unc('nonane','dHvap',200,'ci95_hi')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_b200", "supp", r"budget\s+\$(?P<v>\d+)\$\s+\(\$\[\-0\.005,", "BUDGETS[0]", 0, "budget"),
    E("s4_ci_non500_lo", "supp", r"\(\$\[(?P<v>-?[\d.]+), \+0\.119\]\$ at\s+\$500\$\)", "unc('nonane','dHvap',500,'ci95_lo')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_non500_hi", "supp", r"\$\[-0\.005, (?P<v>[+-]?[\d.]+)\]\$ at\s+\$500\$\)", "unc('nonane','dHvap',500,'ci95_hi')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_b500", "supp", r"\+0\.119\]\$ at\s+\$(?P<v>\d+)\$\)", "BUDGETS[1]", 0, "budget"),
    E("s4_ci_ridge_lo", "supp", r"LO minus ridge on the\s+nonanes, \$\[(?P<v>-?[\d.]+), \+0\.032\]\$", "unc('nonane','dHvap',200,'ci95_lo_ridge')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_ridge_hi", "supp", r"nonanes,\s+\$\[\-0\.101,\s+(?P<v>[+-]?[\d.]+)\]\$\.\s+For", "unc('nonane','dHvap',200,'ci95_hi_ridge')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_tb_lo", "supp", r"intervals are wide \(\$\[(?P<v>-?[\d.]+), \+0\.222\]\$ for LO minus GM", "unc('nonane','T_B',200,'ci95_lo')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_tb_hi", "supp", r"wide\s+\(\$\[\-0\.212,\s+(?P<v>[+-]?[\d.]+)\]\$\s+for", "unc('nonane','T_B',200,'ci95_hi')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_dhf_lo", "supp", r"is worse\s+\(\$\[(?P<v>-?[\d.]+), -0\.044\]\$\)", "unc('octane','dHf',200,'ci95_lo')", 0.0005, "uncertainty_exploratory.csv"),
    E("s4_ci_dhf_hi", "supp", r"\(\$\[-0\.281, (?P<v>-?[\d.]+)\]\$\)\. All these intervals", "unc('octane','dHf',200,'ci95_hi')", 0.0005, "uncertainty_exploratory.csv"),
]

UNCHECKABLE = [e["id"] for e in REGISTRY if e["expected"] is None]

# --------------------------------------------------------------------------
# self-check
# --------------------------------------------------------------------------
def evaluate(entry):
    exp_ = entry["expected"]
    return eval(exp_, globals()) if isinstance(exp_, str) else exp_


def check(verbose=True):
    """Return (n_entries, n_checkable, n_match, mismatches, pattern_problems)."""
    tex = {"main": text("main.tex"), "supp": text("supplement.tex")}
    ids = [e["id"] for e in REGISTRY]
    assert len(ids) == len(set(ids)), "duplicate ids"
    n_match = 0; mism = []; patt = []
    for e in REGISTRY:
        hits = re.findall(e["pattern"], tex[e["file"]])
        if len(hits) != 1:
            patt.append((e["id"], len(hits))); continue
        got = hits[0]
        if e["expected"] is None:
            continue
        try:
            exp_ = evaluate(e)
        except Exception as ex:                      # evaluation error counts as a mismatch
            mism.append((e["id"], got, f"EVAL ERROR {type(ex).__name__}: {ex}", e["note"])); continue
        if isinstance(exp_, str):
            ok = (got == exp_)
        else:
            ok = abs(fnum(got) - float(exp_)) <= e["tol"] + 1e-12
        if ok:
            n_match += 1
        else:
            mism.append((e["id"], got, exp_, e["note"]))
    n_check = len(REGISTRY) - len(UNCHECKABLE)
    if verbose:
        print(f"entries {len(REGISTRY)}  checkable {n_check}  match {n_match}  "
              f"mismatch {len(mism)}  uncheckable {len(UNCHECKABLE)}  pattern problems {len(patt)}")
        for p in patt:
            print("  PATTERN", p)
        for m in mism:
            print("  MISMATCH", m[0], "tex=", m[1], "expected=", m[2], "|", m[3])
    return len(REGISTRY), n_check, n_match, mism, patt


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        REPO = sys.argv[1]
    check()
