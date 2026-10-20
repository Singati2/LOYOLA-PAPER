#!/usr/bin/env python3
"""Checks for the corrections of audit/LOYOLA_REVIEW_2026-10-20.md that are not already covered by
audit/test_corrections_2026_10_19.py (R1, R2, R3, R6 and the pinning part of R7 are tested there).

  python3 audit/test_review_2026_10_20.py        (seconds; no network, no NIST data; needs git)

R4  the 58 aggregate-derived boiling points: direct averages plus means of averages equal the A-AGG tier of
    the quality ledger, and the prose registry entry for 58 fails when the number in the supplement is wrong.
R5  gamma_strict labels its interval as a molecule bootstrap (bp_tests.boot_ci resamples molecules, not seeds).
R7  coverage: both replay harnesses name the same independent cross-checks they do not run, the scripts and
    their evidence files exist, and the pipeline report prints them. Entry point: every Colab link of the
    reviewer guide and the README opens a notebook whose PIN is the commit the guide tells reviewers to check
    out, and no link points to main; the prose and Lean counts are the current ones.
Each check prints PASS or FAIL; the exit status is the number of failures.
"""
import importlib.util, os, re, subprocess, sys, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILS = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def read(*p):
    return open(os.path.join(ROOT, *p)).read()


def r4():
    sys.path.insert(0, ROOT)
    A = load(os.path.join(ROOT, "prose_claims_a.py"), "prose_claims_a_under_test")
    direct, mean, tier = A.bp_avg_stats()[0], A.bp_mean_of_avgs(), A.bp_aggregate_tier()
    check("R4 direct averages + means of averages = ledger A-AGG tier = 58", direct + mean == tier == 58, (direct, mean, tier))
    sup = read("supplement.tex")
    check("R4 supplement states 58", "so $58$ values rest on NIST averages" in sup)
    # mutation: the registry pattern must read the number in the text, so a wrong number cannot pass
    m = re.search(r"so \$(?P<v>\d+)\$ values rest on NIST averages", sup.replace("so $58$ values", "so $59$ values"))
    check("R4 registry pattern reads a changed number (59 != 58)", m is not None and int(m["v"]) != tier)


def r5():
    src = read("audit", "v4030", "gamma_strict.py"); out = read("audit", "v4030", "gamma_strict_out.txt")
    check("R5 script no longer says seed-bootstrap", "seed-bootstrap" not in src)
    check("R5 output no longer says seed-bootstrap", "seed-bootstrap" not in out)
    check("R5 output names the molecule bootstrap twice", out.count("95% molecule-bootstrap interval (conditional on fitted outer predictions)") == 2)
    boot = read("external", "bp", "bp_tests.py")
    body = boot[boot.index("def boot_ci"):boot.index("def run_test")]
    check("R5 boot_ci resamples molecule indices", "rng.integers(0, n, n)" in body and "G[:, idx]" in body)
    for v in ("-0.1294", "12/50", "[-0.1858, -0.0292]", "-0.0397", "10/50", "[-0.0907, -0.0053]"):
        check(f"R5 value {v} unchanged", v in out)


def r7_coverage(tmp):
    sys.path.insert(0, os.path.join(ROOT, "colab"))
    P = load(os.path.join(ROOT, "colab", "pipeline.py"), "pipeline_under_test")
    R = open(os.path.join(ROOT, "audit", "run_all_scripts.py")).read()
    check("R7 pipeline names the two cross-checks it does not run",
          set(P.NOT_REPLAYED) == {"audit/permutation_pipeline_audit.py", "audit/v4030/uncertain_source_crosscheck.py"})
    for k, v in P.NOT_REPLAYED.items():
        ev = re.search(r"evidence (\S+)", v)[1]
        check(f"R7 {k} and its evidence exist", os.path.exists(os.path.join(ROOT, k)) and os.path.exists(os.path.join(ROOT, ev)))
        check(f"R7 {k} is outside the pipeline plan", k not in P.ORDER)
        check(f"R7 run_all_scripts names {k}", f'"{k}"' in R and "NOT REPLAYED" in R)
    check("R7 pipeline report prints the not-replayed section", "## Not replayed by this pipeline" in open(P.__file__).read())


def r7_entry():
    guide, readme, repro = read("REVIEWER_START_HERE.md"), read("README.md"), read("REPRODUCE.md")
    code = re.search(r"git checkout ([0-9a-f]{40})\s+# the pinned commit", guide)
    check("R7 guide names one full pinned commit", code is not None)
    if not code:
        return
    code = code[1]
    check("R7 README names the same commit", code in readme)
    links = re.findall(r"colab\.research\.google\.com/github/Singati2/LOYOLA-PAPER/blob/([^/]+)/(notebooks/[\w.]+\.ipynb)", guide + readme)
    check("R7 guide and README have notebook links", len(links) >= 12, len(links))
    check("R7 no link points to main", all(rev != "main" for rev, _ in links))
    for rev, path in sorted(set(links)):
        r = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT, capture_output=True, text=True)
        pin = re.search(r'LOYOLA_PIN\\", \\"([0-9a-f]{40})', r.stdout)
        check(f"R7 {path} at {rev[:7]} runs the pinned commit", r.returncode == 0 and pin is not None and pin[1] == code,
              (r.returncode, pin and pin[1]))
    for name, text in (("guide", guide), ("REPRODUCE", repro)):
        check(f"R7 {name} has no stale 733/20 prose counts", "733 checked" not in text and "20 cited values" not in text)
    check("R7 guide states the 52-declaration Lean check", "all 52 declarations" in guide)


def main():
    with tempfile.TemporaryDirectory() as tmp:
        for f in (r4, r5, lambda: r7_coverage(tmp), r7_entry):
            try:
                f()
            except Exception as e:                                  # an unexpected error is a failure, not a pass
                check(f"{getattr(f, '__name__', 'check')} ran to the end", False, repr(e))
    print(f"\n{'ALL CHECKS PASSED' if not FAILS else str(len(FAILS)) + ' FAILED: ' + ', '.join(FAILS)}")
    return len(FAILS)


if __name__ == "__main__":
    sys.exit(main())
