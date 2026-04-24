# Project: HLA Equity Simulation

A population-genetics Monte-Carlo simulation quantifying how biodegradable stealth-polymer HSC coatings — which enable partial HLA mismatch tolerance — would expand the donor pool for stem-cell transplantation, with a focus on ethnic equity.

**Author:** Huanxuan (Shawn) Li — TJHSST  
**Target publication:** Journal of Emerging Investigators (JEI) or NHSJS  
**Status:** active — project skeleton phase

---

## Research question

How much does partial HLA mismatch tolerance (enabled by stealth-polymer coating of donor HSCs) expand the match probability for patients of different ethnic ancestries, and does it reduce the historic equity gap in donor availability?

## Core claim the paper will make

Using public HLA allele-frequency data (Allele Frequency Net Database, AFND), a stealth-coated HSC graft tolerating 1–2 locus mismatches would disproportionately benefit non-European patients, reducing the effective-match disparity ratio by X%.

## What this repo contains

```
.
├── docs/
│   ├── PROJECT_PLAN.md           — current plan (publication-focused)
│   ├── MASTER_RESEARCH_PLAN.md   — original bench-research plan (historical context)
│   ├── manuscript/               — draft paper
│   └── _archive/                 — prior Phase 0/1 wet-lab scaffolding (not active)
├── src/
│   ├── hla_sim/                  — Python simulation package
│   └── _archive/                 — prior R analysis scaffold (not active)
├── data/                         — raw + processed HLA allele frequency files
├── notebooks/                    — exploratory analysis
└── tests/                        — unit tests for the simulator
```

## Tech stack

- **Python 3.11+** (single language, keep it simple)
- `numpy`, `pandas`, `scipy.stats`, `matplotlib`, `seaborn`
- `requests` + `beautifulsoup4` (AFND data fetching)
- `pytest` for tests
- `jupyterlab` for exploratory notebooks
- GitHub repo for code + data provenance

## Working rules for this project

### Scope discipline (important — project has a history of scope creep)
- **Publication-focused.** If a task doesn't move the paper forward, defer it.
- **No wet-lab work.** Author has no lab access. Do not write IACUC/IRB/procurement docs. Archived material stays in `docs/_archive/`.
- **No giant extensions.** Skip molecular dynamics, ML models, web dashboards unless explicitly approved.
- **One dataset.** AFND is primary. Only add data sources if the paper demands it.

### Code style
- Simple, readable Python. This is a student project, not a production system.
- No async, no classes unless they clearly pay off. Functions + dataclasses.
- Docstrings on every public function. Typing hints where they help.
- Tests for the simulator core (match counting, probability calcs); snapshot tests for figures OK.

### Reproducibility (required for publication)
- Pin all dependencies in `requirements.txt` with versions.
- Seed every RNG.
- Raw data files committed to `data/raw/` with source URL + access date in header.
- Every figure in the paper regenerable by one script: `python -m hla_sim.make_figures`.

### Writing rules
- Paper drafts in `docs/manuscript/` as plain markdown (convert to DOCX at submission).
- Cite everything. Use a `references.bib` from day 1.
- When in doubt, JEI style: first-person plural ("we"), past tense for methods/results.

### File organization (unchanged from global rules)
- No working files in root.
- `/src`, `/docs`, `/data`, `/tests`, `/notebooks` only.

## What to do first (next actionable work)

1. Write `docs/PROJECT_PLAN.md` with milestones, timeline, and figure list
2. Write `src/hla_sim/fetch_afnd.py` — data fetcher for 5–8 target populations
3. Write `src/hla_sim/simulate.py` — Monte-Carlo donor-recipient matcher
4. Pilot analysis on one population pair (European vs. a chosen underserved group)
5. Refine model: add coating-tolerance parameter, compute disparity ratio

## Non-goals

- Not building a web app.
- Not running molecular simulations.
- Not writing a literature review (the simulation paper has a short Intro, not a full review).
- Not implementing novel statistical methods — use standard approaches.
