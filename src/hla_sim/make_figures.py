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

from . import DEFAULT_POPULATIONS

FIG_DIR = Path("docs/manuscript/figures")
RESULTS = Path("data/derived/match_results.csv")


def _setup():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "figure.dpi": 140,
    })
    FIG_DIR.mkdir(parents=True, exist_ok=True)


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
    """Figure 5: disparity ratio (max/min match prob across populations) vs τ."""
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
    out = FIG_DIR / "fig5_disparity_ratio.pdf"
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
        figure_match_by_population(results),
        figure_pool_expansion(results),
        figure_disparity_ratio(results),
    ]
    print("Wrote figures:")
    for p in paths:
        print(f"  {p}")


if __name__ == "__main__":
    main()
