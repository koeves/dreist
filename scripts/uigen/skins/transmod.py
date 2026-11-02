"""Transmod: the modulator panels, the empty slot, the source bar and
the trigger dialog (Transmod/*.skin).

A modulator panel is a folding card: a header (menu at the left, the
retrigger button at the right, any header switches before it), one row of
knobs, then the modulator's graph filling the rest.  Knob names
(Control0..) follow the modulator's parameter order in
geist_formats::params::ModulatorType::params.
"""

from . import N, skin

W = 260
HEAD = 20
KNOB = 36
PITCH = 46          # knob spacing in the row
ROW_H = 58          # knob + caption


def card(title, h, knobs, header=(), extra=(), graph="TransmodDisplayPanel", graph_name="DisplayPanel"):
    kids = [N("Button", "Options", (3, 3, 15, 15), style="SmallTextButtonStyle", text="▾", optIsMomentary=True)]
    x = W - 19
    kids.append(N("Button", "Trigger", (x, 2, 16, 16), pin="r", style="ExxLargeIconButtonStyle", text="",
                  optIsMomentary=True, displayName="Retrigger"))
    for name, w, attrs in header:
        x -= w + 3
        kids.append(N("Button", name, (x, 2, w, 16), pin="r", **attrs))
    lab = [N("TransmodKnob", n, (6 + i * PITCH, 4, KNOB, KNOB), displayName=cap, style="TransmodStyle")
           for i, (n, cap) in enumerate(knobs)]
    kids.append(N("Labeller", None, (0, HEAD, W, ROW_H), pin="lr", kids=lab, style="SmallControlLabellerStyle",
                  enumTextPosition="Below", intTextOffset=-1))
    kids.extend(extra)
    gy = HEAD + ROW_H + 2
    g = dict(style="TransmodPlotStyle" if graph else "MiniSequencerStyle")
    if graph:
        g["overloadClass"] = graph
    kids.append(N("Panel", graph_name, (4, gy, W - 8, h - gy - 4), pin="lrtb", **g))
    return N("CollapsePanel", None, (0, 0, W, h), pin="r", kids=kids, displayName=title,
             iconicTarget="ARTop", style="TransmodCollapsePanelStyle")


SYNC = ("Control0", 34, dict(style="DefaultButtonStyle", text="Sync", displayName="Tempo Sync"))


def panels():
    out = {}
    out["LFO"] = card("LFO", 130, [("Control1", "Rate"), ("Control3", "Phase"), ("Control4", "Level")], header=[SYNC],
                      extra=[N("PopupButton", "Control2", (W - 90, HEAD + 12, 84, 18), pin="r",
                               style="DefaultPopupButtonStyle", displayName="Wave")])
    out["MorphingLFO"] = card("MORPH LFO", 130, [("Control1", "Rate"), ("Control3", "Phase"), ("Control2", "Morph"),
                                                 ("Control4", "Swing"), ("Control5", "Level")], header=[SYNC])
    out["SampleAndHold"] = card("SAMPLE + HOLD", 130, [("Control1", "Rate"), ("Control3", "Phase"), ("Control2", "Glide"),
                                                       ("Control4", "Level")], header=[SYNC])
    out["ADEnvelope"] = card("ENVELOPE", 130, [("Control0", "Attack"), ("Control2", "A Shape"), ("Control1", "Decay"),
                                               ("Control3", "D Shape"), ("Control4", "Level")])
    out["BouncingBall"] = card("BOUNCE", 130, [("Control0", "Gravity"), ("Control1", "Speed"), ("Control2", "Level")])
    out["Constant"] = card("CONSTANT", 80, [("Control0", "Value"), ("Control1", "Level")], graph=None)
    # Constant has no graph: drop the empty panel the card adds.
    out["Constant"].kids.pop()

    # Maths: operator over two sources, gain at the right.
    ops = [N("PopupButton", "Control0", (6, HEAD + 6, W - 64, 18), pin="lr", style="DefaultPopupButtonStyle",
             displayName="Operation"),
           N("Panel", None, (6, HEAD + 30, W - 64, 18), pin="lr", style="InvisibleStyle", kids=[
               N("PopupButton", "Control1", (0, 0, (W - 64) // 2 - 2, 18), style="DefaultPopupButtonStyle",
                 displayName="Input A", ARLeft="FNear 0.0000", ARRight="Relative 0.4900"),
               N("PopupButton", "Control2", ((W - 64) // 2 + 2, 0, (W - 64) // 2 - 2, 18), 
                 style="DefaultPopupButtonStyle", displayName="Input B", ARLeft="Relative 0.5100", ARRight="FNear 0.0000")])]
    maths = card("MATHS", 130, [], extra=ops)
    lab = maths.kids[2]
    lab.rect = (W - 52, HEAD, 48, ROW_H)
    lab.pin = "r"
    lab.add(N("TransmodKnob", "Control3", (6, 4, KNOB, KNOB), displayName="Level", style="TransmodStyle"))
    out["Math"] = maths

    seq = card("STEP SEQ", 150, [("Control1", "Steps"), ("Control0", "Rate"), ("Control2", "Glide"), ("Control22", "Level")],
               header=[("Control5", 26, dict(style="DefaultButtonStyle", text="Trig", displayName="Steps send triggers")),
                       ("OptionMenu", 16, dict(style="ExxLargeIconButtonStyle", text="", optIsMomentary=True,
                                               displayName="Step shapes"))],
               extra=[N("Button", "Control3", (W - 56, HEAD + 6, 50, 18), pin="r", style="DefaultButtonStyle", text="Drunk",
                        displayName="Random walk: steps may move back as well as forward"),
                      N("Button", "Control4", (W - 56, HEAD + 28, 50, 18), pin="r", style="DefaultButtonStyle", text="Reverse",
                        displayName="Play the steps backwards")],
               graph=None, graph_name="SeqGridRect")
    out["Sequencer"] = seq
    return out


def empty_slot():
    return N("Panel", None, (0, 0, 400, 24), pin="lr", style="InvisibleStyle", kids=[
        N("Button", "TypePopup", (3, 3, 16, 16), pin="l", style="ExxLargeIconButtonStyle", text="",
          optIsMomentary=True, displayName="Add a modulator"),
        N("Label", "SlotID", (24, 2, 370, 18), pin="lr", style="InvisibleEditBoxStyle"),
        N("Panel", "Divider", (24, 23, 352, 1), pin="lrtb", style="LightDividerStyle"),
    ])


def side_panel():
    return N("Panel", None, (0, 0, 400, 750), pin="lrtb", style="SidebarPanelStyle", kids=[
        N("ScrollContainer", "ScrollView", (4, 4, 392, 742), pin="lrtb", style="InvisibleStyle", zorder=500,
          HScrollBarStyle="ScrollbarStyle", ScrollViewStyle="InvisibleStyle", VScrollBarStyle="ScrollbarStyle",
          intScrollBarDim=10, optOverlay=False, optShowHBar=False),
    ])


SOURCES = (["A-Env", "F-Env", "Vel", "Rand"] + [f"S{i}" for i in range(1, 17)] + [f"M{i}" for i in range(1, 5)]
           + ["Wheel", "Bend", "Press", "Trans"])


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
        N("Button", "Src0", (2, 7, 38, 20), pin="m", style="TransmodButtonStyle", text="Base",
          displayName="Edit base values"),
        N("LayoutBox", None, (46, 7, 914, 20), pin="lrm", kids=srcs, **box),
        N("LayoutBox", None, (46, 29, 914, 3), pin="lr", kids=flash, **box),
    ])
    macros = []
    for i in range(4):
        macros.append(N("Labeller", None, (i * 45, 0, 43, H), style="SmallControlLabellerStyle", enumTextPosition="Below",
                        intTextOffset=-1, kids=[
                            N("Knob", f"Macro{i}", (11, 1, 20, 20), pin="ct", displayName=f"Macro {i + 1}",
                              style="AltKnobStyle", realDialThickness=0.3)]))
    right = N("LayoutBox", None, (970, 0, 180, H), pin="lrtb", kids=macros, **box)
    return N("Panel", "TransmodSelectPanel", (0, 0, W, H), pin="lrtb", style="InvisibleStyle", kids=[left, right])


def trigger_dialog():
    """Which events restart a modulator."""
    def check(name, x, tip):
        return N("Button", name, (x, 4, 14, 14), displayName=tip, style="DefaultCheckboxButtonStyle")
    rows = N("Labeller", None, (20, 6, 320, 436), pin="lrtb", displayName="None", enumTextPosition="Above",
             style="DialogPanelLeftLabellerStyle", kids=[
                 N("Labeller", None, (0, 0, 320, 22), pin="lrt", enumTextPosition="Right", intTextOffset=6,
                   style="DialogPanelLeftLabellerStyle", kids=[check("TStart", 0, "Restart when the transport starts")]),
                 N("Labeller", None, (0, 34, 320, 24), pin="lr", displayName="Restart on engine pattern change",
                   enumTextPosition="Right", intTextOffset=6, style="DialogPanelLeftLabellerStyle",
                   kids=[check(f"E{i + 1}", i * 32, str(i + 1)) for i in range(8)]),
                 N("Labeller", None, (0, 66, 320, 28), pin="lrt", enumTextPosition="Right", intTextOffset=6,
                   style="DialogPanelLeftLabellerStyle", kids=[
                       N("PopupButton", "ShowEng", (0, 4, 56, 18), displayName="Engine", style="DefaultPopupButtonStyle")]),
                 N("Matrix", "Matrix", (0, 116, 320, 320), pin="lrtb", displayName="Pads that restart it",
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
