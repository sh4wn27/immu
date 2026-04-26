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
    loci: tuple[str, ...] = None,
) -> np.ndarray:
    """Simulate n_pairs patient-donor pairs; return per-pair match counts.

    Args:
        tables: {locus_name: AlleleFrequencyTable}.
        n_pairs: number of patient–donor pairs to draw.
        rng: numpy Generator.
        loci: which loci to use (defaults to package-level LOCI).

    Returns:
        array shape (n_pairs, n_loci) with values in {0, 1, 2}.
    """
    if loci is None:
        loci = LOCI
    per_locus = []
    for locus_name in loci:
        table = tables[locus_name]
        patient = sample_individuals(table, n_pairs, rng)
        donor = sample_individuals(table, n_pairs, rng)
        per_locus.append(match_count_per_pair(patient, donor))
    return np.stack(per_locus, axis=1)  # (n_pairs, n_loci)


def match_probability(
    matches: np.ndarray, tau: int = 0
) -> float:
    """Fraction of pairs with total_mismatch ≤ tau pooled across all loci.

    Maximum match count is 2 × n_loci. Default LOCI gives a 6-cap.
    """
    n_loci = matches.shape[1]
    max_match = 2 * n_loci
    total_matches = matches.sum(axis=1)
    mismatches = max_match - total_matches
    return float((mismatches <= tau).mean())


def match_probability_per_locus(
    matches: np.ndarray, tau_per_locus: int = 0
) -> float:
    """Fraction of pairs in which mismatch ≤ τ at EVERY locus.

    Alternative tolerance definition: rather than pooling allowed
    mismatches across loci, require each locus to be within τ on its
    own. More permissive than pooled-τ for τ > 0.
    """
    per_locus_mm = 2 - matches  # mismatches at each locus (0, 1, or 2)
    return float((per_locus_mm <= tau_per_locus).all(axis=1).mean())


def hwe_homozygosity(freqs: np.ndarray) -> float:
    """Closed-form Σ f_i² (homozygosity coefficient F).

    Under HWE, F is also the probability that two independent random
    allele draws from the population are identical. This is the
    cleanest closed-form quantity to validate the simulator against:
    take one allele from the patient and one from the donor; the
    probability of identity is exactly F.
    """
    return float(np.sum(freqs ** 2))


def hwe_full_match_per_locus(freqs: np.ndarray) -> float:
    """Closed-form P(m_l = 2): two HWE diploids are identical at locus.

    Combines the two homozygous-and-equal and heterozygous-and-equal
    cases:
        P(m_l = 2) = Σ f^4 + 4 Σ_{i<j} f_i^2 f_j^2 = 2(Σ f²)² − Σ f^4.
    """
    s2 = float(np.sum(freqs ** 2))
    s4 = float(np.sum(freqs ** 4))
    return 2.0 * s2 ** 2 - s4


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
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """End-to-end: load data for each population, simulate, return tidy DFs.

    Returns:
        (per_population_results, disparity_results)
        per_population_results columns: population, tau, match_prob, ci_lo, ci_hi.
        disparity_results columns: tau, disparity, ci_lo, ci_hi.
    """
    rng = np.random.default_rng(seed)
    rows = []
    matches_by_pop: dict[str, np.ndarray] = {}
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
        matches_by_pop[pop] = matches
        for tau in (0, 1, 2):
            point, lo, hi = bootstrap_ci(matches, tau=tau, n_boot=n_boot, rng=rng)
            rows.append(
                dict(population=pop, tau=tau, match_prob=point, ci_lo=lo, ci_hi=hi)
            )
    per_pop = pd.DataFrame(rows)

    disparity_rows = []
    for tau in (0, 1, 2):
        point, lo, hi = paired_bootstrap_disparity(
            matches_by_pop, tau=tau, n_boot=n_boot, rng=rng
        )
        disparity_rows.append(
            dict(tau=tau, disparity=point, ci_lo=lo, ci_hi=hi)
        )
    disparity = pd.DataFrame(disparity_rows)
    return per_pop, disparity


def disparity_ratio(results: pd.DataFrame, tau: int) -> float:
    """Max match prob / min match prob at a given τ, across populations."""
    sub = results[results["tau"] == tau]
    if sub.empty:
        return float("nan")
    return float(sub["match_prob"].max() / max(sub["match_prob"].min(), 1e-9))


def paired_bootstrap_disparity(
    matches_by_pop: dict[str, np.ndarray],
    tau: int,
    n_boot: int,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    """Paired-bootstrap CI on D(τ) preserving cross-population correlation.

    Resamples row indices ONCE per bootstrap iteration and applies them to
    every population's match matrix. Yields tighter, more accurate
    intervals than independent per-population resampling, because the
    same simulated sampling variance enters numerator and denominator.
    """
    pops = list(matches_by_pop)
    if not pops:
        return (float("nan"), float("nan"), float("nan"))
    n = matches_by_pop[pops[0]].shape[0]
    point_probs = [match_probability(matches_by_pop[p], tau=tau) for p in pops]
    point = max(point_probs) / max(min(point_probs), 1e-9)
    estimates = np.empty(n_boot)
    for i in range(n_boot):
        idx = rng.integers(0, n, size=n)
        boot = [match_probability(matches_by_pop[p][idx], tau=tau) for p in pops]
        estimates[i] = max(boot) / max(min(boot), 1e-9)
    lo, hi = np.quantile(estimates, [0.025, 0.975])
    return float(point), float(lo), float(hi)


def main() -> None:
    from . import DEFAULT_POPULATIONS

    per_pop, disparity = run_all_populations(list(DEFAULT_POPULATIONS))
    out = Path("data/derived")
    out.mkdir(parents=True, exist_ok=True)
    pop_path = out / "match_results.csv"
    disp_path = out / "disparity_results.csv"
    per_pop.to_csv(pop_path, index=False)
    disparity.to_csv(disp_path, index=False)
    print(per_pop.to_string(index=False))
    print()
    print("Paired-bootstrap disparity ratio:")
    print(disparity.to_string(index=False))
    print(f"Wrote {pop_path} and {disp_path}")


if __name__ == "__main__":
    main()
