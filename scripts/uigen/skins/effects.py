"""The effect chain strip: the chain frame, one effect's card, and the
add-an-effect slot (Effects/*.skin).  The card hosts an Effects/FX panel in
its `EffectPanel`."""

from . import N, skin

H = 194


def chain():
    icon = dict(style="DefaultIconButtonStyle", optIsMomentary=True)
    rail = [
        N("Button", "ActiveButton", (4, 4, 20, 20), style="DefaultIconButtonStyle", text="", displayName="Chain on/off", id=100006),
        N("Button", "PresetCombo", (4, 28, 20, 20), text="", displayName="Chain presets", id=100006, **icon),
        N("Button", "PresetPrev", (4, 50, 20, 20), text="", displayName="Previous chain", id=100000, **icon),
        N("Button", "PresetNext", (4, 72, 20, 20), text="", displayName="Next chain", id=100001, **icon),
        N("Labeller", None, (2, 98, 24, 38), style="SmallControlLabellerStyle", enumTextPosition="Below", kids=[
            N("Knob", "MixKnob", (2, 0, 20, 20), displayName="Mix", id=100000, style="KnobStyle", realDialThickness=0.3)]),
        N("MultiLineLabel", "IdentifierLabel", (2, 138, 24, 54), pin="tb", style="SmallControlLabellerStyle", intLineHeight=12),
    ]
    return N("Panel", None, (0, 0, 600, H + 4), style="InvisibleStyle", kids=rail + [
        N("ScrollContainer", "FXScroller", (28, 4, 572, H), pin="lrtb", style="InvisibleStyle", HScrollBarStyle="",
          ScrollViewStyle="", VScrollBarStyle="", intScrollBarDim=10, optOverlay=False),
        N("Panel", None, (0, 0, 1, H + 4), pin="ltb", style="LightDividerStyle", zorder=666),
    ])


def card():
    """One effect: header (type menu, preset arrows), the input/mix/output
    column, the effect's own panel and the on switch."""
    W, Hc = 252, 182
    icon = dict(style="DefaultIconButtonStyle", optIsMomentary=True)
    column = N("Labeller", "SetupPanel", (0, 22, 40, 136), pin="ltb", id=100001, style="SmallControlLabellerStyle",
               enumTextPosition="Below", intTextOffset=0, kids=[
                   N("TransmodKnob", n, (5, 2 + i * 44, 30, 30), displayName=cap, id=i_d, style="TransmodStyle")
                   for i, (n, cap, i_d) in enumerate([("TrimKnob", "In", 100005), ("MixKnob", "Mix", 100004),
                                                      ("OutputKnob", "Out", 100005)])])
    return N("CollapsePanel", "CtrlPanel", (0, 0, W, Hc), pin="tb", iconicTarget="ARLeft", style="EffectCollapsePanelStyle", kids=[
        N("Button", "EffectTypeCombo", (3, 3, 16, 16), pin="lt", text="", displayName="Choose effect", id=100002, **icon),
        N("Button", "LastPresetButton", (W - 30, 3, 13, 16), pin="lr", text="", displayName="Previous preset", id=100000, **icon),
        N("Button", "NextPresetButton", (W - 16, 3, 13, 16), pin="lr", text="", displayName="Next preset", id=100001, **icon),
        # The header between the buttons: drag it left or right to move the
        # effect in the chain.
        N("Panel", "HeaderGrip", (21, 0, W - 53, 22), pin="lrt", overloadClass="EffectHeaderGrip", style="InvisibleStyle"),
        column,
        N("Panel", "EffectPanel", (41, 22, 210, Hc - 22), pin="lrtb", id=100012, style="InvisibleStyle"),
        N("Button", "ActiveButton", (3, Hc - 20, 34, 17), displayName="Effect on/off", id=100006, style="DefaultButtonStyle", text="On"),
        N("Panel", None, (W - 1, 0, 1, Hc), pin="lrtb", style="LightDividerStyle", zorder=666),
    ])


def empty():
    return N("Panel", None, (0, 0, 40, H), style="CollapsePanelStyle", kids=[
        N("Button", "AddButton", (10, 4, 20, 20), pin="t", text="", displayName="Add an effect",
          style="ExxLargeIconButtonStyle", optIsMomentary=True),
        N("Panel", None, (39, 0, 1, H), pin="lrtb", style="LightDividerStyle", zorder=666),
    ])


def outputs():
    return {"Skin/Effects/EffectChain.skin": skin(chain()), "Skin/Effects/EffectPanel.skin": skin(card()),
            "Skin/Effects/EmptyEffect.skin": skin(empty())}
