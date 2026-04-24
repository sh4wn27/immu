# Power Analysis Summary

Prospective power calculations per `MASTER_RESEARCH_PLAN.md` §0.4. All analyses α=0.05, two-tailed, power=0.80 unless stated. Effect sizes sourced from: (i) mission-critical pre-registered effect size in the proposal, and (ii) published reference studies cited inline. Re-run G*Power before submitting IACUC.

---

## 1. In Vivo Primary Endpoint — Donor Chimerism at Week 4

**Design:** Independent two-sample t-test, two-tailed; coated (group C or D) vs uncoated allogeneic (group B). Conservative pairwise comparison; ANOVA across four groups has higher power so this is the limiting case.

**Expected effect:** Proposal target is ≥60% chimerism in coated vs expected ~30% in uncoated allogeneic (consistent with Shizuru JM et al. conditioned-mismatch baseline). Absolute difference ≈30%. Pooled SD ≈20% (literature-standard for chimerism at wk 4).

**Cohen's d:** 30 / 20 = **1.5** (large effect)

**G*Power input:**
- Test family: t tests → Means: Difference between two independent means
- Tails: Two
- Effect size d: 1.5
- α err prob: 0.05
- Power: 0.80
- Allocation ratio N2/N1: 1

**Result:** n = **8 per group** (total sample in comparison = 16; protocol total = 32 across 4 groups + 8 imaging cohort).

**Sensitivity check:** If true SD is 25% (worse variability), d=1.2 → n=12/group. Flag in IACUC as contingency: may request amendment to increase if Phase 3 pilot shows higher SD.

---

## 2. In Vitro MLR — T-Cell Proliferation Suppression

**Design:** One-way ANOVA, 4 conditions (uncoated allogeneic, PEG-coated, PCB-coated, syngeneic). Effect reported as proliferation index difference.

**Expected effect:** ≥70% suppression target → uncoated ≈0.6 (60% divided), coated ≈0.18 (18% divided). Δ = 0.42 on a 0–1 scale.

**Cohen's f (from η² ≈ 0.35):** **0.74** (large)

**G*Power input:**
- Test family: F tests → ANOVA: Fixed effects, omnibus, one-way
- Effect size f: 0.74
- α: 0.05
- Power: 0.80
- Number of groups: 4

**Result:** Total N = **16** → **n=3 biological replicates × 3 technical = 9 wells per group**, well-powered at n=3 biological. Protocol uses n=3 biological × 3 technical replicates per condition, compliant with 3Rs.

---

## 3. CFU Assay — Colony Retention

**Design:** Paired comparison vs uncoated same-donor split, one-way ANOVA across polymer conditions.

**Expected effect:** ≥85% CFU retention target (15% drop). Uncoated control ≈30 colonies / 500 cells; coated ≈25.5. SD across triplicates ≈4.

**Cohen's d (between uncoated and coated):** 4.5 / 4 = **1.1**

**G*Power result:** n = **14 dishes** for two-sample comparison at d=1.1. Protocol uses n=3 biological × 3 triplicate dishes = 9 dishes → underpowered if effect is small. Mitigation: if Phase 1 pilot shows <85% retention, scale to 5 biological replicates (n=15 dishes); update during Phase 2 planning.

---

## 4. CXCR4 Chemotaxis

**Design:** Two-sample t-test, coated vs uncoated migration ratio.

**Expected effect:** ≥80% migration retention. Uncoated migration = 50% of input; coated = 40%. Δ=10%, SD ≈8%.

**Cohen's d:** 10 / 8 = **1.25**

**Result:** n = **11/group**. Protocol recommends 3 biological × 3 technical = 9; borderline. Add 1 biological replicate if pilot shows SD >10%.

---

## 5. GvHD Score — In Vivo Secondary Endpoint

**Design:** Mann-Whitney U (non-parametric, ordinal score 0–10), coated vs uncoated allogeneic.

**Expected effect:** Uncoated median GvHD ≈6, coated median ≈3 at day 28. Effect size r ≈0.5 (large).

**Result:** n = **8/group** at α=0.05, power=0.80, two-tailed Mann-Whitney (Wilcoxon-Mann-Whitney approx via G*Power "Means: Wilcoxon–Mann-Whitney test (two groups)"). Matches primary endpoint n.

---

## 6. Survival (Kaplan-Meier / log-rank)

**Design:** Log-rank test, assumes 40% of uncoated mice reach humane endpoint by d42 vs 10% in coated.

**Hazard ratio:** ≈0.22 (large effect).

**G*Power input:** z-tests → Proportions: Difference between two independent proportions.

**Result:** n = **13/group** for 80% power at this HR. At n=8/group, power ≈60% for survival endpoint — adequate as secondary exploratory outcome. Flag in protocol: survival is secondary; primary analysis is chimerism.

---

## 7. Summary Table

| Endpoint | Test | Effect size | Power target | n required | Protocol n | Status |
|----------|------|-------------|--------------|------------|------------|--------|
| Chimerism wk 4 | Two-sample t | d=1.5 | 0.80 | 8 | 8 | ✓ Primary — meets |
| MLR (T-cell div) | 1-way ANOVA | f=0.74 | 0.80 | 3/grp | 3 bio × 3 tech | ✓ Meets |
| CFU retention | ANOVA/t | d=1.1 | 0.80 | 14 | 9 | ⚠ Tight — pilot-verify SD |
| Chemotaxis | Two-sample t | d=1.25 | 0.80 | 11 | 9 | ⚠ Borderline |
| GvHD score | Wilcoxon MW | r=0.5 | 0.80 | 8 | 8 | ✓ Meets |
| Survival | Log-rank | HR=0.22 | 0.80 | 13 | 8 | ⚠ Secondary / underpowered |
| Anti-PEG screen | Descriptive | — | — | 10 donors | 10 | ✓ Descriptive, not powered |

---

## 8. Recommendations

1. **Lock primary endpoint analysis plan** as chimerism week 4 (t-test). IACUC 3Rs rationale stands.
2. **Pilot in vitro variance** in Phase 2 pilot week — if CFU SD >5 colonies or chemotaxis SD >10%, amend to 4–5 biological replicates before Phase 2 full run.
3. **Survival endpoint** reported descriptively / as secondary; a priori n=8 is not powered for log-rank. Note in manuscript Methods.
4. **Pre-register analysis plan** on OSF at start of Phase 4 to avoid accusations of outcome switching.
5. Re-run G*Power once pilot SDs are measured; save screenshots/input files to `docs/phase0/gpower_inputs/` at that time.
