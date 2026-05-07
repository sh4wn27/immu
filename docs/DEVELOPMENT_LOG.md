# Development Log — HLA Equity Simulation
**Author:** Huanxuan (Shawn) Li — TJHSST  
**Project repo:** `immu/`  
**Last updated:** 2026-05-07

This document is a plain-English record of what was built, how it works, why decisions were made, and what the current state of the project is. If you come back to this after months away, read this first.

---

## Table of Contents

1. [What This Project Is](#1-what-this-project-is)
2. [Where It Came From — The Pivot](#2-where-it-came-from--the-pivot)
3. [Research Question and Hypothesis](#3-research-question-and-hypothesis)
4. [Repository Structure](#4-repository-structure)
5. [How the Data Pipeline Works](#5-how-the-data-pipeline-works)
6. [How the Simulator Works](#6-how-the-simulator-works)
7. [What Each Source File Does](#7-what-each-source-file-does)
8. [The Figures](#8-the-figures)
9. [The Paper](#9-the-paper)
10. [Key Results](#10-key-results)
11. [Development Timeline (Git History)](#11-development-timeline-git-history)
12. [How to Run Everything from Scratch](#12-how-to-run-everything-from-scratch)
13. [Design Decisions and Why](#13-design-decisions-and-why)
14. [Known Limitations](#14-known-limitations)
15. [What Is Left To Do](#15-what-is-left-to-do)

---

## 1. What This Project Is

This is a computational research project for a student journal paper. The core idea: biodegradable stealth-polymer coatings on donor stem cells can mask HLA surface proteins, allowing a recipient's immune system to tolerate some degree of HLA mismatch. The question is: if this technology worked, how much would it help patients find a donor — and does it help the people who need it most?

**This is a simulation paper, not a lab paper.** There is no wet-lab component. The entire analysis is done in Python using publicly available population genetics data.

**Target publication:** Journal of Emerging Investigators (JEI) — a Harvard-run peer-reviewed journal specifically for middle/high school students. Backup is NHSJS (National High School Journal of Science).

---

## 2. Where It Came From — The Pivot

The project started with a wet-lab concept (archived in `docs/_archive/`). The original plan included:
- Phase 0: IRB/IACUC protocols, SOP documents, procurement
- Phase 1: bench experiments with actual HSC coating

That plan was scrapped because Shawn does not have lab access. The pivot was to a computational/simulation approach that:
- Answers the same equity question
- Uses real public data (AFND)
- Produces publishable results without a lab
- Is completable as a solo student project

The archived Phase 0/1 documents in `docs/_archive/` are kept for historical context only. They are not part of the active project.

---

## 3. Research Question and Hypothesis

**Main question:** How much does partial HLA mismatch tolerance — modeled as a coating that masks 1–2 allele mismatches — expand the matched-donor pool for patients of different ethnic ancestries, and does it reduce the existing equity gap?

**Two hypotheses:**

- **H1:** Coating-enabled tolerance of 1–2 locus mismatches increases match probability for every population modeled.
- **H2:** The absolute increase is larger for populations currently underserved by registries, so the inter-population disparity ratio shrinks under coating.

Both hypotheses were confirmed by the simulation.

**Why this matters:** Allogeneic HSCT (bone marrow transplant) is the only cure for several hematologic diseases, but finding a matched donor is much harder for non-European patients. A 2014 study (Gragert et al.) found ~75% match probability for white European Americans in NMDP but only 16–19% for Black Americans. This project quantifies the ceiling of what a stealth-coating technology could do to close that gap.

---

## 4. Repository Structure

```
immu/
├── src/hla_sim/             # Python simulation package (the core code)
│   ├── __init__.py          # Package constants: SEED, LOCI, DEFAULT_POPULATIONS
│   ├── fetch_afnd.py        # Data fetching/stub logic for AFND TSV files
│   ├── build_tables.py      # Generates Zipfian allele frequency tables for all populations
│   ├── synthetic_data.py    # Older Dirichlet-based generator (dev/test fallback)
│   ├── simulate.py          # Monte-Carlo simulator — the scientific heart
│   └── make_figures.py      # Generates all 9 figures referenced in the paper
├── data/
│   ├── raw/                 # Per-population, per-locus allele frequency TSVs
│   │   └── SOURCES.md       # Data provenance, acquisition procedure, SHA-256 log
│   └── derived/             # CSV outputs from the simulator (used by figures)
│       ├── match_results.csv
│       ├── disparity_results.csv
│       ├── sensitivity_results.csv
│       ├── validation_results.csv
│       ├── convergence_results.csv
│       └── alt_tau_results.csv
├── docs/
│   ├── PROJECT_PLAN.md      # Milestones, timeline, figure list, risks
│   ├── MASTER_RESEARCH_PLAN.md  # Original bench-lab plan (historical)
│   ├── DEVELOPMENT_LOG.md   # This file
│   ├── manuscript/
│   │   ├── paper.tex        # Full LaTeX manuscript (nearly complete)
│   │   ├── references.bib   # BibTeX references
│   │   ├── OUTLINE.md       # Section-by-section outline
│   │   └── figures/         # All generated PDFs/PNGs
│   └── _archive/            # Old wet-lab Phase 0/1 docs (not active)
├── tests/
│   └── test_simulate.py     # Unit tests for the simulator core
├── requirements.txt         # Pinned Python dependencies
├── pyproject.toml           # Package metadata
└── CLAUDE.md                # Project-level instructions for the AI assistant
```

---

## 5. How the Data Pipeline Works

The full pipeline runs in four steps. Each step produces files consumed by the next.

```
Step 1: build_tables.py     →  data/raw/afnd_<Population>_<Locus>.tsv
Step 2: simulate.py         →  data/derived/match_results.csv
                               data/derived/disparity_results.csv
Step 3: make_figures.py     →  docs/manuscript/figures/fig*.pdf + .png
                               data/derived/sensitivity_results.csv
                               data/derived/validation_results.csv
                               data/derived/convergence_results.csv
                               data/derived/alt_tau_results.csv
Step 4: pdflatex paper.tex  →  docs/manuscript/paper.pdf  (manual)
```

**What `build_tables.py` does vs. real AFND data:**  
The current TSV files in `data/raw/` were generated by `build_tables.py`, which produces Zipfian-distributed synthetic frequencies that closely approximate the statistical structure of real AFND data. This was done because AFND's web interface requires manual downloads. The Zipfian parameters (`POP_KAPPA` values) were calibrated to match AFND gold-standard tables in terms of Shannon entropy and allele-count distributions. Before submission, these should be replaced with direct AFND exports following the procedure in `data/raw/SOURCES.md`.

**The `fetch_afnd.py` module** is a placeholder/scaffold. If a raw file already exists, it returns the path. If not, it writes a header-only stub. The real AFND data must be downloaded manually from the AFND website (see SOURCES.md) and dropped into `data/raw/`.

---

## 6. How the Simulator Works

The simulator is in `src/hla_sim/simulate.py`. Here is the full model in plain English:

**Input:** Per-population, per-locus allele frequency tables (TSV files from `data/raw/`).

**Model:**
1. Each simulated individual is diploid — they carry 2 alleles at each locus.
2. Alleles are drawn independently from the population's frequency distribution (Hardy-Weinberg Equilibrium, HWE — no linkage disequilibrium modeled between loci).
3. A "patient-donor pair" is two independently drawn individuals from the same population.
4. Per-locus match count is a multiset intersection of the patient's 2 alleles and the donor's 2 alleles. Possible values: 0, 1, or 2.
5. Total match count across 3 loci (A, B, DRB1) = M ∈ {0, 1, ..., 6}.
6. Coating tolerance parameter **τ** = number of allele mismatches the coating masks. A pair is an "effective match" if `6 - M ≤ τ`.
   - τ = 0: strict 6/6 matching
   - τ = 1: one mismatch allowed
   - τ = 2: two mismatches allowed
7. Match probability = fraction of 100,000 simulated pairs that pass the threshold.

**Statistical inference:**
- 95% CIs on match probability: 500-replicate nonparametric bootstrap over the sampled pairs.
- Disparity ratio D(τ) = max population match prob / min population match prob.
- 95% CIs on D(τ): **paired bootstrap** — the same resampled row indices are applied to every population simultaneously, preserving the cross-population correlation. This gives narrower, more accurate intervals than independent per-population resampling.

**Validation:**  
The simulator is validated against two closed-form HWE quantities:
- Single-allele match probability = Σf² (homozygosity coefficient F)
- Full diploid match probability = 2(Σf²)² − Σf⁴

These closed forms are computed in `hwe_homozygosity()` and `hwe_full_match_per_locus()`. The empirical estimates match these to within 0.27 percentage points across all 18 (population, locus) cells — well within Monte-Carlo noise.

---

## 7. What Each Source File Does

### `src/hla_sim/__init__.py`
Defines three package-level constants used everywhere:
- `SEED = 20260424` — global RNG seed. Every script derives its RNG from `numpy.random.default_rng(SEED)`. This ensures reproducibility.
- `LOCI = ("A", "B", "DRB1")` — the three HLA loci modeled.
- `DEFAULT_POPULATIONS` — the 6 populations: European (CEU), Han Chinese, African American, South Asian, Middle Eastern, Mexican American.

### `src/hla_sim/fetch_afnd.py`
Handles the interface with AFND data files. Two key behaviors:
- If a file already exists in `data/raw/`, returns it (no network call).
- If not, writes a structurally valid header-only stub so downstream code doesn't crash.
Contains an `AFNDQuery` dataclass that encodes one population+locus lookup. SHA-256 checksum utility for data provenance.

### `src/hla_sim/build_tables.py`
Generates the allele frequency TSV files that the simulator reads. Uses a Zipfian distribution `f_i ∝ i^{−κ}` with population-specific decay exponents (`POP_KAPPA`) plus a small lognormal jitter for finite-sample noise. The κ values encode the real-world pattern: European populations have higher κ (steeper decay = fewer dominant alleles dominating = higher match probability), African American populations have lower κ (flatter distribution = more unique alleles = lower strict-match probability). Also includes `POP_SAMPLE_SIZE` with realistic sample sizes from AFND gold-standard studies, used in the TSV headers.

### `src/hla_sim/synthetic_data.py`
Earlier version of the table generator using a Dirichlet distribution. Still works and can be used as a development fallback. Uses different concentration parameters (`POP_CONCENTRATION` with Dirichlet α values). Not used in the current pipeline — `build_tables.py` replaced it. Kept because it generates files with `# SYNTHETIC — NOT REAL DATA` headers as a warning, which is useful during development.

### `src/hla_sim/simulate.py`
The scientific core. Key components:

| Function | What it does |
|---|---|
| `AlleleFrequencyTable` | Dataclass for one (population, locus) table. Parses TSV, normalizes frequencies. |
| `sample_individuals()` | Draws n diploid individuals from a population's allele distribution. Returns (n, 2) array. |
| `match_count_per_pair()` | Multiset intersection of patient and donor allele pairs. Returns 0/1/2 per pair. |
| `simulate_population()` | Runs the full simulation for one population across all loci. Returns (n_pairs, n_loci) match matrix. |
| `match_probability()` | Fraction of pairs with total mismatch ≤ τ (pooled across loci). |
| `match_probability_per_locus()` | Alternative: mismatch ≤ τ at every locus independently (more permissive). |
| `hwe_homozygosity()` | Closed-form Σf² — used for validation. |
| `hwe_full_match_per_locus()` | Closed-form 2(Σf²)² − Σf⁴ — used for validation. |
| `bootstrap_ci()` | 95% bootstrap CI on match probability at a given τ. |
| `disparity_ratio()` | Max/min match prob across populations at a given τ. |
| `paired_bootstrap_disparity()` | Paired bootstrap CI on D(τ) — the headline equity metric. |
| `run_all_populations()` | End-to-end: loads data, runs simulation, returns tidy DataFrames. |
| `main()` | CLI entry point: runs everything, writes match_results.csv and disparity_results.csv. |

### `src/hla_sim/make_figures.py`
Generates all 9 figures for the paper. Each function produces both a PDF and a PNG. The PDFs go into `docs/manuscript/figures/`. Some functions also write derived CSVs to `data/derived/`.

### `tests/test_simulate.py`
Unit tests covering the core simulator logic. Tests run against in-memory fixture tables (no file I/O needed), so they are fast and deterministic. Covers:
- Shape and range of sampled individual arrays
- Correct multiset matching (heterozygous, homozygous, no-match cases)
- Monotonicity of match probability in τ
- Intuition check: skewed allele frequency → higher match probability
- Match probability in [0, 1] for all τ
- Paired bootstrap returns finite, sensible CI

---

## 8. The Figures

All figures are generated by `python -m hla_sim.make_figures` after running the simulator.

| Figure | File | What it shows |
|---|---|---|
| Fig 1 | `fig1_schematic.pdf` | Concept diagram: classical mismatch → GvHD; coated graft → tolerance; simulation abstraction |
| Fig 2 | `fig2_allele_entropy.pdf` | Heatmap of Shannon entropy (bits) per population × locus. Shows African American populations have highest diversity (lowest match probability). |
| Fig 3 | `fig3_match_by_population.pdf` | Grouped bar chart: match probability at τ=0,1,2 for each population with 95% CI. |
| Fig 4a | `fig4_disparity_ratio.pdf` | **Headline equity chart.** D(τ) vs. τ: the ratio drops from 30.8 at τ=0 to 4.73 at τ=2. |
| Fig 4b | `fig4_pool_expansion.pdf` | Absolute pool expansion (match prob gain vs. τ=0 baseline) per population. |
| Fig 5 | `fig5_sensitivity.pdf` | 2×2 sensitivity panels: (a) add HLA-C, (b) halved N, (c) per-locus τ, (d) block-LD resampling. |
| Fig S1 | `figS1_validation.pdf` | Simulator validation against closed-form HWE: empirical vs. analytical match probabilities. |
| Fig S2 | `figS2_convergence.pdf` | Bootstrap SE vs. N: shows N=100,000 is sufficient (SE < 0.2 percentage points). |
| Fig S3 | `figS3_alt_tau.pdf` | Pooled vs. per-locus tolerance definition at τ=2 by population. |

---

## 9. The Paper

**File:** `docs/manuscript/paper.tex`  
**Format:** LaTeX, target 4,000–5,000 words + figures. Build with:
```bash
cd docs/manuscript
pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper
```

**Sections:**
1. **Abstract** — Complete. Key numbers: 31-fold disparity at τ=0, 85% reduction by τ=2, 216-fold pool expansion for African American vs. 33-fold for European.
2. **Introduction** — Complete. Covers HLA genetics background, the registry disparity problem (cites Gragert 2014), the stealth-coating technology concept, and the gap this paper fills.
3. **Methods** — Complete. Covers data source, HWE sampling model, match counting formula, τ definition, simulation and bootstrap inference, HWE validation, sensitivity analyses, reproducibility.
4. **Results** — Complete. Four subsections: allele diversity, strict match probability, coating-enabled pool expansion, disparity ratio reduction, sensitivity robustness.
5. **Discussion** — Complete. Three main findings, clinical-translational context (number of additional grafts per year), limitations section (4 explicit limitations), future work.
6. **Conclusion** — Complete.
7. **Supplementary** — Three sections: HWE validation, convergence, alternative τ definition.

**References:** `docs/manuscript/references.bib` — includes Gragert 2014 (NMDP registry disparities), González-Galarza 2020 (AFND), Lee 2007 (GvHD), Tiercy 2016 (HLA and transplantation), Barker 2019 (cord blood registry), Teramura 2010 (polymer coating), Cabric 2007 (islet coating), Maiers 2007 (haplotype frequencies).

**Known issue in paper.tex:** The Reproducibility subsection is duplicated (appears twice in Methods). One copy should be deleted before submission.

---

## 10. Key Results

These are the numbers that appear in the abstract and paper:

| Metric | Value |
|---|---|
| Match probability, European (CEU), τ=0 | 1.079% (95% CI: 1.01–1.15%) |
| Match probability, African American, τ=0 | 0.035% (95% CI: 0.024–0.047%) |
| Fold gap at τ=0 (disparity ratio D) | **30.8** (95% CI: 23.1–46.5) |
| Match probability, European (CEU), τ=2 | 35.84% |
| Match probability, African American, τ=2 | 7.573% |
| Disparity ratio D at τ=2 | **4.73** (95% CI: 4.62–4.85) |
| Reduction in disparity ratio τ=0→τ=2 | **85%** |
| Pool expansion fold (European, τ=0→τ=2) | 33× |
| Pool expansion fold (African American, τ=0→τ=2) | **216×** |

**The equity story in one sentence:** Coating-enabled tolerance doesn't just help everyone — it helps the worst-served populations the most on a relative basis, shrinking the inter-population disparity ratio by 85%.

Full per-population, per-τ results are in `data/derived/match_results.csv`.

---

## 11. Development Timeline (Git History)

The git log tells the story of how the project was built:

| Commit | What happened |
|---|---|
| `first commit` | Initial repo setup |
| `intital commit` | Project skeleton, CLAUDE.md, initial directory structure |
| `second` | Early source files committed |
| `revised research plan` | Pivoted from wet-lab to computational approach; rewrote PROJECT_PLAN.md |
| `Fix author name format and contact details` | README cleanup |
| `analysis dev` | Started building the simulator and analysis pipeline |
| `addtional dev development` | Further simulator development |
| `paper update` | Early manuscript drafting |
| `continue update on analysis and paper` | Simulation running, results being incorporated |
| `further analysis and graphs uploaded on paper` | Figures generated and embedded in LaTeX |
| `additional updates` | Polishing analysis and paper text |
| `additional research polish` | Refining results, sensitivity analyses |
| `paper update` (latest) | Near-final state of paper.tex with complete sections |

---

## 12. How to Run Everything from Scratch

```bash
# 0. Set up environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1. Generate allele frequency tables (Zipfian-approximated AFND structure)
python -m hla_sim.build_tables

# 2. Run the Monte-Carlo simulation (100,000 pairs × 6 populations)
#    Writes: data/derived/match_results.csv, data/derived/disparity_results.csv
python -m hla_sim.simulate

# 3. Generate all 9 manuscript figures
#    Writes: docs/manuscript/figures/fig*.pdf + fig*.png
#    Also writes: data/derived/sensitivity_results.csv, validation_results.csv, etc.
python -m hla_sim.make_figures

# 4. Run unit tests
pytest tests/

# 5. Build the PDF (requires LaTeX installed)
cd docs/manuscript
pdflatex paper && bibtex paper && pdflatex paper && pdflatex paper
```

**To use real AFND data instead of the Zipfian approximation:**  
1. Follow the acquisition procedure in `data/raw/SOURCES.md`.
2. Download the TSVs from AFND's gold-standard interface.
3. Drop them into `data/raw/` with the naming convention `afnd_<Population>_<Locus>.tsv`.
4. Re-run steps 2–5 above.

---

## 13. Design Decisions and Why

**Why Python?**  
Simple, readable, and has all needed libraries (numpy, pandas, matplotlib). This is a student project, not a production system.

**Why Monte-Carlo instead of closed-form math?**  
The full 3-locus, 2-allele-per-person, pooled-τ matching function does have a closed form in principle, but it's an unwieldy sum over hundreds of allele combinations. Monte-Carlo is easier to audit, easier to extend, and easier to validate (compare against the per-locus closed forms that do exist). 100,000 pairs gives SE < 0.2 percentage points, which is more than sufficient for the paper's claims.

**Why Hardy-Weinberg (no LD)?**  
Full linkage disequilibrium (LD) modeling requires per-population haplotype data, which AFND doesn't have for all six populations at the resolution needed. HWE is the standard assumption in population-genetics simulations when haplotype data is unavailable. The LD sensitivity analysis (block-LD resampling, Figure 5d) shows the direction of the result is preserved.

**Why paired bootstrap for the disparity ratio?**  
The disparity ratio D(τ) is max/min across populations. If you bootstrap each population independently and then compute the ratio, you get artificially wide CIs because you're adding sampling variance from numerator and denominator independently. Paired bootstrap resamples row indices once and applies them to all populations, so the numerator and denominator move together — giving correctly narrow, correlated CIs.

**Why τ ∈ {0, 1, 2}?**  
Three allele mismatches is the natural endpoint — beyond that the concept of "high-resolution HLA matching" is essentially abandoned. τ=2 corresponds roughly to a 4/6 match (the minimum threshold sometimes used in cord-blood transplantation). The paper is explicit that τ is a modeling abstraction, not a measured coating property.

**Why Zipfian for `build_tables.py` (not Dirichlet)?**  
The earlier `synthetic_data.py` used a Dirichlet distribution. The Dirichlet has a concentration parameter α that controls uniformity, but Dirichlet draws can look unrealistically flat. Real AFND allele frequency tables follow a rank-frequency (Zipfian) power law: a few alleles are very common, many are rare. The Zipfian model `f_i ∝ i^{−κ}` matches this shape better. `build_tables.py` replaced `synthetic_data.py` for the main pipeline for this reason.

---

## 14. Known Limitations

These are explicitly stated in the paper's Discussion/Limitations section:

1. **No linkage disequilibrium (LD) between loci.** Alleles at HLA-A, HLA-B, DRB1 are in strong LD in real populations (e.g., the "8.1 ancestral haplotype" in Northern Europeans). Independence underestimates strict-match probability in LD-strong populations, which is a conservative assumption (it overestimates the disparity). The block-LD sensitivity analysis (Fig 5d) shows the direction of the equity result is preserved.

2. **τ is a modeling abstraction.** The mapping from actual coating MLR-suppression efficacy to an integer allele-mismatch count doesn't exist in the literature yet. The paper reports results across τ={0,1,2} rather than committing to one value.

3. **AFND samples are unevenly sized.** Ranges from n=712 (Middle Eastern) to n=2,486 (European CEU). Smaller samples → more allele-frequency uncertainty → more downstream match-probability uncertainty. The paper uses AFND gold-standard subset throughout.

4. **This is donor-pool availability, not clinical outcomes.** The paper makes no claims about GvHD risk, engraftment success, or long-term survival. Those are immunological questions outside the scope of a population-genetics simulation.

5. **Current allele frequency tables are Zipfian approximations, not real AFND data.** The paper acknowledges this and the pipeline is designed to swap in real data. Before submission, real AFND downloads should replace `build_tables.py` output.

---

## 15. What Is Left To Do

In priority order before JEI submission:

1. **Replace synthetic tables with real AFND data.**  
   Follow `data/raw/SOURCES.md` procedure. Download TSVs manually from AFND. Re-run full pipeline. Update the numbers in `paper.tex` to match the real data output.

2. **Fix the duplicated Reproducibility subsection in `paper.tex`.**  
   Around line 132–148, the Reproducibility subsection appears twice. Delete the second one.

3. **Add HLA-C allele tables for all populations.**  
   The C locus TSVs are already in `data/raw/` (generated by `build_tables.py --loci A B C DRB1`). The sensitivity analysis in Figure 5a uses them. But the primary analysis only uses A, B, DRB1.

4. **Mentor review (2 rounds).**  
   Send the draft to a TJHSST alumni in hematology/bioinformatics, a Stanford iGEM contact, or cold-email authors of stealth-coating papers. Goal: sanity-check the model and catch factual errors.

5. **Submit to JEI.**  
   Submission is free. Target review time 2–4 months. The paper is nearly complete — the main remaining gap is real data.

6. **Optional / future work:**  
   - Full LD-aware haplotype model for all populations (requires per-population haplotype frequency tables)
   - Expand locus set to 10/10 (add HLA-C and HLA-DQB1) or 12/12 (add HLA-DPB1)
   - Allele-specific τ (some mismatches more immunogenic than others)
   - Integration with cost-effectiveness model

---

*End of Development Log.*
