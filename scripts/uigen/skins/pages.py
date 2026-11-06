"""Song, scenes, MIDI mapping and the engine selector
(Song/, Scene/, Automation/, Engines/)."""

from . import N, skin

BAR = 30   # toolbar height on the pages


def btn(name, rect, text, tip=None, momentary=True, flashing=False, style="DefaultButtonStyle", pin="", **kw):
    kw.setdefault("overloadClass", "FlashingButton" if flashing else None)
    return N("Button", name, rect, pin=pin, text=text, displayName=tip, style=style, optIsMomentary=momentary or None, **kw)


def song_page():
    W, H = 800, 500
    tools = N("Panel", None, ((W - 190) // 2, 5, 190, 20), pin="c", style="InvisibleStyle", kids=[
        btn("EraseButton", (0, 0, 60, 20), "Erase", "Erase mode", id=100028),
        btn("ClearAllButton", (64, 0, 60, 20), "Clear All", "Remove every part", id=100028),
        btn("DuplicateButton", (128, 0, 62, 20), "Duplicate", "Duplicate the selection", id=100028),
    ])
    bar = N("Panel", None, (0, 0, W, BAR), pin="lr", style="BasicPanelStyle", kids=[
        btn("SelectPatternButton", (6, 5, 68, 20), "Pattern", "Pattern to insert", flashing=True, style="DefaultPopupButtonStyle", id=100028),
        btn("NextPatternButton", (76, 5, 14, 10), "", "Next pattern", flashing=True, style="SmallIconButtonStyle", id=100028),
        btn("PrevPatternButton", (76, 15, 14, 10), "", "Previous pattern", flashing=True, style="SmallIconButtonStyle", id=100028),
        tools,
    ])
    body_h = H - BAR - 15
    tiny = dict(style="TinyTransparentButtonStyle", id=100000)
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="rb", style="TopRightPanelStyle", kids=[
        bar,
        N("Panel", "TrackHeaderPanel", (0, BAR, 80, body_h), pin="lrtb", id=100003, style="InvisibleStyle"),
        N("ScrollView", "TrackScrollView", (80, BAR, W - 80, body_h), pin="lrtb", id=100001, style="InvisibleStyle"),
        # Part handles the song view moves onto the hovered part.
        btn("PartNextPatternButton", (0, 0, 8, 8), "+", **tiny),
        btn("PartPrevPatternButton", (10, 0, 8, 8), "-", **tiny),
        btn("PartSelectPatternButton", (20, 0, 10, 10), "▾", **tiny),
        N("ScrollBar", "HorizontalScrollBar", (80, H - 14, W - 108, 12), pin="lrb", style="ScrollbarStyle"),
        btn("ZoomOutButton", (W - 27, H - 14, 12, 12), "-", "Zoom out", flashing=True, style="WaveDisplayZoomButtonStyle", pin="rb", id=100028),
        btn("ZoomInButton", (W - 14, H - 14, 12, 12), "+", "Zoom in", flashing=True, style="WaveDisplayZoomButtonStyle", pin="rb", id=100028),
        N("Panel", "BlackoutPanel", (80, BAR, W - 80, body_h), pin="lrtb", id=100001, style="SongPanelBlackoutPanelStyle", zorder=2),
    ])


def song_track_header():
    return N("Panel", "CtrlPanel", (0, 0, 80, 50), pin="lrtb", style="InvisibleStyle", kids=[
        N("Label", "TrackNumberLabel", (4, 0, 76, 50), pin="lrtb", id=100000, style="DarkTextInvisibleEditBoxStyle", text="1")])


def scene():
    W, H = 100, 75
    return N("Panel", "ScenePanel", (0, 0, W, H), pin="lrtb", style="SceneButtonStyle", kids=[
        N("Label", "NameLabel", (5, 4, W - 10, 18), pin="lrt", id=100005, overloadClass="AutoShorteningLabel",
          style="SceneNameLabelStyle", zorder=3),
        N("Label", "ActivityLabel", (5, 24, W - 10, 26), pin="lrm", style="SceneActivityLabelStyle"),
        btn("SelectButton", (2, H - 21, 48, 20), "C-2", "Select scene", momentary=False, style="SceneSelectionButtonStyle",
            pin="ltb", id=100001),
        btn("SnapshotButton", (W - 44, H - 21, 20, 20), "", "Snapshot into this scene", style="SceneIconButtonStyle",
            pin="lrtb", id=100001),
        btn("ClearButton", (W - 22, H - 21, 20, 20), "", "Clear this scene", style="SceneIconButtonStyle",
            pin="lrtb", id=100001),
    ])


def scenes_page():
    W, H = 820, 395
    LW = 520
    banks = N("ButtonGroup", "BankButtons", ((LW - 142) // 2, 5, 142, 23), pin="ct", displayName="Scene bank",
              style="InvisibleStyle", optIsVertical=False, optClipChildren=False, intLeftSpacing=0, intRightSpacing=0,
              intTopSpacing=0, intBottomSpacing=3,
              kids=[N("Button", None, (i * 24, 0, 22, 20), displayName=f"Scene bank {i + 1}", style="DefaultButtonStyle",
                      text=str(i + 1)) for i in range(6)])
    bar = N("Panel", None, (0, 0, LW, BAR), pin="lrt", style="BasicPanelStyle", kids=[
        btn("SnapshotToNextButton", (8, 5, 96, 20), "Snapshot next", "Snapshot into the next free scene", flashing=True, pin="lt", id=100028),
        btn("TriggerPrevSceneButton", (110, 5, 20, 20), "", "Play the previous scene", momentary=False, flashing=True,
            style="ExxLargeIconButtonStyle", pin="lt", id=100028),
        btn("TriggerNextSceneButton", (132, 5, 20, 20), "", "Play the next scene", momentary=False, flashing=True,
            style="ExxLargeIconButtonStyle", pin="lt", id=100028),
        banks,
        btn("ClearAllButton", (LW - 66, 5, 58, 20), "Clear All", "Clear every scene", flashing=True, pin="rt", id=100028),
    ])
    grid = N("Panel", None, (0, BAR, LW, H - BAR - 8), pin="lrtb", style="BasicPanelStyle", kids=[
        N("Matrix", "ScenesPanel", (8, 2, LW - 16, H - BAR - 14), pin="lrtb", id=100006, intNumberOfCols=4, intNumberOfRows=4,
          intIntraSpacing=6, intLeftSpacing=0, intTopSpacing=0, optLayoutFromTop=False, style="InvisibleStyle")])
    left = N("Panel", None, (0, 0, LW, H), pin="lrtb", style="InvisibleStyle", kids=[bar, grid])

    RW = W - LW
    start = N("ButtonGroup", "StartModeButtonGroup", (0, 0, 192, 23), pin="ct", displayName="Start mode",
              id=100003, optIsVertical=False, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=3,
              kids=[N("Button", n, (i * 64, 0, 62, 20), displayName=tip, overloadClass="FlashingButton", style="DefaultButtonStyle",
                      text=t, id=1 if i < 2 else None)
                    for i, (n, t, tip) in enumerate([("ImmediateButton", "Now", "Start scenes at once"),
                                                     ("NextBeatButton", "Beat", "Start scenes on the next beat"),
                                                     ("NextBarButton", "Bar", "Start scenes on the next bar")])])
    right = N("Panel", "CtrlPanel", (LW, 0, RW, H - 10), pin="rtb", id=100009, style="BasicPanelStyle", kids=[
        N("Panel", "Selectors", (10, 6, RW - 20, 46), pin="lrt", overloadClass="PatternSelectors", style="InvisibleStyle"),
        N("Labeller", None, ((RW - 192) // 2, 60, 192, 92), pin="c", style="SmallControlLabellerStyle", enumTextPosition="Below",
          kids=[start, N("TextBox", "NameTextBox", (6, 52, 180, 20), pin="c", displayName="Scene name", id=100001,
                         style="DefaultEditBoxStyle")]),
        N("Panel", None, (10, 162, RW - 20, 184), pin="lrt", style="DarkPanelStyle", kids=[
            N("Panel", None, (1, 1, RW - 22, 182), pin="lrtb", style="BasicPanelStyle", kids=[
                N("TableView", "DetailsTable", (0, 0, RW - 22, 182), pin="lrtb", id=100000, style="DefaultTableViewScrollStyle",
                  HScrollBarStyle="", VScrollBarStyle="", ScrollViewStyle="DefaultTableViewScrollStyle",
                  TableHeaderPanelStyle="DefaultTableViewHeaderStyle", TablePanelStyle="DefaultTableViewStyle")])]),
    ])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="TopRightPanelStyle", kids=[left, right])


def mapping_page():
    W, H = 700, 500
    bar = N("Panel", "MapControls", (0, 0, W, 26), pin="lr", style="InvisibleStyle", kids=[
        btn("Clear", (3, 3, 62, 20), "Clear All", "Remove every mapping", pin="l", id=100016),
        btn("Lock", (69, 3, 20, 20), "", "Lock mappings", momentary=False, style="ExxLargeIconButtonStyle", pin="l", id=100017),
        btn("AddButton", (91, 3, 20, 20), "", "Add a mapping", style="ExxLargeIconButtonStyle", pin="l"),
        btn("Select", (115, 3, 76, 20), "Auto Select", "Select the mapping that receives MIDI", momentary=False, pin="l", id=10000),
        btn("SendNotesButton", (W - 150, 3, 72, 20), "Send Notes", "Send note data to the host", momentary=False, pin="r", id=100000),
        btn("SendCCButton", (W - 75, 3, 72, 20), "Send CC", "Send CCs to the host as they change", momentary=False, pin="r", id=100001),
    ])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="BasicPanelStyle", kids=[
        bar,
        N("TableView", "TableView", (0, 26, W, H - 26), pin="lrtb", id=100001, intScrollBarDim=10, style="InvisibleStyle",
          HScrollBarStyle="ScrollbarStyle", VScrollBarStyle="ScrollbarStyle", ScrollViewStyle="DefaultTableViewScrollStyle",
          TableHeaderPanelStyle="DefaultTableViewHeaderStyle", TablePanelStyle="DefaultTableViewStyle", optOverlay=False, optAutoHide=True),
    ])


def engine_selector():
    """One engine in the header: a round selector with mute, power and
    solo stacked at its right."""
    W, H = 70, 50
    d = 42
    x, y = 6, (H - d) // 2
    small = lambda n, r, st, text=None, tip=None, **kw: N("Button", n, r, style=st, text=text, displayName=tip, **kw)
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="InvisibleStyle", kids=[
        small("StateIndicator", (x - 3, y - 3, d + 6, d + 6), "EngineSelectorStateStyle"),
        small("EngineSelectionButton", (x, y, d, d), "EngineSelectorStyle", tip="Select engine", pin="m", id=100001),
        small("EngineVolIndic", (x, y, d, d), "EngineSelectorOverlayStyle", pin="m", id=100001, zorder=555),
        N("Label", "NameLabel", (x, y, d, d), pin="m", id=100001, style="EngineSelectorLabelStyle", text="1", zorder=666),
        small("EngineMutedIcon", (1, 2, 6, 6), "EngineSelectorMuteIndicatorStyle", id=100000, zorder=555),
        small("EngineSoloedIcon", (1, H - 8, 6, 6), "EngineSelectorSoloIndicatorStyle", id=100001, zorder=555),
        small("MuteButton", (W - 15, 2, 14, 14), "EngineSelectorMButtonStyle", "M", "Mute", pin="t", id=100002, zorder=999),
        small("PatternPower", (W - 15, 18, 14, 14), "EngineSelectorPPButtonStyle", "", "Pattern on/off", pin="m"),
        small("SoloButton", (W - 15, 34, 14, 14), "EngineSelectorSButtonStyle", "S", "Solo", pin="tb", id=100003, zorder=999),
    ])


def outputs():
    return {
        "Skin/Song/SongPanel.skin": skin(song_page()),
        "Skin/Song/SongTrackHeaderPanel.skin": skin(song_track_header()),
        "Skin/Scene/Scene.skin": skin(scene()),
        "Skin/Scene/ScenePanel.skin": skin(scenes_page()),
        "Skin/Automation/AutoMapPanel.skin": skin(mapping_page()),
        "Skin/Engines/EngineSelector.skin": skin(engine_selector()),
    }
