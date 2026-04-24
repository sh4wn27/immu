# Manuscript Outline & Writing Strategy

**Working title:** Modeling the equity impact of partial HLA mismatch tolerance via biodegradable stealth coatings: a population-genetics simulation.

**Target:** Journal of Emerging Investigators (JEI). Backup: NHSJS.
**Length:** 4000–5000 words + 5 figures + 1 table. JEI permits supplementary materials — anything peripheral goes there.

---

## 1. What the paper is actually arguing

One central quantitative claim: **a stealth coating that masks ~1–2 HLA mismatches disproportionately benefits ethnically underserved patients, shrinking the donor-match disparity ratio by roughly X-fold relative to the strict-match baseline.** Every section should bend toward defending that claim. If a result or paragraph does not either (a) support it, (b) qualify it, or (c) rule out a plausible counter-explanation, it gets cut.

Secondary claims the paper must also earn:
- The Monte-Carlo estimator is well-calibrated (validated on a Hardy-Weinberg null case where closed-form match probability is known).
- Conclusions are robust to the three biggest modeling choices: (i) τ, (ii) locus set, (iii) independence assumption across loci.

**What the paper is NOT trying to do:** predict clinical outcomes, model GvHD severity, or validate the coating technology. That scope-honesty belongs up front.

## 2. Depth / analytical target

JEI is for middle- and high-school authors but reviewers are real scientists. The depth bar, concretely:

- **Methods section must be replication-able.** A grad student should be able to reproduce every number from the GitHub repo alone. No hand-waving.
- **Every probability reported gets a 95% bootstrap CI.** No bare point estimates in figures or tables.
- **Every modeling choice gets a sensitivity test.** If τ is the headline parameter, the paper shows how the conclusion changes across τ ∈ {0, 1, 2}. If loci are A/B/DRB1, supplementary shows what adding C or DQB1 does.
- **One validation figure.** Simulated match probability at τ=0 compared against a closed-form expectation under HWE — a one-locus analytical check. Without this, reviewers will reasonably ask whether the simulator is even correct.
- **Limitations section is specific, not generic.** "LD not modeled → match probabilities overstated by roughly factor Y" beats "we did not model LD."

Anything that sounds like a textbook review of HLA biology gets compressed. The Intro is ~500 words, not 1500.

## 3. Figures (final set, in paper order)

| # | Title (working) | What it shows | Why it's in the paper |
|---|-----------------|---------------|-----------------------|
| **Fig 1** | Concept schematic | Hand-drawn/vector diagram: HLA-mismatch → GvHD; coating masks epitopes → partial tolerance; what the simulation represents as a box-and-arrow. | Anchors the biology for non-specialist reviewers. Non-data. |
| **Fig 2** | Allele diversity heatmap | Heatmap of per-locus Shannon entropy (or # alleles at >1% freq) across populations. | Motivates why match probability varies by population. Validates the data is sane. |
| **Fig 3** | Match probability by population and τ | Grouped bar chart w/ bootstrap CIs: match prob at τ=0, 1, 2 for each of 6 populations. | The main result, panel A of the story. |
| **Fig 4** | Equity gap under coating | The headline chart. Disparity ratio (max/min match prob across populations) as a function of τ. Ribbon = bootstrap CI on the ratio. | This is the paper's central equity claim. |
| **Fig 5** | Sensitivity analysis grid | 2×2 subplot: (a) add HLA-C, (b) halve N per population, (c) alternative τ definitions, (d) under LD approximation (if feasible). Each shows disparity-ratio conclusion stability. | Pre-empts the biggest reviewer objections. |

Supplementary figures (not counted in the 5):
- S1: Simulator validation — empirical vs. closed-form match probability for one-locus HWE.
- S2: Per-locus allele-frequency top-10 tables for each population (reproducibility).
- S3: Convergence curve — match-prob estimate vs. N_pairs, showing 100k is sufficient.

## 4. Table (one, small)

| Table 1 | Summary: match probability at τ=0/1/2 and pool-expansion factor per population, with 95% CIs. |

Numerical source of truth that reviewers screenshot. One column: population. Three columns: τ=0, 1, 2 match probs (with CIs). One final column: fold-change (τ=2 / τ=0).

## 5. Section plan (~4500 words)

| Section | Words | What it contains | Load-bearing? |
|---------|-------|------------------|---------------|
| Abstract | 200 | Problem → what we did → headline result with numbers → implication | Yes |
| Introduction | 500 | HSCT equity gap (cite NMDP data) → coating technologies briefly (1 paragraph, cite Treacy et al., Kim et al. on stealth coatings) → quantitative gap in literature → our contribution | Yes |
| Methods | 1200 | Data source; allele sampling model; match definition; τ parameter definition; bootstrap CI procedure; sensitivity analyses planned; code/data availability | Yes |
| Results | 1400 | Fig 2 → Fig 3 → Fig 4 → Fig 5, in that order. Each figure: one paragraph describing, one short paragraph interpreting. | Yes |
| Discussion | 900 | Interpretation of equity result; magnitude in clinical-relevance terms (use a back-of-envelope: e.g., "translates to N more matched donors per 1000 patients for population X"); limitations (LD, single τ assumption, population-sampling bias in AFND itself); future work | Yes |
| Conclusion | 150 | Two sentences restating the claim, one sentence on broader implication | Yes |
| Acknowledgments | 50 | Mentor (if any), AFND, TJHSST | — |
| References | — | BibTeX via `references.bib`. Aim for 20–30 refs, not 80. | — |
| Supplementary | ~500 | Validation figure, robustness tables, deposited-code statement | Yes |

## 6. Writing style rules (JEI-compatible)

- First-person plural ("we"), past tense for methods and results, present for discussion.
- Numbers inline with units and CIs: "match probability at τ=0 was 0.00014 (95% CI: 0.00008–0.00022)" — no naked point estimates.
- Keep sentences short. Aim for Flesch-Kincaid ≤ 12; JEI reviewers include HS peers.
- No unnecessary jargon. First-use definitions for HLA, HSCT, GvHD, LD, HWE, AFND, τ.
- Every number that appears in prose must also appear in a figure or table.
- No banned phrases: "delve into," "in order to," "it is important to note." Strike on sight.

## 7. LaTeX setup

- Class: `article`, 11pt, single column, 1-inch margins (JEI has no strict template at submission — plain article is fine).
- Key packages: `graphicx`, `booktabs`, `siunitx`, `amsmath`, `natbib` with `plainnat`, `microtype`, `hyperref`, `cleveref`.
- Figures: PDF-first (fig3/4/5 are already PDF from `make_figures.py`). Fig 1 = TikZ vector schematic committed as `.tex` for reproducibility.
- BibTeX file: `references.bib`. Critical refs identified below; filled in as reading progresses.

## 8. Reference targets (to collect in `references.bib`)

- **HLA biology & HSCT basics:** Choo 2007 (HLA review); Tiercy 2016 (HLA matching in transplantation).
- **Equity gap data:** Barker et al. 2019 (umbilical cord blood for minorities); NMDP/Be-The-Match annual reports; Gragert et al. NEJM 2014 — the canonical "HLA matching and the global donor registry" paper.
- **Stealth coatings on cells:** Teramura & Iwata 2010 (polymer cell-surface engineering); Cabric et al. 2007 (islet coating); more recent Nature/Nature Biotech papers on HSC masking (need to search).
- **AFND:** González-Galarza et al. 2020, *Nucleic Acids Res.*
- **Population-genetics foundations:** Hardy 1908 / Weinberg 1908 (for HWE, if needed).
- **Monte-Carlo methodology:** Efron bootstrap 1979 (for the CI construction citation).
- **Health-equity framing:** Krieger 2014 or similar (for the disparity ratio concept).

Target: 20–30 refs. If we're citing more than 40, we're drifting into a review.

## 9. Execution order (before first full draft)

1. Replace synthetic TSVs with real AFND downloads (populates `data/raw/`).
2. Add simulator validation test + supplementary Fig S1.
3. Add Fig 2 generator (entropy heatmap) to `make_figures.py`.
4. Re-run full pipeline, regenerate Fig 3/4/5 on real data.
5. Build Table 1 CSV→LaTeX helper.
6. Draft Methods first (the easiest section; it's just describing what the code does).
7. Draft Results from figures, one figure at a time.
8. Intro + Discussion last; they depend on what Results actually show.

## 10. Risks specific to writing

- **The result is underwhelming under real AFND data.** Mitigation: publishable either way; reframe as "quantitative ceiling on coating benefit". Abstract keeps the structure either way.
- **Reviewers will ask about LD.** Mitigation: pre-empt with a supplementary analysis where haplotype data exists (CEU and Han Chinese both have public haplotype freqs via AFND); show disparity-ratio conclusion is directionally unchanged.
- **τ is a hand-wave.** Mitigation: present τ as a modeling abstraction, not a measured quantity. Cite the coating-MLR literature that makes τ∈[0,2] plausible, and show sensitivity across that range.
- **Word count creep in Introduction.** Mitigation: hard cap at 500 words, enforced at every draft pass.
