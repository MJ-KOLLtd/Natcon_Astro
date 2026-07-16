"""Export crisp desktop + mobile heroes from 4K master artwork."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "assets"

DESKTOP_MASTER = Path(
    r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\New Hero Layout.png"
)
MOBILE_MASTER = Path(
    r"C:\Users\MJ\Documents\_Thoughts\C&E Group\CEALS\CE LOGIC\1080 x 1920.png"
)

DESKTOP_1X = (1920, 1080)
DESKTOP_2X = (3840, 2160)
MOBILE_1X = (1080, 1920)
MOBILE_2X = (2160, 3840)

QUALITY_1X = 94
QUALITY_2X = 90
METHOD = 6


def resize_crisp(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    if img.size == size:
        return img.convert("RGB")
    downscale = img.width > size[0] or img.height > size[1]
    resample = Image.Resampling.LANCZOS if downscale else Image.Resampling.BICUBIC
    out = img.convert("RGB").resize(size, resample)
    if downscale:
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