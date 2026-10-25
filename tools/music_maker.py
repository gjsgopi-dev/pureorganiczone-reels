"""Compose a short, warm, royalty-free acoustic loop (plucked guitar + bass + shaker).

Usage: python3 music_maker.py out.wav seconds
"""
import sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter

SR = 44100
rng = np.random.default_rng(7)


def pluck(freq, dur, bright=0.5, decay=0.996):
    """Karplus-Strong plucked string."""
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, period)
    # soften the excitation for a nylon-like tone
    buf = lfilter([bright, 1 - bright], [1], buf)
    out = np.empty(n)
    for i in range(n):
        v = buf[i % period]
        out[i] = v
        buf[i % period] = decay * 0.5 * (v + buf[(i + 1) % period])
    return out


def note(name):
    names = {"C": -9, "C#": -8, "D": -7, "D#": -6, "E": -5, "F": -4, "F#": -3,
             "G": -2, "G#": -1, "A": 0, "A#": 1, "B": 2}
    pitch, octave = name[:-1], int(name[-1])
    return 440.0 * 2 ** ((names[pitch] + 12 * (octave - 4)) / 12)


def add(mix, s, x):
    if s >= len(mix):
        return
    e = min(len(mix), s + len(x))
    mix[s:e] += x[: e - s]


def lowpass(x, cut):
    b, a = butter(2, cut / (SR / 2), "low")
    return lfilter(b, a, x)


def main(out, seconds):
    bpm = 96
    beat = 60 / bpm
    eighth = beat / 2
    total = int(SR * (seconds + 1.5))
    mix = np.zeros(total)

    # I – V – vi – IV in G major, warm and hopeful
    chords = [
        ("G2", ["G3", "B3", "D4", "G4"]),
        ("D3", ["D3", "F#3", "A3", "D4"]),
        ("E2", ["E3", "G3", "B3", "E4"]),
        ("C3", ["C3", "E3", "G3", "C4"]),
    ]
    pattern = [0, 2, 1, 3, 2, 1, 3, 2]  # arpeggio order per bar (8 eighths)

    t = 0.0
    bar = 0
    while t < seconds:
        root, tones = chords[bar % 4]
        # bass on beats 1 and 3
        for b in (0, 2):
            s = int(SR * (t + b * beat))
            tone = pluck(note(root), 1.6, bright=0.2, decay=0.997)
            tone = lowpass(tone, 500) * 0.55
            add(mix, s, tone)
        # guitar arpeggio
        for k, idx in enumerate(pattern):
            s = int(SR * (t + k * eighth + rng.uniform(0, 0.008)))  # slight human timing
            vel = 0.32 if k % 2 == 0 else 0.24
            tone = pluck(note(tones[idx]), 1.4, bright=0.55, decay=0.995) * vel
            add(mix, s, tone)
        # soft shaker on off-beats
        for k in range(8):
            s = int(SR * (t + k * eighth))
            n = int(SR * 0.06)
            sh = rng.uniform(-1, 1, n) * np.exp(-np.linspace(0, 6, n))
            b, a = butter(2, 5000 / (SR / 2), "high")
            sh = lfilter(b, a, sh) * (0.05 if k % 2 else 0.025)
            add(mix, s, sh)
        t += 8 * eighth
        bar += 1

    mix = mix[: int(SR * seconds)]
    # gentle room: a couple of short echoes
    for delay, g in ((0.031, 0.18), (0.067, 0.12), (0.113, 0.08)):
        d = int(SR * delay)
        mix[d:] += g * mix[:-d].copy()
    # fade in/out
    fi, fo = int(SR * 0.3), int(SR * 1.5)
    mix[:fi] *= np.linspace(0, 1, fi)
    mix[-fo:] *= np.linspace(1, 0, fo)
    mix = mix / np.max(np.abs(mix)) * 0.8
    stereo = np.stack([mix, np.roll(mix, int(SR * 0.012))], axis=1)
    wavfile.write(out, SR, (stereo * 32767).astype(np.int16))
    print("wrote", out)


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]))
