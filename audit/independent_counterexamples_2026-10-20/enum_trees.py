"""Enumerate all non-isomorphic trees of orders 2..17 (networkx WROM generator) and store
the multiset of degree-pair profiles per order. Single process."""
import pickle, time, sys
from collections import Counter
import networkx as nx
from common import profile_of_graph

OUT = sys.argv[1] if len(sys.argv) > 1 else "profiles_2_17.pkl"
res = {}
t0 = time.time()
for n in range(2, 18):
    c = Counter()
    N = 0
    for T in nx.nonisomorphic_trees(n):
        N += 1
        c[profile_of_graph(T)] += 1
    res[n] = {"N": N, "profiles": c}
    print(n, N, len(c), f"{time.time()-t0:.1f}s", flush=True)
pickle.dump(res, open(OUT, "wb"))
