"""Dialogs: about, preferences, export, missing files, audio and MIDI
setup, the MIDI monitor."""

from . import N, skin
from .pages import btn

TABLE = dict(HScrollBarStyle="", VScrollBarStyle="", ScrollViewStyle="DefaultTableViewScrollStyle",
             TableHeaderPanelStyle="DefaultTableViewHeaderStyle", TablePanelStyle="DefaultTableViewStyle")


def framed_table(name, rect, pin="lrtb", **kw):
    x, y, w, h = rect
    return N("Panel", None, rect, pin=pin, style="DarkPanelStyle", kids=[
        N("Panel", None, (1, 1, w - 2, h - 2), pin="lrtb", style="BasicPanelStyle", kids=[
            N("TableView", name, (0, 0, w - 2, h - 2), pin="lrtb", **{**TABLE, **kw})])])


def card(title, rect, body, pin="", cap_w=70):
    """A titled box: a tab-style caption over a framed body."""
    x, y, w, h = rect
    return N("Panel", None, rect, pin=pin, style="TabPanelHeaderStyle", kids=[
        N("Label", None, (2, 2, cap_w, 20), pin="lt", style="TabButtonStyle", text=title),
        N("Panel", None, (2, 20, w - 4, h - 22), pin="lrtb", style="BasicPanelStyle", kids=body)])


def about():
    W, H = 500, 200
    return N("Panel", None, (0, 0, W, H), style="DialogPanelStyle", kids=[
        N("Label", "Version", (5, 5, W // 2 - 5, 20), style="DialogPanelLeftLabelStyle", text="Version",
          ARLeft="FNear 5.0000", ARRight="Relative 0.5000", ARTop="FNear 5.0000"),
        N("Label", "DateLabel", (W // 2, 5, W // 2 - 5, 20), style="DialogPanelRightLabelStyle", text="Date",
          ARLeft="Relative 0.5000", ARRight="FNear 5.0000", ARTop="FNear 5.0000"),
        # Two centred lines (the editor puts a line break in the text).
        N("MultiLineLabel", "AboutLabel", (0, 62, W, 52), pin="lrtb", style="DialogPanelLargeCenterLabelStyle", text="",
          intLineHeight=26),
    ])


def preferences():
    W, H = 502, 542
    rows = [("MultiButton", "Pattern editor right click opens menu"),
            ("ForceModeButton", "Forced layers fall through if none found"),
            ("AutoAssign", "Auto assign MIDI CC's to graphs for export"),
            ("QuantizeREXButton", "Quantize loops on load"),
            ("PreFadeButton", "Auxes are pre fade by default"),
            ("ResetLayersButton", "Reset layer settings on load"),
            ("ActiveSensingButton", "Send Active Sensing Messages"),
            ("RestoreOutputsButton", "Restore outputs on preset load"),
            ("KeyboardButton", "Respond to keyboard controls"),
            ("ExtendedKeyboardButton", "Respond to extended keyboard controls"),
            ("YAxisPadVelocityButton", "Use Y-axis pad velocity mode"),
            ("RetardButton", "Use Audio Unit host timing correction")]
    X = 280
    kids = [N("Button", n, (X, 8 + i * 24, 16, 16), displayName=cap, id=100000, style="DefaultCheckboxButtonStyle")
            for i, (n, cap) in enumerate(rows)]
    y = 8 + len(rows) * 24 - 4
    kids.append(N("ButtonGroup", "MIDIModeGroup", (X, y, 94, 20), displayName="MIDI numbering", id=100000,
                  optIsVertical=False, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
                  kids=[N("Button", "CtrlButton", (k * 32, 0, 30, 20), id=i, style="DefaultButtonStyle", text=t)
                        for k, (i, t) in enumerate([(0, "0"), (1, "-2"), (2, "-1")])]))
    y += 24
    kids.append(N("ValueStepper", "UndoStages", (X, y, 50, 20), displayName="Number of undo stages", id=100001, style="DefaultPopupButtonStyle"))
    for n, cap in [("MetroType", "Metronome"), ("ShadingMode", "Pattern shading mode"), ("UIScaling", "UI scaling"),
                   ("UIStyle", "UI style"), ("RemMod", "Modulator remove behaviour")]:
        y += 24
        kids.append(N("PopupButton", n, (X, y, 210, 20), displayName=cap, style="DefaultPopupButtonStyle"))
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="DialogPanelStyle", kids=[
        N("Labeller", "CtrlPanel", (2, 2, W - 4, y + 28), pin="lrt", enumTextPosition="Left", id=100000,
          style="DialogPanelRightLabelStyle", kids=kids),
        N("Labeller", "CtrlPanel", (2, H - 70, W - 12, 20), pin="lrb", enumTextPosition="Left", id=100000,
          style="DialogPanelRightLabelStyle", kids=[
              N("TextBox", "DocumentsPath", (100, 0, W - 220, 20), pin="lr", displayName="Documents path", id=100001,
                style="DefaultEditBoxStyle"),
              btn("BrowseButton", (W - 116, 0, 50, 20), "Browse", None, pin="r", id=100000),
              btn("ResetPathButton", (W - 62, 0, 50, 20), "Reset", None, pin="r", id=100000)]),
        btn("CancelButton", (W - 165, H - 35, 75, 25), "Cancel", None, pin="rb", id=100007),
        btn("ConfirmButton", (W - 85, H - 35, 75, 25), "Finished", None, pin="rb", id=100007),
    ])


def export():
    W, H = 524, 334
    gap0 = dict(intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0)

    def choice(title, y, group, labels, extra=()):
        """A captioned group: right-aligned labels with their radio boxes after them."""
        sec = N("Panel", None, (10, y + 15, W - 20, 80), pin="lr", style="InvisibleStyle", kids=[
            N("LayoutBox", None, (25, 8, 200, 64), pin="lm", style="InvisibleStyle", **gap0,
              kids=[N("Label", "CtrlLabel", (0, i * 22, 200, 20), id=100002, style="DialogPanelRightLabelStyle", text=t)
                    for i, t in enumerate(labels)]),
            N("ButtonGroup", group, (225, 8, 20, 64), pin="lm", id=100000, **gap0,
              kids=[N("Button", "CtrlButton", (0, i * 22, 20, 20), id=100001, style="DefaultCheckboxButtonStyle")
                    for i in range(len(labels))]),
            *extra])
        return [N("Label", "CtrlLabel", (10, y, 78, 15), id=100002, style="DialogPanelLeftLabelStyle", text=title), sec]

    kids = []
    kids += choice("Source", 5, "SourceButtonGroup", ["All Engine Patterns", "Current Engine Pattern", "Song"])
    kids += choice("Files", 100, "OutputTypeButtonGroup", ["Stereo Mixdown", "Single Output", "All assigned outputs (multiple files)"],
                   extra=[N("PopupButton", "SingleOutputComboBox", (255, 30, 165, 20), pin="l", id=100004, style="DefaultPopupButtonStyle")])
    kids.append(N("Label", "CtrlLabel", (10, 195, 78, 15), id=100002, style="DialogPanelLeftLabelStyle", text="Normalization"))
    kids.append(N("Panel", None, (10, 210, W - 20, 80), pin="lr", style="InvisibleStyle", kids=[
        N("Labeller", None, (0, 10, W - 20, 60), pin="lrm", enumTextPosition="Left", id=100006, style="DialogPanelRightLabelStyle", kids=[
            N("PopupButton", "NormalizeComboBox", (225, 7, 195, 20), pin="l", displayName="Normalization mode", id=100002, style="DefaultPopupButtonStyle"),
            N("TextBox", "TailTextBox", (225, 36, 75, 20), pin="l", displayName="Tail Length (seconds)", id=100004, style="DefaultEditBoxStyle"),
            N("Button", "LoopButton", (310, 36, 50, 20), pin="l", id=100005, style="DefaultButtonStyle", text="Loop"),
            N("Button", "AutoCropButton", (370, 36, 60, 20), pin="l", id=100005, style="DefaultButtonStyle", text="AutoCrop")])]))
    kids += [
        N("ProgressBar", "ProgressBar", (10, H - 35, W - 185, 25), pin="lrb", id=100002, style="DialogProgressBarStyle"),
        btn("CancelButton", (W - 165, H - 35, 75, 25), "Cancel", None, pin="rb", id=100003),
        btn("StartButton", (W - 85, H - 35, 75, 25), "Export", None, pin="rb", id=100003),
    ]
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="DialogPanelStyle", kids=kids)


def file_find():
    W, H = 650, 400
    BY = 350
    bs = [("ManualButton", 5, 100, "Find Selected", 100006), ("AutoButton", 110, 100, "Auto Find", 100005),
          ("RemoveButton", 215, 100, "Remove Selected", 100005), ("SelectAll", 380, 70, "Select All", 100005),
          ("SelectNone", 455, 70, "Select None", 100005)]
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="DialogPanelStyle", kids=[
        N("Label", "TitleLabel", (5, 2, W - 10, 20), pin="lrt", id=100003, style="DialogPanelCenterLabelStyle",
          text="The listed audio files could not be found whilst loading"),
        N("Panel", "HoldingPanel", (0, 25, W, H - 25), pin="lrtb", style="InvisibleStyle", kids=[
            framed_table("FileList", (5, 0, W - 10, BY - 5), id=100000, style="DefaultTableViewScrollStyle"),
            *[btn(n, (x, BY, w, 20), t, None, pin="lb", id=i) for n, x, w, t, i in bs],
            btn("Finished", (W - 75, BY, 70, 20), "Finished", None, pin="rb", id=100004),
        ]),
        N("Panel", "ScanningPanel", (5, 25, W - 10, 60), pin="lrt", style="InvisibleStyle", kids=[
            N("Label", "CurrentScan", (5, 5, 115, 20), pin="lt", id=100004, style="DialogPanelLeftLabelStyle", text="Currently scanning"),
            N("Label", "ScanLabel", (120, 5, W - 135, 20), pin="lrt", id=100003, style="DialogPanelLeftLabelStyle"),
            N("ProgressBar", "ProgressBar", (5, 35, W - 75, 20), pin="lrb", style="DialogProgressBarStyle"),
            btn("AbortButton", (W - 65, 35, 50, 20), "Abort", None, pin="rb", id=100002),
        ]),
    ])


def audio_options():
    W, H = 320, 600
    IW = 296
    row = lambda n, y, cap, cls="PopupButton", st="DefaultPopupButtonStyle", **kw: N(cls, n, (90, y, IW - 100, 20), pin="lr",
                                                                                      displayName=cap, style=st, **kw)
    settings = N("Labeller", None, (0, 0, IW, 118), pin="lrtb", enumTextPosition="Left", intTextOffset=10, style="SmallControlLabellerStyle", kids=[
        row("SampleRate", 10, "Samplerate"),
        N("Labeller", "WinSettingPanel", (0, 35, IW, 70), pin="lr", enumTextPosition="Left", intTextOffset=10,
          style="SmallControlLabellerStyle", kids=[
              row("BufferSizeLBL", 0, "Buffer size", cls="Label", st="DefaultButtonStyle", text=""),
              row("ASIODevice", 25, "ASIO device"),
              N("Button", "ASIOButton", (90, 50, IW - 100, 20), pin="lr", style="DefaultButtonStyle", text="Open ASIO Panel")]),
        N("Labeller", "MacSettingPanel", (0, 35, IW, 70), pin="lr", enumTextPosition="Left", intTextOffset=10,
          style="SmallControlLabellerStyle", kids=[row("BufferSize", 0, "Buffer size"), row("InDevice", 25, "Input device"), row("OutDevice", 50, "Output device")]),
    ])
    io = N("Panel", None, (10, 155, 300, 405), pin="tb", style="TabPanelHeaderStyle", kids=[
        N("ButtonGroup", "IOGroup", (2, 2, 140, 20), pin="lt", optIsVertical=False, intIntraSpacing=0, intLeftSpacing=0, intRightSpacing=0,
          intTopSpacing=0, intBottomSpacing=0, kids=[N("Button", None, (i * 70, 0, 70, 20), style="TabButtonStyle", text=t)
                                                     for i, t in enumerate(["INPUTS", "OUTPUTS"])]),
        N("Panel", None, (2, 20, 296, 383), pin="lrtb", style="BasicPanelStyle", kids=[
            N("TableView", "IOTable", (0, 0, 296, 383), pin="lrtb", optOverlay=False, intScrollBarDim=12, style="InvisibleStyle", **TABLE)])])
    return N("Panel", None, (0, 0, W, H), style="BasicPanelStyle", kids=[
        card("SETTINGS", (10, 10, 300, 140), [settings], pin="lt"),
        io,
        btn("Refresh", (10, H - 30, 80, 20), "Refresh", None, pin="lb"),
        N("Button", "CheckBox", (116, H - 29, 20, 20), style="DefaultCheckboxButtonStyle"),
        N("Button", "Close", (W - 80, H - 30, 70, 20), pin="rb", style="DefaultButtonStyle", text="Close"),
    ])


def midi_options():
    W, H = 600, 400
    half = (W - 30) // 2
    tbl = lambda name: N("TableView", name, (0, 0, half - 4, 328), pin="lrtb", optOverlay=False, intScrollBarDim=12, style="InvisibleStyle", **TABLE)
    return N("Panel", None, (0, 0, W, H), style="BasicPanelStyle", kids=[
        card("INPUT DEVICES", (10, 10, half, 350), [tbl("InputTable")], pin="ltb", cap_w=100),
        card("OUTPUT DEVICES", (20 + half, 10, half, 350), [tbl("OutputTable")], pin="rtb", cap_w=100),
        btn("Refresh", (10, H - 30, 80, 20), "Refresh", None, pin="lb"),
        N("Button", "Sync", (100, H - 30, 80, 20), pin="lb", style="DefaultButtonStyle", text="Sync to clock",
          displayName="Follow the MIDI clock of the enabled input"),
        N("Button", "Close", (W - 80, H - 30, 70, 20), pin="rb", style="DefaultButtonStyle", text="Close"),
        N("Button", "CheckBox", (216, 571, 20, 20), style="DefaultCheckboxButtonStyle"),
    ])


def midi_monitor():
    W, H = 400, 400
    filt = [("Notes", "Notes"), ("CCs", "CCs"), ("Other", "Other")]
    return N("Panel", None, (0, 0, W, H), style="DarkPanelStyle", kids=[
        N("ListBox", "OutputView", (5, 5, W - 10, H - 35), pin="lrtb", style="ListViewSyle", LabelStyle="ListViewSyle",
          HScrollBarStyle="", VScrollBarStyle="", ScrollViewStyle="", intLineHeight=20, intScrollBarDim=12, intWrapBoundry=-1,
          optAutoHide=True, optOverlay=False, optShowHBar=False, optSupportsSelection=True, optWrapAtBorder=True),
        btn("Clear", (5, H - 26, 50, 20), "Clear", None),
        *[N("Button", n, (W - 5 - (3 - i) * 55 + 5, H - 26, 50, 20), style="DefaultButtonStyle", text=t, optIsMomentary=False)
          for i, (n, t) in enumerate(filt)],
    ])


def outputs():
    return {
        "Skin/AboutPanel.skin": skin(about()),
        "Skin/OptionsPanel.skin": skin(preferences()),
        "Skin/ExportPanel.skin": skin(export()),
        "Skin/FileFindPanel.skin": skin(file_find()),
        "Skin/AudioOptions.skin": skin(audio_options()),
        "Skin/MIDIOptions.skin": skin(midi_options()),
        "Skin/MIDIDisplayPanel.skin": skin(midi_monitor()),
    }
