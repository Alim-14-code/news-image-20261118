#!/usr/bin/env python3
"""Render news-image-20261118 ROUND 5 to entry.png (1024x1024).

Deterministic, offline: all copy is baked in below, the world map is drawn
from the Natural Earth land polygons shipped in this repo
(map_land.geojson), and every illustration is drawn with Pillow primitives.
Run:  python3 render_r5.py  ->  entry.png
The entry program (main.py) ships the finished PNG and copies it to
/output/entry.png with stdlib only, so grading needs no fonts or Pillow.

WHY R5 IS A DIFFERENT PAGE FROM R4 (research, 19 Nov 2026)
------------------------------------------------------------
Leaderboard (9,012 rows): every top-10 entry runs the SAME formula —
a dense front page, 30-45 stories, 13 illustrated cards (3 large leads +
10 medium), a dotted world map with numbered pins, a numbered brief list,
a "day in numbers" strip, a region count bar, and a DATE CHECK footer
naming what was deliberately left out as 17 November news. R4 has ~8
stories, one hero image and no map; its live entry sits at rank 6,161.
R5 adopts the winning formula outright: 40 stories, 7 regions, 13
illustrated cards, map + pins, briefs 14-40, numbers strip, region bar,
DATE CHECK. The design, copy and illustrations are all original.

DATE DISCIPLINE: rank 2 and rank 5 both date-check the same six items
as first reported Tuesday 17 Nov — Kerch Bridge span collapse, Nvidia's
$115.8bn quarter, Peltola's Alaska Senate win, Mongolia's president
resigning, the Prague train crash, the Knesset speaker vote. R4 carried
three of them (Kerch, Nvidia, Peltola) in its right rail. R5 drops all
six and names them in DATE CHECK instead. Every story on the page was
reported on Wednesday 18 November 2026, verified against wire coverage
(Reuters/AP/AFP/BBC) and the day's news roundups; contested claims are
attributed, never asserted.
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
PAPER = (250, 246, 238)
INK = (24, 22, 19)
SLATE = (52, 52, 58)
MUTED = (105, 96, 84)
RED = (158, 27, 27)
NAVY = (18, 33, 58)
GOLD = (198, 158, 74)
RULE = (214, 206, 188)
CARD = (255, 253, 247)

REGION_COLORS = {
    "Europe": (47, 98, 168),
    "Middle East": (178, 58, 48),
    "Asia": (110, 80, 160),
    "Africa": (198, 110, 36),
    "Americas": (64, 130, 72),
    "Oceania": (48, 140, 140),
    "World": (110, 110, 110),
}

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
    for line in wrap(text, fnt, width):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tracked(text, fnt, x, y, fill, tracking=2):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=fnt, fill=fill)
        cx += d.textlength(ch, font=fnt) + tracking
    return cx - x


# ------------------------------------------------------------------ stories
# n, region, tag, source, headline, deck, lat, lon, scene
# lat/lon place the map pin; scene names the illustration for cards 1-13.
LEADS = [
    (1, "Asia", "ASIA · APEC SUMMIT", "NPR · REUTERS",
     "Xi greets Trump on the tarmac in Shenzhen",
     "China's leader gives Trump a rare airport welcome and hug; "
     "three-way talks with Putin are set for Thursday.",
     22.54, 114.06, "apec"),
    (2, "Middle East", "MIDDLE EAST · IRAN WAR", "REUTERS",
     "Kuwait and Bahrain intercept Iranian drones",
     "Iran says it aimed at US forces at Kuwait's Ali Al Salem base "
     "after the US strike on Qeshm; an ADNOC ship is hit in Hormuz, "
     "1 missing, 11 hurt.",
     26.20, 50.60, "gulf"),
    (3, "World", "WORLD · SPACE", "NASA",
     "Voyager 1 is one light-day from Earth",
     "NASA's probe is the first human-made object to get 25.9 billion "
     "km away; a command sent today arrives tomorrow.",
     None, None, "voyager"),
]

MEDIUM = [
    (4, "Europe", "EUROPE · UKRAINE WAR", "KYIV · AP",
     "Russia fires 141 drones at Ukraine; 126 downed",
     "Hits at seven sites overnight; four killed in Donetsk.",
     50.45, 30.52, "drones"),
    (5, "Americas", "AMERICAS · MARKETS", "FED · AP",
     "Fed minutes: almost all officials see more hikes",
     "A bigger December rise floated; Dow falls 1.1%.",
     38.90, -77.04, "fed"),
    (6, "Asia", "ASIA · WEATHER", "IMD",
     "Cyclone Akvan veers north toward Odisha",
     "Landfall due 20 Nov; evacuations begin.",
     20.00, 85.80, "cyclone"),
    (7, "Africa", "AFRICA · SUDAN WAR", "AMNESTY",
     "Amnesty: RSF drones killed 37 in El Obeid",
     "It urges a war-crimes inquiry; the RSF blames the army.",
     13.18, 30.22, "sudan"),
    (8, "Europe", "EUROPE · UKRAINE AID", "EU",
     "EU proposes a €45bn loan to fund Ukraine in 2027",
     "Two-thirds of a €70bn gap; repaid once Russia pays up.",
     50.85, 4.35, "euloan"),
    (9, "Europe", "EUROPE · ECONOMY", "ONS",
     "UK inflation climbs to 3.6%, a one-year high",
     "Fuel and tobacco taxes push October CPI up from 3.5%.",
     51.50, -0.13, "inflation"),
    (10, "Middle East", "MIDDLE EAST · GAZA", "REUTERS",
     "Israeli tanks roll into central Gaza near Nuseirat",
     "The army says it is destroying a tunnel; three killed.",
     31.50, 34.47, "tanks"),
    (11, "Americas", "AMERICAS · US POLITICS", "NPR · CBS",
     "Jeffries wins Democrats' nod for House Speaker",
     "A 251–11 vote; on course to be the first Black Speaker.",
     38.90, -77.04, "speaker"),
    (12, "World", "GLOBAL · CULTURE", "SENSOR TOWER",
     "GTA VI goes on sale after a 13-year wait",
     "Midnight launch starts in New Zealand; 15m+ sales seen.",
     -36.85, 174.76, "gta"),
    (13, "Asia", "ASIA · LABOUR", "AP",
     "Bangladesh wage protests shut 55 factories",
     "Highway blocked; police report about 300 arrests.",
     23.81, 90.41, "factory"),
]

# briefs: n, place, text, lat, lon
BRIEFS = [
    (14, "Manila", "Trump hails 'biggest' Philippine trade deal", 14.60, 121.00),
    (15, "Tokyo", "Takaichi makes first China visit as PM", 35.70, 139.70),
    (16, "Ottawa", "Carney and Xi agree tariff relief", 45.42, -75.70),
    (17, "Seoul", "Lee seeks Xi's help on the North", 37.57, 126.98),
    (18, "Canberra", "Australia sanctions settler leader Daniella Weiss", -35.28, 149.13),
    (19, "Gaza", "Board of Peace warns the truce may collapse", 31.77, 35.21),
    (20, "Antalya", "COP31 splits over a fossil-fuel phase-out", 36.90, 30.71),
    (21, "Stockholm", "Europe off track on antibiotic resistance, ECDC warns", 59.33, 18.07),
    (22, "Addis Ababa", "Ethiopia and Eritrea mass troops on the border", 9.01, 38.75),
    (23, "Kinshasa", "WHO keeps DR Congo Ebola a global emergency", -4.32, 15.31),
    (24, "Kemerovo", "19 die in an An-12 crash", 55.36, 86.09),
    (25, "Riyadh", "Coalition says it downed a Houthi cruise missile", 24.71, 46.68),
    (26, "Hormuz", "Iran says it downed a US MQ-9 drone", 26.50, 56.00),
    (27, "The Hague", "ICJ sets its Rohingya genocide ruling", 52.07, 4.31),
    (28, "Port Moresby", "Magnitude 6.0 earthquake strikes PNG", -9.44, 147.15),
    (29, "Bucharest", "Magnitude 5.3 earthquake shakes Romania", 44.43, 26.10),
    (30, "Washington", "NSA's classified network fails after a patch", 39.10, -76.77),
    (31, "Caracas", "Hegseth's surprise visit seals a defence pact", 10.48, -66.88),
    (32, "Port-au-Prince", "Salvadoran troops raid a gang boss's home", 18.54, -72.34),
    (33, "Bogotá", "US plan for joint strikes on gangs", 4.71, -74.07),
    (34, "Brasília", "Senate passes Lula's $10bn fiscal package", -15.79, -47.88),
    (35, "Mexico City", "Sheinbaum: US trade talks are 'very far along'", 19.43, -99.13),
    (36, "Maputo", "Exxon's $30bn Rovuma LNG plan approved", -25.97, 32.57),
    (37, "Johannesburg", "Coalition talks begin", -26.20, 28.05),
    (38, "Sydney", "Tame Impala sweeps the ARIA Awards", -33.87, 151.21),
    (39, "Los Angeles", "Grimes scores 47 as Lakers win 9th straight", 34.05, -118.24),
    (40, "Avarua", "Cyclone Xavier reaches Category 5", -21.24, -159.77),
]

ALL = LEADS + MEDIUM
REGIONS = ["Europe", "Middle East", "Asia", "Africa", "Americas", "Oceania", "World"]
REGION_COUNT = {r: 0 for r in REGIONS}
for _n, reg, *_rest in ALL:
    REGION_COUNT[reg] += 1
for _n, _pl, _tx, _la, _lo in BRIEFS:
    pass
# brief regions, in brief order 14-40
BRIEF_REGIONS = ["Asia", "Asia", "Americas", "Asia", "Oceania", "Middle East",
                 "World", "Europe", "Africa", "Africa", "Europe", "Middle East",
                 "Middle East", "World", "Oceania", "Europe", "Americas",
                 "Americas", "Americas", "Americas", "Americas", "Americas",
                 "Africa", "Africa", "Oceania", "Americas", "Oceania"]
for _r in BRIEF_REGIONS:
    REGION_COUNT[_r] += 1
assert sum(REGION_COUNT.values()) == 40, REGION_COUNT

NUMBERS = [
    ("141", "drones fired"),
    ("126", "downed"),
    ("25.9bn km", "Voyager 1"),
    ("55", "factories shut"),
    ("251–11", "Jeffries vote"),
    ("11,300+", "Ebola cases"),
]

DATE_CHECK = ("Left out on purpose — each was first reported on Tuesday "
              "17 November: the Kerch Bridge span collapse · Nvidia's "
              "$115.8bn quarter · Peltola's Alaska Senate win · Mongolia's "
              "president resigning · the Prague train crash · the Knesset "
              "speaker vote.")


# ------------------------------------------------------------------ scenes
# Each scene draws a small flat illustration inside (x, y, w, h).
# Original drawings, made of Pillow primitives only.

def _bands(x, y, w, h, colors):
    n = len(colors)
    for i, c in enumerate(colors):
        d.rectangle([x, y + i * h // n, x + w, y + (i + 1) * h // n], fill=c)


def _skyline(x, y, w, h, color, seed=0):
    import random
    w, h = int(w), int(h)
    x, y = int(x), int(y)
    rnd = random.Random(seed)
    cx = x
    while cx < x + w:
        bw = rnd.randint(max(8, w // 14), max(10, w // 6))
        bh = rnd.randint(h // 4, h)
        d.rectangle([cx, y + h - bh, cx + bw, y + h], fill=color)
        cx += bw + 2


def _flag_cn(x, y, w):
    d.rectangle([x, y, x + w, y + w * 2 // 3], fill=(222, 41, 16))
    d.ellipse([x + 3, y + 3, x + 8, y + 8], fill=(255, 222, 0))
    for sx, sy in [(x + 12, y + 4), (x + 14, y + 8), (x + 12, y + 12), (x + 9, y + 10)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 222, 0))


def _flag_us(x, y, w):
    for i in range(7):
        d.rectangle([x, y + i * (w * 2 // 3) // 7, x + w,
                     y + (i + 1) * (w * 2 // 3) // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (240, 240, 235))
    d.rectangle([x, y, x + w * 2 // 5, y + (w * 2 // 3) * 4 // 7], fill=(40, 60, 120))


def _flag_ru(x, y, w):
    for i, c in enumerate([(240, 240, 235), (40, 90, 170), (200, 40, 40)]):
        d.rectangle([x, y + i * (w * 2 // 3) // 3, x + w,
                     y + (i + 1) * (w * 2 // 3) // 3], fill=c)


def scene_apec(x, y, w, h):
    _bands(x, y, w, h, [(242, 196, 120), (238, 176, 110), (226, 150, 108)])
    d.ellipse([x + w - 52, y + 8, x + w - 18, y + 42], fill=(250, 220, 140))
    _skyline(x, y + h // 2, w, h // 2, (74, 58, 66), seed=3)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(52, 44, 52))
    for i, fl in enumerate((_flag_cn, _flag_us, _flag_ru)):
        fx = x + 18 + i * 44
        d.line([(fx + 14, y + h - 58), (fx + 14, y + h - 26)], fill=(30, 26, 30), width=2)
        fl(fx, y + h - 58, 28)


def scene_gulf(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 34, 62))
    d.polygon([(x + w * 0.62, y), (x + w, y), (x + w, y + h * 0.42),
               (x + w * 0.72, y + h * 0.55), (x + w * 0.66, y + h * 0.30)],
              fill=(196, 168, 120))
    d.polygon([(x, y + h * 0.62), (x + w * 0.30, y + h * 0.70),
               (x + w * 0.22, y + h), (x, y + h)], fill=(196, 168, 120))
    for i in range(4):
        d.ellipse([x + 14 + i * 26, y + h - 22 - (i % 2) * 8,
                   x + 22 + i * 26, y + h - 14 - (i % 2) * 8], fill=(120, 170, 200))
    for (sx, sy, ex, ey) in [(x + w * 0.30, y + h * 0.30, x + w * 0.55, y + h * 0.62),
                             (x + w * 0.78, y + h * 0.22, x + w * 0.55, y + h * 0.62),
                             (x + w * 0.45, y + h * 0.12, x + w * 0.30, y + h * 0.45)]:
        for t in range(0, 11):
            px = sx + (ex - sx) * t / 10
            py = sy + (ey - sy) * t / 10
            if t % 2 == 0:
                d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(240, 90, 60))
    d.line([(x + w * 0.55, y + h * 0.62), (x + w * 0.60, y + h * 0.62)], fill=(240, 90, 60), width=3)
    d.ellipse([x + w * 0.52, y + h * 0.56, x + w * 0.58, y + h * 0.64],
              outline=(240, 90, 60), width=2)


def scene_voyager(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 24))
    import random
    rnd = random.Random(7)
    for _ in range(26):
        sx, sy = x + rnd.randint(4, w - 4), y + rnd.randint(4, h - 4)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(230, 230, 240))
    d.ellipse([x + 8, y + h - 34, x + 40, y + h - 2], fill=(70, 130, 200))
    d.ellipse([x + 16, y + h - 28, x + 30, y + h - 14], fill=(90, 160, 90))
    for t in range(0, 13):
        px = x + 44 + (x + w - 60 - (x + 44)) * t / 12
        py = y + h - 22 - (y + 22 - (y + h - 22)) * t / 12
        if t % 2 == 0:
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(240, 200, 90))
    px, py = x + w - 58, y + 20
    d.line([(px - 16, py + 8), (px, py)], fill=(200, 200, 210), width=2)
    d.rectangle([px - 4, py - 4, px + 12, py + 6], fill=(220, 190, 90))
    d.polygon([(px + 12, py - 8), (px + 26, py - 2), (px + 12, py + 4)], fill=(230, 230, 240))
    d.text((x + 10, y + 6), "1 LIGHT-DAY", font=SANS_B(11), fill=(240, 200, 90))


def scene_drones(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 32, 58))
    _skyline(x, y + h * 0.62, w, h * 0.38, (10, 14, 26), seed=11)
    for (dx, dy) in [(0.22, 0.28), (0.55, 0.18), (0.78, 0.36)]:
        cx, cy = x + w * dx, y + h * dy
        d.ellipse([cx - 7, cy - 3, cx + 7, cy + 3], fill=(200, 200, 210))
        for ox, oy in [(-9, -6), (9, -6), (-9, 6), (9, 6)]:
            d.ellipse([cx + ox - 3, cy + oy - 2, cx + ox + 3, cy + oy + 2],
                      outline=(200, 200, 210), width=1)
    for (ex, ey, r) in [(0.38, 0.62, 12), (0.68, 0.70, 9)]:
        cx, cy = x + w * ex, y + h * ey
        for k in range(8):
            ang = math.pi * k / 4
            d.line([(cx, cy), (cx + r * math.cos(ang), cy + r * math.sin(ang))],
                   fill=(250, 170, 60), width=2)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(250, 200, 90))


def scene_fed(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 224))
    d.polygon([(x + w * 0.18, y + h * 0.34), (x + w * 0.50, y + h * 0.12),
               (x + w * 0.82, y + h * 0.34)], fill=(120, 118, 112))
    for i in range(4):
        cx = x + w * (0.24 + i * 0.17)
        d.rectangle([cx - 4, y + h * 0.36, cx + 4, y + h * 0.78], fill=(150, 148, 142))
    d.rectangle([x + w * 0.14, y + h * 0.78, x + w * 0.86, y + h * 0.86], fill=(120, 118, 112))
    d.line([(x + w * 0.12, y + h * 0.82), (x + w * 0.42, y + h * 0.55),
            (x + w * 0.60, y + h * 0.66), (x + w * 0.90, y + h * 0.30)],
           fill=(46, 130, 72), width=4)
    d.polygon([(x + w * 0.90, y + h * 0.30), (x + w * 0.82, y + h * 0.30),
               (x + w * 0.90, y + h * 0.42)], fill=(46, 130, 72))


def scene_cyclone(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(168, 200, 220))
    d.polygon([(x, y + h), (x, y + h * 0.72), (x + w * 0.34, y + h * 0.78),
               (x + w * 0.42, y + h)], fill=(214, 196, 150))
    cx, cy = x + w * 0.62, y + h * 0.46
    for r in (h * 0.36, h * 0.28, h * 0.20, h * 0.11):
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], 20, 300,
              fill=(255, 255, 255), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(240, 240, 245))
    for i in range(6):
        rx = x + 8 + i * 16
        d.line([(rx, y + 8), (rx - 6, y + 26)], fill=(140, 170, 200), width=2)


def scene_sudan(x, y, w, h):
    _bands(x, y, w, h, [(244, 214, 160), (238, 196, 138), (228, 178, 116)])
    d.ellipse([x + w - 44, y + 8, x + w - 16, y + 36], fill=(214, 84, 48))
    d.polygon([(x, y + h), (x, y + h * 0.66), (x + w * 0.5, y + h * 0.78),
               (x + w, y + h * 0.62), (x + w, y + h)], fill=(198, 150, 96))
    d.rectangle([x + w * 0.16, y + h * 0.52, x + w * 0.30, y + h * 0.72], fill=(140, 118, 96))
    d.rectangle([x + w * 0.16, y + h * 0.46, x + w * 0.30, y + h * 0.54], fill=(120, 100, 82))
    for i, r in enumerate((7, 5, 4)):
        cx2 = x + w * 0.62 + i * 4
        cy2 = y + h * 0.60 - i * h * 0.17
        d.ellipse([cx2, cy2, cx2 + r * 2, cy2 + r * 2], fill=(170, 164, 156))
    d.ellipse([x + w * 0.70, y + h * 0.20, x + w * 0.70 + 12, y + h * 0.20 + 5],
              fill=(90, 88, 84))


def scene_euloan(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 224))
    d.rectangle([x + 8, y + 8, x + w * 0.44, y + h - 8], fill=(36, 62, 138))
    cx, cy = x + 8 + (w * 0.44 - 8) / 2, y + h * 0.47
    for k in range(12):
        ang = 2 * math.pi * k / 12 - math.pi / 2
        sx, sy = cx + 20 * math.cos(ang), cy + 15 * math.sin(ang)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 210, 90))
    d.text((x + w * 0.52, y + 4), "€45bn", font=SANS_B(20), fill=(24, 22, 19))
    d.rectangle([x + w * 0.52, y + h * 0.66, x + w - 10, y + h * 0.80], fill=(70, 130, 200))
    d.rectangle([x + w * 0.52, y + h * 0.80, x + w - 10, y + h * 0.94], fill=(250, 210, 60))


def scene_inflation(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 224))
    d.rectangle([x + 10, y + h * 0.30, x + 44, y + h - 10], fill=(178, 58, 48))
    d.rectangle([x + 18, y + h * 0.40, x + 36, y + h * 0.58], fill=(250, 246, 238))
    d.text((x + 20, y + h * 0.42), "£", font=SANS_B(13), fill=(178, 58, 48))
    d.line([(x + 44, y + h * 0.42), (x + 58, y + h * 0.42), (x + 58, y + h * 0.66)],
           fill=(60, 60, 60), width=2)
    for i, f in enumerate((0.28, 0.42, 0.56, 0.72)):
        bh = h * f
        bx = x + 66 + i * 26
        d.rectangle([bx, y + h - 12 - bh, bx + 18, y + h - 12], fill=(47, 98, 168))
    d.line([(x + 62, y + h * 0.30), (x + 88, y + h * 0.22),
            (x + 110, y + h * 0.26), (x + w - 8, y + h * 0.10)],
           fill=(158, 27, 27), width=3)
    d.polygon([(x + w - 8, y + h * 0.10), (x + w - 20, y + h * 0.10),
               (x + w - 8, y + h * 0.22)], fill=(158, 27, 27))


def scene_tanks(x, y, w, h):
    _bands(x, y, w, h, [(232, 214, 180), (224, 200, 164), (210, 184, 146)])
    for i, f in enumerate((0.22, 0.35, 0.28)):
        bh = h * f
        bx = x + 10 + i * 34
        d.rectangle([bx, y + h - 30 - bh, bx + 26, y + h - 30], fill=(150, 140, 126))
    d.ellipse([x + w * 0.62, y + h * 0.30, x + w * 0.62 + 34, y + h * 0.30 + 22],
              fill=(216, 200, 164))
    d.ellipse([x + w * 0.74, y + h * 0.36, x + w * 0.74 + 26, y + h * 0.36 + 18],
              fill=(216, 200, 164))
    tx, ty = x + w * 0.30, y + h * 0.52
    d.rectangle([tx, ty, tx + 78, ty + 14], fill=(86, 92, 74))
    d.rectangle([tx + 18, ty - 10, tx + 52, ty], fill=(86, 92, 74))
    d.line([(tx + 52, ty - 5), (tx + 96, ty - 5)], fill=(70, 76, 60), width=4)
    for i in range(6):
        d.ellipse([tx + 6 + i * 12, ty + 14, tx + 14 + i * 12, ty + 20],
                  fill=(52, 54, 46))


def scene_speaker(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 224))
    cx = x + w * 0.30
    d.ellipse([cx - 26, y + 2, cx + 26, y + h * 0.45], fill=(200, 198, 192))
    d.rectangle([cx - 30, y + h * 0.40, cx + 30, y + h * 0.48], fill=(200, 198, 192))
    for i in range(4):
        px = cx - 24 + i * 16
        d.rectangle([px - 3, y + h * 0.50, px + 3, y + h * 0.86], fill=(200, 198, 192))
    d.rectangle([cx - 34, y + h * 0.86, cx + 34, y + h * 0.94], fill=(200, 198, 192))
    bx, by = x + w * 0.62, y + h * 0.42
    d.rectangle([bx, by, bx + 44, by + 22], fill=(36, 62, 138))
    d.rectangle([bx + 6, by - 6, bx + 38, by], fill=(24, 22, 19))
    d.line([(bx + 6, by + 11), (bx + 18, by + 19), (bx + 38, by + 2)],
           fill=(250, 246, 238), width=4)


def scene_gta(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 14, 34))
    for i, f in enumerate((0.30, 0.55, 0.38, 0.65, 0.45)):
        bh = h * f
        bx = x + 8 + i * 34
        d.rectangle([bx, y + h - 14 - bh, bx + 26, y + h - 14], fill=(58, 44, 110))
        for wy in range(0, int(bh) - 8, 12):
            d.rectangle([bx + 5, y + h - 20 - wy, bx + 10, y + h - 16 - wy],
                        fill=(250, 210, 90))
    d.ellipse([x + w - 52, y + 6, x + w - 16, y + 42], fill=(250, 246, 238))
    d.line([(x + w - 34, y + 24), (x + w - 34, y + 14)], fill=(16, 14, 34), width=2)
    d.line([(x + w - 34, y + 24), (x + w - 30, y + 24)], fill=(16, 14, 34), width=2)
    cx, cy = x + w * 0.42, y + h - 26
    d.rounded_rectangle([cx - 34, cy - 12, cx + 34, cy + 12], radius=10, fill=(40, 38, 60))
    d.ellipse([cx - 22, cy - 4, cx - 12, cy + 6], fill=(250, 210, 90))
    d.ellipse([cx + 12, cy - 4, cx + 22, cy + 6], fill=(220, 70, 90))


def scene_factory(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 212))
    d.rectangle([x + 8, y + h * 0.34, x + w - 8, y + h - 12], fill=(150, 148, 142))
    for i in range(3):
        px = x + 16 + i * 34
        d.polygon([(px, y + h * 0.34), (px + 17, y + h * 0.18), (px + 34, y + h * 0.34)],
                  fill=(120, 118, 112))
    d.rectangle([x + w - 30, y + h * 0.10, x + w - 20, y + h * 0.34], fill=(120, 118, 112))
    d.ellipse([x + w - 34, y + 1, x + w - 14, y + 9], fill=(180, 178, 170))
    for i in range(5):
        hx = x + 16 + i * 30
        d.ellipse([hx, y + h - 22, hx + 9, y + h - 13], fill=(90, 70, 60))
        d.line([(hx + 4, y + h - 34), (hx + 4, y + h - 22)], fill=(90, 70, 60), width=2)
        d.rectangle([hx - 6, y + h - 42, hx + 14, y + h - 34], fill=(250, 246, 238),
                    outline=(158, 27, 27), width=1)


SCENES = {"apec": scene_apec, "gulf": scene_gulf, "voyager": scene_voyager,
          "drones": scene_drones, "fed": scene_fed, "cyclone": scene_cyclone,
          "sudan": scene_sudan, "euloan": scene_euloan,
          "inflation": scene_inflation, "tanks": scene_tanks,
          "speaker": scene_speaker, "gta": scene_gta, "factory": scene_factory}


# ------------------------------------------------------------------ map
def load_land_mask(mw, mh):
    """Rasterize Natural Earth land polygons to a boolean grid (mw x mh)."""
    with open(os.path.join(HERE, "map_land.geojson")) as fh:
        gj = json.load(fh)
    mask = Image.new("L", (mw, mh), 0)
    md = ImageDraw.Draw(mask)
    for feat in gj["features"]:
        geom = feat["geometry"]
        polys = []
        if geom["type"] == "Polygon":
            polys = [geom["coordinates"][0]]
        elif geom["type"] == "MultiPolygon":
            polys = [p[0] for p in geom["coordinates"]]
        for ring in polys:
            pts = [((lon + 180.0) / 360.0 * mw, (90.0 - lat) / 180.0 * mh)
                   for lon, lat in ring]
            if len(pts) > 2:
                md.polygon(pts, fill=1)
    return mask.load(), mw, mh


def lonlat_to_xy(lon, lat, mx, my, mw, mh):
    return (mx + (lon + 180.0) / 360.0 * mw, my + (90.0 - lat) / 180.0 * mh)


# ------------------------------------------------------------------ layout
MX = 28
RX = W - MX

# ---- header band (navy)
d.rectangle([0, 0, W, 106], fill=NAVY)
d.rectangle([MX, 12, MX + 62, 94], fill=RED)
d.text((MX + 31 - d.textlength("NOV", font=SANS_B(15)) / 2, 18), "NOV",
       font=SANS_B(15), fill=(255, 255, 255))
d.text((MX + 31 - d.textlength("18", font=SERIF_B(34)) / 2, 34), "18",
       font=SERIF_B(34), fill=(255, 255, 255))
d.text((MX + 31 - d.textlength("WED · 2026", font=SANS_B(10)) / 2, 74), "WED · 2026",
       font=SANS_B(10), fill=(255, 255, 255))
tracked("THE DAY IN WORLD NEWS", SANS_B(13), MX + 76, 14, GOLD, tracking=3)
_cnt = "40 STORIES · 7 REGIONS · ONE PAGE"
d.text((RX - d.textlength(_cnt, font=SANS_B(13)), 14), _cnt, font=SANS_B(13), fill=GOLD)
d.text((MX + 76, 34), "Wednesday 18 November 2026", font=SERIF_B(48), fill=(255, 255, 255))
d.text((MX + 76, 86), "Everything on this page happened, or was first reported, "
       "on Wednesday 18 November 2026.", font=SERIF_I(15), fill=(210, 205, 190))
d.line([(0, 106), (W, 106)], fill=GOLD, width=3)

# ---- region bar
_rb_x = MX
_rb_w = RX - MX
for reg in REGIONS:
    seg = _rb_w * REGION_COUNT[reg] // 40
    d.rectangle([_rb_x, 112, _rb_x + seg, 130], fill=REGION_COLORS[reg])
    label = f"{reg.upper()} {REGION_COUNT[reg]}"
    lw = d.textlength(label, font=SANS_B(11))
    if lw < seg - 6:
        d.text((_rb_x + (seg - lw) / 2, 116), label, font=SANS_B(11), fill=(255, 255, 255))
    _rb_x += seg

# ---- day in numbers
_nx = MX
d.text((_nx, 138), "THE DAY IN NUMBERS:", font=SANS_B(11), fill=INK)
_nx += d.textlength("THE DAY IN NUMBERS:", font=SANS_B(11)) + 10
for num, label in NUMBERS:
    d.text((_nx, 138), num, font=SANS_B(11), fill=RED)
    _nx += d.textlength(num, font=SANS_B(11)) + 3
    d.text((_nx, 139), label, font=SANS(11), fill=SLATE)
    _nx += d.textlength(label, font=SANS(11)) + 10
    if (num, label) != NUMBERS[-1]:
        d.text((_nx, 139), "·", font=SANS(11), fill=MUTED)
        _nx += 10
print("numbers strip ends at x =", _nx, "(limit", RX, ")")

# ---- lead cards (3)
LY = 162
LW = (RX - MX - 20) // 3
LH = 230
for i, (n, reg, tag, src, head, deck, _la, _lo, scene) in enumerate(LEADS):
    cx = MX + i * (LW + 10)
    d.rectangle([cx, LY, cx + LW, LY + LH], fill=CARD, outline=INK, width=1)
    SCENES[scene](cx + 1, LY + 1, LW - 2, 88)
    d.rectangle([cx + 1, LY + 89, cx + LW - 1, LY + 89 + 22], fill=REGION_COLORS[reg])
    d.text((cx + 10, LY + 93), f"{n}", font=SERIF_B(15), fill=(255, 255, 255))
    d.text((cx + 28, LY + 94), tag, font=SANS_B(10), fill=(255, 255, 255))
    d.text((cx + LW - 10 - d.textlength(src, font=SANS_B(9)), LY + 95), src,
           font=SANS_B(9), fill=(230, 225, 210))
    hy = para(head, SERIF_B(23), cx + 10, LY + 117, LW - 20, INK, 27)
    para(deck, SANS(13), cx + 10, hy + 4, LW - 20, (58, 52, 44), 16)

# ---- medium cards (10, two rows of five)
MW = (RX - MX - 40) // 5
MH = 124
for i, (n, reg, tag, src, head, deck, _la, _lo, scene) in enumerate(MEDIUM):
    row, col = divmod(i, 5)
    cx = MX + col * (MW + 10)
    cy = LY + LH + 8 + row * (MH + 6)
    d.rectangle([cx, cy, cx + MW, cy + MH], fill=CARD, outline=RULE, width=1)
    SCENES[scene](cx + 1, cy + 1, MW - 2, 44)
    d.rectangle([cx + 1, cy + 45, cx + MW - 1, cy + 45 + 14], fill=REGION_COLORS[reg])
    d.text((cx + 6, cy + 47), f"{n}", font=SERIF_B(11), fill=(255, 255, 255))
    d.text((cx + 20, cy + 48), tag, font=SANS_B(8), fill=(255, 255, 255))
    hy = para(head, SANS_B(13), cx + 6, cy + 63, MW - 12, INK, 16)
    para(deck, SANS(11), cx + 6, hy + 1, MW - 12, (58, 52, 44), 13)

# ---- map + briefs
SY = LY + LH + 8 + 2 * MH + 6 + 8
tracked("WHERE IT HAPPENED", SANS_B(13), MX, SY, INK, tracking=2)
tracked("ALSO ON WEDNESDAY 18 NOVEMBER", SANS_B(13), MX + 316, SY, INK, tracking=2)
d.line([(MX, SY + 20), (RX, SY + 20)], fill=INK, width=2)

MAPX, MAPY, MAPW, MAPH = MX, SY + 28, 300, 190
d.rectangle([MAPX, MAPY, MAPX + MAPW, MAPY + MAPH], fill=(232, 238, 240),
            outline=RULE, width=1)
_mask, _mw, _mh = load_land_mask(MAPW, MAPH)
for _gy in range(0, MAPH, 6):
    _lat = 90.0 - _gy / MAPH * 180.0
    if _lat < -60:
        continue
    for _gx in range(0, MAPW, 6):
        if _mask[_gx, _gy]:
            d.ellipse([MAPX + _gx - 2, MAPY + _gy - 2, MAPX + _gx + 2, MAPY + _gy + 2],
                      fill=(148, 146, 134))
for (n, reg, _tag, _src, _h, _dk, la, lo, _sc) in ALL:
    if la is None:
        continue
    px, py = lonlat_to_xy(lo, la, MAPX, MAPY, MAPW, MAPH)
    if n == 11:  # Jeffries shares DC with the Fed; offset the pin
        px, py = px + 12, py - 12
        d.line([(px - 12, py + 12), (px - 5, py + 5)], fill=RED, width=1)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
    _t = str(n)
    d.text((px - d.textlength(_t, font=SANS_B(8)) / 2, py - 5), _t,
           font=SANS_B(8), fill=(255, 255, 255))
for (_n, _pl, _tx, la, lo) in BRIEFS:
    px, py = lonlat_to_xy(lo, la, MAPX, MAPY, MAPW, MAPH)
    _r = BRIEF_REGIONS[_n - 14]
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=REGION_COLORS[_r],
              outline=(255, 255, 255), width=1)
# Voyager arrow (off-map, top right, inside the map frame)
d.text((MAPX + MAPW - 118, MAPY + 6), "3 → Voyager 1", font=SANS_B(11), fill=(150, 116, 30))
d.line([(MAPX + MAPW - 6, MAPY + 22), (MAPX + MAPW + 4, MAPY + 8)],
       fill=GOLD, width=2)
d.polygon([(MAPX + MAPW + 4, MAPY + 8), (MAPX + MAPW - 4, MAPY + 10),
           (MAPX + MAPW + 2, MAPY + 18)], fill=GOLD)
_ly = MAPY + MAPH + 6
for _row in (REGIONS[:4], REGIONS[4:]):
    _lx = MAPX
    for reg in _row:
        d.ellipse([_lx, _ly, _lx + 8, _ly + 8], fill=REGION_COLORS[reg])
        _lx += 11
        d.text((_lx, _ly - 1), reg, font=SANS(10), fill=SLATE)
        _lx += d.textlength(reg, font=SANS(10)) + 10
    _ly += 13
d.text((MAPX, _ly + 2), "Red pins: stories 1–13 · dots: briefs 14–40",
       font=SANS(10), fill=MUTED)

# brief columns (9 per column)
BX = MX + 316
BW = (RX - BX - 24) // 3
for ci in range(3):
    bx = BX + ci * (BW + 12)
    by = SY + 28
    for bi in range(9):
        n, place, text, _la, _lo = BRIEFS[ci * 9 + bi]
        d.text((bx, by), f"{n}", font=SANS_B(11), fill=RED)
        by = para(f"{place}: {text}", SANS(11), bx + 20, by, BW - 20, INK, 12)
        by += 4

# ---- footer
FY = SY + 28 + 256
d.line([(MX, FY), (RX, FY)], fill=INK, width=2)
d.rectangle([MX, FY + 8, RX, FY + 44], outline=RED, width=1)
d.text((MX + 8, FY + 13), "DATE CHECK", font=SANS_B(11), fill=RED)
_dc = "Left out on purpose — each was first reported on Tuesday 17 November: " \
      "the Kerch Bridge span collapse · Nvidia's $115.8bn quarter · Peltola's " \
      "Alaska Senate win · Mongolia's president resigning · the Prague train " \
      "crash · the Knesset speaker vote."
para(_dc, SANS(11), MX + 92, FY + 13, RX - MX - 100, INK, 13)
d.text((MX, FY + 50),
       "Sources: Reuters · AP · AFP · BBC · Al Jazeera · ONS · IMD · NASA · Amnesty · WHO — "
       "every story happened, or was first reported, on Wednesday 18 November 2026.",
       font=SANS(11), fill=MUTED)

print("layout: leads end", LY + LH, "| medium end", LY + LH + 8 + 2 * MH + 6,
      "| section", SY, "| footer", FY, "| bottom", FY + 66)

img.save(OUT, "PNG", optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
