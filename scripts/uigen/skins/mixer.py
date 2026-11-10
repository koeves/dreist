"""The mixer: the page frame and the channel strips (Mixer/*.skin).

Strips come in three heights (normal, Mid, Large; the editor picks one
from the space it has) and three kinds: pad/layer/engine channels, aux
returns and the master.  Every strip shares one shape: name on top, the
fader block in the middle, effect lights and the output menu at the foot.
"""

from . import N, skin

SIZES = {"": 180, "Mid": 400, "Large": 400}
WIDTH = {"MixerChannel": 88, "AuxChannel": 65, "MasterChannel": 70}
FOOT = 30


def fx_lights(w, h):
    n, gap = 6, 1
    cw = (w - 4 - gap * (n - 1)) // n
    return N("Matrix", "FXMatrix", (2, h - FOOT, w - 4, 8), pin="lrb", style="InvisibleStyle", intNumberOfCols=n,
             intIntraSpacing=gap, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
             kids=[N("Button", f"FxIndi{i}", (i * (cw + gap), 0, cw, 8), style="FXIndicatorStyle") for i in range(n)])


REL = dict(ARTop="Relative 0.5100", ARBottom="FNear 0.0000")   # the lower half of a Large strip
TB = dict(ARTop="FNear 0.0000", ARBottom="FNear 0.0000")
BELOW = lambda y: dict(ARTop=f"FNear {y:.4f}", ARBottom="FNear 0.0000")


def button(name, rect, text, tip, style, **kw):
    return N("Button", name, rect, displayName=tip, style=style, text=text, **kw)


def mute(rect, **kw):
    return button("MuteButton", rect, "M", "Mute", "MuteButtonStyle", **kw)


def solo(rect, **kw):
    return button("SoloButton", rect, "S", "Solo", "SoloButtonStyle", **kw)


def prepost(rect, **kw):
    return button("PrePostButton", rect, "Pre", "Sends before the fader", "DefaultButtonStyle", **kw)


def knob(name, cap, rect, centred=False, transmod=True, **kw):
    if transmod:
        return N("TransmodKnob", name, rect, displayName=cap, style="TransmodStyle", optCentered=centred or None,
                 id=100000 if centred else None, **kw)
    return N("Knob", name, rect, displayName=cap, style="KnobStyle", optCentered=centred or None, id=100000,
             realDialThickness=0.3, **kw)


def labeller(name, rect, offset, kids, **kw):
    return N("Labeller", name, rect, style="SmallControlLabellerStyle", enumTextPosition="Below", intTextOffset=offset, kids=kids, **kw)


def strip(kind, size):
    """One strip, laid out as the shipped Mixer/<kind><size>.skin (strips
    never change width, so the knobs keep fixed x rather than the shipped
    centre anchors, which only put them on half pixels; the Mid strip's
    31 px knobs are 32 px, centred a half pixel up and left, for the same
    reason)."""
    w, h = WIDTH[kind], SIZES[size]
    mh = h - 20 - FOOT - 2
    pad = kind == "MixerChannel"
    fader = dict(displayName="Gain", id=100012)
    if pad:
        fader.update(style="TransmodSliderStyle", realModDim=0.3)
    else:
        fader.update(style="SliderStyle", realTrackInset=0.35)
    cls = "TransmodSlider" if pad else "Slider"
    gain = lambda rect, **kw: N(cls, "GainSlider", rect, **fader, **kw)
    meter = lambda rect, st="DefaultVerticalVUMeterStyle", **kw: N("MultiChannelDBMeter", "VUMeter", rect, style=st, **kw)
    big = lambda x, r: meter((x, 0, w - x - r, 174), "BigVerticalVUMeterStyle", ARLeft=f"FNear {x:.4f}", ARRight=f"FNear {r:.4f}",
                             ARTop="FNear 0.0000", ARBottom="Relative 0.5000")
    group = lambda rect, kids, **kw: N("Panel", None, rect, style="InvisibleStyle", zorder=888, kids=kids, **kw)
    kids = []
    if kind == "MasterChannel":
        kids.append(N("Label", "NameLabel", (0, 2, w, 16), pin="lrt", id=100011, style="MixerChannelEditTitleStyle", text="Master"))
    else:
        kids.append(N("TextBox", "NameLabel", (0, 2, w, 16), pin="lrt", id=100011, style="MixerChannelEditTitleStyle",
                      placeholder="Aux X" if kind == "AuxChannel" else "Name", optSingleClickEdit=False, optSupportsDnD=False))
    if pad:
        mix = {
            "": [gain((5, 0, 20, mh), **TB), meter((29, 0, 18, mh), **TB),
                 labeller("PanPanel", (49, 24, 37, 88), -2, [knob("PanKnob", "Pan", (3, 0, 30, 30), True),
                                                            knob("Pitch", "Pitch", (3, 41, 30, 30), True)],
                          ARBottom="FNear 0.0000"),
                 group((49, 0, 37, 20), [mute((0, 0, 18, 18)), solo((19, 0, 18, 18))])],
            "Mid": [labeller("PanPanel", (0, 0, w, 40), -2, [knob("PanKnob", "Pan", (6, 0, 32, 32), True, pin="t"),
                                                            knob("Pitch", "Pitch", (48, 0, 32, 32), True, pin="t")], pin="lrt"),
                    gain((12, 42, 20, mh - 42), **BELOW(42)), meter((36, 42, 20, mh - 42), **BELOW(42)),
                    group((61, 42, 18, 98), [mute((0, 0, 18, 18)), solo((0, 20, 18, 18))])],
            "Large": [big(3, 5), gain((15, 177, 22, mh - 177), **REL),
                      labeller("PanPanel", (43, 177, 40, 150), -2, [knob("PanKnob", "Pan", (3, 47, 34, 34), True),
                                                                   knob("Pitch", "Pitch", (3, 94, 34, 34), True)],
                               ARLeft="FFar 45.0000", ARRight="FNear 5.0000", ARTop="Relative 0.5100"),
                      group((43, 177, 40, 42), [mute((0, 0, 18, 18)), solo((22, 0, 18, 18), pin="r")],
                            ARRight="FNear 5.0000", ARTop="Relative 0.5100")],
        }[size]
        sends = {"": [(7, 5, 30), (51, 5, 30), (7, 54, 30), (51, 54, 30)],
                 "Mid": [(27, 5 + 42 * i, 32) for i in range(4)],
                 "Large": [(24, 10 + 60 * i, 41) for i in range(4)]}[size]
        kids.append(labeller("SendPanel", (0, 20, w, mh), {"": 0, "Mid": -3, "Large": 0}[size], [
            N("TransmodKnob", f"SendKnob{i}", (x, y, d, d), displayName=str(i + 1), style="TransmodStyle",
              ) for i, (x, y, d) in enumerate(sends)], pin="lrtb"))
    elif kind == "AuxChannel":
        mix = {
            "": [gain((5, 0, 15, mh), **TB), meter((22, 0, 16, mh), **TB), mute((42, 0, 18, 18)), solo((42, 20, 18, 18)),
                 prepost((42, 40, 18, 18))],
            "Mid": [prepost((2, 6, w - 4, 18), pin="lr"), gain((5, 42, 15, mh - 42), **BELOW(42)), meter((23, 42, 16, mh - 42), **BELOW(42)),
                    mute((43, 42, 18, 18)), solo((43, 62, 18, 18))],
            "Large": [big(3, 5), gain((6, 177, 15, mh - 177), **REL), mute((22, 177, 18, 18), ARTop="Relative 0.5100"),
                      solo((42, 177, 18, 18), ARTop="Relative 0.5100"), prepost((22, 198, 38, 18), ARTop="Relative 0.5700")],
        }[size]
    else:
        pitch = lambda rect, **kw: knob("Pitch", "Pitch", rect, True, transmod=False, **kw)
        mix = {
            "": [gain((4, 0, 15, mh), **TB), meter((22, 0, 16, mh), **TB), labeller("PitchPanel", (40, 0, 30, 50), 0, [pitch((2, 0, 25, 25))])],
            "Mid": [labeller("PitchPanel", (0, 0, w, 42), 0, [pitch((22, 2, 27, 27))], pin="lr"),
                    gain((5, 42, 15, mh - 42), **BELOW(42)), meter((23, 42, 16, mh - 42), **BELOW(42))],
            "Large": [big(3, 5), gain((10, 177, 15, mh - 177), **REL),
                      labeller("PitchPanel", (32, 177, 30, 150), 0, [pitch((2, 0, 25, 25))], ARTop="Relative 0.5100")],
        }[size]
    kids.append(N("Panel", "MixPanel" if kind != "MasterChannel" else None, (0, 20, w, mh), pin="lrtb", style="InvisibleStyle", kids=mix))
    kids.append(fx_lights(w, h))
    if kind != "MasterChannel":
        kids.append(N("PopupButton", "OutputCombo", (2, h - 20, w - 4, 18), pin="lrb", id=100010, style="ShorteningPopupButtonStyle"))
    return N("Panel", "CtrlPanel", (0, 0, w, h), pin="tb" if kind == "MasterChannel" else "", style="InvisibleStyle", kids=kids)


def page():
    """The mixer page: the effect chain on top, the mode switches and the
    strips below."""
    W, H = 820, 395
    modes = N("ButtonGroup", "ModeGroup", (4, 7, 45, 64), pin="t", style="InvisibleStyle", intLeftSpacing=0,
              intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
              kids=[N("Button", None, (0, i * 22, 45, 20), style="DefaultButtonStyle", text=t)
                    for i, t in enumerate(["Mix", "Sends", "Effects"])])
    lower = N("Panel", None, (0, 201, W, 194), pin="lrtb", style="InvisibleStyle", kids=[
        N("ScrollContainer", "ChannelScroller", (52, 0, W - 54, 192), pin="lrtb", style="InvisibleStyle", HScrollBarStyle="",
          ScrollViewStyle="InvisibleStyle", VScrollBarStyle="", intScrollBarDim=10, optAutoHide=True, optOverlay=False,
          optShowHBar=False, optShowVBar=False),
        modes,
        N("Labeller", None, (4, 77, 45, 40), style="SmallDarkControlLabellerStyle", enumTextPosition="Below", kids=[
            N("PopupButton", "EffectViewGroup", (0, 0, 45, 20), displayName="Show FX", style="ShorteningPopupButtonStyle")]),
    ])
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="TopRightPanelStyle", kids=[
        lower,
        N("Panel", "EffectPanel", (0, 0, W, 200), pin="lrt", overloadClass="EffectChainPanel", style="BasicPanelStyle", zorder=600),
    ])


def outputs():
    files = {"Skin/Mixer/Mixer.skin": skin(page())}
    for kind in WIDTH:
        for size in SIZES:
            files[f"Skin/Mixer/{kind}{size}.skin"] = skin(strip(kind, size))
    return files
