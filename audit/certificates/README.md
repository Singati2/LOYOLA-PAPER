# Enumeration certificates for the minimal collision orders

This code is independent of the repository's own verifiers. Every script enumerates all unlabeled trees
with `networkx.nonisomorphic_trees` and uses exact rational arithmetic. Runtime: about 60 s in total on one
CPU core, well under 1 GB of memory.

| Script | Checks | Output |
|---|---|---|
| `minimal.py 17` | For orders 2–17, the number of distinct degree-pair profiles, q-histograms and colliding classes, for all trees and for Δ ≤ 4. First collision: 13 for all trees, 16 for Δ ≤ 4 | `minimal_out.txt` |
| `by_delta.py 18` | First collision order for each bound Δ ≤ 3, …, 8 and for all trees, up to order 18; every colliding class at its first order | `by_delta_out.txt`, `first_collisions_upto18.json` |
| `ratio_indices.py` | First order at which SDD or ISDD (exact rationals) gives equal values to distinct profiles: 9 and 10, for all trees and for Δ ≤ 4 | `ratio_indices_out.txt` |
| `witnesses.py` | Builds the four witness trees of Theorem ratio-plane (iii) from their descriptions in `main.tex`. Checks that each is a tree with the stated order and maximum degree, that each pair has distinct profiles and equal q-histograms, and that the pendant-path construction keeps this for orders 13–40 and 16–43 | `witnesses_out.txt` |
| `make_notebook.py` | Writes `collision_orders_colab.ipynb`, which runs all four and asserts the results | — |

Results:
* no collision for Δ ≤ 3 up to order 18 (the proof for every order is in `../NOVELTY_AND_PROOF_MATRIX.md`);
* 16 for Δ ≤ 4 and for Δ ≤ 5;
* 13 for Δ ≥ 6 and for all trees.

Outputs were produced with Python 3.13.16 and networkx 3.6.1 (`requirements-lock.txt`). networkx
3.4.2 gives the same results.

```bash
cd audit/certificates
for s in "minimal.py 17" "by_delta.py 18" ratio_indices.py witnesses.py; do python3 $s | tail -1; done
```

The notebook clones `REVISION` from GitHub when it is not run inside the repository. It works on Colab
only after that revision has been pushed. Run locally, it uses the files of this folder.
