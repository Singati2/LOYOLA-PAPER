#!/usr/bin/env python3
"""Single source of truth for the 18-isomer octane dataset (v36).

Every analysis script, the figure generator and the verifier import OCTANES
from this module; no other file carries a copy of the data.

Columns of OCTANES rows: (SMILES, T_B [deg C], dH_f [kcal/mol, gas, 298 K],
dH_vap [kcal/mol, 298 K], S [cal/(mol K), gas, 298 K], omega [-]).
NAMES[i] is the IUPAC name of OCTANES[i]; the order matches the manuscript
appendix table (tab:octane-data).

v36 data corrections (NIST WebBook phase-change data; identical to the
standard octane QSPR dataset, arXiv:1701.02859 Table 1, to 2 dp):
  3,3-dimethylhexane       dH_vap 9.04 -> 8.97
  3-ethyl-3-methylpentane  dH_vap 9.21 -> 9.08
  2,2,3-trimethylpentane   dH_vap 8.88 -> 8.83
  2,3,3-trimethylpentane   dH_vap 9.02 -> 8.90
(3-ethyl-2-methylpentane dH_vap 9.21 is correct and unchanged.)
"""
import math

PROPS = ["T_B", "dHf", "dHvap", "S", "omega"]

OCTANES = [
    ('CCCCCCCC',         125.6, -49.82, 9.92, 111.55, 0.398),
    ('CC(C)CCCCC',       117.6, -51.50, 9.48, 109.84, 0.378),
    ('CCC(C)CCCC',       118.9, -50.82, 9.52, 111.26, 0.371),
    ('CCCC(C)CCC',       117.7, -50.69, 9.48, 109.32, 0.372),
    ('CC(C)(C)CCCC',     106.8, -53.71, 8.92, 103.13, 0.339),
    ('CC(C)C(C)CCC',     115.6, -51.13, 9.27, 108.02, 0.348),
    ('CC(C)CC(C)CC',     109.4, -52.44, 9.03, 106.98, 0.344),
    ('CC(C)CCC(C)C',     109.1, -53.21, 9.05, 105.72, 0.357),
    ('CCCC(C)(C)CC',     111.9, -52.61, 8.97, 104.74, 0.322),
    ('CCC(C)C(C)CC',     117.7, -50.91, 9.32, 106.59, 0.340),
    ('CCC(CC)C(C)C',     115.6, -50.48, 9.21, 106.06, 0.330),
    ('CCC(C)(CC)CC',     118.3, -51.38, 9.08, 101.48, 0.302),
    ('CCC(CC)CCC',       118.5, -50.40, 9.48, 109.43, 0.362),
    ('CCC(C)C(C)(C)C',   109.8, -52.61, 8.83, 101.31, 0.300),
    ('CC(C)CC(C)(C)C',    99.2, -53.57, 8.40, 101.81, 0.305),
    ('CCC(C)(C)C(C)C',   114.8, -51.73, 8.90, 101.31, 0.291),
    ('CC(C)C(C)C(C)C',   113.5, -51.97, 9.01, 102.39, 0.317),
    ('CC(C)(C)C(C)(C)C', 106.5, -53.99, 8.41,  93.06, 0.247),
]

NAMES = ["octane", "2-methylheptane", "3-methylheptane", "4-methylheptane",
         "2,2-dimethylhexane", "2,3-dimethylhexane", "2,4-dimethylhexane",
         "2,5-dimethylhexane", "3,3-dimethylhexane", "3,4-dimethylhexane",
         "3-ethyl-2-methylpentane", "3-ethyl-3-methylpentane", "3-ethylhexane",
         "2,2,3-trimethylpentane", "2,2,4-trimethylpentane",
         "2,3,3-trimethylpentane", "2,3,4-trimethylpentane",
         "2,2,3,3-tetramethylbutane"]

assert len(OCTANES) == len(NAMES) == 18


def alkane_pairs(smi):
    """Edge degree pairs (d_u, d_v) of a hydrogen-suppressed acyclic alkane
    written as a carbon-only SMILES string (alkane-only parser)."""
    adj = {}; prev = None; stack = []; k = -1
    for ch in smi:
        if ch == '(':
            stack.append(prev)
        elif ch == ')':
            prev = stack.pop()
        elif ch == 'C':
            k += 1; adj[k] = set()
            if prev is not None:
                adj[k].add(prev); adj[prev].add(k)
            prev = k
    seen = set(); out = []
    for u in adj:
        for v in adj[u]:
            e = (min(u, v), max(u, v))
            if e in seen:
                continue
            seen.add(e); out.append((len(adj[u]), len(adj[v])))
    return out


def lo_pairs(P, a, b, g):
    """LO(G; a, b, g) from the list P of edge degree pairs."""
    return sum((i * j) ** a * (i + j) ** b * math.exp(g * abs(i - j) / (i + j)) for i, j in P)
