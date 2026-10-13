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
if grep -rnwE --include='*.lean' 'sorry|admit' LoyolaFormal LoyolaFormal.lean; then
  echo "FAIL: sorry or admit found"; status=1
else echo "OK: no sorry"; fi

echo "--- axiom declarations (source) ---"
if grep -rnE --include='*.lean' '^\s*(axiom|unsafe|@\[implemented_by)' LoyolaFormal LoyolaFormal.lean \
   || grep -rn --include='*.lean' 'native_decide' LoyolaFormal LoyolaFormal.lean; then
  echo "FAIL: axiom/native_decide found"; status=1
else echo "OK: no axiom declarations, no native_decide"; fi

echo "--- #print axioms output (fresh, fail-closed) ---"
# The expected theorem list is a COMMITTED file (expected_axiom_theorems.txt,
# 38 names), not regenerated from the sources being audited; the axiom-check
# file is generated from that list so reports are fresh even on a cached build,
# and a theorem missing from the sources makes the check file fail to compile.
EXPECTED_COUNT=38
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
reported=$(grep "depends on axioms" "$AX" | sed "s/^'\([^']*\)'.*/\1/" | LC_ALL=C sort)
expected_names=$(LC_ALL=C sort expected_axiom_theorems.txt)
if [ "$n" -ne "$expected" ] || [ "$expected" -eq 0 ]; then echo "FAIL: report count mismatch"; status=1; fi
if [ "$reported" != "$expected_names" ]; then echo "FAIL: reported theorem names differ from expected list"; diff <(echo "$reported") <(echo "$expected_names"); status=1; fi
if [ "$(echo "$reported" | sort | uniq -d | wc -l | tr -d ' ')" != "0" ]; then echo "FAIL: duplicate reports"; status=1; fi
bad=$(grep "depends on axioms" "$AX" | sed 's/.*depends on axioms: \[\(.*\)\]/\1/' \
      | tr ',' '\n' | sed 's/ //g' | grep -vE '^(propext|Classical.choice|Quot.sound)$' || true)
if [ -n "$bad" ] || grep -q "sorryAx" "$AX"; then
  echo "FAIL: unexpected axioms: $bad"; status=1
elif [ "$status" -eq 0 ]; then echo "OK: all $n expected theorems report only propext / Classical.choice / Quot.sound"; fi
rm -f "$AX"

echo "--- #print axioms for every declared theorem and lemma (v40.30 audit; stricter than the list above) ---"
# Covers the helper lemmas as well as the 38 listed theorems. A declaration may report no axioms at all;
# any sorryAx or axiom outside propext / Classical.choice / Quot.sound fails the check.
ALL=$(mktemp); ALLSRC=".axiom_all_check.lean"
{ echo "import LoyolaFormal"; echo;
  for f in LoyolaFormal/*.lean; do
    ns=$(grep -m1 -E '^namespace ' "$f" | awk '{print $2}')
    grep -oE '^(theorem|lemma) [A-Za-z0-9_.'"'"']+' "$f" | awk '{print $2}' | while read -r d; do
      if [ -n "$ns" ]; then echo "#print axioms $ns.$d"; else echo "#print axioms $d"; fi; done
  done; } > "$ALLSRC"
ndecl=$(grep -c '^#print axioms' "$ALLSRC")
lake env lean "$ALLSRC" > "$ALL" 2>&1 || { echo "FAIL: $ALLSRC did not compile"; cat "$ALL"; status=1; }
nrep=$(grep -cE "depends on axioms|does not depend on any axioms" "$ALL" || true)
badall=$(grep "depends on axioms" "$ALL" | sed 's/.*depends on axioms: \[\(.*\)\]/\1/' \
      | tr ',' '\n' | sed 's/ //g' | grep -vE '^(propext|Classical.choice|Quot.sound)$' || true)
if [ "$nrep" -ne "$ndecl" ]; then echo "FAIL: $ndecl declarations, $nrep axiom reports"; status=1
elif [ -n "$badall" ] || grep -q "sorryAx" "$ALL"; then echo "FAIL: unexpected axioms among all declarations: $badall"; status=1
else echo "OK: all $ndecl declarations report only standard axioms (or none)"; fi
rm -f "$ALL" "$ALLSRC"
rm -f "$LOG"
exit $status
