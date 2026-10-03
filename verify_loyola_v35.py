#!/usr/bin/env python3
r"""UNIFIED verifier for the LOYOLA manuscript package (v36; filename kept).

v36 changes: data imported from octane_data.py (single source; four corrected
dH_vap values); every numeric table cell is compared as the EXACT display
string of the full-precision recomputed value (no tolerances); tab:ablation,
tab:fgdss and tab:multiorder are recomputed from first principles in this run
([H], [G2], [G3]) and tab:octane-data is checked against octane_data.OCTANES;
tab:lo_tuning_bestfixed reuses the tab:lo_tuning pools (single default_rng(42)
stream); provenance classes are re-derived with a parenthetical-aware parser,
paper values must equal the dataset, and PROV_TOL[dHvap] = 0.04 kcal/mol.

v35 additions: section [N] re-runs the four bundled analysis scripts
(matched-budget nested GM-vs-LO ablation, multi-order degeneracy n=7..12,
redundancy/PCA + BID collision table, Furtula-Gutman-Dehmer structure
sensitivity) in an isolated temp dir and compares all seven produced CSVs to
the bundled canonical copies; the drift guard additionally validates the four
new manuscript tables (tab:ablation, tab:multiorder, tab:fgdss,
tab:collisions) against those canonical CSVs / the octane data.

Exit codes: 0 = full pass; 1 = at least one check failed; 2 = partial / cannot
verify (missing required artifact, missing networkx, or unwritable output).

Sections: [A] Table 2 (60 cells) [B] bolded-cell bootstrap HWs [C] deletion
influence [D] descriptive post-selection paired bootstrap [E] E2 tuning + per-cell
metrics + fold export + constant control [F] best-fixed table [G] 106 trees /
75 decanes [M] mathematics [T] tex drift guard [T2] canonical CSV schema check.

v35 hardening over v29 (all v29 false negatives confirmed by execution first):
- [T] expected table values are DERIVED FROM THE EXECUTED COMPUTATION (CMP),
  not from a second hard-coded table; every numeric cell must be a COMPLETE
  token ($[+-]d.ddd$ signed, $d.ddd$ unsigned, or $\\phantom{+}0.000$ where the
  computed value rounds to zero) -- unexpected precision, nan/inf, scientific
  notation and trailing junk are rejected; all row labels, anchor-block labels,
  property labels, row counts, row order and uniqueness are validated for ALL
  THREE tables (Table 2: 12x5; tuning: 4 blocks x 5 rows x 7 columns;
  best-fixed: 5 rows x 2 labels + 4 values).
- [T2] each canonical CSV is validated against an expected file REBUILT from the
  executed computation with the generator's exact formats: exact header, exact
  row keys and order, exact cell strings (values, '*' best markers, best_in),
  derived-field recomputation (degeneracy_pct = 100(1-k/N), SA = SS/Abr), and
  whole-file byte comparison. Duplicate/missing/extra/reordered/renamed rows or
  columns and malformed cells are rejected.
- --selftest runs the full adversarial attack matrix on ISOLATED temporary
  copies (canonical files are never modified), asserts the EXPECTED diagnostic
  for each corruption (an unrelated crash counts as a FAILED negative test),
  and includes operational subprocess tests (fresh nested --output-dir,
  unwritable output, missing networkx, missing artifact, outside cwd).
- --output-dir is created recursively; an unwritable output target produces a
  controlled diagnostic and exit 2, not a traceback.- v35 (round-11 repair): TeX conditionals and \\catcode changes are rejected
  GLOBALLY on the decommented source (the per-block scan missed an outer
  \\iffalse...\\fi spanning a whole table, and \\catcode could re-bind the
  comment character); Table 2 row labels are matched by EXACT first-cell
  equality, so no prefix or suffix survives. The guard validates raw source
  under conventional catcodes with no conditionals; it does not execute TeX.
- (round-10 repair): TeX comments are stripped before table parsing
  (escaped backslash-percent preserved), so a %-commented row/label/anchor line is invisible
  to both LaTeX and the verifier and is caught by the row/label/count checks;
  TeX conditionals (\if.../\else/\fi) inside a guarded table region are
  rejected outright. Scope: FULL PASS covers the executed computations, the
  three guarded tables, and the canonical artifacts -- NOT every prose numeral
  and NOT the verifier's own integrity (compare SHA256SUMS.txt externally).
"""
import argparse, csv, io, math, os, re, shutil, subprocess, sys, tempfile
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from octane_data import OCTANES, NAMES, PROPS, alkane_pairs, lo_pairs  # single data source (v36)
ROWLABELS = ["M1","M2","HM","mM2","R","chi","H/2","ISI","GA","AG","LO(0,0,1)","LO(0,0,2)"]
RED = {"M1":(0,1,0),"M2":(1,0,0),"HM":(0,2,0),"mM2":(-1,0,0),"R":(-0.5,0,0),
 "chi":(0,-0.5,0),"H/2":(0,-1,0),"ISI":(1,-1,0),"GA":(0.5,-1,0),"AG":(-0.5,1,0),
 "LO(0,0,1)":(0,0,1),"LO(0,0,2)":(0,0,2)}
# manuscript-claim tables (audited against computation in sections A-F; the tex
# drift guard [T] does NOT use these -- it uses the computed CMP values):
MS_T2 = {"M1":(-0.718,-0.762,-0.935,-0.973,-0.970),"M2":(-0.497,-0.542,-0.811,-0.940,-0.988),
"HM":(-0.654,-0.710,-0.903,-0.975,-0.982),"mM2":(0.855,0.891,0.925,0.863,0.794),
"R":(0.819,0.850,0.958,0.933,0.898),"chi":(0.800,0.832,0.961,0.949,0.924),
"H/2":(0.821,0.849,0.961,0.933,0.900),"ISI":(-0.005,-0.000,-0.383,-0.601,-0.738),
"GA":(0.822,0.858,0.965,0.941,0.906),"AG":(-0.816,-0.859,-0.957,-0.939,-0.900),
"LO(0,0,1)":(-0.828,-0.832,-0.984,-0.931,-0.929),"LO(0,0,2)":(-0.829,-0.846,-0.981,-0.939,-0.925)}
BOLD = [("mM2","T_B"),("mM2","dHf"),("LO(0,0,1)","dHvap"),("HM","S"),("M2","omega")]
MS_E2 = {("M2","T_B"):(0.497,0.598,0.353,0.331,0.458),
("M2","dHf"):(0.542,0.635,0.358,0.395,0.540),
("M2","dHvap"):(0.811,0.876,0.185,0.768,0.838),
("M2","S"):(0.940,0.960,0.067,0.919,0.943),
("M2","omega"):(0.988,0.995,0.018,0.985,0.985),
("HM","T_B"):(0.654,0.740,0.257,0.545,0.647),
("HM","dHf"):(0.710,0.786,0.255,0.645,0.741),
("HM","dHvap"):(0.903,0.944,0.082,0.871,0.921),
("HM","S"):(0.975,0.976,0.027,0.967,0.960),
("HM","omega"):(0.982,0.989,0.025,0.979,0.982),
("mM2","T_B"):(0.855,0.864,0.096,0.781,0.759),
("mM2","dHf"):(0.891,0.897,0.087,0.865,0.837),
("mM2","dHvap"):(0.925,0.966,0.068,0.900,0.953),
("mM2","S"):(0.863,0.918,0.188,0.812,0.881),
("mM2","omega"):(0.794,0.881,0.246,0.730,0.853),
("LO(0,0,1)","T_B"):(0.828,0.835,0.161,0.771,0.764),
("LO(0,0,1)","dHf"):(0.832,0.842,0.152,0.800,0.807),
("LO(0,0,1)","dHvap"):(0.984,0.985,0.016,0.978,0.978),
("LO(0,0,1)","S"):(0.931,0.948,0.045,0.892,0.920),
("LO(0,0,1)","omega"):(0.929,0.945,0.074,0.907,0.926)}
MS_F = {"T_B":("mM2",0.855,0.781,0.835,0.764),
"dHf":("mM2",0.891,0.865,0.850,0.815),
"dHvap":("LO(0,0,1)",0.984,0.978,0.985,0.978),
"S":("HM",0.975,0.967,0.948,0.920),
"omega":("M2",0.988,0.985,0.945,0.926)}

CSV_PRED = "lo_sensitivity_prediction_correlations.csv"
CSV_DEG  = "lo_sensitivity_degeneracy_order10_trees.csv"
CSV_SS   = "lo_sensitivity_structure_sensitivity_decanes.csv"
CSV_ABL  = "ablation_summary.csv"
CSV_ABLF = "ablation_perfold.csv"
CSV_MO   = "multi_order_degeneracy.csv"
CSV_FGD  = "fgd_structure_sensitivity_decanes.csv"
CSV_COLL = "bid_collision_table.csv"
CSV_CORR = "descriptor_correlations.csv"
CSV_PCA  = "pca_spectrum.csv"
CSV_ROB  = "ablation_robustness.csv"
CSV_CTRL = "fgd_published_control.csv"
CSV_PROV = "octane_property_provenance_v35.csv"
CSV_EXPR = "expanded_robustness_v35.csv"
CSV_EXPS = "expanded_robustness_summary_v35.csv"
CSV_OMEG = "omega_source_sensitivity_v35.csv"
CSV_SSEN = "entropy_source_sensitivity_v36.csv"
PROV_HALF = {"T_B":0.05,"dHf":0.005,"dHvap":0.005,"S":0.005,"omega":0.0005}
PROV_TOL  = {"T_B":0.15,"dHf":0.15,"dHvap":0.04,"S":0.3,"omega":0.003}  # v36: dHvap tightened so a >=0.05 kcal/mol gap cannot pass
PROV_EXPECT = {"VERIFIED EXACT":3,"VERIFIED AFTER UNIT CONVERSION":34,
 "AGREEMENT WITHIN TOLERANCE":32,"SOURCE VARIATION / EXPLAINED":13,
 "CANNOT VERIFY":7,"CONFLICT":1}
EXPR_SIGNS = {  # (budget, property): (LO better, LO worse) over seeds 0..99 -- manuscript claims
 ("200","T_B"):(53,47),("200","dHf"):(14,86),("200","dHvap"):(100,0),("200","S"):(35,65),("200","omega"):(26,74),
 ("500","T_B"):(64,36),("500","dHf"):(24,76),("500","dHvap"):(100,0),("500","S"):(29,71),("500","omega"):(28,72)}
EXPR_PAIRED = {("200","dHvap"):(100,0),("500","dHvap"):(100,0)}
OMEGA_ALT = {"2,2,4-trimethylpentane":0.303,"2,2,3,3-tetramethylbutane":0.251}
S_ALT = {"octane":111.70,"2,2-dimethylhexane":103.40,"2,2,4-trimethylpentane":104.10,"2,3,3-trimethylpentane":102.10}
FGD_PUBLISHED = {  # Barman & Das, MATCH 95 (2026) 63-94, Table 10, decane column
 "M1":(0.0566,0.1336),"mM2":(0.0516,0.1177),"R":(0.0263,0.0588),"chi":(0.0264,0.0591),
 "H/2":(0.0515,0.1143),"GA":(0.0241,0.0535),"AG":(0.0255,0.0579)}
ANALYSIS_SCRIPTS = {
    "ablation_gm_vs_lo.py": [CSV_ABLF, CSV_ABL],
    "multi_order_degeneracy.py": [CSV_MO],
    "redundancy_collisions.py": [CSV_CORR, CSV_PCA, CSV_COLL],
    "fgd_structure_sensitivity.py": [CSV_FGD, CSV_CTRL],
    "expanded_robustness_v35.py": [CSV_EXPR, CSV_EXPS],
    "source_sensitivity.py": [CSV_OMEG, CSV_SSEN],
    "ablation_robustness.py": [CSV_ROB],
}
COLL_ROWS = [("3-methylheptane",2),("4-methylheptane",3),
             ("3,4-dimethylhexane",9),("3-ethyl-2-methylpentane",10)]
NUM_ANY = re.compile(r"^\$([+-]?\d+\.\d+)\$$")
NUM_INT = re.compile(r"^\$(\d+)\$$")
NUM_FRAC= re.compile(r"^\$(\d+)/18\$$")
PROP_TEX = {"T_B":"$T_B$","dHf":r"$\Delta H_f$","dHvap":r"$\Delta H_{\mathrm{vap}}$",
            "S":"$S$","omega":r"$\omega$"}
IDX_TEX = {"mM2":r"${}^{m}\!M_2$","LO(0,0,2)":"$LO(0,0,2)$","HM":"$HM$","M2":"$M_2$",
           "M1":"$M_1$","LO(0,0,1)":"$LO(0,0,1)$","R":"$R$","chi":r"$\chi$","H/2":"$H/2$",
           "ISI":"$ISI$","GA":"$GA$","AG":"$AG$"}
T2_CELL0 = ["$M_1 = LO(0,1,0)$","$M_2 = LO(1,0,0)$","$HM = LO(0,2,0)$",
    r"${}^{m}\!M_2 = LO(-1,0,0)$","$R = LO(-1/2,0,0)$",r"$\chi = LO(0,-1/2,0)$",
    "$H/2 = LO(0,-1,0)$","$ISI = LO(1,-1,0)$",r"$GA = 2\,LO(1/2,-1,0)$",
    r"$AG = \tfrac12 LO(-1/2,1,0)$","$LO(0,0,1)$","$LO(0,0,2)$"]
ANCHORS = ["M2","HM","mM2","LO(0,0,1)"]
ANCHOR_PATS = [r"near\} \$M_2 = LO\(1,0,0\)\$",r"near\} \$HM = LO\(0,2,0\)\$",
               r"near\} \$\{\}\^\{m\}\\!M_2 = LO\(-1,0,0\)\$",r"near\} \$LO\(0,0,1\)\$"]
NUM_S  = re.compile(r"^\$([+-]\d\.\d{3})\$$")
NUM_SB = re.compile(r"^\$\\mathbf\{([+-]\d\.\d{3})\}\$$")
NUM_U  = re.compile(r"^\$(\d\.\d{3})\$$")
NUM_PH = re.compile(r"^\$\\phantom\{\+\}(0\.000)\$$")
NUM_4  = re.compile(r"^\$(\d\.\d{4})\$$")
NUM_C100=re.compile(r"^\$(\d+)/100\$$")
NUM_MED= re.compile(r"^\$([+-]\d\.\d{3})\\,\[([+-]\d\.\d{3}),\s*([+-]\d\.\d{3})\]\$$")
FGD_LABEL = {"M1":"$M_1$","M2":"$M_2$","HM":"$HM$","mM2":r"${}^{m}\!M_2$","R":"$R$","chi":r"$\chi$",
             "H/2":"$H/2$","ISI":"$ISI$","GA":"$GA$","AG":"$AG$","LO(0,0,1)":"$LO(0,0,1)$","LO(0,0,2)":"$LO(0,0,2)$"}

HEADERS = {
    'lo_octane': 'Index & $T_B$ & $\\Delta H_f$ & $\\Delta H_{\\mathrm{vap}}$ & $S$ & $\\omega$\\\\',
    'collisions': 'Isomer & $T_B$ & $\\Delta H_f$ & $\\Delta H_{\\mathrm{vap}}$ & $S$ & $\\omega$\\\\',
    'lo_tuning': 'Property & $|r|_0$ & $|r|_{50}$ & $\\Delta_{\\mathrm{in}}$ & $\\pm$boot & $\\mathrm{LOO}_0$ & $\\mathrm{LOO}_{50}$ & $\\Delta_{\\mathrm{out}}$\\\\',
    'lo_tuning_bestfixed': 'Property & best fixed & $|r|_{\\mathrm{fix}}$ & $\\mathrm{LOO}_{\\mathrm{fix}}$ & $|r|_{\\mathrm{dec}}$ & $\\mathrm{LOO}_{\\mathrm{dec}}$\\\\',
    'ablation': 'Property & $Q^2_{\\mathrm{GM}}$ & $Q^2_{LO}$ & $\\Delta Q^2$ & $\\mathrm{RMSE}_{\\mathrm{GM}}$ & $\\mathrm{RMSE}_{LO}$ & LO better\\\\',
    'multiorder': '$n$ & set & $N$ & floor & $M_1$ & $M_2$ & $R$ & $LO(0,0,1)$ & $LO(0,0,2)$\\\\',
    'fgdss': 'Index & $SS$ & $Abr$ & $SS/Abr$\\\\',
    'octane-data': 'Isomer & $T_B$ & $\\Delta H_f$ & $\\Delta H_{\\mathrm{vap}}$ & $S$ & $\\omega$\\\\',
}
UNDEF_RESAMPLES = 0

def r_signed(x,y):
    xc=x-x.mean();yc=y-y.mean();s=np.linalg.norm(xc)*np.linalg.norm(yc)
    if s==0:
        global UNDEF_RESAMPLES;UNDEF_RESAMPLES+=1
        return 0.0
    return float(xc@yc/s)
def absr(x,y):return abs(r_signed(x,y))
def loo_pred(x,y):
    N=len(x);pr=np.empty(N)
    for i in range(N):
        m=np.ones(N,bool);m[i]=False;xi,yi=x[m],y[m]
        if xi.var()==0:pr[i]=yi.mean();continue
        b=((xi-xi.mean())*(yi-yi.mean())).sum()/((xi-xi.mean())**2).sum()
        pr[i]=(yi.mean()-b*xi.mean())+b*x[i]
    return pr
def metr(pred,y):
    return (r_signed(pred,y),1-((pred-y)**2).sum()/((y-y.mean())**2).sum(),
            float(np.abs(pred-y).mean()),float(np.sqrt(((pred-y)**2).mean())))
def boot_hw(x,y,B=10000,seed=0):
    rng=np.random.default_rng(seed);v=[]
    for _ in range(B):
        idx=rng.integers(0,len(y),len(y));v.append(absr(x[idx],y[idx]))
    lo_,hi=np.percentile(v,[2.5,97.5]);return (hi-lo_)/2

def decomment_tex(s):
    """Strip TeX comments (unescaped % to end of line), preserving escaped backslash-percent."""
    out=[]
    for line in s.split("\n"):
        i=0;res=[]
        while i<len(line):
            c=line[i]
            if c=="\\" and i+1<len(line):res.append(line[i:i+2]);i+=2;continue
            if c=="%":break
            res.append(c);i+=1
        out.append("".join(res))
    return "\n".join(out)

def load_v35_expectations(here):
    """v36: tables are guarded against first-principles recomputations made in
    this run (CMP["ABL"], CMP["FGD"], CMP["MO"]); the only CSV-derived
    expectation is the 100-seed sweep (expanded_robustness_v35.csv), which
    section [N] regenerates from scratch and compares with the canonical copy."""
    E={"EXPR":{}}
    for r in csv.DictReader(open(os.path.join(here,CSV_EXPR),newline="")):
        E["EXPR"].setdefault((r["budget"],r["property"]),[]).append(float(r["dQ2"]))
    return E

def run_v35_analyses(here):
    """Re-run the four bundled analysis scripts in an isolated temp dir and
    compare every produced CSV against the bundled canonical copy
    (byte-first, numeric fallback at 1e-8 for float cells). Returns (ok,msgs)."""
    import tempfile, shutil as _sh
    msgs=[]
    with tempfile.TemporaryDirectory() as td:
        for sc in ANALYSIS_SCRIPTS: _sh.copy(os.path.join(here,sc),td)
        _sh.copy(os.path.join(here,"octane_data.py"),td)
        _sh.copy(os.path.abspath(__file__),os.path.join(td,"verify_loyola_v35.py"))
        for sc,outs in ANALYSIS_SCRIPTS.items():
            r=subprocess.run([sys.executable,sc],cwd=td,capture_output=True,text=True,timeout=1200)
            if r.returncode!=0:
                msgs.append(f"{sc}: fresh run failed exit {r.returncode}: {r.stderr.strip()[-140:]}");continue
            for out in outs:
                try:
                    fresh=open(os.path.join(td,out),newline="").read()
                    canon=open(os.path.join(here,out),newline="").read()
                except OSError as e:
                    msgs.append(f"{out}: {e}");continue
                if fresh==canon:continue
                fr=list(csv.reader(io.StringIO(fresh)));ca=list(csv.reader(io.StringIO(canon)))
                if len(fr)!=len(ca) or (fr and ca and fr[0]!=ca[0]):
                    msgs.append(f"{out}: structure differs from fresh recomputation");continue
                bad=0
                for i in range(1,len(fr)):
                    if len(fr[i])!=len(ca[i]):bad+=1;continue
                    for a,b in zip(fr[i],ca[i]):
                        if a==b:continue
                        try:
                            if abs(float(a)-float(b))<=1e-8:continue
                        except ValueError:pass
                        bad+=1
                if bad:msgs.append(f"{out}: {bad} cells differ from fresh recomputation beyond 1e-8")
        # v36.1: the two manuscript figures must be byte-identical to a fresh,
        # deterministic regeneration (guards against a stale figure).
        gen="generate_loyola_v35_figures.py";_sh.copy(os.path.join(here,gen),td)
        r=subprocess.run([sys.executable,gen,"--output-dir",td],cwd=td,capture_output=True,text=True,timeout=1200)
        if r.returncode!=0:msgs.append(f"{gen}: fresh run failed exit {r.returncode}: {r.stderr.strip()[-140:]}")
        else:
            for fig in ("fig_lo_prediction_correlation_heatmap_v3.pdf","fig_lo_degeneracy_order10_trees_v2.pdf"):
                try:
                    if open(os.path.join(td,"figures",fig),"rb").read()!=open(os.path.join(here,"figures",fig),"rb").read():
                        msgs.append(f"figures/{fig}: differs from fresh regeneration (stale figure)")
                except OSError as e:msgs.append(f"figures/{fig}: {e}")
            for out in (CSV_PRED,CSV_DEG,CSV_SS):
                try:
                    if open(os.path.join(td,out),newline="").read()!=open(os.path.join(here,out),newline="").read():
                        msgs.append(f"{out}: differs from fresh figure-generator output")
                except OSError as e:msgs.append(f"{out}: {e}")
    return (len(msgs)==0),msgs

# ---------------------------------------------------------------- drift guard
def _cells(row):
    return [c.strip() for c in row.rstrip().rstrip("\\").split("&")]
def fs3(x):
    """Signed 3-dp display string of a FULL-PRECISION value."""
    return f"{x:+.3f}"
def fu3(x):
    """Unsigned 3-dp display string of a FULL-PRECISION value."""
    return f"{x:.3f}"
def _num(cell, signed, allow_phantom=False, computed=None, allow_bold=False):
    """Parse a complete numeric tex token; return (string, is_bold, err).
    v36: the caller compares the returned STRING with the exact formatted
    full-precision value (no numeric tolerance)."""
    m = NUM_S.match(cell) if signed else NUM_U.match(cell)
    if m: return m.group(1), False, None
    if allow_bold and signed:
        m = NUM_SB.match(cell)
        if m: return m.group(1), True, None
    if allow_phantom and NUM_PH.match(cell):
        if computed is not None and fs3(computed) not in ("+0.000","-0.000"):
            return None, False, f"phantom-zero token but computed value {computed:+.3f} does not round to 0.000"
        return "PHANTOM0", False, None
    return None, False, f"cell '{cell}' is not a complete {'signed' if signed else 'unsigned'} 3-decimal token"
def _disp_ok(tok, exp, signed):
    """Exact display check: tok must equal the rounding of the full-precision exp."""
    if tok=="PHANTOM0":return fs3(exp) in ("+0.000","-0.000")
    return tok==(fs3(exp) if signed else fu3(abs(exp)))

def check_tex(texpath, CMP):
    """Drift guard (v36): every numeric cell of every numeric table in main.tex
    must be the EXACT display string of the full-precision value recomputed in
    this run (no tolerances). Tables: lo_octane, lo_tuning, lo_tuning_bestfixed,
    ablation (+ 100-seed median columns), multiorder, fgdss, collisions,
    octane-data. Returns (ok, msgs)."""
    msgs=[]
    try:tex=decomment_tex(open(texpath).read())
    except Exception as e:return False,[f"cannot read {texpath}: {e}"]
    if re.search(r"\\(iffalse|iftrue|ifnum|ifdim|ifcase|ifx|else|fi)(?![a-zA-Z])",tex):
        msgs.append("TeX conditional (\\if.../\\else/\\fi) present in decommented source: raw-source parsing cannot guarantee rendered table semantics; rejected")
    if re.search(r"\\catcode",tex):
        msgs.append("\\catcode change present in source: the guard's comment/token model assumes conventional catcodes; rejected")
    def block(label):
        try:
            b=tex[tex.index(r"\label{tab:%s}"%label):];return b[:b.index(r"\end{tabular}")]
        except ValueError:return None
    def _vec(nm):
        from collections import Counter
        c=Counter(tuple(sorted(q)) for q in alkane_pairs(OCTANES[NAMES.index(nm)][0]))
        return r",\,".join(f"{c[k]}({k[0]},{k[1]})" for k in sorted(c))
    SUBHDRS={r"\multicolumn{8}{l}{\emph{near} "+t+"}\\\\" for t in
             ("$M_2 = LO(1,0,0)$","$HM = LO(0,2,0)$",r"${}^{m}\!M_2 = LO(-1,0,0)$","$LO(0,0,1)$")}
    for a,b in (("3-methylheptane","4-methylheptane"),("3,4-dimethylhexane","3-ethyl-2-methylpentane")):
        if _vec(a)!=_vec(b):msgs.append(f"tab:collisions: {a} and {b} do not share a degree-pair vector")
        SUBHDRS.add(r"\multicolumn{6}{l}{\emph{shared count vector} $"+_vec(a)+"$:}\\\\")
    class _S:
        @staticmethod
        def match(t):return t in SUBHDRS
    SUBHDR=_S
    def datarows(blk,amp=None):
        """v36.1: EVERY non-rule line of the body is a data row or a whitelisted
        sub-header; rows ending in \\\\[..], \\tabularnewline, or carrying an
        unexpected \\multicolumn are reported instead of silently skipped."""
        body=blk[blk.index(r"\midrule")+len(r"\midrule"):] if r"\midrule" in blk else blk
        out=[]
        for l in body.splitlines():
            t=l.strip()
            if not t or re.fullmatch(r"\\(midrule|bottomrule|cmidrule(\(lr\))?\{[\d-]+\})+",t.replace(" ","")):continue
            if r"\multicolumn" in t and SUBHDR.match(t):continue
            if not t.endswith(r"\\") or r"\multicolumn" in t or r"\tabularnewline" in t:
                msgs.append(f"unrecognised table line (not a plain data row): '{t[:60]}'");continue
            if amp is None or t.count("&")==amp:out.append(t)
        return out
    def header_ok(blk,label,expected):
        hdr=blk[:blk.index(r"\midrule")] if r"\midrule" in blk else ""
        rows=[l.strip() for l in hdr.splitlines() if l.strip().endswith(r"\\") and "&" in l]
        if not rows or rows[-1]!=expected:
            msgs.append(f"tab:{label}: column header '{rows[-1][:70] if rows else None}' != expected '{expected[:70]}'")
    # ---- Table 2: 12 labeled rows x 5 SIGNED complete tokens ----
    blk=block("lo_octane")
    if blk is None:msgs.append("tab:lo_octane not found")
    else:
        rowsl=datarows(blk)
        if len(rowsl)!=12:msgs.append(f"tab:lo_octane: expected 12 data rows, found {len(rowsl)}")
        seen=set()
        for k,row in enumerate(rowsl[:12]):
            cs=_cells(row)
            if len(cs)!=6:
                msgs.append(f"tab:lo_octane row {k}: expected 6 cells, found {len(cs)}");continue
            if cs[0]!=T2_CELL0[k]:
                msgs.append(f"tab:lo_octane row {k}: label mismatch, expected {ROWLABELS[k]} cell exactly '{T2_CELL0[k]}', got '{cs[0][:40]}'")
            nm=ROWLABELS[k]
            for j,p in enumerate(PROPS):
                tok,bold,err=_num(cs[1+j],signed=True,allow_bold=True)
                if err:msgs.append(f"tab:lo_octane {nm}/{p}: {err}");continue
                exp=CMP["T2f"][nm][j]
                if not _disp_ok(tok,exp,True):
                    msgs.append(f"tab:lo_octane {nm}/{p}: tex {tok} vs computed {exp:+.6f} (display {fs3(exp)})")
                bestrow=max(range(12),key=lambda i:abs(CMP["T2f"][ROWLABELS[i]][j]))
                if bold!=(k==bestrow):
                    msgs.append(f"tab:lo_octane {nm}/{p}: bolding mismatch (column best is {ROWLABELS[bestrow]})")
            if row in seen:msgs.append(f"tab:lo_octane duplicated row: {row.strip()[:40]}")
            seen.add(row)
    # ---- tuning table: 4 anchor blocks x 5 property rows x 7 complete tokens ----
    blk=block("lo_tuning")
    if blk is None:msgs.append("tab:lo_tuning not found")
    else:
        body=blk[blk.index(r"\midrule"):] if r"\midrule" in blk else blk
        cur=-1;perblock=[[] for _ in ANCHORS];ndata=0
        for l in body.splitlines():
            if r"\multicolumn" in l and "near" in l:
                cur+=1
                if cur<4 and not (re.search(ANCHOR_PATS[cur],l) and l.strip() in SUBHDRS):
                    msgs.append(f"tab:lo_tuning block {cur}: anchor label mismatch, expected near {ANCHORS[cur]}, got '{l.strip()[:60]}'")
            elif l.rstrip().endswith(r"\\") and l.count("&")==7:
                ndata+=1
                if 0<=cur<4:perblock[cur].append(l)
                else:msgs.append(f"tab:lo_tuning: data row before first anchor block: '{l.strip()[:40]}'")
        if cur+1!=4:msgs.append(f"tab:lo_tuning: expected 4 anchor blocks, found {cur+1}")
        if ndata!=20:msgs.append(f"tab:lo_tuning: expected 20 data rows, found {ndata}")
        for bi,anm in enumerate(ANCHORS):
            if bi>cur:break
            if len(perblock[bi])!=5:
                msgs.append(f"tab:lo_tuning block {anm}: expected 5 rows, found {len(perblock[bi])}")
            for ri,row in enumerate(perblock[bi][:5]):
                p=PROPS[ri];cs=_cells(row)
                if len(cs)!=8:
                    msgs.append(f"tab:lo_tuning {anm}/{p}: expected 8 cells, found {len(cs)}");continue
                if cs[0]!=PROP_TEX[p]:
                    msgs.append(f"tab:lo_tuning block {anm} row {ri}: property label mismatch, expected {PROP_TEX[p]}, got '{cs[0]}'")
                r0f,r50f,bootf,l0f,l50f=CMP["E2f"][(anm,p)]
                spec=[(cs[1],False,abs(r0f),"r0"),(cs[2],False,abs(r50f),"r50"),
                      (cs[3],True,r50f-r0f,"gain_in"),(cs[4],False,bootf,"boot"),
                      (cs[5],False,abs(l0f),"LOO0"),(cs[6],False,abs(l50f),"LOO50"),
                      (cs[7],True,l50f-l0f,"gain_LOO")]
                for cell,sgn,exp,tag in spec:
                    tok,_,err=_num(cell,signed=sgn,allow_phantom=sgn,computed=exp)
                    if err:msgs.append(f"tab:lo_tuning {anm}/{p}/{tag}: {err}");continue
                    if not _disp_ok(tok,exp,sgn):
                        msgs.append(f"tab:lo_tuning {anm}/{p}/{tag}: tex {tok} vs computed {exp:+.6f} (display {fs3(exp) if sgn else fu3(exp)})")
    # ---- best-fixed table: 5 rows x (property, index, 4 unsigned tokens) ----
    blk=block("lo_tuning_bestfixed")
    if blk is None:msgs.append("tab:lo_tuning_bestfixed not found")
    else:
        rowsl=datarows(blk)
        if len(rowsl)!=5:msgs.append(f"bestfixed: expected 5 data rows, found {len(rowsl)}")
        seen=set()
        for ri,row in enumerate(rowsl[:5]):
            p=PROPS[ri];cs=_cells(row)
            if len(cs)!=6:
                msgs.append(f"bestfixed {p}: expected 6 cells, found {len(cs)}");continue
            fnm,fixrf,fixloof,decrf,decloof=CMP["Ff"][p]
            if cs[0]!=PROP_TEX[p]:
                msgs.append(f"bestfixed row {ri}: property label mismatch, expected {PROP_TEX[p]}, got '{cs[0]}'")
            if cs[1]!=IDX_TEX[fnm]:
                msgs.append(f"bestfixed {p}: best-fixed index label mismatch, expected {IDX_TEX[fnm]}, got '{cs[1]}'")
            for cell,exp,tag in [(cs[2],fixrf,"fix_r"),(cs[3],fixloof,"fix_LOO"),
                                 (cs[4],decrf,"dec_r"),(cs[5],decloof,"dec_LOO")]:
                tok,_,err=_num(cell,signed=False)
                if err:msgs.append(f"bestfixed {p}/{tag}: {err}");continue
                if not _disp_ok(tok,exp,False):
                    msgs.append(f"bestfixed {p}/{tag}: tex {tok} vs computed {exp:.6f} (display {fu3(exp)})")
            if row in seen:msgs.append(f"bestfixed duplicated row: {row.strip()[:40]}")
            seen.add(row)
    # ---- tab:ablation: panel (a) first-principles single-seed cells; panel (b) 100-seed sweep ----
    if "ABL" in CMP:
        blk=block("ablation")
        if blk is None:msgs.append("tab:ablation not found")
        else:
            rowsl=datarows(blk)
            if len(rowsl)!=5:msgs.append(f"tab:ablation: expected 5 data rows, found {len(rowsl)}")
            for ri,row in enumerate(rowsl[:5]):
                p=PROPS[ri];cs=_cells(row)
                if len(cs)!=7:msgs.append(f"tab:ablation {p}: expected 7 cells, found {len(cs)}");continue
                if cs[0]!=PROP_TEX[p]:msgs.append(f"tab:ablation row {ri}: property label mismatch, got '{cs[0]}'")
                a=CMP["ABL"][p]
                spec=[(cs[1],a["q2g"],True,"Q2_GM"),(cs[2],a["q2l"],True,"Q2_LO"),
                      (cs[3],a["q2l"]-a["q2g"],True,"dQ2"),(cs[4],a["rg"],False,"RMSE_GM"),
                      (cs[5],a["rl"],False,"RMSE_LO")]
                for cell,e,sgn,tag in spec:
                    tok,_,err=_num(cell,signed=sgn)
                    if err:msgs.append(f"tab:ablation {p}/{tag}: {err}");continue
                    if not _disp_ok(tok,e,sgn):
                        msgs.append(f"tab:ablation {p}/{tag}: tex {tok} vs computed {e:+.6f} (display {fs3(e) if sgn else fu3(e)})")
                m=NUM_FRAC.match(cs[6])
                if not m:msgs.append(f"tab:ablation {p}: LO-better cell malformed '{cs[6]}'")
                elif int(m.group(1))!=a["better"]:
                    msgs.append(f"tab:ablation {p}: LO-better {m.group(1)} vs computed {a['better']}")
            # panel (b): the second tabular inside the same table float
            try:
                k0=tex.index(r"\label{tab:ablation}");k1=tex.index(r"\end{tabular}",k0)+len(r"\end{tabular}")
                kend=tex.index(r"\end{table}",k1);seg=tex[k1:kend]
                blk2=seg[:seg.index(r"\end{tabular}")] if r"\begin{tabular}" in seg else None
            except ValueError:blk2=None
            if blk2 is None:msgs.append("tab:ablation panel (b) (100-seed sweep) not found")
            elif "EXPR" in CMP:
                rows2=datarows(blk2)
                if len(rows2)!=5:msgs.append(f"tab:ablation panel (b): expected 5 data rows, found {len(rows2)}")
                for ri,row in enumerate(rows2[:5]):
                    p=PROPS[ri];cs=_cells(row)
                    if len(cs)!=5:msgs.append(f"tab:ablation panel (b) {p}: expected 5 cells, found {len(cs)}");continue
                    if cs[0]!=PROP_TEX[p]:msgs.append(f"tab:ablation panel (b) row {ri}: property label mismatch, got '{cs[0]}'")
                    for ci,b in ((1,"200"),(2,"500")):
                        d=CMP["EXPR"].get((b,p),[])
                        if len(d)!=100:msgs.append(f"tab:ablation {p}: expanded sweep has {len(d)} seeds at budget {b}");continue
                        m=NUM_MED.match(cs[ci])
                        if not m:msgs.append(f"tab:ablation {p}: 100-seed median cell (budget {b}) malformed '{cs[ci]}'")
                        else:
                            exp=(fs3(float(np.median(d))),fs3(min(d)),fs3(max(d)))
                            if m.groups()!=exp:
                                msgs.append(f"tab:ablation {p}: 100-seed median [min,max] at budget {b}: tex {m.groups()} vs computed {exp}")
                        m=NUM_C100.match(cs[ci+2])
                        npos=sum(1 for x in d if x>0)
                        if not m:msgs.append(f"tab:ablation {p}: seed-count cell (budget {b}) malformed '{cs[ci+2]}'")
                        elif int(m.group(1))!=npos:
                            msgs.append(f"tab:ablation {p}: seeds with dQ2>0 at budget {b}: tex {m.group(1)} vs computed {npos}")
    # ---- tab:multiorder (first principles) ----
    if "MO" in CMP:
        blk=block("multiorder")
        if blk is None:msgs.append("tab:multiorder not found")
        else:
            rowsl=datarows(blk)
            if len(rowsl)!=12:msgs.append(f"tab:multiorder: expected 12 data rows, found {len(rowsl)}")
            for ri,row in enumerate(rowsl[:12]):
                if ri>=len(CMP["MO"]):break
                e=CMP["MO"][ri];cs=_cells(row)
                if len(cs)!=9:msgs.append(f"tab:multiorder row {ri}: expected 9 cells, found {len(cs)}");continue
                mset="all" if e["graph_set"]=="all_trees" else "mol."
                if cs[0]!=f"${e['n']}$" or cs[1]!=mset:
                    msgs.append(f"tab:multiorder row {ri}: label cells '{cs[0]} & {cs[1]}' vs expected ${e['n']}$ & {mset}")
                for ci,key in enumerate(["N_trees","distinct_BID_profiles","M1","M2","R","LO001","LO002"]):
                    m=NUM_INT.match(cs[2+ci])
                    if not m:msgs.append(f"tab:multiorder row {ri} col{ci+2}: malformed token '{cs[2+ci]}'");continue
                    if m.group(1)!=e[key]:
                        msgs.append(f"tab:multiorder row {ri} ({key}): tex {m.group(1)} vs computed {e[key]}")
    # ---- tab:fgdss (first principles, exact 4-dp display) ----
    if "FGD" in CMP:
        blk=block("fgdss")
        if blk is None:msgs.append("tab:fgdss not found")
        else:
            rowsl=datarows(blk)
            if len(rowsl)!=12:msgs.append(f"tab:fgdss: expected 12 data rows, found {len(rowsl)}")
            for ri,row in enumerate(rowsl[:12]):
                nm=ROWLABELS[ri];cs=_cells(row)
                if len(cs)!=4:msgs.append(f"tab:fgdss {nm}: expected 4 cells, found {len(cs)}");continue
                if cs[0]!=FGD_LABEL[nm]:msgs.append(f"tab:fgdss row {ri}: label '{cs[0]}' vs expected '{FGD_LABEL[nm]}'")
                for ci,(key,val) in enumerate(zip(["SS","Abr","ratio"],CMP["FGD"][nm])):
                    m=NUM_4.match(cs[1+ci])
                    if not m:msgs.append(f"tab:fgdss {nm} col{ci+1}: malformed token '{cs[1+ci]}'");continue
                    if m.group(1)!=f"{val:.4f}":
                        msgs.append(f"tab:fgdss {nm}/{key}: tex {m.group(1)} vs computed {val:.7f} (display {val:.4f})")
    # ---- tab:collisions (octane data) ----
    blk=block("collisions")
    if blk is None:msgs.append("tab:collisions not found")
    else:
        rowsl=datarows(blk,amp=5)
        if len(rowsl)!=4:msgs.append(f"tab:collisions: expected 4 molecule rows, found {len(rowsl)}")
        fmt=[("{:.1f}",1),("{:.2f}",2),("{:.2f}",3),("{:.2f}",4),("{:.3f}",5)]
        for ri,row in enumerate(rowsl[:4]):
            nm,oi=COLL_ROWS[ri];cs=_cells(row)
            if cs[0]!=nm:msgs.append(f"tab:collisions row {ri}: name '{cs[0]}' vs expected '{nm}'")
            for ci,(f,col) in enumerate(fmt):
                m=NUM_ANY.match(cs[1+ci])
                if not m:msgs.append(f"tab:collisions {nm} col{ci+1}: malformed token '{cs[1+ci]}'");continue
                exp=f.format(OCTANES[oi][col])
                if m.group(1)!=exp:
                    msgs.append(f"tab:collisions {nm} col{ci+1}: tex {m.group(1)} vs data {exp}")
    # ---- tab:octane-data (appendix): must reproduce octane_data.OCTANES exactly ----
    blk=block("octane-data")
    if blk is None:msgs.append("tab:octane-data not found")
    else:
        rowsl=datarows(blk)
        if len(rowsl)!=18:msgs.append(f"tab:octane-data: expected 18 rows, found {len(rowsl)}")
        for ri,row in enumerate(rowsl[:18]):
            cs=_cells(row);expname="$n$-octane" if NAMES[ri]=="octane" else NAMES[ri]
            if len(cs)!=6:msgs.append(f"tab:octane-data row {ri}: expected 6 cells, found {len(cs)}");continue
            if cs[0]!=expname:msgs.append(f"tab:octane-data row {ri}: name '{cs[0]}' vs expected '{expname}'")
            for ci in range(5):
                tok=cs[1+ci]
                if tok.startswith("$") and tok.endswith("$"):tok=tok[1:-1]
                cs[1+ci]=tok
                if not re.match(r"^-?\d+(\.\d+)?$",cs[1+ci]):
                    msgs.append(f"tab:octane-data {NAMES[ri]} col{ci+1}: malformed token '{cs[1+ci]}'");continue
                expd=("{:.1f}","{:.2f}","{:.2f}","{:.2f}","{:.3f}")[ci].format(OCTANES[ri][1+ci])
                if cs[1+ci]!=expd:
                    msgs.append(f"tab:octane-data {NAMES[ri]}/{PROPS[ci]}: tex {cs[1+ci]} vs octane_data {OCTANES[ri][1+ci]}")
    for lab,exp in HEADERS.items():
        b=block(lab)
        if b is not None:header_ok(b,lab,exp)
    try:
        k0=tex.index(r"\label{tab:ablation}");k1=tex.index(r"\end{tabular}",k0)
        header_ok(tex[k1+len(r"\end{tabular}"):tex.index(r"\end{tabular}",k1+1)],"ablation(b)",
                  r"Property & $B = 200$ & $B = 500$ & $B = 200$ & $B = 500$\\")
    except ValueError:msgs.append("tab:ablation panel (b) header not found")
    return (len(msgs)==0),msgs

# ------------------------------------------------------------ CSV schema check
def expected_csv_texts(CMP):
    """Rebuild the three canonical CSVs from the executed computation with the
    generator's exact formats. Returns {filename: text} (csv.writer, CRLF)."""
    out={}
    R=np.array([CMP["T2f"][nm] for nm in ROWLABELS])
    best=[int(np.argmax(np.abs(R[:,j]))) for j in range(5)]
    s=io.StringIO();w=csv.writer(s)
    w.writerow(["index"]+PROPS+["best_in"])
    for i,nm in enumerate(ROWLABELS):
        row=[nm]+[f"{R[i,j]:+.10f}"+("*" if best[j]==i else "") for j in range(5)]
        row.append("; ".join(PROPS[j] for j in range(5) if best[j]==i));w.writerow(row)
    out[CSV_PRED]=s.getvalue()
    s=io.StringIO();w=csv.writer(s)
    w.writerow(["index","N_trees","distinct_values","degeneracy_pct"])
    for nm in ROWLABELS:
        k=CMP["degk"][nm];w.writerow([nm,106,k,f"{100*(1-k/106):.2f}"])
    out[CSV_DEG]=s.getvalue()
    s=io.StringIO();w=csv.writer(s)
    w.writerow(["index","SS","Abr","SA"])
    for nm in ROWLABELS:
        ss,ab=CMP["ss"][nm],CMP["ab"][nm]
        w.writerow([nm,f"{ss:.10f}",f"{ab:.10f}",f"{ss/ab:.10f}"])
    out[CSV_SS]=s.getvalue()
    return out

def check_csvs(dirpath, CMP):
    """Validate all three canonical CSVs against computation-derived expected
    files: byte identity, exact header, row keys/order/count, exact cell strings,
    and derived-field recomputation. Returns (ok, msgs)."""
    msgs=[];exp_all=expected_csv_texts(CMP)
    for fn,exp_text in exp_all.items():
        path=os.path.join(dirpath,fn)
        if not os.path.exists(path):
            msgs.append(f"{fn}: missing required canonical CSV");continue
        try:act_text=open(path,newline="").read()
        except Exception as e:
            msgs.append(f"{fn}: unreadable: {e}");continue
        if act_text==exp_text:continue
        # not byte-identical -> emit precise cell-level diagnostics
        er=list(csv.reader(io.StringIO(exp_text)));ar=list(csv.reader(io.StringIO(act_text)))
        if ar and er and ar[0]!=er[0]:
            msgs.append(f"{fn}: header mismatch: {ar[0]} vs expected {er[0]}")
        if len(ar)!=len(er):
            msgs.append(f"{fn}: expected {len(er)-1} data rows, found {len(ar)-1}")
        for k in range(1,min(len(ar),len(er))):
            if len(ar[k])!=len(er[k]):
                msgs.append(f"{fn} row {k}: expected {len(er[k])} columns, found {len(ar[k])}");continue
            if ar[k][0]!=er[k][0]:
                msgs.append(f"{fn} row {k}: index key '{ar[k][0]}' vs expected '{er[k][0]}' (order/rename)")
            for c in range(1,len(er[k])):
                if ar[k][c]!=er[k][c]:
                    msgs.append(f"{fn} row {k} ({er[k][0]}) col '{er[0][c]}': '{ar[k][c]}' vs expected '{er[k][c]}'")
        if len(msgs)==0 or (msgs and not msgs[-1].startswith(fn)):
            msgs.append(f"{fn}: differs from computation-derived canonical bytes")
    # independent derived-field recomputation on the actual files
    dpath=os.path.join(dirpath,CSV_DEG)
    if os.path.exists(dpath):
        try:
            for r in csv.DictReader(open(dpath,newline="")):
                N=int(r["N_trees"]);k=int(r["distinct_values"])
                if N!=106:msgs.append(f"{CSV_DEG} {r['index']}: N_trees {N} != 106")
                if abs(float(r["degeneracy_pct"])-100*(1-k/N))>6e-3:
                    msgs.append(f"{CSV_DEG} {r['index']}: degeneracy_pct {r['degeneracy_pct']} != 100(1-{k}/{N})")
        except Exception as e:msgs.append(f"{CSV_DEG}: derived-field check failed: {e}")
    spath=os.path.join(dirpath,CSV_SS)
    if os.path.exists(spath):
        try:
            for r in csv.DictReader(open(spath,newline="")):
                ss,ab,sa=float(r["SS"]),float(r["Abr"]),float(r["SA"])
                if not(math.isfinite(ss) and math.isfinite(ab) and math.isfinite(sa)):
                    msgs.append(f"{CSV_SS} {r['index']}: non-finite cell")
                elif abs(sa-ss/ab)>1e-9:
                    msgs.append(f"{CSV_SS} {r['index']}: SA {sa} inconsistent with SS/Abr {ss/ab:.10f}")
        except Exception as e:msgs.append(f"{CSV_SS}: derived-field check failed: {e}")
    return (len(msgs)==0),msgs

def _strip_paren(t):
    prev=None
    while prev!=t:prev=t;t=re.sub(r"\([^()]*\)","",t)
    return t
_PNUM=re.compile(r"(?<![\d.])[-+]?\d+\.\d+")
def prov_values(t):
    """Numeric source values of a provenance cell: parenthetical working
    (e.g. '(427.2/4.184)', '(no conversion; rounds to 0.34)') is removed first,
    and a hyphen between two numbers is a range separator, not a sign."""
    return [float(x) for x in _PNUM.findall(_strip_paren(t or ""))]
def prov_paper(t):
    m=_PNUM.search(t or "") or re.search(r"[-+]?\d+",t or "")
    return float(m.group(0)) if m else None
def prov_expected_class(prop,paper,cands):
    """Strict taxonomy: matched at reported precision (|diff| <= half a unit of
    the last reported digit, or inside the span of the recorded determinations)
    -> VERIFIED; else within PROV_TOL -> AGREEMENT WITHIN TOLERANCE; else CONFLICT."""
    lo_,hi_=min(cands),max(cands)
    d=0.0 if lo_<=paper<=hi_ else min(abs(paper-lo_),abs(paper-hi_))
    if d<=PROV_HALF[prop]+1e-9:return {"VERIFIED EXACT","VERIFIED AFTER UNIT CONVERSION"},d
    if d<=PROV_TOL[prop]+1e-9:return {"AGREEMENT WITHIN TOLERANCE"},d
    return {"CONFLICT"},d

def check_v35_extras(dirpath):
    """v36 checks: (a) FGD published-control CSV consistent with the canonical
    full-precision FGD CSV and the hard-coded Barman-Das Table 10 decane values
    (agreement class from the 4-dp ROUNDING of the full-precision value: 11 exact,
    3 within one unit of the 4th decimal, none worse); (b) robustness CSVs
    (3-seed and 100-seed) consistent with the ablation summary and with the
    sign counts stated in the manuscript; (c) provenance CSV: schema, paper
    values identical to octane_data.OCTANES, value-aware classification and
    counts; (d) omega / S source-sensitivity CSVs vs live recomputation.
    Returns (ok, msgs)."""
    msgs=[]
    try:
        fgd={r["index"]:(float(r["SS_fgd"]),float(r["Abr_fgd"]))
             for r in csv.DictReader(open(os.path.join(dirpath,CSV_FGD),newline=""))}
        ctrl=list(csv.DictReader(open(os.path.join(dirpath,CSV_CTRL),newline="")))
        exact=0;ulp=0
        seen=set()
        for r in ctrl:
            k=r["index"];qty=r["quantity"];seen.add((k,qty))
            pv=FGD_PUBLISHED[k][0 if qty=="SS" else 1]
            mv=fgd[k][0 if qty=="SS" else 1]
            if abs(float(r["published_BarmanDas2026_Table10_decane"])-pv)>1e-12:
                msgs.append(f"{CSV_CTRL} {k}/{qty}: published value differs from primary-source constant")
            if abs(float(r["ours"])-mv)>1e-12:
                msgs.append(f"{CSV_CTRL} {k}/{qty}: 'ours' differs from canonical FGD CSV")
            units=round(abs(round(mv,4)-pv)*1e4)
            cls="exact_at_4dp" if units==0 else ("within_1_unit_4th_dp" if units==1 else "worse")
            if cls=="exact_at_4dp":exact+=1
            elif cls=="within_1_unit_4th_dp":ulp+=1
            else:msgs.append(f"{CSV_CTRL} {k}/{qty}: rounded value {mv:.4f} differs from published {pv} by {units} units")
            if r["agreement"]!=cls:msgs.append(f"{CSV_CTRL} {k}/{qty}: agreement '{r['agreement']}' != derived '{cls}'")
        if len(seen)!=14:msgs.append(f"{CSV_CTRL}: expected 14 comparisons, found {len(seen)}")
        if not(exact==11 and ulp==3):
            msgs.append(f"{CSV_CTRL}: agreement counts exact={exact}, 1unit={ulp}, expected 11/3")
        rob=list(csv.DictReader(open(os.path.join(dirpath,CSV_ROB),newline="")))
        if len(rob)!=30:msgs.append(f"{CSV_ROB}: expected 30 rows, found {len(rob)}")
        abl={}
        for r in csv.DictReader(open(os.path.join(dirpath,CSV_ABL),newline="")):
            abl[(r["property"],r["model"])]=float(r["Q2"])
        by={}
        for r in rob:
            by.setdefault(r["property"],[]).append(float(r["dQ2"]))
            if r["seed"]=="12345" and r["budget"]=="200":
                dref=abl[(r["property"],"LO")]-abl[(r["property"],"GM")]
                if abs(float(r["dQ2"])-dref)>1e-8:
                    msgs.append(f"{CSV_ROB} {r['property']}: canonical-config dQ2 {r['dQ2']} vs ablation_summary {dref:+.10f}")
        if not all(x>0 for x in by.get("dHvap",[])):msgs.append(f"{CSV_ROB}: dHvap dQ2 not consistently positive")
        if not all(x<0 for x in by.get("dHf",[])):msgs.append(f"{CSV_ROB}: dHf dQ2 not consistently negative")
        tb=by.get("T_B",[])
        if tb and not(min(tb)<0<max(tb)):msgs.append(f"{CSV_ROB}: T_B dQ2 unexpectedly consistent in sign")
        # provenance CSV: schema + data identity + VALUE-AWARE classification rules + counts
        prov=list(csv.DictReader(open(os.path.join(dirpath,CSV_PROV),newline="")))
        if len(prov)!=90:msgs.append(f"{CSV_PROV}: expected 90 rows, found {len(prov)}")
        permol={};clscnt={}
        for r in prov:
            permol[r["molecule"]]=permol.get(r["molecule"],0)+1
            c=r["classification"];prop=r["property"]
            if c not in PROV_EXPECT:msgs.append(f"{CSV_PROV}: illegal classification '{c}'")
            clscnt[c]=clscnt.get(c,0)+1
            paper=prov_paper(r["paper_value"])
            if r["molecule"] not in NAMES or prop not in PROPS:
                msgs.append(f"{CSV_PROV}: unknown molecule/property {r['molecule']}/{prop}");continue
            dv=OCTANES[NAMES.index(r["molecule"])][1+PROPS.index(prop)]
            if paper is None or abs(paper-dv)>1e-12:
                msgs.append(f"{CSV_PROV} {r['molecule']}/{prop}: paper_value '{r['paper_value']}' != octane_data value {dv}")
            if c in ("VERIFIED EXACT","VERIFIED AFTER UNIT CONVERSION","AGREEMENT WITHIN TOLERANCE"):
                cands=prov_values(r["converted_value"])
                if not cands and prop=="omega":cands=prov_values(r["source_value"])[:1]
                if paper is None or not cands:
                    msgs.append(f"{CSV_PROV} {r['molecule']}/{prop}: class '{c}' but no numeric source value to check");continue
                want,d=prov_expected_class(prop,paper,cands)
                if c not in want:
                    msgs.append(f"{CSV_PROV} {r['molecule']}/{prop}: class '{c}' inconsistent with |paper-source|={d:.4g} (rule says {sorted(want)})")
        if len(permol)!=18 or any(v!=5 for v in permol.values()):
            msgs.append(f"{CSV_PROV}: not 18 molecules x 5 properties")
        for k,v in PROV_EXPECT.items():
            if clscnt.get(k,0)!=v:
                msgs.append(f"{CSV_PROV}: {k} count {clscnt.get(k,0)} != manuscript claim {v}")
        ex=list(csv.DictReader(open(os.path.join(dirpath,CSV_EXPR),newline="")))
        if len(ex)!=1000:msgs.append(f"{CSV_EXPR}: expected 1000 rows, found {len(ex)}")
        cnt={};pcnt={}
        for r in ex:
            k=(r["budget"],r["property"]);d=float(r["dQ2"]);dp=float(r["dQ2_paired"])
            a,b=cnt.get(k,(0,0));cnt[k]=(a+(d>0),b+(d<0))
            a,b=pcnt.get(k,(0,0));pcnt[k]=(a+(dp>0),b+(dp<0))
            if abs(float(r["Q2_LO"])-float(r["Q2_GM"])-d)>1e-9 or abs(float(r["Q2_LO"])-float(r["Q2_LOzero"])-dp)>1e-9:
                msgs.append(f"{CSV_EXPR} {k} seed {r['seed']}: dQ2 columns inconsistent with Q2 columns")
        for k,exp in EXPR_SIGNS.items():
            if cnt.get(k)!=exp:
                msgs.append(f"{CSV_EXPR}: sign counts for {k} = {cnt.get(k)} != expected {exp} (manuscript claim)")
        for k,exp in EXPR_PAIRED.items():
            if pcnt.get(k)!=exp:
                msgs.append(f"{CSV_EXPR}: paired sign counts for {k} = {pcnt.get(k)} != expected {exp} (manuscript claim)")
        smry=list(csv.DictReader(open(os.path.join(dirpath,CSV_EXPS),newline="")))
        if len(smry)!=10:msgs.append(f"{CSV_EXPS}: expected 10 rows, found {len(smry)}")
        for r in smry:
            k=(r["budget"],r["property"])
            if k in cnt and (int(r["LO_better"]),int(r["LO_worse"]))!=cnt[k]:
                msgs.append(f"{CSV_EXPS} {k}: summary counts disagree with detail rows")
            if k in pcnt and (int(r["paired_better"]),int(r["paired_worse"]))!=pcnt[k]:
                msgs.append(f"{CSV_EXPS} {k}: paired summary counts disagree with detail rows")
        OPl=[alkane_pairs(r_[0]) for r_ in OCTANES]
        for fn,j,alt,pre in ((CSV_OMEG,5,OMEGA_ALT,"omega"),(CSV_SSEN,4,S_ALT,"S")):
            y0=np.array([r_[j] for r_ in OCTANES]);y1=y0.copy()
            for nm_,v_ in alt.items():y1[NAMES.index(nm_)]=v_
            om=list(csv.DictReader(open(os.path.join(dirpath,fn),newline="")))
            if len(om)!=12:msgs.append(f"{fn}: expected 12 rows, found {len(om)}")
            for r in om:
                t=RED.get(r["index"])
                if t is None:msgs.append(f"{fn}: unknown index {r['index']}");continue
                x=np.array([lo_pairs(P,*t) for P in OPl])
                def rr(yv):
                    xc=x-x.mean();yc=yv-yv.mean()
                    return float(xc@yc/(np.linalg.norm(xc)*np.linalg.norm(yc)))
                if abs(float(r[f"r_{pre}_original"])-rr(y0))>1e-9 or abs(float(r[f"r_{pre}_alternative"])-rr(y1))>1e-9:
                    msgs.append(f"{fn} {r['index']}: values differ from live recomputation")
        mt=os.path.join(dirpath,"main.tex")
        if os.path.exists(mt) and "fig_lo_structure_sensitivity" in open(mt).read():
            msgs.append("main.tex references the retired sigma/mu proxy figure fig_lo_structure_sensitivity_*")
    except (OSError,KeyError,ValueError) as e:
        msgs.append(f"v35 extras check failed: {e!r}")
    return (len(msgs)==0),msgs

def check_parser_sanity(HAVE_NX):
    """[P] SMILES-parser audit: each of the 18 structures must be a connected
    acyclic 8-carbon graph with 7 edges and Delta<=4; the 18 structures must
    be pairwise non-isomorphic. The parser is alkane-only by design."""
    msgs=[]
    hashes=[]
    from octane_data import alkane_adj
    for smi,*_ in OCTANES:
        adj=alkane_adj(smi)
        P=sorted(tuple(sorted((len(adj[u]),len(adj[v])))) for u in adj for v in adj[u] if u<v)
        if P!=sorted(tuple(sorted(p)) for p in alkane_pairs(smi)):msgs.append(f"{smi}: alkane_pairs disagrees with alkane_adj")
        n=len(adj);m=sum(len(v) for v in adj.values())//2
        if n!=8 or m!=7:msgs.append(f"{smi}: {n} atoms / {m} edges (expected 8/7)")
        seen={0};stk=[0]
        while stk:
            u=stk.pop()
            for v in adj[u]:
                if v not in seen:seen.add(v);stk.append(v)
        if len(seen)!=n:msgs.append(f"{smi}: not connected")
        if max(len(v) for v in adj.values())>4:msgs.append(f"{smi}: Delta>4")
        if HAVE_NX:
            import networkx as nx
            G=nx.Graph();G.add_nodes_from(adj)
            for u in adj:
                for v in adj[u]:G.add_edge(u,v)
            if not nx.is_tree(G):msgs.append(f"{smi}: not a tree")
            hashes.append(nx.weisfeiler_lehman_graph_hash(G,iterations=10))
    if HAVE_NX and len(set(hashes))!=18:
        msgs.append(f"structures pairwise distinct: {len(set(hashes))}/18")
    for Dm,expect in ((1,1),(2,3),(3,4),(4,4)):
        Pd=[(i,j) for i in range(1,Dm+1) for j in range(i,Dm+1)]
        Z=np.array([[1.0,math.log(i*j),math.log(i+j),abs(i-j)/(i+j)] for i,j in Pd])
        rk=int(np.linalg.matrix_rank(Z))
        if rk!=expect:msgs.append(f"prop:indep rank check Delta={Dm}: rank {rk} != {expect}")
    return (len(msgs)==0),msgs

# ------------------------------------------- first-principles table recomputations
def ablation_first_principles(OP,Y,seed,budget):
    """Matched-budget nested LOO (GM = LO(a,b,0) vs LO = LO(a,b,g)), recomputed
    independently of ablation_gm_vs_lo.py: candidate descriptors by vectorised
    edge sums, inner selection by hat-matrix PRESS RMSE (argmin, first on ties),
    OLS refit on the 17 training isomers, outer prediction of the held-out one.
    Candidate stream: default_rng(seed); LO triples U(-2,2)^(budget x 3) rounded
    to 3 dp drawn FIRST, then GM pairs U(-2,2)^(budget x 2) rounded to 3 dp."""
    rng=np.random.default_rng(seed)
    lo=np.round(rng.uniform(-2,2,(budget,3)),3)
    gm=np.column_stack([np.round(rng.uniform(-2,2,(budget,2)),3),np.zeros(budget)])
    def desc(T):
        X=np.zeros((len(T),len(OP)))
        for m,Pp in enumerate(OP):
            for i,j in Pp:
                X[:,m]+=(i*j)**T[:,0]*(i+j)**T[:,1]*np.exp(T[:,2]*abs(i-j)/(i+j))
        return X
    def press(Xt,yt):
        n=Xt.shape[1];xc=Xt-Xt.mean(1,keepdims=True);Sxx=(xc**2).sum(1,keepdims=True)
        const=Sxx<=1e-12*np.maximum(1.0,(Xt**2).sum(1,keepdims=True))
        Ss=np.where(const,1.0,Sxx);yc=yt-yt.mean()
        b=np.where(const,0.0,(xc*yc).sum(1,keepdims=True)/Ss)
        e=yc-b*xc;h=1.0/n+np.where(const,0.0,xc**2/Ss)
        return np.sqrt(((e/(1-h))**2).mean(1))
    def nested(X,y,C):
        n=len(y);pred=np.empty(n);sel=[]
        for i in range(n):
            m=np.arange(n)!=i;k=int(np.argmin(press(X[:,m],y[m])));x=X[k];xt=x[m];yt=y[m]
            if np.ptp(xt)<=1e-12*max(1.0,float(np.abs(xt).max())):pred[i]=yt.mean()
            else:
                b=((xt-xt.mean())*(yt-yt.mean())).sum()/((xt-xt.mean())**2).sum()
                pred[i]=yt.mean()+b*(x[i]-xt.mean())
            sel.append(tuple(float(v) for v in C[k]))
        return pred,sel
    Xl,Xg=desc(lo),desc(gm);out={}
    for p in PROPS:
        y=Y[p];pg,sg=nested(Xg,y,gm);pl,sl=nested(Xl,y,lo)
        ss=((y-y.mean())**2).sum()
        out[p]=dict(q2g=1-((y-pg)**2).sum()/ss,q2l=1-((y-pl)**2).sum()/ss,
                    rg=float(np.sqrt(((pg-y)**2).mean())),rl=float(np.sqrt(((pl-y)**2).mean())),
                    better=int((np.abs(pl-y)<np.abs(pg-y)-1e-9).sum()),sel_lo=sl,sel_gm=sg)
    return out

def _ahu(adj):
    """Canonical string of an unrooted tree (centre-rooted AHU encoding)."""
    deg={u:len(adj[u]) for u in adj};leaves=[u for u in adj if deg[u]<=1]
    rem=len(adj);gone=set()
    while rem>2:
        nl=[]
        for u in leaves:
            gone.add(u);rem-=1
            for v in adj[u]:
                if v not in gone:
                    deg[v]-=1
                    if deg[v]==1:nl.append(v)
        leaves=nl
    cs=[u for u in adj if u not in gone]
    def enc(u,par):return "("+"".join(sorted(enc(v,u) for v in adj[u] if v!=par))+")"
    return min(enc(c,None) for c in cs)

def fgd_first_principles(dec,RED):
    """FGD (2013) SS/Abr on the decane class, independent of
    fgd_structure_sensitivity.py: neighbours by single-edge relocation within
    Delta<=4, identified by AHU canonical forms (not WL hashes); index values
    by exact edge-degree-pair sums with math.fsum."""
    A=[{u:set(T.neighbors(u)) for u in T} for T in dec]
    cid={_ahu(a):i for i,a in enumerate(A)}
    assert len(cid)==len(A)
    nb=[set() for _ in A]
    for gi,a in enumerate(A):
        for u in a:
            for v in a[u]:
                if u>v:continue
                b={k:set(w) for k,w in a.items()};b[u].discard(v);b[v].discard(u)
                comp={u};st=[u]
                while st:
                    x=st.pop()
                    for y in b[x]:
                        if y not in comp:comp.add(y);st.append(y)
                other=set(b)-comp
                for x in comp:
                    for y in other:
                        if {x,y}=={u,v} or len(b[x])>=4 or len(b[y])>=4:continue
                        c={k:set(w) for k,w in b.items()};c[x].add(y);c[y].add(x)
                        j=cid[_ahu(c)]
                        if j!=gi:nb[gi].add(j)
    out={}
    for nm,(al,be,ga) in RED.items():
        v=[math.fsum((len(a[x])*len(a[y]))**al*(len(a[x])+len(a[y]))**be
                     *math.exp(ga*abs(len(a[x])-len(a[y]))/(len(a[x])+len(a[y])))
                     for x in a for y in a[x] if x<y) for a in A]
        ss=[];ab=[]
        for i in range(len(A)):
            d=[abs(v[j]-v[i])/v[i] for j in nb[i]];ss.append(math.fsum(d)/len(d));ab.append(max(d))
        SS=math.fsum(ss)/len(A);AB=math.fsum(ab)/len(A);out[nm]=(SS,AB,SS/AB)
    return out

def multiorder_first_principles(nx,logr):
    """tab:multiorder rows: N trees, distinct edge-degree-pair profiles and
    distinct values (rounded to 9 dp) of M1, M2, R, LO(0,0,1), LO(0,0,2)."""
    from collections import Counter
    rows=[]
    for n in range(7,13):
        T=list(nx.nonisomorphic_trees(n))
        for gs,S in (("all_trees",T),("molecular",[t for t in T if max(d for _,d in t.degree())<=4])):
            prof=set(tuple(sorted(Counter(tuple(sorted((t.degree(u),t.degree(v)))) for u,v in t.edges()).items())) for t in S)
            r={"n":str(n),"graph_set":gs,"N_trees":str(len(S)),"distinct_BID_profiles":str(len(prof))}
            for key,tr in (("M1",(0,1,0)),("M2",(1,0,0)),("R",(-0.5,0,0)),("LO001",(0,0,1)),("LO002",(0,0,2))):
                r[key]=str(len(set(round(logr(t,*tr),9) for t in S)))
            rows.append(r)
    return rows

# ------------------------------------------------------------------ computation
def run_computation(HAVE_NX, quiet=False):
    """Sections A-M. Returns (fails, rows, folds_out, CMP)."""
    P=print if not quiet else (lambda *a,**k:None)
    OP=[alkane_pairs(r[0]) for r in OCTANES]
    Y={p:np.array([r[1+i] for r in OCTANES]) for i,p in enumerate(PROPS)}
    n=18;rows=[];fails=0;folds_out=[];CMP={"T2f":{},"E2f":{},"Ff":{},"degk":{},"ss":{},"ab":{}}
    def rec(sec,item,got,exp,tol,ok=None):
        nonlocal fails
        if ok is None:
            try:ok=abs(float(got)-float(exp))<=tol
            except Exception:ok=(got==exp)
        if not ok:fails+=1;P(f"  MISMATCH {sec}/{item}: {got} vs {exp}")
        rows.append(dict(section=sec,item=item,computed=got,manuscript=exp,ok=ok))
    def col(t,pl=None):
        a,b,g=t;pl=OP if pl is None else pl
        return np.array([lo_pairs(Pr,a,b,g) for Pr in pl])

    P("[A] Table 2 (60 cells)")
    for nm,t in RED.items():
        x=col(t);CMP["T2f"][nm]=[]
        for j,p in enumerate(PROPS):
            got=r_signed(x,Y[p]);exp=MS_T2[nm][j];CMP["T2f"][nm].append(got)
            ok=abs(abs(got)-abs(exp))<=0.0006 and (abs(exp)<0.006 or np.sign(round(got,3))==np.sign(exp))
            if not ok:fails+=1;P(f"  MISMATCH A/{nm}/{p}")
            rows.append(dict(section="A",item=f"{nm}/{p}",computed=round(got,3),manuscript=exp,ok=ok))
    P("  done")

    P("[B] bolded-cell bootstrap half-widths (B=10000, seed 0); manuscript range 'about 0.02-0.10'")
    for nm,p in BOLD:
        hw=boot_hw(col(RED[nm]),Y[p])
        rec("B",f"{nm}/{p}",round(hw,3),"0.02-0.10",0,ok=0.01<=hw<=0.11)
        P(f"    {nm}/{p}: {hw:.3f}")

    P("[C] deletion influence (bolded cells); manuscript 'at most 0.027'")
    mx=0
    for nm,p in BOLD:
        x=col(RED[nm]);y=Y[p];base=absr(x,y)
        d=max(abs(absr(np.delete(x,i),np.delete(y,i))-base) for i in range(n));mx=max(mx,d)
        rec("C",f"{nm}/{p}",round(d,4),"<=0.0275",0,ok=d<=0.0275)
    P(f"    overall max = {mx:.4f}")

    P("[D] descriptive post-selection paired bootstrap (top-2 per property, B=10000, seed 1)")
    for p in PROPS:
        y=Y[p];rk=sorted(RED,key=lambda nm:-absr(col(RED[nm]),y))
        xa,xb=col(RED[rk[0]]),col(RED[rk[1]]);rng=np.random.default_rng(1);d=[]
        for _ in range(10000):
            idx=rng.integers(0,n,n);d.append(absr(xa[idx],y[idx])-absr(xb[idx],y[idx]))
        lo_,hi=np.percentile(d,[2.5,97.5])
        rec("D",p,f"[{lo_:+.3f},{hi:+.3f}]","contains 0",0,ok=lo_<=0<=hi)
        P(f"    {p}: [{lo_:+.3f},{hi:+.3f}] ({rk[0]} vs {rk[1]})")

    P("[E] E2 tuning (r0, r50, +-boot, LOO0, LOO50 x 20) + per-cell metrics + fold export")
    ANCH=[("M2",(1.,0.,0.)),("HM",(0.,2.,0.)),("mM2",(-1.,0.,0.)),("LO(0,0,1)",(0.,0.,1.))]
    # v36: ONE random stream, default_rng(42), draws the five 50-triple pools in
    # a fixed order -- M2, HM, mM2, LO(0,0,1) (tab:lo_tuning) and then LO(0,0,2).
    # tab:lo_tuning_bestfixed [F] REUSES the LO(0,0,1) pool of tab:lo_tuning
    # (it no longer re-seeds), so the two tables are drawn from identical pools.
    rng=np.random.default_rng(42);POOLS={}
    for anm,(a0,b0,g0) in ANCH+[("LO(0,0,2)",(0.,0.,2.))]:
        perts=[]
        for _ in range(50):
            da,db,dg=(round(float(rng.uniform(-0.3,0.3)),2) for _ in range(3))
            perts.append((round(a0+da,2),round(b0+db,2),round(g0+dg,2)))
        POOLS[anm]=perts
    CMP["POOLS"]=POOLS
    for anm,(a0,b0,g0) in ANCH:
        perts=POOLS[anm]
        pc=[col(t) for t in perts];xb=col((a0,b0,g0))
        for p in PROPS:
            y=Y[p];e=MS_E2[(anm,p)]
            r0f=absr(xb,y);r50f=max(absr(c,y) for c in pc);bootf=boot_hw(xb,y)
            l0f=absr(loo_pred(xb,y),y)
            rec("E",f"{anm}/{p}/r0",round(r0f,3),e[0],0.0015)
            rec("E",f"{anm}/{p}/r50",round(r50f,3),e[1],0.0015)
            rec("E",f"{anm}/{p}/boot",round(bootf,3),e[2],0.0015)
            rec("E",f"{anm}/{p}/LOO0",round(l0f,3),e[3],0.0015)
            pred=np.empty(n)
            for i in range(n):
                m=np.ones(n,bool);m[i]=False;yt=y[m]
                bk,bt=-1,-1.0
                for kk,c in enumerate(pc):
                    rr=absr(c[m],yt)
                    if rr>bt:bt,bk=rr,kk
                x=pc[bk];xt=x[m]
                if xt.var()==0:pred[i]=yt.mean()
                else:
                    b=((xt-xt.mean())*(yt-yt.mean())).sum()/((xt-xt.mean())**2).sum()
                    pred[i]=(yt.mean()-b*xt.mean())+b*x[i]
                folds_out.append(dict(anchor=anm,prop=p,heldout=i,triple=str(perts[bk]),
                                      pred=round(float(pred[i]),4),actual=float(y[i])))
            l50f=absr(pred,y)
            rec("E",f"{anm}/{p}/LOO50",round(l50f,3),e[4],0.0015)
            CMP["E2f"][(anm,p)]=(r0f,r50f,bootf,l0f,l50f)
            sr,q2,mae,rmse=metr(pred,y)
            for lbl,val in [("signed_r",sr),("Q2",q2),("MAE",mae),("RMSE",rmse)]:
                rows.append(dict(section="E_metrics",item=f"{anm}/{p}/{lbl}",computed=round(val,4),
                                 manuscript="(exported)",ok=(sr>0 and q2>0)))
            if not(sr>0 and q2>0):fails+=1;P(f"  PATHOLOGY {anm}/{p}")
    cp=loo_pred(np.ones(n),Y["T_B"]);sr,q2,_,_=metr(cp,Y["T_B"])
    rec("E","constant_control_signed_r",round(sr,3),-1.0,1e-6)
    rec("E","constant_control_Q2",round(q2,3),round(-35/289,3),1e-6)
    P(f"    constant control: signed r={sr:+.3f}, Q2={q2:+.3f} (pathology exhibited; screened)")

    P("[F] best-fixed table (20 values); best-fixed index DERIVED by ranking, not assumed")
    pools={a:[col(t) for t in POOLS[a]] for a in ("LO(0,0,1)","LO(0,0,2)")}  # same pools as [E]
    for p in PROPS:
        y=Y[p];fnm_ms,fr,floo,rdec,ldec=MS_F[p]
        fnm=max(RED,key=lambda nm:absr(col(RED[nm]),y))
        rec("F",f"{p}/fix_index_derived",fnm,fnm_ms,0,ok=(fnm==fnm_ms))
        fixrf=absr(col(RED[fnm]),y);fixloof=absr(loo_pred(col(RED[fnm]),y),y)
        rec("F",f"{p}/fix_r",round(fixrf,3),fr,0.0015)
        rec("F",f"{p}/fix_LOO",round(fixloof,3),floo,0.0015)
        decrf=max(max(absr(c,y) for c in pools[a]) for a in pools)
        rec("F",f"{p}/dec_r",round(decrf,3),rdec,0.0015)
        best=-1
        for a in pools:
            pc=pools[a];pred=np.empty(n)
            for i in range(n):
                m=np.ones(n,bool);m[i]=False;yt=y[m]
                bk,bt=-1,-1.0
                for kk,c in enumerate(pc):
                    rr=absr(c[m],yt)
                    if rr>bt:bt,bk=rr,kk
                x=pc[bk];xt=x[m]
                b=((xt-xt.mean())*(yt-yt.mean())).sum()/((xt-xt.mean())**2).sum()
                pred[i]=(yt.mean()-b*xt.mean())+b*x[i]
            best=max(best,absr(pred,y))
        rec("F",f"{p}/dec_LOO",round(best,3),ldec,0.0015)
        CMP["Ff"][p]=(fnm,fixrf,fixloof,decrf,best)
        r50_lo1=CMP["E2f"][("LO(0,0,1)",p)][1]
        rec("F",f"{p}/dec_r>=tuning_LO001_r50",f"{decrf:.6f}>={r50_lo1:.6f}","consistent pools",0,ok=decrf>=r50_lo1-1e-15)
    P("  done")

    P("[H] matched-budget nested GM-vs-LO ablation recomputed from first principles (seed 12345, budget 200)")
    CMP["ABL"]=ablation_first_principles(OP,Y,12345,200)
    for p in PROPS:
        a=CMP["ABL"][p]
        P(f"    {p}: Q2_GM={a['q2g']:+.7f} Q2_LO={a['q2l']:+.7f} dQ2={a['q2l']-a['q2g']:+.7f} "
          f"RMSE_GM={a['rg']:.7f} RMSE_LO={a['rl']:.7f} LO better {a['better']}/18 max|g|={max(abs(t[2]) for t in a['sel_lo']):.3f}")
        rows.append(dict(section="H",item=f"{p}/Q2_GM|Q2_LO|dQ2|RMSE_GM|RMSE_LO|better",
            computed=f"{a['q2g']:.10f}|{a['q2l']:.10f}|{a['q2l']-a['q2g']:+.10f}|{a['rg']:.10f}|{a['rl']:.10f}|{a['better']}",
            manuscript="(guarded in [T])",ok=True))
    gmax=max(abs(t[2]) for p in PROPS for t in CMP["ABL"][p]["sel_lo"])
    rec("H","max_abs_selected_gamma",f"{gmax:.3f}","0.480",0,ok=f"{gmax:.3f}"=="0.480")
    dsel=set(CMP["ABL"]["dHvap"]["sel_lo"])
    rec("H","dHvap_identical_triple_all_folds",str(sorted(dsel)),"[(-0.27, 0.271, 0.239)]",0,ok=dsel=={(-0.27,0.271,0.239)})

    if HAVE_NX:
        import networkx as nx
        def logr(G,a,b,g):
            return sum((G.degree(u)*G.degree(v))**a*(G.degree(u)+G.degree(v))**b
                       *math.exp(g*abs(G.degree(u)-G.degree(v))/(G.degree(u)+G.degree(v))) for u,v in G.edges())
        P("[G] 106 trees / 75 decanes: ALL 12 degeneracy + SS/Abr/SA values")
        trees=list(nx.nonisomorphic_trees(10));rec("G","trees",len(trees),106,0)
        for nm,t in RED.items():
            k=len(set(round(logr(T,*t),9) for T in trees));CMP["degk"][nm]=k
            rows.append(dict(section="G_degeneracy",item=nm,computed=k,manuscript="(all 12 exported)",ok=True))
        for nm,kexp in [("M1",18),("M2",35),("LO(0,0,1)",79),("LO(0,0,2)",79),("R",79),("GA",79),("AG",79)]:
            rec("G",f"deg_{nm}",CMP["degk"][nm],kexp,0)
        from collections import Counter
        prof=set(tuple(sorted(Counter(tuple(sorted((T.degree(u),T.degree(v)))) for u,v in T.edges()).items())) for T in trees)
        rec("G","BID_profile_floor",len(prof),79,0)
        v1=sorted(set(round(logr(T,0,0,1),12) for T in trees))
        gap=min(b-a for a,b in zip(v1,v1[1:]))
        rec("G","min_gap_LO001_trees",f"{gap:.2e}",">1e-9",0,ok=gap>1e-9)
        stab=all(len(set(round(logr(T,0,0,1),d) for T in trees))==79 for d in (6,8,10,12))
        rec("G","precision_stability_6to12dp",stab,True,0);P(f"    min gap {gap:.2e}; distinct-count stable 6-12dp: {stab}")
        dec=[T for T in trees if max(d for _,d in T.degree())<=4];rec("G","decanes",len(dec),75,0)
        for nm,t in RED.items():
            v=np.array([logr(T,*t) for T in dec])
            CMP["ss"][nm]=v.std(ddof=0)/v.mean();CMP["ab"][nm]=(v.max()-v.min())/v.mean()
            rows.append(dict(section="G_SS",item=nm,
                computed=f"SS={CMP['ss'][nm]:.5f},Abr={CMP['ab'][nm]:.5f},SA={CMP['ss'][nm]/CMP['ab'][nm]:.5f}",
                manuscript="(all 12 exported)",ok=True))
        rec("G","SS_LO002",round(CMP["ss"]["LO(0,0,2)"],3),0.165,0.0006)
        rec("G","LO002_max_SS",max(CMP["ss"],key=CMP["ss"].get),"LO(0,0,2)",0,ok=max(CMP["ss"],key=CMP["ss"].get)=="LO(0,0,2)")
        rec("G","LO002_max_Abr",max(CMP["ab"],key=CMP["ab"].get),"LO(0,0,2)",0,ok=max(CMP["ab"],key=CMP["ab"].get)=="LO(0,0,2)")
        P("  done")

        P("[G2] Furtula-Gutman-Dehmer SS/Abr on the 75 decanes, first principles (own AHU canonical forms)")
        CMP["FGD"]=fgd_first_principles(dec,RED)
        for nm in RED:
            ss_,ab_,ra_=CMP["FGD"][nm]
            rows.append(dict(section="G2_FGD",item=nm,computed=f"SS={ss_:.10f},Abr={ab_:.10f},ratio={ra_:.10f}",
                             manuscript="(guarded in [T])",ok=True))
        P("[G3] multi-order degeneracy n=7..12 (all trees / Delta<=4), first principles")
        CMP["MO"]=multiorder_first_principles(nx,logr)
        P("  done")

        P("[M] mathematics: 9 closed forms; 10 bounds x 200 graphs; equality; asymptotics")
        mrng=np.random.default_rng(5);mbad=0
        def psi(i,j,a,b,g):return (i*j)**a*(i+j)**b*math.exp(g*abs(i-j)/(i+j))
        for _ in range(5):
            a,b,g=mrng.uniform(-2,2,3);N=7
            F=nx.Graph()
            for tt in range(3):F.add_edges_from([(0,2*tt+1),(0,2*tt+2),(2*tt+1,2*tt+2)])
            pet=nx.petersen_graph()
            tests=[("K_n",logr(nx.complete_graph(N),a,b,g),(N*(N-1)/2)*2**b*(N-1)**(2*a+b)),
                   ("C_n",logr(nx.cycle_graph(N),a,b,g),N*4**(a+b)),
                   ("P_6",logr(nx.path_graph(6),a,b,g),2*2**a*3**b*math.exp(g/3)+3*4**(a+b)),
                   ("S_n",logr(nx.star_graph(N-1),a,b,g),(N-1)*(N-1)**a*N**b*math.exp(g*(N-2)/N)),
                   ("K_pq",logr(nx.complete_bipartite_graph(3,4),a,b,g),12*12**a*7**b*math.exp(g/7)),
                   ("Q_k",logr(nx.hypercube_graph(3),a,b,g),3*4*2**b*3**(2*a+b)),
                   ("W_n",logr(nx.wheel_graph(N),a,b,g),(N-1)*(3**a*(N-1)**a*(N+2)**b*math.exp(g*(N-4)/(N+2))+9**a*6**b)),
                   ("F_p",logr(F,a,b,g),3*4**(a+b)+6*12**a*8**b*math.exp(g/2)),
                   ("r-regular(Petersen)",logr(pet,a,b,g),15*2**b*3**(2*a+b))]
            for nm,got,exp in tests:
                if abs(got-exp)>1e-8:mbad+=1;P(f"    CLOSED-FORM FAIL {nm}")
        for _ in range(200):
            while True:
                G=nx.gnp_random_graph(int(mrng.integers(5,10)),float(mrng.uniform(.3,.7)),seed=int(mrng.integers(1e6)))
                if G.number_of_edges()>0 and nx.is_connected(G):break
            m=G.number_of_edges();degs=[d for _,d in G.degree()];dm,dx=min(degs),max(degs)
            a,b,g=mrng.uniform(-1.5,1.5,3);v=logr(G,a,b,g)
            Pr=[(i,j) for i in range(dm,dx+1) for j in range(i,dx+1)]
            if not(m*min(psi(i,j,a,b,g) for i,j in Pr)-1e-9<=v<=m*max(psi(i,j,a,b,g) for i,j in Pr)+1e-9):mbad+=1
            a1,b1,g1=mrng.uniform(-1.5,1.5,3)
            if v>math.sqrt(logr(G,a1,b1,g1)*logr(G,2*a-a1,2*b-b1,2*g-g1))+1e-9:mbad+=1
            an,bn,gn=abs(a),abs(b),abs(g)
            if logr(G,an,bn,gn)>m*dx**(2*an)*(2*dx)**bn*math.exp(gn*(dx-1)/(dx+1))+1e-9:mbad+=1
            if logr(G,an,bn,gn)<m*dm**(2*an)*(2*dm)**bn-1e-9:mbad+=1
            M1_=sum(d*d for d in degs);M2_=sum(G.degree(u)*G.degree(v) for u,v in G.edges())
            bb=float(mrng.uniform(1,3))
            if logr(G,0,bb,0)<m**(1-bb)*M1_**bb-1e-9:mbad+=1
            bb=float(mrng.uniform(.05,.95))
            if logr(G,0,bb,0)>m**(1-bb)*M1_**bb+1e-9:mbad+=1
            aa=float(mrng.uniform(1,3))
            if logr(G,aa,0,0)<m**(1-aa)*M2_**aa-1e-9:mbad+=1
            if logr(G,a,b,0)>math.sqrt(logr(G,2*a,0,0)*logr(G,0,2*b,0))+1e-9:mbad+=1
            SO=sum(math.sqrt(G.degree(u)**2+G.degree(v)**2) for u,v in G.edges())
            bb=float(mrng.uniform(.05,.95))
            if logr(G,0,bb,0)>m**(1-bb)*(math.sqrt(2)*SO)**bb+1e-9:mbad+=1
            prs=set(tuple(sorted((G.degree(u),G.degree(v)))) for u,v in G.edges())
            rt=[psi(i,j,a,b,g)/math.sqrt(i*i+j*j) for i,j in prs]
            if not(min(rt)*SO-1e-9<=v<=max(rt)*SO+1e-9):mbad+=1
        for _ in range(10):
            a,b,g=mrng.uniform(-1.5,1.5,3)
            if abs(logr(nx.cycle_graph(8),a,b,g)-8*psi(2,2,a,b,g))>1e-9:mbad+=1
            if abs(logr(nx.petersen_graph(),a,b,g)-15*psi(3,3,a,b,g))>1e-9:mbad+=1
        while True:
            G=nx.gnp_random_graph(8,.4,seed=77)
            if G.number_of_edges()>0 and nx.is_connected(G):break
        M=max(abs(G.degree(u)-G.degree(v))/(G.degree(u)+G.degree(v)) for u,v in G.edges())
        gam=200.0;lhs=logr(G,0.3,-0.4,gam)/math.exp(gam*M)
        rhs=sum((G.degree(u)*G.degree(v))**0.3*(G.degree(u)+G.degree(v))**-0.4 for u,v in G.edges()
                if abs(abs(G.degree(u)-G.degree(v))/(G.degree(u)+G.degree(v))-M)<1e-12)
        if abs(lhs-rhs)>1e-6:mbad+=1
        rec("M","closedforms+bounds+equality+asymptotics_failures",mbad,0,0)
        P(f"    math failures: {mbad}")
    return fails,rows,folds_out,CMP

# --------------------------------------------------------------------- selftest
def run_selftest(A, here, HAVE_NX):
    print("[SELFTEST] v35 adversarial attack matrix (isolated copies; canonical files untouched)")
    print("  computing reference values once...")
    fails,_,_,CMP=run_computation(HAVE_NX,quiet=True)
    if fails or not HAVE_NX:
        print(f"  cannot self-test: baseline computation fails={fails}, networkx={HAVE_NX}");return 1
    base=open(A.tex).read()
    results=[]  # (name, behaved_correctly, note)
    def line_with(*subs):
        for l in base.splitlines():
            if all(s in l for s in subs):return l
        raise KeyError(str(subs))
    def rep_line(line,old,new):
        assert old in line, (old,line)
        return base.replace(line,line.replace(old,new,1),1)
    CMP.update(load_v35_expectations(here))
    ok0,msgs0=check_tex(A.tex,CMP)
    okc,msgc=check_csvs(here,CMP)
    print(f"  positive control: tex pass={ok0}, csv pass={okc}")
    results.append(("positive-control-tex",ok0,"" if ok0 else (msgs0[0] if msgs0 else "")))
    results.append(("positive-control-csv",okc,"" if okc else (msgc[0] if msgc else "")))

    L_T2M1   = line_with("$M_1 = LO(0,1,0)$")
    L_T2M2   = line_with("$M_2 = LO(1,0,0)$")
    L_T2LAST = line_with("$LO(0,0,2)$ &")
    L_TUNLAST= line_with(r"$\omega$","$0.929$","$0.945$")
    L_TUN_S  = line_with("$S$","$0.931$","$0.948$")
    L_BF_TB  = line_with("$T_B$",r"${}^{m}\!M_2$","$0.855$")
    L_BF_OM  = line_with(r"$\omega$","$M_2$","$0.988$")
    L_ANCH_HM= line_with(r"near} $HM = LO(0,2,0)$")
    L_ABL_TB = line_with("$T_B$","$+0.613$")
    L_FGD_M1 = line_with("$M_1$ &","$0.0566$")
    L_MO_12M = line_with("$12$ & mol.")
    L_COLL_3MH=line_with("3-methylheptane &","$118.9$")
    L_ABL_OM = line_with(r"$\omega$","$+0.979$","$5/18$")
    L_ABL_DV = line_with(r"$\Delta H_{\mathrm{vap}}$","+0.069")
    L_FGD_HM = line_with("$HM$ &","$0.1256$")
    L_APP_33 = line_with("3,3-dimethylhexane & 111.9")
    L_APP_32 = line_with("3-ethyl-2-methylpentane & 115.6 &")
    def wrap_outside(b):
        i=b.index(r"\label{tab:lo_octane}");j=b.index(r"\end{tabular}",i)+len(r"\end{tabular}")
        return b[:i]+"\\iffalse\n"+b[i:j]+"\n\\fi"+b[j:]
    def catcode_attack(b,row):
        i=b.index(r"\label{tab:lo_octane}")
        b=b[:i]+"\\catcode33=14\n"+b[i:]
        b=b.replace(row,"!"+row,1)
        k=b.index(r"\end{tabular}",b.index(r"\label{tab:lo_octane}"))+len(r"\end{tabular}")
        return b[:k]+"\n\\catcode33=12"+b[k:]
    tex_attacks=[
     ("t2-first-sign-flip",     rep_line(L_T2M1,"$-0.718$","$+0.718$"),          "tab:lo_octane M1/T_B"),
     ("t2-last-row-value",      rep_line(L_T2LAST,"$-0.925$","$-0.825$"),        "LO(0,0,2)/omega"),
     ("t2-fourth-decimal",      rep_line(L_T2M1,"$-0.718$","$-0.7189$"),         "token"),
     ("t2-nan-token",           rep_line(L_T2M1,"$-0.718$","$nan$"),             "token"),
     ("t2-missing-row",         base.replace(L_T2M1+"\n","",1),                  "12 data rows"),
     ("t2-duplicated-row",      base.replace(L_T2M1,L_T2M1+"\n"+L_T2M1,1),       "12 data rows"),
     ("t2-extra-row",           base.replace(L_T2M1,L_T2M1+"\n"+r"$ZZ = LO(9,9,9)$ & $+0.100$ & $+0.100$ & $+0.100$ & $+0.100$ & $+0.100$\\",1),"12 data rows"),
     ("t2-swap-rows",           base.replace(L_T2M1,"@@X@@",1).replace(L_T2M2,L_T2M1,1).replace("@@X@@",L_T2M2,1),"label mismatch"),
     ("t2-wrong-label",         rep_line(L_T2M1,"$M_1 = LO(0,1,0)$","$M_9 = LO(0,1,0)$"),"label mismatch"),
     ("t2-bold-removed",        base.replace(r"$\mathbf{+0.855}$","$+0.855$",1),  "bolding mismatch"),
     ("t2-bold-added",          rep_line(L_T2M1,"$-0.718$",r"$\mathbf{-0.718}$"), "bolding mismatch"),
     ("tuning-col-r0",          rep_line(L_TUNLAST,"$0.929$","$0.919$"),         "LO(0,0,1)/omega/r0"),
     ("tuning-col-r50",         rep_line(L_TUNLAST,"$0.945$","$0.935$"),         "LO(0,0,1)/omega/r50"),
     ("tuning-col-gain-in",     rep_line(L_TUNLAST,"$+0.016$","$+0.116$"),       "LO(0,0,1)/omega/gain_in"),
     ("tuning-col-boot",        rep_line(L_TUNLAST,"$0.074$","$0.174$"),         "LO(0,0,1)/omega/boot"),
     ("tuning-col-LOO0",        rep_line(L_TUNLAST,"$0.907$","$0.807$"),         "LO(0,0,1)/omega/LOO0"),
     ("tuning-col-LOO50",       rep_line(L_TUNLAST,"$0.926$","$0.826$"),         "LO(0,0,1)/omega/LOO50"),
     ("tuning-col-gain-LOO",    rep_line(L_TUNLAST,"$+0.019$","$+0.119$"),       "LO(0,0,1)/omega/gain_LOO"),
     ("tuning-sign-flip",       rep_line(L_TUNLAST,"$+0.019$","$-0.019$"),       "LO(0,0,1)/omega/gain_LOO"),
     ("tuning-wrong-property",  rep_line(L_TUNLAST,r"$\omega$",r"$\Omega$"),     "property label"),
     ("tuning-wrong-anchor",    base.replace(r"near} $HM = LO(0,2,0)$",r"near} $H\Sigma = LO(0,2,0)$",1),"anchor label"),
     ("tuning-missing-row",     base.replace(L_TUNLAST+"\n","",1),               "row"),
     ("tuning-duplicated-row",  base.replace(L_TUNLAST,L_TUNLAST+"\n"+L_TUNLAST,1),"row"),
     ("tuning-swap-rows",       base.replace(L_TUN_S,"@@X@@",1).replace(L_TUNLAST,L_TUN_S,1).replace("@@X@@",L_TUNLAST,1),"property label"),
     ("tuning-junk-token",      rep_line(L_TUNLAST,"$0.929$","$0.929e0$"),       "token"),
     ("bestfixed-val-fix-r",    rep_line(L_BF_TB,"$0.855$","$0.755$"),           "bestfixed T_B/fix_r"),
     ("bestfixed-val-fix-LOO",  rep_line(L_BF_TB,"$0.781$","$0.681$"),           "bestfixed T_B/fix_LOO"),
     ("bestfixed-val-dec-r",    rep_line(L_BF_OM,"$0.945$","$0.845$"),           "bestfixed omega/dec_r"),
     ("bestfixed-val-dec-LOO",  rep_line(L_BF_OM,"$0.926$","$0.826$"),           "bestfixed omega/dec_LOO"),
     ("bestfixed-inserted-minus",rep_line(L_BF_OM,"$0.926$","$-0.926$"),         "token"),
     ("bestfixed-v35-reseeded-pool",rep_line(L_BF_TB,"$0.835$","$0.834$"),       "bestfixed T_B/dec_r"),
     ("bestfixed-over-precision",rep_line(L_BF_TB,"$0.855$","$0.8555$"),         "token"),
     ("bestfixed-wrong-labels", rep_line(L_BF_OM,r"$\omega$ & $M_2$",r"$\Omega$ & $HM$"),"label mismatch"),
     ("bestfixed-missing-row",  base.replace(L_BF_TB+"\n","",1),                 "5 data rows"),
     ("bestfixed-duplicated-row",base.replace(L_BF_TB,L_BF_TB+"\n"+L_BF_TB,1),   "5 data rows"),
     ("bestfixed-swap-rows",    base.replace(L_BF_TB,"@@X@@",1).replace(L_BF_OM,L_BF_TB,1).replace("@@X@@",L_BF_OM,1),"label mismatch"),
     ("t2-comment-row",         base.replace(L_T2M1,"%"+L_T2M1,1),               "12 data rows"),
     ("tuning-comment-row",     base.replace(L_TUNLAST,"%"+L_TUNLAST,1),         "row"),
     ("bestfixed-comment-row",  base.replace(L_BF_TB,"%"+L_BF_TB,1),             "5 data rows"),
     ("tuning-comment-anchor",  base.replace(L_ANCH_HM,"%"+L_ANCH_HM,1),         "anchor"),
     ("t2-comment-label",       base.replace(r"\label{tab:lo_octane}","%"+"\\label{tab:lo_octane}",1),"not found"),
     ("t2-iffalse-row",         base.replace(L_T2M1,"\\iffalse\n"+L_T2M1+"\n\\fi",1),"conditional"),
     ("t2-iffalse-outside-slice",wrap_outside(base),                             "conditional"),
     ("t2-catcode-comment",     catcode_attack(base,L_T2M1),                     "catcode"),
     ("t2-bang-prefix-row",     base.replace(L_T2M1,"!"+L_T2M1,1),               "label mismatch"),
     ("ablation-q2-corrupt",    rep_line(L_ABL_TB,"$+0.613$","$+0.713$"),        "tab:ablation"),
     ("ablation-folds-corrupt", rep_line(L_ABL_TB,"$10/18$","$15/18$"),          "LO-better"),
     ("fgdss-value-corrupt",    rep_line(L_FGD_M1,"$0.0566$","$0.0666$"),        "tab:fgdss"),
     ("multiorder-floor-corrupt",rep_line(L_MO_12M,"$137$","$138$",),            "tab:multiorder"),
     ("collision-value-corrupt",rep_line(L_COLL_3MH,"$118.9$","$119.9$"),        "tab:collisions"),
     ("t2-one-unit-display",    base.replace(r"$\mathbf{-0.984}$",r"$\mathbf{-0.983}$",1),"tab:lo_octane LO(0,0,1)/dHvap"),
     ("t2-v35-dhvap-winner",    base.replace(r"$\mathbf{-0.984}$","$-0.984$",1).replace("$-0.981$",r"$\mathbf{-0.981}$",1),"bolding mismatch"),
     ("tuning-one-unit",        rep_line(L_TUNLAST,"$0.929$","$0.930$"),         "LO(0,0,1)/omega/r0"),
     ("ablation-one-unit-dQ2",  rep_line(L_ABL_TB,"$+0.136$","$+0.135$"),        "tab:ablation T_B/dQ2"),
     ("ablation-one-unit-rmse", rep_line(L_ABL_OM,"$0.008$","$0.007$"),          "tab:ablation omega/RMSE_LO"),
     ("ablation-one-unit-q2",   rep_line(L_ABL_OM,"$+0.956$","$+0.957$"),        "tab:ablation omega/Q2_LO"),
     ("ablation-median-corrupt",rep_line(L_ABL_DV,"+0.069","+0.070"),            "100-seed median"),
     ("ablation-seedcount-v35", rep_line(L_ABL_DV,"$100/100$ & $100/100$","$91/100$ & $100/100$"),"seeds with dQ2>0 at budget 200"),
     ("ablation-panelb-missing",base.replace(L_ABL_DV+"\n","",1),               "panel (b): expected 5 data rows"),
     ("fgdss-one-unit",         rep_line(L_FGD_HM,"$0.1256$","$0.1255$"),        "tab:fgdss HM/SS"),
     ("appendix-dhvap-revert",  rep_line(L_APP_33,"& 8.97 &","& 9.04 &"),        "tab:octane-data 3,3-dimethylhexane/dHvap"),
     ("appendix-name-revert",   rep_line(L_APP_32,"3-ethyl-2-methylpentane","2-methyl-3-ethylpentane"),"tab:octane-data row 10: name"),
     ("appendix-missing-row",   base.replace(L_APP_33+"\n","",1),                 "tab:octane-data: expected 18 rows"),
    ]
    with tempfile.TemporaryDirectory() as td:
        for name,content,expect in tex_attacks:
            try:
                fp=os.path.join(td,"c.tex");open(fp,"w").write(content)
                okx,msgs=check_tex(fp,CMP)
                joined="\n".join(msgs)
                behaved=(not okx) and (expect in joined)
                note="" if behaved else (("PASSED (false negative)" if okx else f"wrong diagnostic; first: {msgs[0][:80]}"))
                results.append((f"tex:{name}",behaved,note))
            except Exception as e:
                results.append((f"tex:{name}",False,f"attack-harness exception: {e!r}"))
        results.append(("tex:missing-file",check_tex(os.path.join(td,"absent.tex"),CMP)[0]==False,""))
    # CSV attacks
    def csv_attack(name, fn, mutate, expect):
        try:
            with tempfile.TemporaryDirectory() as td2:
                for f in (CSV_PRED,CSV_DEG,CSV_SS):
                    shutil.copy(os.path.join(here,f),td2)
                if mutate is not None:
                    p=os.path.join(td2,fn);s=open(p,newline="").read();s2=mutate(s)
                    assert s2!=s, "mutation had no effect"
                    open(p,"w",newline="").write(s2)
                else:
                    os.remove(os.path.join(td2,fn))
                okx,msgs=check_csvs(td2,CMP)
                joined="\n".join(msgs)
                behaved=(not okx) and (expect in joined)
                note="" if behaved else (("PASSED (false negative)" if okx else f"wrong diagnostic; first: {msgs[0][:80]}"))
                results.append((f"csv:{name}",behaved,note))
        except Exception as e:
            results.append((f"csv:{name}",False,f"attack-harness exception: {e!r}"))
    csv_attack("pred-value",CSV_PRED,lambda s:s.replace("-0.7180987560","-0.7180987561",1),CSV_PRED)
    csv_attack("pred-4dp-truncation",CSV_PRED,lambda s:s.replace("-0.7180987560","-0.7181",1),CSV_PRED)
    csv_attack("pred-star-removed",CSV_PRED,lambda s:s.replace("-0.9876015088*","-0.9876015088",1),CSV_PRED)
    csv_attack("pred-bestin-wrong",CSV_PRED,lambda s:s.replace("-0.9876015088*,omega","-0.9876015088*,S",1),CSV_PRED)
    csv_attack("pred-dhvap-star-moved",CSV_PRED,lambda s:s.replace("-0.9838407051*","-0.9838407051",1).replace("-0.9812526655,","-0.9812526655*,",1),CSV_PRED)
    csv_attack("pred-duplicated-row",CSV_PRED,lambda s:s.replace("M1,-0.7180987560","M1,-0.7180987560,-0.7623221006,-0.9353729341,-0.9729602386,-0.9702085527,\r\nM1,-0.7180987560",1),"rows")
    csv_attack("pred-deleted-row",CSV_PRED,lambda s:re.sub(r"M1,[^\r\n]*\r?\n","",s,count=1),"rows")
    csv_attack("pred-extra-row",CSV_PRED,lambda s:s+"ZZ,+0.1000,+0.1000,+0.1000,+0.1000,+0.1000,\r\n","rows")
    csv_attack("pred-reordered-rows",CSV_PRED,lambda s:s.replace("M1,-0.7180987560","@@",1).replace("M2,-0.4972511299","M1,-0.7180987560",1).replace("@@","M2,-0.4972511299",1),"index key")
    csv_attack("pred-renamed-key",CSV_PRED,lambda s:s.replace("M1,","MX,",1),"index key")
    csv_attack("deg-N-trees",CSV_DEG,lambda s:s.replace("M1,106,18","M1,105,18",1),CSV_DEG)
    csv_attack("deg-distinct",CSV_DEG,lambda s:s.replace("M1,106,18","M1,106,19",1),CSV_DEG)
    csv_attack("deg-pct",CSV_DEG,lambda s:s.replace("83.02","99.99",1),CSV_DEG)
    csv_attack("deg-deleted-row",CSV_DEG,lambda s:re.sub(r"M1,[^\r\n]*\r?\n","",s,count=1),"rows")
    csv_attack("deg-header-renamed",CSV_DEG,lambda s:s.replace("degeneracy_pct","deg_pct",1),"header")
    csv_attack("deg-column-deleted",CSV_DEG,lambda s:"\r\n".join(",".join(l.split(",")[:-1]) for l in s.splitlines())+"\r\n","header")
    csv_attack("ss-SS-cell",CSV_SS,lambda s:s.replace("0.0750272923,","0.0750272924,",1),CSV_SS)
    csv_attack("ss-Abr-cell",CSV_SS,lambda s:s.replace("0.3444881890","0.3444881891",1),CSV_SS)
    csv_attack("ss-SA-cell",CSV_SS,lambda s:s.replace("0.2177935114","0.9999999999",1),CSV_SS)
    csv_attack("ss-blank-cell",CSV_SS,lambda s:s.replace("0.2177935114","",1),CSV_SS)
    csv_attack("ss-inf-cell",CSV_SS,lambda s:s.replace("0.2177935114","inf",1),CSV_SS)
    csv_attack("ss-over-precision",CSV_SS,lambda s:s.replace("0.0750272923,","0.07502729230,",1),CSV_SS)
    csv_attack("ss-5dp-truncation",CSV_SS,lambda s:s.replace("0.0750272923,","0.07503,",1),CSV_SS)
    csv_attack("ss-reordered-rows",CSV_SS,lambda s:s.replace("M1,0.0750272923","@@",1).replace("M2,0.1098330069","M1,0.0750272923",1).replace("@@","M2,0.1098330069",1),"index key")
    csv_attack("pred-file-missing",CSV_PRED,None,"missing")
    def extras_attack(name,fn,mutate,expect):
        try:
            with tempfile.TemporaryDirectory() as td2:
                for f in (CSV_FGD,CSV_CTRL,CSV_ROB,CSV_ABL,CSV_PROV,CSV_EXPR,CSV_EXPS,CSV_OMEG,CSV_SSEN,"main.tex"):
                    shutil.copy(os.path.join(here,f),td2)
                p=os.path.join(td2,fn);t=open(p,newline="").read();t2=mutate(t)
                assert t2!=t
                open(p,"w",newline="").write(t2)
                okx,msgs=check_v35_extras(td2)
                joined="\n".join(msgs)
                behaved=(not okx) and (expect in joined)
                results.append((f"csv:{name}",behaved,"" if behaved else (msgs[0][:80] if msgs else "PASSED (false negative)")))
        except Exception as e:
            results.append((f"csv:{name}",False,f"attack-harness exception: {e!r}"))
    extras_attack("fgd-control-corrupt",CSV_CTRL,lambda t:t.replace("0.0566","0.0567",1),CSV_CTRL)
    extras_attack("robustness-corrupt",CSV_ROB,lambda t:t.replace("+0.0864474634","+0.0874474634",1),CSV_ROB)
    extras_attack("fgd-control-class-corrupt",CSV_CTRL,lambda t:t.replace("within_1_unit_4th_dp","exact_at_4dp",1),"agreement")
    extras_attack("entropy-sensitivity-corrupt",CSV_SSEN,lambda t:t.replace("-0.9541284205","-0.9551284205",1),CSV_SSEN)
    def prov_line(t,mol,prop,f):
        L=t.split("\r\n")
        for k,l in enumerate(L):
            fl=next(csv.reader([l])) if l else []
            if len(fl)>1 and fl[0]==mol and fl[1]==prop:
                L[k]=f(l);return "\r\n".join(L)
        raise KeyError((mol,prop))
    extras_attack("prov-dhvap-revert-to-v35-value",CSV_PROV,lambda t:prov_line(t,"3,3-dimethylhexane","dHvap",lambda l:l.replace(",8.97,",",9.04,",1)),"octane_data value")
    extras_attack("prov-dhvap-0.05-gap-as-tolerance",CSV_PROV,lambda t:prov_line(t,"3-ethyl-3-methylpentane","dHvap",
        lambda l:l.replace("9.08-9.10 kcal/mol","9.13 kcal/mol",1).replace("VERIFIED AFTER UNIT CONVERSION","AGREEMENT WITHIN TOLERANCE",1)),"rule says ['CONFLICT']")
    extras_attack("prov-reverify-234TMP-S",CSV_PROV,lambda t:prov_line(t,"2,3,4-trimethylpentane","S",lambda l:l.replace("AGREEMENT WITHIN TOLERANCE","VERIFIED AFTER UNIT CONVERSION",1)),"2,3,4-trimethylpentane/S: class")
    extras_attack("prov-reverify-34DMH-omega",CSV_PROV,lambda t:prov_line(t,"3,4-dimethylhexane","omega",lambda l:l.replace("AGREEMENT WITHIN TOLERANCE","VERIFIED AFTER UNIT CONVERSION",1)),"3,4-dimethylhexane/omega: class")
    def extras_attack2(name,mutate,expect):
        try:
            with tempfile.TemporaryDirectory() as td2:
                for f in (CSV_FGD,CSV_CTRL,CSV_ROB,CSV_ABL,CSV_PROV,CSV_EXPR,CSV_EXPS,CSV_OMEG,CSV_SSEN,"main.tex"):
                    shutil.copy(os.path.join(here,f),td2)
                p=os.path.join(td2,CSV_PROV);t=open(p,newline="").read();t2=mutate(t)
                assert t2!=t
                open(p,"w",newline="").write(t2)
                okx,msgs=check_v35_extras(td2)
                joined="\n".join(msgs)
                behaved=(not okx) and (expect in joined)
                results.append((f"csv:{name}",behaved,"" if behaved else (msgs[0][:80] if msgs else "PASSED (false negative)")))
        except Exception as e:
            results.append((f"csv:{name}",False,f"attack-harness exception: {e!r}"))
    extras_attack2("provenance-class-corrupt",lambda t:t.replace("CONFLICT","VERIFIED EXACT",1),CSV_PROV)
    extras_attack("expanded-robustness-corrupt",CSV_EXPR,lambda t:t.replace("0.6780862951,-0.0278575844","0.6780862951,-0.0378575844",1),CSV_EXPR)
    extras_attack("expanded-sign-flip",CSV_EXPR,lambda t:re.sub(r"(\n\d+,200,dHvap,[0-9.]+,)([0-9.]+),\+([0-9.]+)",lambda m:m.group(1)+m.group(2)+",-"+m.group(3),t,count=1),CSV_EXPR)
    extras_attack("omega-sensitivity-corrupt",CSV_OMEG,lambda t:t.replace("-0.9856641032","-0.9956641032",1),CSV_OMEG)
    extras_attack("provenance-value-inconsistent",CSV_PROV,lambda t:t.replace("AGREEMENT WITHIN TOLERANCE","VERIFIED AFTER UNIT CONVERSION",1),CSV_PROV)
    extras_attack("proxy-figure-reintroduced","main.tex",lambda t:t.replace("\\end{document}","\\safefig{fig_lo_structure_sensitivity_decanes_v3.pdf}{0.9}\n\\end{document}",1),"retired sigma/mu proxy")
    # operational subprocess attacks (isolated package copies)
    script=os.path.abspath(__file__)
    def make_pkg(td, skip=None):
        pkg=os.path.join(td,"pkg");os.makedirs(pkg)
        files=["main.tex",CSV_PRED,CSV_DEG,CSV_SS,CSV_ABL,CSV_ABLF,CSV_MO,CSV_FGD,
               CSV_COLL,CSV_CORR,CSV_PCA,CSV_ROB,CSV_CTRL,CSV_PROV,CSV_EXPR,CSV_EXPS,CSV_OMEG,CSV_SSEN,"octane_data.py"]+list(ANALYSIS_SCRIPTS)
        for f in files:
            if f!=skip:shutil.copy(os.path.join(here,f),pkg)
        shutil.copy(script,os.path.join(pkg,os.path.basename(script)))
        # v36.1: figure generator + figures/ are part of the verified package
        shutil.copy(os.path.join(here,"generate_loyola_v35_figures.py"),pkg)
        shutil.copytree(os.path.join(here,"figures"),os.path.join(pkg,"figures"))
        return pkg
    def run_pkg(pkg,args=None,cwd=None,env_extra=None):
        env=dict(os.environ)
        if env_extra:env.update(env_extra)
        return subprocess.run([sys.executable,os.path.join(pkg,os.path.basename(script))]+(args or []),
                              cwd=cwd or pkg,capture_output=True,text=True,timeout=900,env=env)
    ops=[]
    with tempfile.TemporaryDirectory() as td:
        r=run_pkg(make_pkg(td))
        ops.append(("op:package-root",r.returncode==0 and "status: FULL PASS" in r.stdout,f"exit={r.returncode}"))
    with tempfile.TemporaryDirectory() as td:
        pkg=make_pkg(td);fp=os.path.join(pkg,"figures","fig_lo_prediction_correlation_heatmap_v3.pdf")
        open(fp,"ab").write(b"%stale\n")
        r=run_pkg(pkg)
        ops.append(("op:stale-figure",r.returncode==1 and "stale figure" in r.stdout,f"exit={r.returncode}"))
    with tempfile.TemporaryDirectory() as td:
        pkg=make_pkg(td);other=os.path.join(td,"elsewhere");os.makedirs(other)
        r=run_pkg(pkg,args=["--skip-analyses"],cwd=other)
        ops.append(("op:outside-cwd",r.returncode==2 and "TOTAL failures: 0" in r.stdout,f"exit={r.returncode}"))  # --skip-analyses => PARTIAL
    with tempfile.TemporaryDirectory() as td:
        pkg=make_pkg(td);nested=os.path.join(td,"new","nested","outdir")
        r=run_pkg(pkg,args=["--skip-analyses","--output-dir",nested])
        made=os.path.exists(os.path.join(nested,"verify_loyola_v35_results.csv"))
        ops.append(("op:new-nested-output-dir",r.returncode==2 and made,f"exit={r.returncode} created={made}"))
    with tempfile.TemporaryDirectory() as td:
        pkg=make_pkg(td);ro=os.path.join(td,"ro");os.makedirs(ro);os.chmod(ro,0o500)
        r=run_pkg(pkg,args=["--skip-analyses","--output-dir",os.path.join(ro,"sub")])
        controlled=(r.returncode==2 and "CANNOT WRITE OUTPUT" in r.stdout and "Traceback" not in r.stderr)
        os.chmod(ro,0o700)
        ops.append(("op:unwritable-output",controlled,f"exit={r.returncode}"))
    with tempfile.TemporaryDirectory() as td:
        pkg=make_pkg(td);shim=os.path.join(td,"shim");os.makedirs(shim)
        open(os.path.join(shim,"networkx.py"),"w").write("raise ImportError('selftest shim: networkx blocked')\n")
        r=run_pkg(pkg,args=["--skip-analyses"],env_extra={"PYTHONPATH":shim})
        ok_nx=(r.returncode==2 and "networkx" in r.stdout and "status: FULL PASS" not in r.stdout)
        ops.append(("op:missing-networkx",ok_nx,f"exit={r.returncode}"))
    with tempfile.TemporaryDirectory() as td:
        pkg=make_pkg(td,skip=CSV_PRED)
        r=run_pkg(pkg)
        ok_ma=(r.returncode==2 and "status: FULL PASS" not in r.stdout and "missing" in r.stdout.lower())
        ops.append(("op:missing-artifact",ok_ma,f"exit={r.returncode}"))
    results.extend(ops)
    bad=[(n,note) for n,b,note in results if not b]
    for n,b,note in results:
        print(f"  {'PASS' if b else 'FAIL'}  {n}{('  <- '+note) if note and not b else ''}")
    ntex=sum(1 for n,_,_ in results if n.startswith("tex:"))
    ncsv=sum(1 for n,_,_ in results if n.startswith("csv:"))
    nop=sum(1 for n,_,_ in results if n.startswith("op:"))
    print(f"[SELFTEST] {len(results)} tests ({ntex} tex attacks, {ncsv} csv attacks, {nop} operational, 2 positive controls)")
    print(f"[SELFTEST] {'ALL ATTACKS REJECTED FOR THE INTENDED REASON' if not bad else f'{len(bad)} MISBEHAVING TESTS'}")
    return 0 if not bad else 1

# ------------------------------------------------------------------------ main
def main():
    ap=argparse.ArgumentParser(description="LOYOLA v35 unified verifier")
    ap.add_argument("--output-dir",default=os.path.dirname(os.path.abspath(__file__)))
    ap.add_argument("--tex",default=os.path.join(os.path.dirname(os.path.abspath(__file__)),"main.tex"))
    ap.add_argument("--allow-skip",action="store_true",help="allow partial run without networkx (exit 2)")
    ap.add_argument("--selftest",action="store_true",help="run the adversarial attack matrix and exit")
    ap.add_argument("--skip-analyses",action="store_true",help="skip the [N] analysis re-run (used by the operational selftest for runtime; the drift guard still validates all tables against the bundled canonical CSVs)")
    A=ap.parse_args()
    here=os.path.dirname(os.path.abspath(__file__))
    REQUIRED=[A.tex]+[os.path.join(here,f) for f in (CSV_PRED,CSV_DEG,CSV_SS,
        CSV_ABL,CSV_ABLF,CSV_MO,CSV_FGD,CSV_COLL,CSV_CORR,CSV_PCA,CSV_ROB,CSV_CTRL,CSV_PROV,CSV_EXPR,CSV_EXPS,CSV_OMEG,CSV_SSEN,"octane_data.py")]+\
        [os.path.join(here,sc) for sc in ANALYSIS_SCRIPTS]
    missing=[f for f in REQUIRED if not os.path.exists(f)]
    try:
        import networkx;HAVE_NX=True
    except Exception:
        HAVE_NX=False
    if A.selftest:
        if missing:
            print("SELFTEST cannot run: missing required artifact(s):");[print("  -",f) for f in missing];return 2
        return run_selftest(A,here,HAVE_NX)
    if missing:
        print("PARTIAL - CANNOT VERIFY: required artifact(s) missing:")
        for f in missing:print("  -",f)
        print("status: PARTIAL (exit 2); full pass is not attainable without required artifacts.")
        return 2
    if not HAVE_NX and not A.allow_skip:
        print("FATAL: networkx required for sections G/M (install it, or pass --allow-skip for a PARTIAL run).")
        return 2
    fails,rows,folds_out,CMP=run_computation(HAVE_NX)
    if A.skip_analyses:
        print("[N] v35 analyses: SKIPPED (--skip-analyses); tables validated against bundled canonical CSVs only")
        okN,msgsN=True,[]
    else:
        print(f"[N] analyses: fresh re-run of the {len(ANALYSIS_SCRIPTS)} bundled analysis scripts vs canonical CSVs")
        okN,msgsN=run_v35_analyses(here)
    if not okN:fails+=len(msgsN)
    rows.append(dict(section="N",item="v35_analyses_recompute",computed=f"{len(msgsN)} mismatches",manuscript="0",ok=okN))
    for msg in msgsN[:10]:print("    ",msg)
    print(f"    analysis recompute: {'PASS' if okN else 'FAIL'} ({len(msgsN)} diagnostics)")
    print("[P] SMILES-parser sanity (alkane-only parser; 18 structures)")
    okP,msgsP=check_parser_sanity(HAVE_NX)
    if not okP:fails+=len(msgsP)
    rows.append(dict(section="P",item="parser_sanity",computed=f"{len(msgsP)} issues",manuscript="0",ok=okP))
    for msg in msgsP[:6]:print("    ",msg)
    print(f"    parser sanity: {'PASS' if okP else 'FAIL'}")
    print("[N2] FGD published control (Barman-Das Table 10) + ablation robustness consistency")
    okX,msgsX=check_v35_extras(here)
    if not okX:fails+=len(msgsX)
    rows.append(dict(section="N2",item="fgd_control+robustness",computed=f"{len(msgsX)} issues",manuscript="0",ok=okX))
    for msg in msgsX[:8]:print("    ",msg)
    print(f"    v35 extras: {'PASS' if okX else 'FAIL'}")
    CMP.update(load_v35_expectations(here))
    print("[T] drift guard: complete-token, label-validated, COMPUTATION-DERIVED parse of main.tex tables")
    okT,msgs=check_tex(A.tex,CMP)
    if not okT:fails+=len(msgs)
    rows.append(dict(section="T",item="main_tex_tables",computed=f"{len(msgs)} mismatches",manuscript="0",ok=okT))
    for msg in msgs[:12]:print("    ",msg)
    print(f"    tex table check: {'PASS' if okT else 'FAIL'} ({len(msgs)} diagnostics)")
    if HAVE_NX:
        print("[T2] canonical figure-data CSVs: schema + exact-cell + byte comparison vs computation")
        okC,msgsC=check_csvs(here,CMP)
        if not okC:fails+=len(msgsC)
        rows.append(dict(section="T2",item="canonical_csvs",computed=f"{len(msgsC)} mismatches",manuscript="0",ok=okC))
        for msg in msgsC[:12]:print("    ",msg)
        print(f"    canonical CSV check: {'PASS' if okC else 'FAIL'} ({len(msgsC)} diagnostics)")
    io_fail=False
    try:
        os.makedirs(A.output_dir,exist_ok=True)
        out=os.path.join(A.output_dir,"verify_loyola_v35_results.csv")
        with open(out,"w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=["section","item","computed","manuscript","ok"]);w.writeheader()
            for r in rows:w.writerow(r)
        with open(os.path.join(A.output_dir,"verify_loyola_v35_folds.csv"),"w",newline="") as f:
            w=csv.DictWriter(f,fieldnames=["anchor","prop","heldout","triple","pred","actual"]);w.writeheader()
            for r in folds_out:w.writerow(r)
    except OSError as e:
        io_fail=True;out="(not written)"
        print(f"CANNOT WRITE OUTPUT to {A.output_dir}: {e} -- results not persisted (controlled diagnostic).")
    import platform,numpy,scipy
    nxv="absent"
    if HAVE_NX:
        import networkx;nxv=networkx.__version__
    print(f"\nENV: Python {platform.python_version()}, NumPy {numpy.__version__}, SciPy {scipy.__version__}, networkx {nxv}, {platform.system()} {platform.release()}")
    print(f"undefined (zero-variance) bootstrap resamples encountered: {UNDEF_RESAMPLES}")
    if fails>0:status=1
    elif io_fail or not HAVE_NX or A.skip_analyses:status=2  # skipped [N] => canonical CSVs unverified
    else:status=0
    print(f"TOTAL failures: {fails}  status: {'FULL PASS' if status==0 else ('PARTIAL' if status==2 else 'FAILURES')}")
    print("scope: FULL PASS covers the executed computations, all 8 numeric tables of main.tex (exact display strings), and canonical artifacts;")
    print("       prose outside the guarded tables and verifier self-integrity are OUT OF SCOPE (see README/SHA256SUMS.txt).")
    print(f"results: {out} (+ verify_loyola_v35_folds.csv)")
    return status

if __name__=="__main__":
    sys.exit(main())
