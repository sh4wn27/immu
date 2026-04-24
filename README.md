# HLA Equity Simulation

A population-genetics Monte-Carlo model of how partial HLA mismatch tolerance — the kind biodegradable stealth-polymer coatings on donor HSCs would provide — expands the matched-donor pool, with special attention to ethnic equity.

**Author:** Huanxuan (Shawn) Li, TJHSST.  
**Target publication:** Journal of Emerging Investigators.  
**Status:** early development.

## Quickstart

```bash
# Python 3.11+ recommended
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Fetch HLA allele frequencies from AFND (once)
python -m hla_sim.fetch_afnd

# Run the full simulation
python -m hla_sim.simulate

# Regenerate all figures in the paper
python -m hla_sim.make_figures
```

## Project structure

```
docs/
  PROJECT_PLAN.md      ← read this first
  manuscript/          ← paper draft in Markdown
  _archive/            ← inactive prior plan (wet-lab pivot, retained for context)
src/
  hla_sim/             ← simulation package
tests/
  ...
data/                  ← AFND downloads + processed frequencies
notebooks/             ← exploratory work
```

## Citation

If you use or adapt this work, cite:

> Li, H. (2026). *Modeling the equity impact of partial HLA mismatch tolerance via biodegradable stealth coatings: a population-genetics simulation.* [manuscript in preparation].

Underlying allele-frequency data: González-Galarza FF et al. (2020) *Nucleic Acids Res* 48: D783–D788 (Allele Frequency Net Database).

## License

Code: MIT. Data: per AFND terms (academic use, attribution required).
