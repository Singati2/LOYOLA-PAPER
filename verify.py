#!/usr/bin/env python3
"""Single entry point for the verification suites of this repository.

  python3 verify.py          fast path (about 6 minutes):
                               verify_loyola_v35.py      core verifier (tables, figures, re-runs)
                               prose_numbers_check.py    every registered prose numeral
                               external/test_regressions.py
                               external/test_baselines.py
                               constancy_test_check.py
                               audit/check_exploratory_outputs.py, check_source_identities.py, check_mathematics.py
                               audit/check_style.py      sentence length, dashes and stock phrases in the prose
                               structural/extremal_trees_check.py  path/star extremality of the pure-gamma points, orders 4-12
                               structural/minimality_check.py      first q-histogram collision orders 13 / 16, all orders 2-16
                               structural/weak_discrimination_check.py  Theorem thm:weakdisc, chemical trees 4-18, graphs <= 7
                               DATA/build_data.py --check  every file in DATA/ identical to its source
                               manifest.py               SHA-256 of every tracked file
  python3 verify.py --full   also (about one hour):
                               external/verify_external.py
                               structural/structural_checks.py, structural/hp_counts.py
                               verify_loyola_v35.py --selftest
                               audit/attack_checks.py      (13 counter-attacks on the newer checkers)
                               audit/check_labels.py       (labels, references, captions, cross-document numbering; needs tectonic)
                               formal/verify.sh (if a Lean toolchain is installed)
  python3 verify.py --everything   also audit/run_all_scripts.py: every script of the
                               repository re-run in an isolated copy and every file it
                               writes compared with the committed one (about two hours)

Each step is run as a subprocess; the exit status is 0 iff every step exits 0.
See REPRODUCE.md for what each suite covers.
"""
import os, re, shutil, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
FAST = [
    ("core verifier", [PY, "verify_loyola_v35.py"], HERE),
    ("prose numbers", [PY, "prose_numbers_check.py"], HERE),
    ("external regression tests", [PY, "test_regressions.py"], os.path.join(HERE, "external")),
    ("baseline tests", [PY, "test_baselines.py"], os.path.join(HERE, "external")),
    ("constancy test check", [PY, "constancy_test_check.py"], HERE),
    ("auxiliary outputs", [PY, os.path.join("audit", "check_exploratory_outputs.py")], HERE),
    ("archived-source identities", [PY, os.path.join("audit", "check_source_identities.py")], HERE),
    ("interval certificates", [PY, os.path.join("audit", "check_mathematics.py")], HERE),
    ("prose style", [PY, os.path.join("audit", "check_style.py")], HERE),
    ("extremal trees", [PY, "extremal_trees_check.py"], os.path.join(HERE, "structural")),
    ("collision minimality", [PY, "minimality_check.py"], os.path.join(HERE, "structural")),
    ("weak discrimination", [PY, "weak_discrimination_check.py"], os.path.join(HERE, "structural")),
    ("DATA copies", [PY, os.path.join("DATA", "build_data.py"), "--check"], HERE),
    ("manifest", [PY, "manifest.py"], HERE),
]


def check_csv_conventions():
    """octane_property_provenance_v35.csv must keep CRLF row terminators with LF
    only inside quoted fields (the self-test's provenance attacks split rows on
    CRLF; an LF rewrite silently disables them)."""
    import csv
    p = os.path.join(HERE, "octane_property_provenance_v35.csv")
    raw = open(p, "rb").read()
    rows_crlf = [l for l in raw.decode().split("\r\n") if l]
    try:
        parsed = [next(csv.reader([l])) for l in rows_crlf]
    except csv.Error:
        parsed = []
    n_fields = {len(r) for r in parsed}; n_crlf = raw.count(b"\r\n")
    with open(p, newline="") as f:
        n_rows = sum(1 for _ in csv.reader(f))          # header + records, parsed properly
    ok = n_crlf == len(rows_crlf) == n_rows >= 2 and n_fields == {12}
    print(f"[{'PASS' if ok else 'FAIL'}] provenance CSV convention: {n_crlf} CRLF rows, field counts {sorted(n_fields)}", flush=True)
    return ok
FULL = [
    ("external verifier", [PY, "verify_external.py"], os.path.join(HERE, "external")),
    ("structural checks", [PY, "structural_checks.py"], os.path.join(HERE, "structural")),
    ("32-digit recount", [PY, "hp_counts.py"], os.path.join(HERE, "structural")),
    ("verifier self-test", [PY, "verify_loyola_v35.py", "--selftest"], HERE),
    ("counter-attacks on the checkers", [PY, os.path.join("audit", "attack_checks.py")], HERE),
]
EVERYTHING = [
    ("every script replayed in isolation", [PY, os.path.join("audit", "run_all_scripts.py")], HERE),
]


def run(name, cmd, cwd):
    t0 = time.time()
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    lines = [l for l in (r.stdout + r.stderr).strip().splitlines() if l.strip()]
    summary = next((l for l in reversed(lines) if re.search(r"PASS|FAIL|failures|OK|RESULT|manifest|checked", l)), lines[-1] if lines else "")
    print(f"[{'PASS' if r.returncode == 0 else 'FAIL'}] {name} ({time.time() - t0:.0f} s): {summary.strip()[:140]}", flush=True)
    return r.returncode == 0


def main():
    if "--convention-only" in sys.argv:          # used by audit/attack_checks.py
        return 0 if check_csv_conventions() else 1
    steps = list(FAST)
    if "--full" in sys.argv or "--everything" in sys.argv:
        steps += FULL
    if "--full" in sys.argv or "--everything" in sys.argv:
        if shutil.which("tectonic"):
            steps.append(("labels and references", [PY, os.path.join("audit", "check_labels.py")], HERE))
        else:
            print("[SKIP] labels and references: no tectonic on PATH")
        if shutil.which("lake"):
            steps.append(("Lean proofs", ["bash", "verify.sh"], os.path.join(HERE, "formal")))
        else:
            print("[SKIP] Lean proofs: no Lean toolchain (lake) on PATH")
    if "--everything" in sys.argv:
        steps += EVERYTHING
    ok = all([run(*s) for s in steps] + [check_csv_conventions()])
    print("ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
