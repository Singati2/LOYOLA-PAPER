"""Order-10 sharing count, identity of the colliding profile classes at 13 (all) / 16 (Delta<=4),
and exhaustive path/star extremality (Prop. 9) on all trees of orders 4..17."""
import pickle, json
from collections import defaultdict
from fractions import Fraction as F
import mpmath as mp
from common import qhist, maxdeg, lo_mp

mp.mp.dps = 50
res = pickle.load(open("profiles_2_17.pkl", "rb"))
out = {}

# order 10: trees sharing LO(0,0,1) (== q-hist class) with another tree
pr = res[10]["profiles"]
cls = defaultdict(int)
for p, c in pr.items():
    cls[qhist(p)] += c
share = sum(c for c in cls.values() if c > 1)
out["order10_trees_sharing_LO001"] = share
out["order10_degeneracy"] = {k: round(100 * (1 - v / 106), 1) for k, v in {"floor/LO/R/GA/AG": 79, "chi": 77, "M1": 18, "M2": 35}.items()}

# colliding q-hist classes
def coll(n, mol):
    g = defaultdict(list)
    for p in res[n]["profiles"]:
        if mol and maxdeg(p) > 4:
            continue
        g[qhist(p)].append(p)
    return [v for v in g.values() if len(v) > 1]
P = lambda d: tuple(sorted(d.items()))
p13a = P({(1, 2): 1, (1, 3): 2, (1, 6): 5, (2, 3): 2, (2, 6): 1, (3, 3): 1})
p13b = P({(1, 3): 3, (1, 6): 5, (2, 2): 1, (2, 3): 2, (3, 6): 1})
p16a = P({(1, 2): 2, (1, 4): 8, (2, 4): 2, (4, 4): 3}); p16b = P({(1, 4): 8, (2, 2): 3, (2, 4): 4})
c13 = coll(13, False); c16 = coll(16, True)
out["order13_all_colliding_classes"] = [[str(p) for p in v] for v in c13]
out["order13_pair_in_classes"] = any(p13a in v and p13b in v for v in c13)
out["order16_mol_colliding_classes"] = [[str(p) for p in v] for v in c16]
out["order16_pair_is_unique_class"] = len(c16) == 1 and set(c16[0]) == {p16a, p16b}
out["first_order_qhist_collision"] = {s: min(n for n in range(2, 18) if coll(n, s == "mol")) for s in ("all", "mol")}

# extremal trees
path = lambda n: P({(1, 2): 2, (2, 2): n - 3}) if n >= 4 else None
star = lambda n: P({(1, n - 1): n - 1})
ok = True; chem_eq = []
for n in range(4, 18):
    profs = list(res[n]["profiles"])
    for g in (mp.mpf("0.5"), mp.mpf(1), mp.mpf(2), mp.mpf(-1)):
        vals = {p: lo_mp(p, 0, 0, g, mp) for p in profs}
        lo_b = (n - 3) + 2 * mp.e ** (g / 3); hi_b = (n - 1) * mp.e ** (g * mp.mpf(n - 2) / n)
        mn = min(vals.values()); mx = max(vals.values())
        argmn = [p for p, v in vals.items() if v - mn < mp.mpf(10) ** -40]
        argmx = [p for p, v in vals.items() if mx - v < mp.mpf(10) ** -40]
        # path and star profiles each realised by exactly one tree
        if g > 0:
            good = argmn == [path(n)] and argmx == [star(n)] and mp.almosteq(mn, lo_b, 1e-40) and mp.almosteq(mx, hi_b, 1e-40)
        else:
            good = argmx == [path(n)] and argmn == [star(n)] and mp.almosteq(mx, lo_b, 1e-40) and mp.almosteq(mn, hi_b, 1e-40)
        good &= res[n]["profiles"][path(n)] == 1 and res[n]["profiles"][star(n)] == 1
        ok &= good
        if g > 0:
            chem = [v for p, v in vals.items() if maxdeg(p) <= 4]
            bnd = (n - 1) * mp.e ** (3 * g / 5)
            ok &= all(v <= bnd + mp.mpf(10) ** -40 for v in chem)
            if any(mp.almosteq(v, bnd, 1e-40) for v in chem):
                chem_eq.append(n)
out["extremal_path_star_orders4_17_gamma_0.5_1_2_-1"] = ok
out["chemical_bound_equality_orders"] = sorted(set(chem_eq))
print(json.dumps(out, indent=1))
json.dump(out, open("extra_out.json", "w"), indent=1)
