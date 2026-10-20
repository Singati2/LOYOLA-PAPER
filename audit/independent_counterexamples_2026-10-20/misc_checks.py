"""Small symbolic checks: Cruz-Rada f(i,j) values (main 1291), IRLA first-order expansion (main 1156)."""
import sympy as sp
g = sp.symbols("g", positive=True)
x = sp.symbols("x", positive=True)
E = sp.exp(g / 3)
phi = lambda i, j: sp.exp(g * sp.Rational(abs(i - j), i + j))
f = lambda i, j: sp.Rational(i * j, i + j) * (phi(i, j) + 2 * phi(1, 2) - 3 * phi(2, 2))
r1 = sp.simplify(f(1, 2) - 2 * (E - 1)) == 0 and sp.simplify(f(2, 2) - 2 * (E - 1)) == 0
r2 = sp.expand((x - 1) * (3 * x**2 + x + 1)) == 3 * x**3 - 2 * x**2 - 1
r3 = sp.expand(sp.Rational(3, 4) * (x**3 + 2 * x**2 - 3) - 2 * (x**2 - 1) - sp.Rational(1, 4) * (3 * x**3 - 2 * x**2 - 1)) == 0
# numeric scan: f(i,j) > 2(E-1) for all other pairs i<=j<=12, gamma in {0.1,1,5}
r4 = all(float(f(i, j).subs(g, gv)) > float((2 * (E - 1)).subs(g, gv)) for gv in (0.1, 1, 5)
         for i in range(1, 13) for j in range(i, 13) if (i, j) not in [(1, 2), (2, 2), (1, 1)])
# IRLA: d/dgamma sum exp(gamma q) at 0 = sum q = IRLA/2
qs = [sp.Rational(1, 3), sp.Rational(1, 2), 0, sp.Rational(3, 5)]
LO = sum(sp.exp(g * q) for q in qs)
r5 = sp.series(LO, g, 0, 2).removeO() == len(qs) + g / 2 * (2 * sum(qs))
print({"f(1,2)=f(2,2)=2(E-1)": r1, "factorisation": r2, "reduction_identity": r3, "f_larger_elsewhere_scan": r4, "IRLA_first_order": r5})
