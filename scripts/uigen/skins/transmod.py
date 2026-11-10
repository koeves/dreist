"""Transmod: the modulator panels, the empty slot, the source bar and
the trigger dialog (Transmod/*.skin).

A modulator panel is a folding card: a header (menu at the left, the
retrigger button at the right, any header switches before it), one row of
knobs, then the modulator's graph filling the rest.  Knob names
(Control0..) follow the modulator's parameter order in
dreist_formats::params::ModulatorType::params.
"""

from . import N, skin

W = 240             # the narrow cards (LFOs, sample and hold, maths, sequencer)
WIDE = 300          # the wide ones (AD envelope, constant, bouncing ball)
H = 135
HEAD = 20
KNOB = 40
PITCH = 48          # knob spacing in the row
ROW_H = 115         # the knob row's labeller runs down to the card's foot


def card(title, h, knobs, header=(), extra=(), graph="TransmodDisplayPanel", graph_name="DisplayPanel", w=W, row=(HEAD, ROW_H, 5),
         graph_h=50):
    kids = [N("Button", "Options", (2, 3, 16, 16), style="SmallTextButtonStyle", text="▼", optIsMomentary=True)]
    x = w - 18
    kids.append(N("Button", "Trigger", (x, 2, 16, 16), pin="r", style="ExxLargeIconButtonStyle", text="",
                  optIsMomentary=True, displayName="Retrigger"))
    for name, bw, attrs in header:
        x -= bw + 2
        kids.append(N("Button", name, (x, 2, bw, 16), pin="r", **attrs))
    ry, rh, ky = row
    lab = [N("TransmodKnob", n, (i * PITCH, ky, KNOB, KNOB), displayName=cap, style="TransmodStyle")
           for i, (n, cap) in enumerate(knobs)]
    kids.append(N("Labeller", None, (0, ry, w, rh), pin="lr", kids=lab, style="SmallControlLabellerStyle",
                  enumTextPosition="Below", intTextOffset=-2))
    kids.extend(extra)
    g = dict(style="TransmodPlotStyle" if graph else "MiniSequencerStyle")
    if graph:
        g["overloadClass"] = graph
    kids.append(N("Panel", graph_name, (0, 80, w, graph_h), pin="lrtb", **g))
    return N("CollapsePanel", None, (0, 0, w, h), pin="R", kids=kids, displayName=title,
             iconicTarget="ARTop", style="TransmodCollapsePanelStyle")


SYNC = ("Control0", 30, dict(style="DefaultButtonStyle", text="Sync", displayName="Tempo Sync"))


def panels():
    out = {}
    out["LFO"] = card("LFO", H, [("Control1", "Freq"), ("Control3", "Phase"), ("Control4", "Level")], header=[SYNC],
                      extra=[N("PopupButton", "Control2", (W - 85, HEAD + 15, 85, 20), pin="r",
                               style="DefaultPopupButtonStyle", displayName="Shape")])
    out["MorphingLFO"] = card("MORPHING LFO", H, [("Control1", "Freq"), ("Control3", "Phase"), ("Control2", "Shape"),
                                               ("Control4", "Swing"), ("Control5", "Level")], header=[SYNC])
    out["SampleAndHold"] = card("SAMPLE AND HOLD", H, [("Control1", "Freq"), ("Control3", "Phase"), ("Control2", "Slew"),
                                                     ("Control4", "Level")], header=[SYNC])
    out["ADEnvelope"] = card("AD ENVELOPE", H, [("Control0", "Attack"), ("Control2", "A Curve"), ("Control1", "Decay"),
                                             ("Control3", "D Curve"), ("Control4", "Level")], w=WIDE)
    out["BouncingBall"] = card("BOUNCING BALL", H, [("Control0", "Gravity"), ("Control1", "Speed"), ("Control2", "Level")], w=WIDE)
    out["Constant"] = card("CONSTANT", 80, [("Control0", "Constant"), ("Control1", "Level")], graph=None, w=WIDE, row=(HEAD, 60, 5))
    # Constant has no graph: drop the empty panel the card adds.
    out["Constant"].kids.pop()

    # Maths: operator over two sources, gain at the right.
    PW = W - 50
    ops = [N("PopupButton", "Control0", (0, 28, PW, 20), pin="lr", style="DefaultPopupButtonStyle",
             displayName="Argument"),
           N("Panel", None, (0, 52, PW, 20), pin="lr", style="InvisibleStyle", kids=[
               N("PopupButton", "Control1", (0, 0, PW // 2 - 2, 20), style="DefaultPopupButtonStyle",
                 displayName="Source 1", ARLeft="FNear 0.0000", ARRight="Relative 0.4900"),
               N("PopupButton", "Control2", (PW // 2 + 2, 0, PW // 2 - 2, 20),
                 style="DefaultPopupButtonStyle", displayName="Source 2", ARLeft="Relative 0.5100", ARRight="FNear 0.0000")])]
    maths = card("MATHS", H, [], extra=ops)
    lab = maths.kids[2]
    lab.rect = (W - 44, HEAD + 1, KNOB, 60)
    lab.pin = "r"
    lab.add(N("TransmodKnob", "Control3", (0, 7, KNOB, KNOB), displayName="Level", style="TransmodStyle"))
    out["Math"] = maths

    seq = card("MINI SEQUENCER", 150, [("Control1", "Steps"), ("Control0", "Rate"), ("Control2", "Slew"), ("Control22", "Level")],
               header=[("Control5", 16, dict(style="DefaultButtonStyle", text="TR", displayName="Advance one step per trigger of the selected pads")),
                       ("OptionMenu", 16, dict(style="ExxLargeIconButtonStyle", text="", optIsMomentary=True,
                                               displayName="Step shapes"))],
               extra=[N("Button", "Control3", (W - 50, 28, 50, 20), pin="r", style="DefaultButtonStyle", text="Drunk",
                        displayName="Random walk: steps may move back as well as forward"),
                      N("Button", "Control4", (W - 50, 50, 50, 20), pin="r", style="DefaultButtonStyle", text="Reverse",
                        displayName="Play the steps backwards")],
               graph=None, graph_name="SeqGridRect", row=(HEAD + 2, 55, 3), graph_h=68)
    out["Sequencer"] = seq
    return out


def empty_slot():
    return N("Panel", None, (0, 0, 400, 24), pin="lr", style="InvisibleStyle", kids=[
        N("Button", "TypePopup", (2, 2, 16, 16), pin="l", style="ExxLargeIconButtonStyle", text="",
          optIsMomentary=True, displayName="Add a modulator"),
        N("Label", "SlotID", (20, 0, 375, 20), pin="lr", style="InvisibleEditBoxStyle"),
        N("Panel", "Divider", (25, 23, 350, 1), pin="lrtb", style="LightDividerStyle"),
    ])


def side_panel():
    return N("Panel", None, (0, 0, 400, 750), pin="lrtb", style="SidebarPanelStyle", kids=[
        N("ScrollContainer", "ScrollView", (5, 5, 390, 740), pin="lrtb", style="InvisibleStyle", zorder=500,
          HScrollBarStyle="ScrollbarStyle", ScrollViewStyle="InvisibleStyle", VScrollBarStyle="ScrollbarStyle",
          intScrollBarDim=12, optOverlay=False, optShowHBar=False),
    ])


SOURCES = (["A-En", "F-En", "Vel", "Rnd"] + [f"S {i}" for i in range(1, 17)] + [f"M {i}" for i in range(1, 5)]
           + ["Mod", "Pch", "Pres", "Tprt"])


def source_bar():
    """The modulation source buttons plus the four macro knobs."""
    bw, gap = 30, 2
    W, H = 1150, 35
    box = dict(style="InvisibleStyle", optIsVertical=False, intLeftSpacing=0, intRightSpacing=0,
               intTopSpacing=0, intBottomSpacing=0)
    srcs = [N("Button", f"Src{i + 1}", (i * (bw + gap), 0, bw, 20), style="TransmodButtonStyle", text=t)
            for i, t in enumerate(SOURCES)]
    flash = [N("Button", f"FlashSrc{i + 1}", (i * (bw + gap), 0, bw, 20), style="TransmodFlashButtonStyle")
             for i in range(len(SOURCES))]
    left = N("Panel", None, (0, 0, 960, H), pin="lrtb", style="InvisibleStyle", kids=[
        N("Button", "Src0", (0, 7, 40, 20), pin="m", style="TransmodButtonStyle", text="Src",
          displayName="Edit base values"),
        N("LayoutBox", None, (45, 7, 915, 20), pin="lrm", kids=srcs, **box),
        N("LayoutBox", None, (45, 28, 915, 3), pin="lr", kids=flash, **box),
    ])
    macros = []
    for i in range(4):
        macros.append(N("Labeller", None, (i * 45, 0, 43, H), style="SmallControlLabellerStyle", enumTextPosition="Below",
                        intTextOffset=-1, kids=[
                            N("Knob", f"Macro{i}", (11, 1, 20, 20), pin="ct", displayName=f"Macro {i + 1}",
                              style="AltKnobStyle", realDialThickness=0.3)]))
    # From x 960 (not 970) the four macros (178 px) still fit in the
    # smallest window, where this panel is 1140 wide: the last one lost
    # 8 px there.
    right = N("LayoutBox", None, (960, 0, 190, H), pin="lrtb", kids=macros, **box)
    return N("Panel", "TransmodSelectPanel", (0, 0, W, H), pin="lrtb", style="InvisibleStyle", kids=[left, right])


def trigger_dialog():
    """Which events restart a modulator."""
    def check(name, x, tip):
        return N("Button", name, (x, 4, 14, 14), displayName=tip, style="DefaultCheckboxButtonStyle")
    rows = N("Labeller", None, (20, 6, 320, 436), pin="lrtb", displayName="None", enumTextPosition="Above",
             style="DialogPanelLeftLabellerStyle", kids=[
                 N("Labeller", None, (0, 0, 320, 22), pin="lrt", enumTextPosition="Right", intTextOffset=6,
                   style="DialogPanelLeftLabellerStyle", kids=[check("TStart", 0, "Reset at transport start")]),
                 N("Labeller", None, (0, 34, 320, 24), pin="lr", displayName="Reset on engine pattern change",
                   enumTextPosition="Right", intTextOffset=6, style="DialogPanelLeftLabellerStyle",
                   kids=[check(f"E{i + 1}", i * 32, str(i + 1)) for i in range(8)]),
                 N("Labeller", None, (0, 66, 320, 28), pin="lrt", enumTextPosition="Right", intTextOffset=6,
                   style="DialogPanelLeftLabellerStyle", kids=[
                       N("PopupButton", "ShowEng", (0, 4, 56, 18), displayName="Engine", style="DefaultPopupButtonStyle")]),
                 N("Matrix", "Matrix", (0, 116, 320, 320), pin="lrtb", displayName="Pads That Trigger Modulator",
                   intNumberOfCols=4, intNumberOfRows=16, optLayoutFromTop=False, style="InvisibleStyle"),
             ])
    return N("AnchorPanel", "Anchor", (0, 0, 350, 450), enumAnchorEdge="ARLeft", intAnchorPoint=160,
             style="TriggerDialogPanelStyle", kids=[rows])


def outputs():
    files = {f"Skin/Transmod/{k}.skin": skin(v) for k, v in panels().items()}
    files["Skin/Transmod/EmptySlot.skin"] = skin(empty_slot())
    files["Skin/Transmod/TransmodPanel.skin"] = skin(side_panel())
    files["Skin/Transmod/TransmodButtonPanel.skin"] = skin(source_bar())
    files["Skin/Transmod/TriggerPanel.skin"] = skin(trigger_dialog())
    return files
