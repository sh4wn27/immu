"""Monte-Carlo HLA match-probability simulator.

Core model:
  - Each individual carries two alleles per locus, drawn independently from
    that population's AFND frequency distribution (Hardy-Weinberg).
  - A "patient" and a "donor" are drawn from the same population.
  - Match is counted at the allele level per locus; two alleles per locus
    contribute to a 6-count max (A×2 + B×2 + DRB1×2).
  - Coating tolerance parameter τ: the graft is functionally matched if
    the mismatch count ≤ τ. τ=0 is strict 6/6; τ=2 lets two allele
    mismatches slide.

Linkage disequilibrium is NOT modeled — alleles are drawn independently
across loci. This is a documented limitation (see PROJECT_PLAN.md §7).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from . import LOCI, SEED


@dataclass(frozen=True)
class AlleleFrequencyTable:
    """Alleles and probabilities for one population × one locus."""

    population: str
    locus: str
    alleles: np.ndarray   # shape (n_alleles,), dtype=object (strings)
    freqs: np.ndarray     # shape (n_alleles,), normalized to sum=1

    @classmethod
    def from_tsv(cls, path: Path) -> "AlleleFrequencyTable":
        df = pd.read_csv(path, sep="\t", comment="#")
        if df.empty:
            raise ValueError(
                f"Empty allele table at {path}. Run `python -m hla_sim.fetch_afnd` "
                f"and populate real AFND data first."
            )
        freqs = df["frequency"].to_numpy(dtype=float)
        freqs = freqs / freqs.sum()
        # Parse population and locus from filename: afnd_<pop>_<locus>.tsv
        stem = path.stem.split("_", 1)[1]
        pop, locus = stem.rsplit("_", 1)
        return cls(population=pop.replace("_", " "),
                   locus=locus,
                   alleles=df["allele"].to_numpy(),
                   freqs=freqs)


def sample_individuals(
    table: AlleleFrequencyTable, n: int, rng: np.random.Generator
) -> np.ndarray:
    """Draw n diploid individuals → array shape (n, 2) of allele indices."""
    return rng.choice(len(table.alleles), size=(n, 2), p=table.freqs)


def match_count_per_pair(patient: np.ndarray, donor: np.ndarray) -> np.ndarray:
    """Count allele matches per pair across 2 alleles at one locus.

    Each individual has 2 alleles. A locus can match 0, 1, or 2 alleles.
    We use a multiset intersection so homozygous patients and donors
    count correctly.
    """
    # patient, donor shape (n, 2) of allele indices
    n = patient.shape[0]
    out = np.zeros(n, dtype=np.int8)
    # Vectorized multiset intersection of size 2
    # Match patterns: sort each row, compare
    p = np.sort(patient, axis=1)
    d = np.sort(donor, axis=1)
    both_match = (p[:, 0] == d[:, 0]) & (p[:, 1] == d[:, 1])
    cross_match = (p[:, 0] == d[:, 1]) & (p[:, 1] == d[:, 0])
    any_two = both_match | cross_match
    any_one = (
        (p[:, 0] == d[:, 0])
        | (p[:, 0] == d[:, 1])
        | (p[:, 1] == d[:, 0])
        | (p[:, 1] == d[:, 1])
    )
    out[any_one] = 1
    out[any_two] = 2
    return out


def simulate_population(
    tables: dict[str, AlleleFrequencyTable],
    n_pairs: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Simulate n_pairs patient-donor pairs; return per-pair match counts.

    Returns:
        array shape (n_pairs, n_loci) with values in {0, 1, 2}.
    """
    loci = [tables[l] for l in LOCI]
    per_locus = []
    for table in loci:
        patient = sample_individuals(table, n_pairs, rng)
        donor = sample_individuals(table, n_pairs, rng)
        per_locus.append(match_count_per_pair(patient, donor))
    return np.stack(per_locus, axis=1)  # (n_pairs, n_loci)


def match_probability(
    matches: np.ndarray, tau: int = 0
) -> float:
    """Fraction of pairs with total_mismatch ≤ tau across all loci."""
    total_matches = matches.sum(axis=1)  # out of 6
    mismatches = 6 - total_matches
    return float((mismatches <= tau).mean())


def bootstrap_ci(
    matches: np.ndarray, tau: int, n_boot: int, rng: np.random.Generator
) -> tuple[float, float, float]:
    """95% bootstrap CI on match probability at tolerance τ."""
    n = matches.shape[0]
    estimates = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        estimates[i] = match_probability(matches[idx], tau=tau)
    point = match_probability(matches, tau=tau)
    lo, hi = np.quantile(estimates, [0.025, 0.975])
    return point, float(lo), float(hi)


def run_all_populations(
    populations: list[str],
    data_dir: Path = Path("data/raw"),
    n_pairs: int = 100_000,
    n_boot: int = 500,
    seed: int = SEED,
) -> pd.DataFrame:
    """End-to-end: load data for each population, simulate, return tidy DF.

    Columns: population, tau, match_prob, ci_lo, ci_hi.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for pop in populations:
        try:
            tables = {
                locus: AlleleFrequencyTable.from_tsv(
                    data_dir / f"afnd_{pop.replace(' ', '_').replace('(','').replace(')','')}_{locus}.tsv"
                )
                for locus in LOCI
            }
        except ValueError as err:
            print(f"Skipping {pop}: {err}")
            continue
        matches = simulate_population(tables, n_pairs=n_pairs, rng=rng)
        for tau in (0, 1, 2):
            point, lo, hi = bootstrap_ci(matches, tau=tau, n_boot=n_boot, rng=rng)
            rows.append(
                dict(population=pop, tau=tau, match_prob=point, ci_lo=lo, ci_hi=hi)
            )
    return pd.DataFrame(rows)


def disparity_ratio(results: pd.DataFrame, tau: int) -> float:
    """Max match prob / min match prob at a given τ, across populations."""
    sub = results[results["tau"] == tau]
    if sub.empty:
        return float("nan")
    return float(sub["match_prob"].max() / max(sub["match_prob"].min(), 1e-9))


def main() -> None:
    from . import DEFAULT_POPULATIONS

    results = run_all_populations(list(DEFAULT_POPULATIONS))
    out = Path("data/derived")
    out.mkdir(parents=True, exist_ok=True)
    path = out / "match_results.csv"
    results.to_csv(path, index=False)
    print(results.to_string(index=False))
    for tau in (0, 1, 2):
        print(f"Disparity ratio at τ={tau}: {disparity_ratio(results, tau):.2f}")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
