"""Compose 10processor images into a single gallery PDF replacing fig_gallery.pdf."""
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

FIGURES_DIR = Path(r"d:\PythonProject2\AdaIN-StyleKV\figures\10processor")
OUTPUT = Path(r"d:\PythonProject2\AdaIN-StyleKV\figures\fig_gallery.pdf")

# Row definitions: (label, filename_prefix)
ROWS = [
    ("1-block, No AdaIN",  "proc01_adainfalse"),
    ("1-block, AdaIN",     "proc01_adaintrue"),
    ("5-block, No AdaIN",  "proc05_adainfalse"),
    ("5-block, AdaIN",     "proc05_adaintrue"),
    ("10-block, No AdaIN", "proc10_adainfalse"),
    ("10-block, AdaIN",    "proc10_adaintrue"),
]

GAMMAS = [0.2, 0.4, 0.8, 1.0]

n_rows = len(ROWS)
n_cols = len(GAMMAS)

fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 20))

for row_idx, (label, prefix) in enumerate(ROWS):
    for col_idx, gamma in enumerate(GAMMAS):
        ax = axes[row_idx, col_idx]
        fname = f"{prefix}_gamma{gamma}.png"
        fpath = FIGURES_DIR / fname
        img = mpimg.imread(fpath)
        ax.imshow(img)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)

# Column headers (gamma values)
for col_idx, gamma in enumerate(GAMMAS):
    axes[0, col_idx].set_title(rf"$\gamma = {gamma}$", fontsize=13, fontweight="bold", pad=4)

# Row labels
for row_idx, (label, _) in enumerate(ROWS):
    axes[row_idx, 0].set_ylabel(label, fontsize=12, fontweight="bold",
                                 rotation=0, labelpad=60, ha="right", va="center")

plt.tight_layout(pad=1.5, h_pad=0.3, w_pad=0.5)
fig.savefig(OUTPUT, dpi=200, bbox_inches="tight", pad_inches=0.15)
plt.close(fig)
print(f"Saved: {OUTPUT}")
