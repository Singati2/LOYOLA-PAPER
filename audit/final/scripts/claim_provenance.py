#!/usr/bin/env python3
"""Source-independence ledger for every experimental value used in the paper (v40.30).

The provenance files say whether a value AGREES with a source. This script asks a different
question: how many INDEPENDENT primary determinations stand behind the value? Agreement with a
compilation (NBS Circular 461 / API-44 1947, Reid 1972, Wilhoit-Zwolinski 1971, Majer-Svoboda 1985,
Stephenson-Malanowski 1987, KDB, a compiled octane dataset) is derivative: those works reproduce
earlier measurements, so they never count as a second confirmation.

Tiers (strongest first):
  A  INDEPENDENT    two or more primary determinations behind the value (named primary papers from
                    different groups, or the median of two or more non-compilation determinations;
                    a NIST/TRC average that reports two or more determinations counts here, but its
                    constituent papers are not archived, so A-AGG marks it separately)
  B  SINGLE         one identifiable primary determination; any other agreeing source is derivative
  C  DERIVATIVE     only compilations or aggregates with no identifiable primary determination
  D  UNVERIFIED     no source matches (CANNOT VERIFY / CONFLICT), or the reference state is unresolved

Inputs: octane_property_provenance_v35.csv, external/nonane_provenance.csv, external/bp/bp_provenance.csv.
Output: claim_provenance_ledger.csv and claim_provenance_out.txt next to this script.
  cd audit/final/scripts && python3 claim_provenance.py
"""
import collections, csv, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
PRIMARY = {  # primary experimental groups named in the octane provenance (label -> pattern)
    "Prosen & Rossini 1945": r"Prosen", "Good 1972": r"Good 19", "Osborne & Ginnings 1947": r"Osborne",
    "Messerly 1971": r"Messerly", "Pitzer 1941": r"Pitzer", "McMicking & Kay 1965": r"McMicking"}
DERIVED = {"API-44 1947 (NBS Circ. 461)": r"API|C461|Circular 461", "Majer & Svoboda 1985": r"Majer",
           "Reid 1972": r"Reid", "Stephenson & Malanowski 1987": r"Stephenson", "KDB": r"KDB",
           "Daubert 1996": r"Daubert", "compiled octane dataset": r"compiled|TRC-derived|moleculardescriptors|Mondal|arXiv"}
COMPILATION_AUTHORS = r"Reid|Majer|Weast|Labbauf|Labauf|Wilhoit|Daubert|Stephenson|Dreisbach|Rossini, F\.D\.|Lange|CRC|Timmermans|API"


def count_avg(text):
    m = re.search(r"(?:avg|average|AVG)\s*of\s*(\d+)(?:\s*(?:/|of)\s*(\d+))?", text)
    return int(m.group(1)) if m else None


def octane_rows():
    out = []
    for r in csv.DictReader(open(os.path.join(ROOT, "octane_property_provenance_v35.csv"), newline="")):
        txt = " ".join((r["source_value"], r["source"], r["note"]))
        prim = [k for k, p in PRIMARY.items() if re.search(p, txt)]
        der = [k for k, p in DERIVED.items() if re.search(p, txt)]
        n_avg = count_avg(r["source_value"] + " " + r["source"])
        cls, prop = r["classification"], r["property"]
        if cls in ("CANNOT VERIFY", "CONFLICT"):
            tier, why = "D", cls.lower()
        elif prop == "omega":
            tier, why = "C", "acentric factors appear only in compilations (KDB; a compiled octane dataset); their original determination is not identified"
        elif len(prim) >= 2:
            tier, why = "A", "independent primary determinations: " + ", ".join(prim)
        elif n_avg and n_avg >= 2:
            tier, why = "A-AGG", f"NIST/TRC average of {n_avg} determinations (constituent papers not archived)"
        elif len(prim) == 1:
            tier, why = "B", "single primary determination: " + prim[0]
        elif re.search(r"NIST", txt) and not any(re.search(DERIVED[k], r["source_value"]) for k in DERIVED):
            tier, why = "B?", "one NIST value whose primary reference is not recorded in the provenance file"
        else:
            tier, why = "C", "compilation values only"
        if der and tier in ("A", "A-AGG", "B", "B?"):
            why += "; derivative agreement (not counted): " + ", ".join(der)
        out.append(("octane", r["molecule"], prop, r["paper_value"], cls, tier, why))
    return out


def study_groups(determinations):
    """Distinct first-author surnames of the non-compilation determinations in a NIST listing
    ("value (method; Author, A.; ..., YEAR: full reference; ...)"). Two entries of one study (for
    example two methods, or two temperatures) and two papers of one first author count once."""
    groups = set()
    for m in re.finditer(r"(?:\(|;\s*)([A-Z][A-Za-z'\-]+)(?:[^;:()]*?),\s*(\d{4}):", determinations):
        surname = m.group(1)
        if not re.search(COMPILATION_AUTHORS, surname) and surname not in ("Anonymous",):
            groups.add(surname)
    return groups


# First authors who published together are one research group: Fenske, Braun et al. 1947 and Braun,
# Spooner, Fenske 1950 (Penn State); Howard, Mears et al. 1947, Pomerantz, Mears et al. 1949 and
# Mears, Fookson et al. 1950 (National Bureau of Standards). Anonymous entries are not counted.
SAME_GROUP = [{"Fenske", "Braun"}, {"Howard", "Mears", "Pomerantz"}]


def merge_coauthor_groups(groups):
    out = set(groups)
    for g in SAME_GROUP:
        if out & g:
            out = (out - g) | {"/".join(sorted(g))}
    return out


def nonane_rows():
    out = []
    for r in csv.DictReader(open(os.path.join(ROOT, "external", "nonane_provenance.csv"), newline="")):
        rule, d = r["selection_rule"], r["all_determinations"]
        entries = [e.strip() for e in d.split(");") if e.strip()]
        if rule.startswith("NIST average"):
            tier, why = "A-AGG", "NIST average (AVG); constituent determinations listed by NIST but averaged by TRC"
        elif rule.startswith("only one") or rule.startswith("single"):
            src = re.search(r"\(([^()]*?),\s*(\d{4})", d)
            who = (src.group(1).split(";")[-1].strip() + " " + src.group(2)) if src else "unknown"
            if re.search(COMPILATION_AUTHORS, who):
                tier, why = "C", f"single NIST entry, a compilation ({who}); earliest determination not identifiable"
            else:
                tier, why = "B", f"single primary determination ({who})"
        elif rule.startswith("no NIST AVG"):
            groups = merge_coauthor_groups(study_groups(d))
            tier = "A" if len(groups) >= 2 else ("B" if groups else "C")
            why = (f"most recent primary value chosen; {len(groups)} distinct research group(s) among the non-compilation "
                   f"determinations ({', '.join(sorted(groups))})")
        else:
            tier, why = "?", rule[:60]
        out.append(("nonane", r["name"], r["property"], r["value_used"], rule[:40], tier, why))
    return out


def bp_rows():
    out = []
    for r in csv.DictReader(open(os.path.join(ROOT, "external", "bp", "bp_provenance.csv"), newline="")):
        if r["status"] != "INCLUDED":
            continue
        rule = r["rule_or_reason"]; m = re.match(r"median of (\d+) non-compilation", rule)
        if rule.startswith("AVG") or rule.startswith("mean of 2 NIST averages"):
            tier, why = "A-AGG", "NIST average (TRC); constituent points not archived, so their independence cannot be checked"
        elif m and int(m.group(1)) >= 2:
            refs = re.findall(r"\(([^;()]+?),\s*(\d{4});", r["all_determinations"])
            groups = {re.split(r"[ ,]", a.strip())[0] for a, y in refs if not re.search(COMPILATION_AUTHORS, a)} - {"Anonymous"}
            groups = merge_coauthor_groups(groups)
            tier = "A" if len(groups) >= 2 else "B"
            why = f"median of {m.group(1)} non-compilation determinations from {len(groups) or '?'} distinct first authors"
        elif m:
            tier, why = "B", "one non-compilation determination"
        else:
            tier, why = "?", rule[:60]
        out.append(("bp", r["name"], "T_B", r["T_B_C"], rule[:40], tier, why))
    return out


rows = octane_rows() + nonane_rows() + bp_rows()
with open(os.path.join(HERE, "claim_provenance_ledger.csv"), "w", newline="") as f:
    w = csv.writer(f); w.writerow(["dataset", "molecule", "property", "value_used", "provenance_label", "tier", "basis"]); w.writerows(rows)
cnt = collections.Counter((d, p, t) for d, _, p, _, _, t, _ in rows)
lines = ["Source-independence ledger (tiers: A independent, A-AGG NIST/TRC average, B single primary, B? single NIST value,"
         " primary reference not recorded, C derivative only, D unverified)"]
for d, p in sorted({(d, p) for d, _, p, *_ in rows}):
    tiers = {t: cnt[(d, p, t)] for t in ("A", "A-AGG", "B", "B?", "C", "D", "?") if cnt[(d, p, t)]}
    lines.append(f"{d:7} {p:6} n={sum(tiers.values()):3}  " + "  ".join(f"{t}:{n}" for t, n in tiers.items()))
tot = collections.Counter(t for *_, t, _ in rows)
lines.append("all values: " + "  ".join(f"{t}:{tot[t]}" for t in ("A", "A-AGG", "B", "B?", "C", "D", "?") if tot[t]) + f"  (n={len(rows)})")
out = "\n".join(lines) + "\n"
print(out, end="")
open(os.path.join(HERE, "claim_provenance_out.txt"), "w").write(out)
