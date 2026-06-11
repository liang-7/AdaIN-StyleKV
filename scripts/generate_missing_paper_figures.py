"""Generate missing PDF figures referenced by paper_revised.tex."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"
PROC = FIGURES / "10processor"


def font(size: int) -> ImageFont.ImageFont:
    for name in ("arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def square(path: Path, size: int) -> Image.Image:
    image = Image.open(path).convert("RGB")
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side)).resize(
        (size, size), Image.Resampling.LANCZOS
    )


def save_grid(output: Path, rows: list[list[Path]], col_labels=None, row_labels=None) -> None:
    tile = 520
    header = 52 if col_labels else 0
    left = 132 if row_labels else 0
    canvas = Image.new("RGB", (left + tile * len(rows[0]), header + tile * len(rows)), "white")
    draw = ImageDraw.Draw(canvas)
    label_font = font(24)

    if col_labels:
        for col, label in enumerate(col_labels):
            box = draw.textbbox((0, 0), label, font=label_font)
            x = left + col * tile + (tile - (box[2] - box[0])) // 2
            draw.text((x, 12), label, fill="black", font=label_font)

    for row, paths in enumerate(rows):
        if row_labels:
            label = row_labels[row]
            box = draw.textbbox((0, 0), label, font=label_font)
            x = max(4, left - (box[2] - box[0]) - 12)
            y = header + row * tile + (tile - (box[3] - box[1])) // 2
            draw.text((x, y), label, fill="black", font=label_font)
        for col, path in enumerate(paths):
            canvas.paste(square(path, tile), (left + col * tile, header + row * tile))

    canvas.save(output, "PDF", resolution=300.0)
    print(f"Saved: {output}")


def proc(prefix: str, gamma: str) -> Path:
    return PROC / f"{prefix}_gamma{gamma}.png"


def collect_case(folder_name: str) -> list[Path]:
    folder = FIGURES / folder_name
    names = [
        "noadain_1blk.png",
        "adain_1blk.png",
        "noadain_2blk.png",
        "adain_2blk.png",
        "proc05_adainfalse_gamma0.6.png",
        "proc05_adaintrue_gamma0.6.png",
    ]
    return [folder / name for name in names]


def main() -> None:
    gammas = ["0.2", "0.4", "0.8", "1"]

    save_grid(
        FIGURES / "fig_gamma_5blk.pdf",
        [[proc("proc05_adaintrue", gamma) for gamma in gammas]],
        col_labels=[r"gamma=0.2", r"gamma=0.4", r"gamma=0.8", r"gamma=1.0"],
    )

    save_grid(
        FIGURES / "fig_gamma_10blk.pdf",
        [[proc("proc10_adaintrue", gamma) for gamma in gammas]],
        col_labels=[r"gamma=0.2", r"gamma=0.4", r"gamma=0.8", r"gamma=1.0"],
    )

    save_grid(
        FIGURES / "fig_block_compare.pdf",
        [
            [proc("proc01_adaintrue", gamma) for gamma in gammas],
            [proc("proc05_adaintrue", gamma) for gamma in gammas],
        ],
        col_labels=[r"gamma=0.2", r"gamma=0.4", r"gamma=0.8", r"gamma=1.0"],
        row_labels=["1-block", "5-block"],
    )

    save_grid(
        FIGURES / "fig_adain_compare.pdf",
        [
            [proc("proc01_adaintrue", gamma) for gamma in gammas],
            [proc("proc01_adainfalse", gamma) for gamma in gammas],
        ],
        col_labels=[r"gamma=0.2", r"gamma=0.4", r"gamma=0.8", r"gamma=1.0"],
        row_labels=["AdaIN", "No AdaIN"],
    )

    save_grid(
        FIGURES / "fig_variant_compare.pdf",
        [
            collect_case("大象"),
            collect_case("小孩玩电脑"),
        ],
        col_labels=["noadain_1blk", "adain_1blk", "noadain_2blk", "adain_2blk", "proc05_noadain", "proc05_adain"],
        row_labels=["case 1", "case 2"],
    )


if __name__ == "__main__":
    main()
