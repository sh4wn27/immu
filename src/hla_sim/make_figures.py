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


def figure_sensitivity_stub(results: pd.DataFrame) -> Path:
    """Figure 5: 2x2 sensitivity grid placeholder.

    Real panels (HLA-C addition, halved N, per-locus τ, LD haplotype resampling)
    require either re-runs of the simulator under different configs or external
    haplotype data; this stub draws the shell so the manuscript compiles and
    flags the panels with TODO labels until those analyses are implemented.
    """
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    panels = [
        ("a) Add HLA-C", "Add HLA-C to matching\n(8/8 instead of 6/6)"),
        ("b) Halved N", "N = 50,000 pairs\n(SE robustness check)"),
        ("c) Per-locus τ", "τ applied at each locus\n(more permissive)"),
        ("d) Haplotype LD", "Haplotype-level resampling\n(CEU + Han Chinese)"),
    ]
    for ax, (title, body) in zip(axes.flat, panels):
        ax.set_title(title, loc="left", fontsize=10, fontweight="bold")
        ax.text(0.5, 0.5, body + "\n\n[TODO: implement]",
                ha="center", va="center", transform=ax.transAxes,
                fontsize=9, color="#666666")
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_color("#cccccc")
    fig.suptitle("Sensitivity of disparity-ratio conclusion (stub)",
                 fontsize=11, fontweight="bold")
    fig.tight_layout()
    out = FIG_DIR / "fig5_sensitivity.pdf"
    fig.savefig(out)
    fig.savefig(out.with_suffix(".png"))
    plt.close(fig)
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
        figure_allele_entropy(),
        figure_match_by_population(results),
        figure_pool_expansion(results),
        figure_disparity_ratio(results),
        figure_sensitivity_stub(results),
    ]
    print("Wrote figures:")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
