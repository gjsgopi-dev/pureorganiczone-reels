#!/usr/bin/env python3
"""Build a narrated "village story" Reel.

Usage:
  python3 tools/story_reel.py <spec.json> <voice.wav> <timestamps.json> <out.mp4>

spec fields used:
  "story_clips": [ {"file": "<local mp4>", "start": 0.0, "en": "caption", "te": "Telugu caption"}, ... ]
  "end_clip":    "<local mp4 or https URL>"   brand clip, plays last with no captions
  optional per clip "nutrition_card": {"title": "Per 100 g goat meat (raw)",
      "rows": [["Protein", "20.6 g", "builds and repairs muscle"], ...],   (2-4 rows)
      "note": "Source: USDA FoodData Central"}
    drawn as a nutrition panel in the upper half of that scene (blended story + education Reels).
  optional "pitch_clip": {"file": "<local mp4>", "until_word": "Hyderabad", "en": "...", "te": "..."}
    plays at the start of the pitch until that word ends, then the brand clip
    (e.g. a goat-farm shot while the narrator says "from our own goat farms").
timestamps.json: the word_timestamps list returned by HeyGen create_speech_without_player
  (or the whole response object). The voiceover must contain exactly one
  <break time="..."/> between each story clip and before the brand pitch,
  i.e. len(story_clips) breaks. Each scene changes at the middle of its break.

Every scene is 1080x1920, 30 fps. Story clips are cropped to fill the frame,
slowed down (up to 1.7x) if the narration line is longer than the clip,
and get an English + Telugu caption box and a small brand tag.
Audio is loudness-normalised to -16 LUFS.
"""
import json, os, subprocess, sys, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GF = "/usr/share/fonts/truetype/google-fonts/"
TEL = os.path.join(ROOT, "assets", "fonts", "NotoSansTelugu.ttf")
W, H, FPS = 1080, 1920, 30
ENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(FPS), "-an"]


def run(cmd):
    subprocess.run(cmd, check=True)


def dur(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         check=True, capture_output=True, text=True).stdout
    return float(out.strip())


def font(name, size):
    from PIL import ImageFont
    for p in (GF + name, "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise SystemExit("no usable font found")


def caption_png(en, te, path):
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ef = font("Poppins-Bold.ttf", 56)
    words, lines, cur = en.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=ef) <= 900:
            cur = t
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    tf = None
    if te:
        tf = ImageFont.truetype(TEL, 50)
        try:
            tf.set_variation_by_name("SemiBold")
        except Exception:
            pass
    h = len(lines) * 72 + 60 + (60 if te else 0)
    y0 = 1540 - h
    d.rounded_rectangle([60, y0, 1020, y0 + h], radius=28, fill=(10, 30, 20, 170))
    y = y0 + 30
    for l in lines:
        w = d.textlength(l, font=ef)
        d.text(((W - w) / 2, y), l, font=ef, fill=(255, 255, 255, 255))
        y += 72
    if te:
        w = d.textlength(te, font=tf)
        d.text(((W - w) / 2, y + 4), te, font=tf, fill=(182, 220, 114, 255))
    bf = font("Poppins-Bold.ttf", 34)
    label = "PURE ORGANIC ZONE"
    d.rounded_rectangle([60, 140, 60 + d.textlength(label, font=bf) + 48, 200], radius=30, fill=(22, 66, 44, 200))
    d.text((84, 148), label, font=bf, fill=(245, 241, 230, 255))
    im.save(path)


def nutrition_png(card, path):
    """Nutrition panel: title, 2-4 rows of nutrient | amount | what it does, source line."""
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    rows = card.get("rows", [])[:4]
    tf, nf, af, sf, srcf = (font("Poppins-Bold.ttf", 46), font("Poppins-Bold.ttf", 44),
                            font("Poppins-Bold.ttf", 44), font("Poppins-Regular.ttf", 34),
                            font("Poppins-Regular.ttf", 28))
    y0 = 250
    h = 110 + len(rows) * 132 + 70
    d.rounded_rectangle([60, y0, W - 60, y0 + h], radius=32, fill=(250, 246, 236, 232))
    d.rounded_rectangle([60, y0, W - 60, y0 + 96], radius=32, fill=(22, 66, 44, 245))
    d.rectangle([60, y0 + 60, W - 60, y0 + 96], fill=(22, 66, 44, 245))
    title = card.get("title", "Nutrition")
    d.text(((W - d.textlength(title, font=tf)) / 2, y0 + 20), title, font=tf, fill=(245, 241, 230, 255))
    y = y0 + 122
    for r in rows:
        name, amt = str(r[0]), str(r[1])
        what = str(r[2]) if len(r) > 2 else ""
        d.text((100, y), name, font=nf, fill=(22, 66, 44, 255))
        d.text((W - 100 - d.textlength(amt, font=af), y), amt, font=af, fill=(196, 84, 24, 255))
        if what:
            d.text((100, y + 58), what, font=sf, fill=(60, 60, 60, 255))
        y += 132
    note = card.get("note", "")
    if note:
        d.text(((W - d.textlength(note, font=srcf)) / 2, y + 8), note, font=srcf, fill=(90, 90, 90, 255))
    im.save(path)


def app_band_png(path):
    """Band shown over the brand clip: website + app stores + subscriptions."""
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    y0, y1 = 1585, 1795
    d.rounded_rectangle([50, y0, W - 50, y1], radius=32, fill=(22, 66, 44, 235))
    f1 = font("Poppins-Bold.ttf", 46)
    f2 = font("Poppins-Regular.ttf", 36)
    l1 = "Get the Pure Organic Zone app"
    l2 = "App Store  ·  Google Play  ·  pureorganiczone.com"
    l3 = "Better app prices · Subscribe daily, weekly or monthly"
    for txt, f, y, col in ((l1, f1, y0 + 18, (245, 241, 230, 255)),
                           (l2, f2, y0 + 86, (182, 220, 114, 255)),
                           (l3, f2, y0 + 140, (245, 241, 230, 255))):
        w = d.textlength(txt, font=f)
        d.text(((W - w) / 2, y), txt, font=f, fill=col)
    im.save(path)


def main():
    spec_p, voice, ts_p, out = sys.argv[1:5]
    spec = json.load(open(spec_p))
    clips = spec["story_clips"]
    ts = json.load(open(ts_p))
    if isinstance(ts, dict):
        ts = ts.get("word_timestamps", ts)
    breaks = [(w["start"] + w["end"]) / 2 for w in ts if str(w.get("word", "")).startswith("<break")]
    if len(breaks) != len(clips):
        raise SystemExit(f"voiceover has {len(breaks)} breaks but spec has {len(clips)} story clips; "
                         "add one <break> after each story line")
    total = dur(voice) + 0.8
    bounds = [0.0] + breaks + [total]
    tmp = tempfile.mkdtemp(prefix="story_")
    parts = []
    for i, c in enumerate(clips):
        seg = round(bounds[i + 1] - bounds[i], 3)
        avail = dur(c["file"]) - c.get("start", 0)
        speed = max(1.0, seg / avail)
        if speed > 1.7:
            raise SystemExit(f"scene {i+1} narration ({seg}s) is too long for its {avail:.1f}s clip; shorten the line")
        png = os.path.join(tmp, f"cap{i}.png")
        caption_png(c["en"], c.get("te", ""), png)
        fo = round(seg - 0.2, 3)
        o = os.path.join(tmp, f"g{i}.mp4")
        inputs = ["-ss", str(c.get("start", 0)), "-i", c["file"], "-i", png]
        chain = f"[0:v]setpts={speed:.4f}*PTS,fps={FPS},scale=-2:{H},crop={W}:{H},setsar=1,trim=duration={seg}[b];[b][1:v]overlay"
        if c.get("nutrition_card"):
            npng = os.path.join(tmp, f"nut{i}.png")
            nutrition_png(c["nutrition_card"], npng)
            inputs += ["-i", npng]
            chain += f"[c];[c][2:v]overlay=enable='gte(t,0.6)'"
        run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex",
             chain + f",fade=t=in:st=0:d=0.2,fade=t=out:st={fo}:d=0.2,format=yuv420p", *ENC, o])
        parts.append(o)
    end_src = spec["end_clip"]
    if end_src.startswith("http"):
        p = os.path.join(tmp, "end_src.mp4")
        urllib.request.urlretrieve(end_src, p)
        end_src = p
    seg = round(bounds[-1] - bounds[-2], 3)
    pc = spec.get("pitch_clip")
    if pc:
        # Optional clip shown at the start of the pitch (e.g. our goat farm while the
        # narrator says "from our own goat farms"), until the end of `until_word`.
        last_break = bounds[-2]
        ends = [w["end"] for w in ts if w.get("start", 0) > last_break
                and str(w.get("word", "")).strip(".,!?").lower() == str(pc["until_word"]).lower()]
        if not ends:
            raise SystemExit(f"pitch_clip until_word {pc['until_word']!r} not found after the last break")
        pseg = round(ends[0] + 0.25 - last_break, 3)
        pavail = dur(pc["file"]) - pc.get("start", 0)
        pspeed = max(1.0, pseg / pavail)
        if pspeed > 1.7:
            raise SystemExit(f"pitch clip ({pavail:.1f}s) too short for {pseg}s; pick an earlier until_word")
        png = os.path.join(tmp, "cap_pitch.png")
        caption_png(pc.get("en", ""), pc.get("te", ""), png)
        o = os.path.join(tmp, "gpitch.mp4")
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(pc.get("start", 0)), "-i", pc["file"], "-i", png,
             "-filter_complex",
             f"[0:v]setpts={pspeed:.4f}*PTS,fps={FPS},scale=-2:{H},crop={W}:{H},setsar=1,trim=duration={pseg}[b];"
             f"[b][1:v]overlay,fade=t=in:st=0:d=0.2,fade=t=out:st={round(pseg - 0.2, 3)}:d=0.2,format=yuv420p",
             *ENC, o])
        parts.append(o)
        seg = round(seg - pseg, 3)
    speed = max(0.8, min(1.3, seg / dur(end_src)))
    o = os.path.join(tmp, "gend.mp4")
    band = os.path.join(tmp, "band.png")
    app_band_png(band)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", end_src, "-i", band, "-filter_complex",
         f"[0:v]setpts={speed:.4f}*PTS,fps={FPS},scale=-2:{H},crop={W}:{H},setsar=1,tpad=stop_mode=clone:stop_duration=8,"
         f"trim=duration={seg}[b];[b][1:v]overlay,fade=t=in:st=0:d=0.2,format=yuv420p", *ENC, o])
    parts.append(o)
    lst = os.path.join(tmp, "list.txt")
    with open(lst, "w") as f:
        f.writelines(f"file '{p}'\n" for p in parts)
    tmp_out = out[:-4] + ".tmp.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-i", voice,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "apad,loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:a", "aac", "-b:a", "160k", "-ar", "44100", "-shortest", tmp_out])
    os.replace(tmp_out, out)
    print(f"{out}: {dur(out):.1f}s, {os.path.getsize(out)/1e6:.1f} MB, scene changes at "
          + ", ".join(f"{b:.2f}" for b in breaks))


if __name__ == "__main__":
    main()
