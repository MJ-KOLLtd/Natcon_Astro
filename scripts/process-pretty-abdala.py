"""Prepare Pretty Abdala portrait for the speaker carousel."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

SRC = Path(r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\Pips\Pretty Abdala.jpg")
OUT = Path(
    r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\Natcon_Astro\public\assets\speakers\maria-pretty-lay-abdala.jpg"
)

# Trim the graphic frame and the partial text on the left edge.
CROP_BOX = (270, 245, 875, 685)
OUTPUT_SIZE = (1200, 1600)


def build_background(crop: Image.Image, size: tuple[int, int]) -> Image.Image:
    out_w, out_h = size
    backdrop = crop.resize(size, Image.Resampling.LANCZOS)
    backdrop = backdrop.filter(ImageFilter.GaussianBlur(radius=32))

    wash = Image.new("RGB", size, (228, 220, 212))
    return Image.blend(backdrop, wash, alpha=0.48)


def compose_portrait(crop: Image.Image) -> Image.Image:
    out_w, out_h = OUTPUT_SIZE
    cw, ch = crop.size

    background = build_background(crop, OUTPUT_SIZE)

    # Match the head-and-shoulders framing used by the other speaker photos.
    scale = (out_w / cw) * 1.0
    new_size = (out_w, int(ch * scale))
    subject = crop.resize(new_size, Image.Resampling.LANCZOS)

    x = 0
    y = int((out_h - new_size[1]) * 0.16)
    background.paste(subject, (x, y))

    result = background.convert("RGB")
    result = ImageEnhance.Color(result).enhance(1.03)
    result = ImageEnhance.Contrast(result).enhance(1.02)
    return result.filter(ImageFilter.UnsharpMask(radius=0.8, percent=65, threshold=2))


def main() -> None:
    crop = Image.open(SRC).convert("RGB").crop(CROP_BOX)
    portrait = compose_portrait(crop)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    portrait.save(OUT, format="JPEG", quality=93, optimize=True, progressive=True)
    print(f"Saved {OUT} ({portrait.size[0]}x{portrait.size[1]})")


if __name__ == "__main__":
    main()