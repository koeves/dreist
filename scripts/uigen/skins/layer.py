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


def setup():
    w = 96
    return section("ModesPanel", "SETUP", w, [
        lab("SetupLabeller", (0, HEAD, w, H - HEAD), pin="lrtb", offset=1, kids=[
            N("PopupButton", "PlayMode", (0, 6, w - 5, 20), pin="lr", displayName="Playback", style="ShorteningPopupButtonStyle"),
            N("PopupButton", "Choke", (0, 47, w - 5, 20), pin="lr", displayName="Choke", style="ShorteningPopupButtonStyle"),
            button("EnvMode", (0, 88, w - 5, 20), "Track Pitch", "Env Mode"),
            *[button(n, (5 + i * 22, 130, 20, 20), t, tip) for i, (n, t, tip) in enumerate([
                ("PS", "SP", "Set the sample start here"), ("PE", "EP", "Set the sample end here"),
                ("LS", "LS", "Set the loop start here"), ("LE", "LE", "Set the loop end here")])],
        ])])


def mix():
    w = 55
    return section("MixPanel", "MIX", w, [
        lab("MixLabeller", (0, HEAD, w, H - HEAD), pin="lrtb", kids=[
            knob("VoiceGain", "Gain", 7, 6), knob("VoicePan", "Pan", 7, 6 + PITCH + 1, True)]),
        button("LayerMode", (3, FOOT1, w - 9, 20), "Vintage", "Vintage playback"),
        button("Reverse", (3, FOOT2, 22, 20), "", "Reverse", style="ExExLargeIconButtonStyle"),
        button("Phase", (w - 28, FOOT2, 22, 20), "", "Invert phase", style="ExExLargeIconButtonStyle"),
    ])


def tuning():
    w = 100
    big = 60
    return section("TuningPanel", "TUNING", w, [
        N("Panel", None, (0, HEAD, w, H - HEAD), pin="r", overloadClass="LayerDrawPanel", style="InvisibleStyle", kids=[
            lab("CRSPanel", (0, 0, w, 100), pin="lrt", offset=0, style="LargeControlLabellerStyle", kids=[
                knob("CoarseTune", "Tune", (w - big) // 2, 6, True, size=big)]),
            lab(None, (0, 102, w, 54), pin="r", kids=[
                knob("Octave", "Octave", 6, 3, True), knob("FineTune", "Fine", w - K - 6, 3, True)]),
        ])])


def filt():
    w = 115
    big = 60
    return section("FilterPanel", "FILTER", w, [
        N("Panel", None, (0, HEAD, w, H - HEAD), pin="lrb", overloadClass="LayerDrawPanel", style="InvisibleStyle", kids=[
            lab("CutoffPanel", (0, 0, big, 80), pin="t", offset=0, style="LargeControlLabellerStyle", kids=[
                knob("Cutoff", "Cutoff", 0, 6, size=big)]),
            lab(None, (w - K - 6, 0, K, 108), pin="r", kids=[
                knob("FilterDrive", "Drive", 0, 6), knob("Resonance", "Res", 0, 6 + PITCH + 1)]),
        ]),
        button("FilterActive", (0, FOOT1 - 22, 70, 20), "Active", "Filter on/off"),
        N("PopupButton", "FilterAlgorithm", (0, FOOT1, w - 6, 20), pin="lr", displayName="Algorithm", style="DefaultPopupButtonStyle"),
        N("PopupButton", "FilterType", (0, FOOT2, w - 6, 20), pin="lr", displayName="Type", style="DefaultPopupButtonStyle"),
    ])


def play():
    w = 60
    x = 11
    return section("PositionPanel", "PLAY", w, [
        lab("PositionLabeller", (0, HEAD, w, H - HEAD), pin="lrtb", kids=[
            knob("PreDelayTime", "Pre delay", x, 6), knob("SampleStartPoint", "Start Offset", x, 6 + PITCH + 1, True),
            knob("SampleEndPoint", "End Offset", x, 6 + 2 * PITCH + 1, True)])])


def looping():
    w = 115
    a, b = 8, w - K - 13
    return section("LoopPanel", "LOOPING", w, [
        lab("LoopLabeller", (0, HEAD, w, 105), pin="lr", kids=[
            knob("SampleLoopStartPoint", "Start Offset", a, 6, True), knob("SampleLoopEndPoint", "End Offset", b, 6, True),
            knob("XFadeLoopTime", "X-Fade", a, 6 + PITCH + 1), knob("XFadeLoopCurve", "Curve", b, 6 + PITCH + 1, True)]),
        button("LoopInRelease", (0, FOOT1, w - 6, 20), "Release", "Keep looping in the release stage"),
        button("AltLoopMode", (0, FOOT2, w - 6, 20), "Alternate", "Loop back and forth"),
    ])


def stretch():
    w = 50
    return section("StretchPanel", "TS", w, [
        lab("StretchLabeller", (0, HEAD, w, H - HEAD), pin="lrtb", kids=[knob("TimestretchAmount", "Amount", 4, 38, True)]),
        button("TimestretchActive", (0, HEAD + 6, w - 6, 20), "Active", "Time stretch on/off", pin="lr"),
        button("TimestretchMode", (0, FOOT1, w - 6, 20), "Fast", "Constant CPU mode: faster for some pitch ranges", pin="lr"),
        button("TimestretchTracksBPM", (0, FOOT2, w - 6, 20), "Track", "Follow the project tempo", pin="lr"),
    ])


def envelope(name, title, p):
    w = 150
    faders = [N("TransmodSlider", f"{p}{s}", (i * 20, 5, 16, 132), displayName=s[0], style="TransmodSliderStyle")
              for i, s in enumerate(["Attack", "Decay", "Hold", "Sustain", "Release"])]
    curves = [knob(f"{p}{s}Curve", f"{s[0]}-C", 4, 6 + i * PITCH + min(i, 1), True)
              for i, s in enumerate(["Attack", "Decay", "Release"])]
    return section(name, title, w, [
        lab(None, (5, HEAD, 100, H - HEAD), pin="b", offset=2, kids=faders),
        lab(None, (105, HEAD, 45, H - HEAD), pin="b", kids=curves),
    ])


def params():
    gap = 6
    secs = [setup(), mix(), tuning(), filt(), play(), looping(), stretch(),
            envelope("AEPanel", "AMP ENVELOPE", "AmpEnv"), envelope("FEPanel", "FREE ENVELOPE", "FreeEnv")]
    x = 0
    for s in secs:
        s.rect = (x, 0, s.w, s.h)
        x += s.w + gap
    return N("AutoStackBox", "LayerParams", (0, 0, x - gap, H), style="InvisibleStyle", optIsVertical=False, intIntraSpacing=gap,
             intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0, kids=secs)


def outputs():
    return {"Skin/Pad Editor/LayerParams.skin": skin(params())}
