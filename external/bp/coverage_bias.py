#!/usr/bin/env python3
"""Coverage-bias check for the decane boiling-point cohort: are the 34
included decanes structurally different from the 41 excluded ones (31 with
no NIST boiling point, 10 with determinations spreading > 3 K)?
Compares branching and imbalance descriptors with a two-sided permutation
test on the difference in means (20000 permutations, rng 20261005).
Writes coverage_bias.csv."""
import csv, math, os
import numpy as np, networkx as nx

HERE = os.path.dirname(os.path.abspath(__file__))
import importlib.util
spec = importlib.util.spec_from_file_location("bb", os.path.join(HERE, "build_bp_data.py")); bb = importlib.util.module_from_spec(spec); spec.loader.exec_module(bb)


def feats(G):
    d = dict(G.degree()); P = [tuple(sorted((d[u], d[v]))) for u, v in G.edges()]
    q = [abs(i - j) / (i + j) for i, j in P]
    return {"tertiary C (deg 3)": sum(1 for x in d.values() if x == 3),
            "quaternary C (deg 4)": sum(1 for x in d.values() if x == 4),
            "methyl groups (deg 1)": sum(1 for x in d.values() if x == 1),
            "Wiener index": nx.wiener_index(G),
            "IRLA = 2 sum q": 2 * sum(q),
            "LO(0,0,1)": sum(math.exp(x) for x in q),
            "Randic R": sum((i * j) ** -0.5 for i, j in P)}


def main():
    prov = {r["nist_id"]: r for r in csv.DictReader(open(os.path.join(HERE, "bp_provenance.csv")))}
    sk = [a for a in csv.DictReader(open(os.path.join(HERE, "nist_alkanes_skeletons_audit.csv"))) if a["n"] == "10"]
    inc, exc = [], []
    for a in sk:
        G = bb.inchi_tree(a["skel"], 10)
        status = None
        for cid in a["ids"].split():
            if cid in prov:
                status = prov[cid]["status"]; break
        if status is None:  # provenance keyed by first id for excluded entries
            status = next((r["status"] for r in prov.values() if r["n_C"] == "10" and r["nist_id"] == a["ids"]), "EXCLUDED")
        (inc if status == "INCLUDED" else exc).append(feats(G))
    rng = np.random.default_rng(20261005); rows = []
    for k in inc[0]:
        x = np.array([f[k] for f in inc], float); y = np.array([f[k] for f in exc], float)
        obs = x.mean() - y.mean(); allv = np.r_[x, y]; n = len(x); cnt = 0
        for _ in range(20000):
            rng.shuffle(allv); cnt += abs(allv[:n].mean() - allv[n:].mean()) >= abs(obs) - 1e-12
        rows.append([k, len(x), len(y), f"{x.mean():.3f}", f"{y.mean():.3f}", f"{obs:+.3f}", f"{(cnt + 1) / 20001:.4f}"])
        print(rows[-1])
    with open(os.path.join(HERE, "coverage_bias.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["feature", "n_included", "n_excluded", "mean_included", "mean_excluded", "difference", "perm_p_two_sided"]); w.writerows(rows)


if __name__ == "__main__":
    main()
