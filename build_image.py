#!/usr/bin/env python3
"""Build entry.png: a 1024x1024 news-summary infographic for 17 November 2026.

Build-time tool only (uses Pillow + system DejaVu fonts, available on this VM).
The entry program itself (main.ts, Node stdlib) decodes the finished PNG from
its base64 text form (entry.png.b64, made with `base64 -w0 entry.png`) and
writes it to /output/entry.png, so grading is fully deterministic and needs
no network. The binary entry.png itself is git-ignored in the entry dir (the
connector push path is UTF-8 text only).

Stories were supplied as verified 17 Nov 2026 news, cross-checked on 18 Nov
against Reuters, AP, NPR, AFP and Standard Topic.
See news.json for the same data in machine-readable form.
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W, H = 1024, 1024

NAVY = (14, 42, 71)
GOLD = (232, 184, 75)
INK = (17, 24, 39)
GREY = (71, 85, 105)
LIGHT = (241, 245, 249)
CARD_BORDER = (203, 213, 225)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

f_title = ImageFont.truetype(SERIF_B, 58)
f_kicker = ImageFont.truetype(SANS_B, 21)
f_sub = ImageFont.truetype(SANS, 23)
f_tag = ImageFont.truetype(SANS_B, 17)
f_head = ImageFont.truetype(SANS_B, 25)
f_body = ImageFont.truetype(SANS, 19)
f_also = ImageFont.truetype(SANS, 19)
f_also_b = ImageFont.truetype(SANS_B, 19)
f_foot = ImageFont.truetype(SANS, 15)

NEWS = json.loads((HERE / "news.json").read_text(encoding="utf-8"))
STORIES = NEWS["stories"]

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)


def wrap(text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
            while d.textlength(cur, font=font) > max_w:
                split = len(cur) - 1
                while split and d.textlength(cur[:split], font=font) > max_w:
                    split -= 1
                if not split:
                    raise ValueError("Text area is too narrow for one character")
                lines.append(cur[:split])
                cur = cur[split:]
    if cur:
        lines.append(cur)
    return lines


def bounded_lines(text, font, max_w, max_lines):
    lines = wrap(text, font, max_w)
    if max_lines < 1:
        raise ValueError("Text area must have room for at least one line")
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1].rstrip()
        while last and d.textlength(last + "…", font=font) > max_w:
            last = last[:-1].rstrip()
        if d.textlength(last + "…", font=font) > max_w:
            raise ValueError("Text area is too narrow for an ellipsis")
        lines[-1] = last + "…"
    return lines


# ---------- header ----------
d.rectangle([0, 0, W, 168], fill=NAVY)
d.rectangle([0, 168, W, 172], fill=GOLD)
d.text((36, 26), "WORLD NEWS  •  TUESDAY", font=f_kicker, fill=GOLD)
d.text((36, 56), "17 November 2026", font=f_title, fill=WHITE)
d.text((36, 126), "The day's biggest stories, in one image", font=f_sub, fill=(186, 205, 224))
# date badge on the right
d.rounded_rectangle([828, 34, 988, 132], radius=12, outline=GOLD, width=2)
d.text((908, 48), "NOV", font=f_kicker, fill=GOLD, anchor="mt")
d.text((908, 74), "17", font=ImageFont.truetype(SERIF_B, 40), fill=WHITE, anchor="mt")

# ---------- story cards: 2 cols x 3 rows ----------
mx, my, gap = 24, 192, 16
cw = (W - 2 * mx - gap) // 2          # 480
ch = 204
for i, s in enumerate(STORIES):
    col, row = i % 2, i // 2
    x0 = mx + col * (cw + gap)
    y0 = my + row * (ch + gap)
    x1, y1 = x0 + cw, y0 + ch
    color = tuple(int(s["color"][j:j + 2], 16) for j in (1, 3, 5))
    d.rounded_rectangle([x0, y0, x1, y1], radius=14, fill=WHITE,
                        outline=CARD_BORDER, width=1)
    d.rounded_rectangle([x0, y0, x0 + 8, y1], radius=4, fill=color)
    # tag chip
    tag = s["tag"]
    tw = d.textlength(tag, font=f_tag) + 20
    d.rounded_rectangle([x0 + 22, y0 + 16, x0 + 22 + tw, y0 + 44], radius=7, fill=color)
    d.text((x0 + 32, y0 + 21), tag, font=f_tag, fill=WHITE)
    # headline (max 2 lines)
    y = y0 + 56
    for line in bounded_lines(s["headline"], f_head, cw - 44, 2):
        d.text((x0 + 22, y), line, font=f_head, fill=INK)
        y += 30
    summary_lines = wrap(s["summary"], f_body, cw - 44)
    y += 0 if len(summary_lines) > 3 else 6
    line_height = 20 if len(summary_lines) > 3 else 25
    text_bottom = f_body.getbbox(s["summary"])[3]
    max_lines = (y1 - 4 - y - text_bottom) // line_height + 1
    summary_lines = bounded_lines(s["summary"], f_body, cw - 44, max_lines)
    for line in summary_lines:
        d.text((x0 + 22, y), line, font=f_body, fill=GREY)
        y += line_height

# ---------- also-today strip ----------
ay0 = my + 3 * ch + 2 * gap + 16   # 852; band ends at 952, footer at 978
d.rounded_rectangle([mx, ay0, W - mx, ay0 + 100], radius=14, fill=LIGHT)
d.text((mx + 22, ay0 + 10), "ALSO TODAY", font=f_also_b, fill=NAVY)
also = NEWS["also_today"]
y = ay0 + 33
if len(also) > 3:
    raise ValueError("The Also today strip has room for at most three items")
for line in also:
    fitted = bounded_lines("•  " + line, f_also, W - 2 * mx - 44, 1)[0]
    d.text((mx + 22, y), fitted, font=f_also, fill=INK)
    y += 21

# ---------- footer ----------
d.text((W // 2, 978), "Sources: " + " · ".join(NEWS["sources"]) + "  —  17 November 2026",
       font=f_foot, fill=GREY, anchor="mt")

img.save(HERE / "entry.png", "PNG", optimize=True)
print("saved", HERE / "entry.png", img.size)
