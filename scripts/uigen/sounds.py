"""Dreist's metronome clicks, synthesised (no recordings).

Writes Metronomes/<set>/{Bar,Beat}.wav (44.1 kHz, 16-bit mono). Bar is the
accented first beat of the bar. Deterministic: the noise is seeded.
"""

import io
import math
import random
import struct
import wave

SR = 44100


def _wav(samples):
    peak = max(1e-9, max(abs(x) for x in samples))
    gain = 0.89 / peak  # about -1 dBFS
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(round(max(-1.0, min(1.0, x * gain)) * 32767))) for x in samples))
    return buf.getvalue()


def _fade(s, ms=2.0):
    n = int(SR * ms / 1000)
    for i in range(1, n + 1):
        s[-i] *= (i - 1) / n
    return s


def tone_click(freq, decay_ms, length_ms=60, overtone=2.76, snap=0.35):
    """A struck bar: a pitched partial plus an inharmonic one and a short snap."""
    n = int(SR * length_ms / 1000)
    rnd = random.Random(int(freq))
    out = []
    for i in range(n):
        t = i / SR
        env = math.exp(-t * 1000 / decay_ms)
        body = math.sin(2 * math.pi * freq * t) + 0.35 * math.sin(2 * math.pi * freq * overtone * t) * math.exp(-t * 1000 / (decay_ms * 0.4))
        click = snap * (rnd.random() * 2 - 1) * math.exp(-t * 1000 / 0.6)
        out.append(env * body + click)
    return _fade(out)


def wood(freq, length_ms=50):
    """A woody knock: resonant noise (two-pole band-pass) with a fast decay."""
    n = int(SR * length_ms / 1000)
    rnd = random.Random(int(freq) * 7)
    r = 0.995
    w0 = 2 * math.pi * freq / SR
    a1, a2 = -2 * r * math.cos(w0), r * r
    y1 = y2 = 0.0
    out = []
    for i in range(n):
        t = i / SR
        x = (rnd.random() * 2 - 1) * math.exp(-t * 1000 / 1.2)
        y = x - a1 * y1 - a2 * y2
        y2, y1 = y1, y
        out.append(y * math.exp(-t * 1000 / 18))
    return _fade(out)


def blip(freq, length_ms=35):
    """A short electronic blip: square-ish tone, quick decay."""
    n = int(SR * length_ms / 1000)
    out = []
    for i in range(n):
        t = i / SR
        s = sum(math.sin(2 * math.pi * freq * k * t) / k for k in (1, 3, 5))
        out.append(s * math.exp(-t * 1000 / 9))
    return _fade(out)


SETS = {
    "Default": (tone_click(1760, 14), tone_click(1320, 11)),
    "Wood": (wood(1250), wood(900)),
    "Blip": (blip(2093), blip(1568)),
}


def outputs():
    files = {}
    for name, (bar, beat) in SETS.items():
        files[f"Metronomes/{name}/Bar.wav"] = _wav(bar)
        files[f"Metronomes/{name}/Beat.wav"] = _wav(beat)
    return files
