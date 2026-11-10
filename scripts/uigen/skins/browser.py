"""The browser sidebar, the sampler strip and the slicer
(Browser/, Sampler/, Slicer/)."""

from . import N, skin
from .pages import btn


def icon(name, rect, glyph, tip, style="ExExLargeIconButtonStyle", **kw):
    return btn(name, rect, glyph, tip, style=style, **kw)


def browser():
    W, H = 325, 720
    return N("Panel", None, (0, 0, W, H), style="SidebarPanelStyle", kids=[
        N("Panel", "Header", (0, 0, W, 24), pin="lrt", overloadClass="BrowserHeader", style="InvisibleStyle"),
        N("Panel", "Search", (0, 24, W, 0), pin="lrt", overloadClass="BrowserSearchPane", style="InvisibleStyle"),
        N("Panel", "Navigator", (0, 24, W - 30, 22), pin="lrt", overloadClass="BrowserPathNavigator", style="BrowserPathNavStyle"),
        icon("PrevLocnButton", (W - 30, 24, 14, 22), "", "Back", style="TransparentIconButtonStyle", pin="rt", id=100000),
        icon("NextLocnButton", (W - 16, 24, 14, 22), "", "Forward", style="TransparentIconButtonStyle", pin="rt", id=100000),
        N("SplitterPanel", "SplitView", (0, 46, W, H - 46), pin="lrtb", style="InvisibleStyle", SplitterPanelStyle="SplitterStyle",
          # The file pane keeps room for its toolbar (182 px) in the
          # narrowest left column; the source list gives way first.
          intSplitPosition=115, intSplitterDim=3, intMinSize1=182, optIsVertical=False, optDbClkCollapse1=False,
          optSnapCollapse1=False, kids=[
              N("Panel", "SourceList", (0, 0, 115, H - 46), pin="lrtb", displayName="SplitterPanel0",
                overloadClass="BrowserSourceList", style="InvisibleStyle"),
              N("Panel", "Browser", (118, 0, W - 118, H - 46), pin="lrtb", displayName="SplitterPanel1",
                overloadClass="BrowserPane", style="InvisibleStyle"),
          ]),
    ])


def file_list():
    W, H = 210, 618
    t = dict(momentary=False)
    bar = N("Panel", None, (0, 0, W, 46), pin="lrt", style="BasicPanelStyle", kids=[
        btn("AutoAllocateButton", (2, 2, 40, 20), "A Load", "Auto load: load files onto pads when clicked", id=100004, **t),
        btn("SliceModeButton", (44, 2, 40, 20), "Slice", "Open audio files in the slicer when clicked", id=100007, **t),
        icon("PrevFileButton", (86, 2, 12, 20), "", "Previous file", style="DefaultIconButtonStyle", id=100000),
        icon("NextFileButton", (100, 2, 12, 20), "", "Next file", style="DefaultIconButtonStyle", id=100000),
        icon("ParentButton", (114, 2, 20, 20), "", "Up one folder", id=100000),
        icon("EnterButton", (136, 2, 20, 20), "", "Open the selected folder", id=100000),
        icon("RefreshButton", (158, 2, 20, 20), "", "Refresh", id=100000),
        icon("PreviewButton", (2, 24, 40, 20), "", "Audition files when clicked", momentary=False, id=100007),
        icon("StopButton", (44, 24, 40, 20), "", "Stop audition", id=100001),
        N("Slider", "PreviewVolume", (86, 27, W - 91, 15), pin="R", displayName="Preview volume", style="SliderStyle", realTrackInset=0.3),
    ])
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="InvisibleStyle", kids=[
        bar,
        N("Panel", "FileHeadings", (0, 46, W, 16), pin="lrt", overloadClass="BrowserFileHeadings", style="InvisibleStyle",
          displayName="Click to sort; right-click for View, Columns and Sort by"),
        N("Panel", "FileList", (0, 62, W, H - 62), pin="lrtb", overloadClass="BrowserFileList", style="InvisibleStyle")])


def header():
    W = 325
    return N("Panel", "ChooserPanel", (0, 0, W, 24), pin="R", style="InvisibleStyle", kids=[
        icon("ToolButton", (2, 2, 20, 20), "", "Browser options"),
        btn("LockPadsButton", (26, 2, 50, 20), "Lk Pads", "Lock or unlock all pads", momentary=False, id=100001),
        btn("LockPatternsButton", (78, 2, 50, 20), "Lk Pat.", "Lock or unlock all patterns", momentary=False, id=100002),
        N("SearchBox", "SearchBox", (135, 2, W - 137, 20), pin="lr", style="SearchBoxStyle"),
        N("ProgressBar", "Spinner", (156, 18, W - 165, 3), pin="lr", id=100001, optIsIndeterminate=True,
          style="BrowserSpinnerStyle", zorder=50),
    ])


def search_option():
    W = 300
    return N("Panel", None, (0, 0, W, 25), pin="lrtb", style="InvisibleStyle", kids=[
        N("PopupButton", "SearchType", (0, 2, 102, 21), pin="lr", displayName="What to search", id=100004, style="DefaultPopupButtonStyle"),
        N("PopupButton", "SubSearchType", (105, 2, 92, 21), displayName="Search by", id=100004, style="DefaultPopupButtonStyle",
          ARLeft="FFar 195.0000", ARRight="FNear 103.0000"),
        N("TextBox", "SearchTermBox", (200, 2, 100, 21), pin="r", displayName="Search for", id=100002, style="DefaultEditBoxStyle",
          ARRight="FNear 0.0000"),
    ])


def search_pane():
    W, H = 300, 125
    box = dict(intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0, style="InvisibleStyle")
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="InvisibleStyle", kids=[
        N("LayoutBox", None, (2, 5, W - 4, 90), pin="lrtb", kids=[
            N("Panel", f"Option{i + 1}", (0, i * 30, W - 4, 28), pin="lr", overloadClass="BrowserSearchPaneOptionItem",
              style="InvisibleStyle") for i in range(3)], **box),
        N("Labeller", None, (5, H - 25, 120, 20), pin="lb", enumTextPosition="Right", kids=[
            N("Button", "MatchAllButton", (0, 0, 20, 20), pin="tb", displayName="Match all options", id=100005, style="DefaultCheckboxButtonStyle")]),
        N("ProgressBar", "ProgressBar", (120, H - 25, W - 180, 20), pin="lrt", id=100001, optIsIndeterminate=True,
          style="BrowserSpinnerStyle", zorder=50),
        btn("DoSearchButton", (W - 55, H - 25, 50, 20), "Search", None, pin="rb", id=100003),
    ])


def sampler():
    """The recording strip above the pads (80 px: sampler::OPEN_HEIGHT)."""
    W, H = 300, 80
    fl = dict(overloadClass="FlashingButton")
    menus = N("LayoutBox", None, (69, 2, 184, 35), pin="r", optIsVertical=False, intLeftSpacing=0, intRightSpacing=0,
              intTopSpacing=0, intBottomSpacing=0, style="InvisibleStyle", kids=[
                  N("Labeller", None, (i * 62, 0, 60, 35), enumTextPosition="Below", intTextOffset=1,
                    style="SmallControlLabellerStyle", kids=[
                        N("PopupButton", n, (0, 0, 60, 20), pin="lr", displayName=cap, id=i_d, style="DefaultPopupButtonStyle")])
                  for i, (n, cap, i_d) in enumerate([("SourceList", "Source", 100000), ("TriggerMode", "Trigger", None),
                                                     ("Follow", "Assign", None)])])
    lab = N("Labeller", None, (0, 0, W, H), pin="lrtb", enumTextPosition="Below", intTextOffset=1, style="SmallControlLabellerStyle", kids=[
        N("Slider", "InputGain", (4, 3, 15, 63), pin="tb", displayName="In", id=100001, style="SliderStyle", realTrackInset=0.3),
        N("MultiChannelDBMeter", "VUMeter", (22, 2, 15, 64), pin="tb", id=100003, optIsLinear=True, style="DefaultVUMeterStyle"),
        N("Panel", None, (42, 2, 20, 42), style="InvisibleStyle", kids=[
            btn("MonoButton", (0, 0, 20, 20), "M", "Recording channels", id=100028, flashing=True),
            icon("ThruButton", (0, 22, 20, 20), "", "Hear the input", momentary=False, id=100028, flashing=True)]),
        N("Knob", "PreviewVolume", (42, 46, 20, 20), displayName="Thru", id=100001, style="KnobStyle", realDialThickness=0.3),
        menus,
        N("Labeller", "ThresholdPanel", (69, 36, 184, 40), pin="R", id=100001, enumTextPosition="Left", style="SmallControlLabellerStyle", kids=[
            N("Slider", "StartThresholdSlider", (28, 0, 156, 12), pin="Rt", displayName="Start", id=100004, overloadClass="SamplerSlider",
              style="SliderStyle", realTrackInset=0.3),
            N("MultiChannelDBMeter", "ThresholdVU", (28, 14, 156, 12), pin="Rtb", id=100004, optIsLinear=True,
              style="DefaultHorizontalVUMeterStyle"),
            N("Slider", "StopThresholdSlider", (28, 28, 156, 12), pin="Rb", displayName="Stop", id=100004, overloadClass="SamplerSlider",
              style="SliderStyle", realTrackInset=0.3)]),
        N("Panel", "SyncPanel", (69, 36, 180, 50), id=100005, style="InvisibleStyle", kids=[
            N("ButtonGroup", "SyncButtonGroup", (0, 0, 122, 20), id=100003, optIsVertical=False, intLeftSpacing=0, intRightSpacing=0,
              intTopSpacing=0, intBottomSpacing=0, kids=[
                  N("Button", "BeatsButton", (0, 0, 60, 20), displayName="Length in bars and beats", id=1, style="DefaultButtonStyle",
                    text="Beats", **fl),
                  N("Button", "SecsButton", (62, 0, 60, 20), displayName="Length in seconds", style="DefaultButtonStyle", text="Seconds", **fl)]),
            N("Labeller", "BeatsPanel", (0, 22, 170, 20), pin="l", id=100002, enumTextPosition="Right", intTextOffset=1,
              style="SmallControlLabellerStyle", kids=[
                  N("TextBox", "BarsTextBox", (0, 0, 60, 20), displayName="Bars", id=100000, style="DefaultEditBoxStyle"),
                  N("TextBox", "BeatsTextBox", (83, 0, 50, 20), displayName="Beats", id=100000, style="DefaultEditBoxStyle")]),
            N("Labeller", "SecondsPanel", (0, 22, 120, 20), id=100003, enumTextPosition="Right", intTextOffset=1,
              style="SmallControlLabellerStyle", kids=[
                  N("TextBox", "SecsTextBox", (0, 0, 80, 20), displayName="Seconds", id=100000, style="DefaultEditBoxStyle")])]),
        N("Panel", None, (W - 42, 2, 40, 42), pin="r", style="InvisibleStyle", kids=[
            btn("ArmButton", (0, 0, 40, 20), "Arm", "Wait for the start condition", momentary=False, id=100027, flashing=True),
            btn("RecButton", (0, 22, 40, 20), "Rec", "Record now", momentary=False, id=100027, flashing=True)]),
    ])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="BasicPanelStyle", kids=[lab])


def slicer():
    W, H = 870, 740
    tools = N("ButtonGroup", "ToolsButton", (10, 8, 86, 20), displayName="Tools...", intIntraSpacing=1, optIsVertical=False,
              intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0, kids=[
                  N("Button", None, (i * 21, 0, 20, 20), displayName=tip, style=st, text=g)
                  for i, (g, tip, st) in enumerate([("", "Insert tool (Alt-click deletes the slice point to the left)", "ExExLargeIconRadioButtonLeft"),
                                                    ("", "Delete tool (Alt-click inserts a slice point)", "ExExLargeIconRadioButtonCenter"),
                                                    ("", "Lock tool: click in a slice to lock its point", "ExExLargeIconRadioButtonCenter"),
                                                    ("", "Drag tool: drag a slice onto a pad (Alt adds a layer)", "ExExLargeIconRadioButtonRight")])])
    box = lambda n, x, cap, i_d: N("TextBox", n, (x, 8, 50, 20), displayName=cap, id=i_d, style="DefaultEditBoxStyle")
    extract = N("Panel", None, (W - 209, 8, 199, 20), pin="r", style="InvisibleStyle", kids=[
        btn("BothButton", (0, 0, 65, 20), "Audio+Ptn", "Extract the slices to pads and the pattern"),
        btn("AudioButton", (67, 0, 65, 20), "Audio", "Extract the slices to pads"),
        btn("PatternButton", (134, 0, 65, 20), "Pattern", "Extract the pattern to the current pattern")])
    controls = N("Labeller", "Controls", (0, 0, W, 45), pin="lrt", enumTextPosition="Below", style="SmallControlLabellerStyle", kids=[
        tools,
        N("Button", "AutoDetect", (118, 8, 20, 20), displayName="Auto", style="DefaultCheckboxButtonStyle"),
        box("BPMBox", 142, "BPM", 100014), box("BarsBox", 195, "Bars", 100015), box("BeatsBox", 248, "Beats", 100016),
        N("Button", "SliceMode", (313, 8, 60, 20), displayName="Extraction mode...", id=100008, style="DefaultButtonStyle", text="Transient"),
        N("Slider", "Sensitivity", (439, 8, 126, 20), pin="R", displayName="Sensitivity", id=100026, style="SliderStyle", realTrackInset=0.3),
        N("ValueStepper", "ChopDivisionBox", (440, 8, 50, 20), displayName="Divisions", id=100011, style="DefaultEditBoxStyle"),
        N("Panel", None, (W - 289, 8, 65, 20), pin="r", style="InvisibleStyle", kids=[
            btn("MultiLayersButton", (0, 0, 65, 20), "Use layers", "Put slices beyond 64 on extra layers", momentary=False, id=100000)]),
        extract,
    ])
    wave = N("Panel", "WavePanel", (5, 50, W - 10, 410), pin="lrtb", style="WavePanelBackingStyle", kids=[
        N("Panel", "WaveDisplay", (2, 2, W - 14, 386), pin="lrtb", overloadClass="SliceWaveEditor", style="InvisibleStyle"),
        N("Panel", "WaveZoomSlider", (2, 389, W - 85, 20), pin="lrb", displayName="WaveZoomSlider",
          overloadClass="WaveDisplayZoomSlider", style="WaveDisplayZoomSliderStyle"),
        N("Button", "PreviewWave", (W - 78, 389, 15, 20), pin="rb", displayName="Audition active portion", style="WaveDisplayZoomIconButtonStyle", text=""),
        N("Button", "LoopPreview", (W - 62, 389, 15, 20), pin="rb", displayName="Loop active portion", style="WaveDisplayZoomIconButtonStyle",
          text=""),
        btn("ZoomOutButton", (W - 42, 389, 15, 20), "-", "Zoom out", style="WaveDisplayZoomButtonStyle", pin="rb"),
        btn("ZoomInButton", (W - 27, 389, 15, 20), "+", "Zoom in", style="WaveDisplayZoomButtonStyle", pin="rb"),
    ])
    pattern = N("Panel", None, (5, 466, W - 10, 244), pin="lrb", style="DarkPanelStyle", kids=[
        N("Panel", "PatternView", (2, 2, W - 14, 240), pin="lrt", id=100001, overloadClass="SlicePanelPatternDisplay")])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="BasicPanelStyle", kids=[
        controls, wave, pattern,
        btn("CancelButton", (W - 130, H - 25, 60, 20), "Cancel", "Leave without slicing", pin="rb", id=100000),
        btn("DoneButton", (W - 65, H - 25, 60, 20), "Done", "Slice", pin="rb", id=100000),
    ])


def outputs():
    return {
        "Skin/Browser/Browser.skin": skin(browser()),
        "Skin/Browser/FileList.skin": skin(file_list()),
        "Skin/Browser/Header.skin": skin(header()),
        "Skin/Browser/SearchOptionItem.skin": skin(search_option()),
        "Skin/Browser/SearchPane.skin": skin(search_pane()),
        "Skin/Sampler/SimpleSamplerPanel.skin": skin(sampler()),
        "Skin/Slicer/SlicePanel.skin": skin(slicer()),
    }
