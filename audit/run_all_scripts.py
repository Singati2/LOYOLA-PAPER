#!/usr/bin/env python3
"""Run EVERY script of the repository and check that each one reproduces what
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
"""
import hashlib, os, shutil, subprocess, sys, tempfile, time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from verify_loyola_v35 import _pdf_canonical  # noqa: E402

# (script, slow?)  -- slow scripts take more than about two minutes
SCRIPTS = [
    ("external/build_nonane_data.py", False), ("external/check_nonane_structures.py", False),
    ("external/bp/build_bp_data.py", False), ("external/bp/build_calorimetric_set.py", False),
    ("ablation_gm_vs_lo.py", False), ("ablation_robustness.py", True), ("expanded_robustness_v35.py", True),
    ("tmb_exclusion_sensitivity.py", True), ("source_sensitivity.py", False), ("multi_order_degeneracy.py", False),
    ("redundancy_collisions.py", False), ("fgd_structure_sensitivity.py", True), ("generate_loyola_v35_figures.py", False),
    ("external/baselines.py", True), ("external/nonane_validation.py", True), ("external/transfer_exploratory.py", True),
    ("external/uncertainty_exploratory.py", True), ("external/box_sensitivity.py", True),
    ("external/wide_box_diagnostics.py", True), ("external/bp/bp_tests.py", True), ("external/bp/coverage_bias.py", False),
    ("external/bp/make_bp_table.py", False), ("external/make_box_table.py", False), ("external/make_v37_table.py", False),
    ("structural/structural_checks.py", True), ("structural/hp_counts.py", False), ("structural/fractional_points.py", False),
    ("structural/chi_floor.py", False), ("constancy_test_check.py", False), ("tuning_pool_seed_sweep.py", False),
    ("audit/check_exploratory_outputs.py", False), ("audit/check_source_identities.py", False), ("audit/check_mathematics.py", False),
    ("prose_numbers_check.py", False), ("external/test_regressions.py", False), ("external/test_baselines.py", False),
    ("verify_loyola_v35.py", True), ("manifest.py", False),
]


def tracked():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    return [p for p in out if p]   # tracked files only (formal/.lake is untracked); prose_claims_b reads formal/LoyolaFormal/Profiles.lean


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
        cwd = os.path.join(tmp, os.path.dirname(script)) or tmp
        t0 = time.time()
        r = subprocess.run([sys.executable, os.path.basename(script)], cwd=cwd, capture_output=True, text=True, timeout=7200)
        dt = time.time() - t0
        changed, new = [], []
        for dp, _, fns in os.walk(tmp):
            for fn in fns:
                full = os.path.join(dp, fn); rel = os.path.relpath(full, tmp)
                if "__pycache__" in rel or rel == "SHA256SUMS.txt":
                    continue
                if rel in ref:
                    if digest(full) != ref[rel]:
                        changed.append(rel)
                else:
                    new.append(rel)
        present = {os.path.relpath(os.path.join(dp, fn), tmp) for dp, _, fns in os.walk(tmp) for fn in fns}
        changed += sorted(f"{p} (DELETED)" for p in ref if p not in present and p != "SHA256SUMS.txt")
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
        return dict(script=script, exit=r.returncode, seconds=dt, changed=sorted(changed), new=sorted(new), tail=tail[0][:120])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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
    lines = [f"run_all_scripts at {head}: {len(todo)} scripts, each in an isolated copy of the {len(files)} tracked files "
             f"snapshotted before the run; comparison: bytes (PDFs by canonical form)"]
    print(lines[0], flush=True)
    bad = 0
    with ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(lambda s: run_one(s, files, ref), todo):
            ok = res["exit"] == 0 and not res["changed"]
            bad += not ok
            line = (f"[{'OK' if ok else 'PROBLEM'}] {res['script']}: exit {res['exit']}, {res['seconds']:.0f} s"
                    + (f"; CHANGED {res['changed']}" if res["changed"] else "; all written files identical")
                    + (f"; new files {res['new']}" if res["new"] else "") + f"; last line: {res['tail']}")
            lines.append(line); print(line, flush=True)
    lines.append(f"RESULT: {'every script exits 0 and reproduces its committed outputs' if bad == 0 else str(bad) + ' PROBLEM(S)'}")
    print(lines[-1])
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    open(os.path.join(repo, "audit", "run_all_scripts_out.txt"), "w").write("\n".join(lines) + "\n")
    shutil.rmtree(base, ignore_errors=True)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
