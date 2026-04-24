# Project Plan — HLA Equity Simulation Paper

**Title (working):** Modeling the equity impact of partial HLA mismatch tolerance via biodegradable stealth coatings: a population-genetics simulation.

**Author:** Huanxuan (Shawn) Li — TJHSST.  
**Target venue:** Journal of Emerging Investigators (JEI). Backup: National High School Journal of Science (NHSJS).  
**Target length:** 4000–5000 words + 4–6 figures.  
**Estimated calendar time:** 3–4 months of part-time work.

---

## 1. Research question

How much does partial HLA mismatch tolerance — of the kind enabled by transient biodegradable stealth-polymer coatings on donor HSCs — expand the effective matched-donor pool, and does the expansion disproportionately help ethnically underserved patients?

## 2. Why this matters

Allogeneic HSCT is the only curative therapy for β-thalassemia, but <30% of patients find a fully HLA-matched sibling donor and unrelated registries underserve non-European ancestries. Stealth-coating technologies that transiently mask HLA epitopes could turn some "mismatched" donors into functionally acceptable ones. Nobody has quantified how much this would actually change the donor-pool equation for real populations. This paper does.

## 3. Hypothesis

H1: Coating-enabled tolerance of 1–2 locus mismatches increases match probability for every population modeled.  
H2: The absolute increase is larger for populations currently underserved by registries, so the Europe-to-other-population disparity ratio shrinks under coating.

## 4. Methods — one paragraph summary

Download HLA-A, HLA-B, HLA-DRB1 allele frequencies from the Allele Frequency Net Database (AFND) for 5–8 populations. Simulate 100,000 random patient–donor pairs drawn from each population. For each pair, count locus matches at high-resolution allele level. Compute the probability of meeting match thresholds at 6/6 (strict, three loci × two alleles), 5/6, and 4/6. Layer a "coating tolerance parameter" τ derived from published MLR suppression data — τ represents the number of locus mismatches the coating functionally masks. Compute effective pool expansion and the disparity ratio (max population match prob / min population match prob) with and without coating.

## 5. Deliverables

| # | Deliverable | Owner | Due |
|---|-------------|-------|-----|
| D1 | Repo skeleton + `CLAUDE.md` (this file) committed | Claude | Done |
| D2 | `src/hla_sim/fetch_afnd.py` — pull + cache AFND allele frequencies | Shawn + Claude | Week 1 |
| D3 | `src/hla_sim/simulate.py` — Monte-Carlo matcher | Shawn + Claude | Week 2 |
| D4 | Pilot notebook — one population pair, 6/6 match probability | Shawn | Week 2 |
| D5 | Coating tolerance model + disparity ratio calc | Shawn + Claude | Week 3 |
| D6 | Full results across all populations | Shawn | Week 4 |
| D7 | Figures 1–5 | Shawn | Week 5–6 |
| D8 | First manuscript draft | Shawn | Week 8 |
| D9 | Mentor review loop (2 rounds) | Shawn + mentor | Weeks 9–11 |
| D10 | JEI submission | Shawn | Week 12 |

## 6. Target figure set

- **Figure 1 — Schematic.** Concept diagram: HLA mismatch → GvHD; coating masks HLA → partial tolerance; what the simulation models.
- **Figure 2 — Population allele diversity.** Heatmap or Shannon entropy bar chart of HLA-A/B/DRB1 across modeled populations (validates the data and motivates the problem).
- **Figure 3 — Match probability without coating.** Stacked bar chart of 6/6, 5/6, 4/6 match probability by population.
- **Figure 4 — Match probability under coating tolerance τ.** Same populations, same thresholds, showing the pool expansion effect.
- **Figure 5 — Disparity ratio reduction.** The headline chart — ratio (European match prob / underserved match prob) across τ values. Shows equity improvement.
- **Figure 6 (optional) — Sensitivity analysis.** How much does the conclusion depend on assumed τ? On HLA loci modeled (adding C, DQB1)? On population-size assumptions?

## 7. Scope boundaries

**In scope:**
- Three classical HLA loci (A, B, DRB1) at 2-field (4-digit) resolution.
- 5–8 populations covering European, African, East Asian, South Asian, Middle Eastern, Hispanic, and one underrepresented group.
- High-resolution matching (no serological approximations).
- Simple Hardy-Weinberg allele sampling; linkage disequilibrium (LD) between loci discussed as a limitation, not modeled.
- Coating tolerance as a single scalar parameter τ over plausible range 0–2 locus mismatches.

**Out of scope (may be noted as future work):**
- Full haplotype LD modeling (requires per-population haplotype data, not all populations have it).
- HLA-C, HLA-DQB1, HLA-DPB1 (could extend easily; flagged in discussion).
- Minor histocompatibility antigens.
- GvHD-risk modeling beyond match probability.
- Real-world donor registry dynamics (search time, logistics).

## 8. Data source plan

- **Primary:** Allele Frequency Net Database (http://www.allelefrequencies.net) — downloadable CSV/TSV by population and locus. Cite their 2020 paper (González-Galarza et al., *NAR* 2020).
- **Secondary (if needed for validation):** published NMDP registry frequency tables.
- **License note:** AFND is freely available for academic use; cite and acknowledge.
- All raw data files land in `data/raw/` with the URL, access date, and SHA-256 in the header of a `data/raw/SOURCES.md`.

## 9. Statistical approach

- Monte-Carlo simulation with N ≥ 100,000 pair samples per condition (bootstrap SE on match probability ≤ 0.2 percentage points).
- 95% CIs via bootstrap over sampled pairs.
- Disparity ratio uncertainty via paired bootstrap (same RNG seed across populations to preserve correlations).
- No null-hypothesis testing needed; paper reports effect sizes and CIs.
- Seed set via `numpy.random.default_rng(20260424)`; seed declared at top of every script.

## 10. Publication strategy

- **Primary target:** Journal of Emerging Investigators (JEI) — Harvard-run, peer-reviewed, specifically for middle/HS students. Reviews are typically 2–4 months. Free.
- **Backup:** NHSJS — faster turnaround, slightly less prestige.
- **Stretch:** co-author with a Stanford/university mentor into *Bone Marrow Transplantation Letters* or *Biomaterials Science* — would need faculty buy-in.

## 11. Risks and mitigations

| Risk | Mitigation |
|------|------------|
| AFND data structure changes / site goes down | Cache all raw downloads locally; use Wayback Machine as backup source. |
| Simulation results are counter to hypothesis (coating doesn't help much) | Still publishable as a null result; adjust framing to "here's the quantitative ceiling of what coating can do". |
| Overreach on what τ means biologically | Be explicit in Methods and Discussion — τ is a modeling abstraction, not a measured quantity. Cite range from literature. |
| Mentor unavailable | Submit to NHSJS without mentor; reviewers there are more forgiving. |
| Author loses momentum | Short weekly milestones (see §5 table). Each week has one concrete artifact. |

## 12. Mentor search — parallel track

Start reaching out to:
- Stanford iGEM alumni (network).
- TJHSST alumni in hematology / bioinformatics.
- Authors of recent stealth-coating papers (cold-email with a one-paragraph pitch; ~10% response rate is realistic).
- NMDP / Be The Match science staff (they publish on exactly this equity question).

A 30-minute mentor call once a month is enough. Goals: (a) sanity-check the model, (b) catch factual errors, (c) optional co-authorship.

## 13. Open questions for Shawn

- Which 5–8 populations do you want modeled? Default suggestion: European (CEU), Han Chinese, African American, South Asian, Middle Eastern (e.g., Saudi/Emirati), Hispanic (Mexican American). Tell me if you want others.
- Do you have a mentor in mind, or should finding one be the first parallel task?
- Are you OK with Python? (Main alternative would be R; Python is more common in bioinformatics these days.)
- Comfort level with Git/GitHub? If new, we'll set up with clear commits.
