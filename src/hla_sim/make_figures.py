"""Regenerate every figure referenced in the manuscript.

Usage:
    python -m hla_sim.make_figures

Reads data/derived/match_results.csv (produced by `hla_sim.simulate`).
Writes PDFs into docs/manuscript/figures/.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from . import DEFAULT_POPULATIONS, LOCI

FIG_DIR = Path("docs/manuscript/figures")
RESULTS = Path("data/derived/match_results.csv")
RAW_DIR = Path("data/raw")


def _setup():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 140,
    })
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def figure_schematic() -> Path:
    """Figure 1: concept schematic of mismatch → coating → simulation.

    Three-row layout: (a) classical mismatch leads to GvHD;
    (b) stealth-coated graft enables tolerance; (c) population-genetics
    abstraction this work models.
    """
    from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
    fig, ax = plt.subplots(figsize=(8.5, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def cell(cx, cy, color_epis, ring=False):
        c = Circle((cx, cy), 0.45, facecolor="white",
                   edgecolor="black", linewidth=1.4, zorder=2)
        ax.add_patch(c)
        # 6 epitope dots around the rim
        import numpy as _np
        for theta in _np.linspace(0, 2 * _np.pi, 6, endpoint=False):
            ex = cx + 0.34 * _np.cos(theta)
            ey = cy + 0.34 * _np.sin(theta)
            ax.add_patch(Circle((ex, ey), 0.07, facecolor=color_epis,
                                edgecolor="black", linewidth=0.4, zorder=3))
        if ring:
            ax.add_patch(Circle((cx, cy), 0.62, facecolor="none",
                                edgecolor="#3a8ac0", linewidth=1.6,
                                linestyle=(0, (4, 2)), zorder=2))

    def box(cx, cy, w, h, text, fill="#f6f6f6", edge="#444444"):
        bb = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                            boxstyle="round,pad=0.04,rounding_size=0.15",
                            facecolor=fill, edgecolor=edge, linewidth=1.2,
                            zorder=2)
        ax.add_patch(bb)
        ax.text(cx, cy, text, ha="center", va="center", fontsize=9, zorder=3)

    def arrow(x0, y0, x1, y1, label=None):
        a = FancyArrowPatch((x0, y0), (x1, y1),
                            arrowstyle="-|>", mutation_scale=10,
                            linewidth=1.4, color="#222222", zorder=1)
        ax.add_patch(a)
        if label:
            mx, my = (x0 + x1) / 2, (y0 + y1) / 2 + 0.18
            ax.text(mx, my, label, ha="center", fontsize=8)

    # Row (a): classical mismatch → GvHD
    ax.text(5, 9.4, "(a) Classical strict matching",
            ha="center", fontsize=11, fontweight="bold")
    cell(2, 8.2, "#cc3333"); ax.text(2, 7.4, "donor HSC", ha="center", fontsize=8)
    cell(5, 8.2, "#e07a2a"); ax.text(5, 7.4, "recipient", ha="center", fontsize=8)
    box(8, 8.2, 2, 1.0, "GvHD\nrejection", fill="#fde8e8", edge="#a02828")
    arrow(2.5, 8.2, 4.5, 8.2, label="HLA mismatch")
    arrow(5.5, 8.2, 7.0, 8.2)

    # Row (b): coated → tolerance
    ax.text(5, 6.0, "(b) Stealth-coated graft (tolerance $\\tau$)",
            ha="center", fontsize=11, fontweight="bold")
    cell(2, 4.8, "#f0aaaa", ring=True)
    ax.text(2, 4.0, "coated donor", ha="center", fontsize=8)
    cell(5, 4.8, "#e07a2a")
    ax.text(5, 4.0, "recipient", ha="center", fontsize=8)
    box(8, 4.8, 2, 1.0, "tolerated\nengraftment", fill="#e3f3df", edge="#3f7a3f")
    arrow(2.5, 4.8, 4.5, 4.8, label="epitopes masked")
    arrow(5.5, 4.8, 7.0, 4.8)

    # Row (c): population abstraction
    ax.text(5, 2.6, "(c) Population-level abstraction (this work)",
            ha="center", fontsize=11, fontweight="bold")
    box(1.7, 1.4, 2.6, 1.0, "AFND allele\nfrequencies $f^{(p,\\ell)}_k$")
    box(5.0, 1.4, 2.6, 1.0, "Monte-Carlo\npatient–donor pairs")
    box(8.3, 1.4, 2.6, 1.0,
        "$P(\\mathrm{match}\\mid\\tau, p)$;\nDisparity $D(\\tau)$",
        fill="#fff7d6", edge="#9a7d1d")
    arrow(3.0, 1.4, 3.7, 1.4)
    arrow(6.3, 1.4, 7.0, 1.4)

    fig.tight_layout()
    out = FIG_DIR / "fig1_schematic.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)
    return out


def _shannon_entropy(freqs: np.ndarray) -> float:
    """Shannon entropy in bits of an allele-frequency vector."""
    p = freqs[freqs > 0]
    return float(-(p * np.log2(p)).sum())


def figure_allele_entropy(out_dir: Path = RAW_DIR) -> Path:
    """Figure 2: per-locus Shannon entropy by population."""
    from .simulate import AlleleFrequencyTable
    rows = []
    for pop in DEFAULT_POPULATIONS:
        safe = pop.replace(" ", "_").replace("(", "").replace(")", "")
        for locus in LOCI:
            path = out_dir / f"afnd_{safe}_{locus}.tsv"
            if not path.exists():
                continue
            table = AlleleFrequencyTable.from_tsv(path)
            rows.append({"population": pop, "locus": locus,
                         "entropy": _shannon_entropy(table.freqs)})
    df = pd.DataFrame(rows)
    pivot = df.pivot(index="population", columns="locus", values="entropy")
    pivot = pivot.reindex(DEFAULT_POPULATIONS)[list(LOCI)]

    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    im = ax.imshow(pivot.values, aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(len(LOCI)))
    ax.set_xticklabels([f"HLA-{l}" for l in LOCI])
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            ax.text(j, i, f"{pivot.values[i, j]:.2f}",
                    ha="center", va="center", fontsize=8,
                    color="black" if pivot.values[i, j] < pivot.values.mean() else "white")
    fig.colorbar(im, ax=ax, label="Shannon entropy (bits)")
    ax.set_title("HLA allele-frequency diversity by population and locus")
    fig.tight_layout()
    out = FIG_DIR / "fig2_allele_entropy.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)
    return out


def figure_match_by_population(results: pd.DataFrame) -> Path:
    """Figure 3/4 combined: match probability at τ=0,1,2 by population."""
    fig, ax = plt.subplots(figsize=(7, 4.2))
    pops = list(DEFAULT_POPULATIONS)
    width = 0.25
    x = np.arange(len(pops))
    colors = ["#2a5780", "#6aa3d5", "#c8dcec"]
    for i, tau in enumerate([0, 1, 2]):
        sub = (results[results["tau"] == tau]
               .set_index("population").reindex(pops).reset_index())
        yerr = [sub["match_prob"] - sub["ci_lo"], sub["ci_hi"] - sub["match_prob"]]
        ax.bar(
            x + (i - 1) * width, sub["match_prob"], width,
            yerr=yerr, capsize=3, color=colors[i],
            label=f"τ = {tau} mismatches allowed",
        )
    ax.set_xticks(x)
    ax.set_xticklabels(pops, rotation=25, ha="right")
    ax.set_ylabel("Match probability (6/6 = full match)")
    ax.set_ylim(0, max(0.02, results["ci_hi"].max() * 1.15))
    ax.legend(frameon=False, loc="upper right")
    ax.set_title("HLA match probability by population and coating tolerance τ")
    fig.tight_layout()
    out = FIG_DIR / "fig3_match_by_population.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)
    return out


def figure_disparity_ratio(results: pd.DataFrame) -> Path:
    """Figure 4: disparity ratio (max/min match prob across populations) vs τ."""
    taus = sorted(results["tau"].unique())
    ratios = []
    for tau in taus:
        sub = results[results["tau"] == tau]
        ratios.append(sub["match_prob"].max() / max(sub["match_prob"].min(), 1e-9))
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    ax.plot(taus, ratios, "o-", color="#a3324e", linewidth=2)
    ax.set_xticks(taus)
    ax.set_xlabel("Coating tolerance τ (allowed mismatches)")
    ax.set_ylabel("Disparity ratio (max / min across populations)")
    ax.set_title("Equity gap shrinks as coating tolerance increases")
    ax.grid(alpha=0.25)
    for x, y in zip(taus, ratios):
        ax.annotate(f"{y:.2f}", (x, y), xytext=(0, 8),
                    textcoords="offset points", ha="center", fontsize=9)
    fig.tight_layout()
    out = FIG_DIR / "fig4_disparity_ratio.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)
    return out


def figure_pool_expansion(results: pd.DataFrame) -> Path:
    """Figure 4b: absolute pool expansion vs τ per population."""
    pops = list(DEFAULT_POPULATIONS)
    fig, ax = plt.subplots(figsize=(6.5, 4))
    baseline = {
        p: float(results[(results["population"] == p) & (results["tau"] == 0)]
                 ["match_prob"].iloc[0])
        for p in pops if p in results["population"].values
    }
    for p in baseline:
        sub = (results[results["population"] == p]
               .sort_values("tau"))
        expansion = sub["match_prob"] - baseline[p]
        ax.plot(sub["tau"], expansion, "o-", label=p, linewidth=1.8)
    ax.set_xlabel("Coating tolerance τ")
    ax.set_ylabel("Match probability increase vs τ=0 baseline")
    ax.set_title("Absolute donor-pool expansion under coating")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.tight_layout()
    out = FIG_DIR / "fig4_pool_expansion.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)
    return out


def _disparity_from_probs(probs: list[float]) -> float:
    return max(probs) / max(min(probs), 1e-9)


def _run_per_pop_at_taus(
    n_pairs: int,
    loci: tuple[str, ...],
    seed: int,
    per_locus_tau: bool = False,
    ld_block_strength: float = 0.0,
) -> dict[str, dict[int, float]]:
    """Re-run the simulator under a particular config; return
    {pop: {tau: match_prob}}."""
    from .simulate import (
        AlleleFrequencyTable, simulate_population,
        match_probability, match_probability_per_locus,
    )
    rng = np.random.default_rng(seed)
    out: dict[str, dict[int, float]] = {}
    for pop in DEFAULT_POPULATIONS:
        safe = pop.replace(" ", "_").replace("(", "").replace(")", "")
        try:
            tables = {
                locus: AlleleFrequencyTable.from_tsv(
                    RAW_DIR / f"afnd_{safe}_{locus}.tsv"
                )
                for locus in loci
            }
        except (FileNotFoundError, ValueError):
            continue
        matches = simulate_population(tables, n_pairs=n_pairs, rng=rng, loci=loci)
        if ld_block_strength > 0:
            # Coarse positive-LD distortion: pairs that match at locus 0
            # are made more likely to also match at locus 1, mimicking
            # block-haplotype carrying. Implemented by replacing a fraction
            # of locus-1 mismatched rows with full-match outcomes.
            n_loci = matches.shape[1]
            for li in range(1, n_loci):
                shared0 = matches[:, 0] >= 1
                bump = (
                    shared0
                    & (matches[:, li] < 2)
                    & (rng.random(matches.shape[0]) < ld_block_strength)
                )
                matches[bump, li] = 2
        prob_fn = match_probability_per_locus if per_locus_tau else match_probability
        out[pop] = {tau: prob_fn(matches, tau) for tau in (0, 1, 2)}
    return out


def figure_sensitivity(results: pd.DataFrame) -> Path:
    """Figure 5: 2x2 sensitivity panels with real re-runs of the simulator."""
    pops = list(DEFAULT_POPULATIONS)
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.5))

    # Baseline disparity from the main run for overlay reference.
    base_d = {tau: results[results["tau"] == tau]["match_prob"].max()
              / max(results[results["tau"] == tau]["match_prob"].min(), 1e-9)
              for tau in (0, 1, 2)}

    # Panel (a): add HLA-C
    add_c = _run_per_pop_at_taus(
        n_pairs=50_000, loci=("A", "B", "C", "DRB1"), seed=20260424,
    )
    a_d = {tau: _disparity_from_probs([add_c[p][tau] for p in pops if p in add_c])
           for tau in (0, 1, 2)}

    # Panel (b): halved N
    halved = _run_per_pop_at_taus(
        n_pairs=50_000, loci=("A", "B", "DRB1"), seed=20260424 + 1,
    )
    b_d = {tau: _disparity_from_probs([halved[p][tau] for p in pops if p in halved])
           for tau in (0, 1, 2)}

    # Panel (c): per-locus τ
    perloc = _run_per_pop_at_taus(
        n_pairs=50_000, loci=("A", "B", "DRB1"), seed=20260424 + 2,
        per_locus_tau=True,
    )
    c_d = {tau: _disparity_from_probs([perloc[p][tau] for p in pops if p in perloc])
           for tau in (0, 1, 2)}

    # Panel (d): LD-block resampling (synthetic, illustrative only)
    ld = _run_per_pop_at_taus(
        n_pairs=50_000, loci=("A", "B", "DRB1"), seed=20260424 + 3,
        ld_block_strength=0.10,
    )
    d_d = {tau: _disparity_from_probs([ld[p][tau] for p in pops if p in ld])
           for tau in (0, 1, 2)}

    panel_data = [
        ("a) Add HLA-C (8/8 matching)", a_d, "#2a5780"),
        ("b) Halved N (50,000 pairs)", b_d, "#5fa84a"),
        ("c) Per-locus τ definition", c_d, "#a3324e"),
        ("d) Block-LD resampling", d_d, "#c87132"),
    ]
    for ax, (title, d, color) in zip(axes.flat, panel_data):
        taus = sorted(d)
        ax.plot(taus, [base_d[t] for t in taus], "o--", color="#999999",
                label="Main run", linewidth=1.5)
        ax.plot(taus, [d[t] for t in taus], "o-", color=color,
                label="Sensitivity", linewidth=2)
        ax.set_xticks(taus)
        ax.set_xlabel("Coating tolerance τ")
        ax.set_ylabel("Disparity ratio D(τ)")
        ax.set_title(title, loc="left", fontsize=10, fontweight="bold")
        ax.set_yscale("log")
        ax.grid(alpha=0.25, which="both")
        ax.legend(frameon=False, fontsize=8, loc="upper right")
    fig.suptitle("Sensitivity of D(τ) to modeling choices",
                 fontsize=11, fontweight="bold")
    fig.tight_layout()
    out = FIG_DIR / "fig5_sensitivity.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)

    # Persist the sensitivity numbers for citation in the manuscript.
    rows = []
    for label, d, _ in panel_data:
        for tau, val in d.items():
            rows.append({"panel": label, "tau": tau, "disparity": val})
    pd.DataFrame(rows).to_csv(
        Path("data/derived/sensitivity_results.csv"), index=False
    )
    return out


def figure_validation_hwe() -> Path:
    """Supplementary Fig S1: HWE closed-form validation.

    For every (population, locus) cell, two checks against analytical
    quantities under HWE:
      (i)  P(one random patient allele = one random donor allele) = Σ f²
      (ii) P(m_l = 2; full diploid match) = 2(Σ f²)² − Σ f⁴
    Both should lie on y = x within Monte-Carlo noise.
    """
    from .simulate import (
        AlleleFrequencyTable, sample_individuals,
        hwe_homozygosity, hwe_full_match_per_locus,
    )
    rng = np.random.default_rng(20260424)
    pops = list(DEFAULT_POPULATIONS)
    rows = []
    for pop in pops:
        safe = pop.replace(" ", "_").replace("(", "").replace(")", "")
        for locus in LOCI:
            path = RAW_DIR / f"afnd_{safe}_{locus}.tsv"
            if not path.exists():
                continue
            tab = AlleleFrequencyTable.from_tsv(path)
            n = 100_000
            patient = sample_individuals(tab, n, rng)
            donor = sample_individuals(tab, n, rng)
            # Single-allele match (first patient allele vs. first donor allele)
            single_emp = float((patient[:, 0] == donor[:, 0]).mean())
            single_closed = hwe_homozygosity(tab.freqs)
            # Full diploid match m_l = 2
            p_sorted = np.sort(patient, axis=1)
            d_sorted = np.sort(donor, axis=1)
            full_emp = float(((p_sorted[:, 0] == d_sorted[:, 0]) &
                              (p_sorted[:, 1] == d_sorted[:, 1])).mean())
            full_closed = hwe_full_match_per_locus(tab.freqs)
            rows.append({
                "population": pop, "locus": locus,
                "single_empirical": single_emp,
                "single_closed": single_closed,
                "full_empirical": full_emp,
                "full_closed": full_closed,
            })
    df = pd.DataFrame(rows)

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    colors = {"A": "#2a5780", "B": "#a3324e", "DRB1": "#5fa84a"}

    ax = axes[0]
    for locus, sub in df.groupby("locus"):
        ax.scatter(sub["single_closed"], sub["single_empirical"],
                   color=colors.get(locus, "k"), label=f"HLA-{locus}", s=60)
    lo, hi = 0, max(df["single_closed"].max(), df["single_empirical"].max()) * 1.08
    ax.plot([lo, hi], [lo, hi], "--", color="#666", linewidth=1, label="y = x")
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel("Closed form: F = Σf²")
    ax.set_ylabel("Empirical P(single allele match)")
    ax.set_title("(a) Single-allele match validation")
    ax.legend(frameon=False, loc="lower right")

    ax = axes[1]
    for locus, sub in df.groupby("locus"):
        ax.scatter(sub["full_closed"], sub["full_empirical"],
                   color=colors.get(locus, "k"), label=f"HLA-{locus}", s=60)
    lo, hi = 0, max(df["full_closed"].max(), df["full_empirical"].max()) * 1.08
    ax.plot([lo, hi], [lo, hi], "--", color="#666", linewidth=1, label="y = x")
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi)
    ax.set_xlabel("Closed form: 2(Σf²)² − Σf⁴")
    ax.set_ylabel("Empirical P(m_l = 2)")
    ax.set_title("(b) Full diploid match validation")
    ax.legend(frameon=False, loc="lower right")

    fig.suptitle("Simulator validation against HWE closed form (Fig S1)",
                 fontsize=12, fontweight="bold")
    fig.tight_layout()
    out = FIG_DIR / "figS1_validation.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)

    df["single_abs_err"] = (df["single_empirical"] - df["single_closed"]).abs()
    df["full_abs_err"] = (df["full_empirical"] - df["full_closed"]).abs()
    df.to_csv(Path("data/derived/validation_results.csv"), index=False)
    return out


def figure_convergence() -> Path:
    """Supplementary Fig S2: bootstrap SE vs. N for one mid-baseline population."""
    from .simulate import (
        AlleleFrequencyTable, simulate_population, match_probability,
    )
    rng = np.random.default_rng(20260424)
    pop = "Han Chinese"
    safe = pop.replace(" ", "_")
    tables = {l: AlleleFrequencyTable.from_tsv(RAW_DIR / f"afnd_{safe}_{l}.tsv")
              for l in LOCI}
    Ns = [1_000, 5_000, 10_000, 50_000, 100_000, 200_000]
    rows = []
    for N in Ns:
        matches = simulate_population(tables, n_pairs=N, rng=rng)
        for tau in (0, 1, 2):
            n_boot = 200
            ests = np.empty(n_boot)
            for i in range(n_boot):
                idx = rng.integers(0, N, size=N)
                ests[i] = match_probability(matches[idx], tau=tau)
            rows.append({"N": N, "tau": tau, "se": float(ests.std())})
    df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(5.5, 4))
    for tau in sorted(df["tau"].unique()):
        sub = df[df["tau"] == tau].sort_values("N")
        ax.plot(sub["N"], sub["se"] * 100, "o-", label=f"τ = {tau}", linewidth=1.8)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("N pairs simulated")
    ax.set_ylabel("Bootstrap SE (percentage points)")
    ax.set_title(f"Convergence of match-probability estimator ({pop})")
    ax.grid(which="both", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    out = FIG_DIR / "figS2_convergence.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)
    df.to_csv(Path("data/derived/convergence_results.csv"), index=False)
    return out


def figure_alt_tau() -> Path:
    """Supplementary Fig S3: per-locus τ vs. pooled τ comparison across populations."""
    from .simulate import (
        AlleleFrequencyTable, simulate_population,
        match_probability, match_probability_per_locus,
    )
    rng = np.random.default_rng(20260424)
    rows = []
    for pop in DEFAULT_POPULATIONS:
        safe = pop.replace(" ", "_").replace("(", "").replace(")", "")
        try:
            tables = {l: AlleleFrequencyTable.from_tsv(RAW_DIR / f"afnd_{safe}_{l}.tsv")
                      for l in LOCI}
        except (FileNotFoundError, ValueError):
            continue
        matches = simulate_population(tables, n_pairs=50_000, rng=rng)
        for tau in (0, 1, 2):
            rows.append({"population": pop, "tau": tau,
                         "definition": "pooled",
                         "match_prob": match_probability(matches, tau)})
            rows.append({"population": pop, "tau": tau,
                         "definition": "per-locus",
                         "match_prob": match_probability_per_locus(matches, tau)})
    df = pd.DataFrame(rows)

    fig, ax = plt.subplots(figsize=(7, 4.2))
    pops = list(DEFAULT_POPULATIONS)
    width = 0.35
    x = np.arange(len(pops))
    for i, (definition, color) in enumerate([("pooled", "#2a5780"),
                                              ("per-locus", "#c87132")]):
        sub = (df[(df["definition"] == definition) & (df["tau"] == 2)]
               .set_index("population").reindex(pops).reset_index())
        ax.bar(x + (i - 0.5) * width, sub["match_prob"], width,
               color=color, label=f"τ = 2 ({definition})")
    ax.set_xticks(x)
    ax.set_xticklabels(pops, rotation=25, ha="right")
    ax.set_ylabel("Match probability")
    ax.set_title("Pooled vs. per-locus tolerance definition (τ = 2)")
    ax.legend(frameon=False)
    fig.tight_layout()
    out = FIG_DIR / "figS3_alt_tau.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)
    df.to_csv(Path("data/derived/alt_tau_results.csv"), index=False)
    return out


def main() -> None:
    _setup()
    if not RESULTS.exists():
        raise SystemExit(
            f"No results at {RESULTS}. Run:\n"
            f"  python -m hla_sim.synthetic_data   # or fetch_afnd\n"
            f"  python -m hla_sim.simulate\n"
        )
    results = pd.read_csv(RESULTS)
    paths = [
        figure_schematic(),
        figure_allele_entropy(),
        figure_match_by_population(results),
        figure_pool_expansion(results),
        figure_disparity_ratio(results),
        figure_sensitivity(results),
        figure_validation_hwe(),
        figure_convergence(),
        figure_alt_tau(),
    ]
    print("Wrote figures:")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
