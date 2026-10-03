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

echo "--- #print axioms output ---"
n=$(grep -c "depends on axioms" "$LOG" || true)
echo "theorems checked: $n"
bad=$(grep "depends on axioms" "$LOG" | sed 's/.*depends on axioms: \[\(.*\)\]/\1/' \
      | tr ',' '\n' | sed 's/ //g' | grep -vE '^(propext|Classical.choice|Quot.sound)$' || true)
if [ -n "$bad" ] || grep -q "sorryAx" "$LOG"; then
  echo "FAIL: unexpected axioms: $bad"; status=1
else echo "OK: only propext / Classical.choice / Quot.sound"; fi
rm -f "$LOG"
exit $status
