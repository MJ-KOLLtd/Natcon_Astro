"""Blend Imagine-generated Filipino textures onto official hero artwork."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance

ROOT = Path(__file__).resolve().parents[1]
SESSION = Path(
    r"C:\Users\MJ\.grok\sessions\C%3A%5CUsers%5CMJ%5CDocuments%5C_Thoughts%5CC%26E%20Group%5CCEALS%5CCE%20LOGIC%5CNatcon_Astro\019f6395-3fe1-79c1-b00d-f96504d5a26d\images"
)
SRC_DESKTOP = Path(
    r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\New Hero Layout.png"
)
SRC_MOBILE = Path(
    r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\1080 x 1920.png"
)
BG_DESKTOP = SESSION / "5.jpg"
BG_MOBILE = SESSION / "4.jpg"
OUT = ROOT / "public" / "assets"


def warm_tone(img: Image.Image, warmth: float = 1.06) -> Image.Image:
    r, g, b = img.convert("RGB").split()
    r = r.point(lambda i: min(255, int(i * warmth)))
    g = g.point(lambda i: min(255, int(i * (warmth * 0.99))))
    return Image.merge("RGB", (r, g, b))


def apply_texture(
    original: Image.Image,
    texture: Image.Image,
    *,
    base_alpha: float = 0.14,
    bottom_alpha: float = 0.28,
    bottom_start: float = 0.62,
) -> Image.Image:
    size = original.size
    tex = texture.convert("RGB").resize(size, Image.Resampling.LANCZOS)
    base = warm_tone(original)
    out = Image.blend(base, tex, base_alpha)

    # stronger Filipino weave in lower wave area only
    w, h = size
    y0 = int(h * bottom_start)
    top = out.crop((0, 0, w, y0))
    bottom = Image.blend(base.crop((0, y0, w, h)), tex.crop((0, y0, w, h)), bottom_alpha)
    merged = Image.new("RGB", size)
    merged.paste(top, (0, 0))
    merged.paste(bottom, (0, y0))
    return ImageEnhance.Contrast(merged).enhance(1.04)


def save_pair(img: Image.Image, stem: str) -> None:
    png = OUT / f"{stem}.png"
    webp = OUT / f"{stem}.webp"
    img.save(png, format="PNG", optimize=True)
    img.save(webp, format="WEBP", quality=86, method=6)
    print(f"{stem}: {img.size} | png {png.stat().st_size/1024:.0f} KB | webp {webp.stat().st_size/1024:.0f} KB")


def main() -> None:
    desktop = Image.open(SRC_DESKTOP).convert("RGB").resize(
        (1920, 1080), Image.Resampling.LANCZOS
    )
    mobile = Image.open(SRC_MOBILE).convert("RGB").resize(
        (1080, 1920), Image.Resampling.LANCZOS
    )

    desktop_out = apply_texture(desktop, Image.open(BG_DESKTOP))
    mobile_out = apply_texture(mobile, Image.open(BG_MOBILE), bottom_start=0.58)

    save_pair(desktop_out, "hero")
    save_pair(mobile_out, "hero-mobile")
    print("Done.")


if __name__ == "__main__":
    main()