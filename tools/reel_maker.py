"""Generate a 1080x1920 educational Reel (silent MP4) from a scene spec.

Usage: python3 reel_maker.py spec.json out.mp4
"""
import json, math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
FONT_DIR = "/usr/share/fonts/truetype/google-fonts/"
F = lambda w, s: ImageFont.truetype(FONT_DIR + f"Poppins-{w}.ttf", s)

# Brand palette
DEEP = (22, 66, 44)        # deep leaf green
LEAF = (74, 140, 72)       # mid green
LIME = (176, 214, 98)      # fresh accent
CREAM = (250, 246, 234)    # background
EARTH = (139, 94, 52)      # warm brown
INK = (28, 36, 30)


def ease(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def leaf(draw, cx, cy, size, angle, color):
    """Simple leaf: a pointed ellipse with a midrib, rotated."""
    pts = []
    for i in range(60):
        a = 2 * math.pi * i / 60
        x = size * math.cos(a)
        y = size * 0.42 * math.sin(a) * (1 - 0.35 * math.cos(a))
        r = math.radians(angle)
        pts.append((cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)))
    draw.polygon(pts, fill=color)
    r = math.radians(angle)
    draw.line([(cx - size * math.cos(r), cy - size * math.sin(r)),
               (cx + size * math.cos(r), cy + size * math.sin(r))],
              fill=tuple(min(255, c + 40) for c in color), width=max(2, size // 25))


def background(t_global, scene_idx, theme):
    bg = DEEP if theme == "dark" else CREAM
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img, "RGBA")
    # drifting decorative leaves
    specs = [(140, 260, 150, -30), (960, 420, 120, 40), (120, 1650, 170, 20),
             (940, 1720, 140, -50), (900, 980, 90, 10)]
    for i, (x, y, s, a) in enumerate(specs):
        dx = 18 * math.sin(t_global * 0.8 + i)
        dy = 14 * math.cos(t_global * 0.6 + i * 1.3)
        col = (*LIME, 38) if theme == "dark" else (*LEAF, 30)
        leaf(d, x + dx, y + dy, s, a + 6 * math.sin(t_global * 0.5 + i), col)
    return img


def draw_scene(img, scene, t, theme):
    d = ImageDraw.Draw(img, "RGBA")
    fg = CREAM if theme == "dark" else INK
    accent = LIME if theme == "dark" else LEAF
    y = scene.get("top", 640) + 110
    items = scene["items"]
    for k, it in enumerate(items):
        appear = ease((t - 0.12 - k * 0.18) / 0.45)
        if appear <= 0:
            continue
        kind = it["type"]
        alpha = int(255 * appear)
        off = int(60 * (1 - appear))
        if kind == "tag":
            f = F("Medium", 40)
            tw = d.textlength(it["text"], font=f)
            x0 = (W - tw) / 2 - 36
            d.rounded_rectangle([x0, y + off, x0 + tw + 72, y + off + 76], radius=38,
                                fill=(*accent, int(alpha * 0.9)))
            d.text((W / 2, y + off + 38), it["text"], font=f, anchor="mm",
                   fill=(*(DEEP if theme == "dark" else CREAM), alpha))
            y += 120
        elif kind in ("title", "big", "body"):
            size = {"title": 96, "big": 150, "body": 54}[kind]
            weight = {"title": "Bold", "big": "Bold", "body": "Regular"}[kind]
            f = F(weight, it.get("size", size))
            col = accent if it.get("accent") else fg
            for line in wrap(d, it["text"], f, W - 160):
                d.text((W / 2, y + off), line, font=f, anchor="mt", fill=(*col, alpha))
                y += int(f.size * 1.22)
            y += 30
        elif kind == "bars":
            # animated % Daily Value bars: items = [{"label", "pct", "amount"}]
            fl, fa, fp = F("Medium", 46), F("Regular", 34), F("Bold", 50)
            x0, x1, bh = 110, W - 110, 34
            for j, b in enumerate(it["items"]):
                a2 = ease((t - 0.3 - j * 0.28) / 0.5)
                if a2 <= 0:
                    y += 150
                    continue
                al = int(255 * min(1, a2 * 1.4))
                d.text((x0, y), b["label"], font=fl, fill=(*fg, al))
                if b.get("amount"):
                    lw = d.textlength(b["label"] + "  ", font=fl)
                    d.text((x0 + lw, y + 10), b["amount"], font=fa, fill=(*fg, int(al * 0.65)))
                pct = b["pct"]
                shown = int(round(pct * a2))
                d.text((x1, y - 4), f"{shown}%", font=fp, anchor="ra", fill=(*accent, al))
                by = y + 68
                d.rounded_rectangle([x0, by, x1, by + bh], radius=bh // 2, fill=(*fg, 34))
                fillw = (x1 - x0) * min(pct, 100) / 100 * a2
                if fillw > bh:
                    d.rounded_rectangle([x0, by, x0 + fillw, by + bh], radius=bh // 2, fill=(*accent, 235))
                y += 150
            if it.get("note"):
                d.text((W / 2, y + 6), it["note"], font=F("Light", 30), anchor="mt", fill=(*fg, 150))
                y += 50
        elif kind == "bullets":
            f = F("Medium", 56)
            for j, b in enumerate(it["items"]):
                a2 = ease((t - 0.25 - j * 0.22) / 0.4)
                if a2 <= 0:
                    y += 120
                    continue
                o2 = int(50 * (1 - a2))
                d.ellipse([150 - o2, y + 18, 186 - o2, y + 54], fill=(*accent, int(255 * a2)))
                lines = wrap(d, b, f, W - 330)
                for line in lines:
                    d.text((220 - o2, y), line, font=f, fill=(*fg, int(255 * a2)))
                    y += 74
                y += 46
        elif kind == "price":
            f1, f2 = F("Bold", 120), F("Regular", 60)
            d.text((W / 2, y + off), it["now"], font=f1, anchor="mt", fill=(*accent, alpha))
            y += 150
            if it.get("was"):
                tx = it["was"]
                tw = d.textlength(tx, font=f2)
                d.text((W / 2, y + off), tx, font=f2, anchor="mt", fill=(*fg, int(alpha * 0.6)))
                d.line([(W / 2 - tw / 2 - 6, y + off + 42), (W / 2 + tw / 2 + 6, y + off + 42)],
                       fill=(*fg, int(alpha * 0.6)), width=5)
                y += 100
        elif kind == "button":
            f = F("Bold", 52)
            tw = d.textlength(it["text"], font=f)
            x0 = (W - tw) / 2 - 60
            d.rounded_rectangle([x0, y + off, x0 + tw + 120, y + off + 120], radius=60,
                                fill=(*EARTH, alpha))
            d.text((W / 2, y + off + 60), it["text"], font=f, anchor="mm", fill=(*CREAM, alpha))
            y += 170
        elif kind == "small":
            f = F("Light", 34)
            for line in wrap(d, it["text"], f, W - 200):
                d.text((W / 2, y + off), line, font=f, anchor="mt", fill=(*fg, int(alpha * 0.75)))
                y += 46


def chrome(img, frac, theme, handle):
    d = ImageDraw.Draw(img, "RGBA")
    fg = CREAM if theme == "dark" else INK
    # progress bar (safe area: kept below Instagram's top UI)
    d.rounded_rectangle([80, 150, W - 80, 160], radius=5, fill=(*fg, 40))
    d.rounded_rectangle([80, 150, 80 + (W - 160) * frac, 160], radius=5, fill=(*LIME, 230))
    # company logo on a white badge (replaces the old text handle)
    global _LOGO
    if "_LOGO" not in globals():
        import os
        lg = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "logo.png")).convert("RGBA")
        _LOGO = lg.resize((200, round(lg.height * 200 / lg.width)), Image.LANCZOS)
    pad = 16
    bw, bh = _LOGO.width + 2 * pad, _LOGO.height + 2 * pad
    x0, y0 = W // 2 - bw // 2, 190
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=26, fill=(255, 255, 255, 242))
    if img.mode == "RGBA":
        img.alpha_composite(_LOGO, (x0 + pad, y0 + pad))
    else:
        img.paste(_LOGO, (x0 + pad, y0 + pad), _LOGO)


def main(spec_path, out_path):
    spec = json.load(open(spec_path))
    av = spec.get("avatar")
    if av:
        import numpy as np
        from avatar import render_avatar, AV_W, AV_H
        av_imgs = {(m, b): render_avatar(m, b) for m in range(4) for b in (False, True)}
        env = np.load(av["envelope"]) if av.get("envelope") else None
        av_xy = ((W - AV_W) // 2, av.get("top", 1270))
    scenes = spec["scenes"]
    durs = [s.get("dur", 3.0) for s in scenes]
    total = sum(durs)
    nframes = int(total * FPS)
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
         "-shortest", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart",
         out_path], stdin=subprocess.PIPE)
    for fi in range(nframes):
        tg = fi / FPS
        acc, si = 0.0, 0
        while si < len(scenes) - 1 and tg >= acc + durs[si]:
            acc += durs[si]
            si += 1
        t = tg - acc
        sc = scenes[si]
        theme = sc.get("theme", "light")
        img = background(tg, si, theme)
        draw_scene(img, sc, t, theme)
        chrome(img, tg / total, theme, spec.get("handle", ""))
        # quick fade between scenes
        fade = min(1.0, t / 0.18) if si > 0 else 1.0
        if fade < 1.0:
            prev_theme = scenes[si - 1].get("theme", "light")
            base = Image.new("RGB", (W, H), DEEP if prev_theme == "dark" else CREAM)
            img = Image.blend(base, img, fade)
        if av:
            lvl = float(env[min(fi, len(env) - 1)]) if env is not None else 0.0
            mouth = 0 if lvl < 0.08 else 1 if lvl < 0.25 else 2 if lvl < 0.5 else 3
            blink = (tg % 3.7) < 0.12
            av_base = img.convert("RGBA")
            av_base.alpha_composite(av_imgs[(mouth, blink)], av_xy)
            img = av_base.convert("RGB")
        proc.stdin.write(img.tobytes())
    proc.stdin.close()
    proc.wait()
    # cover image = a frame from the hook scene
    print(f"done {out_path} {total:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
