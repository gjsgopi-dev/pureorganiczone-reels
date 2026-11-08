#!/usr/bin/env python3
"""Make a story_reel.py timestamps file for a voiceover that has no word timestamps
(e.g. an ElevenLabs Telugu voiceover).

Usage:
  python3 tools/ts_from_silence.py <voice.wav|mp3> <spec.json> <out_ts.json> [--breaks 2]

The spec's `voiceover` text is split at its <break .../> tags (or at "[pause]").
The N longest silences in the audio (ffmpeg silencedetect) become the breaks, in time order.
Words inside each part get start/end times spread by character length across the voiced
part of that segment, so `pitch_clip.until_word` (e.g. "హైదరాబాద్‌లో" -> use the spec's
`until_word` exactly as written in the voiceover) still works approximately.
"""
import json, re, subprocess, sys


def silences(path, noise="-32dB", dur=0.25):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af",
                          f"silencedetect=noise={noise}:d={dur}", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    total = float(re.findall(r"Duration: (\d+):(\d+):([\d.]+)", out) and
                  (lambda h, m, s: int(h) * 3600 + int(m) * 60 + float(s))(*re.findall(r"Duration: (\d+):(\d+):([\d.]+)", out)[0]))
    pairs = list(zip(starts, ends))
    return pairs, total


def main():
    wav, spec, out = sys.argv[1:4]
    n = int(sys.argv[sys.argv.index("--breaks") + 1]) if "--breaks" in sys.argv else None
    sp = json.load(open(spec))
    text = sp.get("voiceover_te") if sp.get("voiceover_lang") == "te" and sp.get("voiceover_te") else sp["voiceover"]
    parts = [p.strip() for p in re.split(r"<break[^>]*/>|\[pause\]", text) if p.strip()]
    n = n or len(parts) - 1
    pairs, total = silences(wav)
    inner = [p for p in pairs if p[0] > 0.3 and p[1] < total - 0.3]
    if len(inner) < n:
        raise SystemExit(f"found {len(inner)} pauses, need {n}; add longer pauses between parts")
    chosen = sorted(sorted(inner, key=lambda p: p[1] - p[0], reverse=True)[:n])
    lead = pairs[0][1] if pairs and pairs[0][0] < 0.05 else 0.0
    tail = pairs[-1][0] if pairs and pairs[-1][1] >= total - 0.05 else total
    seg_bounds = [lead] + [x for p in chosen for x in p] + [tail]
    ts = [{"word": "<start>", "start": 0.0, "end": 0.0}]
    for i, part in enumerate(parts):
        a, b = seg_bounds[2 * i], seg_bounds[2 * i + 1]
        words = part.split()
        L = sum(len(w) for w in words) or 1
        t = a
        for w in words:
            d = (b - a) * len(w) / L
            ts.append({"word": w, "start": round(t, 3), "end": round(t + d, 3)})
            t += d
        if i < len(chosen):
            s, e = chosen[i]
            ts.append({"word": '<break time="0.6s"/>', "start": round(s, 3), "end": round(e, 3)})
    ts.append({"word": "<end>", "start": round(total, 3), "end": round(total, 3)})
    json.dump(ts, open(out, "w"), ensure_ascii=False)
    print(f"{out}: {len(parts)} parts, breaks at " + ", ".join(f"{(s+e)/2:.2f}" for s, e in chosen) + f", total {total:.2f}s")


if __name__ == "__main__":
    main()
