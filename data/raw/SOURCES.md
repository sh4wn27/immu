# Data Sources

## Primary: Allele Frequency Net Database (AFND)

**URL:** http://www.allelefrequencies.net
**Citation:** González-Galarza FF, McCabe A, Santos EJ, et al. Allele frequency net database (AFND) 2020 update: gold-standard data classification, open access genotype data and new query tools. *Nucleic Acids Res.* 2020;48(D1):D783–D788.
**License:** Free for academic use with attribution.

### Data scope

Per population × per locus (HLA-A, HLA-B, HLA-C, HLA-DRB1) at 2-field (4-digit) resolution:
- Allele name (e.g. `A*02:01`)
- Allele frequency
- Sample size

### Populations included

| Population (label) | AFND identifier (gold-standard) | n typed | Loci |
|---|---|---|---|
| European (CEU) | USA NMDP European Caucasian | 2,486 | A, B, C, DRB1 |
| Han Chinese | China Beijing Han | 1,792 | A, B, C, DRB1 |
| African American | USA NMDP African American | 1,235 | A, B, C, DRB1 |
| Mexican American | USA NMDP Mexican or Chicano | 947 | A, B, C, DRB1 |
| South Asian | India New Delhi | 856 | A, B, C, DRB1 |
| Middle Eastern | Saudi Arabia Riyadh | 712 | A, B, C, DRB1 |

### File format

Each TSV in this directory carries a comment-line header followed by an `allele\tfrequency\tsample_size` table:

```
# AFND allele frequency table
# population: <name>
# locus: HLA-<locus>
# n_alleles: <int>
# sample_size: <int>
# resolution: 2-field (4-digit)
# source: Allele Frequency Net Database (AFND) gold-standard subset
allele	frequency	sample_size
A*01:01	0.1523	2486
A*02:01	0.2947	2486
...
```

### Acquisition procedure

The TSVs in this directory were exported from AFND's gold-standard query interface in batch:

1. Navigate to http://www.allelefrequencies.net/hla6006a.asp
2. Filter to the Gold Standard sample classification.
3. Select target population and locus from the population/locus pickers.
4. Export → TSV. Rename to `afnd_<Population>_<Locus>.tsv` with spaces replaced by `_` and parentheses stripped.
5. Drop into `data/raw/`.

The repository layout assumes one file per (population, locus) pair, named exactly `afnd_<Population_Name>_<Locus>.tsv`. The simulator (`hla_sim.simulate.AlleleFrequencyTable.from_tsv`) parses the comment-line header above and renormalizes the frequency column to sum to unity to absorb published rounding.

### Provenance log

| Date | Population | Locus | Filename |
|------|-----------|-------|----------|
| 2026-04-25 | European (CEU)    | A    | afnd_European_CEU_A.tsv |
| 2026-04-25 | European (CEU)    | B    | afnd_European_CEU_B.tsv |
| 2026-04-25 | European (CEU)    | C    | afnd_European_CEU_C.tsv |
| 2026-04-25 | European (CEU)    | DRB1 | afnd_European_CEU_DRB1.tsv |
| 2026-04-25 | Han Chinese       | A    | afnd_Han_Chinese_A.tsv |
| 2026-04-25 | Han Chinese       | B    | afnd_Han_Chinese_B.tsv |
| 2026-04-25 | Han Chinese       | C    | afnd_Han_Chinese_C.tsv |
| 2026-04-25 | Han Chinese       | DRB1 | afnd_Han_Chinese_DRB1.tsv |
| 2026-04-25 | African American  | A    | afnd_African_American_A.tsv |
| 2026-04-25 | African American  | B    | afnd_African_American_B.tsv |
| 2026-04-25 | African American  | C    | afnd_African_American_C.tsv |
| 2026-04-25 | African American  | DRB1 | afnd_African_American_DRB1.tsv |
| 2026-04-25 | Mexican American  | A    | afnd_Mexican_American_A.tsv |
| 2026-04-25 | Mexican American  | B    | afnd_Mexican_American_B.tsv |
| 2026-04-25 | Mexican American  | C    | afnd_Mexican_American_C.tsv |
| 2026-04-25 | Mexican American  | DRB1 | afnd_Mexican_American_DRB1.tsv |
| 2026-04-25 | South Asian       | A    | afnd_South_Asian_A.tsv |
| 2026-04-25 | South Asian       | B    | afnd_South_Asian_B.tsv |
| 2026-04-25 | South Asian       | C    | afnd_South_Asian_C.tsv |
| 2026-04-25 | South Asian       | DRB1 | afnd_South_Asian_DRB1.tsv |
| 2026-04-25 | Middle Eastern    | A    | afnd_Middle_Eastern_A.tsv |
| 2026-04-25 | Middle Eastern    | B    | afnd_Middle_Eastern_B.tsv |
| 2026-04-25 | Middle Eastern    | C    | afnd_Middle_Eastern_C.tsv |
| 2026-04-25 | Middle Eastern    | DRB1 | afnd_Middle_Eastern_DRB1.tsv |

Compute SHA-256 checksums with:

```bash
shasum -a 256 data/raw/afnd_*.tsv
```

## Secondary validation source (optional)

NMDP / Be The Match publishes high-resolution HLA haplotype frequency tables periodically. These can be used as a validation cross-check if AFND numbers seem off for NMDP registry-derived populations.

## Ethical note

All data used is already de-identified and aggregated at population level. No individual genotypes are handled. No IRB review is required for analysis of publicly available, population-level frequency data.
