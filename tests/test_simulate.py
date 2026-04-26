"""Unit tests for the core simulator. Uses fixture allele tables so
tests run deterministically and do not depend on data/raw/ contents."""

from __future__ import annotations

import numpy as np
import pytest

from hla_sim.simulate import (
    AlleleFrequencyTable,
    match_count_per_pair,
    match_probability,
    paired_bootstrap_disparity,
    sample_individuals,
    simulate_population,
)


def make_table(population="TEST", locus="A", alleles=None, freqs=None):
    alleles = alleles or ["A*01:01", "A*02:01", "A*03:01"]
    freqs = np.asarray(freqs or [1 / 3, 1 / 3, 1 / 3])
    return AlleleFrequencyTable(
        population=population, locus=locus,
        alleles=np.asarray(alleles), freqs=freqs
    )


def test_sample_individuals_shape_and_range():
    t = make_table()
    rng = np.random.default_rng(0)
    inds = sample_individuals(t, n=100, rng=rng)
    assert inds.shape == (100, 2)
    assert inds.min() >= 0
    assert inds.max() < len(t.alleles)


def test_match_count_heterozygous_full_match():
    patient = np.array([[0, 1]])
    donor = np.array([[1, 0]])   # same multiset — full 2-match
    assert match_count_per_pair(patient, donor)[0] == 2


def test_match_count_homozygous_vs_heterozygous():
    patient = np.array([[0, 0]])  # homozygous
    donor = np.array([[0, 1]])     # one allele shared
    assert match_count_per_pair(patient, donor)[0] == 1


def test_match_count_no_match():
    patient = np.array([[0, 1]])
    donor = np.array([[2, 2]])
    assert match_count_per_pair(patient, donor)[0] == 0


def test_match_probability_monotonic_in_tau():
    # Identical fixture tables across loci; one population.
    rng = np.random.default_rng(42)
    tables = {locus: make_table(locus=locus) for locus in ("A", "B", "DRB1")}
    matches = simulate_population(tables, n_pairs=10_000, rng=rng)
    p0 = match_probability(matches, tau=0)
    p1 = match_probability(matches, tau=1)
    p2 = match_probability(matches, tau=2)
    assert 0.0 <= p0 <= p1 <= p2 <= 1.0


def test_skewed_frequency_raises_match_probability():
    """A dominant allele should increase match probability."""
    rng = np.random.default_rng(1)
    uniform = {locus: make_table(locus=locus, freqs=[1/3, 1/3, 1/3])
               for locus in ("A", "B", "DRB1")}
    skewed = {locus: make_table(locus=locus, freqs=[0.9, 0.05, 0.05])
              for locus in ("A", "B", "DRB1")}
    m_uniform = simulate_population(uniform, n_pairs=20_000, rng=rng)
    m_skewed = simulate_population(skewed, n_pairs=20_000, rng=rng)
    assert match_probability(m_skewed, tau=0) > match_probability(m_uniform, tau=0)


@pytest.mark.parametrize("tau", [0, 1, 2])
def test_match_probability_in_unit_interval(tau):
    rng = np.random.default_rng(7)
    tables = {locus: make_table(locus=locus) for locus in ("A", "B", "DRB1")}
    matches = simulate_population(tables, n_pairs=1_000, rng=rng)
    p = match_probability(matches, tau=tau)
    assert 0.0 <= p <= 1.0


def test_paired_bootstrap_disparity_returns_finite_ci():
    """Sanity check: paired bootstrap on D(τ) returns a sensible point and CI
    when one population's allele distribution is more skewed than another."""
    rng = np.random.default_rng(11)
    uniform = {locus: make_table(locus=locus, freqs=[1/3, 1/3, 1/3])
               for locus in ("A", "B", "DRB1")}
    skewed = {locus: make_table(locus=locus, freqs=[0.9, 0.05, 0.05])
              for locus in ("A", "B", "DRB1")}
    m_uniform = simulate_population(uniform, n_pairs=5_000, rng=rng)
    m_skewed = simulate_population(skewed, n_pairs=5_000, rng=rng)
    matches_by_pop = {"uniform": m_uniform, "skewed": m_skewed}
    point, lo, hi = paired_bootstrap_disparity(
        matches_by_pop, tau=2, n_boot=50, rng=rng
    )
    # Skewed population matches more often; D = max/min should exceed 1.
    assert point >= 1.0
    assert lo <= point <= hi
    assert np.isfinite(lo) and np.isfinite(hi)
