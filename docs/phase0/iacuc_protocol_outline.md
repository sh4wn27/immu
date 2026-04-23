# IACUC Protocol Outline
## BALB/c → C57BL/6 Allogeneic HSCT with Biodegradable Polymer-Coated Donor Grafts

Use this as the narrative backbone when filling out the Stanford APLAC e-form. Section numbers map to common IACUC modules; adapt to institutional template.

---

## 1. Protocol Title
Evaluation of biodegradable stealth polymer (PEG / PCB) coatings on donor hematopoietic stem cells for MHC-mismatched allogeneic murine HSCT: engraftment, GvHD, and polymer clearance.

## 2. Lay Summary
β-Thalassemia and other hematologic disorders are curable by stem-cell transplant, but most patients lack an HLA-matched donor. Mismatched transplants cause graft-versus-host disease (GvHD), which can be lethal. We will test whether transiently coating donor stem cells with a biodegradable polymer — to hide surface antigens long enough for the graft to take hold — reduces GvHD while preserving engraftment. The polymer then hydrolyzes away naturally within weeks.

## 3. Hypothesis & Objectives
**Hypothesis:** Donor BALB/c HSCs coated with PEG-NHS or PCB-NHS polymer will achieve ≥60% donor chimerism by week 4 and ≤50% of control GvHD score when transplanted into lethally irradiated C57BL/6 recipients; polymer will clear to background by day 42.

**Specific Aims (animal work):**
- Aim 3a: Measure donor chimerism over 6 weeks post-HSCT in coated vs uncoated vs syngeneic controls.
- Aim 3b: Score GvHD daily using validated composite scale; compare severity and onset.
- Aim 3c: Image polymer clearance (Cy7-labeled cohort) at d1, 3, 7, 14, 21, 28, 42.
- Aim 3d: Terminal histopathology (liver, gut, skin, lung, kidney, BM) + serum chemistry.

## 4. Animal Species, Strains, Numbers

**Donors:** BALB/c (CD45.1 congenic variant, Jackson #000651) — 20 mice  
**Recipients:** C57BL/6J (CD45.2, Jackson #000664) — 40 mice primary study + 8 Cy7 imaging cohort = 48 mice  
**Total:** 68 mice.

**Justification of species:** BALB/c ↔ C57BL/6 is the most thoroughly characterized fully MHC-mismatched allogeneic model; congenic CD45.1/.2 system allows precise flow cytometric tracking of chimerism without genetic modification of donors.

## 5. Experimental Groups (Primary Study)

| Group | n | Graft | Recipient | Conditioning |
|-------|---|-------|-----------|--------------|
| A — Syngeneic control | 8 | BALB/c HSC | BALB/c | 9 Gy TBI |
| B — Allogeneic uncoated | 8 | BALB/c HSC | C57BL/6 | 9 Gy TBI |
| C — PEG-coated allogeneic | 8 | PEG-BALB/c HSC | C57BL/6 | 9 Gy TBI |
| D — PCB-coated allogeneic | 8 | PCB-BALB/c HSC | C57BL/6 | 9 Gy TBI |
| E — Cy7-imaging cohort | 8 | PEG-Cy7 or PCB-Cy7 BALB/c HSC | C57BL/6 | 9 Gy TBI |

## 6. Power Analysis

Primary endpoint: donor chimerism at week 4, two-sample t-test between uncoated allogeneic (group B) and each coated group (C, D). Prior data and proposal-stated effect size: 30% absolute difference in chimerism, pooled SD ≈20%. Cohen's d ≈1.5. G*Power: α=0.05, power=0.80, two-tailed → n=8 per group. See `power_analysis.md` for detail.

## 7. 3Rs Statement

**Replacement:** In vitro MLR, CFU, and chemotaxis assays (Phases 1–2) test coating efficacy and potency before animal work; in vivo phase proceeds only if both in vitro go/no-go thresholds are met (≥70% T-cell suppression, ≥85% CFU). Human cord-blood data is generated in parallel for translational relevance, reducing reliance on murine data for future decisions.

**Reduction:** Power analysis determines minimum n=8/group. Cy7 imaging cohort (n=8) is separate to avoid confounding with primary endpoint measurement (peri-vascular imaging dye can alter flow cytometry), but reuses the same conditioning and procedures so no additional learning is needed. Terminal blood samples pooled across endpoints where volume allows.

**Refinement:** 
- 9 Gy TBI split 4.5 Gy × 2, 4 h apart — literature shows reduced GI toxicity vs single dose.
- Heat lamp recovery, warmed PBS injection buffer (37 °C).
- Acidified water + prophylactic antibiotics × 4 wk post-Tx.
- Daily monitoring with humane endpoints defined a priori (§10).
- Blinded GvHD scoring reduces observer stress-induced variability.
- Submandibular bleeding limited to 50 µL with alternating sides (14-day recovery window).

## 8. Procedures

### 8.1 Irradiation (9 Gy TBI)
Mice placed in pie-chamber irradiator; split dose 4.5 Gy × 2 with 4 h interval. Duration per exposure: 3–5 min. No sedation required (brief duration, no handling during exposure).

### 8.2 HSC Harvest from Donors
Donors euthanized per §10 (CO₂ + cervical dislocation confirmation). Bone marrow flushed from hind-limb long bones post-mortem. No live surgery on donors.

### 8.3 Graft Infusion
Recipient placed in warming box 2 min, restrained in tail-vein device. 200 µL graft injected into lateral tail vein with 27 G needle. Single injection; contralateral attempt permitted once if first fails, then animal excluded. Total restraint time <3 min.

### 8.4 Blood Sampling
Submandibular (cheek) bleed, 50 µL, weekly (6 time points). Isoflurane not required but must have immediate hemostasis and monitoring. Alternate sides each week.

### 8.5 IVIS Imaging (Cy7 cohort only)
Isoflurane anesthesia (1.5–2% maintenance) for 10–15 min per imaging session. Recovery on warming pad until ambulatory. Sessions at d1, 3, 7, 14, 21, 28, 42.

### 8.6 Terminal Tissue Harvest
CO₂ euthanasia, cervical dislocation. Cardiac puncture for terminal serum. Organs harvested and fixed in 10% neutral buffered formalin or snap-frozen.

## 9. Anesthesia / Analgesia

- **IVIS imaging:** Isoflurane, 2% induction / 1.5% maintenance in O₂ @ 1 L/min. Eye lubricant applied.
- **No operative analgesia indicated:** all procedures are non-surgical (IV injection, blood draw, non-invasive imaging). Transplant recipients monitored for distress and treated with subcutaneous buprenorphine (0.1 mg/kg q12h) only if GvHD score ≥4 AND veterinary staff agree pain is a component. Log any rescue analgesia.

## 10. Humane Endpoints

Animals euthanized if any single criterion met:
- Body weight loss >20% from day 0
- GvHD composite score ≥8 (out of 10) for >24 h
- Inability to reach food/water
- Severe respiratory distress, persistent hypothermia, or moribund appearance
- Ulceration or necrosis of skin not responsive to topical care
- Observation of severe pain/distress per veterinary staff at any time

Animals meeting endpoint: CO₂ euthanasia with cervical dislocation confirmation, within 4 h of assessment. Terminal samples collected when feasible.

## 11. Housing & Husbandry

- ABSL-2 barrier facility, autoclaved static cages or IVCs.
- 5 mice / cage maximum post-Tx (reduce if GvHD injury risk).
- Sterile autoclaved food and acidified water ad libitum. Drinking water contains trimethoprim-sulfamethoxazole (40 mg/8 mg per mL) for first 4 wk post-transplant.
- 2-week acclimation period after arrival before procedures.
- Environmental enrichment: nesting material, hut (non-abrasive).

## 12. Personnel & Training

| Role | Training required |
|------|-------------------|
| PI / protocol sponsor | APLAC faculty course, species-specific |
| Bench operator (you) | Rodent handling, IV injection, CO₂ euthanasia, cervical dislocation, BSL-2, ABSL-2, radiation safety |
| Blinded scorer | Rodent observation, GvHD scoring training session + pilot concordance |
| Imaging tech | IVIS system training, isoflurane anesthesia |

All personnel complete CITI modules prior to listing on protocol. Document certification dates.

## 13. Hazards

- **Radiation:** 9 Gy TBI. Animals non-radioactive after exposure (external beam). No shielding required for staff post-treatment.
- **Biohazard:** Human cord-blood handling in separate BSL-2 protocol (not in this APLAC). Murine work is BSL/ABSL-2.
- **Chemical:** NHS-ester reagents handled in BSC; no animal exposure.

## 14. Attachments to Include in Full Submission
- Protocol narrative (this outline expanded)
- SOPs: irradiation, IV injection, blood collection, GvHD scoring, euthanasia (from `sops.md`)
- Power analysis (`power_analysis.md`)
- Personnel training certificates
- Facility certifications (irradiator calibration, BSC certification)
- Drug treatment authorization letter from vet (prophylactic antibiotics, rescue buprenorphine)
- Literature supporting model justification and 3Rs

## 15. Review Milestones
- Draft to PI: week 1
- Internal review + revisions: weeks 2–3
- Submit to APLAC: week 3 end
- APLAC review cycle: ~4–6 wk — build into timeline; no bench animal work until approved
- Annual continuing review + amendment process documented
