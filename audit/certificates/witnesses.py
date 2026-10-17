"""Certificate for Theorem ratio-plane (iii): builds the four witness trees exactly as described in
main.tex, checks that each is a tree of the stated order and maximum degree, that the two members of
each pair have distinct degree-pair profiles and equal q-histograms, and that attaching a pendant path
of length L at a leaf adjacent to a vertex of degree d (3 for order 13, 4 for order 16) preserves both
properties and the maximum degree for every L up to LMAX, giving every order >= 13 (>= 16 for Delta<=4)."""
import networkx as nx
from fractions import Fraction
from collections import Counter

def tree(edges):
    T = nx.Graph(edges); assert nx.is_tree(T); return T

def leaves(T, c, k, tag):           # attach k pendant leaves to c
    return [(c, f"{tag}{c}_{i}") for i in range(k)]

def profile(T):
    d = dict(T.degree()); return Counter(tuple(sorted((d[u], d[v]))) for u, v in T.edges())

def hist(T):
    h = Counter()
    for (i, j), c in profile(T).items(): h[Fraction(j - i, i + j)] += c
    return h

# order 13. T1: path c a b d e l; c has five pendant leaves, b and d one each, l is a leaf
T1 = tree([("c","a"),("a","b"),("b","d"),("d","e"),("e","l")] + leaves(None,"c",5,"x") + leaves(None,"b",1,"x") + leaves(None,"d",1,"x"))
# T2: path c b x y z; c five leaves, b one, z two
T2 = tree([("c","b"),("b","x"),("x","y"),("y","z")] + leaves(None,"c",5,"x") + leaves(None,"b",1,"x") + leaves(None,"z",2,"x"))
# order 16, Delta<=4. U1: path A B C D of degree-4 vertices; A, D three leaves; B, C one leaf and one pendant path of length 2
U1 = tree([("A","B"),("B","C"),("C","D")] + leaves(None,"A",3,"x") + leaves(None,"D",3,"x") + leaves(None,"B",1,"x") + leaves(None,"C",1,"x")
          + [("B","pB1"),("pB1","pB2"),("C","pC1"),("pC1","pC2")])
# U2: A w B and B v1 v2 v3 v4 C; A, B, C carry three, two and three leaves
U2 = tree([("A","w"),("w","B"),("B","v1"),("v1","v2"),("v2","v3"),("v3","v4"),("v4","C")] + leaves(None,"A",3,"x") + leaves(None,"B",2,"x") + leaves(None,"C",3,"x"))

def attach(T, d, L):
    """attach a pendant path of length L at a leaf whose neighbour has degree d"""
    T = T.copy(); deg = dict(T.degree())
    leaf = sorted(v for v in T if deg[v] == 1 and deg[next(iter(T[v]))] == d)[0]
    prev = leaf
    for i in range(L):
        T.add_edge(prev, ("p", i)); prev = ("p", i)
    assert nx.is_tree(T); return T

def check(G, H, n, Dmax, d, LMAX=27):
    for L in range(0, LMAX + 1):
        g, h = (G, H) if L == 0 else (attach(G, d, L), attach(H, d, L))
        assert g.number_of_nodes() == h.number_of_nodes() == n + L
        assert max(dict(g.degree()).values()) == max(dict(h.degree()).values()) == Dmax
        assert profile(g) != profile(h) and hist(g) == hist(h)
    return n + LMAX

for name, G, H, n, Dmax, d in (("order 13", T1, T2, 13, 6, 3), ("order 16, Delta<=4", U1, U2, 16, 4, 4)):
    print(name, "profiles", dict(sorted(profile(G).items())), "|", dict(sorted(profile(H).items())))
    print("   q-histogram", {str(k): v for k, v in sorted(hist(G).items())})
    print("   OK for every order from", n, "to", check(G, H, n, Dmax, d), "(distinct profiles, equal histograms, same max degree", Dmax, ")")
