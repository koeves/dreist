#!/usr/bin/env python3
"""Dreist's app icon, from the in-app logo: the header's logo mark (the "D"
of `dreist_formats::profile::DREIST_LOGO_MARK`, a stem and a bowl, in its
3 px square frame) in the logo's slate blue on the header's charcoal.

Writes assets/ui/AppIcon.png (1024 px) and, on macOS, assets/ui/AppIcon.icns
through `iconutil`. Needs Pillow (`pip install pillow`).

    python3 scripts/icon.py
"""
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "assets", "ui")

# The header (charcoal) and the logo's colour (its accent at half alpha on it).
BG = (37, 42, 44)
MARK = (103, 135, 159)

# DREIST_LOGO_MARK, in the logo's 50×50 box; the frame is 3 px inset 1.5.
STEM = [(9.0, 9.0), (16.0, 9.0), (16.0, 41.0), (9.0, 41.0)]
BOWL = [(18.0, 9.0), (28.0, 9.0), (36.0, 13.0), (41.0, 20.0), (41.0, 30.0), (36.0, 37.0), (28.0, 41.0), (18.0, 41.0),
        (18.0, 34.0), (27.0, 34.0), (32.0, 31.0), (34.0, 27.0), (34.0, 23.0), (32.0, 19.0), (27.0, 16.0), (18.0, 16.0)]

SS = 4  # supersampling


def icon(n):
    s = n * SS
    k = s / 1024.0
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # macOS grid: an 824 px body at 100 px, corner radius 185.
    d.rounded_rectangle([100 * k, 100 * k, 924 * k, 924 * k], radius=185 * k, fill=BG + (255,))
    # The 50-unit logo box, 620 px wide, centred.
    u = 620 * k / 50.0
    ox = oy = (1024 * k - 50 * u) / 2

    def pt(x, y):
        return (ox + x * u, oy + y * u)

    d.rectangle([pt(0, 0), pt(50, 50)], outline=MARK + (255,), width=round(3 * u))
    d.polygon([pt(*p) for p in STEM], fill=MARK + (255,))
    d.polygon([pt(*p) for p in BOWL], fill=MARK + (255,))
    return im.resize((n, n), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    icon(1024).save(os.path.join(OUT, "AppIcon.png"))
    with tempfile.TemporaryDirectory() as tmp:
        iconset = os.path.join(tmp, "AppIcon.iconset")
        os.makedirs(iconset)
        for size in (16, 32, 128, 256, 512):
            for scale in (1, 2):
                name = f"icon_{size}x{size}{'@2x' if scale == 2 else ''}.png"
                icon(size * scale).save(os.path.join(iconset, name))
        subprocess.run(["iconutil", "-c", "icns", iconset, "-o", os.path.join(OUT, "AppIcon.icns")], check=True)


if __name__ == "__main__":
    main()
