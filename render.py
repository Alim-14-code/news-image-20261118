#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page to entry.png (1024x1024).

Deterministic, offline: all copy is baked in below (researched 18 Nov 2026,
sources listed in README.md). Run:  python3 render.py  ->  entry.png
The entry program (main.py) ships the finished PNG and copies it to
/output/entry.png with stdlib only, so grading needs no fonts or Pillow.

Round 3: new lead and new breadth. R2 led with Kerch and was almost all war;
R3 leads with the Gulf escalation — the day's freshest big story, fought
overnight 17-18 Nov — and adds the stories R2 missed: Alaska handing
Democrats the Senate, Ebola passing 11,000 cases, the An-12 crash, the
Knesset speaker vote and Cyclone Xavier. The Kerch bridge stays, as the
war's second story, with the drone figure corrected to the verified 1,336.
Every fact below was reported on 18 November 2026; claims stay attributed.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (251, 248, 241)
INK = (25, 21, 18)
SLATE = (52, 52, 58)          # steel: dark, not pure black
MUTED = (107, 98, 87)
RED = (158, 27, 27)
BLUE = (46, 74, 98)
RULE = (216, 208, 191)
SKY_TOP = (238, 226, 205)     # dusk sky, warm at the top
SKY_BOT = (203, 220, 228)
SUN = (232, 196, 120)
WATER = (127, 163, 181)
WATER_D = (46, 74, 98)
SMOKE = (150, 148, 140)
SMOKE_D = (120, 118, 112)

F = "/usr/share/fonts/truetype/noto/"
def font(name, size):
    return ImageFont.truetype(F + name, size)

SERIF_B = lambda s: font("NotoSerif-Bold.ttf", s)
SERIF = lambda s: font("NotoSerif-Regular.ttf", s)
SERIF_I = lambda s: font("NotoSerif-Italic.ttf", s)
SANS_B = lambda s: font("NotoSans-Bold.ttf", s)
SANS = lambda s: font("NotoSans-Regular.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def wrap(text, fnt, width):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(text, fnt, x, y, width, fill, leading):
    """Draw wrapped paragraph; returns y after last line."""
    for line in wrap(text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y

def tracked(text, fnt, x, y, fill, tracking=2):
    """Draw letterspaced caps text; returns width used."""
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=fnt, fill=fill)
        cx += d.textlength(ch, font=fnt) + tracking
    return cx - x

MX = 36            # side margin
RX = 700           # right rail x
RW = 1024 - MX - RX  # right rail width = 288

# ---------------------------------------------------------------- masthead
d.text((MX, 26), "THE WORLD IN ONE PAGE", font=SERIF_B(64), fill=INK)
tracked("WEDNESDAY, 18 NOVEMBER 2026", SANS_B(17), MX, 112, MUTED, tracking=1)
d.text((1024 - MX - d.textlength("ONE DAY · 18 NOV 2026", font=SANS_B(18)), 108),
       "ONE DAY · 18 NOV 2026", font=SANS_B(18), fill=RED)
d.line([(MX, 140), (1024 - MX, 140)], fill=INK, width=3)
d.line([(MX, 146), (1024 - MX, 146)], fill=RED, width=2)

# ---------------------------------------------------------------- lead story
LY = 168
tracked("THE GULF  ·  WAR IN THE STRAIT", SANS_B(19), MX, LY, RED, tracking=2)
y = para("Iran widens the war to Kuwait",
         SERIF_B(52), MX, LY + 26, 628, INK, 58)
# deck
y = para("Overnight, Iranian drones struck a US base in Kuwait and at Bahrain, "
        "hours after US jets hit a missile site on Iran's Qeshm Island. "
        "Tehran says it downed a US MQ-9.",
        SANS(22), MX, y + 4, 628, (58, 52, 44), 27)

# ---- drawn illustration: the Strait of Hormuz at dusk, flat editorial style
IX, IY, IW, IH = MX, y + 8, 628, 170
d.rectangle([IX, IY, IX + IW, IY + IH], outline=INK, width=2)
# dusk sky in bands, warm top to pale blue at the horizon
for i in range(88):
    t = i / 87
    c = tuple(int(SKY_TOP[k] + (SKY_BOT[k] - SKY_TOP[k]) * t) for k in range(3))
    d.line([(IX, IY + i), (IX + IW, IY + i)], fill=c)
d.rectangle([IX, IY + 88, IX + IW, IY + IH], fill=WATER)  # strait
# low sun, half behind the far headland
d.ellipse([IX + 452, IY + 48, IX + 496, IY + 92], fill=SUN)
# distant headland
d.polygon([(IX, IY + 88), (IX + 90, IY + 64), (IX + 150, IY + 88)], fill=(168, 178, 172))
# drones in the sky, small dark marks with short trails
for dx, dy in ((IX + 150, IY + 52), (IX + 196, IY + 32), (IX + 238, IY + 48)):
    d.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=SLATE)
    d.line([(dx - 16, dy), (dx - 7, dy)], fill=SLATE, width=2)
# tanker: long dark hull, deckhouse, funnel; smoke rising midship (hit)
d.rectangle([IX + 90, IY + 112, IX + 500, IY + 134], fill=SLATE)          # hull
d.polygon([(IX + 500, IY + 112), (IX + 540, IY + 123), (IX + 500, IY + 134)], fill=SLATE)  # bow
d.rectangle([IX + 420, IY + 92, IX + 470, IY + 112], fill=SLATE)          # deckhouse
d.rectangle([IX + 380, IY + 100, IX + 392, IY + 112], fill=SLATE)         # funnel
# smoke plumes over the hit: a rising column rooted on the hull, dark core inside pale
for cx, cy, r in ((IX + 300, IY + 102, 10), (IX + 308, IY + 84, 13), (IX + 318, IY + 64, 10)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
d.ellipse([IX + 302, IY + 78, IX + 314, IY + 90], fill=SMOKE_D)
# waves, lighter and fewer
for wy in (142, 154, 164):
    for wx in range(0, IW, 58):
        d.arc([IX + wx, IY + wy, IX + wx + 34, IY + wy + 12], start=180, end=360,
              fill=WATER_D, width=2)
# small patrol boat
d.polygon([(IX + 520, IY + 146), (IX + 580, IY + 146), (IX + 568, IY + 158), (IX + 532, IY + 158)], fill=BLUE)
d.line([(IX + 550, IY + 146), (IX + 550, IY + 130)], fill=BLUE, width=3)
d.polygon([(IX + 550, IY + 130), (IX + 570, IY + 144), (IX + 550, IY + 144)], fill=BLUE)
CAP_Y = IY + IH + 8
cap_end = para("The Strait of Hormuz at dusk. A tanker was hit; one sailor is missing. Illustration.",
     SERIF_I(16), IX, CAP_Y, IW, MUTED, 19)

# ---- in numbers: one more field (health / disaster / politics) in the left column
NY = cap_end + 12
d.line([(IX, NY), (IX + IW, NY)], fill=RULE, width=1)
tracked("IN NUMBERS", SANS_B(16), IX, NY + 10, INK, tracking=2)
NUMBERS = [
    ("11,000+", "Ebola cases; 5,400 dead"),
    ("19", "dead in the An-12 crash"),
    ("56", "Democratic Senate seats"),
]
col_n = IW // 3
for i, (num, label) in enumerate(NUMBERS):
    nx = IX + i * col_n
    d.text((nx, NY + 32), num, font=SANS_B(20), fill=RED)
    para(label, SANS(14), nx, NY + 58, col_n - 12, (58, 52, 44), 18)
num_end = NY + 58 + 18

# ---------------------------------------------------------------- right rail
tracked("THE DAY IN BRIEF", SANS_B(19), RX, LY, INK, tracking=2)
d.line([(RX, LY + 30), (1024 - MX, LY + 30)], fill=INK, width=2)

BRIEFS = [
    ("UKRAINE", "Kerch span down, grain at risk",
     "A road span lies in the strait after the second strike in two "
     "days; rail is back on one track. Moscow counts 1,336 drones."),
    ("BUSINESS", "Nvidia tops forecasts, no Huang return",
     "Revenue more than doubled to $115.8bn without its founder; the "
     "board will not bring Jensen Huang back."),
    ("WASHINGTON", "Alaska hands Democrats the Senate",
     "The AP calls it for Mary Peltola, 50.12% — the first Democrat "
     "to win the seat since 2008."),
]
by = LY + 44
for kicker, head, body in BRIEFS:
    tracked(kicker, SANS_B(16), RX, by, RED, tracking=2)
    by += 22
    by = para(head, SANS_B(22), RX, by, RW, INK, 25)
    by = para(body, SANS(16), RX, by + 3, RW, (58, 52, 44), 20)
    by += 12
    d.line([(RX, by), (1024 - MX, by)], fill=RULE, width=1)
    by += 12
# rail divider: runs alongside the briefs only, stops at the last one
d.line([(RX - 24, LY), (RX - 24, by - 12)], fill=RULE, width=2)

# ---------------------------------------------------------------- markets strip
MY = max(num_end, by) + 12
d.line([(MX, MY), (1024 - MX, MY)], fill=INK, width=2)
d.text((MX, MY + 10), "MARKETS  ·  TUESDAY CLOSE", font=SANS_B(13), fill=MUTED)
mk = [("DOW", "50,759", "–849  –1.6%"),
      ("S&P 500", "7,341", "–76  –1.0%"),
      ("NASDAQ", "24,328", "–181  –0.7%"),
      ("SALESFORCE", "$194.52", "–9.5%")]
mx = MX
for name, val, chg in mk:
    d.text((mx, MY + 30), name, font=SANS_B(11), fill=MUTED)
    d.text((mx, MY + 44), val, font=SANS_B(18), fill=INK)
    d.text((mx + d.textlength(val, font=SANS_B(18)) + 8, MY + 48),
           chg, font=SANS_B(13), fill=RED)
    mx += 232
mk_end = MY + 66

# ---------------------------------------------------------------- also today
AY = mk_end + 14
d.line([(MX, AY), (1024 - MX, AY)], fill=INK, width=2)
tracked("ALSO TODAY", SANS_B(18), MX, AY + 12, RED, tracking=2)
ALSO = [
    ("KAHANA TAKES THE KNESSET",
     "Israel's parliament elects Matan Kahana speaker, 66 votes of 120, as Netanyahu's rivals take control."),
    ("CYCLONE XAVIER, CATEGORY 5",
     "The season's fiercest storm hits the Northern Cook Islands; Cyclone Akvan bears down on Andhra Pradesh."),
    ("DHONI BOWS OUT OF THE IPL",
     "After 278 matches and five titles, MS Dhoni retires as a player and becomes Chennai's mentor from 2027."),
    ("QUAD MEETS IN MANILA",
     "Trump and the Quad leaders agree steps on critical minerals; APEC opens in Shenzhen ahead of Thursday's three-way summit."),
]
col_w = (1024 - 2 * MX - 40) // 2
ay = AY + 40
for i, (head, body) in enumerate(ALSO):
    ax = MX if i % 2 == 0 else MX + col_w + 40
    ayy = ay + (i // 2) * 58
    d.text((ax, ayy), head, font=SANS_B(17), fill=INK)
    para(body, SANS(15), ax, ayy + 22, col_w, (58, 52, 44), 19)
also_end = ay + 116

# ---------------------------------------------------------------- footer
d.line([(MX, 992), (1024 - MX, 992)], fill=RULE, width=1)
d.text((MX, 1000), "Sources: AP · Reuters · Bloomberg · BBC · UN — "
                  "events reported on 18 November 2026. Claims are attributed, not asserted.",
       font=SANS(14), fill=MUTED)

print("layout: cap_end", cap_end, "num_end", num_end, "rail_end", by,
      "markets", MY, mk_end, "also", AY, also_end)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
