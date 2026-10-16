#!/usr/bin/env bash
# Run the verification stages that were NOT RUN on the audit machine (v40.30), on a machine with
# enough disk (about 10 GB free) and network access, for example the lab workstation:
#   1. Lean 4 proofs: formal/verify.sh, including the all-declarations axiom check
#   2. python3 verify.py --everything with Lean on PATH (about 3 hours)
#   3. the six notebooks in a fresh environment built from the lock files
# Every stage runs even if an earlier one fails. Logs and a PASS / FAIL / NOT RUN summary are written to
# verification_logs/lab_<commit>/. This script commits, pushes and tags nothing.
#
#   git clone https://github.com/Singati2/LOYOLA-PAPER.git && cd LOYOLA-PAPER
#   git checkout audit/v4030-adversarial
#   bash audit/run_remaining_checks.sh            # or: bash audit/run_remaining_checks.sh --skip-everything
set -uo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)
SHA=$(git rev-parse --short HEAD)
OUT="verification_logs/lab_$SHA"; mkdir -p "$OUT"
SUM="$OUT/SUMMARY.txt"
SKIP_EVERYTHING=0; [ "${1:-}" = "--skip-everything" ] && SKIP_EVERYTHING=1
record() { printf '%-36s %s\n' "$1" "$2" | tee -a "$SUM"; }

{
  echo "commit $(git rev-parse HEAD)"
  echo "date   $(date -u)"
  echo "host   $(uname -a)"
  echo "python $(python3 --version 2>&1)"
  echo "disk   $(df -h . | tail -1)"
  echo "tracked-file changes: $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ')"
} | tee "$SUM"
if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
  record "precondition" "FAIL (modified tracked files; results would not belong to $SHA)"; exit 1
fi

# ---------------------------------------------------------------- environment
if ! command -v lake >/dev/null 2>&1; then
  if [ ! -x "$HOME/.elan/bin/lake" ]; then
    curl -sSf https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh | sh -s -- -y --default-toolchain none \
      >"$OUT/elan_install.log" 2>&1 || true
  fi
  export PATH="$HOME/.elan/bin:$PATH"
fi
VENV="$HOME/.loyola-venv-lab"   # outside the repository: verify.py copies the working tree
if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV" && "$VENV/bin/python" -m pip install -q --upgrade pip \
    && "$VENV/bin/python" -m pip install -q -r requirements-lock.txt -r requirements-extras-lock.txt >"$OUT/pip.log" 2>&1
fi
"$VENV/bin/python" -m pip freeze >"$OUT/pip_freeze.txt" 2>/dev/null

# ---------------------------------------------------------------- 1. Lean
if command -v lake >/dev/null 2>&1; then
  (cd formal && bash verify.sh) >"$OUT/lean_verify.log" 2>&1; rc=$?
  ok38=$(grep -c "OK: all 38 expected theorems" "$OUT/lean_verify.log" || true)
  okall=$(grep -c "OK: all 52 declarations" "$OUT/lean_verify.log" || true)
  if [ $rc -eq 0 ] && [ "$ok38" -ge 1 ] && [ "$okall" -ge 1 ]; then record "1 Lean (formal/verify.sh)" "PASS"
  else record "1 Lean (formal/verify.sh)" "FAIL (exit $rc; see lean_verify.log)"; fi
else
  record "1 Lean (formal/verify.sh)" "NOT RUN (no lake after elan install; see elan_install.log)"
fi

# ---------------------------------------------------------------- 2. full suite with Lean
if [ $SKIP_EVERYTHING -eq 1 ]; then
  record "2 verify.py --everything" "NOT RUN (--skip-everything)"
else
  "$VENV/bin/python" verify.py --everything >"$OUT/verify_everything.log" 2>&1; rc=$?
  if [ $rc -eq 0 ] && grep -q "ALL PASS (everything)" "$OUT/verify_everything.log"; then record "2 verify.py --everything" "PASS"
  elif [ $rc -eq 3 ]; then record "2 verify.py --everything" "INCOMPLETE (a stage was skipped; exit 3)"
  else record "2 verify.py --everything" "FAIL (exit $rc; see verify_everything.log)"; fi
fi

# ---------------------------------------------------------------- 3. notebooks
TAG_SHA=$(git rev-parse --verify --quiet "v40.30^{commit}" || true)
if [ -z "$TAG_SHA" ] || [ "$TAG_SHA" != "$(git rev-parse HEAD)" ]; then
  export LOYOLA_ALLOW_MISMATCH=1
  echo "notebooks run with LOYOLA_ALLOW_MISMATCH=1 (tag v40.30 absent or elsewhere): results tied to $SHA, not to the tag" | tee -a "$SUM"
fi
"$VENV/bin/python" -m ipykernel install --sys-prefix --name python3 >/dev/null 2>&1
mkdir -p "$OUT/notebooks"; nbfail=0
for nb in notebooks/0*.ipynb; do
  "$VENV/bin/python" - "$nb" "$OUT/notebooks/$(basename "$nb")" >>"$OUT/notebooks.log" 2>&1 <<'PY'
import sys, os, nbformat
from nbclient import NotebookClient
src, dst = sys.argv[1], sys.argv[2]
nb = nbformat.read(src, as_version=4)
try:
    NotebookClient(nb, timeout=7200, kernel_name="python3", resources={"metadata": {"path": os.path.dirname(os.path.abspath(src))}}).execute()
    status = 0
except Exception as e:
    print(f"{src}: ERROR {type(e).__name__}"); status = 1
nbformat.write(nb, dst)
last = [o.get("text", "") for c in nb.cells if c.cell_type == "code" for o in c.get("outputs", []) if o.get("output_type") == "stream"]
print(f"{src}: {'OK' if status == 0 else 'FAILED'} | {(last[-1].strip().splitlines()[-1] if last else '')}")
sys.exit(status)
PY
  [ $? -eq 0 ] || nbfail=$((nbfail + 1))
done
if [ $nbfail -eq 0 ]; then record "3 notebooks (6, fresh env)" "PASS ($(grep -c ': OK' "$OUT/notebooks.log") of 6)"
else record "3 notebooks (6, fresh env)" "FAIL ($nbfail failed; see notebooks.log)"; fi

echo "summary: $SUM"
echo "Nothing was committed or pushed. Review the logs, then commit $OUT if the results should be kept."
