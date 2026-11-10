"""Dreist's colour palette, fonts and control styles.

Writes assets/ui/Skin/Styles/Dreist.style/{Colours,Fonts,Styles}.stylesheet
and assets/ui/Skin/project.gltinfo. Style and colour *names* are the
interface the skins and the editor code look up; every value is ours.

The look: dark ink chrome around pale paper panels, a cool slate scale in
between, one sky-blue accent, a hot pink for record/mute and a yellow for
solo. Corners are a touch rounder than square-cut.
"""

# ---------------------------------------------------------------- palette

# Our scale, darkest to lightest, plus accents (R, G, B).
INK = (37, 42, 44)
SLATE = (99, 107, 112)
SLATE_ALT = (134, 142, 147)
FOG_ALT = (160, 164, 167)
FOG = (184, 188, 190)
MIST = (216, 223, 227)
PAPER = (237, 241, 243)

NIGHT = (33, 38, 41)  # deepest editor tone
DUSK = (74, 79, 81)
SKY = (118, 172, 216)  # secondary accent

DEEP_SEA = (45, 70, 90)
SEA = (65, 99, 126)
GLOW = (138, 202, 255)  # main accent

SPARK = (240, 36, 95)
SPARK_DEEP = (79, 34, 48)
MUTE = (230, 42, 96)
SOLO = (232, 207, 42)

GRAD_TOP = (216, 223, 228)
GRAD_BOTTOM = (176, 190, 201)


def rgb(c):
    return "#%02X%02X%02X" % c


# name -> literal or (base name, modifier). The names are the ones the
# skins and code ask for.
COLOURS = [
    ("PanelGradientStart", rgb(GRAD_TOP)),
    ("PanelGradientEnd", rgb(GRAD_BOTTOM)),
    ("PanelDarkest", rgb(INK)),
    ("PanelDark", rgb(SLATE)),
    ("PanelAltDark", rgb(SLATE_ALT)),
    ("PanelMedium", rgb(FOG)),
    ("PanelAltMedium", rgb(FOG_ALT)),
    ("PanelBright", rgb(MIST)),
    ("PanelBrightest", rgb(PAPER)),
    ("PanelSpark", rgb(SPARK)),
    ("PanelAltSpark", rgb(SPARK_DEEP)),
    ("MuteSpark", rgb(MUTE)),
    ("SoloSpark", rgb(SOLO)),
    ("EditorDarkest", rgb(NIGHT)),
    ("EditorMedium", rgb(DUSK)),
    ("EditorBrightest", rgb(SKY)),
    ("EditorAltDarkest", rgb(DEEP_SEA)),
    ("EditorAltMedium", rgb(SEA)),
    ("EditorAltBrightest", rgb(GLOW)),
    # Translucent variants.
    ("PanelDarkestAlpha075", ("PanelDarkest", "alpha=0.75")),
    ("PanelDarkAlpha07", ("PanelDark", "alpha=0.7")),
    ("PanelDarkAlpha09", ("PanelDark", "alpha=0.9")),
    ("PanelMediumAlpha05", ("PanelMedium", "alpha=0.5")),
    ("PanelMediumAlpha03", ("PanelMedium", "alpha=0.3")),
    ("PanelSparkAlpha05", ("PanelSpark", "alpha=0.5")),
    ("EditorAltBrightestAlpha05", ("EditorAltBrightest", "alpha=0.5")),
    ("EditorDarkestAlpha03", ("EditorDarkest", "alpha=0.3")),
    ("EditorAltDarkestAlpha075", ("EditorAltDarkest", "alpha=0.75")),
    ("EditorBrightestAlpha02", ("EditorBrightest", "alpha=0.5")),
    ("PanelBrightestAlpha05", ("PanelBrightest", "alpha=0.5")),
    # Roles.
    ("EQBand1Colour", ("EditorBrightest", None)),
    ("EQBand2Colour", ("EditorMedium", None)),
    ("EQBand3Colour", ("EditorMedium", "darker=0.5")),
    ("EQBand4Colour", ("EditorDarkest", None)),
    ("ToolTipPanelColour", ("PanelBrightest", None)),
    ("ToolTipBorderColour", ("PanelDark", None)),
    ("ToolTipTextColour", ("PanelDarkest", None)),
    ("LearnOverlayColour", ("Yellow", None)),
    ("LearnTargetColour", ("Orange", None)),
    ("LearnTextColour", ("PanelDarkest", None)),
]

# ---------------------------------------------------------------- fonts

SANS = "Dreist Sans"  # dreist_gui::text: Liberation Sans, sized to fit
ICONS = "Dreist-Icons"

# name -> (family, size, bold)
FONTS = [
    ("SuperSized", SANS, 30, True),
    ("ExExExLargeBold", SANS, 20, True),
    ("ExExLarge", SANS, 17, False),
    ("ExLarge", SANS, 16, False),
    ("ExLargeBold", SANS, 16, True),
    ("Large", SANS, 14, False),
    ("LargeBold", SANS, 14, True),
    ("LargeStandard", SANS, 13, False),
    ("LargeStandardBold", SANS, 13, True),
    ("Standard", SANS, 12, False),
    ("StandardBold", SANS, 12, True),
    ("SmallStd", SANS, 11, False),
    ("SmallStdBold", SANS, 11, True),
    ("Small", SANS, 10, False),
    ("SmallBold", SANS, 10, True),
    ("Tiny", SANS, 8, False),
    ("TinyBold", SANS, 8, True),
    ("Micro", SANS, 6, False),
    ("MicroBold", SANS, 6, True),
    ("SmallIcons", ICONS, 10, False),
    ("StandardIcons", ICONS, 12, False),
    ("LargeIcons", ICONS, 14, False),
    ("ExLargeIcons", ICONS, 15, False),
    ("ExxLargeIcons", ICONS, 16, False),
    ("ExExLargeIcons", ICONS, 16, False),
]

# ---------------------------------------------------------------- styles

R_SMALL, R_MED, R_LARGE = 3, 3, 5
NO_ROUND = dict(optRoundTopLeft="false", optRoundTopRight="false", optRoundBottomLeft="false", optRoundBottomRight="false")


def corners(tl=False, tr=False, bl=False, br=False):
    b = lambda v: "true" if v else "false"
    return dict(optRoundTopLeft=b(tl), optRoundTopRight=b(tr), optRoundBottomLeft=b(bl), optRoundBottomRight=b(br))


CLEAR = dict(colFill="Transparent", colAltFill="Transparent", colBorder="Transparent", colAltBorder="Transparent")

STYLES = []  # (element, name, parent, attrs)


def S(name, parent="ApplicationStyle", kind="CtrlStyle", **attrs):
    STYLES.append((kind, name, parent, attrs))


def section(title):
    STYLES.append(("#", title, None, None))


section("Base")
S("ShadowStyle", realCornerRounding="0", optDrawShadow="false")
S("CornerRoundingStyle", "ShadowStyle", realCornerRounding=R_MED)
S("CornerRounding2Style", "ShadowStyle", realCornerRounding=R_SMALL - 1)
S("CornerRounding3Style", "ShadowStyle", realCornerRounding=R_SMALL)
S("CornerRounding5Style", "ShadowStyle", realCornerRounding=R_LARGE)

section("Tooltips and menus")
S("TooltipStyle", "ShadowStyle", optDrawShadow="true", enumDisabledDrawMode="NormalDrawing", colFill="ToolTipPanelColour", colBorder="ToolTipBorderColour", colText="ToolTipTextColour", font="Standard")
S("MenuStyle", "CornerRounding5Style", "CtrlOptionMenuStyle", optDrawShadow="true", colFill="ToolTipPanelColour", colBorder="ToolTipBorderColour", colAltFill="EditorAltBrightest", colDivider="PanelMedium", colSubMenuArrow="ToolTipTextColour", colText="ToolTipTextColour", font="Standard")

section("Logo")
S("LogoStyle", optDrawBorder="false", enumDisabledDrawMode="NormalDrawing", colFill="EditorAltBrightestAlpha05", colAltFill="PanelBrightestAlpha05")

section("Panels")
S("BackPanelStyle", "ShadowStyle", optDrawBorder="true", colFill="PanelDarkest", colBorder="PanelDarkest")
S("BasicPanelStyle", "ShadowStyle", optDrawBorder="true", colFill="PanelBrightest", colBorder="PanelBrightest")
S("SplitterStyle", "BackPanelStyle", colAltBorder="PanelMedium")
S("DarkPanelStyle", optDrawBorder="true", colFill="PanelDark", colBorder="PanelDark")
S("LayerPanelStyle", "BasicPanelStyle", realCornerRounding=R_LARGE, **corners(tl=True))
S("SidebarPanelStyle", "BasicPanelStyle", realCornerRounding=R_LARGE, **corners(br=True))
S("TopRightPanelStyle", "DarkPanelStyle", realCornerRounding=R_LARGE, **corners(bl=True))
S("LightDividerStyle", optDrawBorder="true", colFill="PanelBright", colBorder="PanelBright")

section("Collapsible panels")
S("CollapsePanelStyle", "BasicPanelStyle", optDrawBorder="true", colFill="Transparent", colBorder="Transparent", colAltFill="PanelMedium", colText="EditorDarkest", font="Standard")
S("EffectCollapsePanelStyle", "CollapsePanelStyle", enumTextHorizontalAlign="left", realTextOffset="22", enumShortenAlgorithn="end")
S("TransmodCollapsePanelStyle", "CollapsePanelStyle", enumTextHorizontalAlign="left", realTextOffset="18", enumShortenAlgorithn="end")

section("Dialogs")
S("DialogPanelStyle", "CornerRounding5Style", colFill="PanelDarkestAlpha075", optRoundTopLeft="false", optRoundTopRight="false")
S("TriggerDialogPanelStyle", "DialogPanelStyle", optRoundTopLeft="true", optRoundTopRight="true")
S("DialogPanelLeftLabelStyle", optDrawBorder="false", colFill="Transparent", colText="PanelBrightest", enumTextHorizontalAlign="left")
S("DialogPanelRightLabelStyle", "DialogPanelLeftLabelStyle", enumTextHorizontalAlign="right")
S("DialogPanelCenterLabelStyle", "DialogPanelLeftLabelStyle", enumTextHorizontalAlign="center")
S("DialogPanelLargeCenterLabelStyle", "DialogPanelCenterLabelStyle", font="ExLargeBold")
S("DialogPanelLeftLabellerStyle", "DialogPanelLeftLabelStyle")
S("DialogProgressBarStyle", realBorderWidth="15", colFill="Transparent", colBorder="PanelDarkAlpha09", colAltFill="EditorAltBrightest")

section("Labellers")
S("LargeControlLabellerStyle", "InvisibleStyle", colText="EditorDarkest", font="Standard")
S("SmallControlLabellerStyle", "InvisibleStyle", colText="PanelDark", font="Small")
S("SmallDarkControlLabellerStyle", "InvisibleStyle", colText="EditorDarkest", font="Small")

section("Buttons")
S("DefaultButtonStyle", "CornerRoundingStyle", font="Standard", realTextOffset="0", enumTextShortenAlgorithm="end",
  colFill="PanelMedium", colBorder="PanelMedium", colText="EditorDarkest", colAltFill="EditorAltBrightest", colAltBorder="EditorAltBrightest", colAltText="EditorDarkest")
S("MuteButtonStyle", "DefaultButtonStyle", colAltFill="MuteSpark", colAltBorder="MuteSpark")
S("SoloButtonStyle", "DefaultButtonStyle", colAltFill="SoloSpark", colAltBorder="SoloSpark")
S("TransparentButtonStyle", "CornerRoundingStyle", font="Standard", realTextOffset="0", enumTextShortenAlgorithm="end", colText="EditorDarkest", colAltText="EditorAltBrightest", **CLEAR)
S("TinyTransparentButtonStyle", "TransparentButtonStyle", font="Tiny")
S("LargeTextButtonStyle", "DefaultButtonStyle", font="ExLarge")
S("SmallTextButtonStyle", "DefaultButtonStyle", font="Small")
S("DefaultSmallButtonStyle", "DefaultButtonStyle", font="Small")
S("DefaultTinyButtonStyle", "DefaultSmallButtonStyle", realCornerRounding="0", font="SmallBold")
S("DefaultIconButtonStyle", "DefaultButtonStyle", font="StandardIcons")
S("TransparentIconButtonStyle", "TransparentButtonStyle", font="StandardIcons")
S("TransparentLightIconButtonStyle", "TransparentIconButtonStyle", colText="PanelMedium", colAltText="EditorAltBrightest")
S("SmallIconButtonStyle", "DefaultTinyButtonStyle", font="SmallIcons")
S("LargeIconButtonStyle", "DefaultButtonStyle", font="LargeIcons")
S("ExxLargeIconButtonStyle", "DefaultButtonStyle", font="ExxLargeIcons")
S("ExExLargeIconButtonStyle", "DefaultButtonStyle", font="ExExLargeIcons")
S("ExExLargeIconRadioButtonLeft", "ExExLargeIconButtonStyle", optRoundTopRight="false", optRoundBottomRight="false")
S("ExExLargeIconRadioButtonRight", "ExExLargeIconButtonStyle", optRoundTopLeft="false", optRoundBottomLeft="false")
S("ExExLargeIconRadioButtonCenter", "ExExLargeIconButtonStyle", **NO_ROUND)
S("DefaultCheckboxButtonStyle", "DefaultButtonStyle", "CheckBoxButtonRendererStyle", colTick="PanelDarkest")
S("DefaultPopupButtonStyle", "DefaultButtonStyle", enumTextHorizontalAlign="left")
S("ShorteningPopupButtonStyle", "DefaultPopupButtonStyle", enumTextShortenAlgorithm="middle")

section("Text fields")
S("DefaultEditBoxStyle", "CornerRoundingStyle", font="Standard", colText="EditorDarkest", colFill="PanelAltMedium", colAltFill="PanelAltMedium", colBorder="PanelAltMedium", colAltBorder="PanelAltMedium")
S("SearchBoxStyle", "DefaultEditBoxStyle", enumTextHorizontalAlign="left", colAltFill="EditorDarkest")
S("InvisibleEditBoxStyle", optDrawShadow="false", optDrawBorder="false", colFill="Transparent", enumTextHorizontalAlign="left", font="SmallStd")
S("InvisibleCenteredEditBoxStyle", "InvisibleEditBoxStyle", enumTextHorizontalAlign="center")
S("DarkTextInvisibleEditBoxStyle", "InvisibleEditBoxStyle", colText="EditorDarkest")
S("LightTextInvisibleEditBoxStyle", "InvisibleEditBoxStyle", colText="PanelBrightest")
S("EmptyLayerTextStyle", "InvisibleEditBoxStyle", colText="PanelMedium")
S("FieldEditorStyle", enumTextHorizontalAlign="left", font="Standard")
S("ListViewSyle", "DefaultEditBoxStyle", enumTextHorizontalAlign="left", font="Standard")

section("Plots and meters")
S("PlotStyle", "CornerRounding5Style", colFill="PanelMedium", colBorder="PanelMedium", colAltBorder="EditorBrightest", colText="PanelAltMedium")
S("TransmodPlotStyle", "PlotStyle", colFill="PanelDark", colBorder="PanelDark")
S("MeterStyle", optDrawShadow="false", optRoundBottomLeft="false", optRoundBottomRight="false", realBorderWidth="3", realCornerRounding="10", colFill="PanelMedium", colText="EditorDarkest", font="TinyBold")
VU = dict(colChannelBack="EditorDarkest", colClipArea="PanelAltSpark", colClip="PanelSpark", colFill="EditorDarkest", colBorder="EditorDarkest",
          colMarkingLines="Transparent", colMarkingText="EditorDarkest", colMaxDB="EditorAltBrightest", colMidDB="EditorBrightest", colMinDB="EditorAltMedium",
          colPeak="EditorAltBrightest", intClipDimension="8", intMarkingSize="14", intChannelSpacing="0", realTextOffset="1", font="Tiny")
S("DefaultVUMeterStyle", "ShadowStyle", "CtrlMultiChannelDBMeterStyle", **VU)
S("DefaultVerticalVUMeterStyle", "DefaultVUMeterStyle", "CtrlMultiChannelDBMeterStyle", intChannelSpacing="1", intMarkingSize="0")
S("BigVerticalVUMeterStyle", "DefaultVUMeterStyle", "CtrlMultiChannelDBMeterStyle", intChannelSpacing="2", intMarkingSize="12")
S("DefaultHorizontalVUMeterStyle", "DefaultVUMeterStyle", "CtrlMultiChannelDBMeterStyle", optHideMarkingText="true")
S("DefaultLighterHorizontalVUMeterStyle", "DefaultHorizontalVUMeterStyle", "CtrlMultiChannelDBMeterStyle", colChannelBack="EditorMedium")
S("ScrollbarStyle", "CornerRounding3Style", colFill="Transparent", colBorder="Transparent", colAltFill="PanelMedium", colAltBorder="PanelMedium")

section("Sliders, knobs, modulation")
DIAL = dict(optDrawBorder="false", colFill="PanelMedium", colFillHighlight="EditorMedium", colAltFill="PanelDarkest", colBorder="PanelDarkest", colAltBorder="PanelBrightest")
S("SliderStyle", realDisabledAlpha="0.4", **DIAL)
S("KnobStyle", **DIAL)
S("AltKnobStyle", "KnobStyle", colFill="PanelMediumAlpha03", colFillHighlight="EditorBrightest")
TM = dict(optDrawBorder="false", colBorder="Transparent", colModulationIndication="EditorAltBrightest", colModTrackFill="PanelMediumAlpha05",
          colFill="PanelAltDark", colAltFill="EditorMedium", colHandleBorder="PanelBrightest", colHandleFill="PanelDarkest",
          colModulationPos="EditorAltDarkest", colDepth="EditorAltBrightestAlpha05")
S("TransmodStyle", kind="CtrlTransmodStyle", optDrawModTrack="true", **TM)
S("TransmodSliderStyle", "TransmodStyle", "CtrlTransmodStyle", optModStrip="true")
S("MiniSequencerStyle", colFill="EditorAltMedium", colBorder="EditorAltMedium", colAltFill="EditorBrightest", colDisabledOverlay="PanelMediumAlpha05")

section("Tables")
TABLE = dict(optDrawColDividers="true", optDrawRowDividers="false", optColourAlternate="true", colColSelection="EditorAltBrightest",
             colRowSelection="EditorAltBrightest", colColDivider="PanelDark", colRowDivider="Transparent", colSelectedRowDivider="Transparent",
             realColDividerThickness="1", colFill="Transparent", colAltFill="PanelBright", colBorder="Transparent")
S("DefaultTableViewStyle", kind="CtrlTableViewPanelStyle", **TABLE)
S("DefaultTableViewHeaderStyle", optDrawBorder="true", colFill="PanelMedium", colBorder="Transparent", colAltBorder="PanelDark", colText="EditorDarkest", colAltText="PanelDarkest")
S("DefaultTableViewScrollStyle", colFill="Transparent", colBorder="Transparent")
S("InspectorTableStyle", kind="CtrlTableViewPanelStyle", optDrawBorder="false", optColourAlternate="false", colFill="PanelDark", colBorder="PanelDark",
  colColDivider="Transparent", colColSelection="Transparent", colRowDivider="PanelDarkest", colSelectedRowDivider="PanelDarkest",
  colRowSelection="PanelBrightest", colSecRowSelection="PanelAltMedium")
S("VSplitButtonStyle", "InspectorTableStyle", optDrawBorder="true", realBorderWidth="1", realCornerRounding=R_LARGE, colBorder="PanelDarkest", colAltFill="EditorAltBrightest",
  colText="PanelBrightest", font="SmallStd", enumTextHorizontalAlign="left", realTextOffset="4", realDisabledAlpha="0.7", **corners(tl=True))
S("VSplitStyle", colFill="EditorAltDarkest", colBorder="PanelBright", colAltFill="EditorAltBrightest", colAltBorder="PanelDark")
S("LinkPanelStyle", "LayerPanelStyle", colBorder="PanelDarkest")

section("Main tabs")
S("TabPanelStyle", "BackPanelStyle", optDrawBorder="true")
S("TabPanelHeaderStyle", "ShadowStyle", optDrawBorder="true", colFill="PanelDark", colBorder="PanelDark")
S("TabPanelHeaderLeftStyle", "TabPanelHeaderStyle", realCornerRounding=R_LARGE, **corners(tr=True))
S("TabPanelHeaderRightStyle", "TabPanelHeaderStyle", realCornerRounding=R_LARGE, **corners(tl=True))
S("TabButtonStyle", "CornerRounding3Style", optDrawBorder="true", optRoundBottomLeft="false", optRoundBottomRight="false", font="SmallBold",
  colFill="Transparent", colBorder="Transparent", colText="PanelBrightest", colAltFill="PanelBrightest", colAltBorder="PanelBrightest", colAltText="PanelDarkest")

section("Browser")
S("BrowserNavigationButtonStyle", "DefaultButtonStyle", font="ExLargeBold")
S("BrowserSpinnerStyle", realCornerRounding="0", realBorderWidth="3", colFill="Transparent", colBorder="Transparent", colAltFill="EditorAltBrightest", colAltBorder="EditorAltBrightest")
S("BrowserPathNavStyle", optDrawBorder="false", colFill="Transparent", colBorder="PanelMedium", colText="EditorDarkest")
S("BrowserListViewStyle", "DefaultTableViewStyle", "CtrlTableViewPanelStyle")
S("BrowserSourceListStyle", "BrowserListViewStyle", "CtrlTableViewPanelStyle", optColourAlternate="false")
S("BrowserListViewHeaderStyle", "DefaultTableViewHeaderStyle")
S("BrowserListItemStyle", font="Standard", enumTextHorizontalAlign="center", enumTextVerticalAlign="center", colBorder="Transparent", colText="EditorDarkest", colAltFill="EditorAltDarkest")
S("BrowserSourceListItemStyle", "BrowserListItemStyle", enumTextHorizontalAlign="left")

section("Header bar")
HDR_TEXT = dict(optDrawBorder="false", colFill="Transparent", colText="PanelBrightest", font="SmallStd")
S("HeaderBarConsoleStyle", "CornerRounding3Style", optDrawBorder="false", realBorderWidth="0", colFill="PanelMediumAlpha03", colBorder="Transparent")
S("HeaderBarIndicatorStyle", "ShadowStyle", font="Tiny", colText="PanelMediumAlpha03", colAltText="PanelBrightest", **CLEAR)
S("HeaderBarIconIndicatorStyle", "HeaderBarIndicatorStyle", font="StandardIcons", enumDisabledDrawMode="NormalDrawing")
S("HeaderBarIndicatorErrorStyle", "HeaderBarIndicatorStyle", colText="PanelSpark", colAltText="PanelSpark")
S("HeaderBarConsoleTextStyle", "ShadowStyle", enumTextHorizontalAlign="left", **HDR_TEXT)
S("HeaderBarConsoleCenterTextStyle", "HeaderBarConsoleTextStyle", enumTextHorizontalAlign="center")
S("HeaderBarConsoleRightTextStyle", "HeaderBarConsoleTextStyle", enumTextHorizontalAlign="right")
S("HeaderBarPresetStyle", "HeaderBarConsoleTextStyle", colText="EditorAltBrightest")
S("HeaderBarMenuButtonStyle", "ShadowStyle", font="Standard", enumTextHorizontalAlign="left", realTextOffset="2", colText="PanelMedium", colAltText="EditorAltBrightest", **CLEAR)
S("HeaderBarMenuDropButtonStyle", "HeaderBarMenuButtonStyle", font="Small", realTextOffset="0")
HDR_BTN = dict(optDrawBorder="false", realBorderWidth="0", colBorder="Transparent")
S("HeaderBarButtonStyle", "CornerRoundingStyle", font="SmallStd", enumTextShortenAlgorithm="end", colFill="PanelMediumAlpha03", colText="PanelBrightest",
  colAltFill="EditorAltBrightest", colAltBorder="EditorAltBrightest", colAltText="PanelDarkest", **HDR_BTN)
S("HeaderBarIconButtonStyle", "HeaderBarButtonStyle", font="ExExLargeIcons")
S("HeaderBarPopupButtonStyle", "HeaderBarButtonStyle", enumTextHorizontalAlign="left")
S("HeaderBarUndoRedoDropStyle", "HeaderBarButtonStyle", optRoundTopLeft="false", optRoundBottomLeft="false", realTextOffset="0", font="Tiny")
S("RecordButtonStyle", "CornerRoundingStyle", font="ExExLargeIcons", colFill="PanelSparkAlpha05", colText="EditorDarkest", colAltFill="PanelSpark", colAltBorder="PanelSpark", colAltText="PanelDarkest", **HDR_BTN)
S("PlayButtonStyle", "CornerRoundingStyle", font="ExExLargeIcons", colFill="EditorAltBrightestAlpha05", colText="EditorDarkest", colAltFill="EditorAltBrightest", colAltBorder="EditorAltBrightest", colAltText="PanelDarkest", **HDR_BTN)
S("TransmodButtonStyle", "HeaderBarButtonStyle", realCornerRounding="0")
S("TransmodButtonStyleHighlight", "TransmodButtonStyle", optDrawBorder="true", realBorderWidth="2", colBorder="EditorAltBrightest", colAltBorder="EditorAltBrightest")
S("TransmodFlashButtonStyle", "TransmodButtonStyleHighlight", colFill="EditorAltBrightest")

section("Pattern editor")
S("TrackStyle", kind="PatternEditorTrackStyle", font="SmallIcons", colPosition="EditorBrightestAlpha02", colOverlay="PanelMediumAlpha05", colGraphOverlay="MuteSpark",
  colMenuOverlay="EditorBrightest", colLockedOverlay="PanelMediumAlpha05", colStep="PanelDarkest", colSelected="EditorBrightest", colDivider="PanelDark")
S("GraphStyle", "TrackStyle", "PatternEditorTrackStyle", colStep="PanelDark", colDivider="PanelDarkest")
S("PatternTimelineStyle", font="SmallBold", colFill="Transparent", colBorder="PanelMedium", colText="PanelBrightest")
S("TrackSelectedStyle", colFill="PanelBright", colBorder="PanelBright", colAltBorder="PanelMediumAlpha03")
S("TrackNotSelectedStyle", colFill="PanelBrightest", colBorder="PanelBrightest", colAltBorder="PanelMediumAlpha03")
TRACK_BTN = dict(optDrawShadow="false", font="SmallStdBold", colText="EditorDarkest", **CLEAR)
S("TrackMuteStyle", "DefaultButtonStyle", colAltText="MuteSpark", **TRACK_BTN)
S("TrackSoloStyle", "DefaultButtonStyle", colAltText="SoloSpark", **TRACK_BTN)
S("PatternBackPanelStyle", kind="PatternEditorBackingPanelStyle", font="ExExExLargeBold", colText="EditorDarkest", colGridBar="PanelMedium", colGridBeat="PanelMediumAlpha03",
  colPowerOverlay="EditorDarkest", colSelectedTrack="PanelBright", colFill="PanelBrightest", colAltFill="PanelBright", colPosition="EditorBrightestAlpha02")
S("PatternTrackMarkerStyle", None, colFill="PanelDarkest", colAltFill="EditorAltBrightest", colBorder="Transparent")

section("Wave display")
S("WaveDisplayStyle", kind="WaveDisplayStyle", enumDisabledDrawMode="NormalDrawing", font="Small", fontTimeline="Small",
  colFill="PanelGradientStart", colAltFill="PanelGradientEnd", colTimelineBackground="PanelDark", colTimelineText="PanelBright",
  colTimelineMarkers="PanelBright", colCenterLine="PanelDark", colLine="PanelDark", colLineDisabled="PanelMedium", colLineLooping="EditorMedium",
  colStartMarker="PanelBrightest", colEndMarker="PanelBrightest", colLoopStartMarker="EditorBrightest", colLoopEndMarker="EditorBrightest",
  colPlaybackMarker="EditorMedium", colText="PanelBrightest", colEnvelopeBack="EditorBrightest", colEnvelopeLine="EditorBrightest",
  colEnvelopeGrab="EditorBrightest")
S("WaveDisplayZoomSliderStyle", "ScrollbarStyle", colFill="EditorMedium", colBorder="Transparent")
S("WaveDisplayZoomSliderWaveStyle", "WaveDisplayStyle", "WaveDisplayStyle", colLine="PanelBright")
ZOOM = dict(optDrawShadow="false", colText="PanelMedium", colAltText="EditorAltBrightest", **CLEAR)
S("WaveDisplayZoomButtonStyle", "DefaultButtonStyle", font="StandardBold", enumDisabledDrawMode="ColourOverlay", colDisabledOverlay="PanelDarkAlpha07", realDisabledAlpha="0.2", **ZOOM)
S("WaveDisplayZoomIconButtonStyle", "DefaultButtonStyle", font="ExLargeIcons", **ZOOM)
S("WavePanelBackingStyle", "DarkPanelStyle", realCornerRounding=R_SMALL)

section("Engine selectors")
S("EngineSelectorStyle", "PlayButtonStyle", font="SmallStdBold", enumTextShortenAlgorithm="end", realCornerRounding="20")
S("EngineSelectorStateStyle", "PlayButtonStyle", optDrawBorder="true", realBorderWidth="2", realCornerRounding="24", colFill="Transparent", colAltFill="Transparent",
  colBorder="EditorAltBrightestAlpha05", colAltBorder="EditorAltBrightest")
S("EngineSelectorOverlayStyle", "CornerRoundingStyle", optDrawBorder="false", realCornerRounding="20", enumDisabledDrawMode="Normal",
  colFill="Transparent", colBorder="Transparent", colAltBorder="Transparent", colAltFill="PanelBrightestAlpha05")
S("EngineSelectorLabelStyle", "DarkTextInvisibleEditBoxStyle", optDrawBorder="false", colFill="Transparent", font="SmallStdBold", enumTextHorizontalAlign="center", enumTextShortenAlgorithm="end")
S("EngineSelectorButtonStyle", "EngineSelectorStyle", enumTextHorizontalAlign="center", realTextOffset="0", realCornerRounding="7", colText="EditorDarkest", colAltFill="EditorAltBrightest", colAltText="PanelDarkest")
S("EngineSelectorSButtonStyle", "EngineSelectorButtonStyle", colAltFill="SoloSpark")
S("EngineSelectorMButtonStyle", "EngineSelectorButtonStyle", colAltFill="MuteSpark")
S("EngineSelectorPPButtonStyle", "EngineSelectorButtonStyle", font="SmallIcons")
INDI = dict(optDrawShadow="false", optDrawBorder="false", realCornerRounding=R_SMALL, colFill="Transparent")
S("EngineSelectorMuteIndicatorStyle", "CornerRoundingStyle", colAltFill="MuteSpark", **INDI)
S("EngineSelectorSoloIndicatorStyle", "CornerRoundingStyle", colAltFill="SoloSpark", **INDI)

section("Pads")
S("PadStyle", "CornerRounding5Style", realCornerRounding=5, optDrawBorder="false", realBorderWidth="1", realDisabledAlpha="0.5", font="StandardBold", enumTextShortenAlgorithm="middle",
  colFill="EditorMedium", colBorder="EditorMedium", colText="PanelBrightest", colAltFill="PanelBrightest")
S("PadSelectedStyle", "PadStyle", colFill="EditorAltBrightest", colBorder="EditorAltBrightest")
S("PadOverlayStyle", "CornerRounding5Style", realCornerRounding=5, optDrawBorder="false", realDisabledAlpha="0.2", colFill="PanelBright", colAltFill="PanelBright")
RING = dict(optDrawBorder="true", realBorderWidth="2", colBorder="PanelBrightest", colAltBorder="PanelBrightest")
S("PadOnStyle", "PadStyle", colFill="EditorAltMedium", colBorder="EditorAltMedium")
S("PadOnSelectedStyle", "PadStyle", colFill="EditorAltMedium", **RING)
S("PadOffStyle", "PadStyle")
S("PadOffSelectedStyle", "PadStyle", **RING)
S("PadAccentStyle", "PadStyle", colFill="EditorAltBrightest", colBorder="EditorAltBrightest")
S("PadAccentSelectedStyle", "PadStyle", colFill="EditorAltBrightest", **RING)
S("PadNameLabelStyle", "InvisibleStyle", enumDisabledDrawMode="NormalDrawing", enumTextShortenAlgorithm="end", font="SmallStdBold", colText="PanelBrightest")
S("PadNameLabelSelectedStyle", "PadNameLabelStyle", colText="EditorDarkest")
S("PadStepNameLabelStyle", "PadNameLabelStyle", font="Small", colText="PanelBrightest")
S("PadStepNameLabelSelectedStyle", "PadStepNameLabelStyle", colText="EditorDarkest")
# Empty slots: a flat 30 % square (an alpha border over the alpha fill
# would read as a darker outlined box).
S("PadLayerIndicatorStyle", "ShadowStyle", optDrawBorder="true", enumDisabledDrawMode="NormalDrawing", colFill="EditorDarkestAlpha03", colBorder="Transparent",
  colAltFill="EditorAltBrightest", colAltBorder="EditorAltBrightest")
S("PadLayerIndicatorSelectedStyle", "PadLayerIndicatorStyle", colFill="EditorAltDarkestAlpha075", colBorder="EditorAltDarkest", colAltFill="EditorDarkest", colAltBorder="EditorDarkest")
S("PadLayerMutedIndicatorStyle", "PadLayerIndicatorStyle", colAltFill="MuteSpark", colAltBorder="MuteSpark")
S("PadLayerSoloedIndicatorStyle", "PadLayerIndicatorStyle", colAltFill="SoloSpark", colAltBorder="SoloSpark")
S("PadLayerMutedSoloedIndicatorStyle", "PadLayerIndicatorStyle", colAltFill="Orange", colAltBorder="Orange")
S("PadLockIndicatorStyle", "CornerRoundingStyle", optDrawShadow="false", optDrawBorder="false", font="LargeIcons", colFill="Transparent", colAltFill="Transparent",
  colText="Transparent", colAltText="PanelBrightest")

section("Scenes")
S("SceneButtonStyle", "PadStyle", colText="EditorDarkest")
S("SceneSelectedStyle", "PadSelectedStyle", colText="EditorDarkest", enumTextHorizontalAlign="center", enumTextShortenAlgorithm="end")
S("SceneNameLabelStyle", "PadNameLabelStyle", font="LargeBold", colText="PanelBrightest", enumTextHorizontalAlign="center", enumTextShortenAlgorithm="end")
S("SceneSelectedNameLabelStyle", "PadNameLabelStyle", font="LargeBold", colText="EditorDarkest")
S("SceneUsedStyle", "PadSelectedStyle", colFill="EditorBrightest", colBorder="EditorBrightest", colText="EditorDarkest")
S("SceneSmallButtonStyle", "PadNameLabelStyle", optDrawShadow="false", optDrawBorder="false", realTextOffset="0", font="SmallStdBold",
  colText="PanelBrightest", colAltText="EditorDarkest", colFill="Transparent", colAltFill="Transparent", colBorder="Transparent")
S("SceneIconButtonStyle", "SceneSmallButtonStyle", font="ExxLargeIcons")
S("SceneSelectionButtonStyle", "SceneSmallButtonStyle")
S("SceneSelectedIconButtonStyle", "SceneSmallButtonStyle", font="ExxLargeIcons", colText="PanelDarkest")
S("SceneActivityLabelStyle", "InvisibleStyle", enumDisabledDrawMode="NormalDrawing", font="SuperSized", colText="EditorDarkest", colBorder="Pink")

section("Mixer")
S("MixerChannelOddStyle", colFill="PanelBrightest", colBorder="PanelBrightest")
S("MixerChannelEvenStyle", colFill="PanelBrightest", colBorder="PanelBrightest")
S("FXIndicatorStyle", "CornerRoundingStyle", optDrawShadow="false", realCornerRounding="0", enumDisabledDrawMode="NormalDrawing",
  colFill="Transparent", colBorder="EditorAltBrightestAlpha05", colAltFill="EditorAltBrightest", colAltBorder="EditorAltBrightest")
TITLE = dict(optDrawShadow="false", optDrawBorder="true", enumTextShortenAlgorithm="end", font="Standard")
S("MixerChannelEditTitleStyle", colFill="PanelMedium", colBorder="PanelMedium", colText="EditorDarkest", **TITLE)
S("MixerChannelEditTitleSelectedStyle", colFill="EditorAltBrightest", colBorder="EditorAltBrightest", colText="EditorDarkest", **TITLE)
S("MixerChannelEditTitleSubSelStyle", colFill="EditorAltMedium", colBorder="EditorAltMedium", colText="EditorBrightest", **TITLE)

section("Song")
S("SongPartStyle", kind="SongPartStyle", realCornerRounding="7", font="Small", colBorder="PanelDarkest", colAltBorder="PanelBright", colFill="PanelMedium",
  colAltFill="EditorAltBrightest", colText="PanelDarkest", colAltText="PanelDarkest", colPart="PanelMedium", colSelected="EditorBrightest",
  colRecording="PanelSpark", colRetro="PanelAltSpark", colEmpty="EditorBrightestAlpha02")
S("SongTimelineStyle", "PatternTimelineStyle")
S("SongPanelStyle", kind="SongPanelStyle", colRubberBand="PanelDarkest", colPosition="PanelDarkest", colInsertMarker="PanelDarkest", colDrawMarker="PanelDarkest",
  colLoopHost="EditorBrightestAlpha02", colLoopInternal="EditorAltBrightestAlpha05", colLoopExternal="PanelMediumAlpha05")
S("SongPanelBlackoutPanelStyle", colFill="0, 0, 0, 50")
S("SongBodyPanelStyle", "TrackNotSelectedStyle", colFill="Transparent", colBorder="PanelMediumAlpha03")
S("SongTrackPanelStyle0", "TrackNotSelectedStyle", colBorder="PanelMedium")
S("SongTrackPanelStyle1", "TrackNotSelectedStyle", colBorder="PanelMedium")
S("SongTrackPanelSelectedStyle", "TrackSelectedStyle", colBorder="PanelMedium")
S("SongTrackPanelPreviewingStyle", None, colFill="EditorAltMedium")


# ---------------------------------------------------------------- output

def _q(v):
    return str(v).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def colours_xml():
    out = ["<root>", "    <!-- Dreist palette. Generated by scripts/uigen/theme.py. -->"]
    for name, v in COLOURS:
        if isinstance(v, tuple):
            base, mod = v
            out.append(f'    <VColour name="{name}" colour="{base}"' + (f' modifier="{mod}"' if mod else "") + " />")
        else:
            out.append(f'    <VColour name="{name}" colour="{v}" />')
    out.append("</root>\n")
    return "\n".join(out)


def fonts_xml():
    out = ["<root>", "    <!-- Dreist type scale. Generated by scripts/uigen/theme.py. -->"]
    for name, fam, size, bold in FONTS:
        out.append(f'    <VFont name="{name}" fontName="{fam}" fontSize="{size}"' + (' weight="bold"' if bold else "") + " />")
    out.append("</root>\n")
    return "\n".join(out)


def styles_xml():
    out = ["<root>", "    <!-- Dreist control styles. Generated by scripts/uigen/theme.py. -->"]
    for kind, name, parent, attrs in STYLES:
        if kind == "#":
            out.append(f"\n    <!-- {name} -->")
            continue
        a = [f'name="{name}"'] + ([f'parentStyle0="{parent}"'] if parent else []) + [f'{k}="{_q(v)}"' for k, v in attrs.items()]
        out.append(f"    <{kind} " + " ".join(a) + " />")
    out.append("</root>\n")
    return "\n".join(out)


def gltinfo_xml():
    return """<root>
    <vector name="defaultStyles">
        <VString string="/Styles/Dreist.style/Colours.stylesheet" />
        <VString string="/Styles/Dreist.style/Fonts.stylesheet" />
        <VString string="/Styles/Dreist.style/Styles.stylesheet" />
    </vector>
</root>
"""


# Alternative themes: colour overrides on top of the default.
THEMES = {
    "Ember": [
        ("EditorBrightest", rgb((222, 160, 110))),
        ("EditorAltDarkest", rgb((92, 58, 38))),
        ("EditorAltMedium", rgb((140, 86, 52))),
        ("EditorAltBrightest", rgb((255, 178, 102))),
        ("PanelGradientStart", rgb((230, 224, 218))),
        ("PanelGradientEnd", rgb((204, 192, 182))),
    ],
}


def theme_xml(name, colours):
    out = ["<root>", f"    <!-- Dreist theme \"{name}\". Generated by scripts/uigen/theme.py. -->"]
    out += [f'    <VColour name="{n}" colour="{v}" />' for n, v in colours]
    # Derived colours follow their (overridden) base.
    out += [f'    <VColour name="{n}" colour="{b}"' + (f' modifier="{m}"' if m else "") + " />" for n, v in COLOURS if isinstance(v, tuple) for b, m in [v]]
    out.append("</root>\n")
    return "\n".join(out)


def outputs():
    return {
        **{f"Skin/Styles/{n}.style/Colours.stylesheet": theme_xml(n, c).encode() for n, c in THEMES.items()},
        "Skin/project.gltinfo": gltinfo_xml().encode(),
        "Skin/Styles/Dreist.style/Colours.stylesheet": colours_xml().encode(),
        "Skin/Styles/Dreist.style/Fonts.stylesheet": fonts_xml().encode(),
        "Skin/Styles/Dreist.style/Styles.stylesheet": styles_xml().encode(),
    }
