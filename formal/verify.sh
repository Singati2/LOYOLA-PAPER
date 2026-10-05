#!/usr/bin/env bash
# Build the Lean formalization and check for sorry / extra axioms.
set -euo pipefail
cd "$(dirname "$0")"
export PATH="$HOME/.elan/bin:$PATH"

LOG=$(mktemp)
lake exe cache get >/dev/null 2>&1 || true
lake build 2>&1 | tee "$LOG" | tail -3

status=0
echo "--- sorry check (source) ---"
if grep -rn --include='*.lean' -w 'sorry' LoyolaFormal LoyolaFormal.lean; then
  echo "FAIL: sorry found"; status=1
else echo "OK: no sorry"; fi

echo "--- axiom declarations (source) ---"
if grep -rnE --include='*.lean' '^\s*(axiom|unsafe|@\[implemented_by)' LoyolaFormal LoyolaFormal.lean \
   || grep -rn --include='*.lean' 'native_decide' LoyolaFormal LoyolaFormal.lean; then
  echo "FAIL: axiom/native_decide found"; status=1
else echo "OK: no axiom declarations, no native_decide"; fi

echo "--- #print axioms output (fresh, fail-closed) ---"
# The expected theorem list is a COMMITTED file (expected_axiom_theorems.txt,
# 36 names), not regenerated from the sources being audited; the axiom-check
# file is generated from that list so reports are fresh even on a cached build,
# and a theorem missing from the sources makes the check file fail to compile.
EXPECTED_COUNT=36
if [ "$(sort -u expected_axiom_theorems.txt | grep -c .)" -ne "$EXPECTED_COUNT" ]; then
  echo "FAIL: expected_axiom_theorems.txt must list exactly $EXPECTED_COUNT distinct names"; exit 1; fi
for t in $(cat expected_axiom_theorems.txt); do
  short="${t##*.}"
  if ! grep -qE "^(theorem|lemma) $short( |$|\()" LoyolaFormal/*.lean; then echo "FAIL: $t is listed but not declared in the sources"; exit 1; fi
done
{ echo "import LoyolaFormal"; echo; while read -r t; do echo "#print axioms $t"; done < expected_axiom_theorems.txt; } > AxiomCheck.lean
AX=$(mktemp); lake env lean AxiomCheck.lean > "$AX" 2>&1 || { echo "FAIL: AxiomCheck.lean did not compile"; cat "$AX"; status=1; }
expected=$EXPECTED_COUNT
n=$(grep -c "depends on axioms" "$AX" || true)
echo "theorems expected: $expected, reports: $n"
reported=$(grep "depends on axioms" "$AX" | sed "s/^'\([^']*\)'.*/\1/" | sort)
if [ "$n" -ne "$expected" ] || [ "$expected" -eq 0 ]; then echo "FAIL: report count mismatch"; status=1; fi
if [ "$reported" != "$(cat expected_axiom_theorems.txt)" ]; then echo "FAIL: reported theorem names differ from expected list"; diff <(echo "$reported") expected_axiom_theorems.txt; status=1; fi
if [ "$(echo "$reported" | sort | uniq -d | wc -l | tr -d ' ')" != "0" ]; then echo "FAIL: duplicate reports"; status=1; fi
bad=$(grep "depends on axioms" "$AX" | sed 's/.*depends on axioms: \[\(.*\)\]/\1/' \
      | tr ',' '\n' | sed 's/ //g' | grep -vE '^(propext|Classical.choice|Quot.sound)$' || true)
if [ -n "$bad" ] || grep -q "sorryAx" "$AX"; then
  echo "FAIL: unexpected axioms: $bad"; status=1
elif [ "$status" -eq 0 ]; then echo "OK: all $n expected theorems report only propext / Classical.choice / Quot.sound"; fi
rm -f "$AX"
rm -f "$LOG"
exit $status
