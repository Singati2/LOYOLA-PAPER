# Rada 2019 and the q-histogram: formal mapping, 2026-10-23

**Question.** Does Rada's index-induced equivalence give exactly the manuscript's q-histogram equivalence, or only a related relation? The answer decides the wording of the Corollary 3.5 credit (patch L3 of `3a5f061`).

**Source.** J. Rada, *Exponential vertex-degree-based topological indices and discrimination*, MATCH 82 (2019) 29–41. The full text was read in a private local copy, which is not in the repository. The parts used:
- Table 1 (p. 30);
- the definition of $\mathcal G_n$ (p. 31);
- eqs. (3)–(6) and Definition 2.3 (p. 33);
- Proposition 2.5 (p. 34);
- Theorem 3.4 and Corollary 3.5 (pp. 36–37).

## 1. Rada's objects

- **Graph class.** $\mathcal G_n$ is the set of graphs with $n$ non-isolated vertices.
- **Index space.** $K = \{(i,j): 1 \le i \le j \le n-1\}$; the degree pairs are unordered, with $i \le j$.
- **Indices.** A vertex-degree-based index is a vector $\varphi = (\varphi_{ij}) \in \mathbb R^{h}$, with $\varphi(G) = \sum_{(i,j)\in K} m_{ij}(G)\,\varphi_{ij}$.
- **Equivalence.** Eq. (3) sets $(i,j) \sim (i',j')$ iff $\varphi_{ij} = \varphi_{i'j'}$. This partitions $K$ into classes $[i_k,j_k]$, $k = 1,\dots,p$.
- **Counts.** $\widehat m_{i_kj_k}(G) = \sum_{(r,s)\in[i_k,j_k]} m_{rs}(G)$ (eq. 6). $G$ and $G'$ have the same $\widehat m_\varphi$-structure iff the vectors $\widehat m_\varphi(G)$ and $\widehat m_\varphi(G')$ are equal (Definition 2.3).
- **Theorem 3.4.** If every $\varphi_{ij}$ is algebraic, then $e^{\varphi}(G) = \sum m_{ij}(G)e^{\varphi_{ij}}$ has the discrimination property on $\mathcal G_n$: $e^\varphi(G) = e^\varphi(G') \iff \widehat m_\varphi(G) = \widehat m_\varphi(G')$.
- **Corollary 3.5.** This holds for every index of Table 1. Table 1 contains GA, with $\varphi_{ij} = 2\sqrt{ij}/(i+j)$.

## 2. Claim and proof

**Claim.** For every $n$, the partition of $K$ induced by $GA_{ij} = 2\sqrt{ij}/(i+j)$ equals the partition induced by $q_{ij} = (j-i)/(i+j)$. Consequently, for $G, G' \in \mathcal G_n$:

$$e^{GA}(G) = e^{GA}(G') \iff \widehat m_{GA}(G) = \widehat m_{GA}(G') \iff G \text{ and } G' \text{ have equal } q\text{-histograms}.$$

**Proof.**
1. Since $(i+j)^2 - (j-i)^2 = 4ij$, we have $GA_{ij}^2 = 1 - q_{ij}^2$, with $GA_{ij} > 0$ and $q_{ij} \in [0,1)$ for $i \le j$.
2. The map $q \mapsto \sqrt{1-q^2}$ is strictly decreasing on $[0,1)$, so $GA_{ij} = GA_{i'j'} \iff q_{ij} = q_{i'j'}$. The two partitions of $K$ therefore coincide.
3. So $\widehat m_{GA}(G)$ is the vector of edge counts per $q$-value. For each value that some pair in $K$ attains, it lists the number of edges of $G$ with that imbalance, which is zero when no edge has that value.
4. Two such vectors, both indexed by the same $K$ for fixed $n$, are equal iff the $q$-histograms are equal.
5. $GA_{ij}$ is algebraic, being the square root of a rational. Theorem 3.4 and Corollary 3.5 therefore apply, which gives the claim. ∎

**Same argument for the pure-γ points.** Take $\varphi_{ij} = \gamma q_{ij}$ with $\gamma$ algebraic and non-zero. Multiplying by $\gamma \ne 0$ is injective, so the induced partition is again the $q$-partition. This is the existing credit in Theorem 2(ii) and its attribution paragraph.

## 3. Conditions and degeneracies

| Aspect | Status |
|---|---|
| **Equal order** | Rada's statement is on $\mathcal G_n$, which means equal numbers of non-isolated vertices. The manuscript's graphs are connected with at least one edge, so they have no isolated vertices and this is equal order. The L3 sentence says "For graphs of equal order", which is correct. For graphs of different order Rada's statement says nothing. The manuscript's own proof of Theorem 2(ii) covers that case, illustrated by $K_4$ and $K_{1,3}$ |
| **Orientation** | Degree pairs are unordered in both Rada ($i \le j$) and the manuscript (multiset), and $q$ uses $|d_u - d_v|$. No orientation issue |
| **Symmetry and $(1,1)$** | $q_{11} = 0$ falls in the same class as all $(i,i)$, in both the GA and the $q$ partition. No discrepancy |
| **GA itself versus $e^{GA}$** | Rada's result is for the exponential index $e^{GA}$. GA itself does not separate the histograms: the manuscript finds that it merges two at order 17. The L3 sentence says "the exponential GA index", followed by "GA itself does not", which is correct |
| **SDD and ISDD** | Their weights are also algebraic and injective in $q$, so Theorem 3.4 applies to $e^{SDD}$ and $e^{ISDD}$ as well. They are not in Rada's Table 1, so Corollary 3.5 does not name them. The manuscript does not claim this; adding it is optional |

**Computer check.** `audit/independent_recompute_2026-10-23/rada_ga_partition_check.py` uses exact rationals and compares $GA^2 = 1 - q^2$ as fractions. For every $n = 2,\dots,60$ it confirms that the partitions of $K$ induced by GA, by $q$ and by $\gamma q$ ($\gamma = 3$ and $\gamma = -1$) coincide. It runs in about 1.4 s.

## 4. Verdict and wording

**VERIFIED.** The relation is exactly the q-histogram relation, not a related or conditional one, on graphs of equal order. The L3 sentence is correct as written:

> For graphs of equal order the exponential $GA$ index does the same, by~\cite[Corollary~3.5]{Rada2019ExpVDB}, since its weight $\sqrt{1-q^2}$ is algebraic and injective in $q$.

**Novelty consequence.** Separating exactly the q-histograms on $\mathcal G_n$ is known: from Rada 2019 for $e^{GA}$, and by his Theorem 3.4 for any algebraic weight that is injective in $q$. The manuscript adds the following:
- the extension of Theorem 2(ii) to graphs of different orders (elementary);
- the one-parameter family of such separators inside LO;
- the witnesses and minimal orders 13 and 16 (computer-assisted).

No claim of first discovery is made for the separation property. The contribution list already credits Rada for equal order. The search statement after Theorem 2 is limited to the orders and to the profile-distinct, histogram-equal pairs, and it is presented as the result of a search, not as proof of novelty.
