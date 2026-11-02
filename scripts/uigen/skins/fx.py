"""The 42 effect panels (Effects/FX/<Effect>.skin).

Each effect is described by what it controls, and one layout rule places
everything: an optional level meter on top, the knobs in even rows (the
knob size follows how many share a row), a strip of switches, and an
optional response plot along the bottom.  Control names (Control1..9,
VUMeter, Display) are what the editor binds to the effect's parameters.
"""

from . import N, skin, spread

W, H = 210, 137
LABEL = 13          # room for the knob caption below each knob
SWITCH_H = 18

# Knob tuples: (control, caption).  Switch tuples: (control, kind, tooltip,
# text, width) with kind "btn" (toggle) or "pop" (menu).
FX = {
    "Gain": dict(knobs=[("Control1", "Gain")]),
    "StereoWidth": dict(knobs=[("Control1", "Gain"), ("Control2", "Width")]),
    "DirtyDac": dict(knobs=[("Control1", "Rate"), ("Control2", "Anti-alias")]),
    "Shifter": dict(knobs=[("Control1", "Shift"), ("Control2", "Amount")]),
    "Chorus": dict(knobs=[("Control1", "Rate"), ("Control2", "Depth"), ("Control3", "Width")]),
    "GuruFilter": dict(knobs=[("Control1", "Mode"), ("Control2", "Cutoff"), ("Control3", "Reso")]),
    "BreverbInverse": dict(knobs=[("Control1", "Time"), ("Control2", "Pre-delay"), ("Control3", "Diffuse")]),
    "BreverbHall": dict(knobs=[("Control1", "Time"), ("Control4", "Size"), ("Control2", "Pre-delay"),
                               ("Control6", "Shape"), ("Control5", "Width"), ("Control3", "Diffuse")]),
    "BreverbPlate": dict(knobs=[("Control1", "Time"), ("Control4", "Size"), ("Control2", "Pre-delay"),
                                ("Control5", "Width"), ("Control3", "Diffuse")]),
    "BreverbRoom": dict(knobs=[("Control1", "Time"), ("Control4", "Size"), ("Control2", "Pre-delay"),
                               ("Control5", "Width"), ("Control3", "Diffuse")]),
    "FXpansionReverb": dict(knobs=[("Control1", "Room"), ("Control4", "Density"), ("Control2", "Decay"),
                                   ("Control3", "Pre-delay"), ("Control5", "Damp Hz"), ("Control6", "Damp")]),
    "TinCan": dict(knobs=[("Control2", "Size"), ("Control1", "Decay"), ("Control3", "Damp"),
                          ("Control4", "Pinch"), ("Control5", "Squeeze")]),
    "Crusher": dict(knobs=[("Control1", "Drive"), ("Control3", "Bits"), ("Control2", "Rate"),
                           ("Control5", "Low Cut"), ("Control4", "High Cut"), ("Control6", "Tone")]),
    "Flanger": dict(knobs=[("Control1", "Rate"), ("Control2", "Depth"), ("Control4", "Feedback"),
                           ("Control3", "Offset"), ("Control6", "Phase"), ("Control5", "Width")]),
    "Freezer": dict(knobs=[("Control1", "Gate"), ("Control2", "Loop"), ("Control3", "Grain"),
                           ("Control4", "Smooth"), ("Control6", "Speed"), ("Control5", "Scratch")]),
    "NoiseGate": dict(knobs=[("Control4", "Threshold"), ("Control5", "Hysteresis"), ("Control6", "Key LPF"),
                             ("Control1", "Attack"), ("Control2", "Hold"), ("Control3", "Release")]),
    "Delay": dict(knobs=[("Control1", "Time"), ("Control2", "Feedback"), ("Control5", "Swing"),
                         ("Control3", "Low Cut"), ("Control4", "High Cut")],
                  switches=[("Control6", "btn", "Tempo Sync", "Sync", 44)]),
    "Bloom": dict(knobs=[("Control2", "Time"), ("Control3", "Feedback"), ("Control4", "Tone")],
                  switches=[("Control1", "pop", "Delay Model", None, 58), ("Control5", "btn", "Tempo Sync", "Sync", 32),
                            ("Control6", "btn", "Freeze", "Hold", 32), ("Control7", "btn", "Ping-Pong", "P-P", 28),
                            ("Control8", "btn", "Reverse", "Rev", 28)]),
    "Amber": dict(knobs=[("Control2", "Rate"), ("Control3", "Width")],
                  switches=[("Control1", "pop", "Model", None, 76), ("Control4", "btn", "Bright", "Bright", 48)]),
    "AnalogRingMod": dict(knobs=[("Control2", "Drive"), ("Control3", "Pitch"), ("Control4", "Tone")],
                          switches=[("Control1", "pop", "Carrier", None, 84)]),
    "RingSting": dict(knobs=[("Control1", "Drive"), ("Control3", "Pitch")],
                      switches=[("Control2", "pop", "Carrier", None, 84)]),
    "Enhancer": dict(knobs=[("Control1", "Freq"), ("Control3", "Amount")],
                     switches=[("Control2", "pop", "Model", None, 84)]),
    "ModelFilter": dict(knobs=[("Control1", "Drive"), ("Control3", "Cutoff"), ("Control4", "Reso")],
                        switches=[("Control2", "pop", "Filter Model", None, 84)]),
    "Comb": dict(knobs=[("Control1", "Drive"), ("Control3", "Pitch"), ("Control4", "Reso")],
                 switches=[("Control2", "btn", "Polarity", "Invert", 56)]),
    "Distortion": dict(knobs=[("Control2", "Drive"), ("Control5", "Tone"), ("Control6", "Dry"),
                              ("Control4", "Low Cut"), ("Control3", "High Cut")],
                       switches=[("Control1", "pop", "Curve", None, 84)]),
    "DrumDynamics": dict(knobs=[("Control1", "Attack"), ("Control2", "Sustain")],
                         switches=[("Control4", "btn", "Mono Sidechain", "Mono Key", 60),
                                   ("Control3", "btn", "Fast Envelopes", "Fast", 40)]),
    "EnvShaper": dict(knobs=[("Control1", "Attack"), ("Control2", "Sustain"), ("Control4", "Sense"), ("Control3", "Gain")],
                      switches=[("Control5", "btn", "Link Channels", "Link", 48)]),
    "Mault": dict(knobs=[("Control2", "Drive"), ("Control3", "Input"), ("Control4", "Output")],
                  switches=[("Control1", "pop", "Curve", None, 72), ("Control5", "btn", "Saturation", "Sat", 36),
                            ("Control6", "btn", "Limiter", "Limit", 40)]),
    "SingleMault": dict(knobs=[("Control2", "Drive"), ("Control3", "Post Hz"), ("Control4", "Restore"), ("Control5", "Output")],
                        switches=[("Control1", "pop", "Curve", None, 80), ("Control6", "btn", "Saturation", "Sat", 40)]),
    "Maul": dict(knobs=[("Control2", "Lo Hz"), ("Control3", "Lo Res"), ("Control6", "Hi Hz"), ("Control7", "Hi Res"),
                        ("Control4", "Lo Drive"), ("Control5", "Lo Gain"), ("Control8", "Hi Drive"), ("Control9", "Hi Gain")],
                 switches=[("Control1", "pop", "Curve", None, 84)], switch_top=True),
    "ModFilter": dict(knobs=[("Control2", "Cutoff"), ("Control3", "Reso"), ("Control6", "Env Amt"),
                             ("Control4", "Attack"), ("Control5", "Decay")],
                      switches=[("Control1", "pop", "Filter Type", None, 84)]),
    "PhaseMod": dict(knobs=[("Control1", "Pitch"), ("Control3", "Stack"), ("Control5", "Spread"),
                            ("Control6", "Depth"), ("Control4", "Width")],
                     switches=[("Control2", "pop", "Algorithm", None, 64)]),
    "Phaser": dict(knobs=[("Control5", "Rate"), ("Control6", "Depth"), ("Control4", "Feedback"),
                          ("Control3", "Pitch"), ("Control1", "Drive")],
                   switches=[("Control2", "pop", "Stages", None, 56)]),
    "BusComp": dict(knobs=[("Control1", "Thresh"), ("Control3", "Ratio"), ("Control2", "Attack"),
                           ("Control4", "Release"), ("Control5", "Makeup")],
                    switches=[("Control6", "btn", "Limiter", "Limit", 44)], meter=True),
    "ChanComp": dict(knobs=[("Control1", "Input"), ("Control2", "Attack"), ("Control3", "Release"), ("Control5", "Output")],
                     switches=[("Control4", "pop", "Ratio", None, 60)], meter=True),
    "VCAComp": dict(knobs=[("Control3", "Thresh"), ("Control6", "Ratio"), ("Control1", "Attack"),
                           ("Control2", "Release"), ("Control4", "Key In"), ("Control5", "Output")], meter=True),
    "Limiter": dict(knobs=[("Control2", "Input"), ("Control1", "Knee"), ("Control3", "Output")], meter=True),
    "DJEQ": dict(knobs=[("Control1", "Low"), ("Control2", "Mid"), ("Control3", "Mid Hz"), ("Control4", "High")], plot=True),
    "HILO": dict(knobs=[("Control1", "Tilt"), ("Control2", "Pivot")], plot=True),
    "Filter": dict(knobs=[("Control4", "Lo Hz"), ("Control2", "Hi Hz")],
                   switches=[("Control3", "btn", "Low Pass", "LP", 32), ("Control1", "btn", "High Pass", "HP", 32)], plot=True,
                   switch_inline=True),
    "ParaEQ": dict(knobs=[("Control2", "Lo Hz"), ("Control3", "Lo dB"), ("Control1", "Lo Q"),
                          ("Control5", "Hi Hz"), ("Control6", "Hi dB"), ("Control4", "Hi Q")], plot=True),
    "VariEQ": dict(knobs=[("Control2", "Freq"), ("Control3", "Q"), ("Control4", "Gain")],
                   switches=[("Control1", "pop", "EQ Shape", None, 56)], plot=True, switch_inline=True, root_name="VarLab"),
}


def knob_size(per_row, rows, band_h):
    """The largest knob from our size ladder that fits the band."""
    by_count = {1: 72, 2: 56, 3: 48, 4: 40}.get(per_row, 34)
    fit = band_h / rows - LABEL - 4
    for s in (72, 56, 48, 40, 34, 32, 28, 24):
        if s <= by_count and s <= fit:
            return s
    return 24


def rows_for(n, compact):
    if n <= (6 if compact else 4):
        return [n]
    if n == 5:
        return [3, 2]
    half = (n + 1) // 2
    return [half, n - half]


def switch(name, kind, tip, text, rect):
    if kind == "pop":
        return N("PopupButton", name, rect, displayName=tip, style="DefaultPopupButtonStyle")
    return N("Button", name, rect, displayName=tip, text=text, style="DefaultButtonStyle")


def switch_box(sw, x, y, vertical=False, gap=5):
    """Switches in an unlabelled box (the labeller captions only knobs)."""
    kids, at = [], 0
    for name, kind, tip, text, w in sw:
        r = (0, at, w, SWITCH_H) if vertical else (at, 0, w, SWITCH_H)
        kids.append(switch(name, kind, tip, text, r))
        at += (SWITCH_H if vertical else w) + gap
    at -= gap
    size = (max(s[4] for s in sw), at) if vertical else (at, SWITCH_H)
    if x is None:
        x = (W - size[0]) // 2
    return N("Panel", None, (x, y, *size), kids=kids, style="InvisibleStyle")


def panel(spec):
    kids = []
    top, bottom = 4, H - 4
    sw = spec.get("switches", [])
    if spec.get("meter"):
        mx = (W - 96) // 2 - (28 if sw else 0)
        kids.append(N("Meter", "VUMeter", (mx, top, 96, 30), style="MeterStyle", realRadius=0.75,
                      textLeftRange="-∞", textRightRange="0", textUnits="dB"))
        if sw:
            kids.append(switch_box(sw, mx + 104, top + 6))
            sw = []
        top += 34
    if spec.get("plot"):
        ph = 70
        kids.append(N("PolyPlot", "Display", (3, H - ph, W - 6, ph), id=100000, overloadClass="EffectEQPlot", style="PlotStyle"))
        bottom = H - ph - 2
    knobs = spec["knobs"]
    inline = spec.get("switch_inline")
    if sw and not inline:
        if spec.get("switch_top"):
            kids.append(switch_box(sw, None, top))
            top += SWITCH_H + 4
        else:
            kids.append(switch_box(sw, None, bottom - SWITCH_H))
            bottom -= SWITCH_H + 6
    rows = rows_for(len(knobs), spec.get("plot", False) or (spec.get("meter", False) and len(knobs) <= 5))
    # Inline switches take one column at the right of a single knob row.
    cols_extra = 1 if inline else 0
    size = knob_size(rows[0] + cols_extra, len(rows), bottom - top)
    if spec.get("plot"):
        size = min(size, 28 if len(knobs) > 4 else 34)
    cell = size + LABEL
    ys = spread(len(rows), cell, bottom - top)
    i = 0
    for r, n in enumerate(rows):
        y = top + ys[r]
        width = W - (64 if inline else 0)
        for x in spread(n, size, width):
            name, cap = knobs[i]
            kids.append(N("TransmodKnob", name, (x, y, size, size), displayName=cap, style="TransmodStyle"))
            i += 1
    if inline:
        sh = len(sw) * (SWITCH_H + 4) - 4
        sy = top + (cell - sh) // 2 if len(rows) == 1 else top
        kids.append(switch_box([(a, b, c, d, 56) for a, b, c, d, _ in sw], W - 62, sy, vertical=True, gap=4))
    return N("Labeller", spec.get("root_name"), (0, 0, W, H), kids=kids, style="SmallControlLabellerStyle",
             enumTextPosition="Below", intTextOffset=1, id=6000)


def outputs():
    return {f"Skin/Effects/FX/{k}.skin": skin(panel(v)) for k, v in sorted(FX.items())}
