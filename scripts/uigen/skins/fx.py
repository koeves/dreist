"""The 42 effect panels (Effects/FX/<Effect>.skin).

Each panel follows the shipped skin of its effect ([re:ee3c0f]): the same
rects, control classes, captions and anchors, drawn with Dreist's own
styles. Control names (Control1..9, VUMeter, Display) are what the editor
binds to the effect's parameters, its gain-reduction output and its
response curves. The root labeller captions the knobs below them.

Meters and plots: the original draws the dynamics panels' VUMeter with its
meter class and the EQ / filter panels' Display with its EQ plot class
([re:664306], [re:faafb0]); here they take the effect styles of
theme.py's "Effect panel meters and plots" block.
"""

from . import N, skin

W, H = 210, 137


def K(name, caption, rect, pin=""):
    return N("TransmodKnob", name, rect, pin=pin, displayName=caption, style="TransmodStyle")


def Pop(name, tip, rect, pin=""):
    return N("PopupButton", name, rect, pin=pin, displayName=tip, style="DefaultPopupButtonStyle")


def Btn(name, tip, text, rect, pin=""):
    return N("Button", name, rect, pin=pin, displayName=tip, text=text, style="DefaultButtonStyle")


def Box(rect, kids):
    """An unlabelled group (the labeller captions only its own knobs)."""
    return N("Panel", None, rect, kids=kids, style="InvisibleStyle")


def Meter(rect, pin=""):
    """The gain-reduction meter: a needle over -oo..0 dB."""
    return N("Meter", "VUMeter", rect, pin=pin, style="EffectMeterStyle", realRadius=0.75, textLeftRange="-∞", textRightRange="0", textUnits="dB")


def Plot(rect):
    """The response plot, down to the card's bottom edge."""
    return N("PolyPlot", "Display", rect, pin="lrtb", id=100000, overloadClass="EffectEQPlot", style="EffectEQPlotStyle")


def _centre_pins(node, pw):
    """The shipped skins mark some off-centre controls `Center`; the
    original only applies anchors when the parent resizes (the panels keep
    their width), so they stay where their rects put them. Keep the
    horizontal centring pin only on controls that are centred."""
    for k in node.kids:
        x, _, w, _ = k.rect
        if "c" in k.pin and abs(x + w / 2 - pw / 2) > 1:
            k.pin = k.pin.replace("c", "")
        _centre_pins(k, w)
    return node


def fx(kids, name=None, text_offset=0, pin=""):
    return _centre_pins(N("Labeller", name, (0, 0, W, H), pin=pin, kids=kids, style="SmallControlLabellerStyle", enumTextPosition="Below",
             intTextOffset=text_offset, id=6000), W)


FX = {
    "Amber": fx([
        K("Control2", "Speed", (27, 12, 50, 50)),
        K("Control3", "Spread", (132, 12, 50, 50)),
        Box((65, 83, 80, 45), [Pop("Control1", "Model", (0, 0, 80, 20), "c"), Btn("Control4", "Bright Mode", "Bright", (0, 25, 80, 20), "c")]),
    ]),
    "AnalogRingMod": fx([
        K("Control2", "Drive", (17, 12, 50, 50)),
        K("Control4", "Tone", (80, 12, 50, 50), "c"),
        K("Control3", "Pitch", (142, 12, 50, 50)),
        Box((65, 83, 80, 20), [Pop("Control1", "Carrier", (0, 0, 80, 20), "c")]),
    ]),
    "Bloom": fx([
        K("Control3", "Feedback", (17, 12, 50, 50)),
        K("Control2", "Delay Time", (80, 12, 50, 50), "c"),
        K("Control4", "Tone", (142, 12, 50, 50)),
        Box((19, 83, 175, 45), [Pop("Control1", "Delay model", (45, 0, 85, 20)), Btn("Control6", "Freeze", "Freeze", (0, 25, 40, 20)), Btn("Control5", "Sync To Host Tempo", "Sync", (45, 25, 40, 20)), Btn("Control7", "Ping Pong Mode", "Pong", (90, 25, 40, 20)), Btn("Control8", "Reversed Delay Mode", "Rev", (135, 25, 40, 20))]),
    ], text_offset=-1),
    "BreverbHall": fx([
        K("Control1", "Time", (17, 5, 50, 50)),
        K("Control4", "Size", (80, 5, 50, 50)),
        K("Control2", "Predelay", (142, 5, 50, 50)),
        K("Control6", "Shape", (17, 72, 50, 50)),
        K("Control5", "Spread", (80, 72, 50, 50)),
        K("Control3", "Diffusion", (142, 72, 50, 50)),
    ]),
    "BreverbInverse": fx([
        K("Control1", "Time", (17, 12, 50, 50)),
        K("Control2", "Predelay", (80, 12, 50, 50), "c"),
        K("Control3", "Diffusion", (142, 12, 50, 50)),
    ]),
    "BreverbPlate": fx([
        K("Control1", "Time", (17, 5, 50, 50)),
        K("Control4", "Size", (80, 5, 50, 50)),
        K("Control2", "Predelay", (142, 5, 50, 50)),
        K("Control5", "Spread", (44, 72, 50, 50)),
        K("Control3", "Diffusion", (111, 72, 50, 50)),
    ]),
    "BreverbRoom": fx([
        K("Control1", "Time", (17, 5, 50, 50)),
        K("Control4", "Size", (80, 5, 50, 50)),
        K("Control2", "Predelay", (142, 5, 50, 50)),
        K("Control5", "Spread", (44, 72, 50, 50)),
        K("Control3", "Diffusion", (111, 72, 50, 50)),
    ]),
    "BusComp": fx([
        K("Control1", "Threshold", (10, 5, 40, 40)),
        Meter((60, 5, 90, 40), "c"),
        K("Control5", "Makeup", (160, 5, 40, 40)),
        Box((85, 50, 40, 20), [Btn("Control6", "Analog Limiting", "Limit", (0, 0, 40, 20), "c")]),
        K("Control2", "Attack", (10, 77, 40, 40)),
        K("Control3", "Ratio", (85, 77, 40, 40), "c"),
        K("Control4", "Release", (160, 77, 40, 40)),
    ]),
    "ChanComp": fx([
        K("Control1", "Input", (10, 5, 40, 40)),
        Meter((60, 5, 90, 40), "c"),
        K("Control5", "Output", (160, 5, 40, 40)),
        Pop("Control4", "Ratio", (75, 50, 60, 17), "c"),
        K("Control2", "Attack", (40, 77, 40, 40)),
        K("Control3", "Release", (130, 77, 40, 40)),
    ]),
    "Chorus": fx([
        K("Control2", "Depth", (17, 38, 50, 50)),
        K("Control1", "Frequency", (80, 38, 50, 50)),
        K("Control3", "Spread", (142, 38, 50, 50)),
    ]),
    "Comb": fx([
        K("Control1", "Drive", (17, 12, 50, 50)),
        K("Control3", "Pitch", (80, 12, 50, 50)),
        K("Control4", "Rez", (142, 12, 50, 50)),
        Box((65, 83, 80, 20), [Btn("Control2", "Direction", "Negative", (0, 0, 80, 20), "c")]),
    ]),
    "Crusher": fx([
        K("Control1", "Drive", (17, 5, 50, 50)),
        K("Control4", "High Cut", (80, 5, 50, 50)),
        K("Control2", "Freq", (142, 5, 50, 50)),
        K("Control6", "Tone", (17, 72, 50, 50)),
        K("Control5", "Low Cut", (80, 72, 50, 50)),
        K("Control3", "Bits", (142, 72, 50, 50)),
    ]),
    "DJEQ": fx([
        K("Control1", "Low Gain", (9, 5, 40, 40)),
        K("Control2", "Mid Gain", (59, 5, 40, 40)),
        K("Control3", "Mid Freq", (109, 5, 40, 40)),
        K("Control4", "High Gain", (159, 5, 40, 40)),
        Plot((0, 62, 205, 75)),
    ], pin="lrtb"),
    "Delay": fx([
        K("Control1", "Time", (17, 5, 50, 50), "t"),
        K("Control2", "F-back", (142, 5, 50, 50), "t"),
        Box((85, 20, 40, 20), [Btn("Control6", "Sync To Host Tempo", "Sync", (0, 0, 40, 20), "c")]),
        K("Control3", "Low Cut", (22, 75, 40, 40)),
        K("Control4", "High Cut", (147, 75, 40, 40)),
        K("Control5", "Swing", (85, 76, 40, 40)),
    ]),
    "DirtyDac": fx([
        K("Control1", "Frequency", (22, 30, 60, 60)),
        K("Control2", "Anti Alias", (128, 30, 60, 60)),
    ]),
    "Distortion": fx([
        K("Control2", "Drive", (75, 5, 60, 60), "c"),
        K("Control5", "Tone", (14, 15, 40, 40)),
        K("Control6", "Clean", (159, 15, 40, 40)),
        K("Control4", "Low Cut", (14, 80, 40, 40)),
        K("Control3", "Hi Cut", (159, 80, 40, 40)),
        Box((68, 83, 75, 20), [Pop("Control1", "Algorithm", (0, 0, 75, 20), "c")]),
    ]),
    "DrumDynamics": fx([
        K("Control1", "Attack", (27, 12, 50, 50)),
        K("Control2", "Sustain", (132, 12, 50, 50)),
        Box((80, 83, 50, 45), [Btn("Control4", "Use A Merged Mono Sidechain For Each Channel", "SChain", (0, 0, 50, 20), "c"), Btn("Control3", "Enable Faster Envelopes", "Fast", (0, 25, 50, 20), "c")]),
    ]),
    "Enhancer": fx([
        K("Control1", "Frequency", (27, 12, 50, 50)),
        K("Control3", "Depth", (132, 12, 50, 50)),
        Box((65, 83, 80, 20), [Pop("Control2", "Model", (0, 0, 80, 20), "c")]),
    ]),
    "EnvShaper": fx([
        K("Control1", "Attack", (9, 10, 40, 40)),
        K("Control2", "Sustain", (59, 10, 40, 40)),
        K("Control4", "Sensitivity", (109, 10, 40, 40)),
        K("Control3", "Gain", (159, 10, 40, 40)),
        Box((80, 80, 50, 20), [Btn("Control5", "Mono Link Left And Right", "Linked", (0, 0, 50, 20), "c")]),
    ]),
    "Filter": fx([
        K("Control2", "H Freq", (75, 5, 40, 40)),
        K("Control4", "L Freq", (15, 5, 40, 40)),
        Box((135, 5, 60, 44), [Btn("Control1", "High Pass Filter", "HP Active", (0, 0, 60, 20)), Btn("Control3", "Low Pass Filter", "LP Active", (0, 24, 60, 20))]),
        Plot((0, 62, 205, 75)),
    ], pin="ltb"),
    "Flanger": fx([
        K("Control1", "Frequency", (17, 5, 50, 50)),
        K("Control4", "Feedback", (80, 5, 50, 50)),
        K("Control2", "Depth", (142, 5, 50, 50)),
        K("Control6", "Phase", (17, 72, 50, 50)),
        K("Control5", "Spread", (80, 72, 50, 50)),
        K("Control3", "Pos", (142, 72, 50, 50)),
    ]),
    "Freezer": fx([
        K("Control1", "Gate", (17, 5, 50, 50)),
        K("Control4", "Smoothing", (80, 5, 50, 50)),
        K("Control2", "Loop Length", (142, 5, 50, 50)),
        K("Control6", "Speed", (17, 72, 50, 50)),
        K("Control5", "Scratch", (80, 72, 50, 50)),
        K("Control3", "Grain Length", (142, 72, 50, 50)),
    ]),
    "Gain": fx([
        K("Control1", "Gain", (60, 23, 90, 90), "cm"),
    ]),
    "GuruFilter": fx([
        K("Control1", "Mode", (17, 12, 50, 50)),
        K("Control2", "Cutoff", (80, 12, 50, 50), "c"),
        K("Control3", "Rez", (142, 12, 50, 50)),
    ]),
    "HILO": fx([
        K("Control1", "Balance", (54, 5, 40, 40), "t"),
        K("Control2", "Crossover", (117, 5, 40, 40), "t"),
        Plot((0, 62, 205, 75)),
    ], pin="lrtb"),
    "Limiter": fx([
        Meter((60, 5, 90, 40), "c"),
        K("Control2", "Pre Gain", (17, 60, 50, 50)),
        K("Control1", "Hardness", (80, 60, 50, 50), "c"),
        K("Control3", "Post Gain", (142, 60, 50, 50)),
    ]),
    "Maul": fx([
        Pop("Control1", None, (68, 5, 75, 20), "c"),
        K("Control2", "L Freq", (9, 29, 40, 40)),
        K("Control3", "L Rez", (59, 29, 40, 40)),
        K("Control4", "L Drive", (9, 84, 40, 40)),
        K("Control5", "L Gain", (59, 84, 40, 40)),
        K("Control6", "H Freq", (109, 29, 40, 40)),
        K("Control7", "H Rez", (159, 29, 40, 40)),
        K("Control8", "H Drive", (109, 84, 40, 40)),
        K("Control9", "H Gain", (159, 84, 40, 40)),
    ]),
    "Mault": fx([
        K("Control2", "Drive", (10, 5, 60, 60), "c"),
        Box((90, 14, 102, 43), [Pop("Control1", "Algorithm", (0, 0, 102, 20), "c"), Btn("Control5", "Analog Overdrive", "Saturate", (0, 23, 50, 20)), Btn("Control6", "Analog Limiting", "Limit", (52, 23, 50, 20))]),
        K("Control3", "In Gain", (20, 81, 40, 40)),
        K("Control4", "Out Gain", (85, 81, 40, 40)),
    ]),
    "ModFilter": fx([
        K("Control6", "Depth", (7, 5, 50, 50)),
        K("Control2", "Cutoff", (80, 5, 50, 50), "c"),
        K("Control3", "Resonance", (152, 5, 50, 50)),
        K("Control4", "Attack", (12, 80, 40, 40)),
        Box((68, 80, 75, 20), [Pop("Control1", "Filter Type", (0, 0, 75, 20), "c")]),
        K("Control5", "Decay", (157, 81, 40, 40)),
    ]),
    "ModelFilter": fx([
        K("Control1", "Drive", (17, 12, 50, 50)),
        K("Control3", "Cutoff", (80, 12, 50, 50)),
        K("Control4", "Rez", (142, 12, 50, 50)),
        Box((65, 83, 80, 20), [Pop("Control2", "Filter Type", (0, 0, 80, 20), "c")]),
    ]),
    "NoiseGate": fx([
        K("Control1", "Attack", (17, 5, 50, 50)),
        K("Control4", "Threshold", (80, 5, 50, 50)),
        K("Control2", "Hold", (142, 5, 50, 50)),
        K("Control6", "LPF", (17, 72, 50, 50)),
        K("Control5", "Hysteresis", (80, 72, 50, 50)),
        K("Control3", "Release", (142, 72, 50, 50)),
    ]),
    "ParaEQ": fx([
        K("Control5", "H Freq", (109, 5, 28, 28)),
        K("Control6", "H Gain", (142, 5, 28, 28)),
        K("Control4", "H Q", (175, 5, 28, 28)),
        K("Control2", "L Freq", (5, 5, 28, 28)),
        K("Control3", "L Gain", (38, 5, 28, 28)),
        K("Control1", "L Q", (71, 5, 28, 28)),
        Plot((0, 52, 205, 85)),
    ], pin="lrtb"),
    "PhaseMod": fx([
        K("Control3", "Stack", (17, 5, 50, 50)),
        K("Control5", "Spread", (142, 5, 50, 50)),
        Box((80, 20, 50, 20), [Pop("Control2", "Algorithm", (0, 0, 50, 20), "c")]),
        K("Control6", "Depth", (17, 72, 50, 50)),
        K("Control1", "Pitch", (80, 72, 50, 50), "c"),
        K("Control4", "Width", (142, 72, 50, 50)),
    ]),
    "Phaser": fx([
        K("Control3", "Pitch", (17, 5, 50, 50)),
        K("Control5", "Frequency", (142, 5, 50, 50)),
        Box((80, 20, 50, 20), [Pop("Control2", "Number Of Stages", (0, 0, 50, 20), "c")]),
        K("Control6", "Depth", (17, 72, 50, 50)),
        K("Control1", "Drive", (80, 72, 50, 50), "c"),
        K("Control4", "Resonance", (142, 72, 50, 50)),
    ]),
    "Reverb": fx([
        K("Control1", "Room Size", (17, 5, 50, 50)),
        K("Control4", "Density", (80, 5, 50, 50)),
        K("Control2", "Decay", (142, 5, 50, 50)),
        K("Control6", "Damp Gain", (17, 72, 50, 50)),
        K("Control5", "Damp Freq", (80, 72, 50, 50)),
        K("Control3", "Pre Delay", (142, 72, 50, 50)),
    ]),
    "RingSting": fx([
        K("Control1", "Drive", (27, 12, 50, 50)),
        K("Control3", "Pitch", (132, 12, 50, 50)),
        Box((68, 83, 80, 20), [Pop("Control2", "Carrier", (0, 0, 80, 20), "c")]),
    ]),
    "Shifter": fx([
        K("Control1", "Pitch", (22, 30, 60, 60)),
        K("Control2", "Amp", (128, 30, 60, 60)),
    ]),
    "SingleMault": fx([
        K("Control2", "Drive", (10, 5, 60, 60)),
        Box((100, 14, 75, 43), [Pop("Control1", "Algorithm", (0, 0, 75, 20)), Btn("Control6", "Analog Overdrive", "Saturate", (0, 23, 75, 20))]),
        K("Control3", "Post Freq", (20, 81, 40, 40)),
        K("Control4", "Restore", (85, 81, 40, 40), "c"),
        K("Control5", "Out Gain", (150, 81, 40, 40)),
    ]),
    "StereoWidth": fx([
        K("Control1", "Gain", (22, 30, 60, 60)),
        K("Control2", "Width", (128, 30, 60, 60)),
    ]),
    "TinCan": fx([
        K("Control1", "Decay", (17, 5, 50, 50)),
        K("Control4", "Pinch", (80, 5, 50, 50)),
        K("Control2", "Size", (142, 5, 50, 50)),
        K("Control5", "Squeeze", (44, 72, 50, 50)),
        K("Control3", "Damp", (111, 72, 50, 50)),
    ]),
    "VCAComp": fx([
        K("Control4", "SC In", (10, 5, 40, 40)),
        K("Control5", "Output", (160, 5, 40, 40)),
        Meter((60, 8, 90, 40), "c"),
        K("Control1", "Attack", (10, 72, 40, 40)),
        K("Control2", "Release", (60, 72, 40, 40)),
        K("Control6", "Ratio", (110, 72, 40, 40), "c"),
        K("Control3", "Threshold", (160, 72, 40, 40), "c"),
    ]),
    "VariEQ": fx([
        K("Control2", "Frequency", (10, 5, 40, 40)),
        K("Control4", "Gain", (102, 5, 40, 40)),
        K("Control3", "Q", (56, 5, 40, 40)),
        Box((150, 15, 55, 20), [Pop("Control1", "EQ Mode", (0, 0, 55, 20))]),
        # The shipped rect says y 63, its anchors 62 (the layout uses them).
        Plot((0, 62, 205, 75)),
    ], name="VarLab", pin="lrtb"),

}


def outputs():
    return {f"Skin/Effects/FX/{k}.skin": skin(v) for k, v in sorted(FX.items())}
