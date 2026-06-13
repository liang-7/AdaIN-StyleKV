from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"

methods = [
    "AdaIN\n1-block",
    "AdaIN\n2-block",
    "w/o AdaIN\n1-block\n(InstantStyle baseline)",
    "w/o AdaIN\n2-block\n(InstantStyle baseline)",
    "AdaIN-only\nw/o ControlNet",
    "Ours\nw/o AdaIN\n$\\gamma$=0.6",
    "Ours\nAdaIN\n$\\gamma$=0.6",
]

short_methods = [
    "AdaIN 1-block",
    "AdaIN 2-block",
    "w/o AdaIN 1-block (InstantStyle baseline)",
    "w/o AdaIN 2-block (InstantStyle baseline)",
    "AdaIN-only w/o ControlNet",
    "Ours w/o AdaIN $\\gamma$=0.6",
    "Ours AdaIN $\\gamma$=0.6",
]

fid = np.array([73.34, 88.54, 76.57, 91.56, 70.75, 78.14, 78.48])
art_fid = np.array([103.17, 98.42, 98.63, 95.02, 104.12, 85.43, 90.76])
lpips = np.array([0.581, 0.5994, 0.597, 0.612, 0.7455, 0.6285, 0.5991])

colors = ["#7b2cc7", "#9c4ddb", "#326795", "#4f7fb0", "#8290a3", "#f26735", "#cf1f2b"]


def ordinal_ranks(values: np.ndarray) -> np.ndarray:
    order = np.argsort(values)
    ranks = np.empty_like(order)
    ranks[order] = np.arange(1, len(values) + 1)
    return ranks


def save_quantitative_bars() -> None:
    metrics = [
        ("(a) FID ↓", fid, (63, 102), "{:.2f}"),
        ("(b) Art-FID ↓", art_fid, (79, 113), "{:.2f}"),
        ("(c) LPIPS ↓", lpips, (0.52, 0.83), "{:.3f}"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(14.8, 4.2))
    fig.suptitle("Quantitative Comparison Across Evaluation Metrics", fontsize=14, fontweight="bold")

    for ax, (title, values, ylim, fmt) in zip(axes, metrics):
        x = np.arange(len(methods))
        bars = ax.bar(x, values, color=colors, width=0.68)
        ax.set_title(title, loc="left", fontsize=11, fontweight="bold")
        ax.set_ylim(*ylim)
        ax.set_xticks(x)
        ax.set_xticklabels(methods, rotation=38, ha="right", fontsize=8)
        ax.grid(axis="y", linestyle="--", alpha=0.25)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + (ylim[1] - ylim[0]) * 0.012,
                fmt.format(value),
                ha="center",
                va="bottom",
                rotation=90,
                fontsize=8,
            )

    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(FIGURES / "image2.pdf", bbox_inches="tight")
    plt.close(fig)


def save_rank_heatmap() -> None:
    ranks = np.vstack([
        ordinal_ranks(fid),
        ordinal_ranks(art_fid),
        ordinal_ranks(lpips),
    ]).T

    fig, ax = plt.subplots(figsize=(6.6, 5.4))
    im = ax.imshow(ranks, cmap="YlGnBu_r", vmin=1, vmax=7)
    ax.set_title("Ablation Rank Heatmap (lower rank is better)", fontsize=13, fontweight="bold")
    ax.set_xticks(np.arange(3))
    ax.set_xticklabels(["FID ↓", "Art-FID ↓", "LPIPS ↓"], fontsize=10)
    ax.set_yticks(np.arange(len(short_methods)))
    ax.set_yticklabels(short_methods, fontsize=8)

    for row in range(ranks.shape[0]):
        for col in range(ranks.shape[1]):
            ax.text(col, row, f"#{ranks[row, col]}", ha="center", va="center", fontsize=10, fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Rank")
    fig.tight_layout()
    fig.savefig(FIGURES / "image4.pdf", bbox_inches="tight")
    fig.savefig(FIGURES / "fig_userstudy_docx.pdf", bbox_inches="tight")
    plt.close(fig)


def save_gamma_trends() -> None:
    gammas = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    gamma_fid = np.array([76.57, 76.91, 77.46, 78.48, 79.67, 82.36])
    gamma_art_fid = np.array([98.63, 94.26, 89.72, 90.76, 83.58, 82.91])
    gamma_lpips = np.array([0.597, 0.606, 0.617, 0.599, 0.655, 0.697])

    metrics = [
        ("(a) $\\gamma$ vs FID", gamma_fid, "FID ↓"),
        ("(b) $\\gamma$ vs Art-FID", gamma_art_fid, "Art-FID ↓"),
        ("(c) $\\gamma$ vs LPIPS", gamma_lpips, "LPIPS ↓"),
    ]

    fig, axes = plt.subplots(1, 3, figsize=(9.2, 2.7))
    fig.suptitle("Metric Trends along Gamma Sweep", fontsize=11, fontweight="bold")
    for ax, (title, values, ylabel) in zip(axes, metrics):
        ax.plot(gammas, values, color="#1f77b4", marker="o", linewidth=1.5, markersize=3.5)
        ax.scatter([0.6], [values[3]], marker="*", s=70, color="crimson", edgecolor="black", zorder=3)
        ax.text(0.62, values[3], "$\\gamma$=0.6", fontsize=7, color="crimson", va="bottom")
        for gamma, value in zip(gammas, values):
            if gamma == 0.6:
                continue
            ax.text(gamma + 0.01, value, f"$\\gamma$={gamma:.1f}", fontsize=6, color="#1f77b4")
        ax.set_title(title, loc="left", fontsize=8, fontweight="bold")
        ax.set_xlabel("Gamma ($\\gamma$)", fontsize=7)
        ax.set_ylabel(ylabel, fontsize=7)
        ax.tick_params(labelsize=6)
        ax.grid(alpha=0.2, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

    fig.tight_layout(rect=(0, 0, 1, 0.9))
    fig.savefig(FIGURES / "fig_ref_comprehensive.pdf", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    save_quantitative_bars()
    save_rank_heatmap()
    save_gamma_trends()
