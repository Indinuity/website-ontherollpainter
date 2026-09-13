#!/usr/bin/env python3
"""Make a web-ready copy of a photo for the site.

    python3 tools/prep-photo.py "images/Barbs kitchen after.jpg" work-01

Writes images/work-01.jpg: resized to 1600px on the long edge, rotated the way the
camera intended, re-encoded as a progressive JPEG, and with ALL metadata dropped —
phone photos carry the GPS coordinates of where they were taken, which is the
customer's house. The original is left untouched.

Allowed slot names match what index.html references: hero, about, work-01 …,
before, after, og-image. A before/after slider plate takes two files, e.g.
work-03-before and work-03-after. og-image is cropped to 1200×630 for social previews.

Gallery photos use gallery/<project>-<n> or gallery/<project>-before-<n>, e.g.

    python3 tools/prep-photo.py "images/IMG_6146.jpg" gallery/white-kitchen-2

which writes images/gallery/white-kitchen-2.jpg at 1200px (the gallery page shows
many photos, so they are made a little smaller). An optional fourth argument crops
first — left,top,right,bottom as fractions of the original, e.g. 0,0,0.8,1 keeps
the left 80% — for taking a house number or a face out of frame.

Needs Pillow:  python3 -m pip install pillow
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

LONG_EDGE = 1600
QUALITY = 82
SLOTS = re.compile(r"^(hero|about|work-\d{2}(-before|-after)?|before|after|og-image|gallery/[a-z0-9]+(-[a-z0-9]+)*)$")


def main() -> int:
    if len(sys.argv) not in (3, 4):
        print(__doc__)
        return 2
    src, slot = Path(sys.argv[1]), sys.argv[2]
    crop = [float(v) for v in sys.argv[3].split(",")] if len(sys.argv) == 4 else None
    if not SLOTS.match(slot):
        print(f"'{slot}' is not one of the names the site uses; see the docstring.")
        return 2
    dest = Path("images") / f"{slot}.jpg"

    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")  # apply rotation, then forget EXIF
    if crop:
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
    if slot == "og-image":
        im = ImageOps.fit(im, (1200, 630), Image.LANCZOS)
    elif slot.startswith("gallery/"):
        im.thumbnail((1200, 1200), Image.LANCZOS)
    else:
        im.thumbnail((LONG_EDGE, LONG_EDGE), Image.LANCZOS)

    dest.parent.mkdir(exist_ok=True)
    im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)  # no exif= → nothing carried over
    print(f"{src} → {dest}  {im.size[0]}×{im.size[1]}  {dest.stat().st_size // 1024} KB, no metadata")
    return 0


if __name__ == "__main__":
    sys.exit(main())
