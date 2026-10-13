# Running the Lean 4 verification on another machine

The Lean stage of `verify.py --full` was **not run** on the audit machine. A Mathlib build needs about 7.6 GB of free disk, and about 4.6 GB was available. The owner chose not to free space by deleting toolchains or caches. This file gives the exact steps for a machine with enough space, for example a Linux workstation.

## Requirements

- About 10 GB of free disk: the Mathlib cache plus the build.
- Network access, for elan, the Mathlib cache and the git clone.
- git and bash. On macOS, bash 3.2 is enough.
- Python 3.13 with `requirements-lock.txt`, only for the full `verify.py` run in step 4. The Lean steps do not need Python.

## Steps

```bash
# 1. Exact revision (the audit branch head; replace by the tag once it exists)
git clone https://github.com/Singati2/LOYOLA-PAPER.git && cd LOYOLA-PAPER
git fetch origin audit/v4030-adversarial          # once the branch is pushed
git checkout <commit>                              # the audited commit, see below
git status --porcelain                             # must print nothing

# 2. Lean toolchain pinned by formal/lean-toolchain (leanprover/lean4:v4.34.1)
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none
source "$HOME/.elan/env"
cd formal && elan show                              # must resolve v4.34.1 from lean-toolchain

# 3. Build and check (Mathlib revision pinned in lake-manifest.json)
bash verify.sh 2>&1 | tee ../verification_logs/lean_$(git rev-parse --short HEAD).log
echo "exit=$?"
cd ..

# 4. Optional, the complete suite with Lean included (about 3 hours)
python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements-lock.txt
python3 verify.py --everything 2>&1 | tee verification_logs/everything_$(git rev-parse --short HEAD).log
```

**The audited commit.** The code repairs are frozen at `01ad6c6`, and the audit evidence is at `53bb763`. The stricter Lean check described below is added by the commit that adds this file, so run step 3 at that commit or later. `formal/LoyolaFormal/` is unchanged since `3af7f67`, so the proofs being checked are those that passed there.

## Expected output of `formal/verify.sh`

Each line below must appear, and the script must exit 0:

```
OK: no sorry
OK: no axiom declarations, no native_decide
theorems expected: 38, reports: 38
OK: all 38 expected theorems report only propext / Classical.choice / Quot.sound
OK: all 52 declarations report only standard axioms (or none)
```

**What the script checks:**
- `lake build` fails the script on any compile error (`set -euo pipefail`).
- The sources are scanned for `sorry` and `admit`, and for `axiom`, `unsafe`, `@[implemented_by]` and `native_decide`.
- The 38 theorems of `expected_axiom_theorems.txt` must exist in the sources and appear exactly once in a fresh `#print axioms` report.
- Every report must contain only propext, Classical.choice and Quot.sound, and no `sorryAx`.
- **New in the v40.30 audit:** the same axiom check runs on all 52 declared theorems and lemmas, including the 14 helper lemmas that are not on the list.

**The new check was not executed on the audit machine,** which had no build. The script passes `bash -n`, and its generated file was inspected: 52 `#print axioms Loyola.<name>` lines in the namespace used by the sources. If that one step fails to compile on a correct build, report it as a defect in the check, not as a proof failure. Do not remove it to make the run pass.

## What the Lean files prove, and what they do not

This is the scope stated in Supplementary Section S7 and `LEAN_VERIFICATION.md`, checked against the sources in the audit.

**Formalised:**
- the termwise (Δ, δ) bounds, the Cauchy–Schwarz interpolation, and the summation step of the bracket and ratio bounds, with the per-edge bounds as hypotheses;
- log-sum-exp convexity;
- the spanning statement of Lemma 3.1 for every Δ ≥ 3, via det W = (1/6) ln 2 (8 ln 3 − 13 ln 2), which the audit recomputed as −0.025648 to 30 digits;
- 1 − q² = 4xy/(x+y)²;
- the order-13 profile pair, with equal q-histograms and equal pure-γ values, realised by explicit trees.

**Not formalised:**
- the equality characterisations;
- the gradient, Hessian and strict-convexity statements;
- the ratio-plane theorem (i) and (ii);
- the γ-crossing bound and the identifiability proposition;
- the closed forms and the extremal trees;
- the ceiling and generic-discrimination propositions;
- every statistical and chemical result.

**Encoding.** Graphs are encoded by their degree-pair data, so the link "these are the vertex degrees of a graph" is not formalised, except for the two explicit order-13 trees.

## Recording the result

1. Commit the log under `verification_logs/` on the audited commit's branch.
2. Update `audit/V4030_SUBMISSION_READINESS.md`, Lean row, from NOT RUN to PASS or FAIL, with the commit.
3. A failure of any Lean check blocks the release tag.
