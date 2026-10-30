"""Finish a HeyGen AI-video Reel: brand text cards + HeyGen voiceover + soft music.

Usage: python3 tools/heygen_reel.py <heygen_spec.json> <footage.mp4> <voice.wav> <out.mp4>

The heygen spec has a "cards" list; each card is shown from "start" to "end" (seconds):
  {"start": 0, "end": 3.8, "tag": "BLOOD SUGAR AWARE?", "title": "3 easy food swaps", "big": "1",
   "price": "₹1,391", "was": "₹1,546", "url": "pureorganiczone.com", "small": "disclaimer"}
All fields except start/end are optional. Optional "footage_map": [[src_start, src_end, out_len], ...]
plays those slices of the footage back to back, sped up or slowed to out_len seconds each, so each
shot lands under the matching spoken line (check the voice's word timestamps). Text is drawn here (Poppins), never by the AI model,
so spelling, prices and the health disclaimer are always exact. Keep text clear of the top 220px
and bottom 420px, where Instagram puts its own buttons. The logo badge sits at y 215-487, so\ncards start at top >= 560.
"""
import json, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FD = "/usr/share/fonts/truetype/google-fonts/"
F = lambda w, s: ImageFont.truetype(FD + f"Poppins-{w}.ttf", s)
DEEP, LIME, CREAM, EARTH = (22, 66, 44), (176, 214, 98), (250, 246, 234), (139, 94, 52)
HERE = os.path.dirname(os.path.abspath(__file__))


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur] if cur else lines


def card_png(c, path):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    blocks = []  # (kind, lines, font, colour, line_gap)
    if c.get("tag"):
        blocks.append(("tag", [c["tag"]], F("Bold", 44), DEEP, 0))
    if c.get("big"):
        blocks.append(("txt", [c["big"]], F("Bold", 190), LIME, 0))
    if c.get("title"):
        f = F("Bold", c.get("size", 74))
        blocks.append(("txt", wrap(d, c["title"], f, 900), f, CREAM, 12))
    if c.get("price"):
        blocks.append(("txt", [c["price"]], F("Bold", 110), LIME, 0))
    if c.get("was"):
        blocks.append(("strike", [c["was"]], F("Medium", 48), CREAM, 0))
    if c.get("url"):
        blocks.append(("txt", [c["url"]], F("Bold", 46), CREAM, 0))
    if c.get("small"):
        f = F("Medium", 34)
        blocks.append(("txt", wrap(d, c["small"], f, 880), f, CREAM, 6))

    def bh(b):
        kind, lines, f, _, gap = b
        asc, desc = f.getmetrics()
        h = len(lines) * (asc + desc) + (len(lines) - 1) * gap
        return h + (40 if kind == "tag" else 0)

    gap = 28
    total = sum(bh(b) for b in blocks) + gap * (len(blocks) - 1)
    top = c.get("top", 560)
    pad = 56
    # dark rounded panel so text reads over any footage
    d.rounded_rectangle((60, top - pad, W - 60, top + total + pad), 44, fill=(12, 34, 22, 190))
    y = top
    for b in blocks:
        kind, lines, f, col, lg = b
        asc, desc = f.getmetrics()
        lh = asc + desc
        if kind == "tag":
            tw = d.textlength(lines[0], font=f)
            d.rounded_rectangle((W / 2 - tw / 2 - 32, y, W / 2 + tw / 2 + 32, y + lh + 40), 40, fill=LIME)
            d.text((W / 2, y + 20 + lh / 2), lines[0], font=f, anchor="mm", fill=col)
        else:
            for i, line in enumerate(lines):
                ly = y + i * (lh + lg)
                d.text((W / 2, ly + lh / 2), line, font=f, anchor="mm", fill=col)
                if kind == "strike":
                    tw = d.textlength(line, font=f)
                    d.line((W / 2 - tw / 2, ly + lh / 2, W / 2 + tw / 2, ly + lh / 2), fill=col, width=4)
        y += bh(b) + gap
    logo_badge(img)
    img.save(path)


def logo_badge(img, cx=W // 2, top=215, logo_w=230):
    """Company logo (assets/logo.png) on a white rounded badge, always on, inside the safe area."""
    logo = Image.open(os.path.join(HERE, "..", "assets", "logo.png")).convert("RGBA")
    logo = logo.resize((logo_w, round(logo.height * logo_w / logo.width)), Image.LANCZOS)
    pad = 18
    bw, bh = logo.width + 2 * pad, logo.height + 2 * pad
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((cx - bw // 2, top, cx + bw // 2, top + bh), 28, fill=(255, 255, 255, 242))
    img.alpha_composite(logo, (cx - logo.width // 2, top + pad))


def main(spec_path, footage, voice, out):
    spec = json.load(open(spec_path))
    cards = spec["cards"]
    vdur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", voice]).decode().strip())
    total = round(max(vdur + 0.5, cards[-1]["end"]), 2)
    tmp = tempfile.mkdtemp()
    music = os.path.join(tmp, "music.wav")
    subprocess.run([sys.executable, os.path.join(HERE, "music_maker.py"), music, str(total),
                    spec.get("music", "calm")], check=True, capture_output=True)
    ins = ["-i", footage, "-i", voice, "-i", music]
    base = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},fps=30"
    fmap = spec.get("footage_map")  # [[src_start, src_end, out_len], ...] to retime shots to the voice
    if fmap:
        n = len(fmap)
        chain = f"[0:v]{base},split={n}" + "".join(f"[s{k}]" for k in range(n))
        for k, (a, b, ln) in enumerate(fmap):
            chain += f";[s{k}]trim={a}:{b},setpts=(PTS-STARTPTS)*{ln / (b - a):.4f}[g{k}]"
        chain += ";" + "".join(f"[g{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=0,fps=30[gc]"
        chain += f";[gc]tpad=stop_mode=clone:stop_duration=5,trim=0:{total},setpts=PTS-STARTPTS[v0]"
    else:
        chain = (f"[0:v]{base},tpad=stop_mode=clone:stop_duration=5,trim=0:{total},"
                 f"setpts=PTS-STARTPTS[v0]")
    last = "v0"
    for i, c in enumerate(cards):
        p = os.path.join(tmp, f"card{i}.png")
        card_png(c, p)
        ins += ["-loop", "1", "-t", str(total), "-i", p]
        fade = (f"[{i + 3}:v]format=rgba,fade=in:st={c['start']}:d=0.25:alpha=1,"
                f"fade=out:st={max(c['start'], c['end'] - 0.2)}:d=0.2:alpha=1[c{i}]")
        chain += f";{fade};[{last}][c{i}]overlay=0:0:enable='between(t,{c['start']},{c['end']})'[v{i + 1}]"
        last = f"v{i + 1}"
    chain += (f";[1:a]adelay=200|200,volume=1.0[vo];[2:a]volume=0.18[mu];"
              f"[vo][mu]amix=inputs=2:duration=longest:normalize=0,atrim=0:{total}[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", chain,
                    "-map", f"[{last}]", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", "-t", str(total), out], check=True)
    print(out, total, "s")


if __name__ == "__main__":
    main(*sys.argv[1:5])
