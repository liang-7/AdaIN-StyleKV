from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FIGURES_DIR = ROOT / "figures" / "10processor"
OUTPUT = ROOT / "figures" / "fig_gallery.pdf"

# Row definitions: (label, filename_prefix)
ROWS = [
    ("1-proc", "No AdaIN", "proc01_adainfalse"),
    ("1-proc", "AdaIN", "proc01_adaintrue"),
    ("5-proc", "No AdaIN", "proc05_adainfalse"),
    ("5-proc", "AdaIN", "proc05_adaintrue"),
    ("10-proc", "No AdaIN", "proc10_adainfalse"),
    ("10-proc", "AdaIN", "proc10_adaintrue"),
]

GAMMAS = ["0.2", "0.4", "0.8", "1"]


def font(size: int) -> ImageFont.ImageFont:
    for name in ("arialbd.ttf", "arial.ttf", "DejaVuSans-Bold.ttf", "DejaVuSans.ttf"):
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


def centered_text(draw: ImageDraw.ImageDraw, xywh, text: str, text_font, fill="black") -> None:
    x, y, width, height = xywh
    box = draw.textbbox((0, 0), text, font=text_font)
    text_width = box[2] - box[0]
    text_height = box[3] - box[1]
    draw.text(
        (x + (width - text_width) / 2, y + (height - text_height) / 2),
        text,
        fill=fill,
        font=text_font,
    )


def main() -> None:
    tile = 420
    label_width = 180
    header = 64
    canvas = Image.new("RGB", (label_width + tile * len(GAMMAS), header + tile * len(ROWS)), "white")
    draw = ImageDraw.Draw(canvas)
    header_font = font(26)
    row_font = font(22)
    subrow_font = font(18)

    for col, gamma in enumerate(GAMMAS):
        label = f"gamma = {gamma if gamma != '1' else '1.0'}"
        centered_text(draw, (label_width + col * tile, 0, tile, header), label, header_font)

    for row, (block, adain, prefix) in enumerate(ROWS):
        y = header + row * tile
        centered_text(draw, (0, y + tile * 0.40, label_width, 28), block, row_font)
        centered_text(draw, (0, y + tile * 0.50, label_width, 24), adain, subrow_font)
        for col, gamma in enumerate(GAMMAS):
            path = FIGURES_DIR / f"{prefix}_gamma{gamma}.png"
            canvas.paste(square(path, tile), (label_width + col * tile, y))

    canvas.save(OUTPUT, "PDF", resolution=300.0)
    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    main()
