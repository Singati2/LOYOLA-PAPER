#!/usr/bin/env python3
"""Independent counter-attacks on the three v40.30 fixes (written without the repository checkers).

T1  press_size. Leave-one-out PRESS for y ~ 1 + z + x is undefined exactly when deleting some row i
    leaves a rank-deficient design, which (for a full-rank full design) is equivalent to h_ii = 1.
    The old implementation (git 0c4a4db) is loaded from git and compared with the current one on:
    (a) the outside audit's five-point design, whose deletion of row 0 is rank 2 for every
        perturbation delta of x[0], so the fit is undefined and inf is correct;
    (b) a family that is valid but nearly singular: x[1] is also perturbed by eps, so every deletion
        has full rank and 1 - h_00 shrinks with eps; the reference is explicit leave-one-out least
        squares in 60-digit mpmath;
    (c) 400 random well-posed designs (n = 8 to 40), where nothing may be rejected and both versions
        must equal the reference.
T2  constancy coverage. The candidate triples of every generator that selects on the octanes with
    its own constancy test (expanded_robustness_v35, tmb_exclusion_sensitivity, ablation_gm_vs_lo,
    ablation_robustness) are rebuilt from their own sampling recipes, the octane degree pairs are
    recomputed from the SMILES with a parser written here, and the smallest relative range over all
    outer and inner training folds is recomputed.
T3  entropy lists. The two lists of supplement item (i) are parsed from supplement.tex, checked
    disjoint, totalling 13, and compared with the provenance CSV.
  cd audit/final/scripts && python3 counterattack_v4030.py      -> counterattack_v4030_out.txt
"""
import csv, importlib.util, os, re, subprocess, sys, tempfile
import numpy as np
import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, "external")); sys.path.insert(0, os.path.join(ROOT, "external", "bp"))
import bp_tests as NEW
out = []


def load_old():
    src = subprocess.run(["git", "show", "0c4a4db:external/bp/bp_tests.py"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    f = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False); f.write(src); f.close()
    spec = importlib.util.spec_from_file_location("bp_old", f.name); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def loo_ref(x, z, y, dps=60):
    """Explicit leave-one-out RMSE in high precision; None if a deletion is rank deficient."""
    mp.mp.dps = dps; n = len(y); e = []
    for i in range(n):
        rows = [k for k in range(n) if k != i]
        A = mp.matrix([[1, mp.mpf(z[k]), mp.mpf(x[k])] for k in rows]); b = mp.matrix([mp.mpf(y[k]) for k in rows])
        M = A.T * A
        if abs(mp.det(M)) < mp.mpf(10) ** (-dps // 2): return None
        c = mp.lu_solve(M, A.T * b)
        e.append(mp.mpf(y[i]) - (c[0] + c[1] * z[i] + c[2] * x[i]))
    return float(mp.sqrt(sum(v * v for v in e) / n))


OLD = load_old()
z = np.arange(1., 6.); y = np.array([2., -1., 3., 4., 0.])
# T1(a)
for d in (1e-1, 1e-4, 1e-7):
    x = z.copy(); x[0] += d
    o, nw = OLD.press_size(x[None, :], z, y)[0], NEW.press_size(x[None, :], z, y)[0]
    out.append(f"T1a delta={d:g}: deleted rank {np.linalg.matrix_rank(np.column_stack([np.ones(4), z[1:], x[1:]]))}; old {o:.6g}; new {nw}; reference {loo_ref(x, z, y)}")
# T1(b)
for eps in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5):
    x = z.copy(); x[0] += 0.5; x[1] += eps
    ref = loo_ref(x, z, y); o, nw = OLD.press_size(x[None, :], z, y)[0], NEW.press_size(x[None, :], z, y)[0]
    A = np.column_stack([np.ones(5), (z - z.mean()) / z.std(), x]); U, _, _ = np.linalg.svd(A, full_matrices=False)
    gap = float((1 - (U ** 2).sum(1)).min())
    rel = (lambda v: "rejected" if not np.isfinite(v) else f"{abs(v - ref) / ref:.1e}")
    out.append(f"T1b eps={eps:g}: min(1-h) {gap:.2e}; reference {ref:.6g}; old rel.err {rel(o)}; new rel.err {rel(nw)}")
# T1(c)
rng = np.random.default_rng(7); bad = 0; worst = 0.0
for t in range(400):
    n = int(rng.integers(8, 41)); zz = rng.normal(size=n); xx = rng.normal(size=n); yy = rng.normal(size=n)
    ref = loo_ref(xx, zz, yy, dps=40); a, b = OLD.press_size(xx[None, :], zz, yy)[0], NEW.press_size(xx[None, :], zz, yy)[0]
    if not (np.isfinite(b) and a == b): bad += 1
    worst = max(worst, abs(b - ref) / ref)
out.append(f"T1c 400 random well-posed designs: rejected or old != new in {bad}; max rel. error vs 40-digit reference {worst:.1e}")

# T2
def degrees(smiles):
    """Carbon degrees of an acyclic alkane SMILES (C, parentheses only) and its edge list."""
    deg, edges, stack, prev = [], [], [], None
    for ch in smiles:
        if ch == "C":
            deg.append(0); cur = len(deg) - 1
            if prev is not None: edges.append((prev, cur)); deg[prev] += 1; deg[cur] += 1
            prev = cur
        elif ch == "(": stack.append(prev)
        elif ch == ")": prev = stack.pop()
        else: raise ValueError(smiles)
    return [(deg[a], deg[b]) for a, b in edges]

sys.path.insert(0, ROOT)
from octane_data import OCTANES, NAMES
pairs = [degrees(r[0]) for r in OCTANES]
assert all(len(p) == 7 for p in pairs)

def lo(P, a, b, g):
    return sum(np.exp(a * np.log(i * j) + b * np.log(i + j) + g * abs(i - j) / (i + j)) for i, j in P)

trip = []
def stream(seed, budget, lz):
    r = np.random.default_rng(seed); L = np.round(r.uniform(-2, 2, (budget, 3)), 3); G = np.round(r.uniform(-2, 2, (budget, 2)), 3)
    trip.extend(map(tuple, L)); trip.extend((a, b, 0.0) for a, b in G)
    if lz: trip.extend((a, b, 0.0) for a, b, _ in L)
for s in range(100):
    for b in (200, 500): stream(s, b, True)            # expanded_robustness_v35, tmb_exclusion_sensitivity
stream(12345, 200, False)                              # ablation_gm_vs_lo
for s in (12345, 777, 2024):
    for b in (200, 500): stream(s, b, False)           # ablation_robustness
T = np.unique(np.array(trip), axis=0)
X = np.array([[lo(P, *t) for P in pairs] for t in T])
idx18 = list(range(18)); idx17 = [k for k in idx18 if NAMES[k] != "2,2,3,3-tetramethylbutane"]
folds = []
for base in (idx18, idx17):
    for i in base:
        o = [k for k in base if k != i]; folds.append(o)
        folds += [[k for k in o if k != j] for j in o]   # inner folds
minrel = min(float(((X[:, f].max(1) - X[:, f].min(1)) / np.abs(X[:, f]).max(1)).min()) for f in folds)
out.append(f"T2 distinct triples over all four generators {len(T)} (current checker: 163487 without ablation_robustness); "
           f"folds {len(folds)} (outer and inner); smallest relative range {minrel:.3e}; exact-zero std count "
           f"{sum(int((X[:, f].std(1) == 0).sum()) for f in folds)}")

# T3
tex = open(os.path.join(ROOT, "supplement.tex")).read()
item = tex[tex.index("Thirteen gas-phase entropies"):]; item = item[:item.index("could not be matched")]
i1 = item.index("Six of them (") + 13; first = item[i1:item.index(")", i1)]; second = item[item.index("remaining seven (") + 17:]
second = second[:second.rindex(")")]
def expand(s):
    s = re.sub(r"\s+", " ", s.replace("\\-", "")); names = []
    for part in re.split(r",\s+(?:and\s+)?|\s+and\s+", s):
        names.append(part.strip())
    full = []; pending = []
    for nm in names:
        if nm.endswith("-"): pending.append(nm); continue
        stem = re.sub(r"^[\d,]+-", "", nm); full += [p + stem for p in pending] + [nm]; pending = []
    return {f.strip() for f in full if f.strip()}
A, B = expand(first), expand(second)
csvS = {r["molecule"]: r["classification"] for r in csv.DictReader(open(os.path.join(ROOT, "octane_property_provenance_v35.csv"), newline="")) if r["property"] == "S"}
cv = {m for m, c in csvS.items() if c == "CANNOT VERIFY"}
out.append(f"T3 first list {len(A)}, second list {len(B)}, overlap {sorted(A & B)}, total {len(A | B)}; "
           f"second list == CANNOT VERIFY rows: {B == cv}; first list classes: {sorted({csvS[m] for m in A})}")
text = "\n".join(out) + "\n"
print(text, end="")
open(os.path.join(HERE, "counterattack_v4030_out.txt"), "w").write(text)

# T4 units, phase and temperature of every octane value (independent re-conversion)
conv = {"T_B": {"K": lambda v: v - 273.15}, "dHf": {"kJ/mol": lambda v: v / 4.184}, "dHvap": {"kJ/mol": lambda v: v / 4.184},
        "S": {"J/(mol K)": lambda v: v / 4.184, "cal/(mol K)": lambda v: v}, "omega": {"dimensionless": lambda v: v}}
tol = {"T_B": 0.15, "dHf": 0.15, "dHvap": 0.15, "S": 0.3, "omega": 0.003}
phase_ok = {"T_B": r"1 atm", "dHf": r"(?i)gas", "dHvap": r"(?i)liquid\s*->\s*gas|298", "S": r"(?i)gas", "omega": r"."}
checked = within = 0; issues = []
for r in csv.DictReader(open(os.path.join(ROOT, "octane_property_provenance_v35.csv"), newline="")):
    p = r["property"]
    if not re.search(phase_ok[p], r["phase_condition"]): issues.append(f"{r['molecule']} {p}: phase '{r['phase_condition'][:40]}'")
    if r["classification"] in ("CANNOT VERIFY",): continue
    unit = next((u for u in conv[p] if r["source_unit"].startswith(u)), None)
    m = re.match(r"\s*([-+]?\d+\.?\d*)", r["source_value"])
    if unit is None or m is None: issues.append(f"{r['molecule']} {p}: unparsed '{r['source_value'][:30]}' [{r['source_unit']}]"); continue
    checked += 1; d = abs(conv[p][unit](float(m.group(1))) - float(re.match(r"\s*([-+]?\d+\.?\d*)", r["paper_value"]).group(1)))
    if d <= tol[p] + 1e-9: within += 1
    else: issues.append(f"{r['molecule']} {p}: |converted first source value - paper| = {d:.3f} > {tol[p]} [{r['classification']}]")
out.append(f"T4 octane values re-converted from their first quoted source value: {checked}; within the audit tolerance {within}; notes:")
out += ["   " + s for s in issues]
text = "\n".join(out) + "\n"
print(text, end="")
open(os.path.join(HERE, "counterattack_v4030_out.txt"), "w").write(text)
