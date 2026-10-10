import networkx as nx, mpmath as mp
from fractions import Fraction as F
mp.mp.dps = 50
def LO(G, a, b, g):
    s = mp.mpf(0)
    for u, v in G.edges():
        du, dv = G.degree(u), G.degree(v)
        q = mp.mpf(abs(du-dv))/(du+dv)
        s += mp.power(du*dv, a)*mp.power(du+dv, b)*mp.e**(g*q)
    return s
def circ(n, D):
    return nx.circulant_graph(n, range(1, D//2+1))
# the K9 / C72 example
print("C72", LO(nx.cycle_graph(72), 0, mp.mpf(1)/2, 1), "K9", LO(nx.complete_graph(9), 0, mp.mpf(1)/2, 1))
# (alpha, beta) with kappa = p/r, gamma algebraic
cases = [(F(0),F(1,2)), (F(0),F(-1,2)), (F(-1),F(-1,2)), (F(1,2),F(1,2)), (F(0),F(1,3)), (F(-1),F(-1,3)), (F(1,4),F(3,4)), (F(-2),F(1,2))]
for a, b in cases:
    k = 2*a+b; p, r = k.numerator, k.denominator; D = 2**(r+1); e = p+r
    n = (D+1)*2**max(0,-e); N = (D+1)*2**max(0,e)
    H, G = circ(n, D), nx.cycle_graph(N)
    assert nx.is_connected(H) and all(d == D for _, d in H.degree()) and H.number_of_edges() == n*D//2
    for g in (1, mp.sqrt(2), mp.mpf(-3)/7):
        x, y = LO(G, mp.mpf(a.numerator)/a.denominator, mp.mpf(b.numerator)/b.denominator, g), LO(H, mp.mpf(a.numerator)/a.denominator, mp.mpf(b.numerator)/b.denominator, g)
        assert abs(x-y) < mp.mpf(10)**-40*abs(x), (a, b, g, x, y)
    print(f"alpha={a} beta={b} kappa={k} D={D} e={e}: C_{N} vs {D}-regular circulant on {n}: LO equal = {mp.nstr(x,15)}")
