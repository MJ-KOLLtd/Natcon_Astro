"""Export crisp desktop + mobile heroes from 4K master artwork."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "assets"

DESKTOP_MASTER = Path(
    r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\Natcon Horizontal.png"
)
MOBILE_MASTER = Path(
    r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\Natcon Vertical.png"
)

# Masters are 1920x1080 (horizontal) and 1080x1920 (vertical) — never upscale.
DESKTOP_1X = (1600, 900)
DESKTOP_2X = (1920, 1080)
MOBILE_1X = (828, 1472)
MOBILE_2X = (1080, 1920)

QUALITY_1X = 94
QUALITY_2X = 90
METHOD = 6


def resize_crisp(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    img = img.convert("RGB")
    if img.size == size:
        return img
    # Never upscale past the master — return source when target is larger.
    if img.width < size[0] or img.height < size[1]:
        return img
    out = img.resize(size, Image.Resampling.LANCZOS)
    out = out.filter(ImageFilter.UnsharpMask(radius=0.9, percent=115, threshold=2))
    return out


def save_webp(img: Image.Image, path: Path, *, quality: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(
        path,
        format="WEBP",
        quality=quality,
        method=METHOD,
        lossless=False,
    )
    print(f"  {path.name}: {img.width}x{img.height} | {path.stat().st_size / 1024:.0f} KB | q{quality}")


def export_desktop() -> None:
    print("Desktop hero")
    master = Image.open(DESKTOP_MASTER)
    save_webp(
        resize_crisp(master, DESKTOP_1X),
        OUT / "hero.webp",
        quality=QUALITY_1X,
    )
    save_webp(
        resize_crisp(master, DESKTOP_2X),
        OUT / "hero@2x.webp",
        quality=QUALITY_2X,
    )


def export_mobile() -> None:
    print("Mobile hero")
    master = Image.open(MOBILE_MASTER)
    save_webp(
        resize_crisp(master, MOBILE_1X),
        OUT / "hero-mobile.webp",
        quality=QUALITY_1X,
    )
    save_webp(
        resize_crisp(master, MOBILE_2X),
        OUT / "hero-mobile@2x.webp",
        quality=QUALITY_2X,
    )


def main() -> None:
    if not DESKTOP_MASTER.exists():
        raise FileNotFoundError(DESKTOP_MASTER)
    if not MOBILE_MASTER.exists():
        raise FileNotFoundError(MOBILE_MASTER)

    export_desktop()
    export_mobile()
    print("Done.")


if __name__ == "__main__":
    main()