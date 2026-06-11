"""Compose figures/大叔 images into the Figure 4 progress panel."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "figures" / "大叔"
OUTPUT = ROOT / "figures" / "fig_variant_progress.pdf"

ORDER = [
    "org.png",
    "noadain_1blk.png",
    "adain_1blk.png",
    "noadain_2blk.png",
    "adain_2blk.png",
    "proc05_adainfalse_gamma0.6.png",
    "proc05_adaintrue_gamma0.6.png",
]

LABELS = [
    "org",
    "noadain_1blk",
    "adain_1blk",
    "noadain_2blk",
    "adain_2blk",
    "proc05_noadain",
    "proc05_adain",
]


def center_crop_square(image: Image.Image) -> Image.Image:
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    return image.crop((left, top, left + side, top + side))


def main() -> None:
    paths = [IMAGE_DIR / name for name in ORDER]
    style_path = IMAGE_DIR / "style.png"
    missing = [path.name for path in [*paths, style_path] if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Missing images: {', '.join(missing)}")

    tile_size = 620
    header = 58
    inset_size = int(tile_size * 0.24)
    style = center_crop_square(Image.open(style_path).convert("RGB")).resize(
        (inset_size, inset_size), Image.Resampling.LANCZOS
    )

    canvas = Image.new("RGB", (tile_size * len(paths), header + tile_size), "white")
    draw = ImageDraw.Draw(canvas)
    label_font = ImageFont.truetype("arial.ttf", 32)

    for idx, (path, label) in enumerate(zip(paths, LABELS)):
        tile = center_crop_square(Image.open(path).convert("RGB")).resize(
            (tile_size, tile_size), Image.Resampling.LANCZOS
        )
        tile.paste(style, (0, tile_size - inset_size))

        text_box = draw.textbbox((0, 0), label, font=label_font)
        text_width = text_box[2] - text_box[0]
        draw.text(
            (idx * tile_size + (tile_size - text_width) / 2, 12),
            label,
            fill="black",
            font=label_font,
        )
        canvas.paste(tile, (idx * tile_size, header))

    canvas.save(OUTPUT, "PDF", resolution=300.0)
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
