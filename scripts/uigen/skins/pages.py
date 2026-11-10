"""Song, scenes, MIDI mapping and the engine selector
(Song/, Scene/, Automation/, Engines/)."""

from . import N, skin

BAR = 30   # toolbar height on the pages


def btn(name, rect, text, tip=None, momentary=True, flashing=False, style="DefaultButtonStyle", pin="", **kw):
    kw.setdefault("overloadClass", "FlashingButton" if flashing else None)
    return N("Button", name, rect, pin=pin, text=text, displayName=tip, style=style, optIsMomentary=momentary or None, **kw)


def song_page():
    W, H = 800, 500
    tools = N("Panel", None, (308, 5, 184, 20), pin="c", style="InvisibleStyle", kids=[
        btn("EraseButton", (0, 0, 60, 20), "Erase", "Erase mode", id=100028),
        btn("ClearAllButton", (62, 0, 60, 20), "Clear All", "Remove every part", id=100028),
        btn("DuplicateButton", (125, 0, 60, 20), "Duplicate", "Duplicate the selection", id=100028),
    ])
    bar = N("Panel", None, (0, 0, W, BAR), pin="lr", style="BasicPanelStyle", kids=[
        btn("SelectPatternButton", (5, 5, 70, 20), "Pattern", "Pattern to insert", flashing=True, style="DefaultPopupButtonStyle", id=100028),
        btn("NextPatternButton", (74, 5, 16, 10), "", "Next pattern", flashing=True, style="SmallIconButtonStyle", id=100028),
        btn("PrevPatternButton", (74, 15, 16, 10), "", "Previous pattern", flashing=True, style="SmallIconButtonStyle", id=100028),
        tools,
    ])
    body_h = H - BAR - 15
    tiny = dict(style="TinyTransparentButtonStyle", id=100000)
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="RB", style="TopRightPanelStyle", kids=[
        bar,
        N("Panel", "TrackHeaderPanel", (0, BAR, 80, body_h), pin="ltb", id=100003, style="InvisibleStyle"),
        N("ScrollView", "TrackScrollView", (80, BAR, W - 80, body_h), pin="lrtb", id=100001, style="InvisibleStyle"),
        # Part handles the song view moves onto the hovered part.
        btn("PartNextPatternButton", (0, 0, 8, 8), "+", **tiny),
        btn("PartPrevPatternButton", (10, 0, 8, 8), "-", **tiny),
        btn("PartSelectPatternButton", (20, 0, 10, 10), "▼", **tiny),
        N("ScrollBar", "HorizontalScrollBar", (80, H - 14, W - 106, 12), pin="lrb", style="ScrollbarStyle"),
        btn("ZoomOutButton", (W - 26, H - 14, 12, 12), "-", "Zoom out", flashing=True, style="WaveDisplayZoomButtonStyle", pin="rb", id=100028),
        btn("ZoomInButton", (W - 14, H - 14, 12, 12), "+", "Zoom in", flashing=True, style="WaveDisplayZoomButtonStyle", pin="rb", id=100028),
        N("Panel", "BlackoutPanel", (80, BAR, W - 80, body_h), pin="lrtb", id=100001, style="SongPanelBlackoutPanelStyle", zorder=2),
    ])


def song_track_header():
    return N("Panel", "CtrlPanel", (0, 0, 80, 50), pin="lrtb", style="InvisibleStyle", kids=[
        N("Label", "TrackNumberLabel", (2, 0, 78, 50), pin="lrtb", id=100000, style="DarkTextInvisibleEditBoxStyle", text="1")])


def scene():
    W, H = 100, 75
    return N("Panel", "ScenePanel", (0, 0, W, H), pin="lrtb", style="SceneButtonStyle", kids=[
        N("Label", "NameLabel", (5, 5, W - 10, 18), pin="lrt", id=100005, overloadClass="AutoShorteningLabel",
          style="SceneNameLabelStyle", zorder=3),
        N("Label", "ActivityLabel", (5, 22, W - 10, 30), pin="lrm", style="SceneActivityLabelStyle"),
        btn("SelectButton", (1, H - 21, 46, 20), "C-2", "Select scene", momentary=False, style="SceneSelectionButtonStyle",
            pin="lb", id=100001),
        btn("SnapshotButton", (W - 44, H - 21, 20, 20), "", "Snapshot into this scene", style="SceneIconButtonStyle",
            pin="rb", id=100001),
        btn("ClearButton", (W - 22, H - 21, 20, 20), "", "Clear this scene", style="SceneIconButtonStyle",
            pin="rb", id=100001),
    ])


def scenes_page():
    W, H = 820, 395
    LW = 520
    banks = N("ButtonGroup", "BankButtons", ((LW - 130) // 2, 5, 130, 23), pin="ct", displayName="Scene bank",
              style="InvisibleStyle", optIsVertical=False, optClipChildren=False, intLeftSpacing=0, intRightSpacing=0,
              intTopSpacing=0, intBottomSpacing=3,
              kids=[N("Button", None, (i * 22, 0, 20, 20), displayName=f"Scene bank {i + 1}", style="DefaultButtonStyle",
                      text=str(i + 1)) for i in range(6)])
    bar = N("Panel", None, (0, 0, LW, BAR), pin="lrt", style="BasicPanelStyle", kids=[
        btn("SnapshotToNextButton", (10, 5, 100, 20), "Snapshot Next", "Snapshot into the next free scene", flashing=True, pin="lt", id=100028),
        btn("TriggerPrevSceneButton", (120, 5, 20, 20), "", "Play the previous scene", momentary=False, flashing=True,
            style="ExxLargeIconButtonStyle", pin="lt", id=100028),
        btn("TriggerNextSceneButton", (142, 5, 20, 20), "", "Play the next scene", momentary=False, flashing=True,
            style="ExxLargeIconButtonStyle", pin="lt", id=100028),
        banks,
        btn("ClearAllButton", (LW - 68, 5, 55, 20), "Clear All", "Clear every scene", flashing=True, pin="rt", id=100028),
    ])
    grid = N("Panel", None, (0, BAR, LW, H - BAR - 10), pin="lrtb", style="BasicPanelStyle", kids=[
        N("Matrix", "ScenesPanel", (10, 0, LW - 20, H - BAR - 15), pin="lrtb", id=100006, intNumberOfCols=4, intNumberOfRows=4,
          intIntraSpacing=5, intLeftSpacing=0, intTopSpacing=0, optLayoutFromTop=False, style="InvisibleStyle")])
    left = N("Panel", None, (0, 0, LW, H), pin="lrtb", style="InvisibleStyle", kids=[bar, grid])

    RW = W - LW
    TH = H - 10 - 165 - 5   # the engine table, 5 px above the panel's bottom
    start = N("ButtonGroup", "StartModeButtonGroup", (0, 0, 190, 23), pin="ct", displayName="Select Start Mode",
              id=100003, optIsVertical=False, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=3,
              kids=[N("Button", n, (i * 64, 0, 62, 20), displayName=tip, overloadClass="FlashingButton", style="DefaultButtonStyle",
                      text=t, id=1 if i < 2 else None)
                    for i, (n, t, tip) in enumerate([("ImmediateButton", "Immediate", "Start scenes at once"),
                                                     ("NextBeatButton", "Next Beat", "Start scenes on the next beat"),
                                                     ("NextBarButton", "Next Bar", "Start scenes on the next bar")])])
    right = N("Panel", "CtrlPanel", (LW, 0, RW, H - 10), pin="rtb", id=100009, style="BasicPanelStyle", kids=[
        N("Panel", "Selectors", (10, 5, RW - 19, 46), pin="lrt", overloadClass="PatternSelectors", style="InvisibleStyle"),
        N("Labeller", None, ((RW - 190) // 2, 60, 190, 90), pin="c", style="SmallControlLabellerStyle", enumTextPosition="Below",
          kids=[start, N("TextBox", "NameTextBox", (8, 51, 175, 20), pin="c", displayName="Scene Name", id=100001,
                         style="DefaultEditBoxStyle")]),
        # The engine table ends above the panel's bottom edge, scrolling
        # when the editor tabs are short (it ran out of the panel).
        N("Panel", None, (10, 165, RW - 19, TH), pin="lrtb", style="DarkPanelStyle", kids=[
            N("Panel", None, (1, 1, RW - 21, TH - 2), pin="lrtb", style="BasicPanelStyle", kids=[
                N("TableView", "DetailsTable", (0, 0, RW - 21, TH - 2), pin="lrtb", id=100000, style="DefaultTableViewScrollStyle",
                  HScrollBarStyle="", VScrollBarStyle="", ScrollViewStyle="DefaultTableViewScrollStyle",
                  TableHeaderPanelStyle="DefaultTableViewHeaderStyle", TablePanelStyle="DefaultTableViewStyle")])]),
    ])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="TopRightPanelStyle", kids=[left, right])


def mapping_page():
    W, H = 700, 500
    bar = N("Panel", "MapControls", (0, 0, W, 25), pin="lr", style="InvisibleStyle", kids=[
        btn("Clear", (2, 2, 60, 20), "Clear All", "Remove every mapping", pin="l", id=100016),
        btn("Lock", (84, 2, 20, 20), "", "Lock mappings", momentary=False, style="ExxLargeIconButtonStyle", pin="l", id=100017),
        btn("AddButton", (106, 2, 20, 20), "", "Add a mapping", style="ExxLargeIconButtonStyle", pin="l"),
        btn("Select", (128, 2, 70, 20), "Auto select", "Select the mapping that receives MIDI", momentary=False, pin="l", id=10000),
        btn("SendNotesButton", (W - 144, 2, 70, 20), "Send Note", "Send note data to the host", momentary=False, pin="r", id=100000),
        btn("SendCCButton", (W - 72, 2, 70, 20), "Send CC", "Send CCs to the host as they change", momentary=False, pin="r", id=100001),
    ])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="BasicPanelStyle", kids=[
        bar,
        N("TableView", "TableView", (0, 25, W, H - 25), pin="lrtb", id=100001, intScrollBarDim=12, style="InvisibleStyle",
          HScrollBarStyle="ScrollbarStyle", VScrollBarStyle="ScrollbarStyle", ScrollViewStyle="DefaultTableViewScrollStyle",
          TableHeaderPanelStyle="DefaultTableViewHeaderStyle", TablePanelStyle="DefaultTableViewStyle", optOverlay=False, optAutoHide=True),
    ])


def engine_selector():
    """One engine in the header: a round selector with mute, power and
    solo stacked at its right."""
    W, H = 70, 50
    d = 40
    x, y = 9, (H - d) // 2
    small = lambda n, r, st, text=None, tip=None, **kw: N("Button", n, r, style=st, text=text, displayName=tip, **kw)
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="InvisibleStyle", kids=[
        small("StateIndicator", (x - 4, y - 4, d + 8, d + 8), "EngineSelectorStateStyle"),
        small("EngineSelectionButton", (x, y, d, d), "EngineSelectorStyle", tip="Select engine", pin="m", id=100001),
        small("EngineVolIndic", (x, y, d, d), "EngineSelectorOverlayStyle", pin="m", id=100001, zorder=555),
        N("Label", "NameLabel", (x, y, d, d), pin="m", id=100001, style="EngineSelectorLabelStyle", text="1", zorder=666),
        small("EngineMutedIcon", (2, 3, 6, 6), "EngineSelectorMuteIndicatorStyle", id=100000, zorder=555),
        small("EngineSoloedIcon", (2, H - 9, 6, 6), "EngineSelectorSoloIndicatorStyle", id=100001, zorder=555),
        small("MuteButton", (W - 15, 2, 14, 14), "EngineSelectorMButtonStyle", "M", "Mute", pin="t", id=100002, zorder=999),
        small("PatternPower", (W - 15, 18, 14, 14), "EngineSelectorPPButtonStyle", "", "Pattern on/off", pin="m"),
        small("SoloButton", (W - 15, 34, 14, 14), "EngineSelectorSButtonStyle", "S", "Solo", pin="b", id=100003, zorder=999),
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
