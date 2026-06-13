from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "figures" / "fig15"
OUT = ROOT / "figures" / "fig_canny_res.pdf"

ROWS = [
    ("canny_lowsolution.png", "output_low_solution.png"),
    ("canny_highsolution.png", "output_high_solution.png"),
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for name in ("arial.ttf", "Arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def fit_image(path: Path, size: tuple[int, int]) -> Image.Image:
    image = Image.open(path).convert("RGB")
    image.thumbnail(size, Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, "white")
    x = (size[0] - image.width) // 2
    y = (size[1] - image.height) // 2
    canvas.paste(image, (x, y))
    return canvas


def draw_centered(draw: ImageDraw.ImageDraw, xywh: tuple[int, int, int, int], text: str, font) -> None:
    x, y, w, h = xywh
    bbox = draw.textbbox((0, 0), text, font=font)
    tx = x + (w - (bbox[2] - bbox[0])) // 2
    ty = y + (h - (bbox[3] - bbox[1])) // 2
    draw.text((tx, ty), text, fill="black", font=font)


def main() -> None:
    tile_w, tile_h = 420, 235
    header_h = 36
    gap = 0
    margin = 10
    label_font = load_font(18)

    style = Image.open(SRC / "style.png").convert("RGB")
    inset = int(tile_h * 0.28)
    style = style.resize((inset, inset), Image.Resampling.LANCZOS)

    width = margin * 2 + tile_w * 2 + gap
    height = margin * 2 + header_h + tile_h * len(ROWS)
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)

    draw_centered(draw, (margin, margin, tile_w, header_h), "canny", label_font)
    draw_centered(draw, (margin + tile_w + gap, margin, tile_w, header_h), "output", label_font)

    y = margin + header_h
    for canny_name, output_name in ROWS:
        canny = fit_image(SRC / canny_name, (tile_w, tile_h))
        output = fit_image(SRC / output_name, (tile_w, tile_h))
        output.paste(style, (0, tile_h - inset))

        canvas.paste(canny, (margin, y))
        canvas.paste(output, (margin + tile_w + gap, y))

        row_label = "low resolution" if "low" in canny_name else "high resolution"
        draw.text((margin + 7, y + 7), row_label, fill="black", font=load_font(14))
        y += tile_h

    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT, "PDF", resolution=300.0)
    print(f"Saved {OUT}")


if __name__ == "__main__":
    main()
