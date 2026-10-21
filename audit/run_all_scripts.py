#!/usr/bin/env python3
"""Run every script of the repository (except the independent cross-checks in NOT_REPLAYED, which are
listed in the output) and check that each one reproduces what
is committed.

Each script runs in its own isolated copy of the git-tracked tree (so scripts
cannot interfere and every file a script writes can be attributed to it), with
the working directory set to the script's directory.  Afterwards every tracked
file of that copy is compared with the committed file: text and CSV files
byte-for-byte, PDFs by the verifier's canonical form (object streams compared,
/Length objects ignored, as verify_loyola_v35.py does), and new untracked files
are listed.  Exit status 0 iff every script exits 0 and no committed file
differs.  Orchestrators (verify.py, verify_external.py, the self-test) are not
run here because they only re-run the scripts below.

  python3 audit/run_all_scripts.py            everything (about two hours; three scripts at a time)
  python3 audit/run_all_scripts.py --fast     only scripts that finish in under two minutes

Output: audit/run_all_scripts_out.txt (committed).

A script that exceeds LOYOLA_SCRIPT_TIMEOUT seconds (default 7200) is reported as a PROBLEM marked
TIMED OUT (its outputs are not compared) and the replay continues.  Every changed output is copied to
a loyola_changed_* directory, created only when the first changed file is found; the RESULT line names
that directory only if it exists and holds files, so a discrepancy can be diffed after the run (v40.31).

A script is OK only if it exits 0, rewrites every file listed for it in colab/expected_outputs.py, rewrites
no other tracked file, and every tracked file of its copy is identical to the commit (2026-10-21). The list
is fixed in advance and reviewed, so a script that exits 0 without producing its outputs is a PROBLEM.
"""
import hashlib, importlib.util, os, shutil, subprocess, sys, tempfile, threading, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = int(os.environ.get("LOYOLA_SCRIPT_TIMEOUT", "7200"))   # seconds per script; a timeout is reported, not fatal
KEEP = None                                                      # changed outputs are copied here for diffing (created lazily)
_KEEP_LOCK = threading.Lock()                                    # run_one runs in a ThreadPoolExecutor
sys.path.insert(0, ROOT)
from verify_loyola_v35 import _pdf_canonical  # noqa: E402
_spec = importlib.util.spec_from_file_location("loyola_expected_outputs", os.path.join(ROOT, "colab", "expected_outputs.py"))
_inv = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_inv)
EXPECTED, INCIDENTAL = _inv.EXPECTED, _inv.INCIDENTAL


def _keep_dir():
    """Return the directory for changed outputs, creating it on first use (thread-safe)."""
    global KEEP
    with _KEEP_LOCK:
        if KEEP is None:
            KEEP = tempfile.mkdtemp(prefix="loyola_changed_")
        return KEEP

# (script, slow?)  -- slow scripts take more than about two minutes
SCRIPTS = [
    ("external/build_nonane_data.py", False), ("external/check_nonane_structures.py", False),
    ("external/bp/build_bp_data.py", False), ("external/bp/build_calorimetric_set.py", False),
    ("ablation_gm_vs_lo.py", False), ("ablation_robustness.py", True), ("expanded_robustness_v35.py", True),
    ("tmb_exclusion_sensitivity.py", True), ("source_sensitivity.py", False), ("multi_order_degeneracy.py", False),
    ("redundancy_collisions.py", False), ("fgd_structure_sensitivity.py", True), ("generate_loyola_v35_figures.py", False),
    ("external/baselines.py", True), ("external/baselines.py --dataset nonane", True), ("external/nonane_validation.py", True), ("external/transfer_exploratory.py", True),
    ("external/uncertainty_exploratory.py", True), ("external/box_sensitivity.py", True),
    ("external/wide_box_diagnostics.py", True), ("external/bp/bp_tests.py", True), ("external/bp/coverage_bias.py", False), ("external/bp/selection_resampling.py", True), ("external/nonane_tb_conflict.py", True),
    ("external/bp/make_bp_table.py", False), ("external/make_box_table.py", False), ("external/make_v37_table.py", False),
    ("structural/structural_checks.py", True), ("structural/hp_counts.py", False), ("structural/fractional_points.py", False),
    ("structural/chi_floor.py", False), ("structural/extremal_trees_check.py", False), ("structural/minimality_check.py", False), ("structural/sumconn_pair_check.py", False), ("structural/count_dimension_check.py", False), ("structural/exact_ties.py", False), ("external/bp/wiener_baseline.py", False), ("audit/final/scripts/bp_duplicate_sensitivity.py", False), ("audit/final/scripts/press_size_probe.py", True), ("audit/final/scripts/claim_provenance.py", False), ("audit/final/scripts/counterattack_v4030.py", False), ("audit/v4030/math_independent.py", False), ("audit/v4030/table2_independent.py", False), ("audit/v4030/uncertain_source_sensitivity.py", False), ("audit/v4030/leakage_probe.py", False), ("audit/v4030/feature_leakage_probe.py", False), ("audit/v4030/gamma_strict.py", True), ("audit/v4030/sensitivity_followup.py", True), ("audit/v4030/refit_stability.py", True), ("tmb_dhvap_audit.py", False), ("DATA/build_data.py", False), ("constancy_test_check.py", False), ("tuning_pool_seed_sweep.py", False),
    ("audit/check_exploratory_outputs.py", False), ("audit/check_source_identities.py", False), ("audit/check_mathematics.py", False),
    ("prose_numbers_check.py", False), ("external/test_regressions.py", False), ("external/test_baselines.py", False),
    ("verify_loyola_v35.py", True), ("manifest.py", False),
]
# Independent cross-checks that neither replay harness runs (each takes its own environment or about an hour).
# They are listed in every report so that a complete replay is not read as covering them; their committed
# outputs are the separate evidence and must be rerun on their own before claiming that they reproduce.
NOT_REPLAYED = {
    "audit/permutation_pipeline_audit.py": "scikit-learn re-implementation of the 200-permutation check; about 30-60 min; "
                                           "evidence audit/permutation_pipeline_audit_out.txt",
    "audit/v4030/uncertain_source_crosscheck.py": "pandas/scikit-learn cross-check of uncertain_source_sensitivity.py; "
                                                  "evidence audit/v4030/uncertain_source_crosscheck_out.txt",
}
# Scripts that only check (exit status is their result) and write no tracked
# file; for every other script a run that rewrites nothing is a PROBLEM.
CHECK_ONLY = {"external/check_nonane_structures.py", "audit/check_exploratory_outputs.py", "audit/check_source_identities.py",
              "audit/check_mathematics.py", "prose_numbers_check.py", "external/test_regressions.py", "external/test_baselines.py",
              "manifest.py"}


def tracked():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    sys.path.insert(0, os.path.join(ROOT, "external"))
    from nist_pages import local_paths          # the NIST pages are downloaded, not tracked (external/nist_pages.py)
    return [p for p in out if p] + local_paths()   # formal/.lake is untracked; prose_claims_b reads formal/LoyolaFormal/Profiles.lean


def digest(path):
    with open(path, "rb") as f:
        data = f.read()
    if path.endswith(".pdf"):
        canon = _pdf_canonical(data)          # list of canonical PDF objects (/Length objects ignored)
        return hashlib.sha256(repr(canon).encode()).hexdigest()
    return hashlib.sha256(data).hexdigest()


def make_copy(files, dest):
    for p in files:
        d = os.path.join(dest, p); os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, p), d)


def run_one(script, files, ref):
    tmp = tempfile.mkdtemp(prefix="loyola_run_")
    try:
        make_copy(files, tmp)
        cwd = os.path.join(tmp, os.path.dirname(script.split()[0])) or tmp
        t0 = time.time()
        parts = script.split()
        try:
            r = subprocess.run([sys.executable, os.path.basename(parts[0])] + parts[1:], cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            # v40.31: a timeout is a PROBLEM of this script, not a crash of the whole replay
            return dict(script=script, exit=f"timeout after {TIMEOUT} s", seconds=time.time() - t0, changed=[], new=[],
                        tail="(not completed; outputs not compared)", touched=0, touched_files=[], timed_out=True)
        dt = time.time() - t0
        changed, new, touched, touched_files = [], [], 0, []
        for dp, _, fns in os.walk(tmp):
            for fn in fns:
                full = os.path.join(dp, fn); rel = os.path.relpath(full, tmp)
                if "__pycache__" in rel or rel == "SHA256SUMS.txt":
                    continue
                if rel in ref:
                    if os.path.getmtime(full) > t0:
                        touched += 1                               # v40.22: the script must rewrite something
                        touched_files.append(rel)
                    if digest(full) != ref[rel]:
                        changed.append(rel)
                        keep = os.path.join(_keep_dir(), script.replace(" ", "_").replace("/", "__"), rel)   # v40.31: retained for diffing
                        os.makedirs(os.path.dirname(keep), exist_ok=True); shutil.copy2(full, keep)
                else:
                    new.append(rel)
        present = {os.path.relpath(os.path.join(dp, fn), tmp) for dp, _, fns in os.walk(tmp) for fn in fns}
        changed += sorted(f"{p} (DELETED)" for p in ref if p not in present and p != "SHA256SUMS.txt")
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
        return dict(script=script, exit=r.returncode, seconds=dt, changed=sorted(changed), new=sorted(new), tail=tail[0][:120],
                    touched=touched, touched_files=sorted(touched_files))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def judge(res):
    """(ok, detail): exit 0, no committed file changed, every expected output rewritten, no unlisted tracked rewrite."""
    script = res["script"]
    if res.get("timed_out"):
        return False, "TIMED OUT, outputs not compared"
    expected = EXPECTED.get(script, [] if script in CHECK_ONLY else None)
    if expected is None:
        return False, "not in colab/expected_outputs.py"
    touched = set(res["touched_files"])
    missing = [f for f in expected if f not in touched]
    unlisted = sorted(touched - set(expected) - set(INCIDENTAL.get(script, ())))
    detail = "; ".join(x for x in (f"CHANGED {res['changed']}" if res["changed"] else "",
                                   f"expected output missing or not rewritten: {missing}" if missing else "",
                                   f"unlisted tracked file rewritten: {unlisted}" if unlisted else "") if x)
    ok = res["exit"] == 0 and not detail
    if ok:
        detail = (f"all {len(expected)} expected outputs rewritten and identical" if expected
                  else "check-only script, writes no file")
    return ok, detail


def main():
    fast = "--fast" in sys.argv
    files = tracked()
    # one snapshot of the tracked tree, taken before anything runs, is the source
    # of every per-script copy and of the reference digests, so edits made to
    # the working tree while this script runs cannot contaminate the comparison
    global ROOT
    base = tempfile.mkdtemp(prefix="loyola_base_"); make_copy(files, base); ROOT = base
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          capture_output=True, text=True).stdout.strip()
    ref = {p: digest(os.path.join(ROOT, p)) for p in files}
    todo = [s for s, slow in SCRIPTS if not (fast and slow)]
    lines = [f"run_all_scripts at {head}: {len(todo)} scripts, each in an isolated copy of the {len(files)} tracked files and downloaded NIST pages "
             f"snapshotted before the run; comparison: bytes (PDFs by canonical form)"]
    print(lines[0], flush=True)
    bad = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(lambda s: run_one(s, files, ref), todo):
            ok, detail = judge(res)
            bad += not ok
            line = (f"[{'OK' if ok else 'PROBLEM'}] {res['script']}: exit {res['exit']}, {res['seconds']:.0f} s; {detail}"
                    + (f"; new files {res['new']}" if res["new"] else "") + f"; last line: {res['tail']}")
            lines.append(line); print(line, flush=True)
    lines += [f"NOT REPLAYED (independent cross-check, run separately): {k}: {v}" for k, v in NOT_REPLAYED.items()]
    kept = KEEP is not None and any(fns for _, _, fns in os.walk(KEEP))
    lines.append(f"RESULT: {'every script exits 0 and reproduces its committed outputs' if bad == 0 else str(bad) + ' PROBLEM(S); ' + ('changed outputs kept in ' + KEEP if kept else 'no changed outputs to keep')}")
    print(lines[-1])
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    open(os.path.join(repo, "audit", "run_all_scripts_out.txt"), "w").write("\n".join(lines) + "\n")
    shutil.rmtree(base, ignore_errors=True)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
