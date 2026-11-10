"""The window: root layout (splitters, tab strips) and the header bar
(RootSkin.skin, HeaderBar.skin)."""

from . import N, skin
from .pages import btn

W, H = 1400, 850


def tabs(name, w, items, style, right=0):
    """A tab strip: (id, label) pairs left to right; a None id starts the
    right-aligned group."""
    kids, x = [], 8
    right_items = [t for t in items if t[2]]
    for tid, text, at_right in items:
        if at_right:
            continue
        tw = 14 + 7 * len(text)
        kids.append(N("Button", None, (x, 2, tw, 20), id=tid, style="TabButtonStyle", text=text))
        x += tw + 16
    xr = w - 8
    for tid, text, _ in reversed(right_items):
        tw = 14 + 7 * len(text)
        xr -= tw
        kids.append(N("Button", None, (xr, 2, tw, 20), pin="r", id=tid, style="TabButtonStyle", text=text))
    return N("ButtonGroup", name, (0, 0, w, 20), pin="lrt", style=style, optChildPositionsAreLocked=True, optIsVertical=False,
             optUseChildID=True, intLeftSpacing=5, intRightSpacing=right, intTopSpacing=0, intBottomSpacing=0, intIntraSpacing=0,
             kids=kids)


def root():
    IW, IH = W - 10, H - 104
    SIDE = 300
    SPLIT = 8
    util_h = 518
    side = N("SplitterPanel", None, (0, 0, SIDE, IH), displayName="SplitterPanel0", style="TabPanelStyle", SplitterPanelStyle="SplitterStyle",
             intSplitPosition=util_h, intSplitterDim=SPLIT, intMinSize0=66, intMinSize1=220, intMaxSize1=400, optSnapCollapse0=False,
             strAutoSaveName="padSplitterAS", kids=[
                 N("Panel", "UtilityPanel", (0, 0, SIDE, util_h), displayName="SplitterPanel0", style="TabPanelStyle", kids=[
                     tabs("UtilityTabButtonGroup", SIDE, [(0, "BROWSER", False), (1, "TRANSMOD", False)], "TabPanelHeaderLeftStyle",
                          right=120),
                     N("TabPanel", "UtilityTabPanel", (0, 20, SIDE, util_h - 20), pin="lrtb", style="TabPanelStyle")]),
                 N("Panel", "PadsPanel", (0, util_h + SPLIT, SIDE, IH - util_h - SPLIT), pin="lrtb", displayName="SplitterPanel1",
                   overloadClass="EditorPads", style="InvisibleStyle")])
    MW = IW - SIDE - SPLIT
    ed_h = 372
    editor_tabs = [(0, "PATTERN", False), (3, "LAYER MIXER", False), (4, "PAD MIXER", False), (5, "GLOBAL MIXER", False),
                   (1, "SCENES", False), (2, "SONG", False), (6, "MAPPING", True)]
    main = N("Panel", "MainPanel", (SIDE + SPLIT, 0, MW, IH), displayName="SplitterPanel1", style="InvisibleStyle", kids=[
        N("SplitterPanel", "MainSplitter", (0, 0, MW, IH), pin="lrtb", style="InvisibleStyle", SplitterPanelStyle="SplitterStyle",
          intSplitPosition=ed_h, intSplitterDim=SPLIT, intMinSize0=190, intMinSize1=360, intMaxSize1=390, strAutoSaveName="mainSplitAS",
          kids=[
              N("Panel", "EditorPanel", (0, 0, MW, ed_h), displayName="SplitterPanel0", style="TabPanelStyle", kids=[
                  tabs("EditorTabButtons", MW, editor_tabs, "TabPanelHeaderRightStyle"),
                  N("TabPanel", "EditorTabPanel", (0, 20, MW, ed_h - 20), pin="lrtb", style="TabPanelStyle")]),
              N("Panel", "PadInspector", (0, ed_h + SPLIT, MW, IH - ed_h - SPLIT), pin="lrtb", displayName="SplitterPanel1",
                overloadClass="PadInspector", style="InvisibleStyle")])])
    return N("Panel", "BackPanel", (0, 0, W, H), pin="lrtb", id=100002, style="BackPanelStyle", kids=[
        N("Panel", "Header", (5, 3, IW, 60), pin="lrt", overloadClass="HeaderBar", style="InvisibleStyle"),
        N("SplitterPanel", "UtilitySplitter", (5, 66, IW, IH), pin="lrtb", style="InvisibleStyle", SplitterPanelStyle="SplitterStyle",
          intSplitPosition=SIDE, intSplitterDim=SPLIT, intMinSize0=250, intMaxSize0=600, optIsVertical=False, optDbClkCollapse1=False,
          strAutoSaveName="utilitySplitAS", kids=[side, main]),
        N("Panel", "TransmodSelectPanel", (5, H - 35, IW, 35), pin="lrb", overloadClass="TransmodButtonPanel", style="InvisibleStyle"),
    ])


def header():
    HH = 60
    menu = N("Panel", "Menu", (75, 3, 200, 15), style="InvisibleStyle", kids=[
        btn("LoadButton", (0, 0, 40, 15), "File", None, style="HeaderBarMenuButtonStyle", pin="tb", zorder=10),
        btn("ToolButton", (42, 0, 50, 15), "Tools", None, style="HeaderBarMenuButtonStyle", pin="tb", zorder=10),
        btn("HelpButton", (94, 0, 50, 15), "Help", None, style="HeaderBarMenuButtonStyle", pin="tb", zorder=10),
        *[N("Label", "DropArrowLabel", (x, 3, 10, 10), style="HeaderBarMenuDropButtonStyle", text="▼") for x in (22, 74, 123)],
    ])
    console = N("Panel", "PresetPanel", (75, 20, 200, 35), pin="b", id=100002, style="HeaderBarConsoleStyle", kids=[
        N("Label", None, (2, 2, 44, 15), id=100002, style="HeaderBarConsoleTextStyle", text="PRESET:"),
        # Liberation Sans sets "PRESET:" a few px wider than the original's
        # 40 px label: the name starts 3 px later.
        N("Label", "PresetLabel", (46, 2, 96, 15), pin="r", id=100002, style="HeaderBarPresetStyle", text=""),
        N("Button", "VoiceIndi", (145, 2, 12, 15), id=100002, style="HeaderBarIconIndicatorStyle", text=""),
        N("TempoBox", "BPMTextBox", (156, 2, 42, 15), displayName="Tempo", id=100002, style="HeaderBarConsoleRightTextStyle"),
        N("Label", None, (2, 17, 22, 15), id=100002, style="HeaderBarConsoleTextStyle", text="KIT:"),
        N("Label", "KitLabel", (26, 17, 116, 15), pin="r", id=100002, style="HeaderBarPresetStyle", text=""),
        N("Button", "MIDIIndi", (145, 17, 12, 15), id=100002, style="HeaderBarIconIndicatorStyle", text=""),
        N("Label", "MemoryUsageBox", (158, 17, 40, 15), id=100002, style="HeaderBarConsoleRightTextStyle", text=""),
    ])
    hb = dict(style="HeaderBarIconButtonStyle")
    # Transport: two rows of 24 px buttons.
    r1, r2 = 0, 26
    transport = N("Panel", "Transport", (W - 250, 5, 250, 50), pin="rtb", id=100002, style="InvisibleStyle", kids=[
        N("Button", "PlayButton", (0, r1, 36, 24), displayName="Play", id=100002, style="PlayButtonStyle", text=""),
        N("Button", "RecButton", (38, r1, 36, 24), displayName="Record", id=100003, style="RecordButtonStyle", text=""),
        btn("RetroButton", (76, r1, 36, 24), "", "Capture what you just played", style="RecordButtonStyle", id=100002),
        N("Button", "SongButton", (117, r1, 50, 24), displayName="Song mode", id=100000, style="HeaderBarButtonStyle", text="Song"),
        btn("UndoButton", (172, r1, 32, 24), "", "Undo", id=100000, **hb),
        btn("UndoHistory", (203, r1, 18, 24), "▼", "Undo history", style="HeaderBarUndoRedoDropStyle", id=100000),
        btn("MetroVolLearnButton", (224, r1, 24, 24), "MV", "Learn metronome level", style="HeaderBarButtonStyle", id=100001),
        btn("OptionsButton", (224, r1, 24, 24), "", "Transport options", id=100001, **hb),
        N("Button", "MetroButton", (0, r2, 36, 24), displayName="Metronome", id=100003, text="", **hb),
        N("Button", "QuantizeButton", (38, r2, 36, 24), displayName="Quantise MIDI input", id=100003, text="", **hb),
        N("Button", "LearnButton", (76, r2, 36, 24), displayName="MIDI learn", text="", **hb),
        N("Button", "LoopButton", (117, r2, 24, 24), displayName="Loop", text="", **hb),
        btn("RestartButton", (143, r2, 24, 24), "", "Back to the start", **hb),
        btn("RedoButton", (172, r2, 32, 24), "", "Redo", id=100001, **hb),
        btn("RedoHistory", (203, r2, 18, 24), "▼", "Redo history", style="HeaderBarUndoRedoDropStyle", id=100001),
        btn("PanicButton", (224, r2, 24, 24), "", "Panic: stop everything", id=100001, **hb),
    ])
    sel_w = 8 * 70 + 7 * 3
    return N("Panel", "HeaderBar", (0, 0, W, HH), pin="lrt", id=100002, style="InvisibleStyle", kids=[
        menu,
        N("Labeller", None, (5, 5, 65, 50), pin="tb", enumTextPosition="Below", intTextOffset=-1, style="SmallControlLabellerStyle", kids=[
            N("Panel", "MasterVU", (0, 0, 50, 50), overloadClass="LogoMeter", style="LogoStyle"),
            N("Slider", "GlobalGain", (53, 0, 12, 50), displayName="Master level", style="SliderStyle", realTrackInset=0.3)]),
        console,
        N("LayoutBox", "EngineSelectors", ((W - sel_w + 1) // 2, 5, sel_w, 50), pin="ctb", id=100002, overloadClass="EditorEngineSelectors",
          optIsVertical=False, intIntraSpacing=3, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
          style="InvisibleStyle"),
        transport,
    ])


def outputs():
    return {"Skin/RootSkin.skin": skin(root()), "Skin/HeaderBar.skin": skin(header())}
