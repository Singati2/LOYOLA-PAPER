# MATCH format and reference check of `main.tex` (2026-10-18)

Scope: abstract, conclusion, references, tables and figures of `main.tex`, checked against the
current MATCH template (downloaded from `match.pmf.kg.ac.rs/template/match_template.zip` on
2026-10-18), the MATCH "prepare" instructions, and recent MATCH papers (Rada, MATCH 96 (2026)
841–863; Gutman et al., MATCH 97 (2027) 165–174; Nyauli–Buragohain, MATCH 97 (2027) 135–164;
Kırgız, MATCH 97 (2027) 121–134).

## Template and layout

| Item | Result |
|---|---|
| Template code above "DO NOT MODIFY THE EXISTING CODE ABOVE THIS LINE" | byte-identical to the current template; added packages and macros are in the permitted slots |
| Page size, font size | A5 (419.5 × 595.3 pt), 10 pt, same as the published papers |
| First page (header box, title, authors, address, e-mail, "Received", abstract, footnote) | same layout as Rada 2026 when rendered side by side |
| Running page number, section headings, line spacing (page 2) | same as Rada 2026 |
| Abstract | rewritten 2026-10-19 to the current MATCH pattern: one paragraph, 183 words (16 abstracts of MATCH 97 (2027): median 167, range 41 to 248), object defined first with short inline formulas, results next, statistics in one closing sentence; no citations or cross-references (template rule); fits on page 1 with no overfull or underfull line. Content kept: the family and its reduction to M_{alpha,beta}, Rada's separation theorem, the shared limit of degree-ratio indices, orders 12/15 with counterexamples at every larger order, at most five order exchanges, the extremal trees, both statistical outcomes |
| Keywords, MSC | none (template: "No keywords! No Mathematics Subject Classification!") |
| References | alphabetical by first author, as required; format follows the template examples |
| E-mail line | now lists every author's address in author order, as recent multi-author MATCH papers do: nataraad@oregonstate.edu (Advik Natarajan; Oregon State University mathematics directory, 2026-10-19), gshiwakoti2022@fau.edu (supplied by Ganesh Shiwakoti), marockiaraj@gmail.com |
| Acknowledgment | conforms: uses the template's `\acknowledgment` command. The text is the authors' own (commit `3c3d363`, shortened by the authors in `8d1cd25`), so it was left unchanged |
| Colour figures (90 EUR each) | `main.tex` has no figures; both figures are in the supplement |

## Conclusion, tables and figures against recent MATCH papers (2026-10-19)

| Item | Recent MATCH practice | `main.tex` |
|---|---|---|
| Last section | "Conclusion(s)" or "Concluding remarks": summary of results, open problems (Rada, MATCH 96 (2026) 841–863; Nyauli–Buragohain and Gutman et al., MATCH 97 (2027)) | "Conclusion": summary, open problems; same pattern |
| Table captions | bold "Table N." label, small type, from the template's caption settings; placed above the table in 6 of the 9 MATCH 97(2) papers with tables, below in 3 | bold "Table N.", small type, above; matches the majority practice |
| Figures | — | none in `main.tex` (both are in the supplement) |
| Data availability | absent in the 12 recent MATCH papers checked; not required or forbidden by MATCH | present, because it states that the NIST pages are not redistributed; kept |
| Acknowledgment | template's `\acknowledgment` command, as in recent papers | same |

## Abstract and conclusion against the body

* All numbers agree with the body: orders 12/13 and 16, at most five exchanges, the boiling-point and
  vaporisation-enthalpy verdicts, the in-point-estimate qualifiers.
* Changed on 2026-10-18: the abstract and the conclusion presented the separation of imbalance
  histograms at algebraic γ, and the shared limit of all degree-ratio indices, without crediting Rada
  2019 (Theorem 3.4 and Proposition 2.5). Both now credit them, as the short version's abstract already
  did. The abstract was tightened so that it still fits on page 1.

## Tables and figures

Six tables (`tab:collisions`, `tab:firstfail`, `tab:fgdss`, `tab:lo_octane`, `tab:bp`,
`tab:deviations`), no figures. Each has a caption and a label, and each is referenced in the text
before it appears. 0 overfull boxes. Their numerical contents are checked by the core verifier
(FULL PASS in `verify.py --full` on `8052959`; no table has changed since).

## References: existence and bibliographic data (56 of 56 cited, 0 uncited, 0 duplicates)

The template warns that manuscripts with non-existent references are rejected and their authors
black-listed. Each reference was checked against an authoritative record:

| Source of the check | References |
|---|---|
| MATCH's own issue contents pages (authors, title, volume, pages) and volume years | AliGutmanEtAl2027DRSO (97: 639–656), BarmanDas2026HSO (95: 63–94), CruzRada2019PathStar (82: 715–732), Gutman2021Sombor (86: 11–16), Gutman2026SomborSurvey (96: 819–837), GutmanRedzepovicBuragohainNyauli2027 (97: 165–174), HuMATCH2022 (88: 505–520), MovahediGutmanRedzepovicFurtula2026 (95: 141–162), NyauliBuragohain2026CoRSO (96: 295–324), NyauliBuragohain2027DRSO (97: 135–164), Rada2019ExpVDB (82: 29–41), Rada2026LinearVDB (96: 841–863), RadaRodriguezSigarreta2022Weak (87: 97–108), RetiSharafdini2018IRLA (79: 509–524), ShaoJahanbani2027 (97: 657–675; Crossref's first page 567 is a Crossref error), SongHuang2023EDV (89: 343–370). Years: 79 = 2018, 82 = 2019, 86 = 2021, 87 and 88 = 2022, 89 = 2023, 95 and 96 = 2026, 97 = 2027 |
| Crossref record (title, authors, volume, print year, pages) | AliGutmanFurtula2026BID, AliGutmanFurtulaAlbalahiHamza2025, Besicovitch1940, CarballosaQuintanaRodriguezSigarreta2023, CruzMonsalveRada2020, DasMondal2024ExpGA (print 2024), DasMondalRazaPal2025ExpISDD, FurtulaGutmanDehmer2013SS, GaoAMC2024, GranadosJMC2025GM, GutmanBuragohainNyauli2026, GutmanMilovanovic2020AKCE, GutmanTrinajstic1972, Jameson2006, Konstantinova1996Degeneracy, LinZhouWangMiao2022, Mityagin2020, MolinaSigarreta2025GM, PortillaJMC2025GM, RakicFurtula2019SS, Randic1975, Reid1972, Sigarreta2022ExpVDB, VukicevicFurtula2009GA, Wiener1947, ZhouTrinajstic2009sumconn, ZhouTrinajstic2010 (print 2010), Brown1986 (DOI 10.1214/lnms/1215466757) |
| zbMATH open API | BollobasErdos1998 (Ars Combin. 50 (1998) 225–233, zbMATH 1602780) |
| Journal or index pages found by web search | Albertson1997 (DBLP; Ars Combin. 46 (1997)); DeutschKlavzar2015 (SID, DOI 10.22052/ijmc.2015.10106); VukicevicGasperov2010 (Hrčak); GutmanRedzepovicKizilirmakKulli2025EU (DOI 10.30538/oms2025.0249); ShirdelRezapourSayadi2013HM (DOI 10.22052/ijmc.2013.5294) |
| Library catalogue / DOI resolver | Baker1975, APIProject44Circ461 (Open Library); NISTWebBook (DOI 10.18434/T4D303 resolves to the WebBook); WilhoitZwolinski1971 (the subject of the Reid 1972 review); LoyolaRepo (the repository itself) |

Crossref flags that are not errors in the paper: Crossref's year for DasMondal2024ExpGA (2023),
ZhouTrinajstic2010 (2009), SongHuang2023EDV (2022), RadaRodriguezSigarreta2022Weak (2021) and the MATCH 97
papers (2026) is the online-first date; the print year, which the paper cites, matches. For MATCH papers
Crossref stores the issue number in the volume field (e.g. "3" for Gutman2026SomborSurvey, which is
volume 96, issue 3) and only the first page; both were checked against MATCH's contents pages above.

Open points for the authors:

* **LabaufGreenshieldsRossini1961**: resolved 2026-10-19. Ganesh Shiwakoti checked the printed article
  (J. Chem. Eng. Data 6 (1961) 261–263, DOI 10.1021/je60010a023): the byline reads "A. Labauf", as in the
  publisher's metadata. The bibliography entries of the paper, the supplement and the short versions, and the
  supplement's in-text author list, now read "Labauf". Where the text quotes NIST's attribution ("NIST lists 4
  under Labbauf et al.") NIST's spelling is kept and "(printed as Labauf)" is added.
* ShirdelRezapourSayadi2013HM was corrected by Basavanagoud and Patil (Iran. J. Math. Chem. 7 (2016)).
  The paper cites it only for the hyper-Zagreb index name, which the correction does not affect.
* Affiliations (2026-10-19, on the authors' instruction): Advik Natarajan, Department of Mathematics, Oregon State University (the department directory lists him as a graduate student); Michael Arockiaraj, Loyola College, now affiliation c.
