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
                               structural/sumconn_pair_check.py   Example ex:sumconn from the order-18 chemical trees
                               structural/count_dimension_check.py  affine dimension of the counts (7 / 8) and the octane T_B error floor
                               DATA/build_data.py --check  every file in DATA/ identical to its source
                               manifest.py               SHA-256 of every tracked file
  python3 verify.py --full   also (about one hour):
                               external/verify_external.py
                               structural/structural_checks.py, structural/hp_counts.py
                               verify_loyola_v35.py --selftest
                               audit/attack_checks.py      (13 counter-attacks on the newer checkers)
                               audit/check_labels.py       (labels, references, captions, cross-document numbering; needs pdflatex or tectonic)
                               formal/verify.sh (if a Lean toolchain is installed)
  python3 verify.py --everything   also audit/run_all_scripts.py: every script of the
                               repository re-run in an isolated copy and every file it
                               writes compared with the committed one (about two hours)

NIST WebBook pages. The checks marked [NIST] below read the NIST WebBook pages, which are not
redistributed with the repository and are never downloaded by this script. Retrieve them once with
`python3 external/nist_pages.py --download` (explicit, one request per second); the script then
checks each against its archived digest. Without them:
  python3 verify.py --offline   runs every other check and reports the [NIST] checks as NOT RUN
                                (exit 0 if everything run passes; this is what CI runs)
  python3 verify.py             without --offline, missing pages make the run INCOMPLETE (exit 3)
[NIST] checks: archived-source identities, auxiliary outputs (it rebuilds the calorimetric census),
external regression tests (one test), external verifier,
counter-attacks on the checkers, every script replayed in isolation.

Each step is run as a subprocess; the exit status is 0 iff every step exits 0 and no stage was
skipped. With --full or --everything, a missing TeX engine (pdflatex or tectonic) or lake skips that stage, the run ends
"INCOMPLETE" and exits with status 3; --allow-skip accepts the skips (exit 0, still INCOMPLETE).
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
    ("sum-connectivity pair", [PY, "sumconn_pair_check.py"], os.path.join(HERE, "structural")),
    ("count dimension and error floor", [PY, "count_dimension_check.py"], os.path.join(HERE, "structural")),
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
    ("exact tie certificate", [PY, "exact_ties.py"], os.path.join(HERE, "structural")),
    ("verifier self-test", [PY, "verify_loyola_v35.py", "--selftest"], HERE),
    ("counter-attacks on the checkers", [PY, os.path.join("audit", "attack_checks.py")], HERE),
]
# steps that read the NIST WebBook pages (see the docstring); test_regressions skips its one page test itself
NEEDS_NIST = {"archived-source identities", "auxiliary outputs", "external verifier", "counter-attacks on the checkers",
              "every script replayed in isolation"}
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
    steps, skipped = list(FAST), []
    if "--full" in sys.argv or "--everything" in sys.argv:
        steps += FULL
    if "--full" in sys.argv or "--everything" in sys.argv:
        if shutil.which("pdflatex") or shutil.which("tectonic"):
            steps.append(("labels and references", [PY, os.path.join("audit", "check_labels.py")], HERE))
        else:
            print("[SKIP] labels and references: neither pdflatex nor tectonic on PATH"); skipped.append("labels and references")
        if shutil.which("lake"):
            steps.append(("Lean proofs", ["bash", "verify.sh"], os.path.join(HERE, "formal")))
        else:
            print("[SKIP] Lean proofs: no Lean toolchain (lake) on PATH"); skipped.append("Lean proofs")
    if "--everything" in sys.argv:
        steps += EVERYTHING
    sys.path.insert(0, os.path.join(HERE, "external"))
    import nist_pages
    same, changed, missing = nist_pages.status()
    pages_ok = True
    if changed or (missing and same):
        print(f"[FAIL] NIST WebBook pages: {len(same)} identical, {len(changed)} changed, {len(missing)} missing "
              "(python3 external/nist_pages.py shows which)"); pages_ok = False
    elif missing:
        tag = "NOT RUN" if "--offline" in sys.argv else "SKIP"
        print(f"[{tag}] NIST WebBook pages not downloaded (not redistributed; python3 external/nist_pages.py --download). "
              f"Not run: {', '.join(n for n, _, _ in steps if n in NEEDS_NIST)}; external regression tests skip one test")
        not_run = [s for s in steps if s[0] in NEEDS_NIST]
        steps = [s for s in steps if s[0] not in NEEDS_NIST]
        if "--offline" not in sys.argv:
            skipped += [s[0] for s in not_run]
    else:
        print(f"[PASS] NIST WebBook pages: all {len(same)} present and identical to the archived versions")
    ok = all([run(*s) for s in steps] + [check_csv_conventions()]) and pages_ok
    mode = "everything" if "--everything" in sys.argv else "full" if "--full" in sys.argv else "fast path"
    if not ok:
        print("FAILURES")
    elif skipped:   # v40.30: a run with skipped stages is not a full verification and must not read as one
        print(f"INCOMPLETE ({mode}): executed steps passed, SKIPPED: {', '.join(skipped)}")
        # exit status 3 unless the caller accepts the skips explicitly (--allow-skip), so that a script
        # or CI job testing the exit status cannot mistake an incomplete run for a complete one
        return 0 if "--allow-skip" in sys.argv else 3
    elif missing and "--offline" in sys.argv:
        print(f"ALL PASS ({mode}, offline: the checks that read the NIST WebBook pages were NOT RUN)")
    else:
        print(f"ALL PASS ({mode})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
