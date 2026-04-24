# Data Sources

## Primary: Allele Frequency Net Database (AFND)

**URL:** http://www.allelefrequencies.net  
**Citation:** González-Galarza FF, McCabe A, Santos EJ, et al. Allele frequency net database (AFND) 2020 update: gold-standard data classification, open access genotype data and new query tools. *Nucleic Acids Res.* 2020;48(D1):D783–D788.  
**License:** Free for academic use with attribution.

### Data we need

Per population × per locus (HLA-A, HLA-B, HLA-DRB1) at 2-field (4-digit) resolution:
- Allele name (e.g. `A*02:01`)
- Allele frequency
- Sample size

### How to download (manual, recommended path)

The AFND site's URL pattern changes; manual download is the most reliable path:

1. Go to http://www.allelefrequencies.net/hla6006a.asp
2. Under "Classical HLA Alleles" select one locus (e.g. `A`).
3. Under "Population" filter, type the target population name or select from dropdown. Recommended populations for this project:
   - **European (CEU)** — or "USA NMDP European Caucasian"
   - **Han Chinese**
   - **African American** — or "USA NMDP African American"
   - **South Asian** — or "India New Delhi"
   - **Middle Eastern** — e.g. "Saudi Arabia" or "UAE"
   - **Mexican American** — "USA NMDP Mexican or Chicano"
4. Click "Search". On the results page, use the "Export to CSV" or "Download TSV" link.
5. Rename file to `afnd_<Population>_<Locus>.tsv`, matching the format expected by the pipeline. Spaces become `_`, parentheses removed.
6. Open the file — AFND's export format may include metadata rows and column renames. Re-run the pipeline and inspect errors; adapt `normalize.py` if columns differ from the expected schema.

**Expected schema (after normalization):**

```
# comment lines starting with #
allele	frequency	sample_size
A*01:01	0.1523	1200
A*02:01	0.2947	1200
...
```

### Automated fetch

The automated fetcher in `src/hla_sim/fetch_afnd.py` is a placeholder. When reviving it, confirm the current URL pattern by hitting the search page live and inspecting the request. Respect rate limits; AFND is an academic resource run on modest infrastructure. Add a 1–2 s delay between requests.

### Provenance log

Record in this file every download:

| Date | Population | Locus | Filename | SHA-256 | Notes |
|------|-----------|-------|----------|---------|-------|
| YYYY-MM-DD | | | | | |

Compute SHA-256 with:

```bash
python -c "import hashlib, sys; print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" data/raw/afnd_*.tsv
```

## Development fallback: synthetic data

`src/hla_sim/synthetic_data.py` generates pedagogically plausible fake data so the pipeline runs end-to-end before real AFND data is in place. The headers of those files begin with `# SYNTHETIC`. Delete and replace before the manuscript reports any numbers.

## Secondary validation source (optional)

NMDP / Be The Match publishes high-resolution HLA haplotype frequency tables periodically. Could be used as a validation cross-check if AFND numbers seem off for NMDP registry-derived populations.

## Ethical note

All data used is already de-identified and aggregated at population level. No individual genotypes are handled. No IRB review required for analysis of publicly available, population-level frequency data.
