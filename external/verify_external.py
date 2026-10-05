#!/usr/bin/env python3
"""Verify the v37 external-validation package end to end:
1. nonane structures (strict parser, isomorphism, NIST InChI);
2. nonane dataset rebuilds byte-identically from the archived NIST pages;
3. baselines reproduce the octane package values (test_baselines.py);
4. fresh re-runs of nonane_validation.py, baselines (octane + nonane) and
   make_v37_table.py reproduce the committed CSVs byte-for-byte;
5. every row of tab:external and tab:box (looked up in ../main.tex, then
   ../supplement.tex) equals the generated row.
Exit 0 only if all pass."""
import os, subprocess, sys, shutil, tempfile, filecmp
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
fails = []
def run(args, cwd):
    r = subprocess.run([sys.executable] + args, cwd=cwd, capture_output=True, text=True)
    if r.returncode != 0: fails.append(f"{' '.join(args)}: exit {r.returncode}: {r.stderr.strip()[-200:]}")
    return r
OUTS = ["nonane_data.csv", "nonane_provenance.csv", "nonane_validation_seeds.csv",
        "nonane_validation_summary.csv", "baselines_octane.csv", "baselines_nonane.csv",
        "v37_classical_fixed.csv", "v37_table_rows.tex",
        "transfer_exploratory.csv", "transfer_exploratory_summary.csv",
        "uncertainty_exploratory.csv", "box_sensitivity.csv", "box_sensitivity_summary.csv",
        "box_table_rows.tex"]
with tempfile.TemporaryDirectory() as td:
    ext = os.path.join(td, "external"); shutil.copytree(HERE, ext)
    for f in os.listdir(ROOT):
        if f.endswith(".py") or f.endswith(".csv"): shutil.copy(os.path.join(ROOT, f), td)
    for f in OUTS:
        p = os.path.join(ext, f)
        if os.path.exists(p): os.remove(p)
    run(["build_nonane_data.py"], ext)
    run(["check_nonane_structures.py"], ext)
    run(["test_baselines.py"], ext)
    run(["nonane_validation.py"], ext)
    run(["baselines.py", "--dataset", "octane"], ext)
    run(["baselines.py", "--dataset", "nonane"], ext)
    run(["make_v37_table.py"], ext)
    run(["transfer_exploratory.py"], ext)
    run(["uncertainty_exploratory.py"], ext)
    run(["box_sensitivity.py"], ext)
    run(["make_box_table.py"], ext)
    for f in OUTS:
        a, b = os.path.join(ext, f), os.path.join(HERE, f)
        if not os.path.exists(a): fails.append(f"{f}: not regenerated")
        elif not filecmp.cmp(a, b, shallow=False): fails.append(f"{f}: fresh run differs from committed file")
# v40 boiling-point tests: rebuild data, re-run analysis, compare outputs and table
with tempfile.TemporaryDirectory() as td2:
    bp = os.path.join(td2, "external", "bp"); shutil.copytree(os.path.join(HERE, "bp"), bp)
    shutil.copy(os.path.join(HERE, "baselines.py"), os.path.join(td2, "external"))
    for f in os.listdir(ROOT):
        if f.endswith(".py"): shutil.copy(os.path.join(ROOT, f), td2)
    BPO = ["bp_data.csv", "bp_provenance.csv", "bp_results_seeds.csv", "bp_results_summary.csv", "bp_baselines.csv", "bp_table_rows.tex"]
    for f in BPO: os.remove(os.path.join(bp, f))
    for sc in ("build_bp_data.py", "bp_tests.py", "make_bp_table.py"): run([sc], bp)
    for f in BPO:
        a_, b_ = os.path.join(bp, f), os.path.join(HERE, "bp", f)
        if not os.path.exists(a_): fails.append(f"bp/{f}: not regenerated")
        elif not filecmp.cmp(a_, b_, shallow=False): fails.append(f"bp/{f}: fresh run differs from committed file")
rows = [l.strip() for l in open(os.path.join(HERE, "v37_table_rows.tex")) if l.strip()]
# tables are looked up by label in main.tex followed by supplement.tex, so a
# guarded table may live in either document
tex = open(os.path.join(ROOT, "main.tex")).read()
if os.path.exists(os.path.join(ROOT, "supplement.tex")):
    tex += "\n" + open(os.path.join(ROOT, "supplement.tex")).read()
i = tex.index(r"\label{tab:external}"); blk = tex[tex.index(r"\midrule", i):tex.index(r"\bottomrule", i)]
body = [l.strip() for l in blk.splitlines()[1:] if l.strip()]
if body != rows: fails.append("tab:external in main.tex/supplement.tex differs from generated rows")
brows = [l.strip() for l in open(os.path.join(HERE, "box_table_rows.tex")) if l.strip()]
i = tex.index(r"\label{tab:box}"); blk = tex[tex.index(r"\midrule", i):tex.index(r"\bottomrule", i)]
bbody = [l.strip() for l in blk.splitlines()[1:] if l.strip()]
if bbody != brows: fails.append("tab:box in main.tex/supplement.tex differs from generated rows")
prows = [l.strip() for l in open(os.path.join(HERE, "bp", "bp_table_rows.tex")) if l.strip()]
i = tex.index(r"\label{tab:bp}"); blk = tex[tex.index(r"\midrule", i):tex.index(r"\bottomrule", i)]
if [l.strip() for l in blk.splitlines()[1:] if l.strip()] != prows: fails.append("tab:bp differs from generated rows")
print("\n".join(fails) if fails else "external verification: PASS (structures, rebuild, baseline validation, fresh re-runs, table)")
sys.exit(1 if fails else 0)
