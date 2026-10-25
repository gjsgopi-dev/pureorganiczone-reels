"""Illustrated presenter: an Indian woman in a saree, drawn in flat vector style.

render_avatar(mouth, blink) -> RGBA image (AV_W x AV_H)
mouth: 0 closed, 1 slightly open, 2 open, 3 wide; blink: True draws closed eyes.
"""
from PIL import Image, ImageDraw, ImageFilter

S = 2                      # supersample factor for smooth edges
AV_W, AV_H = 480, 520      # final size
SKIN = (196, 136, 94)
SKIN_SH = (172, 114, 76)
HAIR = (34, 22, 18)
BLOUSE = (128, 28, 44)
SAREE = (36, 104, 64)
BORDER = (214, 168, 64)
GOLD = (222, 176, 70)
JASMINE = (250, 248, 238)
LIP = (150, 46, 56)
MOUTH_IN = (82, 22, 30)
EYE_W = (250, 246, 240)
IRIS = (40, 24, 18)
BINDI = (196, 30, 40)


def _e(d, cx, cy, rx, ry, **kw):
    d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], **kw)


def render_avatar(mouth=0, blink=False):
    W, H = AV_W * S, AV_H * S
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = AV_W / 2

    # hair behind head, with a side bun and jasmine gajra
    _e(d, cx, 175, 118, 140, fill=HAIR)
    _e(d, cx + 112, 150, 52, 50, fill=HAIR)
    for i in range(9):
        import math
        a = math.radians(-70 + i * 20)
        _e(d, cx + 112 + 54 * math.cos(a), 150 + 52 * math.sin(a), 11, 11, fill=JASMINE)

    # shoulders: blouse, then saree pallu across one shoulder with gold border
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    sd.rectangle([0, 380 * S, W, H], fill=BLOUSE)
    pallu = [(cx - 40) * S, 390 * S, (cx + 230) * S, 390 * S, (cx + 230) * S, (AV_H + 10) * S, (cx - 150) * S, (AV_H + 10) * S]
    sd.polygon(list(zip(pallu[::2], pallu[1::2])), fill=SAREE)
    sd.line([((cx - 40) * S, 392 * S), ((cx - 150) * S, (AV_H + 10) * S)], fill=BORDER, width=18 * S)
    sd.line([((cx - 12) * S, 396 * S), ((cx - 118) * S, (AV_H + 10) * S)], fill=BORDER, width=5 * S)
    for k in range(6):  # small gold motifs on the pallu
        x, y = cx + 40 + (k % 3) * 46, 440 + (k // 3) * 44
        sd.ellipse([(x - 7) * S, (y - 7) * S, (x + 7) * S, (y + 7) * S], fill=BORDER)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rounded_rectangle([(cx - 190) * S, 400 * S, (cx + 190) * S, (AV_H + 60) * S],
                                           radius=110 * S, fill=255)
    img.paste(sh, (0, 0), mask)
    d = ImageDraw.Draw(img)

    # neck and face
    d.rounded_rectangle([(cx - 40) * S, 300 * S, (cx + 40) * S, 410 * S], radius=30 * S, fill=SKIN_SH)
    _e(d, cx, 205, 98, 122, fill=SKIN)
    # ears with jhumkas
    for side in (-1, 1):
        ex = cx + side * 96
        _e(d, ex, 212, 16, 26, fill=SKIN_SH)
        _e(d, ex, 246, 9, 9, fill=GOLD)
        d.pieslice([(ex - 18) * S, 250 * S, (ex + 18) * S, 286 * S], 180, 360, fill=GOLD)
        for b in range(5):
            _e(d, ex - 14 + b * 7, 270, 3, 3, fill=GOLD)

    # hair framing the forehead, centre parting
    d.chord([(cx - 104) * S, 70 * S, (cx + 104) * S, 230 * S], 180, 360, fill=HAIR)
    d.line([(cx * S, 74 * S), (cx * S, 118 * S)], fill=SKIN_SH, width=3 * S)

    # eyebrows
    for side in (-1, 1):
        bx = cx + side * 40
        d.arc([(bx - 30) * S, 148 * S, (bx + 30) * S, 176 * S], 200 if side < 0 else 200, 340, fill=HAIR, width=6 * S)

    # eyes
    for side in (-1, 1):
        ex = cx + side * 40
        if blink:
            d.arc([(ex - 22) * S, 182 * S, (ex + 22) * S, 206 * S], 10, 170, fill=HAIR, width=5 * S)
        else:
            _e(d, ex, 192, 22, 13, fill=EYE_W)
            _e(d, ex + side * 1, 193, 10, 11, fill=IRIS)
            _e(d, ex + side * 1 - 3, 189, 3, 3, fill=(255, 255, 255))
            d.arc([(ex - 24) * S, 176 * S, (ex + 24) * S, 206 * S], 195, 345, fill=HAIR, width=5 * S)  # lash line / kajal

    # bindi, nose with small gold stud
    _e(d, cx, 160, 7, 7, fill=BINDI)
    d.line([(cx * S, 200 * S), ((cx - 6) * S, 236 * S), ((cx + 6) * S, 240 * S)], fill=SKIN_SH, width=4 * S)
    _e(d, cx + 13, 236, 4, 4, fill=GOLD)

    # cheeks
    for side in (-1, 1):
        _e(d, cx + side * 56, 238, 16, 10, fill=(204, 133, 100))

    # mouth (4 states)
    my = 268
    if mouth == 0:
        d.rounded_rectangle([(cx - 24) * S, (my - 4) * S, (cx + 24) * S, (my + 6) * S], radius=6 * S, fill=LIP)
    else:
        h = {1: 9, 2: 15, 3: 21}[mouth]
        _e(d, cx, my + h / 3, 24, h, fill=LIP)
        _e(d, cx, my + h / 3, 17, max(3, h - 6), fill=MOUTH_IN)
        if mouth >= 2:
            d.rectangle([(cx - 12) * S, (my + h / 3 - h + 6) * S, (cx + 12) * S, (my + h / 3 - h + 10) * S], fill=(245, 240, 232))

    # gold necklace
    d.arc([(cx - 52) * S, 330 * S, (cx + 52) * S, 400 * S], 20, 160, fill=GOLD, width=6 * S)
    _e(d, cx, 398, 9, 9, fill=GOLD)

    img = img.resize((AV_W, AV_H), Image.LANCZOS)
    return img


if __name__ == "__main__":
    row = Image.new("RGBA", (AV_W * 5, AV_H), (248, 244, 232, 255))
    for i, (m, b) in enumerate([(0, False), (1, False), (2, False), (3, False), (0, True)]):
        a = render_avatar(m, b)
        row.alpha_composite(a, (i * AV_W, 0))
    row.convert("RGB").save("/tmp/avatar_states.png")
    print("saved")
