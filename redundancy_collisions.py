#!/usr/bin/env python3
"""Redundancy (PART 1) and BID-collision (PART 2) analysis for the 18 octanes.

Imports OCTANES, NAMES, alkane_pairs, lo_pairs from octane_data.py.
Outputs:
  descriptor_correlations.csv  (12x12 signed Pearson matrix)
  pca_spectrum.csv             (component, eigenvalue, cumvar)
  bid_collision_table.csv      (per-molecule BID profile + properties)
"""
import csv, itertools, os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from octane_data import OCTANES, NAMES, alkane_pairs, lo_pairs

WORK = os.path.dirname(os.path.abspath(__file__))
PROPS = ["T_B", "dHf", "dHvap", "S", "omega"]

# NAMES (IUPAC, same order as OCTANES) come from octane_data.py

INDICES = [("M1", (0, 1, 0)), ("M2", (1, 0, 0)), ("HM", (0, 2, 0)),
           ("mM2", (-1, 0, 0)), ("R", (-0.5, 0, 0)), ("chi", (0, -0.5, 0)),
           ("H2", (0, -1, 0)), ("ISI", (1, -1, 0)), ("GA", (0.5, -1, 0)),
           ("AG", (-0.5, 1, 0)), ("LO001", (0, 0, 1)), ("LO002", (0, 0, 2))]

# ---------------------------------------------------------------- PART 1
def part1():
    pair_lists = [alkane_pairs(r[0]) for r in OCTANES]
    X = np.array([[lo_pairs(P, *abg) for _, abg in INDICES] for P in pair_lists])
    assert X.shape == (18, 12)
    labels = [n for n, _ in INDICES]

    # signed Pearson correlation matrix (12x12)
    C = np.corrcoef(X, rowvar=False)
    with open(os.path.join(WORK, "descriptor_correlations.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow([""] + labels)
        for i, lab in enumerate(labels):
            w.writerow([lab] + [f"{C[i, j]:.10f}" for j in range(12)])

    pairs99, pairs999 = [], []
    for i, j in itertools.combinations(range(12), 2):
        r = C[i, j]
        if abs(r) >= 0.99:
            pairs99.append((labels[i], labels[j], r))
        if abs(r) >= 0.999:
            pairs999.append((labels[i], labels[j], r))

    print("=== PART 1: redundancy ===")
    print(f"pairs with |r| >= 0.99  : {len(pairs99)}")
    for a, b, r in sorted(pairs99, key=lambda t: -abs(t[2])):
        print(f"  {a:6s} {b:6s} r = {r:+.6f}")
    print(f"pairs with |r| >= 0.999 : {len(pairs999)}")
    for a, b, r in sorted(pairs999, key=lambda t: -abs(t[2])):
        print(f"  {a:6s} {b:6s} r = {r:+.6f}")

    # PCA on z-scored matrix (ddof=0)
    Z = (X - X.mean(axis=0)) / X.std(axis=0, ddof=0)
    S = (Z.T @ Z) / Z.shape[0]            # = correlation matrix
    lam = np.linalg.eigvalsh(S)[::-1]
    lam = np.clip(lam, 0, None)
    cum = np.cumsum(lam) / lam.sum()
    with open(os.path.join(WORK, "pca_spectrum.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["component", "eigenvalue", "cumvar"])
        for k in range(12):
            w.writerow([k + 1, f"{lam[k]:.8f}", f"{cum[k]:.8f}"])
    n95 = int(np.searchsorted(cum, 0.95) + 1)
    n99 = int(np.searchsorted(cum, 0.99) + 1)
    pr = lam.sum() ** 2 / (lam ** 2).sum()
    print(f"eigenvalues: {np.array2string(lam, precision=5, suppress_small=True)}")
    print(f"cumvar PC1={cum[0]:.6f}  PC1-2={cum[1]:.6f}  PC1-3={cum[2]:.6f}")
    print(f"components for 95% var: {n95};  for 99% var: {n99}")
    print(f"effective rank (participation ratio): {pr:.4f}")

# ------------------------------------------------- SMILES -> IUPAC verifier
from octane_data import alkane_adj as smiles_adj  # single validated parser

def all_longest_paths(adj):
    n = len(adj); best = []; bl = 0
    def dfs(path, seen):
        nonlocal best, bl
        ext = False
        for v in adj[path[-1]]:
            if v not in seen:
                ext = True
                dfs(path + [v], seen | {v})
        if not ext:
            if len(path) > bl:
                bl = len(path); best = [list(path)]
            elif len(path) == bl:
                best.append(list(path))
    for s in adj:
        dfs([s], {s})
    return best

def branch_size(adj, root, avoid):
    seen = {avoid}; stack = [root]; cnt = 0
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u); cnt += 1
        stack.extend(adj[u] - seen)
    return cnt

def derive_name(smi):
    """Derive IUPAC name (methyl/ethyl substituents only) from an alkane SMILES."""
    adj = smiles_adj(smi)
    parents = {4: "butane", 5: "pentane", 6: "hexane", 7: "heptane", 8: "octane"}
    cands = []
    for path in all_longest_paths(adj):
        chain = set(path)
        subs = []  # (locant, subname)
        ok = True
        for pos, atom in enumerate(path, start=1):
            for nb in adj[atom]:
                if nb in chain:
                    continue
                sz = branch_size(adj, nb, atom)
                if sz == 1:
                    subs.append((pos, "methyl"))
                elif sz == 2 and len(adj[nb] - {atom}) == 1:
                    subs.append((pos, "ethyl"))
                else:
                    ok = False  # complex substituent -> not the preferred chain
        if ok:
            cands.append((len(path), subs))
    if not cands:
        return None
    L = cands[0][0]
    # rule: among longest chains, max number of substituents, then lowest locants
    mx = max(len(s) for _, s in cands)
    cands = [s for _, s in cands if len(s) == mx]
    best = min(cands, key=lambda s: sorted(l for l, _ in s))
    if not best:
        return parents[L]
    groups = {}
    for l, nm in sorted(best):
        groups.setdefault(nm, []).append(l)
    mult = {1: "", 2: "di", 3: "tri", 4: "tetra"}
    parts = [f"{','.join(map(str, groups[nm]))}-{mult[len(groups[nm])]}{nm}"
             for nm in sorted(groups)]  # alphabetical by substituent name
    return "-".join(parts) + parents[L]

def norm_name(name):
    """Normalize a claimed name to a canonical set of (locant, sub) + parent."""
    import re
    parents = ["heptane", "hexane", "pentane", "butane", "octane"]
    for p in parents:
        if name.endswith(p):
            stem, parent = name[:-len(p)], p
            break
    subs = []
    for m in re.finditer(r"([\d,]+)-(di|tri|tetra)?(methyl|ethyl)", stem):
        for loc in m.group(1).split(","):
            subs.append((int(loc), m.group(3)))
    return parent, tuple(sorted(subs))

# ---------------------------------------------------------------- PART 2
def part2():
    print("\n=== PART 2: name verification ===")
    focus = {"3-methylheptane", "4-methylheptane", "3,4-dimethylhexane",
             "3-ethyl-2-methylpentane"}
    all_ok, focus_ok = True, True
    for name, row in zip(NAMES, OCTANES):
        smi = row[0]
        derived = derive_name(smi)
        if name == "octane":
            ok = derived == "octane"
        else:
            ok = derived is not None and norm_name(derived) == norm_name(name)
        tag = "OK " if ok else "FAIL"
        star = " *" if name in focus else ""
        print(f"  [{tag}] {smi:16s} claimed={name:26s} derived={derived}{star}")
        all_ok &= ok
        if name in focus:
            focus_ok &= ok
    print(f"focus-4 verification: {'PASS' if focus_ok else 'FAIL'}; "
          f"all-18 verification: {'PASS' if all_ok else 'FAIL'}")

    print("\n=== PART 2: BID collisions ===")
    profiles = []
    for row in OCTANES:
        pairs = sorted(tuple(sorted(p)) for p in alkane_pairs(row[0]))
        profiles.append(tuple(pairs))

    def prof_str(prof):
        out = []
        for p in sorted(set(prof)):
            out.append(f"{prof.count(p)}x({p[0]},{p[1]})")
        return ";".join(out)

    prof_id = {}
    for prof in profiles:
        if prof not in prof_id:
            prof_id[prof] = f"P{len(prof_id) + 1:02d}"
    n_unique = len(prof_id)
    classes = {}
    for name, prof in zip(NAMES, profiles):
        classes.setdefault(prof, []).append(name)

    with open(os.path.join(WORK, "bid_collision_table.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "smiles", "bid_profile", "profile_id",
                    "T_B", "dHf", "dHvap", "S", "omega", "collides_with"])
        for name, row, prof in zip(NAMES, OCTANES, profiles):
            others = [n for n in classes[prof] if n != name]
            w.writerow([name, row[0], prof_str(prof), prof_id[prof],
                        row[1], row[2], row[3], row[4], row[5],
                        ";".join(others)])

    print(f"unique BID profiles: {n_unique} / 18")
    idx = {n: i for i, n in enumerate(NAMES)}
    for prof, members in classes.items():
        if len(members) < 2:
            continue
        print(f"collision class {prof_id[prof]} [{prof_str(prof)}]: {members}")
        for a, b in itertools.combinations(members, 2):
            ra, rb = OCTANES[idx[a]], OCTANES[idx[b]]
            diffs = ", ".join(f"d{p}={ra[1+k]-rb[1+k]:+.3f}"
                              for k, p in enumerate(PROPS))
            print(f"  {a} vs {b}: {diffs}")

if __name__ == "__main__":
    part1()
    part2()
