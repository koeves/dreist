"""A layer's parameter strip (Pad Editor/LayerParams.skin): a row of
folding sections, each a grid of 36 px knobs (two rows of 48 px plus a
switch row at the foot), the envelopes as fader banks.  Control names are
the layer parameters the editor binds."""

from . import N, skin

H = 176
HEAD = 20
K = 36
PITCH = 49          # knob + caption
FOOT1, FOOT2 = H - 48, H - 26    # the two switch rows


def section(name, title, w, kids):
    return N("CollapsePanel", name, (0, 0, w, H), pin="tb", displayName=title, iconicTarget="ARLeft", style="CollapsePanelStyle",
             kids=[N("Panel", None, (w - 1, 0, 1, H - 12), pin="rtb", style="LightDividerStyle")] + kids)


def knob(name, cap, x, y, centred=False, size=K):
    return N("TransmodKnob", name, (x, y, size, size), displayName=cap, style="TransmodStyle", optCentered=centred or None)


def lab(name, rect, kids, pin="", offset=-1, style="SmallControlLabellerStyle"):
    return N("Labeller", name, rect, pin=pin, enumTextPosition="Below", intTextOffset=offset, style=style, kids=kids)


def button(name, rect, text, tip=None, style="DefaultButtonStyle", pin=""):
    return N("Button", name, rect, pin=pin, displayName=tip, style=style, text=text)


def col(x, w):
    """x of a knob centred in a w-wide column starting at x."""
    return x + (w - K) // 2


def setup():
    w = 98
    return section("ModesPanel", "SETUP", w, [
        lab("SetupLabeller", (0, HEAD, w - 4, H - HEAD), pin="lrtb", offset=1, kids=[
            N("PopupButton", "PlayMode", (2, 6, w - 8, 20), pin="lr", displayName="Playback", style="ShorteningPopupButtonStyle"),
            N("PopupButton", "Choke", (2, 46, w - 8, 20), pin="lr", displayName="Choke group", style="ShorteningPopupButtonStyle"),
            button("EnvMode", (2, 86, w - 8, 20), "Track Pitch", "Envelope timing"),
            *[button(n, (2 + i * 23, 128, 21, 20), t, tip) for i, (n, t, tip) in enumerate([
                ("PS", "S", "Set the sample start here"), ("PE", "E", "Set the sample end here"),
                ("LS", "LS", "Set the loop start here"), ("LE", "LE", "Set the loop end here")])],
        ])])


def mix():
    w = 56
    return section("MixPanel", "MIX", w, [
        lab("MixLabeller", (0, HEAD, w, H - HEAD), pin="lrtb", kids=[
            knob("VoiceGain", "Gain", col(0, w - 2), 6), knob("VoicePan", "Pan", col(0, w - 2), 6 + PITCH, True)]),
        button("LayerMode", (3, FOOT1, w - 8, 20), "Vintage", "Vintage playback"),
        button("Reverse", (3, FOOT2, 23, 20), "", "Reverse", style="ExExLargeIconButtonStyle"),
        button("Phase", (w - 28, FOOT2, 23, 20), "", "Invert phase", style="ExExLargeIconButtonStyle"),
    ])


def tuning():
    w = 102
    big = 58
    return section("TuningPanel", "TUNING", w, [
        N("Panel", None, (0, HEAD, w, H - HEAD), pin="r", overloadClass="LayerDrawPanel", style="InvisibleStyle", kids=[
            lab("CRSPanel", (0, 0, w, 100), pin="lrt", offset=0, style="LargeControlLabellerStyle", kids=[
                knob("CoarseTune", "Tune", (w - big) // 2, 8, True, size=big)]),
            lab(None, (0, 102, w, 54), pin="r", kids=[
                knob("Octave", "Octave", 8, 3, True), knob("FineTune", "Fine", w - K - 8, 3, True)]),
        ])])


def filt():
    w = 116
    big = 58
    return section("FilterPanel", "FILTER", w, [
        N("Panel", None, (0, HEAD, w, H - HEAD), pin="lrb", overloadClass="LayerDrawPanel", style="InvisibleStyle", kids=[
            lab("CutoffPanel", (2, 0, 64, 84), pin="t", offset=0, style="LargeControlLabellerStyle", kids=[
                knob("Cutoff", "Cutoff", 3, 8, size=big)]),
            lab(None, (w - K - 8, 0, K, 108), pin="r", kids=[
                knob("FilterDrive", "Drive", 0, 6), knob("Resonance", "Reso", 0, 6 + PITCH)]),
        ]),
        button("FilterActive", (2, FOOT1 - 22, 66, 20), "On", "Filter on/off"),
        N("PopupButton", "FilterAlgorithm", (2, FOOT1, w - 8, 20), pin="lr", displayName="Filter model", style="DefaultPopupButtonStyle"),
        N("PopupButton", "FilterType", (2, FOOT2, w - 8, 20), pin="lr", displayName="Filter type", style="DefaultPopupButtonStyle"),
    ])


def play():
    w = 64
    x = col(0, w - 2)
    return section("PositionPanel", "PLAY", w, [
        lab("PositionLabeller", (0, HEAD, w, H - HEAD), pin="lrtb", kids=[
            knob("PreDelayTime", "Delay", x, 6), knob("SampleStartPoint", "Start", x, 6 + PITCH, True),
            knob("SampleEndPoint", "End", x, 6 + 2 * PITCH, True)])])


def looping():
    w = 116
    a, b = 10, w - K - 12
    return section("LoopPanel", "LOOP", w, [
        lab("LoopLabeller", (0, HEAD, w, 104), pin="lr", kids=[
            knob("SampleLoopStartPoint", "Start", a, 6, True), knob("SampleLoopEndPoint", "End", b, 6, True),
            knob("XFadeLoopTime", "X-Fade", a, 6 + PITCH), knob("XFadeLoopCurve", "Curve", b, 6 + PITCH, True)]),
        button("LoopInRelease", (2, FOOT1, w - 8, 20), "Loop in Release", "Keep looping after note off"),
        button("AltLoopMode", (2, FOOT2, w - 8, 20), "Ping-Pong", "Loop back and forth"),
    ])


def stretch():
    w = 54
    return section("StretchPanel", "STRETCH", w, [
        lab("StretchLabeller", (0, HEAD, w, H - HEAD), pin="lrtb", kids=[knob("TimestretchAmount", "Amount", col(0, w - 4), 34, True)]),
        button("TimestretchActive", (2, HEAD + 6, w - 8, 20), "On", "Time stretch on/off", pin="lr"),
        button("TimestretchMode", (2, FOOT1, w - 8, 20), "Fast", "Constant CPU mode: faster for some pitch ranges", pin="lr"),
        button("TimestretchTracksBPM", (2, FOOT2, w - 8, 20), "Sync", "Follow the project tempo", pin="lr"),
    ])


def envelope(name, title, p):
    w = 152
    faders = [N("TransmodSlider", f"{p}{s}", (i * 20, 5, 16, 132), displayName=s[0], style="TransmodSliderStyle")
              for i, s in enumerate(["Attack", "Decay", "Hold", "Sustain", "Release"])]
    curves = [knob(f"{p}{s}Curve", f"{s[0]} Curve", 4, 6 + i * PITCH, True)
              for i, s in enumerate(["Attack", "Decay", "Release"])]
    return section(name, title, w, [
        lab(None, (6, HEAD, 98, H - HEAD), pin="b", offset=2, kids=faders),
        lab(None, (106, HEAD, 44, H - HEAD), pin="b", kids=curves),
    ])


def params():
    gap = 6
    secs = [setup(), mix(), tuning(), filt(), play(), looping(), stretch(),
            envelope("AEPanel", "AMP ENV", "AmpEnv"), envelope("FEPanel", "FREE ENV", "FreeEnv")]
    x = 0
    for s in secs:
        s.rect = (x, 0, s.w, s.h)
        x += s.w + gap
    return N("AutoStackBox", "LayerParams", (0, 0, x - gap, H), style="InvisibleStyle", optIsVertical=False, intIntraSpacing=gap,
             intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0, kids=secs)


def outputs():
    return {"Skin/Pad Editor/LayerParams.skin": skin(params())}
