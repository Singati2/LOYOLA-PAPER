"""Structure/identity check for the 35 nonane isomers (C9H20).

1. Enumerates all trees on 9 vertices with max degree <= 4 (networkx).
2. Parses every SMILES in nonane_data.csv with the package's strict parser
   (octane_data.alkane_adj) and checks each is isomorphic to exactly one
   enumerated tree, and that all 35 trees are covered exactly once.
3. Parses the carbon connectivity layer of the IUPAC InChI that NIST WebBook
   lists for each CAS (nonane_identity.csv, fetched 2026-10-03) and checks it is
   isomorphic to the SMILES graph of the same row (name/CAS/SMILES agreement).
Exit status 0 only if every check passes.
"""
import csv, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, '..')
from octane_data import alkane_adj
import networkx as nx

def graph_from_adj(adj):
    g = nx.Graph(); g.add_nodes_from(adj)
    g.add_edges_from((u, v) for u in adj for v in adj[u])
    return g

def graph_from_inchi(inchi):
    m = re.search(r'/c([^/]*)', inchi)
    assert inchi.startswith('InChI=1S/C9H20/') and m, inchi
    g = nx.Graph(); prev = None; stack = []
    for tok in re.findall(r'\d+|[-(),]', m.group(1)):
        if tok.isdigit():
            a = int(tok); g.add_node(a)
            if prev is not None: g.add_edge(prev, a)
            prev = a
        elif tok == '(': stack.append(prev)
        elif tok == ',': prev = stack[-1]
        elif tok == ')': prev = stack.pop()
    return g

trees = [t for t in nx.nonisomorphic_trees(9) if max(d for _, d in t.degree()) <= 4]
assert len(trees) == 35, len(trees)
rows = list(csv.DictReader(open(os.path.join(HERE, 'nonane_data.csv'))))
ident = {r['cas']: r for r in csv.DictReader(open(os.path.join(HERE, 'nonane_identity.csv')))}
assert len(rows) == 35 and len({r['cas'] for r in rows}) == 35 and len({r['name'] for r in rows}) == 35
hits = [0] * 35; ok = True
for r in rows:
    g = graph_from_adj(alkane_adj(r['smiles']))
    assert g.number_of_nodes() == 9 and nx.is_tree(g)
    m = [i for i, t in enumerate(trees) if nx.is_isomorphic(g, t)]
    if len(m) != 1: ok = False; print('SMILES match count != 1:', r['name'], m)
    for i in m: hits[i] += 1
    idr = ident[r['cas']]
    if idr['smiles'] != r['smiles'] or idr['name'] != r['name']: ok = False; print('identity row mismatch', r['name'])
    if not nx.is_isomorphic(g, graph_from_inchi(idr['nist_inchi'])):
        ok = False; print('NIST InChI not isomorphic to SMILES:', r['name'], r['cas'])
if hits != [1] * 35: ok = False; print('coverage:', hits)
print('35 trees enumerated; 35 SMILES parsed strictly;',
      'each matches exactly one tree, all covered once; NIST InChI == SMILES for all CAS' if ok else 'FAILED')
sys.exit(0 if ok else 1)
