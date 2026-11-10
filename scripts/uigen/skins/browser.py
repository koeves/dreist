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
        N("Panel", "Navigator", (0, 24, W - 32, 22), pin="lrt", overloadClass="BrowserPathNavigator", style="BrowserPathNavStyle"),
        icon("PrevLocnButton", (W - 31, 24, 14, 22), "", "Back", style="TransparentIconButtonStyle", pin="rt", id=100000),
        icon("NextLocnButton", (W - 16, 24, 14, 22), "", "Forward", style="TransparentIconButtonStyle", pin="rt", id=100000),
        N("SplitterPanel", "SplitView", (0, 46, W, H - 46), pin="lrtb", style="InvisibleStyle", SplitterPanelStyle="SplitterStyle",
          intSplitPosition=110, intSplitterDim=3, intMinSize1=120, optIsVertical=False, optDbClkCollapse1=False,
          optSnapCollapse1=False, kids=[
              N("Panel", "SourceList", (0, 0, 110, H - 46), pin="lrtb", displayName="SplitterPanel0",
                overloadClass="BrowserSourceList", style="InvisibleStyle"),
              N("Panel", "Browser", (113, 0, W - 113, H - 46), pin="lrtb", displayName="SplitterPanel1",
                overloadClass="BrowserPane", style="InvisibleStyle"),
          ]),
    ])


def file_list():
    W, H = 210, 618
    t = dict(momentary=False)
    bar = N("Panel", None, (0, 0, W, 46), pin="lrt", style="BasicPanelStyle", kids=[
        btn("AutoAllocateButton", (2, 2, 40, 20), "A Load", "Auto load: load files onto pads when clicked", id=100004, **t),
        btn("SliceModeButton", (44, 2, 40, 20), "Slice", "Open audio files in the slicer when clicked", id=100007, **t),
        icon("PrevFileButton", (88, 2, 12, 20), "", "Previous file", style="DefaultIconButtonStyle", id=100000),
        icon("NextFileButton", (101, 2, 12, 20), "", "Next file", style="DefaultIconButtonStyle", id=100000),
        icon("ParentButton", (116, 2, 20, 20), "", "Up one folder", id=100000),
        icon("EnterButton", (138, 2, 20, 20), "", "Open the selected folder", id=100000),
        icon("RefreshButton", (160, 2, 20, 20), "", "Refresh", id=100000),
        icon("PreviewButton", (2, 24, 40, 20), "", "Audition files when clicked", momentary=False, id=100007),
        icon("StopButton", (44, 24, 40, 20), "", "Stop audition", id=100001),
        N("Slider", "PreviewVolume", (88, 27, W - 92, 15), pin="lr", displayName="Preview volume", style="SliderStyle", realTrackInset=0.3),
    ])
    return N("Panel", None, (0, 0, W, H), pin="lrtb", style="InvisibleStyle", kids=[
        bar,
        N("Panel", "FileHeadings", (0, 46, W, 16), pin="lrt", overloadClass="BrowserFileHeadings", style="InvisibleStyle",
          displayName="Click to sort; right-click for View, Columns and Sort by"),
        N("Panel", "FileList", (0, 62, W, H - 62), pin="lrtb", overloadClass="BrowserFileList", style="InvisibleStyle")])


def header():
    W = 325
    return N("Panel", "ChooserPanel", (0, 0, W, 24), pin="r", style="InvisibleStyle", kids=[
        icon("ToolButton", (2, 2, 20, 20), "", "Browser options"),
        btn("LockPadsButton", (25, 2, 48, 20), "Pads", "Lock or unlock all pads", momentary=False, id=100001),
        btn("LockPatternsButton", (75, 2, 48, 20), "Patterns", "Lock or unlock all patterns", momentary=False, id=100002),
        N("SearchBox", "SearchBox", (128, 2, W - 130, 20), pin="lr", style="SearchBoxStyle"),
        N("ProgressBar", "Spinner", (140, 19, W - 150, 3), pin="lr", id=100001, optIsIndeterminate=True,
          style="BrowserSpinnerStyle", zorder=50),
    ])


def search_option():
    W = 300
    return N("Panel", None, (0, 0, W, 25), pin="lrtb", style="InvisibleStyle", kids=[
        N("PopupButton", "SearchType", (0, 2, 100, 21), displayName="What to search", id=100004, style="DefaultPopupButtonStyle",
          ARLeft="Relative 0.0000", ARRight="Relative 0.3333"),
        N("PopupButton", "SubSearchType", (103, 2, 94, 21), displayName="Search by", id=100004, style="DefaultPopupButtonStyle",
          ARLeft="Relative 0.3433", ARRight="Relative 0.6567"),
        N("TextBox", "SearchTermBox", (200, 2, 100, 21), displayName="Search for", id=100002, style="DefaultEditBoxStyle",
          ARLeft="Relative 0.6667", ARRight="Relative 1.0000"),
    ])


def search_pane():
    W, H = 300, 125
    box = dict(intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0, style="InvisibleStyle")
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="r", style="InvisibleStyle", kids=[
        N("LayoutBox", None, (2, 4, W - 4, 90), pin="lrtb", kids=[
            N("Panel", f"Option{i + 1}", (0, i * 30, W - 4, 28), pin="lr", overloadClass="BrowserSearchPaneOptionItem",
              style="InvisibleStyle") for i in range(3)], **box),
        N("Labeller", None, (4, H - 24, 110, 20), pin="lb", enumTextPosition="Right", kids=[
            N("Button", "MatchAllButton", (0, 2, 16, 16), displayName="Match all", id=100005, style="DefaultCheckboxButtonStyle")]),
        N("ProgressBar", "ProgressBar", (120, H - 16, W - 180, 4), pin="lrb", id=100001, optIsIndeterminate=True,
          style="BrowserSpinnerStyle", zorder=50),
        btn("DoSearchButton", (W - 56, H - 24, 52, 20), "Search", None, pin="rb", id=100003),
    ])


def sampler():
    """The recording strip above the pads (80 px: sampler::OPEN_HEIGHT)."""
    W, H = 300, 80
    fl = dict(overloadClass="FlashingButton")
    menus = N("LayoutBox", None, (70, 2, 184, 34), pin="r", optIsVertical=False, intLeftSpacing=0, intRightSpacing=0,
              intTopSpacing=0, intBottomSpacing=0, style="InvisibleStyle", kids=[
                  N("Labeller", None, (i * 62, 0, 60, 34), enumTextPosition="Below", intTextOffset=1,
                    style="SmallControlLabellerStyle", kids=[
                        N("PopupButton", n, (0, 0, 60, 19), pin="lr", displayName=cap, id=i_d, style="DefaultPopupButtonStyle")])
                  for i, (n, cap, i_d) in enumerate([("SourceList", "Source", 100000), ("TriggerMode", "Trigger", None),
                                                     ("Follow", "Assign", None)])])
    lab = N("Labeller", None, (0, 0, W, H), pin="lrtb", enumTextPosition="Below", intTextOffset=1, style="SmallControlLabellerStyle", kids=[
        N("Slider", "InputGain", (4, 3, 15, 62), pin="tb", displayName="Input", id=100001, style="SliderStyle", realTrackInset=0.3),
        N("MultiChannelDBMeter", "VUMeter", (21, 3, 14, 62), pin="tb", id=100003, optIsLinear=True, style="DefaultVUMeterStyle"),
        N("Panel", None, (40, 3, 24, 42), style="InvisibleStyle", kids=[
            btn("MonoButton", (2, 0, 20, 20), "M", "Recording channels", id=100028, flashing=True),
            icon("ThruButton", (2, 22, 20, 20), "", "Hear the input", momentary=False, id=100028, flashing=True)]),
        N("Knob", "PreviewVolume", (42, 47, 20, 20), displayName="Thru", id=100001, style="KnobStyle", realDialThickness=0.3),
        menus,
        N("Labeller", "ThresholdPanel", (70, 37, 184, 40), pin="r", id=100001, enumTextPosition="Left", style="SmallControlLabellerStyle", kids=[
            N("Slider", "StartThresholdSlider", (30, 0, 154, 12), pin="rt", displayName="Start", id=100004, overloadClass="SamplerSlider",
              style="SliderStyle", realTrackInset=0.3),
            N("MultiChannelDBMeter", "ThresholdVU", (30, 14, 154, 12), pin="rtb", id=100004, optIsLinear=True,
              style="DefaultHorizontalVUMeterStyle"),
            N("Slider", "StopThresholdSlider", (30, 28, 154, 12), pin="rtb", displayName="Stop", id=100004, overloadClass="SamplerSlider",
              style="SliderStyle", realTrackInset=0.3)]),
        N("Panel", "SyncPanel", (70, 37, 184, 42), id=100005, style="InvisibleStyle", kids=[
            N("ButtonGroup", "SyncButtonGroup", (0, 0, 120, 18), id=100003, optIsVertical=False, intLeftSpacing=0, intRightSpacing=0,
              intTopSpacing=0, intBottomSpacing=0, kids=[
                  N("Button", "BeatsButton", (0, 0, 58, 18), displayName="Length in bars and beats", id=1, style="DefaultButtonStyle",
                    text="Beats", **fl),
                  N("Button", "SecsButton", (60, 0, 60, 18), displayName="Length in seconds", style="DefaultButtonStyle", text="Seconds", **fl)]),
            N("Labeller", "BeatsPanel", (0, 21, 170, 19), pin="l", id=100002, enumTextPosition="Right", intTextOffset=2,
              style="SmallControlLabellerStyle", kids=[
                  N("TextBox", "BarsTextBox", (0, 0, 52, 19), displayName="Bars", id=100000, style="DefaultEditBoxStyle"),
                  N("TextBox", "BeatsTextBox", (82, 0, 52, 19), displayName="Beats", id=100000, style="DefaultEditBoxStyle")]),
            N("Labeller", "SecondsPanel", (0, 21, 120, 19), id=100003, enumTextPosition="Right", intTextOffset=2,
              style="SmallControlLabellerStyle", kids=[
                  N("TextBox", "SecsTextBox", (0, 0, 70, 19), displayName="Seconds", id=100000, style="DefaultEditBoxStyle")])]),
        N("Panel", None, (W - 42, 3, 40, 42), pin="r", style="InvisibleStyle", kids=[
            btn("ArmButton", (0, 0, 40, 20), "Arm", "Wait for the start condition", momentary=False, id=100027, flashing=True),
            btn("RecButton", (0, 22, 40, 20), "Rec", "Record now", momentary=False, id=100027, flashing=True)]),
    ])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="BasicPanelStyle", kids=[lab])


def slicer():
    W, H = 870, 740
    tools = N("ButtonGroup", "ToolsButton", (8, 8, 83, 20), displayName="Slice tool", intIntraSpacing=1, optIsVertical=False,
              intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0, kids=[
                  N("Button", None, (i * 21, 0, 20, 20), displayName=tip, style=st, text=g)
                  for i, (g, tip, st) in enumerate([("", "Insert tool (Alt-click deletes the slice point to the left)", "ExExLargeIconRadioButtonLeft"),
                                                    ("", "Delete tool (Alt-click inserts a slice point)", "ExExLargeIconRadioButtonCenter"),
                                                    ("", "Lock tool: click in a slice to lock its point", "ExExLargeIconRadioButtonCenter"),
                                                    ("", "Drag tool: drag a slice onto a pad (Alt adds a layer)", "ExExLargeIconRadioButtonRight")])])
    box = lambda n, x, cap, i_d: N("TextBox", n, (x, 8, 48, 20), displayName=cap, id=i_d, style="DefaultEditBoxStyle")
    extract = N("Panel", None, (W - 206, 8, 198, 20), pin="r", style="InvisibleStyle", kids=[
        btn("BothButton", (0, 0, 64, 20), "Audio+Ptn", "Extract the slices to pads and the pattern"),
        btn("AudioButton", (67, 0, 64, 20), "Audio", "Extract the slices to pads"),
        btn("PatternButton", (134, 0, 64, 20), "Pattern", "Extract the pattern to the current pattern")])
    controls = N("Labeller", "Controls", (0, 0, W, 46), pin="lrt", enumTextPosition="Below", style="SmallControlLabellerStyle", kids=[
        tools,
        N("Button", "AutoDetect", (104, 10, 16, 16), displayName="Auto", style="DefaultCheckboxButtonStyle"),
        box("BPMBox", 128, "BPM", 100014), box("BarsBox", 180, "Bars", 100015), box("BeatsBox", 232, "Beats", 100016),
        N("Button", "SliceMode", (292, 8, 70, 20), displayName="Detection mode", id=100008, style="DefaultButtonStyle", text="Transient"),
        N("Slider", "Sensitivity", (378, 8, 130, 20), pin="r", displayName="Sensitivity", id=100026, style="SliderStyle", realTrackInset=0.3),
        N("ValueStepper", "ChopDivisionBox", (378, 8, 52, 20), displayName="Divisions", id=100011, style="DefaultEditBoxStyle"),
        N("Panel", None, (W - 284, 8, 66, 20), pin="r", style="InvisibleStyle", kids=[
            btn("MultiLayersButton", (0, 0, 66, 20), "Use layers", "Put slices beyond 64 on extra layers", momentary=False, id=100000)]),
        extract,
    ])
    wave = N("Panel", "WavePanel", (4, 50, W - 8, 412), pin="lrtb", style="WavePanelBackingStyle", kids=[
        N("Panel", "WaveDisplay", (2, 2, W - 12, 386), pin="lrtb", overloadClass="SliceWaveEditor", style="InvisibleStyle"),
        N("Panel", "WaveZoomSlider", (2, 390, W - 90, 20), pin="lrb", displayName="WaveZoomSlider",
          overloadClass="WaveDisplayZoomSlider", style="WaveDisplayZoomSliderStyle"),
        N("Button", "PreviewWave", (W - 84, 390, 16, 20), pin="rb", displayName="Audition active portion", style="WaveDisplayZoomIconButtonStyle", text=""),
        N("Button", "LoopPreview", (W - 67, 390, 16, 20), pin="rb", displayName="Loop active portion", style="WaveDisplayZoomIconButtonStyle",
          text=""),
        btn("ZoomOutButton", (W - 46, 390, 16, 20), "-", "Zoom out", style="WaveDisplayZoomButtonStyle", pin="rb"),
        btn("ZoomInButton", (W - 29, 390, 16, 20), "+", "Zoom in", style="WaveDisplayZoomButtonStyle", pin="rb"),
    ])
    pattern = N("Panel", None, (4, 466, W - 8, 244), pin="lrb", style="DarkPanelStyle", kids=[
        N("Panel", "PatternView", (2, 2, W - 12, 240), pin="lrtb", id=100001, overloadClass="SlicePanelPatternDisplay")])
    return N("Panel", "CtrlPanel", (0, 0, W, H), pin="lrtb", style="BasicPanelStyle", kids=[
        controls, wave, pattern,
        btn("CancelButton", (W - 132, H - 25, 62, 20), "Cancel", "Leave without slicing", pin="rb", id=100000),
        btn("DoneButton", (W - 66, H - 25, 62, 20), "Done", "Slice", pin="rb", id=100000),
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
