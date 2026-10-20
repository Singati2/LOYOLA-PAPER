"""Structure sensitivity (Furtula-Gutman-Dehmer) on the 75 decane trees, written from the definition:
S(G) = non-isomorphic trees in the class (n=10, Delta<=4) obtained from G by deleting one edge and
adding one other edge (graph edit distance two), excluding G itself."""
import itertools, math, json
import networkx as nx
from common import tree_canon

trees = [T for T in nx.nonisomorphic_trees(10) if max(d for _, d in T.degree()) <= 4]
canon = lambda G: tree_canon({v: list(G[v]) for v in G})
C = [canon(T) for T in trees]
idx = {c: k for k, c in enumerate(C)}
assert len(trees) == 75 and len(idx) == 75

nbrs = []
for k, T in enumerate(trees):
    s = set()
    for (u, v) in list(T.edges()):
        H = T.copy(); H.remove_edge(u, v)
        A = nx.node_connected_component(H, u); B = set(T) - A
        for x in A:
            for y in B:
                if {x, y} == {u, v}:
                    continue
                H2 = H.copy(); H2.add_edge(x, y)
                if H2.degree(x) > 4 or H2.degree(y) > 4:
                    continue
                c = canon(H2)
                if c != C[k]:
                    s.add(idx[c])
    nbrs.append(s)
sizes = [len(s) for s in nbrs]
sym = all(k in nbrs[j] for k in range(75) for j in nbrs[k])

def lo(T, a, b, g, f=None):
    tot = 0.0
    for u, v in T.edges():
        i, j = T.degree(u), T.degree(v)
        tot += (i * j) ** a * (i + j) ** b * math.exp(g * abs(i - j) / (i + j)) if f is None else f(i, j)
    return tot

IDX = {
    "M1": lambda T: lo(T, 0, 1, 0), "M2": lambda T: lo(T, 1, 0, 0), "HM": lambda T: lo(T, 0, 2, 0),
    "mM2": lambda T: lo(T, -1, 0, 0), "R": lambda T: lo(T, -.5, 0, 0), "chi": lambda T: lo(T, 0, -.5, 0),
    "H/2": lambda T: lo(T, 0, -1, 0), "ISI": lambda T: lo(T, 1, -1, 0), "GA": lambda T: 2 * lo(T, .5, -1, 0),
    "AG": lambda T: .5 * lo(T, -.5, 1, 0), "LO(0,0,1)": lambda T: lo(T, 0, 0, 1), "LO(0,0,2)": lambda T: lo(T, 0, 0, 2),
    "LO(0,0,0.5)": lambda T: lo(T, 0, 0, .5), "LO(0,0,5)": lambda T: lo(T, 0, 0, 5),
    "IRLA": lambda T: lo(T, 0, 0, 0, f=lambda i, j: 2 * abs(i - j) / (i + j)),
}
res = {"n_trees": 75, "S_sizes_min_max": [min(sizes), max(sizes)], "symmetric": sym}
for name, f in IDX.items():
    vals = [f(T) for T in trees]
    ss = [sum(abs(vals[j] - vals[k]) / vals[k] for j in nbrs[k]) / len(nbrs[k]) for k in range(75)]
    ab = [max(abs(vals[j] - vals[k]) / vals[k] for j in nbrs[k]) for k in range(75)]
    SS, AB = sum(ss) / 75, sum(ab) / 75
    res[name] = {"SS": round(SS, 4), "Abr": round(AB, 4), "ratio": round(SS / AB, 4)}
    print(name, res[name], flush=True)
print(res["S_sizes_min_max"], sym)
json.dump(res, open("fgd_decanes_out.json", "w"), indent=1)
