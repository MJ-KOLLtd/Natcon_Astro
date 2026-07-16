"""Extract and convert Layout himay hero layers to optimized WebP assets."""

from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\Layout himay")
OUT = ROOT / "public" / "assets" / "hero"

WEBP_QUALITY = 90
WEBP_METHOD = 6
BG_QUALITY = 82


def alpha_bbox(img: Image.Image, threshold: int = 12) -> tuple[int, int, int, int] | None:
    if img.mode != "RGBA":
        rgb = img.convert("RGB")
        mask = Image.new("L", img.size)
        px = rgb.load()
        mpx = mask.load()
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = px[x, y]
                mpx[x, y] = 255 if (r > threshold or g > threshold or b > threshold) else 0
        return mask.getbbox()

    alpha = img.split()[3]
    mask = alpha.point(lambda p: 255 if p > threshold else 0)
    return mask.getbbox()


def save_webp(
    img: Image.Image,
    path: Path,
    *,
    max_width: int | None = None,
    quality: int = WEBP_QUALITY,
) -> None:
    out = img
    if max_width and out.width > max_width:
        ratio = max_width / out.width
        out = out.resize(
            (max_width, max(1, round(out.height * ratio))),
            Image.Resampling.LANCZOS,
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    if out.mode != "RGBA":
        out = out.convert("RGBA")

    out.save(
        path,
        format="WEBP",
        quality=quality,
        method=WEBP_METHOD,
        lossless=False,
    )
    print(f"  {path.name}: {out.width}x{out.height}")


def crop_layer(filename: str, crop_box: tuple[int, int, int, int] | None = None) -> Image.Image:
    img = Image.open(SRC / filename)
    if crop_box:
        return img.crop(crop_box)
    bbox = alpha_bbox(img)
    if not bbox:
        return img
    return img.crop(bbox)


def main() -> None:
    print(f"Output: {OUT}")

    bg = Image.open(SRC / "6.png").convert("RGB")
    save_webp(bg, OUT / "bg.webp", max_width=1600, quality=BG_QUALITY)
    save_webp(bg, OUT / "bg@2x.webp", max_width=1920, quality=BG_QUALITY)

    waves = crop_layer("7.png")
    save_webp(waves, OUT / "waves.webp", max_width=1920)

    mark = crop_layer("8.png", (523, 239, 900, 700))
    save_webp(mark, OUT / "ce-mark.webp", max_width=480)

    up_seal = crop_layer("9.png")
    save_webp(up_seal, OUT / "up-seal.webp", max_width=320)

    paarl = crop_layer("10.png")
    save_webp(paarl, OUT / "paarl.webp", max_width=400)

    plai = crop_layer("11.png")
    save_webp(plai, OUT / "plai.webp", max_width=200)

    cpd = crop_layer("12.png")
    save_webp(cpd, OUT / "cpd-badge.webp", max_width=360)

    print("Done.")


if __name__ == "__main__":
    main()