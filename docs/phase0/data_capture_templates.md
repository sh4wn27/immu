# Data Capture Templates — ELN-Ready Schemas

Each template below is a flat tabular schema ready to paste into Benchling / LabArchives / Excel. Headers are the authoritative column order. Enforce type and unit per column. Every row is one observation. Do not merge cells. No color formatting that loses on export. File naming: `YYYY-MM-DD_<assay>_<operator-initials>.xlsx`.

---

## T-00 — Reagent Lot Log (single sheet, reused)

| Column | Type | Example |
|--------|------|---------|
| date_received | ISO date | 2026-05-03 |
| item | string | PEG-NHS 5 kDa |
| vendor | string | Laysan Bio |
| catalog_no | string | MPEG-SCM-5000 |
| lot_no | string | L2026-0412 |
| quantity | numeric | 500 mg |
| storage_location | string | Freezer −20 °C, shelf 3 |
| coa_filename | string | COA_PEG_L2026-0412.pdf |
| qualified_for_study | boolean | TRUE |
| notes | string | Qualified for entire Phase 1–4 |

---

## T-01 — Polymer Coating Run Log (SOP-01)

| Column | Type | Example |
|--------|------|---------|
| run_id | string | 2026-05-10-R01 |
| operator | initials | SL |
| date | ISO date | 2026-05-10 |
| polymer_type | enum | PEG / PCB |
| polymer_lot | string | L2026-0412 |
| polymer_conc_mgmL | numeric | 2.0 |
| reaction_buffer | string | 20 mM HEPES pH 7.4 |
| temperature_C | numeric | 22 |
| time_min | numeric | 30 |
| cell_source | enum | K562 / LSK-mouse / CD34-human |
| cell_input_count | integer | 100000 |
| quench_agent | string | 100 mM glycine, 5 min RT |
| viability_percent | numeric | 94.2 |
| coverage_percent_fitc | numeric | 82.0 |
| cxcr4_mfi | numeric | 4280 |
| cxcr4_mfi_uncoated_ctrl | numeric | 5120 |
| cxcr4_ratio | numeric | 0.84 |
| pass_fail | enum | PASS / FAIL |
| notes | string | Polymer dissolved cleanly; no precipitate |

---

## T-02 — DLS Size Characterization

| Column | Type | Example |
|--------|------|---------|
| sample_id | string | PEG-HSC-2mg-30min |
| measurement_date | ISO date | 2026-05-11 |
| instrument | string | Zetasizer Nano ZS |
| material | enum | polymer-alone / coated-HSC / uncoated-HSC |
| z_avg_nm | numeric | 18.6 |
| pdi | numeric | 0.18 |
| peak1_nm | numeric | 17.8 |
| peak1_intensity_pct | numeric | 98.4 |
| replicate | integer | 1 |
| run_pass_qc | boolean | TRUE |
| notes | string | 3 runs averaged |

---

## T-03 — FT-IR Amide Bond Confirmation

| Column | Type | Example |
|--------|------|---------|
| sample_id | string | PCB-HSC-1mg-60min |
| measurement_date | ISO date | 2026-05-12 |
| instrument | string | Bruker Alpha II ATR |
| amide_I_cm1 | numeric | 1648 |
| amide_II_cm1 | numeric | 1540 |
| baseline_corrected | boolean | TRUE |
| peak_height_amide_I | numeric | 0.42 |
| peak_height_amide_I_baseline | numeric | 0.08 |
| confirmed_amide | boolean | TRUE |
| notes | string | Clear amide I shift vs polymer-alone ctrl |

---

## T-04 — Mixed Lymphocyte Reaction (SOP-03)

One row per well.

| Column | Type | Example |
|--------|------|---------|
| plate_id | string | MLR-20260520-P01 |
| well | string | B3 |
| stimulator_type | enum | uncoated-alloB / PEG-alloB / PCB-alloB / syngeneic / polyclonal / none |
| stimulator_lot | string | LSK-2026-05-15 |
| responder_lot | string | CD3-B6-2026-05-18 |
| et_ratio | string | 1:5 |
| biological_rep | integer | 1 |
| technical_rep | integer | 2 |
| incubation_hr | numeric | 72 |
| cfse_divided_pct | numeric | 48.2 |
| proliferation_index | numeric | 2.1 |
| ifn_gamma_pgmL | numeric | 820 |
| il_2_pgmL | numeric | 140 |
| live_t_cells_recovered | integer | 68000 |
| flagged_for_qc | boolean | FALSE |
| notes | string | |

Derived columns (computed, not entered): `ifn_gamma_suppression_vs_uncoated`, `prolif_suppression_vs_uncoated`.

---

## T-05 — CFU Assay (SOP-04)

| Column | Type | Example |
|--------|------|---------|
| dish_id | string | CFU-20260525-D01 |
| plating_date | ISO date | 2026-05-25 |
| scoring_date | ISO date | 2026-06-08 |
| cell_source | enum | uncoated / PEG / PCB / human-CD34 |
| input_cells | integer | 500 |
| methocult_lot | string | M3434-2026-04 |
| biological_rep | integer | 1 |
| technical_rep | integer | 1 |
| cfu_gemm | integer | 4 |
| cfu_gm | integer | 18 |
| bfu_e | integer | 12 |
| cfu_total | integer | 34 |
| scorer_1_initials | string | SL |
| scorer_2_initials | string | AB |
| scorer_agreement | numeric | 0.94 |
| photo_filename | string | CFU-D01-10x-colony.jpg |
| secondary_replate | boolean | FALSE |
| notes | string | |

---

## T-06 — Chemotaxis (Transwell)

| Column | Type | Example |
|--------|------|---------|
| assay_id | string | CHEMO-20260526-R01 |
| well | string | A2 |
| condition | enum | uncoated / PEG / PCB / no-chemokine-ctrl |
| sdf1a_ngmL | numeric | 100 |
| input_cells_upper | integer | 10000 |
| migrated_count_lower | integer | 3420 |
| migration_pct | numeric | 34.2 |
| biological_rep | integer | 1 |
| technical_rep | integer | 1 |
| retention_vs_uncoated | numeric | 0.82 |
| pass_fail | enum | PASS / FAIL |

---

## T-07 — Degradation Kinetics

| Column | Type | Example |
|--------|------|---------|
| sample_id | string | DEG-PEG-t7d |
| polymer_type | enum | PEG / PCB |
| matrix | string | 50% human plasma, 37 °C |
| timepoint_hr | numeric | 168 |
| fitc_mfi_residual | numeric | 820 |
| fitc_mfi_t0 | numeric | 3800 |
| pct_remaining | numeric | 21.6 |
| dls_zavg_nm | numeric | 14.2 |
| mtt_viability_3t3 | numeric | 0.96 |
| replicate | integer | 1 |

---

## T-08 — In Vivo Animal Master Log

One row per mouse.

| Column | Type | Example |
|--------|------|---------|
| mouse_id | string | M-001 |
| ear_tag | integer | 1 |
| strain | enum | BALB/c / C57BL/6 |
| sex | enum | F / M |
| dob_estimated | ISO date | 2026-03-15 |
| arrival_date | ISO date | 2026-08-01 |
| weight_d0_g | numeric | 21.4 |
| cage_id | string | C-01 |
| group | enum | A-syn / B-uncoated / C-PEG / D-PCB / E-imaging |
| irradiation_date | ISO date | 2026-08-15 |
| irradiation_dose_Gy | numeric | 9.0 |
| graft_lot | string | LSK-2026-08-15 |
| graft_viability_pct | numeric | 92 |
| graft_coverage_pct | numeric | 81 |
| injection_time | ISO datetime | 2026-08-15T16:20 |
| injection_success | boolean | TRUE |
| endpoint_date | ISO date | 2026-09-26 |
| endpoint_reason | enum | scheduled-d42 / humane-weight / humane-gvhd / other |
| notes | string | |

---

## T-09 — GvHD Daily Score (SOP-06)

| Column | Type | Example |
|--------|------|---------|
| mouse_id | string | M-001 |
| date | ISO date | 2026-08-20 |
| day_post_tx | integer | 5 |
| scorer | initials | AB |
| blinded | boolean | TRUE |
| weight_g | numeric | 19.8 |
| weight_loss_pct | numeric | 7.5 |
| weight_score | integer | 0 |
| posture_score | integer | 1 |
| activity_score | integer | 1 |
| fur_score | integer | 1 |
| skin_score | integer | 0 |
| total_gvhd | integer | 3 |
| pi_notified | boolean | FALSE |
| notes | string | |

---

## T-10 — Chimerism Flow (Weekly Bleeds)

| Column | Type | Example |
|--------|------|---------|
| mouse_id | string | M-001 |
| bleed_date | ISO date | 2026-09-05 |
| day_post_tx | integer | 21 |
| cd45_1_donor_pct | numeric | 68.4 |
| cd45_2_host_pct | numeric | 29.1 |
| cd45_dn_pct | numeric | 2.5 |
| cd3_pct | numeric | 14 |
| cd19_pct | numeric | 38 |
| cd11b_pct | numeric | 42 |
| live_events | integer | 24500 |
| fcs_filename | string | M001_d21.fcs |
| notes | string | Clean sample |

---

## T-11 — IVIS Polymer Clearance

| Column | Type | Example |
|--------|------|---------|
| mouse_id | string | M-041 |
| session_date | ISO date | 2026-09-15 |
| day_post_tx | integer | 1 |
| exposure_s | numeric | 30 |
| emission_filter_nm | integer | 780 |
| radiant_efficiency_liver | numeric | 4.2e9 |
| radiant_efficiency_spleen | numeric | 2.8e9 |
| radiant_efficiency_hindlimb_BM | numeric | 1.6e9 |
| radiant_efficiency_background | numeric | 1.2e7 |
| pct_initial_signal | numeric | 100.0 |
| tiff_filename | string | IVIS_M041_d1.tif |
| notes | string | Baseline post-injection |

---

## T-12 — Terminal Serum Chemistry

| Column | Type | Example |
|--------|------|---------|
| mouse_id | string | M-001 |
| sample_date | ISO date | 2026-09-26 |
| alt_u_L | numeric | 42 |
| ast_u_L | numeric | 89 |
| bun_mgdL | numeric | 24 |
| creatinine_mgdL | numeric | 0.24 |
| c3a_ngmL | numeric | 85 |
| c5a_ngmL | numeric | 6.2 |
| anti_peg_igm_od | numeric | 0.12 |
| anti_peg_igg_od | numeric | 0.08 |
| notes | string | |

---

## T-13 — Histopathology Scoring (Blinded)

| Column | Type | Example |
|--------|------|---------|
| mouse_id | string | M-001 |
| organ | enum | liver / gut-SI / gut-colon / lung / kidney / skin / BM |
| block_id | string | HIS-2026-09-26-M001-liver |
| scorer | initials | AB |
| blinded | boolean | TRUE |
| inflammation_score | integer (0–4) | 2 |
| apoptosis_score | integer (0–4) | 1 |
| architecture_score | integer (0–4) | 1 |
| composite_organ_score | integer | 4 |
| image_filename | string | HE_M001_liver_10x.svs |
| notes | string | Mild periportal lymphocytic infiltrate |

---

## File-organization convention

```
.
└── data/
    ├── raw/
    │   ├── flow_fcs/
    │   ├── ivis_tif/
    │   ├── histo_slides/
    │   └── elisa_plates/
    ├── sheets/         # T-00 through T-13 spreadsheets, one per run
    ├── derived/        # computed summary tables, figures
    └── archive/        # locked at endpoint, read-only
```

**Backup cadence:** nightly Stanford OneDrive sync + weekly Benchling snapshot. Raw flow FCS and IVIS TIFF files kept forever; spreadsheets versioned with date suffix.

**Data-integrity rules (ALCOA+):**
- Attributable: every row has operator initials and date.
- Legible: typed entries only; handwritten lab notebook pages scanned within 48 h.
- Contemporaneous: entries made at time of observation.
- Original: raw instrument output preserved unedited.
- Accurate: units explicit; double entry for high-stakes measurements (flow gating, histology scores).
- Complete, Consistent, Enduring, Available.

---

## Minimum viable handoff dataset (for manuscript)

At study end, package the following as single ZIP for submission + public repo:
1. All T-00 through T-13 sheets, finalized.
2. Corresponding raw files referenced by `*_filename` columns.
3. Analysis scripts (R/Python) with seed set.
4. Protocol PDFs (SOPs + IACUC/IRB approvals).
5. README describing schema mapping.
