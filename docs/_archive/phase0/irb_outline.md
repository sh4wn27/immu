# IRB Protocol Outline
## De-identified Pediatric Cord-Blood CD34⁺ Cells for In Vitro Polymer Coating Validation

Use this as the narrative backbone for Stanford IRB e-protocol. Most human-subjects review boards treat de-identified, already-banked cord-blood units as Exempt Category 4 or Not Human Subjects Research — confirm at intake meeting.

---

## 1. Protocol Title
In vitro validation of biodegradable stealth polymer coating on de-identified human umbilical cord-blood CD34⁺ hematopoietic stem cells.

## 2. Principal Investigator
Huanxuan (Shawn) Li — Stanford iGEM Team / Stanford University.

## 3. Background & Rationale
Coating conditions optimized in murine HSCs (`MASTER_RESEARCH_PLAN.md` Phases 1–2) must be validated on human cells to support translational relevance. Cord-blood CD34⁺ units from de-identified pediatric donors are a standard research reagent used extensively for HSC biology without consent burden when banked de-identified.

## 4. Human Subjects Determination

**Proposed classification:** Not Human Subjects Research (NHSR) or Exempt Category 4.

**Basis:**
- All cord-blood units are de-identified prior to receipt.
- No subject interaction; no intervention; no linkage to identifiable data.
- Material is either:
  (a) Purchased from commercial biorepository (STEMCELL Technologies catalog cord blood — donor identifiers stripped at collection), OR
  (b) Received from Stanford Blood Center under existing institutional de-identification workflow with IRB-approved discard/research-use consent.
- Investigator receives only CD34⁺ count, donor sex, and collection date. No DOB, no maternal identifiers, no medical history beyond term-birth confirmation.

If IRB determines full review is needed, submit as Minimal Risk Expedited (Category 5: research involving existing specimens).

## 5. Specimen Source & Quantity

- **Primary source:** STEMCELL Technologies 70008.1 (frozen CD34⁺ cord blood, ≥90% purity, ≥1×10⁶ cells/vial).
- **Secondary source (if procurement via Stanford Blood Center):** Remnant cord-blood units not suitable for clinical banking, de-identified per SBC SOP. Limited to 5 donors over 18 months.
- **Quantity:** ≤1×10⁶ CD34⁺ cells per donor unit × 5 donors = 5×10⁶ cells total.

## 6. Study Procedures (In Vitro Only)

1. Thaw CD34⁺ cells per manufacturer SOP.
2. Apply polymer coating per SOP-01 (see `sops.md`).
3. Assess viability, coverage, CXCR4 function, CFU in MethoCult H4434.
4. Set up human MLR: coat human CD34⁺ cells, co-culture with HLA-mismatched PBMCs (also de-identified commercial — e.g., STEMCELL 70025).
5. Measure T-cell proliferation (CFSE) and cytokines (human IFN-γ ELISA).
6. Freeze residual cells or dispose as medical waste.

No genetic modification, no reimplantation into any host, no commercial product development within scope of this protocol.

## 7. Data Management

- All raw data labeled by internal study ID (e.g., `CB-2026-001`).
- No PHI fields created. Any inbound metadata (sex, collection date) stored in REDCap or LabArchives with access restricted to study personnel.
- Flow cytometry FCS files retained for publication archive.

## 8. Risks & Benefits
- **Risk to subjects:** None — no interaction, material already collected and de-identified.
- **Benefit:** Advances understanding of HSC biology and stealth-coating translational potential; no direct benefit to individual donors.
- **Risk to investigators:** Standard BSL-2 handling of human primary cells. Bloodborne pathogen training required.

## 9. Biosafety Coordination

- BSL-2 registration filed for lab. Documented in EHS system.
- All human cell work performed in BSC Class II A2.
- Sharps bins + biohazard bags for all waste streams.
- Exposure response: Stanford EHS incident hotline on-call per lab SOP.

## 10. Data Sharing
Aggregate, de-identified results published in peer-reviewed journal. No individual-level specimen data shared. Code and analysis scripts deposited publicly on GitHub at manuscript acceptance.

## 11. Attachments for Submission
- This outline expanded to full IRB narrative.
- Certificate: vendor's de-identification SOP (STEMCELL) OR Stanford Blood Center IRB documentation.
- EHS biosafety registration confirmation.
- CITI completion for blood-borne pathogens + human subjects (even if NHSR, recommended).

## 12. Timeline
- Draft to PI: week 1
- Submit to IRB: week 2
- Determination expected: 2–4 wk (NHSR fast track) or 4–6 wk (Exempt review)
- No human cells ordered until determination letter in hand (STEMCELL requires IRB documentation for research-use shipment).
