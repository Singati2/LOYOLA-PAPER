"""Exact check that the partition of K = {(i,j): 1 <= i <= j <= n-1} induced by the GA weight
2*sqrt(ij)/(i+j) (Rada 2019, eq. (3)) equals the partition induced by q_ij = (j-i)/(i+j),
and equals the partition induced by gamma*q_ij for gamma != 0. Uses exact rationals:
GA_ij^2 = 4ij/(i+j)^2 = 1 - q_ij^2 and GA_ij > 0, so comparing GA^2 is exact.
Reads nothing from the repository and writes nothing. Usage: python rada_ga_partition_check.py [N]"""
import sys
from fractions import Fraction as F
N = int(sys.argv[1]) if len(sys.argv) > 1 else 60
for n in range(2, N + 1):
    K = [(i, j) for i in range(1, n) for j in range(i, n)]
    q = {e: F(e[1] - e[0], e[0] + e[1]) for e in K}
    ga2 = {e: F(4 * e[0] * e[1], (e[0] + e[1]) ** 2) for e in K}
    assert all(ga2[e] == 1 - q[e] ** 2 for e in K)
    def part(w):
        groups = {}
        for e in K:
            groups.setdefault(w[e], []).append(e)
        return sorted(groups.values())
    assert part(q) == part(ga2), n
    assert part({e: 3 * q[e] for e in K}) == part(q)          # gamma = 3 (any gamma != 0 scales injectively)
    assert part({e: -q[e] for e in K}) == part(q)             # gamma = -1
print(f"partitions induced by GA, q and gamma*q coincide on K for every n = 2..{N}")
