# Extra counts: chi at orders 7..12 (all and Delta<=4); (1/3,0,gamma) and (1/6,0,gamma) at order 16.
import networkx as nx, mpmath as mp
from collections import Counter
mp.mp.dps = 50
def prof(T):
    d = dict(T.degree()); return tuple(sorted(Counter(tuple(sorted((d[u], d[v]))) for u, v in T.edges()).items()))
def distinct(vals):
    vs = sorted(vals); k = 1
    for a, b in zip(vs, vs[1:]):
        if b - a > mp.mpf(10)**-40 * max(1, abs(a)): k += 1
    return k
def val(p, a, b, g): return mp.fsum(m * mp.power(i*j, a) * mp.power(i+j, b) * mp.exp(g*mp.mpf(j-i)/(i+j)) for (i, j), m in p)
for n in range(7, 13):
    P = {prof(T) for T in nx.nonisomorphic_trees(n)}
    Pc = {p for p in P if max(j for (i, j), m in p) <= 4}
    print(n, "chi all", distinct([val(p, 0, -0.5, 0) for p in P]), "/", len(P), " chem", distinct([val(p, 0, -0.5, 0) for p in Pc]), "/", len(Pc))
P = {prof(T) for T in nx.nonisomorphic_trees(16)}
for a, b, g in [(mp.mpf(1)/3, 0, 0), (mp.mpf(1)/3, 0, 1), (mp.mpf(1)/6, 0, 0), (mp.mpf(1)/6, 0, 1), (0, -0.5, 0), (0, -0.5, 1)]:
    print("order16", (a, b, g), distinct([val(p, a, b, g) for p in P]))
