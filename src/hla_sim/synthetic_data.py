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
# resolution in AFND data, coarse order-of-magnitude only.
LOCUS_N_ALLELES = {"A": 40, "B": 60, "DRB1": 35}

# Population-level concentration parameter for a Dirichlet prior over allele
# frequencies. Higher alpha → flatter distribution → easier matches.
# Values chosen to produce plausible rank-order of match probability
# (European ~ high, Middle Eastern / Hispanic mid, African lower at strict τ).
POP_CONCENTRATION = {
    "European (CEU)": 1.6,
    "Han Chinese": 1.2,
    "African American": 0.7,
    "South Asian": 1.0,
    "Middle Eastern": 1.1,
    "Mexican American": 1.3,
}


@dataclass(frozen=True)
class SyntheticFrequencyConfig:
    population: str
    locus: str
    n_alleles: int
    concentration: float


def draw_frequencies(cfg: SyntheticFrequencyConfig, rng: np.random.Generator) -> np.ndarray:
    """Draw a frequency vector from a Dirichlet(alpha, ..., alpha)."""
    alpha = np.full(cfg.n_alleles, cfg.concentration)
    return rng.dirichlet(alpha)


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
        alpha = POP_CONCENTRATION.get(pop, 1.0)
        for locus in loci:
            cfg = SyntheticFrequencyConfig(
                population=pop, locus=locus,
                n_alleles=LOCUS_N_ALLELES[locus], concentration=alpha,
            )
            freqs = draw_frequencies(cfg, rng)
            safe = pop.replace(" ", "_").replace("(", "").replace(")", "")
            path = out_dir / f"afnd_{safe}_{locus}.tsv"
            write_table(path, cfg, freqs)
            paths.append(path)
    return paths


def main() -> None:
    paths = generate_all()
    print(f"Wrote {len(paths)} synthetic allele tables to data/raw/")
    for p in paths:
        print(f"  {p.name}")
    print("\nWARNING: these are NOT real frequencies. Replace with AFND data "
          "before reporting results. See data/raw/SOURCES.md.")


if __name__ == "__main__":
    main()
