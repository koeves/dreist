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


def card(title, rect, body, pin=""):
    """A titled box: a tab-style caption over a framed body."""
    x, y, w, h = rect
    return N("Panel", None, rect, pin=pin, style="TabPanelHeaderStyle", kids=[
        N("Label", None, (4, 2, 7 * len(title) + 16, 18), pin="lt", style="TabButtonStyle", text=title),
        N("Panel", None, (2, 20, w - 4, h - 22), pin="lrtb", style="BasicPanelStyle", kids=body)])


def about():
    W, H = 500, 200
    return N("Panel", None, (0, 0, W, H), style="DialogPanelStyle", kids=[
        N("Label", "Version", (8, 6, W // 2 - 8, 20), style="DialogPanelLeftLabelStyle", text="Version",
          ARLeft="FNear 8.0000", ARRight="Relative 0.5000", ARTop="FNear 6.0000"),
        N("Label", "DateLabel", (W // 2, 6, W // 2 - 8, 20), style="DialogPanelRightLabelStyle", text="Date",
          ARLeft="Relative 0.5000", ARRight="FNear 8.0000", ARTop="FNear 6.0000"),
        N("Label", "AboutLabel", (10, 44, W - 20, H - 70), pin="lrtb", style="DialogPanelLargeCenterLabelStyle", text=""),
    ])


def preferences():
    W, H = 502, 542
    rows = [("MultiButton", "Pattern editor right-click opens menu"),
            ("ForceModeButton", "Forced layers fall through if none found"),
            ("AutoAssign", "Auto-assign MIDI CCs to graphs on export"),
            ("QuantizeREXButton", "Quantize loops on load"),
            ("PreFadeButton", "Auxes are pre-fade by default"),
            ("ResetLayersButton", "Reset layer settings on load"),
            ("ActiveSensingButton", "Send Active Sensing messages"),
            ("RestoreOutputsButton", "Restore outputs on preset load"),
            ("KeyboardButton", "Computer keyboard shortcuts"),
            ("ExtendedKeyboardButton", "Extended keyboard shortcuts"),
            ("YAxisPadVelocityButton", "Pad velocity from click height"),
            ("RetardButton", "Use Audio Unit host timing correction")]
    X = 290
    kids = [N("Button", n, (X, 8 + i * 24, 16, 16), displayName=cap, id=100000, style="DefaultCheckboxButtonStyle")
            for i, (n, cap) in enumerate(rows)]
    y = 8 + len(rows) * 24 - 4
    kids.append(N("ButtonGroup", "MIDIModeGroup", (X, y, 96, 20), displayName="MIDI numbering (lowest octave)", id=100000,
                  optIsVertical=False, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
                  kids=[N("Button", None, (k * 32, 0, 30, 20), id=i, style="DefaultButtonStyle", text=t)
                        for k, (i, t) in enumerate([(0, "0"), (2, "-1"), (1, "-2")])]))
    y += 24
    kids.append(N("ValueStepper", "UndoStages", (X, y, 56, 20), displayName="Number of undo stages", id=100001, style="DefaultPopupButtonStyle"))
    for n, cap in [("MetroType", "Metronome"), ("ShadingMode", "Pattern shading mode"), ("UIScaling", "UI scaling"),
                   ("UIStyle", "UI style"), ("RemMod", "Modulator remove behaviour")]:
        y += 24
        kids.append(N("PopupButton", n, (X, y, 200, 20), displayName=cap, style="DefaultPopupButtonStyle"))
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="DialogPanelStyle", kids=[
        N("Labeller", "CtrlPanel", (2, 2, W - 4, y + 28), pin="lrt", enumTextPosition="Left", id=100000,
          style="DialogPanelRightLabelStyle", intTextOffset=10, kids=kids),
        N("Labeller", "CtrlPanel", (2, H - 70, W - 12, 20), pin="lrb", enumTextPosition="Left", id=100000,
          style="DialogPanelRightLabelStyle", kids=[
              N("TextBox", "DocumentsPath", (110, 0, W - 236, 20), pin="lr", displayName="Documents path", id=100001,
                style="DefaultEditBoxStyle"),
              btn("BrowseButton", (W - 122, 0, 54, 20), "Browse", None, pin="r", id=100000),
              btn("ResetPathButton", (W - 66, 0, 54, 20), "Reset", None, pin="r", id=100000)]),
        btn("CancelButton", (W - 168, H - 34, 78, 25), "Cancel", None, pin="rb", id=100007),
        btn("ConfirmButton", (W - 86, H - 34, 78, 25), "Done", None, pin="rb", id=100007),
    ])


def export():
    W, H = 524, 334

    def choice(title, y, group, labels, extra=()):
        """A captioned group of radio boxes with their labels."""
        sec = N("Panel", None, (10, y + 16, W - 20, 76), pin="lr", style="InvisibleStyle", kids=[
            N("ButtonGroup", group, (24, 6, 20, 64), id=100000, intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0,
              intBottomSpacing=0, kids=[N("Button", "CtrlButton", (2, i * 22 + 2, 16, 16), id=100001, style="DefaultCheckboxButtonStyle")
                                        for i in range(len(labels))]),
            N("LayoutBox", None, (50, 6, 220, 64), intLeftSpacing=0, intRightSpacing=0, intTopSpacing=0, intBottomSpacing=0,
              style="InvisibleStyle", kids=[N("Label", "CtrlLabel", (0, i * 22, 220, 20), id=100002, style="DialogPanelLeftLabelStyle", text=t)
                                            for i, t in enumerate(labels)]),
            *extra])
        return [N("Label", "CtrlLabel", (10, y, 120, 15), id=100002, style="DialogPanelLeftLabelStyle", text=title), sec]

    kids = []
    kids += choice("Source", 4, "SourceButtonGroup", ["All engine patterns", "Current engine pattern", "Song"])
    kids += choice("Files", 100, "OutputTypeButtonGroup", ["Stereo mixdown", "Single output", "All assigned outputs"],
                   extra=[N("PopupButton", "SingleOutputComboBox", (280, 28, 170, 20), id=100004, style="DefaultPopupButtonStyle")])
    kids.append(N("Label", "CtrlLabel", (10, 196, 120, 15), id=100002, style="DialogPanelLeftLabelStyle", text="Level"))
    kids.append(N("Panel", None, (10, 212, W - 20, 76), pin="lr", style="InvisibleStyle", kids=[
        N("Labeller", None, (0, 8, W - 20, 60), pin="lr", enumTextPosition="Left", id=100006, style="DialogPanelRightLabelStyle",
          intTextOffset=8, kids=[
              N("PopupButton", "NormalizeComboBox", (180, 6, 200, 20), displayName="Normalization", id=100002, style="DefaultPopupButtonStyle"),
              N("TextBox", "TailTextBox", (180, 34, 70, 20), displayName="Tail Length (s)", id=100004, style="DefaultEditBoxStyle"),
              N("Button", "LoopButton", (258, 34, 56, 20), id=100005, style="DefaultButtonStyle", text="Loop"),
              N("Button", "AutoCropButton", (320, 34, 60, 20), id=100005, style="DefaultButtonStyle", text="AutoCrop")])]))
    kids += [
        N("ProgressBar", "ProgressBar", (10, H - 34, W - 186, 24), pin="lrb", id=100002, style="DialogProgressBarStyle"),
        btn("CancelButton", (W - 168, H - 34, 76, 24), "Cancel", None, pin="rb", id=100003),
        btn("StartButton", (W - 86, H - 34, 76, 24), "Export", None, pin="rb", id=100003),
    ]
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="DialogPanelStyle", kids=kids)


def file_find():
    W, H = 650, 400
    BY = 345
    bs = [("ManualButton", 5, 96, "Locate...", 100006), ("AutoButton", 105, 96, "Search", 100005),
          ("RemoveButton", 205, 96, "Remove", 100005), ("SelectAll", 380, 72, "All", 100005), ("SelectNone", 456, 72, "None", 100005)]
    return N("Panel", "CtrlPanel", (0, 0, W, H), style="DialogPanelStyle", kids=[
        N("Label", "TitleLabel", (6, 3, W - 12, 20), pin="lrt", id=100003, style="DialogPanelCenterLabelStyle",
          text="These samples were not found"),
        N("Panel", "HoldingPanel", (0, 25, W, H - 25), pin="lrtb", style="InvisibleStyle", kids=[
            framed_table("FileList", (5, 0, W - 10, BY - 4), id=100000, style="DefaultTableViewScrollStyle"),
            *[btn(n, (x, BY, w, 20), t, None, pin="lb", id=i) for n, x, w, t, i in bs],
            btn("Finished", (W - 77, BY, 72, 20), "Done", None, pin="rb", id=100004),
        ]),
        N("Panel", "ScanningPanel", (5, 25, W - 10, 60), pin="lrt", style="InvisibleStyle", kids=[
            N("Label", "CurrentScan", (5, 5, 110, 20), pin="lt", id=100004, style="DialogPanelLeftLabelStyle", text="Searching"),
            N("Label", "ScanLabel", (118, 5, W - 133, 20), pin="lrt", id=100003, style="DialogPanelLeftLabelStyle"),
            N("ProgressBar", "ProgressBar", (5, 34, W - 76, 20), pin="lrb", style="DialogProgressBarStyle"),
            btn("AbortButton", (W - 66, 34, 52, 20), "Stop", None, pin="rb", id=100002),
        ]),
    ])


def audio_options():
    W, H = 320, 600
    IW = 296
    row = lambda n, y, cap, cls="PopupButton", st="DefaultPopupButtonStyle", **kw: N(cls, n, (96, y, IW - 106, 20), pin="lr",
                                                                                      displayName=cap, style=st, **kw)
    settings = N("Labeller", None, (0, 0, IW, 118), pin="lrtb", enumTextPosition="Left", intTextOffset=8, style="SmallControlLabellerStyle", kids=[
        row("SampleRate", 10, "Sample rate"),
        N("Labeller", "WinSettingPanel", (0, 35, IW, 70), pin="lr", enumTextPosition="Left", intTextOffset=8,
          style="SmallControlLabellerStyle", kids=[
              row("BufferSizeLBL", 0, "Buffer", cls="Label", st="DefaultButtonStyle", text=""),
              row("ASIODevice", 25, "Device"),
              N("Button", "ASIOButton", (96, 50, IW - 106, 20), pin="lr", style="DefaultButtonStyle", text="Driver Settings")]),
        N("Labeller", "MacSettingPanel", (0, 35, IW, 70), pin="lr", enumTextPosition="Left", intTextOffset=8,
          style="SmallControlLabellerStyle", kids=[row("BufferSize", 0, "Buffer"), row("InDevice", 25, "Input"), row("OutDevice", 50, "Output")]),
    ])
    io = N("Panel", None, (10, 156, 300, 404), pin="tb", style="TabPanelHeaderStyle", kids=[
        N("ButtonGroup", "IOGroup", (2, 2, 140, 20), pin="lt", optIsVertical=False, intIntraSpacing=0, intLeftSpacing=0, intRightSpacing=0,
          intTopSpacing=0, intBottomSpacing=0, kids=[N("Button", None, (i * 70, 0, 70, 20), style="TabButtonStyle", text=t)
                                                     for i, t in enumerate(["INPUTS", "OUTPUTS"])]),
        N("Panel", None, (2, 20, 296, 382), pin="lrtb", style="BasicPanelStyle", kids=[
            N("TableView", "IOTable", (0, 0, 296, 382), pin="lrtb", optOverlay=False, intScrollBarDim=10, style="InvisibleStyle", **TABLE)])])
    return N("Panel", None, (0, 0, W, H), style="BasicPanelStyle", kids=[
        card("DEVICE", (10, 10, 300, 140), [settings], pin="lt"),
        io,
        btn("Refresh", (10, H - 30, 80, 20), "Rescan", None, pin="lb"),
        N("Button", "CheckBox", (100, H - 28, 16, 16), style="DefaultCheckboxButtonStyle"),
        N("Button", "Close", (W - 80, H - 30, 70, 20), pin="rb", style="DefaultButtonStyle", text="Close"),
    ])


def midi_options():
    W, H = 600, 400
    half = (W - 30) // 2
    tbl = lambda name: N("TableView", name, (0, 0, half - 4, 328), pin="lrtb", optOverlay=False, intScrollBarDim=10, style="InvisibleStyle", **TABLE)
    return N("Panel", None, (0, 0, W, H), style="BasicPanelStyle", kids=[
        card("MIDI IN", (10, 10, half, 350), [tbl("InputTable")], pin="ltb"),
        card("MIDI OUT", (20 + half, 10, half, 350), [tbl("OutputTable")], pin="rtb"),
        btn("Refresh", (10, H - 30, 80, 20), "Rescan", None, pin="lb"),
        N("Button", "Sync", (96, H - 30, 90, 20), pin="lb", style="DefaultButtonStyle", text="Send Clock"),
        N("Button", "Close", (W - 80, H - 30, 70, 20), pin="rb", style="DefaultButtonStyle", text="Close"),
        N("Button", "CheckBox", (200, H - 28, 16, 16), style="DefaultCheckboxButtonStyle"),
    ])


def midi_monitor():
    W, H = 400, 400
    filt = [("Notes", "Notes"), ("CCs", "CCs"), ("Other", "Other")]
    return N("Panel", None, (0, 0, W, H), style="DarkPanelStyle", kids=[
        N("ListBox", "OutputView", (5, 5, W - 10, H - 34), pin="lrtb", style="ListViewSyle", LabelStyle="ListViewSyle",
          HScrollBarStyle="", VScrollBarStyle="", ScrollViewStyle="", intLineHeight=18, intScrollBarDim=10, intWrapBoundry=-1,
          optAutoHide=True, optOverlay=False, optShowHBar=False, optSupportsSelection=True, optWrapAtBorder=True),
        btn("Clear", (5, H - 25, 52, 20), "Clear", None),
        *[N("Button", n, (W - 5 - (3 - i) * 54, H - 25, 52, 20), style="DefaultButtonStyle", text=t, optIsMomentary=False)
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
