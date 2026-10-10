#!/usr/bin/env python3
"""Generate the verification notebooks in notebooks/ (run from the repository root)."""
import os, sys
import nbformat as nbf

OUT = sys.argv[1] if len(sys.argv) > 1 else "notebooks"
REPO_URL = "https://github.com/Singati2/LOYOLA-PAPER"
COLAB = "https://colab.research.google.com/github/Singati2/LOYOLA-PAPER/blob/main/notebooks/{}"

SETUP = r'''# Setup: runs inside the repository, or on Google Colab (clones the repository first).
import os, sys, subprocess
if os.path.exists("../verify.py"):
    os.chdir("..")
elif not os.path.exists("verify.py"):
    if not os.path.exists("LOYOLA-PAPER"):
        subprocess.run(["git", "clone", "--depth", "1", "https://github.com/Singati2/LOYOLA-PAPER.git"], check=True)
    os.chdir("LOYOLA-PAPER")
if "google.colab" in sys.modules:
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt", "pandas", "scikit-learn"], check=True)
ROOT = os.getcwd()
for p in (ROOT, os.path.join(ROOT, "external"), os.path.join(ROOT, "external", "bp"), os.path.join(ROOT, "structural")):
    if p not in sys.path:
        sys.path.insert(0, p)
print("working directory:", ROOT)'''

HELPERS = r'''import re, csv, time
import numpy as np, pandas as pd
RESULTS = []

def check(what, paper, got, tol=0.0):
    """Record one comparison between a value printed in the paper and the recomputed value."""
    if isinstance(paper, (int, float)) and not isinstance(paper, bool):
        ok = abs(float(paper) - float(got)) <= tol + 1e-12
    else:
        ok = paper == got
    RESULTS.append({"check": what, "paper": paper, "recomputed": got, "status": "OK" if ok else "MISMATCH"})
    print(f"{'OK      ' if ok else 'MISMATCH'} {what}: paper {paper}, recomputed {got}")
    return ok

def run(cmd, tail=25):
    """Run a repository script, show the end of its output and require exit status 0."""
    t = time.time()
    env = {k: v for k, v in os.environ.items() if k != "MPLBACKEND"}   # Jupyter's inline backend must not leak into scripts
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
    out = (r.stdout + r.stderr).strip().splitlines()
    print("\n".join(out[-tail:]))
    print(f"[exit {r.returncode}, {time.time() - t:.0f} s]")
    RESULTS.append({"check": f"script: {cmd}", "paper": "exit 0", "recomputed": f"exit {r.returncode}",
                    "status": "OK" if r.returncode == 0 else "MISMATCH"})
    return r.stdout'''

SUMMARY = r'''summary = pd.DataFrame(RESULTS)
display(summary) if "display" in dir() else print(summary.to_string())
n_bad = int((summary.status != "OK").sum())
print(f"{len(summary)} checks, {n_bad} mismatches")
assert n_bad == 0, "some recomputed values differ from the paper"'''


def nb(fname, title, intro, cells):
    n = nbf.v4.new_notebook()
    n.metadata = {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                  "language_info": {"name": "python"}}
    badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({COLAB.format(fname)})"
    n.cells = [nbf.v4.new_markdown_cell(f"# {title}\n\n{badge}\n\n{intro}\n\nEvery check prints the value in the paper "
                                        "next to the recomputed value. The last cell fails if any of them differ."),
               nbf.v4.new_code_cell(SETUP), nbf.v4.new_code_cell(HELPERS)]
    for kind, src in cells:
        n.cells.append(nbf.v4.new_markdown_cell(src) if kind == "md" else nbf.v4.new_code_cell(src))
    n.cells.append(nbf.v4.new_markdown_cell("## Summary"))
    n.cells.append(nbf.v4.new_code_cell(SUMMARY))
    os.makedirs(OUT, exist_ok=True)
    nbf.write(n, os.path.join(OUT, fname))


# ---------------------------------------------------------------- 01 data
nb("01_data.ipynb", "1. The datasets",
   "Loads every dataset in `DATA/` and checks that each file is identical to the file the analyses read.",
   [("code", 'run("python DATA/build_data.py --check")'),
    ("md", "### Octane isomers (Table 4, Supplementary Table S5)"),
    ("code", '''oct = pd.read_csv("DATA/octane_properties.csv")
display(oct) if "display" in dir() else print(oct)
check("number of octane isomers", 18, len(oct))
check("dHvap of 2,2,3,3-tetramethylbutane used (kcal/mol)", 8.41, float(oct.set_index("name").loc["2,2,3,3-tetramethylbutane", "dHvap_kcal_per_mol"]))'''),
    ("md", "### Nonane isomers (Section 6.3) and measured boiling points (Section 6.4)"),
    ("code", '''non = pd.read_csv("DATA/nonane_properties.csv")
bp = pd.read_csv("DATA/boiling_points_C6_C10.csv")
print(non.head()); print(bp.head())
check("nonane isomers", 35, len(non))
check("nonane dHvap values", 34, int(non.dHvap_kcal.notna().sum()))
check("pooled C6-C10 boiling points", 100, len(bp))
check("decanes in the boiling-point cohort", 34, int((bp.n_C == 10).sum()))'''),
    ("md", "### Provenance\n\nEvery value has a source record. The tetramethylbutane audit is in `TMB_DHVAP_AUDIT.md`."),
    ("code", '''prov = pd.read_csv("DATA/octane_provenance.csv")
print(prov.classification.value_counts().to_string())
print(open("TMB_DHVAP_AUDIT.md").read()[:1500])'''),
    ])

# ---------------------------------------------------------------- 02 mathematics
nb("02_mathematics.ipynb", "2. The mathematical results (Sections 3 and 4)",
   "Lemma 3.1, the collision pairs of Theorem 3.5, Example 4.3 and the exhaustive certificates.",
   [("md", "### Lemma 3.1: the witness determinant without the pair (1,1)"),
    ("code", '''from mpmath import mp, mpf, log, matrix, det, exp, sqrt
mp.dps = 30
v = lambda i, j: [1, log(i * j), log(i + j), mpf(abs(i - j)) / (i + j)]
d = det(matrix([v(1, 2), v(1, 3), v(2, 2), v(3, 3)]))
closed = -log(mpf(3) / 2) * log(mpf(2) ** 13 / mpf(3) ** 8) / 6
check("det of (1,2),(1,3),(2,2),(3,3)", -0.0150, float(d), 5e-5)
check("closed form -(1/6) ln(3/2) ln(2^13/3^8)", float(d), float(closed), 1e-20)
check("3^8 != 2^13", True, 3 ** 8 != 2 ** 13)'''),
    ("md", "### Theorem 3.5(iii): the colliding profiles of orders 13 and 16"),
    ("code", '''from fractions import Fraction
from collections import Counter
def qhist(profile):
    h = Counter()
    for (i, j), c in profile.items():
        h[Fraction(abs(i - j), i + j)] += c
    return dict(h)
T1 = {(1,2):1, (1,3):2, (1,6):5, (2,3):2, (2,6):1, (3,3):1}
T2 = {(1,3):3, (1,6):5, (2,2):1, (2,3):2, (3,6):1}
C1 = {(1,2):2, (1,4):8, (2,4):2, (4,4):3}
C2 = {(1,4):8, (2,2):3, (2,4):4}
for name, A, B, n in (("order 13", T1, T2, 13), ("order 16, max degree 4", C1, C2, 16)):
    check(f"{name}: profiles differ", True, A != B)
    check(f"{name}: equal q-histograms", True, qhist(A) == qhist(B))
    check(f"{name}: edges = order - 1", n - 1, sum(A.values()))
print("order-13 histogram:", {str(k): v for k, v in sorted(qhist(T1).items())})'''),
    ("code", '''out = run("python structural/minimality_check.py")
m = re.search(r"sharing a q-histogram: (\\d+) \\(all trees\\), (\\d+)", out)
check("first collision order, all trees (orders 2-16 enumerated)", 13, int(m.group(1)))
check("first collision order, max degree 4", 16, int(m.group(2)))'''),
    ("md", "### Example 4.3: the sum-connectivity pair of Rada, Rodriguez and Sigarreta (2022)"),
    ("code", '''D = lambda g: 3 * (exp(g / 2) - 1) - 4 / sqrt(5) * (exp(3 * g / 5) - exp(g / 5)) + 4 / sqrt(6) * (1 - exp(g / 3))
check("D(0) = chi(S) - chi(T)", 0.0, float(D(0)), 1e-25)
check("D(1)", 0.2255, float(D(1)), 5e-5)
check("D(1e-6)", 2.4e-7, float(D(mpf("1e-6"))), 5e-9)
out = run("python structural/sumconn_pair_check.py", tail=6)
check("the order-18 trees themselves give the same D(gamma)", True, "RESULT: Example ex:sumconn confirmed" in out)
check("K4 and K_{1,3} at gamma = ln 4 (Remark 3.9)", 6.0, float(3 * exp(log(4) / 2)), 1e-20)'''),
    ("md", "### Proposition 5.2 and the interval certificates"),
    ("code", 'run("python structural/extremal_trees_check.py", tail=3)\nrun("python audit/check_mathematics.py", tail=6)'),
    ])

# ---------------------------------------------------------------- 03 degeneracy
nb("03_degeneracy.ipynb", "3. Degeneracy and first loss of discrimination (Section 4, Table 2)",
   "Enumerates all trees and counts distinct index values at 11 significant digits, as in the paper. Takes a few minutes.",
   [("code", '''import networkx as nx
from collections import Counter
import octane_data as od
def profiles(n, chem=False):
    out = set()
    for T in nx.nonisomorphic_trees(n):
        d = dict(T.degree())
        if chem and max(d.values()) > 4:
            continue
        out.add(tuple(sorted(Counter(tuple(sorted((d[u], d[v]))) for u, v in T.edges()).items())))
    return out
def distinct(profs, a, b, g):
    return len({f"{od.lo_pairs([p for p, c in P for _ in range(c)], a, b, g):.10e}" for P in profs})'''),
    ("md", "### The 106 trees of order 10 (Section 4.2)"),
    ("code", '''trees10 = list(nx.nonisomorphic_trees(10)); P10 = profiles(10)
def values10(a, b, g):
    vals = set()
    for T in trees10:
        d = dict(T.degree())
        vals.add(f"{od.lo_pairs([tuple(sorted((d[u], d[v]))) for u, v in T.edges()], a, b, g):.10e}")
    return len(vals)
check("trees of order 10", 106, len(trees10))
check("distinct profiles", 79, len(P10))
check("LO(0,0,1) degeneracy (%)", 25.5, round(100 * (1 - values10(0, 0, 1) / 106), 1))
check("M1 degeneracy (%)", 83.0, round(100 * (1 - values10(0, 1, 0) / 106), 1))
check("M2 degeneracy (%)", 67.0, round(100 * (1 - values10(1, 0, 0) / 106), 1))
check("chi distinct values", 77, values10(0, -0.5, 0))'''),
    ("md", "### Table 2: first order with fewer values than profiles"),
    ("code", '''rows = {}
for n in range(12, 18):
    for chem in (False, True):
        if not chem and n == 17:
            continue
        P = profiles(n, chem)
        rows[(n, chem)] = (len(P), distinct(P, 0, 0, 1), distinct(P, -0.5, 0, 0))
        print(n, "max degree 4" if chem else "all trees", rows[(n, chem)])
check("LO(0,0,1), all trees: order 13 values", 566, rows[(13, False)][1])
check("LO(0,0,1), all trees: order 13 profiles", 570, rows[(13, False)][0])
check("LO(0,0,1), all trees: order 12 at the floor", True, rows[(12, False)][1] == rows[(12, False)][0])
check("LO(0,0,1), max degree 4: order 16 values", 809, rows[(16, True)][1])
check("LO(0,0,1), max degree 4: order 16 profiles", 810, rows[(16, True)][0])
check("R, all trees: order 14 values", 1095, rows[(14, False)][2])
check("R, all trees: order 14 profiles", 1100, rows[(14, False)][0])
check("R, max degree 4: order 17 values", 1191, rows[(17, True)][2])
check("R, max degree 4: order 17 profiles", 1194, rows[(17, True)][0])'''),
    ("md", "### Section 4.2: what gamma recovers off the ratio plane (all trees of order 16)"),
    ("code", '''P16 = profiles(16)
check("profiles of order 16", 4069, len(P16))
for a, b, g, want in ((0, 0.5, 0, 3475), (0, 1/3, 0, 3476), (0, 0.5, 1, 4069), (0, 1/3, 1, 4069),
                      (0.5, 0, 0, 3940), (0.5, 0, 1, 4067), (-0.5, 0, 0, 4007), (-0.5, 0, 1, 4068), (0.5, -1, 0, 3996)):
    check(f"distinct values of LO({a:g},{b:.3g},{g:g})", want, distinct(P16, a, b, g))'''),
    ])

# ---------------------------------------------------------------- 04 octane
nb("04_octane_correlations.ipynb", "4. Octane correlations and the tetramethylbutane audit (Section 6.1, Table 4)",
   "Recomputes all 60 correlations of Table 4 from the data and compares each with the value printed in `main.tex`.",
   [("code", '''import octane_data as od
P = [od.alkane_pairs(r[0]) for r in od.OCTANES]
Y = {k: np.array([r[i + 1] for r in od.OCTANES]) for i, k in enumerate(od.PROPS)}
rows = [("$M_1", (0, 1, 0)), ("$M_2", (1, 0, 0)), ("$HM", (0, 2, 0)), ("${}^{m}", (-1, 0, 0)), ("$R ", (-0.5, 0, 0)),
        ("$\\\\chi", (0, -0.5, 0)), ("$H/2", (0, -1, 0)), ("$ISI", (1, -1, 0)), ("$GA", (0.5, -1, 0)), ("$AG", (-0.5, 1, 0)),
        ("$LO(0,0,1)$ &", (0, 0, 1)), ("$LO(0,0,2)$ &", (0, 0, 2))]
tex = open("main.tex").read()
tab = tex[tex.index(r"\\label{tab:lo_octane}"):]
tab = tab[tab.index(r"\\midrule"):tab.index(r"\\bottomrule")]
lines = [l for l in tab.splitlines() if "&" in l]
for (prefix, t), line in zip(rows, lines):
    printed = [float(x) for x in re.findall(r"([+-]?\\d\\.\\d{3})", line)]
    x = np.array([od.lo_pairs(p, *t) for p in P])
    for k, pv in zip(od.PROPS, printed):
        r = np.corrcoef(x, Y[k])[0, 1]
        check(f"r({line.split('&')[0].strip()[:22]}, {k})", pv, round(r, 3), 0.0006)'''),
    ("md", "### The tetramethylbutane audit (`TMB_DHVAP_AUDIT.md`)\n\n"
           "Four values are reported separately; none replaces the benchmark value."),
    ("code", '''run("python tmb_dhvap_audit.py", tail=6)
aud = pd.read_csv("tmb_dhvap_audit.csv").set_index("variant")
print(aud[["tmb_dhvap_kcal", "top_index", "top_abs_r", "abs_r_LO001"]])
for name, want in (("original", 0.984), ("excluded", 0.980), ("hypothetical liquid estimate", 0.976), ("NIST 298 K, solid to gas", 0.374)):
    check(f"|r| of LO(0,0,1) on dHvap, {name}", want, round(aud.loc[name, "abs_r_LO001"], 3), 0.0006)
    check(f"column leader, {name}", "LO(0,0,1)", aud.loc[name, "top_index"])'''),
    ])

# ---------------------------------------------------------------- 05 boiling points
nb("05_boiling_points.ipynb", "5. Pre-registered boiling-point tests (Section 6.4, Table 5)",
   "Recomputes the within-fold baselines of Table 5 and the 200-permutation check (about 5 minutes). "
   "The seed medians come from the committed run; set `RUN_SLOW = True` to recompute them (about 30 minutes) "
   "and the exploratory selection-aware resampling (about 30 minutes).",
   [("code", "RUN_SLOW = False"),
    ("code", '''import bp_tests as T
import baselines as B
rows, Pall, y, z = T.load()
dec = [i for i, r in enumerate(rows) if r["n_C"] == "10"]
base = T.baselines("A", [Pall[i] for i in dec], y[dec]) + T.baselines("B", Pall, y, z)
got = {(b[0], b[1]): float(b[3]) for b in base}
tex = open("main.tex").read()
tab = tex[tex.index(r"\\label{tab:bp}"):]
lines = [l for l in tab[tab.index(r"\\midrule"):tab.index(r"\\bottomrule")].splitlines() if "&" in l]
pa = [float(x) for x in re.findall(r"\\$([+-]?\\d+\\.\\d{3})\\$", lines[0])]
pb = [float(x) for x in re.findall(r"\\$([+-]?\\d+\\.\\d{3})\\$", lines[1])]
for name, key, i in (("Base", "mean", 0), ("Class.", "classical best", 1), ("IRLA", "IRLA", 2), ("LO_1", "LO(0,0,1) fixed", 3), ("Ridge", "ridge on degree-pair counts", 4)):
    check(f"decanes {name}", pa[i], round(got[("A", key)], 3), 0.0006)
for name, key, i in (("Base", "size only", 0), ("Class.", "size + classical best", 1), ("IRLA", "size + IRLA", 2), ("LO_1", "size + LO(0,0,1) fixed", 3), ("Ridge", "ridge on degree-pair counts", 4)):
    check(f"pooled {name}", pb[i], round(got[("B", key)], 3), 0.0006)'''),
    ("code", '''if RUN_SLOW:
    run("cd external/bp && python bp_tests.py", tail=6)
s = pd.read_csv("external/bp/bp_results_summary.csv")
print(s.T)
for line, row, lab in ((pa, s.iloc[0], "decanes"), (pb, s.iloc[1], "pooled")):
    check(f"{lab} GM median (wide box)", line[5], round(row.median_Q2_GM12, 3), 0.0006)
    check(f"{lab} LO_h median", line[6], round(row.median_Q2_LOh, 3), 0.0006)
    check(f"{lab} median dQ2", line[7], round(row.median_dQ2_LOh_GM12, 3), 0.0006)
    check(f"{lab} pre-registered verdict", "no evidence that gamma adds value", row.prereg_verdict)'''),
    ("md", "### The permutation check (selection-aware: the ridge penalty is re-chosen in every fold)"),
    ("code", '''F = np.array([B.count_vector(Pall[i]) for i in dec], float); yd = y[dec]
real = B.scores(B.outer_loo(B.fold_ridge, F, yd)[0], yd)[0]
rng = np.random.default_rng(20261005); q = []
t0 = time.time()
for _ in range(200):
    yp = rng.permutation(yd); q.append(B.scores(B.outer_loo(B.fold_ridge, F, yp)[0], yp)[0])
q = np.array(q); print(f"{time.time() - t0:.0f} s")
check("observed ridge Q2, decanes", 0.860, round(real, 3), 0.0006)
check("permutation median", -0.09, round(float(np.median(q)), 2), 0.006)
check("permutation 95th percentile", -0.01, round(float(np.percentile(q, 95)), 2), 0.006)
check("permutation maximum", 0.20, round(float(q.max()), 2), 0.006)
check("permutations reaching 0.860", 0, int((q >= real).sum()))'''),
    ("md", "### Exploratory selection-aware resampling (added after the results; not pre-registered)"),
    ("code", '''if RUN_SLOW:
    run("cd external/bp && python selection_resampling.py 500 200", tail=4)
sr = pd.read_csv("external/bp/selection_resampling_summary.csv")
print(sr)
check("decanes median dQ2", -0.110, round(sr.iloc[0].median_dQ2, 3), 0.0006)
check("decanes 2.5 percentile", -0.510, round(sr.iloc[0]["p2.5"], 3), 0.0006)
check("decanes 97.5 percentile", 0.312, round(sr.iloc[0]["p97.5"], 3), 0.0006)
check("pooled median dQ2", 0.001, round(sr.iloc[1].median_dQ2, 3), 0.0006)'''),
    ])

# ---------------------------------------------------------------- 06 verification
nb("06_verification_suite.ipynb", "6. The repository's own verification suite",
   "Runs `python verify.py` (the fast path, about 6 minutes plus about 1 minute of installation): table and prose "
   "recomputation, regression tests, certificates and the file manifest. The core verifier also regenerates the "
   "figures and compares them byte for byte, which needs the exact library versions of `requirements-lock.txt`. "
   "The notebook therefore runs the suite inside a small dedicated environment with those versions, leaving your "
   "own Python installation unchanged. The longer suites are `python verify.py --full` and `--everything`; the "
   "Lean proofs need a Lean toolchain (see `LEAN_VERIFICATION.md`).",
   [("code", '''import venv
env = os.path.join(ROOT, ".venv-verify")
py = os.path.join(env, "bin", "python")
if not os.path.exists(py):
    venv.create(env, with_pip=True)
    run(f"{py} -m pip install -q -r requirements-lock.txt", tail=3)
run(f"{py} -m pip list --format=freeze", tail=20)'''),
    ("code", '''out = run(f"{py} verify.py", tail=40)
check("fast path result", True, "ALL PASS" in out)'''),
    ])
print("notebooks written to", OUT)
