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


def mute_solo(x, y, stacked=False, gap=2, w=None):
    m = N("Button", "MuteButton", (0, 0, 18, 18), displayName="Mute", style="MuteButtonStyle", text="M")
    s = N("Button", "SoloButton", (0, 18 + gap, 18, 18) if stacked else (18 + gap, 0, 18, 18), displayName="Solo",
          style="SoloButtonStyle", text="S")
    size = (18, 36 + gap) if stacked else (w or 36 + gap, 20)
    return N("Panel", None, (x, y, *size), style="InvisibleStyle", zorder=888, kids=[m, s])


def knob(name, cap, x, y, size, centred=False, transmod=True):
    if transmod:
        return N("TransmodKnob", name, (x, y, size, size), displayName=cap, style="TransmodStyle",
                 optCentered=centred or None, id=100000 if centred else None)
    return N("Knob", name, (x, y, size, size), displayName=cap, style="KnobStyle", optCentered=centred or None,
             id=100000, realDialThickness=0.3)


def strip(kind, size):
    w, h = WIDTH[kind], SIZES[size]
    mh = h - 20 - FOOT - 2
    tall = size != ""
    kids = []
    if kind == "MasterChannel":
        kids.append(N("Label", "NameLabel", (0, 2, w, 16), pin="lrt", id=100011, style="MixerChannelEditTitleStyle", text="Master"))
    else:
        kids.append(N("TextBox", "NameLabel", (0, 2, w, 16), pin="lrt", id=100011, style="MixerChannelEditTitleStyle",
                      placeholder="Aux" if kind == "AuxChannel" else "Name", optSingleClickEdit=False, optSupportsDnD=False))
    mix = []
    pad = kind == "MixerChannel"
    fader = dict(displayName="Gain", id=100012)
    if pad:
        fader.update(style="TransmodSliderStyle", realModDim=0.3)
    else:
        fader.update(style="SliderStyle", realTrackInset=0.35)
    cls = "TransmodSlider" if pad else "Slider"
    if size == "Large":
        # A wide meter over the top half, the fader and knobs below it.
        top = mh // 2
        mix.append(N("MultiChannelDBMeter", "VUMeter", (3, 0, w - 6, top - 4), pin="lrt", ARBottom="Relative 0.4900",
                     style="BigVerticalVUMeterStyle"))
        mix.append(N(cls, "GainSlider", (6, top, 20, mh - top), pin="b", ARTop="Relative 0.5100", **fader))
        rest = N("Labeller", "PanPanel" if kind != "AuxChannel" else None, (30, top, w - 32, mh - top), pin="lr",
                 ARTop="Relative 0.5100", style="SmallControlLabellerStyle", enumTextPosition="Below", intTextOffset=-1)
        ks = 30 if pad else 26
        y = 24
        if kind != "AuxChannel":
            if pad:
                rest.add(knob("PanKnob", "Pan", (rest.w - ks) // 2, y, ks, True))
                y += ks + 16
            rest.add(knob("Pitch", "Pitch", (rest.w - ks) // 2, y, ks, True, transmod=pad))
            mix.append(rest)
        if kind != "MasterChannel":
            # Beside the fader's top, moving down with it as the strip
            # grows (they stayed put over the meter), and inside the narrow
            # aux strip (its Solo button stuck out at x 32).
            ms = mute_solo(min(32, w - 39), top)
            ms.attrs["ARTop"] = "Relative 0.5100"
            mix.append(ms)
            if kind == "AuxChannel":
                mix.append(N("Button", "PrePostButton", (32, top + 22, w - 34, 18), displayName="Sends before the fader",
                             style="DefaultButtonStyle", text="Pre", ARTop=f"Relative {(top + 22 + 3) / mh:.4f}"))
    else:
        y0 = 0
        if tall and kind != "AuxChannel":
            # Knobs across the top, then a full-height fader and meter.
            lab = N("Labeller", "PanPanel" if pad else "PitchPanel", (0, 0, w, 44), pin="lr", style="SmallControlLabellerStyle",
                    enumTextPosition="Below", intTextOffset=-1)
            if pad:
                lab.add(knob("PanKnob", "Pan", 6, 0, 34, True), knob("Pitch", "Pitch", w - 40, 0, 34, True))
            else:
                lab.add(knob("Pitch", "Pitch", (w - 28) // 2, 1, 28, True, transmod=False))
            mix.append(lab)
            y0 = 46
        if tall and kind == "AuxChannel":
            mix.append(N("Button", "PrePostButton", (3, 6, w - 6, 18), pin="lr", displayName="Sends before the fader",
                         style="DefaultButtonStyle", text="Pre"))
            y0 = 30
        if not tall:
            # The compact strips: fader, meter, then the buttons and knobs.
            if pad:
                mix.append(N(cls, "GainSlider", (5, 0, 20, mh), pin="tb", **fader))
                mix.append(N("MultiChannelDBMeter", "VUMeter", (29, 0, 18, mh), pin="tb", style="DefaultVerticalVUMeterStyle"))
                mix.append(mute_solo(49, 0, gap=1, w=37))
                mix.append(N("Labeller", "PanPanel", (49, 24, w - 51, 88), pin="b", style="SmallControlLabellerStyle",
                             enumTextPosition="Below", intTextOffset=-2,
                             kids=[knob("PanKnob", "Pan", 3, 0, 30, True), knob("Pitch", "Pitch", 3, 41, 30, True)]))
            elif kind == "AuxChannel":
                mix.append(N(cls, "GainSlider", (5, 0, 15, mh), pin="tb", **fader))
                mix.append(N("MultiChannelDBMeter", "VUMeter", (22, 0, 16, mh), pin="tb", style="DefaultVerticalVUMeterStyle"))
                mix.append(mute_solo(42, 0, stacked=True))
                mix.append(N("Button", "PrePostButton", (42, 40, 18, 18), displayName="Sends before the fader",
                             style="DefaultButtonStyle", text="Pre"))
            else:
                mix.append(N(cls, "GainSlider", (4, 0, 15, mh), pin="tb", **fader))
                mix.append(N("MultiChannelDBMeter", "VUMeter", (22, 0, 16, mh), pin="tb", style="DefaultVerticalVUMeterStyle"))
                mix.append(N("Labeller", "PitchPanel", (40, 0, 30, 50), style="SmallControlLabellerStyle",
                             enumTextPosition="Below", intTextOffset=0,
                             kids=[knob("Pitch", "Pitch", 2, 0, 25, True, transmod=False)]))
        else:
            fw = 20 if pad else 16
            mix.append(N(cls, "GainSlider", (4, y0, fw, mh - y0), pin="tb", **fader))
            mix.append(N("MultiChannelDBMeter", "VUMeter", (6 + fw, y0, 16, mh - y0), pin="tb", style="DefaultVerticalVUMeterStyle"))
            if kind != "MasterChannel":
                mix.append(mute_solo(6 + fw + 18, y0, stacked=True))
    mix_panel = N("Panel", "MixPanel" if kind != "MasterChannel" else None, (0, 20, w, mh), pin="lrtb", style="InvisibleStyle", kids=mix)
    if pad:
        ks = 30 if size == "" else 34
        if size == "":
            pos = [(7, 5), (w - 37, 5), (7, 54), (w - 37, 54)]
        else:
            step = 60 if size == "Large" else 46
            pos = [((w - ks) // 2, 8 + i * step) for i in range(4)]
        sends = N("Labeller", "SendPanel", (0, 20, w, mh), pin="lrtb", style="SmallControlLabellerStyle",
                  enumTextPosition="Below", intTextOffset=0,
                  kids=[N("TransmodKnob", f"SendKnob{i}", (x, y, ks, ks), pin="c" if size else "", displayName=str(i + 1),
                          style="TransmodStyle") for i, (x, y) in enumerate(pos)])
        kids.append(sends)
    kids.append(mix_panel)
    kids.append(fx_lights(w, h))
    if kind != "MasterChannel":
        kids.append(N("PopupButton", "OutputCombo", (2, h - 20, w - 4, 18), pin="lrb", id=100010, style="ShorteningPopupButtonStyle"))
    return N("Panel", "CtrlPanel", (0, 0, w, h), pin="tb" if kind == "MasterChannel" else "", style="InvisibleStyle", kids=kids)


def page():
    """The mixer page: the effect chain on top, the mode switches and the
    strips below."""
    W, H = 820, 395
    modes = N("ButtonGroup", "ModeGroup", (4, 6, 46, 64), pin="t", style="InvisibleStyle", intLeftSpacing=0,
              intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
              kids=[N("Button", None, (0, i * 22, 46, 20), style="DefaultButtonStyle", text=t)
                    for i, t in enumerate(["Mix", "Sends", "Effects"])])
    lower = N("Panel", None, (0, 201, W, 194), pin="lrtb", style="InvisibleStyle", kids=[
        N("ScrollContainer", "ChannelScroller", (54, 0, W - 56, 192), pin="lrtb", style="InvisibleStyle", HScrollBarStyle="",
          ScrollViewStyle="InvisibleStyle", VScrollBarStyle="", intScrollBarDim=10, optAutoHide=True, optOverlay=False,
          optShowHBar=False, optShowVBar=False),
        modes,
        N("Labeller", None, (4, 78, 46, 40), style="SmallDarkControlLabellerStyle", enumTextPosition="Below", kids=[
            N("PopupButton", "EffectViewGroup", (0, 0, 46, 20), displayName="Effects of", style="ShorteningPopupButtonStyle")]),
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
