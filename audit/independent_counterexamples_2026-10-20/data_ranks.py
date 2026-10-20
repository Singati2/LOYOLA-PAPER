"""Remark 'Dimension of the counts': ranks of centred count matrices of the 34 measured decanes and the
100 pooled alkanes. Molecule membership is taken from the repository data file (data only); degree
pairs are re-derived here independently by parsing the InChI connection layer, then compared with the
file's own degree_pairs column."""
import csv, sys, re, json
from collections import Counter
from fractions import Fraction as F
import numpy as np

PATH = sys.argv[1]

def parse_inchi(inchi):
    layer = [p for p in inchi.split("/") if p.startswith("c")][0][1:]
    toks = re.findall(r"\d+|[()\-,]", layer)
    edges, stack, prev = [], [], None
    for t in toks:
        if t.isdigit():
            a = int(t)
            if prev is not None:
                edges.append((prev, a))
            prev = a
        elif t == "(":
            stack.append(prev)
        elif t == ",":
            prev = stack[-1]
        elif t == ")":
            prev = stack.pop()
    return edges

rows = list(csv.DictReader(open(PATH)))
pairs10 = [(i, j) for i in range(1, 5) for j in range(i, 5) if (i, j) != (1, 1)]
mats = {"decanes": [], "pooled": []}
mism = 0
ident_ok = True
for r in rows:
    E = parse_inchi(r["inchi_skeleton"])
    deg = Counter()
    for a, b in E:
        deg[a] += 1; deg[b] += 1
    n = int(r["n_C"])
    assert len(deg) == n and len(E) == n - 1
    prof = Counter(tuple(sorted((deg[a], deg[b]))) for a, b in E)
    filep = Counter(tuple(int(x) for x in s.split("-")) for s in r["degree_pairs"].split())
    mism += prof != filep
    ident_ok &= sum(m * (F(1, i) + F(1, j)) for (i, j), m in prof.items()) == n
    vec = [prof.get(p, 0) for p in pairs10]
    mats["pooled"].append(vec)
    if n == 10:
        mats["decanes"].append(vec)
out = {"rows": len(rows), "inchi_vs_file_profile_mismatches": mism, "vertex_identity_holds": ident_ok}
for k, M in mats.items():
    M = np.array(M, float)
    out[k] = {"N": len(M), "centred_rank": int(np.linalg.matrix_rank(M - M.mean(0)))}
print(out)
json.dump(out, open("data_ranks_out.json", "w"), indent=1)
