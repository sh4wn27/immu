# Standard Operating Procedures — Phase 0 Sign-Off Package

All SOPs below must be reviewed and signed by PI + bench operator before first use. Version-control every revision. Each SOP numbered per `MASTER_RESEARCH_PLAN.md` §0.5.

---

## SOP-01 — NHS-Ester Stealth Polymer Coating of HSCs

**Purpose:** Covalently attach PEG-NHS (5 kDa) or PCB-NHS (6 kDa) to surface amines of CD34⁺ HSCs with ≥80% coverage and ≥90% viability.

**Scope:** Primary murine LSK (Lin⁻Sca1⁺cKit⁺) cells and human CD34⁺ cord-blood cells.

**Materials:**
- Lyophilized polymer-NHS (stored −20 °C, desiccated, used within 6 months)
- HEPES buffer, 20 mM, pH 7.4, sterile-filtered 0.22 µm
- 100 mM glycine quench solution, pH 8.0
- PBS (Ca²⁺/Mg²⁺-free), sterile
- StemSpan SFEM II + CC100 cocktail (post-wash resuspension)

**Procedure:**
1. Pre-warm HEPES buffer to reaction temperature (RT or 4 °C per condition).
2. Immediately before use, dissolve polymer-NHS in HEPES to 2× target working concentration (0.5–10 mg/mL). Discard unused stock after 15 min — NHS hydrolyzes rapidly in aqueous solution.
3. Pellet 1×10⁵–1×10⁶ cells at 300 g × 5 min. Aspirate supernatant.
4. Resuspend cells in pre-warmed HEPES (half reaction volume).
5. Add equal volume polymer-NHS stock. Final concentration = working target. Mix by gentle pipetting.
6. Incubate for defined time (15 / 30 / 60 min) at defined temperature (4 °C or 22 °C). Do NOT vortex.
7. Quench: add 100 mM glycine to 10 mM final. Incubate 5 min at RT.
8. Wash 3× in cold PBS, 300 g × 5 min each. Transfer to fresh tube after wash 2 to eliminate polymer carry-over.
9. Resuspend in StemSpan SFEM II + CC100 at downstream assay concentration.
10. QC immediately: viability (Live/Dead flow), coverage (FITC-polymer flow, MFI), record in run log.

**Acceptance criteria:** Viability ≥90%, FITC⁺ ≥80%, CXCR4 MFI within 70% of uncoated baseline.

**Critical control points:**
- Polymer stock freshness (<15 min after reconstitution)
- pH must stay 7.0–8.0 during reaction (NHS reactivity window)
- Glycine quench is mandatory; residual NHS will react with media amines

**Waste:** Polymer stock + supernatants → biohazard liquid waste. Glycine-containing rinses → standard aqueous.

---

## SOP-02 — HSC Isolation from Murine Bone Marrow

**Purpose:** Yield ≥5×10⁵ LSK (Lin⁻Sca1⁺cKit⁺) cells per BALB/c donor at >95% purity for coating and transplant studies.

**Materials:**
- BALB/c donor mice (8–12 wk, sex-matched per study)
- 70% ethanol spray
- Dissection kit (sterile, separate per mouse)
- 25 G needle + 3 mL syringe with MACS buffer (PBS + 0.5% BSA + 2 mM EDTA)
- 70 µm cell strainer
- Miltenyi Lineage Cell Depletion Kit (mouse)
- MACS LS columns + QuadroMACS separator
- Anti-Sca1-PE, anti-cKit-APC, Live/Dead dye
- FACS sorter or MACS Sca1/cKit sequential enrichment

**Procedure:**
1. Euthanize mouse per IACUC (CO₂ + cervical dislocation confirmation). Record time of death.
2. Spray with 70% ethanol. Open skin and remove hind limbs intact.
3. Clean muscle from femurs and tibias using sterile gauze. Keep bones on ice in MACS buffer.
4. Flush bones: insert 25 G needle through epiphysis, flush with 5 mL MACS buffer into 50 mL tube. Alternative: crush bones in mortar, filter.
5. Pass through 70 µm strainer. Lyse RBCs (ACK buffer, 3 min RT). Wash 2× in MACS buffer.
6. Count on hemocytometer. Expect 2–5×10⁷ nucleated cells per mouse.
7. Lineage depletion per Miltenyi kit. Collect Lin⁻ flow-through.
8. Stain Lin⁻ fraction: Sca1-PE, cKit-APC, Live/Dead. Incubate 20 min, 4 °C, dark. Wash.
9. Sort live Sca1⁺cKit⁺ cells on FACS (LSK gate) into StemSpan SFEM II + CC100. Target purity ≥95%.
10. Count sorted cells. Rest 1 h at 37 °C before coating or plating.

**Acceptance criteria:** ≥5×10⁵ LSK/mouse, ≥95% purity, ≥95% viability at sort.

**Failure modes:** BM flush clotting → add EDTA, keep cold. Low LSK yield → confirm mouse age/strain, check cytokine activity.

---

## SOP-03 — Mixed Lymphocyte Reaction (MLR)

**Purpose:** Quantify allogeneic T-cell activation against coated vs uncoated BALB/c stimulators.

**Materials:**
- BALB/c LSK HSCs (stimulators), irradiated 30 Gy immediately before setup
- C57BL/6 splenic CD3⁺ T cells (responders), negative-selected (Miltenyi Pan T Cell kit)
- CellTrace CFSE, 5 µM final, labeled per manufacturer
- RPMI 1640 + 10% heat-inactivated FBS + 1% penicillin/streptomycin + 50 µM 2-ME
- 96-well U-bottom plates
- Anti-CD3-PE, anti-CD8-FITC, anti-CD4-PerCP, Live/Dead (flow panel)
- IFN-γ and IL-2 ELISA kits (BioLegend or R&D)

**Procedure:**
1. Label C57BL/6 T cells with CFSE per kit. Count, resuspend to 1×10⁶/mL.
2. Plate responders: 1×10⁵ T cells per well in 100 µL.
3. Add irradiated stimulators at E:T = 1:1, 1:5, 1:10 (T:HSC) in 100 µL.
4. Controls per plate: responders alone, polyclonal (anti-CD3/CD28 Dynabeads 1:1), syngeneic BALB/c T responders + BALB/c stimulators, polymer-only + responders.
5. Incubate 72 h at 37 °C, 5% CO₂. Do not disturb.
6. Harvest 100 µL supernatant per well → freeze −80 °C for ELISA.
7. Wash cells in FACS buffer. Stain surface panel + Live/Dead. Fix in 1% PFA.
8. Acquire on flow cytometer. Gate: Live → CD3⁺ → CFSE dilution. Compute proliferation index (FlowJo Proliferation Platform).
9. Run IFN-γ and IL-2 ELISAs per kit on thawed supernatants.

**Acceptance criteria (per run):** Polyclonal control shows ≥5 divisions; allogeneic uncoated shows ≥50% divided; syngeneic <5% divided.

**Statistical analysis:** n=3 biological replicates. One-way ANOVA + Tukey post-hoc, α=0.05.

---

## SOP-04 — Colony-Forming Unit (CFU) Assay

**Purpose:** Measure multilineage potency retention (≥85% of uncoated control) post-coating.

**Materials:**
- MethoCult M3434 (mouse) or H4434 (human), thawed overnight 4 °C, single-use aliquots
- 35 mm gridded culture dishes + 100 mm meta-dish for humidity
- 3 mL syringes + 16 G blunt needles
- Inverted microscope, 4× and 10× objectives

**Procedure:**
1. Dilute 500 HSCs into 300 µL IMDM + 2% FBS.
2. Add to 3 mL MethoCult aliquot. Vortex 4 s, let air bubbles dissipate 5 min.
3. Dispense 1.1 mL per 35 mm dish using blunt needle. Plate in triplicate per condition.
4. Place three dishes + one 35 mm dish of sterile water in a 100 mm dish. Incubate 14 d at 37 °C, 5% CO₂. Do not disturb after day 2.
5. Score at day 14: CFU-GEMM, CFU-GM, BFU-E per standard morphology (STEMCELL atlas). Two independent scorers, blinded to condition.
6. Photo-document representative colonies at 10× for figure.
7. For serial replating (self-renewal, SOP extension): pool colonies by trypsinization/wash, replate 500 cells in fresh MethoCult, score at day 28.

**Acceptance criteria:** Inter-scorer agreement ≥90%; uncoated control ≥30 total colonies per 500 cells.

---

## SOP-05 — Murine HSCT Procedure

**Purpose:** Lethal TBI conditioning + tail-vein HSC infusion with survival monitoring to day 42.

**Materials:**
- C57BL/6 recipients, 8 wk, sex-matched within cohort
- Cesium or X-ray irradiator (calibrated within 6 mo)
- Sterile acidified water + trimethoprim-sulfamethoxazole (drinking, 4 wk post-Tx)
- Autoclaved food and bedding
- 27 G × 1/2" needles + 1 mL syringes
- Heat lamp or 37 °C warming box
- Restraint device (tail-vein injection)

**Procedure:**
1. **Day −1:** Switch recipients to sterile food/water. Weigh and ear-tag. Record in study log.
2. **Day 0 morning:** Irradiate 9 Gy TBI (split 4.5 Gy × 2, 4 h apart preferred for GI tolerance). Log dose, time, chamber ID.
3. **Day 0 afternoon:** Prepare grafts per SOP-01 + SOP-02. QC: viability ≥90%, coverage ≥80% (spot-check 1000 cells by flow). Final formulation 1×10⁶ HSC in 200 µL sterile PBS.
4. Warm mouse in 37 °C box ×2 min to dilate tail vein. Wipe tail with 70% ethanol.
5. Inject 200 µL IV into lateral tail vein. Confirm successful bolus (no bleb). If failed, attempt contralateral vein once; if second failure, exclude mouse and document.
6. Return mouse to clean cage under heat lamp ×15 min for recovery.
7. Record injection time, graft lot, any complications.
8. **Post-transplant monitoring:** Daily GvHD score (SOP-06), body weight daily first 2 wk then 2×/wk, weekly submandibular bleed for chimerism panel.
9. **Humane endpoints (any single criterion):** weight loss >20% from day 0, GvHD score ≥8, severe respiratory distress, moribund appearance. Euthanize + terminal tissue harvest.
10. **Day 42 endpoint:** Terminal bleed, spleen harvest, organ panel (liver, kidney, lung, gut, skin, BM) into 10% NBF.

**Acceptance criteria:** Injection success rate ≥95%. Syngeneic control group survival ≥90% to day 42.

---

## SOP-06 — GvHD Composite Scoring (0–10)

**Purpose:** Blinded daily assessment of GvHD severity using Cooke et al. composite scale.

**Scoring criteria:**

| Parameter | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| Weight loss | none | <10% | 10–25% | >25% |
| Posture | normal | hunched when still | hunched continuously | — |
| Activity | normal | mildly reduced | stationary unless prodded | — |
| Fur texture | normal smooth | mild ruffling | severe ruffling / piloerection | — |
| Skin integrity | normal | scaly paws/tail | obvious lesions | — |

Total range 0–10.

**Procedure:**
1. Scorer is blinded to group assignment. Same scorer for duration of study when feasible; if multiple scorers, run inter-rater concordance pilot (κ ≥0.8).
2. Score at consistent time of day (±2 h). Do not score immediately after cage change or procedure.
3. Record on study log. Flag score ≥5 for PI review same day. Flag score ≥8 → humane endpoint discussion within 2 h.
4. Weigh mouse before scoring (weight loss data feeds into score).
5. Keep mouse in cage during observation ≥30 s before handling; do not penalize handling-induced activity changes.

**Acceptance criteria:** Inter-rater κ ≥0.8 on pilot mice before study start.

---

## Sign-off
| SOP | Author | PI Review | Effective Date | Next Review |
|-----|--------|-----------|----------------|-------------|
| 01 | _______ | _______ | _______ | +6 mo |
| 02 | _______ | _______ | _______ | +6 mo |
| 03 | _______ | _______ | _______ | +6 mo |
| 04 | _______ | _______ | _______ | +6 mo |
| 05 | _______ | _______ | _______ | +6 mo |
| 06 | _______ | _______ | _______ | +6 mo |
