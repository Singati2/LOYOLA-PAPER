#!/usr/bin/env python3
"""Counter-attacks on the checkers that are NOT covered by the core verifier's
own 114-attack self-test.  Each attack copies the tracked tree, applies one
mutation (a corrupted output file, data file, manuscript numeral or archived
page) and requires the named checker to exit non-zero.  A checker that still
passes is a false negative and fails this script.

  python3 audit/attack_checks.py          (about three minutes)

Output: audit/attack_checks_out.txt (committed).
"""
import os, re, shutil, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable


def tracked():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    return [p for p in out if p]   # tracked files only (formal/.lake is untracked); prose_claims_b reads formal/LoyolaFormal/Profiles.lean


def edit(tmp, rel, old, new, count=1, binary=False):
    p = os.path.join(tmp, rel)
    mode = "rb" if binary else "r"
    data = open(p, mode, **({} if binary else {"newline": ""})).read()
    assert data.count(old) >= 1, f"attack anchor not found in {rel}: {old!r}"
    data = data.replace(old, new, count)
    open(p, "wb" if binary else "w", **({} if binary else {"newline": ""})).write(data)


def drop_first_line(tmp, rel, prefix):
    p = os.path.join(tmp, rel); lines = open(p, newline="").read().split("\n")
    k = next(i for i, l in enumerate(lines) if l.startswith(prefix)); del lines[k]
    open(p, "w", newline="").write("\n".join(lines))


def swap_skeletons(tmp, rel):
    """Swap the carbon skeletons of the first two C10 records (different isomers)."""
    import csv
    p = os.path.join(tmp, rel); rows = list(csv.DictReader(open(p, newline=""))); hdr = list(rows[0].keys())
    i, j = [k for k, r in enumerate(rows) if r["n"] == "10"][:2]
    rows[i]["skel"], rows[j]["skel"] = rows[j]["skel"], rows[i]["skel"]
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=hdr); w.writeheader(); w.writerows(rows)


def first_csv_number(tmp, rel, column_hint=None):
    """Return (old, new) for the first decimal number of the file with >= 3 decimals."""
    t = open(os.path.join(tmp, rel), newline="").read()
    m = re.search(r"-?\d+\.\d{3,}", t)
    old = m.group(0); d = list(old); i = len(d) - 1
    d[i] = "0" if d[i] != "0" else "1"
    return old, "".join(d)


ATTACKS = [
    # (name, checker command (cwd-relative to its directory), mutation(tmp))
    ("prose: a prose numeral changed", ["prose_numbers_check.py"],
     lambda t: edit(t, "main.tex", "by up to $0.043$ in $|r|$", "by up to $0.044$ in $|r|$")),
    ("prose: a registered sentence reworded", ["prose_numbers_check.py"],
     lambda t: edit(t, "main.tex", "this union contains nine of the ten", "this union contains all ten")),
    ("auxiliary outputs: fractional-point output corrupted", ["audit/check_exploratory_outputs.py"],
     lambda t: edit(t, "structural/fractional_points_out.txt", *first_csv_number(t, "structural/fractional_points_out.txt"))),
    ("auxiliary outputs: calorimetric CSV corrupted", ["audit/check_exploratory_outputs.py"],
     lambda t: edit(t, "external/bp/calorimetric_dHvap298_alkanes.csv", "True", "False")),
    ("source identities: two decane skeletons swapped", ["audit/check_source_identities.py"],
     lambda t: swap_skeletons(t, "external/bp/nist_alkanes_skeletons_audit.csv")),
    ("32-digit recount: an S1 count altered", ["structural/hp_counts.py"],
     lambda t: edit(t, "structural/structural_checks_out.txt", "  13 all 1301 570 566 570 566 566 566 0", "  13 all 1301 570 566 570 566 567 566 0")),
    ("manifest: a tracked file modified", ["manifest.py"],
     lambda t: edit(t, "octane_data.py", "102.06", "102.07")),
    ("coverage bias: a decane provenance row removed", ["external/bp/coverage_bias.py"],
     lambda t: drop_first_line(t, "external/bp/bp_provenance.csv", "10,")),
    ("data build: archived page removed", ["external/bp/build_bp_data.py"],
     lambda t: os.remove(os.path.join(t, "external/bp/nist_raw/C500006531.html"))),
    ("constancy check: a constant descriptor injected", ["constancy_test_check.py"],
     lambda t: edit(t, "constancy_test_check.py", "X = np.array([[lo_pairs(P, a, b, g) for P in OP] for a, b, g in T])",
                    "X = np.array([[lo_pairs(P, a, b, g) for P in OP] for a, b, g in T]); X[0, :] = 1.0")),
    ("regression tests: silent skip of a missing page restored", ["external/test_regressions.py"],
     lambda t: edit(t, "external/bp/build_bp_data.py",
                    'raise FileNotFoundError(f"missing required archived NIST page: {p}")', "continue")),
    ("regression tests: structural certificate check disabled", ["external/test_regressions.py"],
     lambda t: edit(t, "structural/structural_checks.py", "if not witnesses:", "if False:")),
    ("CSV convention: provenance CSV rewritten with LF rows", ["verify.py", "--convention-only"],
     lambda t: edit(t, "octane_property_provenance_v35.csv", b"\r\n", b"\n", -1, binary=True)),
]


def run_attack(name, cmd, mutate, files):
    tmp = tempfile.mkdtemp(prefix="loyola_attack_")
    try:
        for p in files:
            d = os.path.join(tmp, p); os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(os.path.join(ROOT, p), d)
        mutate(tmp)
        script = cmd[0]; cwd = os.path.join(tmp, os.path.dirname(script)) or tmp
        t0 = time.time()
        r = subprocess.run([PY, os.path.basename(script)] + cmd[1:], cwd=cwd, capture_output=True, text=True, timeout=1800)
        rejected = r.returncode != 0
        tail = (r.stdout + r.stderr).strip().splitlines()[-1:] or [""]
        return rejected, f"{time.time() - t0:.0f} s; exit {r.returncode}; {tail[0][:110]}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    files = tracked(); lines = []; bad = 0
    for name, cmd, mutate in ATTACKS:
        try:
            rejected, info = run_attack(name, cmd, mutate, files)
        except Exception as e:  # noqa: BLE001
            rejected, info = False, f"harness exception: {e!r}"
        bad += not rejected
        line = f"[{'REJECTED' if rejected else 'NOT REJECTED (false negative)'}] {name}: {info}"
        lines.append(line); print(line, flush=True)
    lines.append(f"RESULT: {len(ATTACKS)} attacks, {len(ATTACKS) - bad} rejected, {bad} false negatives")
    print(lines[-1])
    open(os.path.join(ROOT, "audit", "attack_checks_out.txt"), "w").write("\n".join(lines) + "\n")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
