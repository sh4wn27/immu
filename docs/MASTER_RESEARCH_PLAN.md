# Master Research Plan
## Biodegradable Stealth Polymer Coatings to Enable Universal HSC Grafts for Curative β-Thalassemia Transplantation

**PI / Lead Researcher:** Huanxuan (Shawn) Li  
**Affiliation:** Stanford iGEM Team, Stanford University  
**Plan Version:** 1.0 | April 2026  
**Target Duration:** 18 months (12-month core + 6-month extension/translation)  
**Total Budget Estimate:** $14,400 (core) + $8,000 (extension option)

---

## Part I — Research Synopsis

### The Problem
β-Thalassemia affects 60,000+ newborns annually with lifelong transfusion dependence. Allogeneic HSCT is the only cure, but:
- <30% of patients find a fully HLA-matched sibling donor
- Unrelated registries underserve ethnically diverse (especially Asian/Middle Eastern) populations
- Mismatched grafts trigger GvHD — 5-year survival <25% in severe cases
- Current immunosuppression causes infections, organ toxicity, and relapse risk

### The Core Innovation
Transiently coat donor CD34⁺ HSCs with biodegradable "stealth" polymers — either:
- **PEG-NHS (5 kDa):** NHS-ester covalent conjugation, well-characterized, anti-PEG antibody risk
- **PCB-NHS (6 kDa):** Zwitterionic poly(carboxybetaine methacrylate), hydrolyzes to benign osmolytes, no anti-polymer immunity

The ~20 nm corona physically masks donor MHC/HLA epitopes during the critical early alloresponse window, then hydrolyzes away to restore native CXCR4-mediated homing and self-renewal.

### The Three Aims
| Aim | Metric | Go/No-Go Threshold |
|-----|--------|--------------------|
| 1 — Coating Optimization | Surface coverage, viability, CXCR4 function | ≥80% coverage AND ≥90% viability |
| 2 — In Vitro Immune Evasion | T-cell proliferation, IFN-γ/IL-2, CFU potency, chemotaxis | ≥70% T-cell suppression AND ≥85% CFU |
| 3 — In Vivo Murine HSCT | Donor chimerism, GvHD score, polymer clearance, organ histology | ≥60% chimerism at wk4, ≤50% GvHD vs control, polymer cleared by day 42 |

---

## Part II — Master Timeline (18 Months)

```
Month:  1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18
Phase:  [─────── Phase 0+1 ───────][────── Phase 2 ──────][─Phase 3─][──── Phase 4 ────][── Phase 5 ──]
        Foundation & Synthesis      In Vitro               Optim.    In Vivo             Translation
```

### Phase 0: Foundation (Weeks 1–4, before lab work begins)
### Phase 1: Polymer Synthesis & Characterization (Months 1–3)
### Phase 2: In Vitro Studies (Months 4–6)
### Phase 3: Dose/Ratio Optimization Bridge (Months 7–9)
### Phase 4: In Vivo Murine Model (Months 10–12)
### Phase 5: Data Analysis, Manuscript & Translational Planning (Months 13–18)

---

## Part III — Phase-by-Phase Experimental Plan

---

### PHASE 0: Foundation (Weeks 1–4)

#### 0.1 Regulatory & Ethics Setup
- [ ] Submit IACUC protocol for BALB/c → C57BL/6 murine HSCT model (9 Gy TBI, n=8/group, humane endpoint criteria)
- [ ] Register under IRB for human cord-blood cell procurement (de-identified, pediatric donor units)
- [ ] Complete CITI training: blood-borne pathogens, animal handling, radiation safety
- [ ] Confirm biosafety level: BSL-2 for human primary cells; ABSL-2 for murine work
- [ ] Obtain DEA/radiation use authorization if not already in place (9 Gy irradiator)

#### 0.2 Lab Setup & Equipment Checklist
**Required — confirm in-kind access:**
- [ ] Flow cytometer with 488 nm + 647 nm lasers (FITC, APC, PE channels minimum)
- [ ] Biosafety cabinet (Class II, Type A2)
- [ ] −80°C freezer and liquid nitrogen cryostorage
- [ ] CO₂ incubator (37°C, 5% CO₂)
- [ ] IVIS imaging system (near-IR capable, 700–800 nm)
- [ ] DLS instrument (Zetasizer Nano or equivalent)
- [ ] FT-IR spectrometer (ATR attachment for amide-bond confirmation)
- [ ] Real-time PCR system (for chimerism quantification if flow is limited)
- [ ] Inverted microscope for CFU scoring

**Core facility reservations (schedule ahead):**
- [ ] DLS/FT-IR core — book Months 1–3 slots
- [ ] IVIS imaging — book Months 10–12 slots
- [ ] Irradiator (9 Gy, cesium or X-ray source) — schedule Month 10

#### 0.3 Reagent & Supply Procurement
**Polymers:**
- PEG-NHS ester, 5 kDa (Laysan Bio, NANOCS, or Sigma) — 500 mg initial
- PCB-NHS ester, 6 kDa (synthesized in-house via RAFT polymerization OR sourced from Biolinker/Sigma) — 200 mg initial
- Fluorescein-NHS (for labeled polymer batches) — 50 mg

**Cell sources:**
- Mouse: BALB/c donors (CD45.1), C57BL/6 recipients (CD45.2) — coordinate with vivarium, allow 2-week acclimation
- Human: De-identified cord-blood CD34⁺ units — procure from Stanford Blood Center or STEMCELL Technologies catalog cord blood

**Culture supplies:**
- MethoCult H4434 (human) and M3434 (mouse) for CFU assay
- CFSE (CellTrace) for T-cell proliferation assay
- SDF-1α (CXCL12) recombinant protein, carrier-free
- HEPES buffer pH 7.4, sterile-filtered
- HSC media: StemSpan SFEM II + CC100 cytokine cocktail (SCF, Flt3L, IL-3, IL-6)

**ELISA kits:**
- Mouse IFN-γ ELISA (R&D or BioLegend)
- Mouse IL-2 ELISA
- Human IFN-γ ELISA (for human cord-blood validation)

**Antibodies (flow cytometry panel):**
- Anti-CD34-PE (HSC marker)
- Anti-CXCR4-APC (homing receptor)
- Anti-CD45.1-FITC / Anti-CD45.2-APC (chimerism)
- Anti-CD3-PE (T cells for MLR readout)
- Anti-CD19, CD11b (lineage for chimerism panel)
- Live/Dead fixable viability dye

**Serum chemistry:**
- ALT, AST, BUN, Creatinine — multiplex or send-out assay
- Complement activation: CH50 or C3/C5a ELISA
- Anti-PEG IgM/IgG ELISA (Exosome Sciences or in-house)

#### 0.4 Power Analysis Confirmation
- Re-run G*Power for each assay:
  - MLR: n=3 biological replicates × 3 technical → 80% power, α=0.05 for 30% effect
  - In vivo: n=8 per group (4 groups: uncoated, PEG-coated, PCB-coated, syngeneic control) → 80% power, α=0.05
  - CFU: n=3 biological replicates, 500 cells/dish

#### 0.5 SOP Development
- Write and sign off SOPs for:
  - NHS-ester coating protocol (temperature, time, quench step)
  - HSC isolation (mouse BM flush, lineage depletion, CD34 enrichment)
  - MLR setup and readout
  - CFU plating and scoring
  - Murine HSCT procedure (irradiation, tail-vein injection, blood sampling)
  - GvHD scoring (0–10 composite: weight, posture, activity, fur, skin)

---

### PHASE 1: Polymer Synthesis & Characterization — Aim 1 (Months 1–3)

#### Goal: Achieve ≥80% surface coverage on CD34⁺ HSCs with ≥90% viability; confirm CXCR4 function intact

#### Experiment 1.1 — PCB Polymer Synthesis (if not sourced commercially)
**Protocol:**
1. RAFT polymerization of carboxybetaine methacrylate monomer
2. End-group modification to NHS-reactive ester (DCC/NHS coupling)
3. Characterize by GPC (target Mn ≈ 6 kDa, PDI <1.2)
4. ¹H NMR to confirm structure and NHS activation
5. Store as lyophilized powder at −20°C, <6 months shelf-life

**Milestones:**
- PCB-NHS batch ≥100 mg, purity >95% by NMR
- PEG-NHS batch validated (commercial, certificate of analysis reviewed)

#### Experiment 1.2 — Coating Protocol Optimization on Cell Lines (before primary HSCs)
**Rationale:** Optimize NHS-ester reaction conditions on a robust cell line (K562 or 32Dcl3) before using precious primary HSCs.

**Variables to screen (dose-response matrix):**
| Variable | Range | Steps |
|----------|-------|-------|
| Polymer concentration | 0.5, 1, 2, 5, 10 mg/mL | 5 |
| Incubation time | 15, 30, 60 min | 3 |
| Temperature | 4°C, RT (22°C) | 2 |
| pH | 7.0, 7.4, 8.0 | 3 |

**Readouts per condition:**
- Cell viability: Trypan blue exclusion (>90% threshold)
- Surface coverage: Flow cytometry with fluorescein-labeled polymer (% cells FITC+, MFI)
- Hydrodynamic diameter: DLS (expect +20–30 nm shift)
- Amide bond confirmation: FT-IR (1650 cm⁻¹ amide I peak)

**Deliverable:** Identify top 3 coating conditions for each polymer; proceed to primary HSCs

#### Experiment 1.3 — Primary HSC Coating (Mouse CD34⁺ / Lin⁻Sca1⁺cKit⁺)
**Cell isolation:**
- Harvest BM from BALB/c femurs and tibias via flush method
- Lineage depletion with magnetic beads (Miltenyi Lineage Cell Depletion Kit)
- Enrich LSK (Lin⁻Sca1⁺cKit⁺) by MACS or sort by FACS

**Coating:**
- Apply top 3 conditions from 1.2 to 1×10⁵ LSK cells per condition
- Quench unreacted NHS with 100 mM glycine, 5 min RT
- Wash 3× in PBS, resuspend in StemSpan for downstream assays

**Readouts:**
- Flow cytometry: viability (Live/Dead), FITC-polymer coverage, CXCR4-APC expression (quantitative MFI, not just %)
- CXCR4 functional assay (see 1.4 below)
- Colony-forming assay: plate 500 cells in MethoCult M3434, enumerate CFU-GEMM/GM/E at day 14

#### Experiment 1.4 — CXCR4 Functional Integrity (Transwell Chemotaxis)
**Setup:**
- 24-well transwell plate, 8 µm pore
- Lower chamber: 100 ng/mL SDF-1α in StemSpan
- Upper chamber: 1×10⁴ coated or uncoated HSCs
- Incubate 4 h at 37°C
- Count migrated cells in lower chamber by hemocytometer or flow

**Success criterion:** Coated HSC migration ≥80% of uncoated control (not in proposal but recommended stricter threshold since engraftment depends on CXCR4)

#### Experiment 1.5 — Degradation Kinetics
**Setup:**
- 50% human plasma at 37°C
- Sample polymer-coated beads or cells (if cell viability allows) at: 0, 6 h, 24 h, 72 h, 7 d, 14 d, 21 d, 28 d
- Readout: flow cytometry for residual FITC signal, DLS for particle size
- For PCB: confirm hydrolysis products are non-toxic (MTT assay on 3T3 fibroblasts with conditioned media)

**Key question:** Does PCB clear faster or slower than PEG? At what timepoint is the coat functionally gone?

#### Phase 1 Go/No-Go Criteria:
- ✅ **GO:** ≥80% coverage, ≥90% viability for at least ONE polymer at ONE dose
- ❌ **NO-GO trigger:** Both polymers fail viability at all doses → pivot to lipid-anchored stealth lipids (DSPE-PEG) or reversible click chemistry approach

---

### PHASE 2: In Vitro Immune Evasion & Stem-Cell Potency — Aim 2 (Months 4–6)

#### Goal: ≥70% reduction in T-cell proliferation and IFN-γ/IL-2; ≥85% CFU potency retained

#### Experiment 2.1 — Mixed Lymphocyte Reaction (MLR)
**Setup:**
- **Stimulators (responders):** Coated or uncoated BALB/c LSK HSCs (irradiated 30 Gy to prevent proliferation, prevent confounding from HSC divisions)
- **Responders:** CFSE-labeled C57BL/6 CD3⁺ T cells, isolated by negative selection
- **Effector:Target ratios:** 1:1, 1:5, 1:10 (E:T where E = T cell, T = HSC stimulator)
- Culture: 72 hours in RPMI + 10% FBS + antibiotics

**Readouts at 72 h:**
- T-cell proliferation: CFSE dilution by flow cytometry (% divided cells, proliferation index)
- IFN-γ: ELISA on supernatant (100 µL)
- IL-2: ELISA on supernatant (same plate)
- Optional: IL-17A, TNF-α multiplex if budget allows

**Controls:**
- Uncoated BALB/c HSC + C57BL/6 T cells (positive MLR, maximum alloresponse)
- Syngeneic BALB/c HSC + BALB/c T cells (negative MLR, baseline)
- Anti-CD3/CD28 bead stimulation (polyclonal proliferation control)
- Polymer alone (no cells) + T cells (polymer direct effect control)

**Statistical analysis:** One-way ANOVA + Tukey post-hoc; n=3 biological replicates

#### Experiment 2.2 — Multilineage Colony-Forming Assay (CFU)
**Setup:**
- 500 coated or uncoated HSCs per 35-mm dish in MethoCult M3434
- Triplicate dishes per condition
- Enumerate at day 14:
  - CFU-GEMM (granulocyte-erythroid-macrophage-megakaryocyte): darkest, densest
  - CFU-GM (granulocyte-macrophage): spread colonies
  - BFU-E (erythroid burst): red/orange hemoglobinized

**Success criterion:** ≥85% total CFU vs uncoated control  
**Additional readout:** Colony morphology photo-documentation for size/shape comparison

#### Experiment 2.3 — Serial Colony Replating (Self-Renewal Test)
**Rationale:** Not in original proposal but critical — polymer coating must not impair self-renewal capacity.
- Re-plate primary colonies in fresh MethoCult after 14 days
- Count secondary CFUs at day 28
- Compare coated vs uncoated HSC serial replating efficiency

#### Experiment 2.4 — Human CD34⁺ Cord Blood Validation (Parallel Track)
**Why:** The proposal mentions human cord-blood cells for validation; this de-risks the translatability of mouse data.
- Procure de-identified human cord-blood CD34⁺ cells (IRB-approved)
- Apply optimized coating conditions (from Phase 1)
- Run human MLR: coat human CD34⁺ cells, stimulate HLA-mismatched allogeneic PBMCs
- CFU in MethoCult H4434
- CXCR4 chemotaxis toward SDF-1α

**Note:** Human data strengthens manuscript significantly and is required for IND-enabling studies later.

#### Experiment 2.5 — Anti-PEG Antibody Screening
**Rationale:** Yang et al. (2024) showed >40% seroprevalence of anti-PEG IgM/IgG in healthy donors. If any donor serum pre-coated with anti-PEG antibodies shows accelerated T-cell activation against PEG-coated HSCs, the PEG arm must be deprioritized.
- Screen serum from 10 healthy donors for anti-PEG IgM/IgG
- Incubate anti-PEG+ serum with PEG-coated HSCs, then run abbreviated MLR
- If anti-PEG accelerates alloresponse: **drop PEG arm entirely**, proceed with PCB only

#### Phase 2 Go/No-Go Criteria:
- ✅ **GO:** ≥70% T-cell suppression AND ≥85% CFU for at least ONE polymer
- ❌ **NO-GO — polymer specific:** If PEG fails anti-PEG screen OR fails MLR → PCB-only arm forward
- ❌ **NO-GO — full stop:** Both polymers fail MLR AND CFU → Pivot to lipid-anchor or click-chemistry approach

---

### PHASE 3: Dose & Ratio Optimization Bridge (Months 7–9)

#### Goal: Identify the optimal polymer concentration (0.5–5 mg/mL) and HSC dose (0.5–2×10⁶ cells) for in vivo experiments

#### Experiment 3.1 — Dose-Response Refinement
**Matrix:**
| Polymer Concentration | 0.5 mg/mL | 1 mg/mL | 2 mg/mL | 5 mg/mL |
|----------------------|-----------|---------|---------|---------|
| MLR suppression | | | | |
| CFU retention | | | | |
| CXCR4 function | | | | |

- Use the best conditions from Phase 1–2 as reference point
- Select **single optimal concentration** for Phase 4

#### Experiment 3.2 — HSC Dose Titration (Pilot In Vivo)
**Pilot study (n=3/group, not powered for statistical significance, exploratory only):**
- Lethally irradiate C57BL/6 mice (9 Gy)
- Inject: 0.5×10⁶, 1×10⁶, or 2×10⁶ BALB/c HSCs (uncoated, to set engraftment baseline)
- Monitor survival and chimerism at day 14, 28
- Select dose achieving ≥60% chimerism for Phase 4 definitive study

#### Experiment 3.3 — Polymer Clearance Pilot (IVIS)
- Label optimized PCB and PEG batches with NHS-Cy7 near-IR dye
- Inject n=2 mice per polymer, track IVIS signal at: days 1, 3, 7, 14, 21, 28, 42
- Confirm clearance kinetics; verify signal is gone by day 42

---

### PHASE 4: Definitive In Vivo Murine HSCT Model — Aim 3 (Months 10–12)

#### Goal: ≥60% donor chimerism by week 4, ≤50% GvHD score vs uncoated; polymer cleared by day 42; normal organ histology

#### Study Design

**Groups (n=8 per group, 32 mice total):**
| Group | Graft | Expected Outcome |
|-------|-------|-----------------|
| A: Syngeneic control | BALB/c HSC → BALB/c (no MHC mismatch) | High chimerism, no GvHD |
| B: Allogeneic uncoated | BALB/c HSC → C57BL/6 | High GvHD, poor/moderate chimerism |
| C: PEG-coated allogeneic | PEG-BALB/c HSC → C57BL/6 | Reduced GvHD, maintained chimerism |
| D: PCB-coated allogeneic | PCB-BALB/c HSC → C57BL/6 | Reduced GvHD, maintained chimerism |

**Randomization:** Mice block-randomized by weight; transplant done in 2 cohorts of 16 (reduces irradiator scheduling pressure)  
**Blinding:** GvHD scorer blinded to group assignment

#### Experiment 4.1 — Recipient Conditioning
- C57BL/6 mice, 8 weeks, male (or female, consistent within study)
- 9 Gy total-body irradiation (split 4.5 Gy × 2, 4 h apart to reduce GI toxicity, OR single 9 Gy — confirm with radiation core)
- Sterilize water and food 48 h pre-TBI; antibiotics in water (trimethoprim-sulfamethoxazole) for 4 weeks post-transplant
- Transplant within 24 h of irradiation

#### Experiment 4.2 — Graft Preparation & Infusion
- Harvest BALB/c BM on day of transplant (fresh, not frozen)
- Coat with optimal polymer conditions (from Phase 3)
- Final product: 1×10⁶ HSCs in 200 µL PBS
- Quality control pre-infusion: viability ≥90%, polymer coverage ≥80% (spot-check on 1000 cells by flow)
- IV injection via tail vein (warm mouse in 37°C water 2 min prior)

#### Experiment 4.3 — Longitudinal Monitoring (42 Days)

**Weekly blood draws (submandibular vein, 50 µL, alternate sides):**
- Chimerism panel: Anti-CD45.1-FITC / Anti-CD45.2-APC / Anti-CD3 / Anti-CD11b / Anti-CD19
- CBC (optional, terminal or biweekly if volume allows)

**Daily scoring (same observer, blinded):**
- GvHD composite score (0–10):
  - Weight loss: 0 (none) – 3 (>25%)
  - Posture: 0 (normal) – 2 (hunched)
  - Activity: 0 (normal) – 2 (reduced)
  - Fur texture: 0 (normal) – 2 (ruffled/piloerect)
  - Skin integrity: 0 (normal) – 1 (lesions)
- Humane endpoints: weight loss >20%, GvHD score ≥8, severe respiratory distress

**IVIS imaging (Cy7-labeled polymer cohort, n=4 extra mice):**
- Days: 1, 3, 7, 14, 21, 28, 42
- Quantify radiant efficiency (photons/sec/cm²/sr per µW/cm²) in liver, spleen, BM cavities
- Report as % initial signal remaining

**Day 42 Terminal Assessment:**
- Blood: Serum ALT, AST, BUN, Creatinine, complement activation (C3a/C5a), anti-PEG IgM/IgG
- Tissues harvested: liver, spleen, kidney, lung, gut (small intestine, colon), skin, BM
- Fix in 10% NBF → paraffin embedding → H&E staining
- Pathology scoring (blinded): liver periportal inflammation, gut villous blunting, lung infiltrates, BM cellularity

**Spleen for flow at terminal:**
- Donor vs host T-cell ratio
- Treg quantification (CD4⁺CD25⁺FoxP3⁺)
- NK and NKT cells
- Donor myeloid reconstitution

#### Statistics (Phase 4)
- Chimerism over time: Repeated-measures ANOVA, Bonferroni correction for multiple timepoints
- GvHD score: Non-parametric (Mann-Whitney U) due to ordinal nature of scoring
- Survival: Kaplan-Meier, log-rank test
- Organ histology: Blind scoring, Fisher's exact for categorical outcomes
- All analyses: α = 0.05, two-tailed

#### Phase 4 Go/No-Go Criteria:
- ✅ **PRIMARY SUCCESS:** ≥60% chimerism at week 4 AND ≤50% GvHD score vs control AND polymer signal gone by day 42
- ✅ **PARTIAL SUCCESS:** Chimerism achieved but GvHD reduction <50% → still publishable as proof-of-concept with mechanistic explanation
- ❌ **FAILURE MODE:** <20% chimerism in coated groups → investigate if CXCR4 impaired in vivo (add Plerixafor rescue arm in extension)

---

### PHASE 5: Data Analysis, Manuscript & Translational Planning (Months 13–18)

#### 5.1 — Data Compilation & Statistical Analysis
- Finalize all statistical analyses in R or GraphPad Prism
- Generate publication-quality figures:
  - Figure 1: Polymer synthesis schematic + DLS/FT-IR characterization + degradation kinetics
  - Figure 2: Coating optimization — concentration vs coverage vs viability heatmap
  - Figure 3: MLR data — CFSE histograms, proliferation index, IFN-γ/IL-2 bar graphs
  - Figure 4: CFU data — colony photos + quantification + chemotaxis
  - Figure 5: In vivo — chimerism line plot, GvHD score curve, Kaplan-Meier, IVIS clearance
  - Figure 6: Histopathology panel — H&E images, scoring bar graphs, serum chemistry
  - Supplemental: Human CD34⁺ validation data, anti-PEG antibody screen

#### 5.2 — Manuscript Drafting
**Target journal (in order of preference):**
1. *Nature Biomedical Engineering* (IF ~29, if in vivo data is clean)
2. *Biomaterials* (IF ~14, polymer + cell biology focus)
3. *Blood* (IF ~21, hematology focus)
4. *ACS Nano* (IF ~18, if materials characterization is strong)

**Manuscript structure:**
- Abstract (250 words)
- Introduction (background, gap, hypothesis)
- Results (Aims 1–3, organized by figure)
- Discussion (mechanism interpretation, limitations, translational path)
- Methods (full protocol reproducibility)
- Data availability statement
- Code availability (statistical analysis scripts on GitHub)

**Timeline for manuscript:**
- Month 13: Data lock, begin figure assembly
- Month 14: First draft complete
- Month 15: Internal review (PI, iGEM team, collaborators)
- Month 16: Submission

#### 5.3 — Conference Presentations
- **iGEM Giant Jamboree (October):** Present preliminary Phase 1–2 data as poster; aim for Best New Application award
- **ASH (American Society of Hematology, December):** Submit abstract if Phase 4 data is available; oral or poster presentation
- **BMES (Biomedical Engineering Society, Fall):** Materials/cellular engineering track

#### 5.4 — Translational Roadmap (18-month Extension)
If core study succeeds, the next phase targets:

**Step 1 — Scale-up validation (Month 13–15):**
- Optimize coating for GMP-grade reagents (endotoxin-tested, clinical-grade PCB if available)
- Validate on human CD34⁺ cord-blood cells (n=5 donors, full MLR + CFU + CXCR4 panel)

**Step 2 — Humanized mouse model (Month 15–18):**
- NSG mice engrafted with human CD34⁺ cells (hu-NSG model)
- Test coated human HSCs in MHC-mismatched setting (NSG-SGM3 with human cytokines)
- Primary endpoint: human chimerism (CD45⁺ in PB), GvHD markers (human CD3⁺ T cells)

**Step 3 — IND-enabling studies (18+ months, separate funding):**
- Good Laboratory Practice (GLP) toxicology: PCB polymer at 10× clinical dose in rodent + rabbit (28-day repeat dose)
- Genotoxicity: Ames test + in vitro micronucleus
- Biodistribution: ¹⁴C-labeled PCB in rats (full mass balance)
- GMP manufacturing development for PCB-NHS ester

---

## Part IV — Risk Management & Contingency Plans

| Risk | Probability | Impact | Contingency |
|------|-------------|--------|-------------|
| PEG-NHS coating impairs CXCR4 (H2S4 crosslinker over-reacts) | Medium | High | Switch to shorter PEG (2 kDa) or mPEG-Maleimide for thiol-directed conjugation; or proceed PCB-only |
| Anti-PEG IgM detected in serum screen | High (>40% seroprevalence) | Medium | Pre-planned: Drop PEG arm, PCB-only |
| In vivo chimerism <20% in coated groups | Medium | High | Add Plerixafor (AMD3100) co-treatment to mobilize and enhance CXCR4-independent homing; assess if coating dose needs reduction day-of-transplant |
| GvHD still severe despite coating | Medium | High | Combine with low-dose rapamycin (sub-immunosuppressive) + coated graft; test whether partial masking + mild IST synergizes |
| PCB synthesis fails / low yield | Low | Medium | Switch to commercially available PCB-NHS from Biolinker or synthesize via atom-transfer radical polymerization (ATRP) instead of RAFT |
| Mouse irradiator booking blocked | Low | Low | Coordinate with radiation core 8 weeks ahead; schedule backup irradiator at SLAC/shared facility |
| Polymer clearance incomplete by day 42 | Low | High | Extend observation to day 60; assess if residual signal is cell debris vs intact polymer; adjust PCB hydrolysis by modifying ester linkage density |
| Human cord blood CD34⁺ procurement delayed | Medium | Low | Use frozen STEMCELL Technologies catalog cord blood as backup; does not affect primary mouse aims |

---

## Part V — Budget Breakdown (12-Month Core)

| Category | Items | Cost |
|----------|-------|------|
| **Polymers & Chemistry** | PEG-NHS (5 kDa), PCB-NHS (6 kDa), fluorescein-NHS, Cy7-NHS, HEPES, glycine | $1,200 |
| **Cell Culture & Assays** | MethoCult M3434+H4434, StemSpan SFEM II, CC100, recomb SDF-1α, FBS, antibiotics | $2,200 |
| **Cytokine Assays** | IFN-γ ELISA ×6, IL-2 ELISA ×6, anti-PEG IgM/IgG ELISA ×2 | $1,100 |
| **Flow Cytometry Reagents** | 8-color antibody panel, CFSE, Live/Dead dye, compensation beads | $1,300 |
| **Core Facility Fees** | DLS (12h), FT-IR (6h), IVIS imaging (10 sessions) | $2,000 |
| **Animals** | 40 mice (BALB/c + C57BL/6) purchase + 42-day housing @ $1.50/mouse/day | $2,880 |
| **Consumables** | Pipettes, plates, transwell inserts, syringes, tubes, gloves, BSC supplies | $1,000 |
| **Serum Chemistry** | ALT/AST/BUN/Cr, complement panels, CBC sends (×32 terminal samples) | $500 |
| **Histopathology** | Paraffin embedding, H&E sectioning (3 sections × 32 mice × 7 organs) | $1,000 |
| **20% Contingency** | — | $2,400 (omit if tight) |
| **TOTAL** | | **$14,180** |

**In-kind (confirmed needed):**
- Flow cytometer, BSC, incubators, −80°C storage, irradiator (departmental)
- Statistical software (GraphPad Prism via Stanford site license)

---

## Part VI — Key Collaborators & Expertise Gaps

| Expertise Needed | Suggested Source |
|-----------------|-----------------|
| Polymer synthesis (PCB RAFT) | Stanford Chemistry — Zhenan Bao lab (polymer materials) |
| HSC biology & murine HSCT | Stanford Stem Cell Biology — Weissman lab or Bhatt lab |
| GvHD pathology scoring | Stanford Hematology / Veterinary Pathology |
| IVIS & in vivo imaging | Canary Center at Stanford (preclinical imaging) |
| Biostatistics | Stanford Quantitative Sciences Unit (free consultations for students) |
| GMP scale-up advice | Stanford SPARK translational program |

---

## Part VII — Success Metrics & Publication Readiness Checklist

### Minimum Publishable Unit (MPU):
- [ ] Phase 1 complete: coating characterized by DLS, FT-IR, flow; degradation kinetics in plasma
- [ ] Phase 2 complete: MLR (≥70% suppression), CFU (≥85%), CXCR4 chemotaxis — triplicate biological replicates
- [ ] Phase 4 complete: n=8/group in vivo, chimerism + GvHD + histopathology + polymer clearance

### Upgraded Publication (if human data included):
- [ ] Human cord-blood CD34⁺ coating and MLR data
- [ ] Anti-PEG seroprevalence screen (n=10 donors)
- [ ] Mechanistic data: T-cell subset analysis, Treg induction, donor myeloid reconstitution

### Data Integrity:
- [ ] All raw data in electronic lab notebook (benchling or Labarchives)
- [ ] Flow cytometry: FCS files archived, gating strategy documented
- [ ] Statistical code in R/Python on GitHub (public repo at submission)
- [ ] ARRIVE 2.0 guidelines followed for in vivo reporting
- [ ] Cell line authentication (STR profiling if human lines used)

---

## Part VIII — Personal Research Narrative

This research is directly motivated by personal experience with transfusion-dependent β-thalassemia. The proposal's closing remarks describe waiting for HLA-matched donors, financial strain on families, and friends who did not receive the transplant needed. That motivation gives this project unusual focus and credibility.

**For grant applications and presentations, emphasize:**
- The 60,000 newborns per year statistic — majority in low-resource settings where HLA registries are sparse
- Cost differential: $40,000/year in the US vs $5,000–10,000 in India — the populations most affected can least afford alternatives
- The off-the-shelf potential of a coating-based approach: no genetic modification of cells, no permanent immunosuppression, applicable to existing HSC banking infrastructure
- The personal story is a strength — rare to have a PI who is also a patient

---

*Last updated: April 2026 | Version 1.0*  
*Next review: After Phase 1 go/no-go decision (Month 3)*
