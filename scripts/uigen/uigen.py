#!/usr/bin/env python3
"""Generate Dreist's own UI graphics into assets/ui.

Everything here is original drawing for this project (MIT OR Apache-2.0,
like the rest of the workspace). It replaces the graphics that came with
the original plugin's resources:

- Fonts/Dreist-Icons.ttf: the icon font. Same code points (U+E900..U+E92B)
  and meanings as the skins expect, so the .skin captions keep working.
- Cursors/*.png and Cursors/Cursors.hotspots: the named image cursors.
- AppIcon.icns (+ AppIcon.png, 1024 px): the macOS app icon, the header's
  "D" mark on Apple's icon grid (824 px rounded square on a 1024 canvas,
  continuous corners, drop shadow).
- Metronomes/: synthesised click sets (scripts/uigen/sounds.py).
- Skin/: the default stylesheets and colour theme (scripts/uigen/theme.py).
- preview.png: a contact sheet of both, for review.

Needs: python3, skia-python, fontTools.

    python3 scripts/uigen/uigen.py            # writes assets/ui
    python3 scripts/uigen/uigen.py --check    # fails if the output is stale

Icons are drawn on a 16 x 16 grid (y down, centre 8,8, artwork mostly in
2..14) with a 2-unit pen, round caps and joins: a softer, rounder cousin of
the solid look the skins were designed around.
"""

import hashlib
import io
import math
import os
import sys

import skia

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skins  # noqa: E402
import sounds  # noqa: E402
import theme  # noqa: E402
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import ReverseContourPen
from fontTools.pens.ttGlyphPen import TTGlyphPen

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(ROOT, "assets", "ui")

PEN = 2.0  # stroke width in grid units


# ---------------------------------------------------------------- geometry


def stroke(path, width=PEN, cap=skia.Paint.kRound_Cap, join=skia.Paint.kRound_Join):
    paint = skia.Paint(Style=skia.Paint.kStroke_Style, StrokeWidth=width, StrokeCap=cap, StrokeJoin=join, AntiAlias=True)
    out = skia.Path()
    paint.getFillPath(path, out, None, 4.0)
    return out


def union(*paths):
    acc = skia.Path()
    for p in paths:
        acc = skia.Op(acc, p, skia.PathOp.kUnion_PathOp)
    return acc


def minus(a, *bs):
    for b in bs:
        a = skia.Op(a, b, skia.PathOp.kDifference_PathOp)
    return a


def poly(pts, close=True):
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    return p


def line(*pts, w=PEN, cap=skia.Paint.kRound_Cap):
    return stroke(poly(pts, close=False), w, cap)


def circle(cx, cy, r):
    p = skia.Path()
    p.addCircle(cx, cy, r)
    return p


def ring(cx, cy, r, w=PEN):
    return minus(circle(cx, cy, r + w / 2), circle(cx, cy, r - w / 2))


def rrect(x, y, w, h, r):
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), r, r))
    return p


def arc(cx, cy, r, start, sweep, w=PEN, cap=skia.Paint.kRound_Cap):
    """Stroked arc; angles in degrees, 0 = east, clockwise (y down)."""
    p = skia.Path()
    p.addArc(skia.Rect.MakeLTRB(cx - r, cy - r, cx + r, cy + r), start, sweep)
    return stroke(p, w, cap)


def soft_poly(pts, r=0.6):
    """Filled polygon with corners rounded by r (stroke-and-fill)."""
    p = poly(pts)
    # Shrink by r, then grow back with round joins.
    inner = skia.Path()
    skia.Paint(Style=skia.Paint.kFill_Style).getFillPath(p, inner)
    paint = skia.Paint(Style=skia.Paint.kStrokeAndFill_Style, StrokeWidth=2 * r, StrokeJoin=skia.Paint.kRound_Join)
    shrunk = inset_polygon(pts, r)
    out = skia.Path()
    paint.getFillPath(poly(shrunk), out)
    return out


def inset_polygon(pts, d):
    """Offset a convex polygon (any winding) inwards by d."""
    n = len(pts)
    area = sum(pts[i][0] * pts[(i + 1) % n][1] - pts[(i + 1) % n][0] * pts[i][1] for i in range(n))
    sgn = 1 if area > 0 else -1
    lines = []
    for i in range(n):
        (x0, y0), (x1, y1) = pts[i], pts[(i + 1) % n]
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx, ny = -dy / L * sgn, dx / L * sgn  # inward normal
        lines.append(((x0 + nx * d, y0 + ny * d), (dx, dy)))
    out = []
    for i in range(n):
        (p, r), (q, s) = lines[i - 1], lines[i]
        den = r[0] * s[1] - r[1] * s[0]
        t = ((q[0] - p[0]) * s[1] - (q[1] - p[1]) * s[0]) / den
        out.append((p[0] + r[0] * t, p[1] + r[1] * t))
    return out


def tri(direction, cx=8, cy=8, size=10.0):
    """Solid rounded triangle pointing up/down/left/right."""
    h = size * 0.88
    pts = {
        "up": [(cx, cy - h / 2 - 0.6), (cx + size / 2 + 0.6, cy + h / 2), (cx - size / 2 - 0.6, cy + h / 2)],
        "down": [(cx, cy + h / 2 + 0.6), (cx - size / 2 - 0.6, cy - h / 2), (cx + size / 2 + 0.6, cy - h / 2)],
        "left": [(cx - h / 2 - 0.6, cy), (cx + h / 2, cy - size / 2 - 0.6), (cx + h / 2, cy + size / 2 + 0.6)],
        "right": [(cx + h / 2 + 0.6, cy), (cx - h / 2, cy + size / 2 + 0.6), (cx - h / 2, cy - size / 2 - 0.6)],
    }[direction]
    return soft_poly(pts, 0.7)


def arrowhead(tip, angle_deg, size=3.2):
    """Solid arrowhead with its tip at `tip`, pointing along angle."""
    a = math.radians(angle_deg)
    bx, by = tip[0] - math.cos(a) * size, tip[1] - math.sin(a) * size
    px, py = -math.sin(a) * size * 0.62, math.cos(a) * size * 0.62
    return soft_poly([tip, (bx + px, by + py), (bx - px, by - py)], 0.35)


def arc_arrow(cx, cy, r, start, sweep, w=PEN, head=4.6):
    """Stroked arc with an arrowhead at its end, along the direction of travel."""
    end = start + sweep
    turn = 1 if sweep > 0 else -1
    # Stop the line short of the head so the tip stays sharp.
    trim = math.degrees(head * 0.55 / r) * turn
    base = on_arc(cx, cy, r, end)
    d = end + 90 * turn
    tip = (base[0] + math.cos(math.radians(d)) * head * 0.75, base[1] + math.sin(math.radians(d)) * head * 0.75)
    return union(arc(cx, cy, r, start, sweep - trim, w), arrowhead(tip, d + turn * math.degrees(head * 0.4 / r), head))


def on_arc(cx, cy, r, deg):
    a = math.radians(deg)
    return (cx + r * math.cos(a), cy + r * math.sin(a))


def gear(cx, cy, r_out, r_in, teeth, hole):
    """Gear: a disc with rounded square teeth and a centre hole."""
    parts = [circle(cx, cy, r_in)]
    tw = 2 * math.pi * r_in / teeth * 0.5
    for i in range(teeth):
        t = rrect(cx - tw / 2, cy - r_out, tw, r_out - r_in + 1.0, 0.5)
        t.transform(skia.Matrix.RotateDeg(i * 360 / teeth, skia.Point(cx, cy)))
        parts.append(t)
    return minus(union(*parts), circle(cx, cy, hole))


def sine(x0, x1, cy, amp, w=PEN, cycles=1.0, steps=48):
    pts = [(x0 + (x1 - x0) * i / steps, cy - amp * math.sin(2 * math.pi * cycles * i / steps)) for i in range(steps + 1)]
    return line(*pts, w=w)


# ---------------------------------------------------------------- icons


def icons():
    """Code point -> path on the 16-grid."""
    g = {}
    g[0xE900] = tri("up")
    g[0xE901] = tri("left")
    g[0xE902] = tri("down")
    g[0xE903] = tri("right")
    g[0xE904] = rrect(4, 4, 8, 8, 1.4)  # stop
    g[0xE905] = line((3.5, 6), (8, 10.5), (12.5, 6))  # chevron down
    g[0xE906] = line((10, 3.5), (5.5, 8), (10, 12.5))  # chevron left
    g[0xE907] = line((6, 3.5), (10.5, 8), (6, 12.5))  # chevron right
    g[0xE908] = line((3.5, 10), (8, 5.5), (12.5, 10))  # chevron up
    # power: open ring + stem
    g[0xE909] = union(arc(8, 8.6, 5.2, -50, 280), line((8, 1.8), (8, 7.4)))
    # phase invert / null: ring with a slash through
    g[0xE90A] = union(ring(8, 8, 4.6), line((3, 13), (13, 3)))
    # redo: a ring travelling clockwise from the right round to the top,
    # head pointing right; undo is its mirror image
    redo = arc_arrow(8, 8.6, 5, 0, 262, head=4.2)
    undo = skia.Path(redo)
    undo.transform(skia.Matrix.MakeAll(-1, 0, 16, 0, 1, 0, 0, 0, 1))
    g[0xE90B] = redo
    g[0xE90C] = undo
    # settings: gear with a small drop-down mark
    g[0xE90D] = union(gear(7, 7, 6.2, 4.4, 7, 1.9), tri("down", 13.6, 13.4, 3.4))
    # metronome: rounded trapezoid outline with the pendulum
    body = stroke(poly([(5.6, 2.6), (10.4, 2.6), (13, 13.4), (3, 13.4)]), 1.8)
    g[0xE90E] = union(body, line((4, 10.4), (12, 10.4), w=1.6), line((8, 10.4), (13.6, 3.2), w=1.8), circle(13.6, 3.2, 1.3))
    g[0xE90F] = circle(8, 8, 5.4)  # record
    # up to parent: arrow to the top left
    g[0xE910] = union(line((12.5, 12.5), (5, 5)), soft_poly([(3.2, 3.2), (9.8, 3.6), (3.6, 9.8)], 0.5))
    # folder (open)
    back = rrect(2, 3.4, 11, 9.8, 1.2)
    tab = rrect(2, 2.4, 5, 3, 1)
    front = soft_poly([(4.2, 7), (15, 7), (12.6, 13.4), (1.6, 13.4)], 0.5)
    g[0xE911] = union(minus(union(back, tab), soft_poly([(3.4, 6), (15.6, 6), (13.4, 14.4), (0.6, 14.4)], 0.5)), front)
    # refresh: two arcs, two heads
    g[0xE912] = union(arc_arrow(8, 8, 5.2, 190, 125, head=4.0), arc_arrow(8, 8, 5.2, 10, 125, head=4.0))
    # preview backwards: ring with a left triangle
    g[0xE913] = union(ring(8, 8, 5.6, 1.8), tri("left", 7.6, 8, 4.2))
    # speaker with waves
    spk = soft_poly([(2, 6), (4.6, 6), (8.4, 2.8), (8.4, 13.2), (4.6, 10), (2, 10)], 0.5)
    g[0xE914] = union(spk, arc(8.4, 8, 2.8, -45, 90, 1.6), arc(8.4, 8, 5.4, -50, 100, 1.6))
    # lock
    g[0xE915] = minus(union(rrect(3, 7, 10, 8, 1.6), arc(8, 6.6, 3.2, 180, 180, 1.9), line((4.8, 6.6), (4.8, 7.5), w=1.9), line((11.2, 6.6), (11.2, 7.5), w=1.9)),
                      circle(8, 10.4, 1.3), rrect(7.4, 10.4, 1.2, 2.6, 0.5))
    # eraser: tilted block, light tip cut out, baseline
    m = skia.Matrix.RotateDeg(-35, skia.Point(8, 7))
    block = rrect(2.6, 4.4, 10.8, 5.4, 1.2)
    block.transform(m)
    cut = rrect(2.6, 4.4, 4.2, 5.4, 0)
    cut.transform(m)
    tip = rrect(3.8, 5.6, 2.2, 3.0, 0.5)
    tip.transform(m)
    g[0xE916] = union(minus(block, cut), tip, line((4, 14), (12.5, 14), w=1.6))
    # MIDI DIN socket: ring, five pins, key notch
    pins = [circle(*on_arc(8, 8, 3.4, a), 0.95) for a in (180, 225, 270, 315, 0)]
    g[0xE917] = union(ring(8, 8, 5.8, 1.6), rrect(7.2, 12.2, 1.6, 1.6, 0.3), *pins)
    # range ends and range
    g[0xE918] = union(line((2.5, 8), (10, 8), w=1.8), arrowhead((12, 8), 0, 4), line((13.4, 4.4), (13.4, 11.6), w=1.8))
    g[0xE919] = union(line((13.5, 8), (6, 8), w=1.8), arrowhead((4, 8), 180, 4), line((2.6, 4.4), (2.6, 11.6), w=1.8))
    g[0xE91A] = union(line((1.8, 4.4), (1.8, 11.6), w=1.8), line((14.2, 4.4), (14.2, 11.6), w=1.8),
                      arrowhead((3.4, 8), 180, 4), arrowhead((12.6, 8), 0, 4), line((5, 8), (11, 8), w=1.6))
    # crossfade: a span between two posts
    g[0xE91B] = union(line((1.6, 8), (4, 8), w=1.6), line((12, 8), (14.4, 8), w=1.6), line((5.4, 4.6), (5.4, 11.4), w=1.8),
                      line((10.6, 4.6), (10.6, 11.4), w=1.8), line((5.4, 8), (10.6, 8), w=1.6))
    g[0xE91C] = line((4, 8), (12, 8))  # minus
    g[0xE91D] = union(line((4, 8), (12, 8)), line((8, 4), (8, 12)))  # plus
    g[0xE91E] = union(line((4.5, 8), (11.5, 8), w=1.8), arrowhead((2.4, 8), 180, 3.8), arrowhead((13.6, 8), 0, 3.8))
    g[0xE91F] = sine(2, 14, 7.6, 4.2, 1.8)  # sine
    # sine over a baseline (thin)
    g[0xE920] = union(sine(2.2, 13.8, 7, 4.4, 1.1), line((1.8, 12.8), (14.2, 12.8), w=1.1), line((2.2, 11.6), (2.2, 12.8), w=1.1))
    g[0xE921] = line((2, 11.4), (5, 11.4), (5, 4.6), (11, 4.6), (11, 11.4), (14, 11.4), w=1.9)  # pulse
    g[0xE922] = union(line((4, 4), (12, 12)), line((12, 4), (4, 12)))  # close
    # camera
    cam = union(rrect(2, 5, 12, 8.4, 1.6), rrect(5.4, 3.2, 5.2, 3, 1))
    g[0xE923] = union(minus(cam, circle(8, 9.2, 3.1)), circle(8, 9.2, 1.6))
    # to start
    g[0xE924] = union(rrect(3, 3.4, 2, 9.2, 0.5), tri("left", 9.6, 8, 8))
    # loop: rounded rectangle path with a head
    lp = skia.Path()
    lp.moveTo(5.4, 11.6)
    lp.lineTo(4.6, 11.6)
    lp.arcTo(skia.Rect.MakeLTRB(2.2, 6.2, 6.8, 11.6), 90, 90, False)
    lp.lineTo(2.2, 7.6)
    lp.arcTo(skia.Rect.MakeLTRB(2.2, 3.8, 6.4, 8.6), 180, 90, False)
    lp.lineTo(11.4, 3.8)
    lp.arcTo(skia.Rect.MakeLTRB(9.6, 3.8, 13.8, 8.6), 270, 90, False)
    lp.lineTo(13.8, 9.4)
    lp.arcTo(skia.Rect.MakeLTRB(9.2, 7.0, 13.8, 11.6), 0, 90, False)
    lp.lineTo(9.8, 11.6)
    g[0xE925] = union(stroke(lp, 1.9), arrowhead((7.0, 11.6), 180, 4.4))
    # Q (quantise)
    g[0xE926] = union(stroke(skia.Path().addOval(skia.Rect.MakeLTRB(3.8, 2.4, 12.2, 12.6)), 1.7), line((9.4, 10.2), (12.4, 14.2), w=1.7))
    # record arm/retrigger: dot inside an open circular arrow
    g[0xE927] = union(circle(8.4, 8, 2.3), arc_arrow(8.4, 8, 5.4, -30, -270, 1.8, 4.4))
    # warning
    warn = stroke(poly([(8, 2.4), (14.2, 13.2), (1.8, 13.2)]), 1.7)
    g[0xE928] = union(warn, line((8, 6.4), (8, 9.4), w=1.7), circle(8, 11.4, 0.95))
    # A
    g[0xE929] = union(line((4.6, 12.6), (8, 3.2), (11.4, 12.6), w=1.5), line((5.9, 9.4), (10.1, 9.4), w=1.4))
    g[0xE92A] = ring(8, 8, 3.4, 1.4)  # ring
    g[0xE92B] = union(ring(5.8, 8, 3.6, 1.4), ring(10.2, 8, 3.6, 1.4))  # linked
    return g


NAMES = {
    0xE900: "triangle up", 0xE901: "triangle left", 0xE902: "triangle down", 0xE903: "triangle right",
    0xE904: "stop", 0xE905: "chevron down", 0xE906: "chevron left", 0xE907: "chevron right",
    0xE908: "chevron up", 0xE909: "power", 0xE90A: "phase invert", 0xE90B: "redo", 0xE90C: "undo",
    0xE90D: "settings menu", 0xE90E: "metronome", 0xE90F: "record", 0xE910: "up to parent",
    0xE911: "folder", 0xE912: "refresh", 0xE913: "reverse", 0xE914: "speaker", 0xE915: "lock",
    0xE916: "eraser", 0xE917: "MIDI", 0xE918: "to end", 0xE919: "to start", 0xE91A: "range",
    0xE91B: "crossfade", 0xE91C: "minus", 0xE91D: "plus", 0xE91E: "left-right", 0xE91F: "sine",
    0xE920: "wave on baseline", 0xE921: "pulse", 0xE922: "close", 0xE923: "snapshot",
    0xE924: "skip to start", 0xE925: "loop", 0xE926: "quantise", 0xE927: "retrigger record",
    0xE928: "warning", 0xE929: "A", 0xE92A: "ring", 0xE92B: "linked",
}


# ---------------------------------------------------------------- font


def _contours(path):
    """Split a skia path into contours of fontTools pen calls (16-grid -> font units)."""
    def tx(p):
        return (round(p.x() * 64), round((14 - p.y()) * 64))
    out, cur = [], None
    it = skia.Path.Iter(path, True)
    while True:
        verb, pts = it.next()
        if verb == skia.Path.kDone_Verb:
            break
        if verb == skia.Path.kMove_Verb:
            cur = RecordingPen()
            out.append(cur)
            cur.moveTo(tx(pts[0]))
        elif verb == skia.Path.kLine_Verb:
            if tx(pts[0]) != tx(pts[1]):
                cur.lineTo(tx(pts[1]))
        elif verb == skia.Path.kQuad_Verb:
            cur.qCurveTo(tx(pts[1]), tx(pts[2]))
        elif verb == skia.Path.kConic_Verb:
            quads = skia.Path.ConvertConicToQuads(pts[0], pts[1], pts[2], it.conicWeight(), 2)
            for i in range(1, len(quads) - 1, 2):
                cur.qCurveTo(tx(quads[i]), tx(quads[i + 1]))
        elif verb == skia.Path.kCubic_Verb:
            cur.curveTo(tx(pts[1]), tx(pts[2]), tx(pts[3]))
        elif verb == skia.Path.kClose_Verb:
            cur.closePath()
    return [c for c in out if len(c.value) > 2]


def _poly_of(rec):
    return [pt for _, args in rec.value for pt in args]


def _area(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly))) / 2


def _inside(pt, poly):
    x, y = pt
    n, inside = len(poly), False
    for i in range(n):
        (x0, y0), (x1, y1) = poly[i], poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            inside = not inside
    return inside


def to_glyph(path):
    """skia path on the 16-grid -> TrueType glyph (1024 upm, baseline at grid y 14).

    Contours are oriented by nesting depth (outer clockwise, holes
    anticlockwise), so the glyph fills correctly under the nonzero rule.
    """
    contours = _contours(path)
    polys = [_poly_of(c) for c in contours]
    pen = TTGlyphPen(None)
    cpen = Cu2QuPen(pen, 1.0)
    for i, (rec, pl) in enumerate(zip(contours, polys)):
        probe = pl[0]
        depth = sum(1 for j, other in enumerate(polys) if j != i and abs(_area(other)) > abs(_area(pl)) and _inside(probe, other))
        want_cw = depth % 2 == 0
        is_cw = _area(pl) < 0
        target = ReverseContourPen(cpen) if want_cw != is_cw else cpen
        rec.replay(target)
    return pen.glyph()


def build_font(glyphs, family, path):
    order = [".notdef", "space"] + [f"uni{cp:04X}" for cp in sorted(glyphs)]
    fb = FontBuilder(1024, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap({0x20: "space", **{cp: f"uni{cp:04X}" for cp in glyphs}})
    empty = TTGlyphPen(None).glyph()
    tt = {".notdef": empty, "space": empty}
    for cp, p in glyphs.items():
        p = skia.Path(p)
        p = skia.Op(p, skia.Path(), skia.PathOp.kUnion_PathOp)  # resolve overlaps
        tt[f"uni{cp:04X}"] = to_glyph(p)
    fb.setupGlyf(tt)
    metrics = {n: (1024, 0) for n in order}
    metrics["space"] = (512, 0)
    fb.setupHorizontalMetrics({n: (w, tt[n].xMin if hasattr(tt[n], "xMin") else 0) for n, (w, _) in metrics.items()})
    fb.setupHorizontalHeader(ascent=896, descent=-128)
    fb.setupNameTable({"familyName": family, "styleName": "Regular", "uniqueFontIdentifier": f"{family}-Regular",
                       "fullName": family, "psName": family, "version": "Version 1.0",
                       "copyright": "Dreist contributors. MIT OR Apache-2.0.",
                       "description": "Dreist UI icons (scripts/uigen/uigen.py)"})
    fb.setupOS2(sTypoAscender=896, sTypoDescender=-128, sTypoLineGap=0, usWinAscent=896, usWinDescent=128, achVendID="DRST")
    fb.setupPost()
    fb.setupHead(unitsPerEm=1024, created=0, modified=0)
    fb.font["head"].created = fb.font["head"].modified = 0x7C259DC0  # fixed: reproducible output
    buf = io.BytesIO()
    fb.save(buf)
    return buf.getvalue()


# ---------------------------------------------------------------- cursors

INK = skia.Color(0x1E, 0x24, 0x2B)  # pointer body
EDGE = skia.Color(0xF4, 0xF7, 0xF8)  # pointer outline
CARD = skia.Color(0xC8, 0xD3, 0xDB)  # drag cards
CARD_EDGE = skia.Color(0x3A, 0x45, 0x52)
GO = skia.Color(0x2E, 0xB8, 0x7A)  # "copy" badge
STOP = skia.Color(0xE0, 0x3A, 0x5E)


def fill(c, path, colour):
    c.drawPath(path, skia.Paint(Color=colour, AntiAlias=True))


def outline(c, path, colour, w):
    c.drawPath(path, skia.Paint(Color=colour, AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap))


def inked(c, path, w=1.6):
    """Dark shape with a light rim: readable on light and dark panels."""
    outline(c, path, EDGE, w)
    fill(c, path, INK)


def pointer(x=1.5, y=1.5, s=1.0):
    """Our pointer: a narrow dart with a notched tail."""
    pts = [(0, 0), (0, 10.5), (2.7, 8.2), (4.4, 11.8), (6.0, 11.1), (4.4, 7.6), (7.8, 7.4)]
    return poly([(x + px * s, y + py * s) for px, py in pts])


def badge_plus(c, cx, cy, r=3.6):
    fill(c, circle(cx, cy, r + 0.8), EDGE)
    fill(c, circle(cx, cy, r), GO)
    for p in (line((cx - r * 0.55, cy), (cx + r * 0.55, cy), w=1.3), line((cx, cy - r * 0.55), (cx, cy + r * 0.55), w=1.3)):
        fill(c, p, EDGE)


def dbl_arrow(cx, cy, length, vertical=False, w=1.4, head=3.2):
    h = length / 2
    if vertical:
        return union(line((cx, cy - h + 1.5), (cx, cy + h - 1.5), w=w), arrowhead((cx, cy - h), 270, head), arrowhead((cx, cy + h), 90, head))
    return union(line((cx - h + 1.5, cy), (cx + h - 1.5, cy), w=w), arrowhead((cx - h, cy), 180, head), arrowhead((cx + h, cy), 0, head))


def pencil(tip=(2, 2), length=15, width=4.2, angle=45):
    """Pencil with its tip at `tip`, running down-right at `angle`."""
    m = skia.Matrix()
    m.setRotate(angle - 90 + 0.0)
    body = union(soft_poly([(0, 0), (width / 2, 3.6), (-width / 2, 3.6)], 0.2),
                 rrect(-width / 2, 3.6, width, length - 6.0, 0.4),
                 rrect(-width / 2, length - 2.2, width, 2.2, 1.0))
    t = skia.Matrix.Translate(*tip)
    t.preRotate(angle - 90)
    body.transform(t)
    return body


def card(x, y, w, h, fold=3.5):
    return soft_poly([(x, y), (x + w - fold, y), (x + w, y + fold), (x + w, y + h), (x, y + h)], 0.6)


def cursor_images():
    """name -> (size, draw function, hotspot)."""
    cur = {}

    def reg(name, size, hot):
        def deco(fn):
            cur[name] = (size, fn, hot)
            return fn
        return deco

    @reg("Drag", (20, 20), (2, 2))
    def _(c):
        inked(c, pointer(2, 2))

    @reg("DragCopy", (20, 20), (2, 2))
    def _(c):
        inked(c, pointer(2, 2))
        badge_plus(c, 14.4, 14.4)

    @reg("Delete", (20, 20), (2, 2))
    def _(c):
        inked(c, pointer(2, 2))
        m = skia.Matrix.RotateDeg(-35, skia.Point(14, 14))
        e = rrect(9.2, 11.6, 9.6, 4.8, 1.2)
        e.transform(m)
        inked(c, e, 1.4)
        tip = rrect(9.2, 11.6, 3.2, 4.8, 1.0)
        tip.transform(m)
        fill(c, tip, STOP)

    @reg("DragAudio", (20, 20), (2, 2))
    def _(c):
        inked(c, pointer(2, 2))
        bars = [(11.0, 2.2), (13.0, 5.0), (15.0, 3.4), (17.0, 1.6)]
        for x, h in bars:
            outline(c, line((x, 14.5 - h), (x, 14.5 + h), w=1.3), EDGE, 1.6)
        for x, h in bars:
            fill(c, line((x, 14.5 - h), (x, 14.5 + h), w=1.3), INK)

    @reg("Preview", (20, 20), (2, 2))
    def _(c):
        inked(c, pointer(2, 2))
        spk = soft_poly([(10, 12.5), (12, 12.5), (15, 10), (15, 18.5), (12, 16), (10, 16)], 0.3)
        inked(c, union(spk, arc(15, 14.25, 2.6, -50, 100, 1.2)), 1.4)

    def env_arrows(c, arrows):
        inked(c, pointer(2, 2))
        inked(c, arrows, 1.5)

    @reg("DragEnvelopePointLR", (20, 20), (2, 2))
    def _(c):
        env_arrows(c, dbl_arrow(13, 15, 12))

    @reg("DragEnvelopePointUD", (20, 20), (2, 2))
    def _(c):
        env_arrows(c, dbl_arrow(14.5, 12, 14, vertical=True))

    @reg("DragEnvelopePointMulti", (20, 20), (2, 2))
    def _(c):
        env_arrows(c, union(dbl_arrow(12.4, 15.6, 10), dbl_arrow(15.8, 9.4, 13, vertical=True)))

    @reg("ResizeBiDir", (20, 20), (2, 2))
    def _(c):
        env_arrows(c, dbl_arrow(12, 15, 13))

    @reg("Zoom", (20, 20), (2, 2))
    def _(c):
        inked(c, pointer(2, 2))
        inked(c, union(ring(13, 12, 3.2, 1.5), line((15.4, 14.4), (18, 17), w=1.9)), 1.4)

    @reg("Pen", (20, 20), (2, 2))
    def _(c):
        inked(c, pencil((2, 2), 18, 4.4), 1.4)

    @reg("Multi", (20, 20), (2, 2))
    def _(c):
        inked(c, pencil((2, 2), 14, 4.0), 1.4)
        inked(c, union(line((14.5, 11.5), (14.5, 18.5), w=1.6), line((11, 15), (18, 15), w=1.6)), 1.4)

    @reg("Selection", (20, 20), (10, 10))
    def _(c):
        cross = union(line((10, 3), (10, 8), w=1.4), line((10, 12), (10, 17), w=1.4), line((3, 10), (8, 10), w=1.4), line((12, 10), (17, 10), w=1.4))
        inked(c, union(cross, circle(10, 10, 0.9)), 1.6)

    @reg("NotAllowed", (20, 20), (10, 10))
    def _(c):
        sym = union(ring(10, 10, 6.4, 2.2), line((5.6, 14.4), (14.4, 5.6), w=2.2, cap=skia.Paint.kButt_Cap))
        outline(c, sym, EDGE, 1.6)
        fill(c, sym, STOP)

    def bracket(c, x, flip, h0=3, h1=17, w=1.8, foot=3.2):
        d = -foot if flip else foot
        inked(c, line((x + d, h0), (x, h0), (x, h1), (x + d, h1), w=w), 1.4)

    @reg("ResizeLeft", (20, 20), (3, 10))
    def _(c):
        bracket(c, 3, False)
        inked(c, union(line((7.5, 10), (15, 10), w=1.4), arrowhead((16.6, 10), 0, 3.0), arrowhead((6.4, 10), 180, 3.0)), 1.3)

    @reg("ResizeRight", (20, 20), (16, 10))
    def _(c):
        bracket(c, 16, True)
        inked(c, union(line((5, 10), (12.5, 10), w=1.4), arrowhead((3.4, 10), 180, 3.0), arrowhead((13.6, 10), 0, 3.0)), 1.3)

    @reg("ResizeRightThin", (10, 20), (7, 2))
    def _(c):
        bracket(c, 7, True, 2, 18, 1.6, 4.4)

    @reg("Trash", (20, 23), (10, 11))
    def _(c):
        can = union(soft_poly([(4.4, 6.8), (15.6, 6.8), (14.6, 20.6), (5.4, 20.6)], 0.8), rrect(3, 4.2, 14, 2.2, 1), rrect(8, 2.2, 4, 2.6, 0.8))
        can = minus(can, rrect(7.6, 9, 1.2, 9, 0.6), rrect(11.2, 9, 1.2, 9, 0.6))
        inked(c, can, 1.6)

    def tm(c, kind):
        inked(c, pointer(1.5, 1.5))
        if kind in ("primary",):
            inked(c, ring(17.5, 17.5, 2.6, 1.6), 1.4)
        if kind in ("secondary", "both"):
            inked(c, union(arrowhead((18.5, 10.6), 270, 3.6), arrowhead((18.5, 22.2), 90, 3.6)), 1.4)
        if kind == "both":
            fill(c, circle(18.5, 16.4, 2.2), EDGE)
            fill(c, circle(18.5, 16.4, 1.5), INK)

    @reg("TransmodPrimary", (24, 24), (1, 1))
    def _(c):
        tm(c, "primary")

    @reg("TransmodSecondary", (24, 24), (1, 1))
    def _(c):
        tm(c, "secondary")

    @reg("TransmodBoth", (24, 24), (1, 1))
    def _(c):
        tm(c, "both")

    @reg("DragFile", (40, 40), (20, 20))
    def _(c):
        p = card(9, 4, 22, 30, 6)
        fill(c, p, CARD)
        outline(c, p, CARD_EDGE, 1.4)
        inked(c, pointer(20, 20, 1.15))

    @reg("DragFiles", (40, 40), (20, 20))
    def _(c):
        for dx in (0, 3.5, 7):
            p = card(4 + dx, 4 + dx, 21, 28, 5.5)
            fill(c, p, CARD)
            outline(c, p, CARD_EDGE, 1.4)
        inked(c, pointer(20, 20, 1.15))

    @reg("DragFolder", (40, 40), (20, 20))
    def _(c):
        back = union(rrect(4, 8, 28, 22, 2.4), rrect(4, 5, 11, 6, 2))
        fill(c, back, CARD)
        outline(c, back, CARD_EDGE, 1.4)
        front = soft_poly([(9, 14), (36, 14), (31, 31), (3, 31)], 1.0)
        fill(c, front, skia.Color(0xDD, 0xE5, 0xEA))
        outline(c, front, CARD_EDGE, 1.4)
        inked(c, pointer(20, 20, 1.15))

    def pad(c, copy):
        tile = rrect(1, 1, 20, 15, 2.2)
        fill(c, tile, skia.Color(0x55, 0x5D, 0x63))
        outline(c, tile, EDGE, 1.2)
        for i in range(5):
            fill(c, rrect(3 + i * 3.4, 12, 2.6, 2, 0.4), skia.Color(0x3C, 0x42, 0x47))
        inked(c, pointer(8, 4, 0.95))
        if copy:
            badge_plus(c, 19.6, 14.6, 3.2)

    @reg("DragPad", (25, 20), (8, 4))
    def _(c):
        pad(c, False)

    @reg("DragPadCopy", (25, 20), (8, 4))
    def _(c):
        pad(c, True)

    def pattern(c, mode):
        sheet = rrect(1.5, 1.5, 12, 21, 1.6)
        fill(c, sheet, skia.Color(0xEE, 0xF2, 0xF4))
        outline(c, sheet, CARD_EDGE, 1.2)
        for i, x in enumerate((3.5, 6.5, 9.5)):
            fill(c, rrect(x, 4 + i * 4, 2.4, 1.6, 0.4), CARD_EDGE)
        if mode == "end":
            fill(c, union(tri("right", 6.4, 4.2, 3.0), tri("right", 9.0, 4.2, 3.0)), CARD_EDGE)
        inked(c, pointer(7, 11, 0.95))
        if mode == "copy":
            badge_plus(c, 15.4, 6.0, 3.2)

    @reg("DragPattern", (20, 25), (7, 11))
    def _(c):
        pattern(c, "")

    @reg("DragPatternCopy", (20, 25), (7, 11))
    def _(c):
        pattern(c, "copy")

    @reg("DragPatternToEnd", (20, 25), (7, 11))
    def _(c):
        pattern(c, "end")

    @reg("DragWave", (250, 20), (2, 10))
    def _(c):
        strip = rrect(0.5, 0.5, 249, 19, 2)
        fill(c, strip, skia.ColorSetARGB(0xC8, 0xDD, 0xE5, 0xEA))
        outline(c, strip, CARD_EDGE, 1.0)
        # A decaying hit drawn as a filled envelope.
        top, bot = [], []
        for i in range(120):
            x = 4 + i * 1.0
            a = 7.5 * math.exp(-i / 26.0) * (0.55 + 0.45 * abs(math.sin(i * 0.9) * math.cos(i * 0.37)))
            top.append((x, 10 - a - 0.4))
            bot.append((x, 10 + a + 0.4))
        fill(c, poly(top + bot[::-1]), CARD_EDGE)
        fill(c, rrect(1.2, 1.5, 1.6, 17, 0.6), INK)

    return cur


def render_cursor(size, fn):
    surf = skia.Surface(*size)
    with surf as c:
        c.clear(skia.ColorTRANSPARENT)
        fn(c)
    img = surf.makeImageSnapshot()
    return bytes(img.encodeToData(skia.kPNG, 100))


def hotspots_xml(cur):
    rows = "\n".join(f'        <CursorHotspot x="{hot[0]}" y="{hot[1]}" cursorName="{name}" />' for name, (_, _, hot) in sorted(cur.items()))
    return ("<root>\n    <!-- Generated by scripts/uigen/uigen.py. -->\n"
            '    <VObjectArray_CursorHotspot name="Hotspots" >\n' + rows + "\n    </VObjectArray_CursorHotspot>\n</root>\n")


# ---------------------------------------------------------------- app icon

# The header logo (dreist_gui::render, `geist_logo`) on its 50 x 50 grid.
LOGO_STEM = [(9.0, 9.0), (16.0, 9.0), (16.0, 41.0), (9.0, 41.0)]
LOGO_BOWL = [(18.0, 9.0), (28.0, 9.0), (36.0, 13.0), (41.0, 20.0), (41.0, 30.0), (36.0, 37.0), (28.0, 41.0),
             (18.0, 41.0), (18.0, 34.0), (27.0, 34.0), (32.0, 31.0), (34.0, 27.0), (34.0, 23.0), (32.0, 19.0),
             (27.0, 16.0), (18.0, 16.0)]


def squircle(x, y, size, n=5.0, steps=360):
    """Superellipse |x|^n + |y|^n = 1: the continuous-corner shape of macOS icons."""
    r = size / 2
    cx, cy = x + r, y + r
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        c, s_ = math.cos(t), math.sin(t)
        pts.append((cx + r * math.copysign(abs(c) ** (2 / n), c), cy + r * math.copysign(abs(s_) ** (2 / n), s_)))
    return poly(pts)


def app_icon(px):
    """The app icon at px x px (macOS grid: body 824/1024, shadow below)."""
    k = px / 1024
    surf = skia.Surface(px, px)
    body = squircle(100 * k, 100 * k, 824 * k)
    with surf as c:
        c.clear(skia.ColorTRANSPARENT)
        if px >= 64:
            shadow = skia.Paint(Color=skia.ColorSetARGB(0x70, 0, 0, 0), AntiAlias=True,
                                MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 14 * k))
            sh = skia.Path(body)
            sh.offset(0, 12 * k)
            c.drawPath(sh, shadow)
        grad = skia.GradientShader.MakeLinear([skia.Point(0, 100 * k), skia.Point(0, 924 * k)],
                                              [skia.Color(0x3A, 0x42, 0x45), skia.Color(0x1F, 0x24, 0x25)])
        c.drawPath(body, skia.Paint(Shader=grad, AntiAlias=True))
        # A faint top highlight along the rim.
        c.save()
        c.clipPath(body, doAntiAlias=True)
        c.drawPath(body, skia.Paint(Color=skia.ColorSetARGB(0x30, 0xFF, 0xFF, 0xFF), AntiAlias=True,
                                    Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.0, 6 * k)))
        c.restore()
        # The mark: frame + D, 50-unit logo scaled to 560 px, centred.
        s = 560 * k / 50
        o = 512 * k - 25 * s
        c.save()
        c.translate(o, o)
        c.scale(s, s)
        blue = skia.GradientShader.MakeLinear([skia.Point(0, 0), skia.Point(0, 50)],
                                              [skia.Color(0x9C, 0xD3, 0xFF), skia.Color(0x5E, 0x9F, 0xD6)])
        mark = union(stroke(rrect(1.5, 1.5, 47, 47, 2.0), 3.0, join=skia.Paint.kMiter_Join), poly(LOGO_STEM), poly(LOGO_BOWL))
        c.drawPath(mark, skia.Paint(Shader=blue, AntiAlias=True))
        c.restore()
    return bytes(surf.makeImageSnapshot().encodeToData(skia.kPNG, 100))


def icns():
    """AppIcon.icns: PNG entries for 16..1024 px (1x and 2x)."""
    kinds = [("icp4", 16), ("icp5", 32), ("icp6", 64), ("ic07", 128), ("ic08", 256), ("ic09", 512), ("ic10", 1024),
             ("ic11", 32), ("ic12", 64), ("ic13", 256), ("ic14", 512)]
    cache = {}
    body = b""
    for kind, px in kinds:
        if px not in cache:
            cache[px] = app_icon(px)
        body += kind.encode() + (8 + len(cache[px])).to_bytes(4, "big") + cache[px]
    return b"icns" + (8 + len(body)).to_bytes(4, "big") + body, cache[1024]


# ---------------------------------------------------------------- preview


def preview(glyphs, cursors, font_bytes):
    cols, cell = 11, 64
    rows_icons = (len(glyphs) + cols - 1) // cols
    rows_cur = (len(cursors) + 7) // 8
    W = cols * cell + 20
    H = 40 + rows_icons * (cell + 18) + 30 + rows_cur * 74 + 20
    surf = skia.Surface(W, H)
    light = skia.Color(0xED, 0xF1, 0xF2)
    dark = skia.Color(0x28, 0x2E, 0x2D)
    tf = skia.Typeface.MakeFromData(skia.Data.MakeWithCopy(font_bytes))
    label_font = skia.Font(skia.Typeface("DejaVu Sans"), 9)
    with surf as c:
        c.clear(light)
        c.drawString("Dreist-Icons (U+E900..)", 10, 22, skia.Font(skia.Typeface("DejaVu Sans"), 13), skia.Paint(Color=dark, AntiAlias=True))
        for i, cp in enumerate(sorted(glyphs)):
            x, y = 10 + (i % cols) * cell, 34 + (i // cols) * (cell + 18)
            bg = dark if (i // cols) % 2 else skia.Color(0x67, 0x6E, 0x72)
            c.drawRect(skia.Rect.MakeXYWH(x + 2, y, cell - 4, cell - 4), skia.Paint(Color=bg))
            # Big and at UI size (14 px).
            c.drawString(chr(cp), x + 8, y + 40, skia.Font(tf, 32), skia.Paint(Color=light, AntiAlias=True))
            c.drawString(chr(cp), x + 42, y + 54, skia.Font(tf, 14), skia.Paint(Color=skia.Color(0x86, 0xC8, 0xFF), AntiAlias=True))
            c.drawString(f"{cp:04X}", x + 4, y + cell + 8, label_font, skia.Paint(Color=dark, AntiAlias=True))
        y0 = 34 + rows_icons * (cell + 18) + 16
        c.drawString("Cursors (1x)", 10, y0, skia.Font(skia.Typeface("DejaVu Sans"), 13), skia.Paint(Color=dark, AntiAlias=True))
        for i, (name, (size, fn, hot)) in enumerate(sorted(cursors.items())):
            x, y = 10 + (i % 8) * 88, y0 + 10 + (i // 8) * 74
            bg = skia.Color(0x67, 0x6E, 0x72) if i % 2 else skia.Color(0xBA, 0xBC, 0xBD)
            c.drawRect(skia.Rect.MakeXYWH(x, y, 84, 56), skia.Paint(Color=bg))
            c.save()
            c.translate(x + 4, y + 4)
            sc = min(2.0, 76 / size[0], 48 / size[1])
            c.scale(sc, sc)
            fn(c)
            c.restore()
            c.drawString(name[:16], x, y + 66, label_font, skia.Paint(Color=dark, AntiAlias=True))
    return bytes(surf.makeImageSnapshot().encodeToData(skia.kPNG, 100))


# ---------------------------------------------------------------- main


def outputs():
    glyphs = icons()
    font = build_font(glyphs, "Dreist-Icons", None)
    cur = cursor_images()
    files = {"Fonts/Dreist-Icons.ttf": font, "Cursors/Cursors.hotspots": hotspots_xml(cur).encode()}
    for name, (size, fn, _) in cur.items():
        files[f"Cursors/{name}.png"] = render_cursor(size, fn)
    files["AppIcon.icns"], files["AppIcon.png"] = icns()
    files.update(theme.outputs())
    files.update(sounds.outputs())
    files.update(skins.outputs())
    files["preview.png"] = preview(glyphs, cur, font)
    return files


def main():
    check = "--check" in sys.argv
    stale = []
    for rel, data in sorted(outputs().items()):
        path = os.path.join(OUT, rel)
        old = open(path, "rb").read() if os.path.exists(path) else None
        if old == data:
            continue
        if check:
            stale.append(rel)
            continue
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        print("wrote", rel, hashlib.sha1(data).hexdigest()[:8])
    if stale:
        print("stale:", ", ".join(stale))
        sys.exit(1)


if __name__ == "__main__":
    main()
