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

Round 4: same lead, verified again and sharpened — the MQ-9 claim is now
an 18 November event, and the gas carrier Tara Gas caught fire too.
New this round: the NSA network outage gets its own brief (it was buried
in R3's markets strip), the Trump-Xi-Putin summit is confirmed for
Thursday in Shenzhen, the Knesset vote is given as 66-52, Xavier gets its
220 km/h wind speed, Akvan gets its orange alert, Dhoni's No. 7 shirt
retires, and the markets strip swaps unverified Salesforce for Brent
oil. The lead art is a fresh generated dusk illustration of the strait,
embedded as art-hormuz-dusk.png; all text stays Pillow-rendered so it
stays crisp. IN NUMBERS drops the Senate figure (it duplicates the
Alaska brief) for the 1,336 drones Moscow counts.
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
y = para("Overnight, Iranian drones hit a US base in Kuwait and at Bahrain, "
        "hours after US jets struck Qeshm Island. Tehran says it downed "
        "a US MQ-9.",
        SANS(22), MX, y + 4, 628, (58, 52, 44), 27)

# ---- lead illustration: generated dusk scene of the Strait of Hormuz
IX, IY, IW, IH = MX, y + 8, 628, 170
art = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "art-hormuz-dusk.png")).convert("RGB")
art = art.resize((IW, IH), Image.LANCZOS)
img.paste(art, (IX, IY))
d.rectangle([IX, IY, IX + IW, IY + IH], outline=INK, width=2)
CAP_Y = IY + IH + 8
cap_end = para("The Strait of Hormuz at dusk. A ship was hit and a gas carrier "
     "caught fire; one sailor is missing. Illustration.",
     SERIF_I(16), IX, CAP_Y, IW, MUTED, 19)

# ---- in numbers: one more field (health / disaster / politics) in the left column
NY = cap_end + 12
d.line([(IX, NY), (IX + IW, NY)], fill=RULE, width=1)
tracked("IN NUMBERS", SANS_B(16), IX, NY + 10, INK, tracking=2)
NUMBERS = [
    ("11,000+", "Ebola cases; 5,400 dead"),
    ("19", "dead in the An-12 crash"),
    ("1,336", "drones Moscow counts"),
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
    ("UKRAINE", "Kerch span is down",
     "Second strike in two days drops a road span; rail is back on one "
     "track. Moscow counts 1,336 drones."),
    ("BUSINESS", "Nvidia beats forecasts",
     "Revenue more than doubled to $115.8bn; the board rules out "
     "Huang's return, guides $130bn next quarter."),
    ("WASHINGTON", "Alaska flips the Senate",
     "Mary Peltola wins, just over 50% — the first Democrat in the "
     "seat since 2008."),
    ("TECHNOLOGY", "NSA network goes down",
     "The spy agency's classified net failed after a patch; no sign "
     "of attack. The Dow fell 849 points."),
]
by = LY + 44
for kicker, head, body in BRIEFS:
    tracked(kicker, SANS_B(16), RX, by, RED, tracking=2)
    by += 20
    by = para(head, SANS_B(22), RX, by, RW, INK, 25)
    by = para(body, SANS(16), RX, by + 2, RW, (58, 52, 44), 20)
    by += 10
    d.line([(RX, by), (1024 - MX, by)], fill=RULE, width=1)
    by += 10
# rail divider: runs alongside the briefs only, stops at the last one
d.line([(RX - 24, LY), (RX - 24, by - 12)], fill=RULE, width=2)

# ---------------------------------------------------------------- markets strip
MY = max(num_end, by) + 12
d.line([(MX, MY), (1024 - MX, MY)], fill=INK, width=2)
d.text((MX, MY + 10), "MARKETS  ·  TUESDAY CLOSE", font=SANS_B(13), fill=MUTED)
mk = [("DOW", "50,759", "–849  –1.6%"),
      ("S&P 500", "7,341", "–76  –1.0%"),
      ("NASDAQ", "24,328", "–181  –0.7%"),
      ("BRENT", "$91.69", "–1.6%")]
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
     "Israel's parliament elects Matan Kahana speaker, 66–52, as Netanyahu's rivals take control."),
    ("CYCLONE XAVIER, CATEGORY 5",
     "The season's fiercest storm bears down on Pukapuka at 220 km/h; Akvan heads for Andhra Pradesh on an orange alert."),
    ("DHONI BOWS OUT OF THE IPL",
     "After 278 matches and five titles, MS Dhoni retires as a player; Chennai makes him mentor from 2027 and retires his No. 7."),
    ("TRUMP, XI AND PUTIN TO MEET",
     "China confirms the first three-way summit: Trump, Xi and Putin meet Thursday in Shenzhen."),
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
d.text((MX, 1000), "Sources: AP · Reuters · Bloomberg · BBC · UN · WHO — "
                  "events reported on 18 November 2026. Claims are attributed, not asserted.",
       font=SANS(14), fill=MUTED)

print("layout: cap_end", cap_end, "num_end", num_end, "rail_end", by,
      "markets", MY, mk_end, "also", AY, also_end)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
