#!/usr/bin/env python3
"""Make a web-ready copy of a photo for the site.

    python3 tools/prep-photo.py "images/Barbs kitchen after.jpg" work-01

Writes images/work-01.jpg: resized to 1600px on the long edge, rotated the way the
camera intended, re-encoded as a progressive JPEG, and with ALL metadata dropped —
phone photos carry the GPS coordinates of where they were taken, which is the
customer's house. The original is left untouched.

Allowed slot names match what index.html references: hero, portrait, work-01 …,
before, after, og-image. og-image is cropped to 1200×630 for social previews.

Needs Pillow:  python3 -m pip install pillow
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

LONG_EDGE = 1600
QUALITY = 82
SLOTS = re.compile(r"^(hero|portrait|work-\d{2}|before|after|og-image)$")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src, slot = Path(sys.argv[1]), sys.argv[2]
    if not SLOTS.match(slot):
        print(f"'{slot}' is not one of the names the site uses; see the docstring.")
        return 2
    dest = Path("images") / f"{slot}.jpg"

    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")  # apply rotation, then forget EXIF
    if slot == "og-image":
        im = ImageOps.fit(im, (1200, 630), Image.LANCZOS)
    else:
        im.thumbnail((LONG_EDGE, LONG_EDGE), Image.LANCZOS)

    dest.parent.mkdir(exist_ok=True)
    im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)  # no exif= → nothing carried over
    print(f"{src} → {dest}  {im.size[0]}×{im.size[1]}  {dest.stat().st_size // 1024} KB, no metadata")
    return 0


if __name__ == "__main__":
    sys.exit(main())
