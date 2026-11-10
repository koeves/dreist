"""The pattern page: frame, toolbar, editor, track rows, graph lanes,
pattern selector keys and the step-count convertor (Patterns/)."""

from . import N, skin
from .pages import btn

SMALL_KNOB = dict(style="KnobStyle", realDialThickness=0.3)


def selectors():
    """24 pattern keys laid out as two octaves of a keyboard: naturals on
    the lower row, sharps above them."""
    W, H = 224, 46
    kw, gap = 14, 2
    naturals = [k for k in range(24) if k % 12 in (0, 2, 4, 5, 7, 9, 11)]
    sharps = [k for k in range(24) if k not in naturals]
    ids = [100003, 100004, 100005, 100006, 100007, 100008, 100009, 100010, 100011, 100012, 100000, 100001]
    kids = []
    for i, k in enumerate(naturals):
        kids.append((k, (i * (kw + gap), 24)))
    for k in sharps:
        below = naturals.index(k - 1)
        kids.append((k, (below * (kw + gap) + (kw + gap) // 2, 2)))
    kids.sort(key=lambda t: (t[1][1], t[1][0]))
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="InvisibleStyle", kids=[
        N("Button", f"Key{k}", (x, y, kw, 20), id=ids[k % 12], overloadClass="PatternSelector", style="DefaultIconButtonStyle")
        for k, (x, y) in kids])


def page():
    W, H = 900, 500
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="InvisibleStyle", kids=[
        N("Panel", "ToolBar", (0, 0, W, 46), pin="lrt", overloadClass="PatternEditorToolBar", style="BasicPanelStyle"),
        N("Panel", "PatternEditor", (0, 46, W, H - 46), pin="lrtb", overloadClass="PatternEditor", style="InvisibleStyle"),
    ])


def toolbar():
    W, H = 1400, 46
    SEL = 224
    sub = lambda cap, x, w, kids: N("Panel", None, (x, 0, w, 20), displayName=cap, style="InvisibleStyle", kids=kids)
    steps = sub("Steps", 0, 54, [
        N("ValueBox", "LengthBox", (0, 0, 38, 20), displayName="Steps", id=100002, placeholder="16", optCanBeDragged=False,
          realIncDecRange=1, realMinValue=1, realMaxValue=1024, style="DefaultEditBoxStyle"),
        btn("PlusButton", (36, 0, 17, 10), "", "More steps", style="SmallIconButtonStyle", id=100001),
        btn("MinusButton", (36, 10, 17, 10), "", "Fewer steps", style="SmallIconButtonStyle", id=100000)])
    play = sub("Playback", 114, 106, [
        btn("Gated", (0, 0, 52, 20), "Gated", "Play only while the note is held", momentary=False),
        btn("Restart", (54, 0, 52, 20), "Restart", "Start from the top on every trigger", momentary=False)])
    pattern = N("Labeller", None, (58, 6, 222, 38), enumTextPosition="Below", style="SmallControlLabellerStyle", kids=[
        steps,
        N("PopupButton", "StepLengthCombo", (58, 0, 52, 20), displayName="Step Length", id=100004, style="DefaultPopupButtonStyle"),
        play])
    edit = N("Labeller", "EditLabeller", (286, 6, 222, 38), enumTextPosition="Below", style="SmallControlLabellerStyle", kids=[
        sub("Edit", 0, 222, [
            btn("QuantizeButton", (0, 0, 54, 20), "Quantize", "Quantise the pattern (or the selection)", id=100000),
            btn("RepeatButton", (56, 0, 56, 20), "Duplicate", "Repeat the pattern (or the selection)", id=100007),
            btn("Remix", (114, 0, 52, 20), "Remix", "Remix mode: one step sounds at a time", momentary=False),
            btn("CopyToNext", (168, 0, 54, 20), "Copy", "Copy to the next free pattern")])])
    tempo = N("Panel", None, (10, 0, 48, 20), displayName="Tempo Modifier", style="DefaultButtonStyle", kids=[
        N("ValueBox", "TempoNum", (2, 0, 18, 20), displayName="Tempo Modifier", placeholder="1", optSingleClickEdit=False,
          realIncDecRange=1, realMinValue=1, realMaxValue=16, style="InvisibleCenteredEditBoxStyle"),
        N("Label", None, (20, 0, 8, 20), style="SmallControlLabellerStyle", text="/"),
        N("ValueBox", "TempoDenom", (28, 0, 18, 20), displayName="Tempo Modifier", placeholder="1", optSingleClickEdit=False,
          realIncDecRange=1, realMinValue=1, realMaxValue=16, style="InvisibleCenteredEditBoxStyle")])
    engine = N("Labeller", "EngineControls", (W - SEL - 170, 6, 164, 38), pin="r", enumTextPosition="Below",
               style="SmallControlLabellerStyle", kids=[
                   tempo,
                   N("Knob", "SwingKnob", (80, 0, 20, 20), displayName="Swing", **SMALL_KNOB),
                   btn("SwingDrop", (102, 6, 10, 10), "▼", None, style="HeaderBarMenuDropButtonStyle"),
                   N("Knob", "InstoGraph", (126, 0, 20, 20), displayName="Graph Rec", **SMALL_KNOB)])
    left = N("Labeller", None, (0, 0, W - SEL, H), pin="lrtb", enumTextPosition="Below", style="SmallControlLabellerStyle", kids=[
        N("Panel", "ViewPanel", (6, 6, 46, 20), displayName="View", style="InvisibleStyle", kids=[
            btn("View", (0, 0, 46, 20), "Single", "One graph lane for all tracks", momentary=False)]),
        btn("OptionsButton", (14, 6, 20, 20), "", "Options", style="ExExLargeIconButtonStyle"),
        pattern, edit,
        N("PopupButton", "DragEdit", (514, 6, 90, 20), displayName="Drag edits", style="DefaultPopupButtonStyle"),
        N("TextBox", "PatternNameBox", (610, 6, 150, 20), displayName="Pattern name", id=100000, style="DefaultEditBoxStyle"),
        engine,
    ])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrt", style="InvisibleStyle", kids=[
        left, N("Panel", "Selectors", (W - SEL, 0, SEL, H), pin="rtb", overloadClass="PatternSelectors", style="InvisibleStyle")])


def editor():
    W, H = 800, 400
    CW = 160            # track controls column
    SB = 12
    split = 308
    lane = 75
    top_h = split
    step_h = top_h - 14
    upper = N("Panel", None, (0, 0, W, top_h), pin="lrtb", displayName="SplitterPanel0", style="InvisibleStyle", kids=[
        N("Panel", "StepPanel", (0, 14, W, step_h), pin="lrtb", style="InvisibleStyle", zorder=3, kids=[
            N("ScrollBar", "VScrollBar", (W - SB - 2, 0, SB, step_h - 2 * SB), pin="rtb", style="ScrollbarStyle"),
            btn("ZoomOutV", (W - SB - 2, step_h - 2 * SB, SB, SB), "-", None, style="WaveDisplayZoomButtonStyle", pin="rb"),
            btn("ZoomInV", (W - SB - 2, step_h - SB, SB, SB), "+", None, style="WaveDisplayZoomButtonStyle", pin="rb"),
            N("ScrollView", "ControlsScrollView", (0, 0, CW, step_h), pin="ltb", style="InvisibleStyle", zorder=2),
            N("ScrollView", "PatternScrollView", (CW, 0, W - CW - SB - 2, step_h), pin="lrtb", style="InvisibleStyle", zorder=2),
        ]),
        N("ScrollView", "TimelineView", (CW, 0, W - CW - SB - 18, 14), pin="lrt", style="InvisibleStyle", zorder=10),
    ])
    lower = N("Panel", "SingleViewPanel", (0, split + 1, W, lane), pin="lrtb", displayName="SplitterPanel1", style="InvisibleStyle", kids=[
        N("Panel", "SingleAutoControl", (0, 0, CW, lane), pin="ltb", overloadClass="PatternEditorGraphControls", style="InvisibleStyle"),
        N("ScrollView", "SingleScrollView", (CW, 0, W - CW - SB - 2, lane), pin="lrtb", style="InvisibleStyle"),
    ])
    nav = dict(style="TransparentLightIconButtonStyle", overloadClass="wdButton", pin="b")
    foot_y = H - 14
    navs = [("NextTrackButton", 5, "", "Next track"), ("PreviousTrackButton", 18, "", "Previous track"),
            ("NudgeTrackBackButton", 40, "", "Move this track one step earlier"),
            ("NudgeTrackForwardButton", 53, "", "Move this track one step later"),
            ("NudgePatternBackButton", 75, "", "Move the pattern (or selection) one step earlier"),
            ("NudgePatternForwardButton", 88, "", "Move the pattern (or selection) one step later")]
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="TopRightPanelStyle", kids=[
        N("SplitterPanel", "Splitter", (0, 2, W, H - 16), pin="lrtb", style="InvisibleStyle", SplitterPanelStyle="InvisibleStyle",
          intSplitPosition=split, intSplitterDim=1, intMinSize1=lane, intMaxSize1=lane, kids=[upper, lower]),
        *[btn(n, (x, foot_y, 12, 12), g, tip, **nav) for n, x, g, tip in navs],
        N("Panel", "HBarPanel", (CW, foot_y, W - CW, SB), pin="lrb", style="InvisibleStyle", kids=[
            N("ScrollBar", "HScrollBar", (0, 0, W - CW - 2 * SB - 12, SB), pin="lrtb", style="ScrollbarStyle"),
            btn("ZoomOutH", (W - CW - 2 * SB - 12, 0, SB, SB), "-", None, style="WaveDisplayZoomButtonStyle", pin="rtb"),
            btn("ZoomInH", (W - CW - SB - 12, 0, SB, SB), "+", None, style="WaveDisplayZoomButtonStyle", pin="rtb"),
        ]),
    ])


def track_row():
    W, H = 200, 20
    return N("Panel", "HighlightPanel", (0, 0, W, H), pin="lrtb", style="TrackNotSelectedStyle", kids=[
        N("DisclosureButton", "AutomateButton", (5, 0, 15, H), pin="ltb", displayName="Show graphs", id=100003, realScaling=0.5,
          style="InvisibleStyle", text="A"),
        N("Label", "SelectArea", (20, 0, W - 70, H), pin="lrtb", id=100000, style="DarkTextInvisibleEditBoxStyle", text=""),
        N("Knob", "PadLevel", (W - 48, 2, 16, 16), pin="rm", displayName="Pad level", **SMALL_KNOB),
        N("Button", "MuteButton", (W - 28, 4, 12, 12), pin="rm", displayName="Mute this track's steps", id=100002,
          style="TrackMuteStyle", text="M"),
        N("Button", "SoloButton", (W - 14, 4, 12, 12), pin="rm", displayName="Solo this track's steps", id=100004,
          style="TrackSoloStyle", text="S"),
    ])


def graph_lane():
    W, H = 150, 75
    knobs = [("ScaleKnob", "Offset", 100001), ("CompKnob", "Comp", 100005), ("RandKnob", "Rand", 100002),
             ("VarianceKnob", "Spread", 100002)]
    return N("Panel", "HighlightPanel", (0, 0, W, H), pin="lrtb", style="TrackNotSelectedStyle", kids=[
        btn("OptionsButton", (6, 2, 20, 20), "", "Graph tools", style="ExExLargeIconButtonStyle", pin="lt", id=100009),
        btn("GraphCombo", (28, 2, W - 30, 20), None, "Graph to show", style="DefaultPopupButtonStyle", pin="lrt", id=100009),
        N("Labeller", None, (0, 25, W, 50), pin="lrtb", enumTextPosition="Below", intTextOffset=-1, style="SmallControlLabellerStyle", kids=[
            *[N("Knob", n, (10 + i * 35, 3, 20, 20), displayName=cap, id=i_d, optCentered=True, **SMALL_KNOB)
              for i, (n, cap, i_d) in enumerate(knobs)],
            N("Button", "Learn", (W - 48, 36, 46, 12), pin="r", style="DefaultSmallButtonStyle", text="Learn")]),
        btn("AddButton", (6, H - 14, 12, 12), "+", "Add a graph lane", style="TransparentButtonStyle"),
        btn("RemoveButton", (20, H - 14, 12, 12), "x", "Remove this graph lane", style="TransparentButtonStyle"),
    ])


def convertor():
    W, H = 300, 160
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="DialogPanelStyle", kids=[
        N("Labeller", "CtrlPanel", (0, 0, W, H), pin="lrtb", enumTextPosition="Left", style="DialogPanelRightLabelStyle", kids=[
            N("ValueStepper", "NumStepsBox", (140, 16, 110, 20), pin="l", displayName="Steps", id=100001, style="DefaultPopupButtonStyle"),
            N("PopupButton", "RezCombo", (140, 48, 110, 20), pin="l", displayName="Grid", id=100004, style="DefaultPopupButtonStyle"),
            N("Button", "ApplyToAll", (140, 82, 16, 16), pin="l", displayName="All patterns", id=100008, style="DefaultCheckboxButtonStyle")]),
        btn("CancelButton", (W - 136, H - 28, 62, 20), "Cancel", None, momentary=False, pin="rb", id=100007),
        btn("ApplyButton", (W - 70, H - 28, 62, 20), "Apply", None, momentary=False, pin="rb", id=100006),
    ])


def outputs():
    return {
        "Skin/Patterns/PatternSelectors.skin": skin(selectors()),
        "Skin/Patterns/PatternPanel.skin": skin(page()),
        "Skin/Patterns/Toolbar.skin": skin(toolbar()),
        "Skin/Patterns/PatternEditor.skin": skin(editor()),
        "Skin/Patterns/TrackControls.skin": skin(track_row()),
        "Skin/Patterns/AutomationControls.skin": skin(graph_lane()),
        "Skin/Patterns/PatternConvertor.skin": skin(convertor()),
    }
