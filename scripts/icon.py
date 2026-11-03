#!/usr/bin/env python3
"""Dreist's app icon: a geometric blue "D" on a dark rounded square (the same
style as Einst's icon, which has an amber "E").

Writes assets/ui/AppIcon.png (1024 px) and, on macOS, assets/ui/AppIcon.icns
through `iconutil`. No third-party modules; the PNGs are written by hand.

    python3 scripts/icon.py
"""
import os
import struct
import subprocess
import tempfile
import zlib

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "assets", "ui")

BG = (0x1d, 0x22, 0x2b)
FG = (0x3d, 0x8b, 0xf0)


def pixel(x, y, n):
    """RGBA of pixel (x, y) in an n×n icon (coordinates scaled from 1024)."""
    u, v = x * 1024.0 / n, y * 1024.0 / n
    # Rounded square with a transparent margin.
    m, r = 100.0, 180.0
    cx = min(max(u, m + r), 1024 - m - r)
    cy = min(max(v, m + r), 1024 - m - r)
    if (u - cx) ** 2 + (v - cy) ** 2 > r * r:
        return (0, 0, 0, 0)
    # "D": a stem and a bowl (half-ellipse ring) of the same weight.
    if not (280 <= v <= 744):
        return BG + (255,)
    if 330 <= u <= 430:
        return FG + (255,)
    cx, cy = 470.0, 512.0
    outer = u <= cx or ((u - cx) / 230.0) ** 2 + ((v - cy) / 232.0) ** 2 <= 1.0
    inner = 370 < v < 654 and (u <= cx or ((u - cx) / 140.0) ** 2 + ((v - cy) / 142.0) ** 2 < 1.0)
    return FG + (255,) if 330 <= u and outer and not inner else BG + (255,)


def png(n):
    rows = b"".join(b"\x00" + bytes(c for x in range(n) for c in pixel(x, y, n)) for y in range(n))

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, 6, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "AppIcon.png"), "wb") as f:
        f.write(png(1024))
    with tempfile.TemporaryDirectory() as tmp:
        iconset = os.path.join(tmp, "AppIcon.iconset")
        os.makedirs(iconset)
        for size in (16, 32, 128, 256, 512):
            for scale in (1, 2):
                name = f"icon_{size}x{size}{'@2x' if scale == 2 else ''}.png"
                with open(os.path.join(iconset, name), "wb") as f:
                    f.write(png(size * scale))
        subprocess.run(["iconutil", "-c", "icns", iconset, "-o", os.path.join(OUT, "AppIcon.icns")], check=True)


if __name__ == "__main__":
    main()
