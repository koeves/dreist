"""The pads and the pad editor (Pad Editor/): pad grid, one pad, the pad
inspector with its layer list, the layer wave view and the sample
metadata dialog.  LayerParams and VelocitySplitPanel live in layer.py."""

from . import N, skin
from .pages import btn


def pads_panel():
    W, H = 400, 400
    bank = N("ButtonGroup", "PadBank", (88, 2, 90, 20), intIntraSpacing=1, optIsVertical=False, intLeftSpacing=0,
             intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0, style="InvisibleStyle",
             kids=[N("Button", None, (i * 18, 0, 17, 20), style="TransmodButtonStyle", text=t)
                   for i, t in enumerate(["A", "B", "C", "D", "All"])])
    bar = N("Panel", "PadControl", (0, 0, W, 24), pin="lrt", style="InvisibleStyle", kids=[
        N("PopupButton", "PadMode", (2, 2, 83, 20), displayName="Pad mode", style="HeaderBarPopupButtonStyle"),
        bank,
        N("Button", "EraseButton", (192, 2, 20, 20), displayName="Erase: hold a pad to clear its steps", id=100002,
          style="HeaderBarIconButtonStyle", text=""),
        N("Button", "RepeatButton", (224, 2, 40, 20), displayName="Note repeat", id=100001, style="TransmodButtonStyle", text="Repeat"),
        btn("RepeatCount", (266, 2, 30, 20), "1/16", "Note repeat rate", style="TransmodButtonStyle", id=100000),
        N("Button", "FullLevelButton", (307, 2, 30, 20), displayName="Fixed velocity", id=100000, style="TransmodButtonStyle", text="Full"),
        N("Knob", "FullLevelKnob", (341, 2, 20, 20), displayName="Fixed velocity", id=100001, style="AltKnobStyle", realDialThickness=0.3),
        btn("Options", (W - 22, 2, 20, 20), "", "More pad options", style="HeaderBarIconButtonStyle", pin="r"),
    ])
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="InvisibleStyle", kids=[
        bar,
        N("SplitterPanel", "Splitter", (0, 26, W, H - 26), pin="lrtb", style="InvisibleStyle", SplitterPanelStyle="InvisibleStyle",
          intSplitPosition=0, intSplitterDim=1, intMaxSize0=80, optDbClkCollapse1=False, kids=[
              N("Matrix", "PadsMatrix", (0, 1, W, H - 27), pin="b", displayName="SplitterPanel1", intNumberOfCols=4, intNumberOfRows=4,
                intIntraSpacing=4, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
                optLayoutFromTop=False, style="InvisibleStyle")]),
    ])


def pad():
    W, H = 75, 45
    leds = N("Panel", None, ((W - 63) // 2, H - 10, 63, 8), pin="cb",
             style="InvisibleStyle", kids=[N("Button", f"LI{i}", (i * 8, 0, 7, 7), style="PadLayerIndicatorStyle") for i in range(8)])
    return N("Panel", None, (0, 0, W, H), style="PadStyle", kids=[
        N("Panel", "Overlay", (2, 2, W - 4, H - 4), pin="lrtb", style="PadOverlayStyle"),
        N("Label", "StepLabel", (3, 3, W - 6, 10), pin="lrt"),
        N("Button", "MuteIndi", (3, 3, 10, 5), pin="lt", style="EngineSelectorMuteIndicatorStyle"),
        N("Button", "SoloIndi", (15, 3, 10, 5), pin="lt", style="EngineSelectorSoloIndicatorStyle"),
        N("Button", "ColourIndi", (27, 3, W - 42, 5), ARRight="FNear 15.0000", style="InvisibleStyle"),
        N("Label", "NameLabel", (0, 10, W, 22), pin="lr", ARTop="Relative 0.2200", ARBottom="Relative 0.7200"),
        leds,
        N("Button", "LockIndi", (W - 13, 3, 10, 10), pin="r", style="PadLockIndicatorStyle", text="", zorder=50),
    ])


def pad_button():
    """The selected pad's header in the inspector."""
    W, H = 120, 58
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lr", style="InvisibleStyle", kids=[
        N("TextBox", "PadName", (2, 0, W - 4, 16), pin="lrt", id=100020, optSingleClickEdit=False, placeholder="Pad",
          style="LightTextInvisibleEditBoxStyle"),
        N("MultiChannelDBMeter", "VUMeter", (2, 18, W - 4, 14), pin="lr", style="DefaultLighterHorizontalVUMeterStyle"),
        N("Button", "Mute", (2, 37, 18, 18), displayName="Mute", style="MuteButtonStyle", text="M"),
        N("Button", "Solo", (22, 37, 18, 18), displayName="Solo", style="SoloButtonStyle", text="S"),
        N("Button", "AllPads", (44, 37, 36, 18), displayName="Edits apply to every pad", style="DefaultButtonStyle", text="Pad"),
        N("Button", "AllLayers", (82, 37, 36, 18), displayName="Edits apply to every layer", style="DefaultButtonStyle", text="Layer"),
    ])


def layer_button():
    W, H = 120, 32
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lt", style="InvisibleStyle", kids=[
        N("TextBox", "SampleName", (2, 0, W - 6, 16), pin="lrt", id=100020, optSingleClickEdit=False, placeholder="Empty Layer",
          style="DarkTextInvisibleEditBoxStyle"),
        N("Button", "Mute", (2, 17, 18, 14), displayName="Mute", style="MuteButtonStyle", text="M"),
        N("Button", "Solo", (22, 17, 18, 14), displayName="Solo", style="SoloButtonStyle", text="S"),
        N("MultiChannelDBMeter", "VUMeter", (42, 17, W - 46, 14), pin="lrt", style="DefaultHorizontalVUMeterStyle"),
    ])


def inspector():
    W, H = 800, 350
    LW = 120
    side = N("Panel", None, (0, 0, LW, H), pin="ltb", style="BackPanelStyle", kids=[
        N("Panel", None, (0, -5, LW, 60), pin="t", style="InvisibleStyle", kids=[
            N("Panel", "PadSelButton", (0, 0, LW, 60), pin="lr", overloadClass="PadSelectionButton")]),
        N("Button", "ShowSplits", (0, 57, LW, 22), pin="lrt", displayName="Velocity splits and pad options",
          style="VSplitButtonStyle", text="Pad options ▶"),
        N("TableView", "LayerTable", (0, 79, LW, H - 79), pin="lrtb", style="InvisibleStyle", HScrollBarStyle="", VScrollBarStyle="",
          ScrollViewStyle="InvisibleStyle", TableHeaderPanelStyle="InvisibleStyle", TablePanelStyle="InspectorTableStyle",
          intHeaderHeight=0, intScrollBarDim=10),
    ])
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="BackPanelStyle", kids=[
        side,
        N("Panel", "LayerPanel", (LW, 0, W - LW, H), pin="lrtb", overloadClass="LayerPanel", style="LayerPanelStyle"),
        N("Panel", "VelocitySplitPanel", (LW, 0, W - LW, H), pin="lrtb", overloadClass="VelocitySplitPanel", style="InvisibleStyle"),
    ])


def layer_panel():
    W, H = 800, 390
    WH = 196
    bw = W - 10
    zoom = N("ButtonGroup", "AutoZoomGroup", (bw - 104, WH - 21, 66, 20), pin="rb", optChildPositionsAreLocked=True,
             optIsVertical=False, intIntraSpacing=0, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
             kids=[N("Button", None, (i * 17, 0, 15, 19), displayName=tip, style="WaveDisplayZoomIconButtonStyle", text=g)
                   for i, (g, tip) in enumerate([("", "Zoom: free"), ("", "Zoom: follow start and end"),
                                                 ("", "Zoom: follow start"), ("", "Zoom: follow end")])])
    wave = N("Panel", "WaveDisplayPanel", (5, 5, bw, WH), pin="lrtb", style="WavePanelBackingStyle", kids=[
        N("Panel", "WaveDisplay", (2, 2, bw - 4, WH - 25), pin="lrtb", overloadClass="LayerWaveDisplay", style="InvisibleStyle"),
        N("Panel", "WaveZoomSlider", (2, WH - 21, bw - 146, 20), pin="lrb", displayName="WaveZoomSlider",
          overloadClass="WaveDisplayZoomSlider", style="WaveDisplayZoomSliderStyle"),
        N("Button", "ShowAmpEnvButton", (bw - 140, WH - 21, 15, 20), pin="rb", displayName="Draw the amp envelope on the wave",
          style="WaveDisplayZoomButtonStyle", text="A"),
        N("Button", "ShowFreeEnvButton", (bw - 124, WH - 21, 15, 20), pin="rb", displayName="Draw the free envelope on the wave",
          style="WaveDisplayZoomButtonStyle", text="F"),
        zoom,
        btn("ZoomOutButton", (bw - 34, WH - 21, 15, 20), "", "Zoom out", style="WaveDisplayZoomIconButtonStyle", pin="rb"),
        btn("ZoomInButton", (bw - 18, WH - 21, 15, 20), "", "Zoom in", style="WaveDisplayZoomIconButtonStyle", pin="rb"),
    ])
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="BasicPanelStyle", kids=[
        wave,
        N("ScrollContainer", "ParamScroller", (5, WH + 7, bw, H - WH - 7), pin="lrb", style="InvisibleStyle",
          HScrollBarStyle="ScrollbarStyle", VScrollBarStyle="ScrollbarStyle", ScrollViewStyle="InvisibleStyle", intScrollBarDim=10,
          optAutoHide=False, optOverlay=False, optShowHBar=True, optShowVBar=False),
    ])


def metadata_dialog():
    W, H = 300, 275
    IW = 270
    box = lambda n, r, cap, pin="lt", cls="TextBox", st="DefaultEditBoxStyle": N(cls, n, r, pin=pin, displayName=cap, style=st)
    inner = N("Labeller", None, (0, 0, IW, H - 10), pin="lrtb", enumTextPosition="Below", intTextOffset=4,
              style="DialogPanelLeftLabellerStyle", kids=[
                  box("BPMBox", (10, 10, 54, 20), "BPM"), box("BarsBox", (84, 10, 54, 20), "Bars"),
                  box("BeatsBox", (158, 10, 54, 20), "Beats"),
                  box("Root", (10, 60, 80, 20), "Root Hz"),
                  box("RootNote", (100, 60, 80, 20), "Root note", cls="PopupButton", st="DefaultPopupButtonStyle"),
                  box("Author", (10, 120, IW - 20, 20), "Author", pin="lrt"),
                  box("Description", (10, 170, IW - 20, 20), "Description", pin="lrt"),
                  btn("GuessButton", (10, H - 40, 54, 20), "Detect", None, pin="lb"),
                  btn("CancelButton", (IW - 124, H - 40, 54, 20), "Cancel", None, pin="rb"),
                  btn("SaveButton", (IW - 64, H - 40, 54, 20), "Save", None, pin="rb"),
              ])
    return N("AnchorPanel", None, (0, 0, W, H), enumAnchorEdge="ARLeft", intAnchorPoint=20, style="TriggerDialogPanelStyle", kids=[
        N("Labeller", None, (25, 5, IW, H - 10), pin="lrtb", displayName="None", enumTextPosition="Above",
          style="DialogPanelLeftLabellerStyle", kids=[inner])])


def outputs():
    d = "Skin/Pad Editor/"
    return {
        d + "PadsPanel.skin": skin(pads_panel()),
        d + "Pad.skin": skin(pad()),
        d + "PadSelectionButton.skin": skin(pad_button()),
        d + "LayerSelectionButton.skin": skin(layer_button()),
        d + "PadInspector.skin": skin(inspector()),
        d + "LayerPanel.skin": skin(layer_panel()),
        d + "MetaDataAnchor.skin": skin(metadata_dialog()),
        d + "VelocitySplitPanel.skin": skin(velocity_splits()),
    }


def velocity_splits():
    """Pad options: layer play mode, velocity-to-amp, auto split, the 64
    pad link switches, and the velocity split rows (built by the editor)."""
    W, H = 800, 350
    IW = W - 10
    cols, bw, gap = 32, 14, 2
    links = N("Matrix", "LinkMatrix", (IW - cols * (bw + gap) + gap, 2, cols * (bw + gap) - gap, 38), pin="r",
              displayName="Linked pads", intNumberOfCols=cols, intNumberOfRows=2, intLeftSpacing=0, intRightSpacing=0,
              intTopSpacing=0, intBottomSpacing=0, style="InvisibleStyle",
              kids=[N("Button", f"LinkButton{i + 1}", ((i % cols) * (bw + gap), (i // cols) * 20, bw, 18),
                      displayName=f"Link to pad {i + 1}", style="DefaultSmallButtonStyle", text=str(i + 1)) for i in range(64)])
    top = N("Labeller", None, (5, 5, IW, 56), pin="lr", enumTextPosition="Below", intTextOffset=1, style="SmallControlLabellerStyle", kids=[
        N("PopupButton", "SelModeCombo", (0, 10, 128, 20), pin="l", displayName="Layer play mode", style="DefaultPopupButtonStyle"),
        btn("Insert", (136, 10, 54, 20), "Auto", "Auto V Split", style="DefaultPopupButtonStyle"),
        N("Knob", "v2a", (204, 6, 26, 26), displayName="V-to-A", style="KnobStyle", realDialThickness=0.3),
        links,
    ])
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="LayerPanelStyle", kids=[
        top,
        N("LayoutBox", "LayoutBox", (5, 76, IW, H - 76), pin="lrb", intIntraSpacing=1, intLeftSpacing=0, intRightSpacing=0,
          intTopSpacing=1, intBottomSpacing=0, style="InvisibleStyle"),
    ])
