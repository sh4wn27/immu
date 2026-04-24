# Phase 1 Run Plan — Polymer Synthesis & Coating Characterization (Months 1–3)

Week-by-week schedule that turns `MASTER_RESEARCH_PLAN.md` Phase 1 into executable tasks. All bench work gated on Phase 0 completion (`docs/phase0/index.md`). Operator = SL unless delegated.

**Aim 1 success criteria (must all be met before Phase 2 launch):**
- Surface coverage ≥80% on CD34⁺ HSCs
- Viability ≥90%
- CXCR4 function ≥80% of uncoated baseline
- Degradation kinetics characterized in 50% plasma out to day 28

---

## Month 1 — Polymer synthesis & QC

### Week 1 — Kickoff
- Day 1 (Mon): confirm all Tier 1 reagents received; update `reagent_lot_log` (T-00).
- Day 1–2: reconstitute PEG-NHS and PCB-NHS per SOP-01 spec; confirm solubility, prepare 100 µL freezer aliquots.
- Day 3: book DLS + FT-IR core time for Weeks 2–4.
- Day 3–4: if in-house PCB synthesis route, start RAFT reaction (see `pcb_synthesis.md` to be written if needed). Otherwise QC commercial PCB-NHS COA.
- Day 5: DLS/FT-IR dry-run on polymer-only samples (no cells) — confirm signal and workflow.

### Week 2 — Polymer characterization
- DLS: polymer-alone, 3 runs per polymer, record into T-02.
- FT-IR: polymer film on ATR crystal, identify amide I/II peaks, record T-03.
- GPC/NMR (if in-house PCB): confirm Mn ≈ 6 kDa, PDI <1.2, NHS activation by ¹H NMR integration.
- **Gate:** polymer passes COA review AND DLS peak1 at expected size (5 kDa PEG ≈ 3–4 nm, 6 kDa PCB ≈ 4–5 nm). If fail → reorder or retry RAFT.

### Week 3 — Fluorescent labeling & Cy7 batches
- Prepare fluorescein-NHS-co-polymer by dual labeling: 10% fluorescein-NHS + 90% polymer-NHS (molar) for flow coverage reads.
- Prepare Cy7-NHS-co-polymer batch for IVIS pilot.
- Validate labeling efficiency by UV/Vis (fluorescein ε₄₉₄ = 68,000; Cy7 ε₇₅₀ = 240,000).
- Freeze aliquots. Note: labeled polymers expire at 6 months even frozen.

### Week 4 — Cell-line coating dose-response matrix start
- Plate K562 or 32Dcl3 cells (these are easier to obtain than LSK; confirm with PI which line). Thaw, expand over Week 3.
- Run full dose-response matrix per Experiment 1.2:
  - Polymer concentration × time × temperature × pH → 90 conditions total
  - Realistic plan: fractional-factorial design to reduce to ~30 conditions using Resolution IV; full factorial blows budget and time.
- Readouts per condition: trypan blue viability, flow for FITC⁺ coverage + CXCR4 MFI.
- Data entered into T-01 immediately.

**Month 1 milestone:** Polymer batches QCed, dose-response matrix data in hand.

---

## Month 2 — Optimization on cell lines → primary HSCs

### Week 5 — Analyze Week 4 matrix
- Run `src/analysis/analysis.R` dose-response summary (add a new function `analyze_dose_response()` next iteration — scaffold can extend).
- Identify **top 3 conditions per polymer**: maximize coverage × viability × CXCR4 retention.
- Reserve: PEG top condition, PCB top condition, one "aggressive" condition for mechanistic insight.

### Week 6 — DLS + FT-IR on cell-coated samples
- Apply top 3 conditions to fresh K562. DLS measures +20–30 nm shift expected; FT-IR confirms amide bond on cell surface (this is technically demanding — confirm with core facility that cell suspensions can be measured, or fix cells first).
- Document T-02, T-03.

### Week 7 — Primary mouse HSC isolation & coating pilot
- SOP-02: harvest BM from 2 BALB/c donors (pilot; not in final experimental count).
- Expect 5×10⁵–1×10⁶ LSK per donor.
- Apply top 2 conditions per polymer (can only run a limited matrix on primary cells; choose strongest candidates).
- Flow readouts per SOP-01.

### Week 8 — CXCR4 chemotaxis on primary HSC
- Experiment 1.4: transwell chemotaxis with SDF-1α gradient.
- Triplicate wells per condition; data in T-06.
- **Gate:** chemotaxis ≥80% of uncoated. If below, reduce polymer concentration 50% and re-test; if still below, proceed to next candidate.

**Month 2 milestone:** One PEG condition + one PCB condition meeting all three coverage/viability/CXCR4 criteria, on primary mouse HSC.

---

## Month 3 — Degradation kinetics & Phase 1 gate

### Week 9 — Start degradation kinetics study
- Experiment 1.5: fluorescein-polymer on beads (or cells at 4 °C to prevent confounding endocytosis) in 50% pooled human plasma at 37 °C.
- Sampling days 0, 0.25, 1, 3, 7, 14 (Week 9 = plating + days 0, 0.25, 1, 3; Weeks 10–12 capture day 7, 14; 21, 28 spill into Month 4 but can overlap).
- Readouts: FITC MFI by flow, DLS z-average. MTT assay of conditioned media on 3T3 at each timepoint (cytotoxicity).

### Week 10 — CFU pilot on primary HSC
- Experiment 1.3 readout: plate 500 LSK cells per condition in MethoCult M3434, triplicate.
- Score at day 14 per SOP-04. This bridges into Phase 2.

### Week 11 — Degradation kinetics continues + Phase 1 data lock
- Complete day 14 degradation timepoint.
- Assemble Phase 1 figure set per plan §5.1 Figure 1 (polymer characterization, degradation).
- Draft Phase 1 results memo: coverage, viability, CXCR4, chemotaxis, CFU, degradation.

### Week 12 — Phase 1 go/no-go review
- PI meeting with data. Apply gate:
  - ✅ **GO:** ≥80% coverage + ≥90% viability + ≥80% chemotaxis + ≥85% CFU (bleeding into Phase 2 success) for at least one polymer at one dose
  - ❌ **NO-GO:** Both polymers fail viability → pivot to lipid-anchored stealth (DSPE-PEG) or click chemistry. Extension plan: add 4 weeks to evaluate pivot before proceeding.
- If GO, lock optimized coating condition for Phase 2–4. Order additional polymer / antibody inventory per Tier 2 procurement.

**Month 3 deliverable:** Phase 1 memo with figures, go/no-go decision signed by PI.

---

## Resource allocation during Phase 1

| Resource | Weekly demand |
|---------|---------------|
| Bench time (operator) | ~35 h/wk (tight; de-scope dose-response matrix if ≥40 h/wk) |
| BSC | ~15 h/wk |
| Flow cytometer | ~6 h/wk |
| DLS | ~4 h total in M1, 4 h total in M2 |
| FT-IR | ~2 h total M1 |
| Vivarium / BM harvest | 0.5 d × 2–3 times across Weeks 7, 10 |
| Analyst / stats | ~4 h/wk (own time) |

---

## Deviations & change control

- Protocol deviations logged in Benchling with justification + PI sign-off.
- Any in-process change to coating SOP requires minor revision to `sops.md` and re-sign.
- Reagent lot changes mid-phase: re-run one matching condition from prior lot for bridging (qualification).

---

## Parallel tracks starting during Phase 1

Non-blocking work to start in parallel:
- **IRB amendment** for human cord-blood after Week 4 if Phase 1 data trends well — procurement from STEMCELL has ~3 wk lead time.
- **Biostatistics consult** (Stanford QSU) at Week 6 — bring in a consultant to validate the mixed-model design for CFU before running Phase 2 full n.
- **Manuscript figure layout** sketch at Week 10 — lightweight template so data drops in during Phases 2–4.

---

## Cross-reference

- SOPs: `docs/phase0/sops.md`
- Data schemas: `docs/phase0/data_capture_templates.md`
- Statistical analysis: `src/analysis/analysis.R`
- Procurement: `docs/phase0/procurement.md`
- Power analysis: `docs/phase0/power_analysis.md`
