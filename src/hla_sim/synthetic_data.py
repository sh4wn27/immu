"""Generate realistic synthetic HLA allele frequency tables.

Purpose: let the whole pipeline (fetch → simulate → figures) run end-to-end
before real AFND data is in place, so development isn't blocked on data
acquisition.

These are NOT real frequencies — they are pedagogically plausible
distributions. They encode two publication-relevant stylized facts:
  1. European populations show a more even allele distribution (flatter
     tail), so match probability is higher.
  2. Certain non-European populations show more unique/rare alleles, so
     match probability is lower at strict thresholds.

Real AFND data should replace these before anything is reported or plotted
for the manuscript. The `data/raw/SOURCES.md` file documents the swap.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import DEFAULT_POPULATIONS, LOCI


# Per-locus approximate number of alleles typically observed at 2-field
# resolution in AFND gold-standard tables.
LOCUS_N_ALLELES = {"A": 40, "B": 60, "C": 35, "DRB1": 35}

# Population-specific Zipfian decay exponent κ for the synthetic
# allele-frequency distribution f_i ∝ i^{−κ}. Higher κ → more
# concentration on a handful of common alleles → higher match
# probability. Tuned so the downstream Monte-Carlo across HLA-A/B/DRB1
# produces empirically plausible 6/6 strict match probabilities
# (~1.2% European down to ~0.1% African American).
POP_KAPPA = {
    "European (CEU)":   2.10,
    "Han Chinese":      2.00,
    "Mexican American": 1.90,
    "Middle Eastern":   1.78,
    "South Asian":      1.65,
    "African American": 1.55,
}

# Backwards-compat: still expose the prior Dirichlet-style alpha names
# in case external scripts reference them. Not used by the new generator.
POP_CONCENTRATION = POP_KAPPA

# Approximate AFND gold-standard sample sizes (number of typed individuals)
# used in TSV headers; values are within the realistic range for each
# population's largest gold-standard study.
POP_SAMPLE_SIZE = {
    "European (CEU)":   2486,
    "Han Chinese":      1792,
    "African American": 1235,
    "Mexican American":  947,
    "South Asian":       856,
    "Middle Eastern":    712,
}


@dataclass(frozen=True)
class SyntheticFrequencyConfig:
    population: str
    locus: str
    n_alleles: int
    concentration: float


def draw_frequencies(cfg: SyntheticFrequencyConfig, rng: np.random.Generator) -> np.ndarray:
    """Build a Zipfian allele-frequency vector with light jitter.

    f_i ∝ i^{−κ}, then multiplied by a small lognormal perturbation
    drawn from rng (so two populations with the same κ still differ
    in detail). κ is read from cfg.concentration. Result is normalized
    to sum to 1.
    """
    kappa = cfg.concentration
    base = np.arange(1, cfg.n_alleles + 1, dtype=float) ** (-kappa)
    jitter = rng.lognormal(mean=0.0, sigma=0.05, size=cfg.n_alleles)
    f = base * jitter
    return f / f.sum()


def allele_name(locus: str, idx: int) -> str:
    """Fake but AFND-style 2-field allele name, e.g. A*01:01."""
    major = 1 + (idx // 99)
    minor = 1 + (idx % 99)
    return f"{locus}*{major:02d}:{minor:02d}"


def write_table(
    path: Path,
    cfg: SyntheticFrequencyConfig,
    freqs: np.ndarray,
    sample_size: int = 200,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# SYNTHETIC allele frequency table — NOT REAL DATA\n"
        f"# population: {cfg.population}\n"
        f"# locus: HLA-{cfg.locus}\n"
        f"# n_alleles: {cfg.n_alleles}\n"
        f"# concentration: {cfg.concentration}\n"
        f"# generator: hla_sim.synthetic_data\n"
        f"# WARNING: replace with AFND data before publishing\n"
        f"allele\tfrequency\tsample_size\n"
    )
    lines = [
        f"{allele_name(cfg.locus, i)}\t{freqs[i]:.6f}\t{sample_size}"
        for i in range(cfg.n_alleles)
    ]
    path.write_text(header + "\n".join(lines) + "\n")


def generate_all(
    populations=DEFAULT_POPULATIONS,
    loci=LOCI,
    out_dir: Path = Path("data/raw"),
    seed: int = 20260424,
) -> list[Path]:
    rng = np.random.default_rng(seed)
    paths = []
    for pop in populations:
        alpha = POP_CONCENTRATION.get(pop, 0.30)
        sample_size = POP_SAMPLE_SIZE.get(pop, 1000)
        for locus in loci:
            cfg = SyntheticFrequencyConfig(
                population=pop, locus=locus,
                n_alleles=LOCUS_N_ALLELES[locus], concentration=alpha,
            )
            freqs = draw_frequencies(cfg, rng)
            safe = pop.replace(" ", "_").replace("(", "").replace(")", "")
            path = out_dir / f"afnd_{safe}_{locus}.tsv"
            write_table(path, cfg, freqs, sample_size=sample_size)
            paths.append(path)
    return paths


def main() -> None:
    # Generate the primary three-locus set plus HLA-C, which is needed
    # for the sensitivity analysis comparing 6/6 vs. 8/8 matching.
    paths = generate_all(loci=("A", "B", "C", "DRB1"))
    print(f"Wrote {len(paths)} synthetic allele tables to data/raw/")
    for p in paths:
        print(f"  {p.name}")
    print("\nWARNING: these are NOT real frequencies. Replace with AFND data "
          "before reporting results. See data/raw/SOURCES.md.")


if __name__ == "__main__":
    main()
