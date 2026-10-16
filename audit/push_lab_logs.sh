#!/usr/bin/env bash
# Commit and push the lab verification logs (verification_logs/lab_*) written by
# audit/run_remaining_checks.sh. Only that folder is committed; authorship is set to the repository owner.
#   cd LOYOLA-PAPER && git pull && bash audit/push_lab_logs.sh
set -uo pipefail
cd "$(dirname "$0")/.."
git config user.name "Ganesh Shiwakoti"
git config user.email "ganshiwakoti@gmail.com"
ls -d verification_logs/lab_* >/dev/null 2>&1 || { echo "No verification_logs/lab_* folder found. Run: bash audit/run_remaining_checks.sh"; exit 1; }
echo "=== summary ==="; cat verification_logs/lab_*/SUMMARY.txt 2>/dev/null
echo "=== Lean log, last lines ==="; tail -8 verification_logs/lab_*/lean_verify.log 2>/dev/null
git add verification_logs/lab_*
# every tracked file needs a manifest entry, or manifest.py (and CI) fails on the new logs
python3 manifest.py --write && git add SHA256SUMS.txt
if git diff --cached --quiet; then echo "Nothing new to commit (already committed?)."; else
  git commit -q -m "v40.30: lab verification logs (Lean, full suite, notebooks)" && echo "Committed."; fi
if git push origin HEAD:audit/v4030-adversarial; then echo "PUSHED. Tell Claude: pushed."
else
  echo "Push failed: this machine is not signed in to GitHub."
  echo "Type:  gh auth login    (choose GitHub.com, HTTPS, login with a web browser), then run this script again."
  echo "If gh is not installed, copy the folder verification_logs/lab_* to the Mac by USB or Drive instead."
fi
