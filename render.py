#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page to entry.png (1024x1024).

Deterministic, offline: all copy is baked in below (researched 18 Nov 2026,
sources listed in README.md). Run:  python3 render.py  ->  entry.png
The entry program (main.py) ships the finished PNG and copies it to
/output/entry.png with stdlib only, so grading needs no fonts or Pillow.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 48                      # side margin
CW = W - 2 * M              # 928 content width

PAPER = (251, 250, 247)
INK   = (25, 24, 23)
SOFT  = (58, 56, 53)
GREY  = (110, 106, 99)
RULE  = (217, 210, 196)
RED   = (166, 38, 30)
SEA   = (47, 74, 90)
SEA_L = (126, 154, 168)

F = "/usr/share/fonts/truetype/liberation/"
def serif(sz, bold=False, italic=False):
    name = "LiberationSerif-Bold.ttf" if bold else \
           "LiberationSerif-Italic.ttf" if italic else "LiberationSerif-Regular.ttf"
    return ImageFont.truetype(F + name, sz)
def sans(sz, bold=False):
    name = "LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"
    return ImageFont.truetype(F + name, sz)

def wrap(draw, text, font, width):
    """Greedy word wrap; returns list of lines (balanced-ish, no orphans)."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, font, width, lh, fill=INK):
    for ln in wrap(draw, text, font, width):
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y

def kicker(draw, x, y, text, size=15):
    draw.rectangle([x, y + 2, x + 10, y + 12], fill=RED)
    draw.text((x + 18, y), text, font=sans(size, bold=True), fill=RED)
    return y + size + 8

def hairline(draw, y, x0=M, x1=W - M, fill=RULE, wdt=1):
    draw.rectangle([x0, y, x1, y + wdt - 1], fill=fill)

# ---------------------------------------------------------------- canvas
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- masthead
d.text((M, 34), "THE WORLD IN ONE PAGE", font=sans(15, bold=True), fill=INK)
d.text((W - M - d.textlength("WEDNESDAY 18 NOVEMBER 2026", font=sans(15, bold=True)),
        34), "WEDNESDAY 18 NOVEMBER 2026", font=sans(15, bold=True), fill=RED)
d.text((M, 58), "The World Today", font=serif(80, bold=True), fill=INK)
d.rectangle([M, 168, W - M, 172], fill=RED)
hairline(d, 178, fill=INK)

# ---------------------------------------------------------------- lead story
y = 198
y = kicker(d, M, y, "UKRAINE  —  THE WAR IN EUROPE")
y = para(d, M, y, "Ukraine cripples the Crimean bridge as Russia hits back at Kyiv\u2019s bridges",
         serif(44, bold=True), CW, 50)
y += 8
# left: dek + facts
LX, LW = M, 556
dy = y
dy = para(d, LX, dy,
          "Kyiv says its drones and missiles brought down the road arch of the 19-km Kerch "
          "bridge \u2014 its biggest drone attack of the war, 1,441 drones in a single night. "
          "Two people were killed; traffic is halted.",
          serif(19), LW, 27)
dy += 6
dy = para(d, LX, dy,
          "Moscow answered by striking Kyiv\u2019s North and South bridges and damaging "
          "part of the metro.",
          serif(19), LW, 27)
# right: bridge schematic (flat, labelled as illustration)
BX, BY, BW, BH = 640, y - 4, 336, 148
d.rectangle([BX, BY + 96, BX + BW, BY + BH], fill=SEA)          # sea
for wx in (BX + 28, BX + 128, BX + 238):                        # wave marks
    d.arc([wx, BY + 112, wx + 44, BY + 128], 180, 360, fill=SEA_L, width=3)
    d.arc([wx + 8, BY + 126, wx + 36, BY + 140], 180, 360, fill=SEA_L, width=3)
d.rectangle([BX, BY + 88, BX + 128, BY + 96], fill=INK)         # left deck
d.rectangle([BX + 208, BY + 88, BX + BW, BY + 96], fill=INK)    # right deck
d.rectangle([BX + 40, BY + 96, BX + 48, BY + 128], fill=INK)    # pillars
d.rectangle([BX + 268, BY + 96, BX + 276, BY + 128], fill=INK)
d.polygon([(BX + 128, BY + 88), (BX + 208, BY + 96),            # fallen span
           (BX + 196, BY + 112), (BX + 128, BY + 100)], fill=(90, 88, 84))
d.ellipse([BX + 158, BY + 78, BX + 170, BY + 90], fill=RED)     # break marker
cap_y = BY + BH + 8
d.text((BX, cap_y), "The Kerch bridge: the road arch is down,",
       font=serif(14, italic=True), fill=GREY)
d.text((BX, cap_y + 18), "traffic halted.  Illustration.",
       font=serif(14, italic=True), fill=GREY)

lead_end = max(dy, cap_y + 36)
hairline(d, lead_end + 16)

# ---------------------------------------------------------------- second row
y = lead_end + 32
COLW, GAP = 452, 24
RX = M + COLW + GAP
# --- left: Nvidia
ly = kicker(d, M, y, "BUSINESS  —  TECHNOLOGY", 14)
ly = para(d, M, ly, "Nvidia posts a record $115.8bn quarter \u2014 board rules out Huang\u2019s return",
          serif(26, bold=True), COLW, 30)
ly += 5
ly = para(d, M, ly,
          "Revenue more than doubled to $115.8bn, beating the $109.1bn Wall Street expected. "
          "Interim chief Colette Kress guided to about $130bn next quarter; shares rose after hours.",
          serif(17), COLW, 24)
# --- right: Gulf
ry = kicker(d, RX, y, "THE GULF  —  IRAN AND THE US", 14)
ry = para(d, RX, ry, "Iran\u2019s third drone attack on a US radar in Bahrain in five days is intercepted",
          serif(26, bold=True), COLW, 30)
ry += 5
ry = para(d, RX, ry,
          "No damage and no injuries, US Central Command says. American jets then hit an "
          "IRGC missile site on Qeshm Island; in Manila, Trump said Iran \u201ccan\u2019t have a nuclear weapon.\u201d",
          serif(17), COLW, 24)

row2_end = max(ly, ry)
# ---------------------------------------------------------------- markets strip
hairline(d, row2_end + 14)
my = row2_end + 26
d.text((M, my), "MARKETS  ·  TUESDAY CLOSE", font=sans(13, bold=True), fill=GREY)
mk = [("DOW", "50,759", "\u2212849  \u22121.6%"),
      ("S&P 500", "7,341", "\u221276  \u22121.0%"),
      ("NASDAQ", "24,328", "\u2212181  \u22120.7%"),
      ("SALESFORCE", "$194.52", "\u22129.5%")]
mx = M
for name, val, chg in mk:
    d.text((mx, my + 22), name, font=sans(12, bold=True), fill=GREY)
    d.text((mx, my + 38), val, font=sans(20, bold=True), fill=INK)
    d.text((mx + d.textlength(val, font=sans(20, bold=True)) + 10, my + 43),
           chg, font=sans(15, bold=True), fill=RED)
    mx += 232
mk_end = my + 60
hairline(d, mk_end)

# ---------------------------------------------------------------- also today
y = mk_end + 12
d.text((M, y), "ALSO TODAY", font=sans(14, bold=True), fill=RED)
y += 24
briefs = [
    ("MANILA  —  DIPLOMACY",
     "Trump meets the Quad leaders \u2014 Japan, India and Australia \u2014 in Manila, ahead of talks with Putin and Xi."),
    ("CRICKET  —  INDIA",
     "MS Dhoni retires from the IPL and becomes mentor of the Chennai Super Kings."),
    ("WEATHER  —  BAY OF BENGAL",
     "Cyclone Akvan is expected to strengthen into a severe cyclonic storm over the bay."),
    ("TRADE  —  AHEAD OF APEC",
     "Canada and China extend trade deals ahead of APEC; Britain sanctions Israeli settlement firms."),
]
by = y
for i, (h, b) in enumerate(briefs):
    bx = M if i % 2 == 0 else RX
    byy = by + (i // 2) * 60
    d.text((bx, byy), h, font=sans(13, bold=True), fill=INK)
    para(d, bx, byy + 17, b, serif(15), COLW, 18, fill=SOFT)
briefs_end = by + 120

# ---------------------------------------------------------------- footer
hairline(d, briefs_end + 12, fill=INK)
d.text((M, briefs_end + 20), "Sources: Reuters, TechCrunch, MarketWatch, CNBC. Every event above was first reported on 18 November 2026.",
       font=sans(12), fill=GREY)
print("layout: lead_end", lead_end, "row2_end", row2_end, "mk_end", mk_end,
      "briefs_end", briefs_end, "footer", briefs_end + 20)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG", optimize=True)
print("saved", out, os.path.getsize(out), "bytes")
