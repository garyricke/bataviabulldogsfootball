#!/usr/bin/env python3
"""Crop the real Story-of-the-Season cards from the screenshot and composite a fan."""
import math
from PIL import Image, ImageFilter, ImageDraw

SRC = "assets/sots-grid-raw.png"
OUT = "generated_imgs/sots-fan.png"
im = Image.open(SRC).convert("RGB")
W, H = im.size
px = im.load()

def near_white(x, y):
    r, g, b = px[x, y]
    return r > 236 and g > 236 and b > 236

# --- whiteness profiles to find gutters ---
ylo, yhi = 150, 1385
col_white = []
for x in range(W):
    c = sum(near_white(x, y) for y in range(ylo, yhi, 3))
    col_white.append(c / len(range(ylo, yhi, 3)))
xlo, xhi = 28, 1903
row_white = []
for y in range(H):
    c = sum(near_white(x, y) for x in range(xlo, xhi, 3))
    row_white.append(c / len(range(xlo, xhi, 3)))

def ranges(profile, thresh, minlen):
    out, start = [], None
    for i, v in enumerate(profile):
        if v < thresh and start is None:
            start = i
        elif v >= thresh and start is not None:
            if i - start >= minlen:
                out.append((start, i))
            start = None
    if start is not None and len(profile) - start >= minlen:
        out.append((start, len(profile)))
    return out

cols = ranges(col_white, 0.84, 180)   # 4 columns
rows = ranges(row_white, 0.84, 300)   # 2 card rows (thin title/pill bands filtered by minlen)
print("cols:", cols)
print("rows:", rows)

INSET = 5
def crop(cx, cy):
    x0, x1 = cols[cx]; y0, y1 = rows[cy]
    return im.crop((x0 + INSET, y0 + INSET, x1 - INSET, y1 - INSET)).convert("RGBA")

def rounded(card, rad_frac=0.05):
    w, h = card.size
    rad = int(min(w, h) * rad_frac)
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=rad, fill=255)
    card.putalpha(mask)
    return card

# pick cards: (row, col) -> yearbook, ch14, ch13, ch12, ch11
picks = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0)]
cards = [rounded(crop(c, r)) for (r, c) in picks]

# --- composite a fan ---
CW, CH = 1920, 1080
canvas = Image.new("RGBA", (CW, CH), (20, 18, 16, 255))
# subtle vignette glow
glow = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse([CW*0.2, -CH*0.5, CW*0.8, CH*0.9], fill=(166, 25, 46, 60))
canvas = Image.alpha_composite(canvas, glow.filter(ImageFilter.GaussianBlur(180)))

n = len(cards)
target_h = 800
angles = [22 - 44 * i / (n - 1) for i in range(n)]
xs = [300 + (1620 - 300) * i / (n - 1) for i in range(n)]
for i, card in enumerate(cards):
    scale = target_h / card.height
    c = card.resize((max(1, int(card.width * scale)), target_h), Image.LANCZOS)
    rot = c.rotate(angles[i], expand=True, resample=Image.BICUBIC)
    t = (i - (n - 1) / 2) / ((n - 1) / 2)
    cx = int(xs[i]); cy = int(486 + 96 * (t * t))
    px0 = cx - rot.width // 2; py0 = cy - rot.height // 2
    # shadow
    sh = Image.new("RGBA", rot.size, (0, 0, 0, 0))
    sh.putalpha(rot.split()[3].point(lambda a: int(a * 0.55)))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    canvas.alpha_composite(sh, (px0 + 12, py0 + 20))
    canvas.alpha_composite(rot, (px0, py0))

canvas.convert("RGB").save(OUT, quality=94)
print("saved", OUT, canvas.size)
