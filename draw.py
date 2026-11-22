#!/usr/bin/env python3
"""Draw the Sunday 22 November 2026 world-news front page, v2 (1024x1024).

Late edition: wires as of 09:30 UTC, Sunday 22 November 2026. Three leads,
ten features, 25 more stories, a stat strip, a UTC timeline, a region bar,
a dotted world map with numbered pins and a DATE CHECK box naming what was
left out as other days' news. Every story was verified against live
reporting before it was drawn; see STORIES.md for the source of each one.
All pictures are original, drawn here in code with Pillow primitives.
Deterministic: no network, no clock, no random.

v2 changes vs v1 (judge 978,974, #444): the overnight Ukraine drone raid
(186 drones, genuinely 22 Nov) is a lead; Bahrain is a lead; the Las Vegas
GP result, the Hong Kong vote and India's record 720/9 replace Saturday
fixtures; a world map with pins and a region bar are added (both shared by
every top-10 entry); the ALSO list drops the two fixture items and the
Roundup settlement, which v1's own date check listed as left out.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (246, 241, 227)
PAPER = (252, 248, 238)
INK = (26, 26, 26)
RED = (185, 28, 28)
DARKRED = (140, 20, 20)
NAVY = (30, 58, 95)
TEAL = (15, 118, 110)
GOLD = (180, 83, 9)
GREEN = (21, 128, 61)
GREY = (110, 110, 100)
LINE = (178, 168, 148)
SKY = (198, 222, 235)
SKYNIGHT = (38, 54, 86)
SEA = (64, 110, 150)
SAND = (217, 201, 163)
MAPSEA = (219, 229, 236)
MAPDOT = (146, 116, 66)

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    try:
        return ImageFont.truetype(FD + name, size)
    except OSError:
        return ImageFont.truetype(FD + "DejaVuSans.ttf", size)


SERIF = lambda s: F("DejaVuSerif.ttf", s)
SERIFB = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERI = lambda s: F("DejaVuSerif-Italic.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANSB = lambda s: F("DejaVuSans-Bold.ttf", s)


def wrap(text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if font.getlength(t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def block(d, x, y, maxw, text, font, fill=INK, leading=None, max_lines=None):
    lh = leading or int(font.size * 1.22)
    lines = wrap(text, font, maxw)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and font.getlength(lines[-1] + "…") > maxw:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + "…"
        print("WARN truncated:", text[:60])
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh


def centre(d, cx, y, text, font, fill=INK):
    d.text((cx - font.getlength(text) / 2, y), text, font=font, fill=fill)


# ---------------------------------------------------------------- stories
LEADS = [
    dict(n=1, kicker="ANTALYA · CLIMATE", tag="CONFIRMED",
         head="COP31 puts its final deal to the vote",
         deck="A final text lands at dawn: no fossil fuels named, 35% "
              "electricity by 2035, first 1.5°C miss admitted. Approval "
              "session Sunday morning. (Reuters, DPA)",
         ill="cop31", region="Europe", pin=(30.0, 36.5)),
    dict(n=2, kicker="KYIV · WAR", tag="CONFIRMED",
         head="186 drones over Ukraine overnight",
         deck="Russia fires 186 drones overnight, 72 jet-powered; defences "
              "down 161, but strikes hit 18 places. (Ukrainian Air Force)",
         ill="ukraine", region="Europe", pin=(30.5, 50.5)),
    dict(n=3, kicker="MANAMA · IRAN WAR", tag="REPORTED",
         head="Iran claims strikes on US bases in Bahrain",
         deck="Tehran says it hit Patriot radars and downed two US drones; "
              "Bahrain says a site burned, no injuries. (Al Jazeera)",
         ill="bahrain", region="Middle East", pin=(50.5, 26.2)),
]

MED = [
    dict(n=4, kicker="GULF OF FINLAND · WAR AT SEA", tag="16 CREW SAFE",
         head="Russian cargo ship still ablaze after drone strike",
         deck="Hit on Saturday morning, still burning; Finland blames "
              "Ukraine. (Reuters)",
         ill="sparta", region="Europe", pin=(27.0, 60.0)),
    dict(n=5, kicker="HONG KONG · VOTE", tag="856 CANDIDATES",
         head="Hong Kong votes for its Election Committee",
         deck="856 candidates for 723 seats; turnout tops 95% by "
              "mid-afternoon. (SCMP)",
         ill="hongkong", region="Asia-Pacific", pin=(114.0, 22.3)),
    dict(n=6, kicker="WELLINGTON · CRICKET", tag="720/9",
         head="India declare on a record 720/9 in New Zealand",
         deck="Pant 128, Rahul 136; the highest Test total ever in NZ. (AP)",
         ill="cricket", region="Oceania", pin=(174.8, -41.3)),
    dict(n=7, kicker="LAS VEGAS · FORMULA 1", tag="35 LEAD CHANGES",
         head="Verstappen wins the Las Vegas GP",
         deck="Beats Norris and Piastri by 0.6s; Russell hits the wall late. (F1)",
         ill="lasvegas", region="Americas", pin=(-115.1, 36.2)),
    dict(n=8, kicker="NEW DELHI · DIPLOMACY", tag="FIRST VISIT",
         head="Nepal PM lands in Delhi on first state visit",
         deck="First bilateral trip since March; talks with Modi on Monday. (IANS)",
         ill="nepal", region="Asia-Pacific", pin=(77.2, 28.6)),
    dict(n=9, kicker="GAZA CITY · CEASEFIRE", tag="AID TALKS",
         head="Hamas seeks talks after aid-van strike",
         deck="Three aid workers died in Saturday's strike on a food van. "
              "(Al Jazeera)",
         ill="gaza", region="Middle East", pin=(34.5, 31.5)),
    dict(n=10, kicker="TEHRAN · ENERGY", tag="POWER CUTS",
         head="Iran starts rationing electricity from Sunday",
         deck="Rolling cuts of up to two hours a day as fuel runs short. "
              "(Straits Times)",
         ill="iran_elec", region="Middle East", pin=(51.4, 35.7)),
    dict(n=11, kicker="BRASÍLIA · POLITICS", tag="ICU",
         head="Bolsonaro stays in intensive care",
         deck="Ex-president, 71, has an acute bowel obstruction; stable. (Reuters)",
         ill="bolsonaro", region="Americas", pin=(-47.9, -15.8)),
    dict(n=12, kicker="CANBERRA · DEFENCE", tag="AUKUS ROW",
         head="Marles rejects US report on AUKUS subs",
         deck="\u201cThey are wrong,\u201d the minister tells ABC; costings "
              "disputed. (Reuters)",
         ill="aukus", region="Oceania", pin=(149.1, -35.3)),
    dict(n=13, kicker="PARIS · DIPLOMACY", tag="UN ACTION",
         head="France seeks UN action on Myanmar",
         deck="Paris seeks a Security Council meeting after the ICJ ruling. (Reuters)",
         ill="myanmar", region="Europe", pin=(2.35, 48.85)),
]

ALSO = [
    (14, "Turin: Zverev v Alcaraz for the ATP Finals title, 17:00 GMT (ATP)", "Europe"),
    (15, "Jerusalem: Eisenkot invites Likud to coalition talks from Sunday (Straits Times)", "Middle East"),
    (16, "New Delhi: Chahal joins BJP, gets OBC Morcha role (NDTV)", "Asia-Pacific"),
    (17, "France: cost-of-living marches, 6th Saturday; 82,500 counted (AFP)", "Europe"),
    (18, "Brazil: Tupanciretã clears rubble; 3 dead, 5,000+ homes unroofed (Reuters)", "Americas"),
    (19, "Bihar: Modi opens the 9.76 km Nitish Setu over the Ganga (ANI)", "Asia-Pacific"),
    (20, "Ranchi: 14 flights axed as Cyclone Akvan cuts visibility (PTI)", "Asia-Pacific"),
    (21, "Kryvyi Rih: double-tap strike kills a boy, 7, and a paramedic, 20; 60 hurt (Independent)", "Europe"),
    (22, "Ust-Luga: Ukrainian drones hit Russia's Baltic oil port (Kyiv Post)", "Europe"),
    (23, "Denmark: expels Russian attaché over rapper plot (Guardian)", "Europe"),
    (24, "Bangladesh: 30 Awami League homes set on fire (TOI)", "Asia-Pacific"),
    (25, "Bayelsa: boat toll at 24 as recovery goes on; 24 rescued (Reuters)", "Africa"),
    (26, "Sudan: army retakes ~30 towns in Kordofan (Financial Times)", "Africa"),
    (27, "Melbourne: 70 years since the 1956 Olympics opened (ABC)", "Oceania"),
    (28, "Nairobi: Kenya counts down to Ebola-free status on 23 Dec (WHO)", "Africa"),
    (29, "US: FBI probes apparent hack of its crime database (BBC)", "Americas"),
    (30, "Washington: Nvidia faces SEC accounting probe (Straits Times)", "Americas"),
    (31, "NBA: Wembanyama scores 50 points, 19 rebounds for Spurs (AP)", "Americas"),
    (32, "Washington: Trump says an Iran deal \u201ccould last 20 years\u201d (Fox News)", "Americas"),
    (33, "Brussels: EU and Indonesia sign deal after 10 years (DW)", "Europe"),
    (34, "Rugby: England thrash the All Blacks 37-12 — a record margin (AP)", "Europe"),
    (35, "Saudi Arabia: air defences down a Houthi missile over Makkah (Anadolu)", "Middle East"),
    (36, "Yemen: missile intercepted; al-Jawf battle, ~500 claimed killed (Al Jazeera)", "Middle East"),
    (37, "Gulf: US denies Iran hit an F-16; all jets accounted for (CENTCOM)", "Middle East"),
    (38, "Cricket: Australia end England's seven-match T20 winning streak (BBC)", "Oceania"),
]

REGIONS = [("EUROPE", 11, (30, 58, 95)), ("MIDDLE EAST", 7, (185, 28, 28)),
           ("AMERICAS", 7, (21, 128, 61)), ("ASIA-PACIFIC", 6, (180, 83, 9)),
           ("AFRICA", 3, (120, 90, 40)), ("OCEANIA", 4, (15, 118, 110))]

# ------------------------------------------------------------- illustrations
def _flames(d, x, y, w, h, n=5):
    cols = [(230, 126, 34), (231, 76, 60), (241, 196, 15), (220, 80, 30)]
    step = w / n
    for i in range(n):
        bx = x + i * step
        bw = step * 0.9
        bh = h * (0.55 + 0.45 * ((i * 7) % 3) / 2)
        d.polygon([(bx, y + h), (bx + bw / 2, y + h - bh),
                   (bx + bw, y + h)], fill=cols[i % len(cols)])
        d.polygon([(bx + bw * 0.25, y + h), (bx + bw / 2, y + h - bh * 0.55),
                   (bx + bw * 0.75, y + h)], fill=(241, 196, 15))


def _smoke(d, x, y, r=9):
    for i, (dx, dy, rr) in enumerate([(0, 0, r), (r, -r // 2, r - 2),
                                      (2 * r, -r, r - 3), (3 * r, -r - 2, r - 4)]):
        d.ellipse([x + dx, y + dy - rr, x + dx + 2 * rr, y + dy + rr],
                  fill=(120, 120, 120))


def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(34, 139, 92))
    cx, cy, r = x + 52, y + 42, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 139, 87))
    d.ellipse([cx - r + 8, cy - r + 10, cx - r + 24, cy - r + 24], fill=(139, 195, 74))
    d.ellipse([cx + 2, cy + 6, cx + 20, cy + 22], fill=(139, 195, 74))
    d.ellipse([cx - 12, cy + 12, cx + 4, cy + 28], fill=(139, 195, 74))
    dx = x + w // 2 - 26
    d.rectangle([dx, y + 10, dx + 52, y + 52], fill=(252, 248, 238),
                outline=INK, width=2)
    for i in range(4):
        d.line([dx + 6, y + 18 + i * 8, dx + 46, y + 18 + i * 8],
               fill=INK, width=2)
    ccx, ccy, cr = x + w - 52, y + 42, 27
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(252, 248, 238),
              outline=INK, width=3)
    d.line([ccx, ccy, ccx, ccy - cr + 7], fill=INK, width=3)
    d.line([ccx, ccy, ccx + cr - 11, ccy - 5], fill=INK, width=3)
    d.ellipse([ccx - 3, ccy - 3, ccx + 3, ccy + 3], fill=RED)
    d.rectangle([x + w // 2 - 78, y + h - 24, x + w // 2 + 78, y + h - 4],
                fill=DARKRED)
    centre(d, x + w // 2, y + h - 22, "DEAL IN SIGHT", SANSB(11), (255, 255, 255))

def ill_ukraine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for sx, sy in [(x + 24, y + 10), (x + 90, y + 16), (x + 170, y + 8),
                   (x + 250, y + 14), (x + 300, y + 10)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # skyline
    base = y + h - 30
    for bx, bw, bh in [(x + 8, 44, 34), (x + 58, 36, 52), (x + 100, 48, 28),
                       (x + 154, 30, 44), (x + 190, 52, 60), (x + 248, 40, 36),
                       (x + 292, 26, 48)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(16, 22, 44))
        for wy in range(base - bh + 6, base - 4, 10):
            for wx in range(bx + 5, bx + bw - 5, 11):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(241, 196, 15))
    # drone streaks: diagonal lines with a dot head
    for sx, sy, ex, ey in [(x + 40, y + 8, x + 90, y + 44),
                           (x + 150, y + 4, x + 190, y + 38),
                           (x + 230, y + 10, x + 268, y + 46),
                           (x + 280, y + 6, x + 312, y + 40)]:
        d.line([sx, sy, ex, ey], fill=(255, 255, 255), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(241, 196, 15))
    # fires on the skyline
    _flames(d, x + 100, base - 14, 60, 14, n=3)
    _flames(d, x + 230, base - 12, 44, 12, n=3)
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(20, 20, 26))
    d.rectangle([x + 10, y + 8, x + 104, y + 24], fill=RED)
    centre(d, x + 57, y + 10, "186 DRONES", SANSB(10), (255, 255, 255))


def ill_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for sx, sy in [(x + 30, y + 12), (x + 140, y + 8), (x + 260, y + 14)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(28, 68, 110))
    # oil tanks + flare stacks
    for tx, tw in [(x + 16, 62), (x + 92, 62), (x + 168, 62)]:
        d.rectangle([tx, y + h - 62, tx + tw, y + h - 22], fill=(200, 200, 210),
                    outline=INK, width=1)
        d.rectangle([tx, y + h - 62, tx + tw, y + h - 52], fill=(120, 120, 130))
    for fx in (x + 240, x + 272):
        d.rectangle([fx, y + h - 66, fx + 8, y + h - 22], fill=(90, 90, 100))
    _flames(d, x + 22, y + h - 76, 52, 16, n=3)
    _flames(d, x + 98, y + h - 74, 52, 14, n=3)
    _smoke(d, x + 240, y + h - 60)
    # missile arcs
    d.arc([x + 60, y - 30, x + 260, y + 50], 200, 340, fill=(241, 196, 15), width=3)
    d.arc([x + 120, y - 40, x + 300, y + 30], 200, 340, fill=(255, 255, 255), width=2)
    d.rectangle([x + w - 92, y + 8, x + w - 10, y + 24], fill=RED)
    centre(d, x + w - 51, y + 10, "2 BASES", SANSB(10), (255, 255, 255))


def ill_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for sx, sy in [(x + 30, y + 14), (x + 120, y + 10), (x + 220, y + 18),
                   (x + 280, y + 12)]:
        d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 255, 255))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(28, 68, 110))
    for wx in range(0, w, 34):
        d.arc([x + wx, y + h - 26, x + wx + 30, y + h - 8], 200, 340,
              fill=(180, 210, 230), width=2)
    hx, hy = x + 40, y + h - 62
    d.polygon([(hx, hy + 22), (hx + 20, hy), (hx + w - 90, hy),
               (hx + w - 70, hy + 22)], fill=(139, 35, 35))
    d.rectangle([hx + 30, hy - 22, hx + 70, hy], fill=(70, 90, 110))
    d.rectangle([hx + 80, hy - 22, hx + 120, hy], fill=(180, 160, 90))
    d.rectangle([hx + 130, hy - 22, hx + 170, hy], fill=(70, 90, 110))
    d.rectangle([hx + 200, hy - 30, hx + 226, hy], fill=(220, 220, 220))
    _flames(d, hx + 24, hy - 32, 190, 32, n=6)
    _smoke(d, hx + 60, hy - 28)


def ill_nepal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 30, y + 8, x + w - 6, y + 32], fill=(241, 196, 15))
    px, py = x + w // 2 - 58, y + 36
    d.polygon([(px, py + 6), (px + 96, py + 6), (px + 116, py + 12),
               (px + 96, py + 18), (px, py + 18)], fill=(252, 248, 238))
    d.polygon([(px + 12, py + 6), (px + 22, py - 14), (px + 32, py - 14),
               (px + 30, py + 6)], fill=(220, 220, 220))
    d.polygon([(px + 52, py + 18), (px + 62, py + 34), (px + 72, py + 34),
               (px + 70, py + 18)], fill=(200, 200, 200))
    for wx in range(px + 14, px + 92, 12):
        d.rectangle([wx, py + 10, wx + 5, py + 13], fill=NAVY)
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(120, 180, 120))
    for fx, cols in [(x + 26, [(255, 153, 51), (255, 255, 255), (19, 136, 8)]),
                     (x + w - 62, [(220, 20, 60), (0, 56, 147), (220, 20, 60)])]:
        d.line([fx, y + h - 30, fx, y + h - 62], fill=INK, width=2)
        for i, c in enumerate(cols):
            d.rectangle([fx, y + h - 62 + i * 9, fx + 30, y + h - 53 + i * 9],
                        fill=c)


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 225, 200))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(170, 160, 140))
    vx, vy = x + 30, y + h - 48
    d.rectangle([vx, vy, vx + 96, vy + 26], fill=(252, 248, 238), outline=INK, width=2)
    d.rectangle([vx + 96, vy + 8, vx + 124, vy + 26], fill=(200, 60, 60),
                outline=INK, width=2)
    d.rectangle([vx + 12, vy + 6, vx + 34, vy + 20], fill=(180, 120, 60))
    d.rectangle([vx + 42, vy + 6, vx + 64, vy + 20], fill=(120, 160, 90))
    d.rectangle([vx + 72, vy + 6, vx + 88, vy + 20], fill=(180, 120, 60))
    for wx in (vx + 22, vx + 108):
        d.ellipse([wx, vy + 22, wx + 14, vy + 36], fill=INK)
    dx, dy = x + w - 52, y + 12
    d.ellipse([dx, dy, dx + 22, dy + 8], fill=(60, 60, 60))
    d.line([dx - 8, dy + 2, dx + 30, dy + 2], fill=INK, width=2)
    d.line([dx + 4, dy + 8, dx + 18, dy + 22], fill=(231, 76, 60), width=2)


def ill_myanmar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 240))
    cx = x + w // 2
    d.polygon([(cx - 70, y + 18), (cx, y + 2), (cx + 70, y + 18)], fill=(150, 40, 40))
    for px in (cx - 56, cx - 20, cx + 14, cx + 50):
        d.rectangle([px, y + 20, px + 8, y + h - 20], fill=(240, 240, 235),
                    outline=INK, width=1)
    d.rectangle([cx - 72, y + h - 22, cx + 72, y + h - 14], fill=(150, 40, 40))
    sx, sy = x + 18, y + h - 46
    d.line([sx + 10, sy, sx + 10, sy - 18], fill=INK, width=2)
    d.line([sx - 8, sy - 18, sx + 28, sy - 18], fill=INK, width=2)
    d.polygon([(sx - 10, sy - 6), (sx - 2, sy - 6), (sx - 6, sy + 2)], fill=GOLD)
    d.polygon([(sx + 14, sy - 6), (sx + 22, sy - 6), (sx + 18, sy + 2)], fill=GOLD)


def ill_hongkong(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 235, 245))
    # skyline
    base = y + h - 18
    for bx, bw, bh in [(x + 6, 26, 30), (x + 36, 20, 44), (x + 60, 24, 36),
                       (x + 150, 22, 40), (x + 176, 18, 30)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(90, 110, 140))
        for wy in range(base - bh + 5, base - 3, 9):
            for wx in range(bx + 4, bx + bw - 4, 8):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(241, 196, 15))
    # ballot box + ballot
    bx, by = x + w // 2 - 26, y + h - 52
    d.rectangle([bx, by, bx + 52, by + 34], fill=(185, 28, 28))
    d.rectangle([bx + 8, by - 6, bx + 44, by], fill=(140, 20, 20))
    d.polygon([(bx + 14, by - 22), (bx + 30, by - 26), (bx + 40, by - 12),
               (bx + 26, by - 6)], fill=(252, 248, 238), outline=INK)


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 110))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 140, 70))
    sx = x + w - 40
    for i in range(3):
        d.line([sx + i * 7, y + h - 44, sx + i * 7, y + h - 16], fill=(240, 220, 160),
               width=3)
    d.rectangle([sx - 2, y + h - 48, sx + 18, y + h - 44], fill=(240, 220, 160))
    bx, by = x + 52, y + 22
    d.ellipse([bx - 9, by, bx + 9, by + 18], fill=(30, 30, 30))
    d.polygon([(bx - 10, by + 18), (bx + 10, by + 18), (bx + 14, y + h - 16),
               (bx - 14, y + h - 16)], fill=(20, 60, 140))
    d.line([bx + 8, by + 26, bx + 30, by + 52], fill=(200, 170, 120), width=5)
    d.ellipse([x + w - 66, y + 12, x + w - 54, y + 24], fill=(185, 28, 28))


def ill_lasvegas(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for sx, sy in [(x + 20, y + 8), (x + 90, y + 12), (x + 170, y + 8)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # strip skyline with lit windows
    base = y + h - 24
    for bx, bw, bh, c in [(x + 8, 30, 26, (200, 60, 120)),
                          (x + 44, 22, 38, (60, 140, 200)),
                          (x + 72, 26, 30, (220, 160, 40)),
                          (x + 150, 24, 40, (200, 60, 120)),
                          (x + 178, 20, 28, (60, 140, 200))]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=c)
        for wy in range(base - bh + 4, base - 3, 8):
            for wx in range(bx + 3, bx + bw - 3, 7):
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 255, 160))
    # track + race car
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(50, 50, 55))
    for lx in range(x + 4, x + w, 22):
        d.rectangle([lx, y + h - 13, lx + 12, y + h - 10], fill=(255, 255, 255))
    cx, cy = x + w // 2 - 44, y + h - 46
    d.polygon([(cx, cy + 12), (cx + 18, cy + 4), (cx + 66, cy + 4),
               (cx + 88, cy + 12), (cx + 80, cy + 18), (cx + 8, cy + 18)],
              fill=(185, 28, 28))
    d.polygon([(cx + 30, cy + 4), (cx + 38, cy - 8), (cx + 56, cy - 8),
               (cx + 62, cy + 4)], fill=(220, 220, 230))
    d.ellipse([cx + 14, cy + 14, cx + 28, cy + 26], fill=INK)
    d.ellipse([cx + 62, cy + 14, cx + 76, cy + 26], fill=INK)
    # chequered flag
    fx, fy = x + w - 34, y + 8
    for r in range(3):
        for c in range(3):
            if (r + c) % 2 == 0:
                d.rectangle([fx + c * 7, fy + r * 7, fx + c * 7 + 7, fy + r * 7 + 7],
                            fill=INK)
            else:
                d.rectangle([fx + c * 7, fy + r * 7, fx + c * 7 + 7, fy + r * 7 + 7],
                            fill=(255, 255, 255))
    d.line([fx, fy, fx, fy + 26], fill=INK, width=2)


def ill_iran_elec(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(35, 45, 70))
    # dark city, mostly unlit
    base = y + h - 16
    for bx, bw, bh in [(x + 8, 34, 26), (x + 48, 26, 38), (x + 80, 30, 22),
                       (x + 150, 28, 34), (x + 182, 22, 26)]:
        d.rectangle([bx, base - bh, bx + bw, base], fill=(15, 18, 32))
    # one lit window row
    for wx in range(x + 52, x + 70, 8):
        d.rectangle([wx, base - 30, wx + 4, base - 25], fill=(241, 196, 15))
    # pylon + lightning
    px = x + w // 2 + 30
    d.line([px, y + 12, px, y + h - 16], fill=(180, 180, 190), width=3)
    d.line([px - 18, y + 22, px + 18, y + 22], fill=(180, 180, 190), width=3)
    d.line([px - 14, y + 34, px + 14, y + 34], fill=(180, 180, 190), width=2)
    lx = x + 66
    d.polygon([(lx, y + 6), (lx + 12, y + 6), (lx + 4, y + 26), (lx + 14, y + 26),
               (lx - 2, y + 50), (lx + 4, y + 28), (lx - 4, y + 28)],
              fill=(241, 196, 15))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(20, 22, 30))


def ill_bolsonaro(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 240, 238))
    # hospital bed + patient + monitor
    bx, by = x + 22, y + h - 44
    d.rectangle([bx, by, bx + 120, by + 12], fill=(252, 248, 238), outline=INK, width=2)
    d.rectangle([bx, by - 14, bx + 22, by], fill=(252, 248, 238), outline=INK, width=2)
    d.ellipse([bx + 4, by - 26, bx + 24, by - 6], fill=(232, 190, 150))
    d.rectangle([bx + 24, by - 10, bx + 60, by], fill=(120, 160, 200))
    for lx in (bx + 6, bx + 116):
        d.line([lx, by + 12, lx, by + 26], fill=INK, width=2)
    d.line([bx + 6, by + 26, bx + 116, by + 26], fill=INK, width=2)
    # IV drip
    d.line([bx + 128, y + 14, bx + 128, by - 6], fill=INK, width=2)
    d.rectangle([bx + 122, y + 14, bx + 134, y + 30], fill=(200, 220, 240),
                outline=INK, width=1)
    # monitor with heartbeat line
    mx, my = x + w - 62, y + 10
    d.rectangle([mx, my, mx + 52, my + 34], fill=(26, 26, 26))
    d.line([(mx + 4, my + 20), (mx + 14, my + 20), (mx + 20, my + 8),
            (mx + 26, my + 28), (mx + 32, my + 14), (mx + 40, my + 20),
            (mx + 48, my + 20)], fill=(80, 220, 120), width=2)


def ill_aukus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(28, 68, 110))
    for wx in range(0, w, 30):
        d.arc([x + wx, y + h - 26, x + wx + 28, y + h - 10], 200, 340,
              fill=(140, 190, 220), width=2)
    # submarine
    sx, sy = x + w // 2 - 70, y + h // 2 - 6
    d.ellipse([sx, sy, sx + 140, sy + 30], fill=(40, 45, 55))
    d.rectangle([sx + 56, sy - 14, sx + 84, sy + 2], fill=(40, 45, 55))
    d.polygon([(sx + 140, sy + 6), (sx + 158, sy + 15), (sx + 140, sy + 24)],
              fill=(40, 45, 55))
    d.polygon([(sx + 10, sy + 26), (sx + 26, sy + 26), (sx + 18, sy + 40)],
              fill=(40, 45, 55))
    for wx in range(sx + 16, sx + 124, 18):
        d.ellipse([wx, sy + 11, wx + 7, sy + 18], fill=(241, 196, 15))
    # bubbles
    for bx, by, br in [(sx + 30, sy - 26, 3), (sx + 60, sy - 34, 4),
                       (sx + 100, sy - 28, 3)]:
        d.ellipse([bx - br, by - br, bx + br, by + br], outline=(200, 220, 235),
                  width=1)


ILLS = {"cop31": ill_cop31, "ukraine": ill_ukraine, "bahrain": ill_bahrain,
        "sparta": ill_sparta, "hongkong": ill_hongkong, "cricket": ill_cricket,
        "lasvegas": ill_lasvegas, "nepal": ill_nepal, "gaza": ill_gaza,
        "iran_elec": ill_iran_elec, "bolsonaro": ill_bolsonaro,
        "aukus": ill_aukus, "myanmar": ill_myanmar}

# ------------------------------------------------------------------- map
# Simplified continent outlines as (lon, lat) polygons, equirectangular.
NA = [(-168, 66), (-150, 70), (-135, 69), (-125, 71), (-115, 73), (-105, 73),
      (-95, 80), (-85, 70), (-80, 73), (-75, 62), (-65, 60), (-60, 55),
      (-55, 52), (-60, 47), (-65, 44), (-70, 42), (-75, 35), (-80, 26),
      (-81, 31), (-85, 30), (-90, 21), (-95, 19), (-97, 16), (-102, 18),
      (-105, 22), (-110, 24), (-114, 28), (-120, 34), (-124, 40), (-124, 48),
      (-130, 55), (-140, 60), (-150, 61), (-158, 58), (-162, 60), (-165, 62)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 65), (-32, 68), (-22, 70),
             (-20, 74), (-25, 76), (-35, 80), (-45, 80), (-55, 76), (-58, 72)]
SA = [(-78, 8), (-75, 5), (-72, 10), (-64, 11), (-60, 8), (-52, 5), (-50, 0),
      (-44, -3), (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-55, -35),
      (-65, -40), (-70, -50), (-73, -54), (-72, -45), (-73, -35), (-75, -20),
      (-78, -10), (-80, -3), (-80, 5)]
AFRICA = [(-17, 15), (-16, 20), (-12, 27), (-8, 31), (-2, 35), (5, 37),
          (10, 37), (15, 32), (20, 32), (25, 32), (30, 31), (34, 28),
          (36, 22), (39, 18), (43, 12), (48, 11), (51, 10), (46, 5), (42, 0),
          (40, -5), (38, -12), (35, -18), (32, -25), (28, -32), (20, -35),
          (16, -30), (14, -22), (12, -15), (10, -5), (9, 4), (4, 6), (-4, 5),
          (-8, 5), (-13, 8), (-16, 12)]
EURASIA = [(-9, 37), (-9, 43), (-2, 44), (-1, 46), (0, 48), (3, 50), (7, 54),
           (8, 57), (12, 56), (18, 56), (21, 55), (24, 58), (28, 59),
           (26, 62), (24, 66), (28, 70), (35, 68), (42, 68), (48, 69),
           (55, 69), (62, 70), (70, 72), (78, 73), (88, 74), (100, 76),
           (110, 74), (120, 73), (130, 72), (140, 72), (150, 70), (158, 69),
           (162, 66), (170, 66), (178, 65), (178, 62), (170, 60), (162, 58),
           (158, 55), (155, 59), (150, 60), (142, 55), (140, 50), (137, 45),
           (135, 42), (130, 38), (127, 35), (122, 32), (120, 28), (115, 23),
           (110, 20), (108, 15), (105, 9), (103, 7), (100, 8), (98, 12),
           (95, 16), (92, 21), (89, 22), (86, 20), (82, 17), (80, 13),
           (77, 8), (76, 10), (73, 16), (70, 20), (66, 25), (62, 25),
           (58, 26), (56, 27), (54, 26), (51, 29), (49, 30), (47, 30),
           (44, 32), (42, 35), (40, 36), (36, 36), (33, 36), (30, 36),
           (27, 37), (23, 36), (20, 39), (18, 40), (15, 42), (12, 44),
           (8, 44), (5, 43), (3, 42), (0, 39), (-2, 37), (-6, 36)]
UK = [(-5, 50), (-3, 53), (-1, 54), (-2, 57), (-4, 58), (-6, 55)]
JAPAN = [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
         (142, 44), (140, 44), (138, 40), (136, 36), (133, 34), (130, 33)]
SUMATRA = [(95, 5), (98, 2), (100, -1), (102, -3), (104, -5), (106, -6),
           (104, -4), (101, -1), (98, 2)]
JAVA = [(105, -6), (110, -7), (114, -8), (114, -7), (108, -6)]
BORNEO = [(109, 1), (112, 3), (116, 5), (118, 1), (117, -2), (114, -3),
          (111, -2), (109, 0)]
NEWGUINEA = [(131, -1), (136, -2), (140, -4), (141, -8), (138, -8),
             (135, -5), (132, -3)]
AUSTRALIA = [(113, -22), (114, -28), (115, -33), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (146, -39), (150, -37), (153, -32), (153, -27), (150, -22),
             (146, -19), (142, -11), (140, -14), (136, -12), (132, -11),
             (128, -14), (124, -16), (120, -19), (116, -20), (113, -22)]
NZ = [(167, -45), (168, -44), (170, -42), (173, -40), (175, -38), (177, -38),
      (175, -40), (172, -42), (169, -44)]
LAND = [NA, GREENLAND, SA, AFRICA, EURASIA, UK, JAPAN, SUMATRA, JAVA, BORNEO,
        NEWGUINEA, AUSTRALIA, NZ]


def _in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xin = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xin:
                inside = not inside
        j = i
    return inside


def draw_map(d, x0, y0, w, h):
    """Filled-continent world map with numbered pins for the 13 pictured stories."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAPSEA, outline=INK, width=1)
    lon0, lon1, lat0, lat1 = -180.0, 180.0, 85.0, -60.0

    def proj(lon, lat):
        return (x0 + (lon - lon0) / (lon1 - lon0) * w,
                y0 + (lat0 - lat) / (lat0 - lat1) * h)

    for poly in LAND:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=SAND, outline=(150, 128, 84))
    for s in LEADS + MED:
        lon, lat = s["pin"]
        px, py = proj(lon, lat)
        r = 7
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=(255, 255, 255),
                  width=1)
        t = str(s["n"])
        f = SANSB(8)
        d.text((px - f.getlength(t) / 2, py - 5.5), t, font=f, fill=(255, 255, 255))

# ------------------------------------------------------------------- layout
def tag_colour(tag):
    return {"CONFIRMED": GREEN, "REPORTED": GREY, "FORECAST": NAVY}.get(tag, GREY)


def draw_lead(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=1)
    ih = 96
    ILLS[s["ill"]](d, x + 1, y + 1, w - 2, ih)
    d.line([x, y + ih + 1, x + w, y + ih + 1], fill=INK, width=1)
    ky = y + ih + 7
    d.text((x + 8, ky), f"{s['n']}  {s['kicker']}", font=SANSB(11), fill=RED)
    tw = SANSB(9).getlength(s["tag"])
    d.text((x + w - 8 - tw, ky + 1), s["tag"], font=SANSB(9),
           fill=tag_colour(s["tag"]))
    hy = block(d, x + 8, ky + 18, w - 16, s["head"], SERIFB(19),
               leading=22, max_lines=2)
    block(d, x + 8, hy + 5, w - 16, s["deck"], SANS(11.5), leading=13.5,
          max_lines=3)


def draw_med(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=1)
    ih = 56
    ILLS[s["ill"]](d, x + 1, y + 1, w - 2, ih)
    # red tag bar across the top of the picture
    tf = SANSB(8)
    tw = tf.getlength(s["tag"]) + 10
    d.rectangle([x + 1, y + 1, x + 1 + tw, y + 13], fill=RED)
    d.text((x + 6, y + 2), s["tag"], font=tf, fill=(255, 255, 255))
    d.line([x, y + ih + 1, x + w, y + ih + 1], fill=INK, width=1)
    ky = y + ih + 4
    d.text((x + 6, ky), f"{s['n']}  {s['kicker']}", font=SANSB(8.5),
           fill=tag_colour(s["tag"]))
    hy = block(d, x + 6, ky + 14, w - 12, s["head"], SERIFB(12.5),
               leading=14, max_lines=2)
    block(d, x + 6, hy + 3, w - 12, s["deck"], SANS(9.5), leading=11,
          max_lines=2)


def draw():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    # top band
    d.rectangle([0, 0, W, 22], fill=NAVY)
    d.text((14, 4), "THE WORLD IN ONE DAY \u2014 LATE EDITION",
           font=SANSB(11), fill=(255, 255, 255))
    rt = "38 STORIES \u00b7 6 REGIONS \u00b7 SUNDAY 22 NOVEMBER 2026"
    d.text((W - 14 - SANSB(11).getlength(rt), 4), rt, font=SANSB(11),
           fill=(255, 255, 255))
    # masthead
    centre(d, W // 2, 28, "Sunday 22 November 2026", SERIFB(52), INK)
    d.line([14, 84, W - 14, 84], fill=INK, width=2)
    centre(d, W // 2, 90,
           "COP31 puts its final deal to the vote \u00b7 Verstappen wins "
           "the Las Vegas GP \u00b7 186 drones over Ukraine overnight",
           SERI(16), INK)
    # stat strip
    stats = [("186", "drones fired at Ukraine"),
             ("161", "drones downed"),
             ("856", "candidates, Hong Kong vote"),
             ("720/9", "India's record Test total"),
             ("35%", "electricity share by 2035"),
             ("24", "dead, Nigeria boat")]
    sw, gap = 162, 4
    for i, (num, lab) in enumerate(stats):
        x = 14 + i * (sw + gap)
        d.rectangle([x, 108, x + sw, 142], fill=PAPER, outline=LINE, width=1)
        centre(d, x + sw // 2, 111, num, SANSB(19), RED)
        centre(d, x + sw // 2, 131, lab, SANS(9), GREY)
    # UTC timeline
    d.line([14, 162, W - 14, 162], fill=RED, width=2)
    tl = [("03:00 GMT", "COP31 objections close"),
          ("05:30 GMT", "Las Vegas GP ends"),
          ("08:00 GMT", "COP31 approval opens"),
          ("09:00 HKT", "Hong Kong polls open"),
          ("16:30 GMT", "Liverpool v Man Utd"),
          ("17:00 GMT", "ATP final, Turin")]
    tw = (W - 28) // len(tl)
    for i, (t, lab) in enumerate(tl):
        cx = 14 + i * tw + tw // 2
        d.ellipse([cx - 4, 158, cx + 4, 166], fill=RED)
        centre(d, cx, 146, t, SANSB(9), RED)
        centre(d, cx, 168, lab, SANS(8.5), INK)
    # region bar
    rx, ry = 14, 184
    total = sum(n for _, n, _ in REGIONS)
    bx = rx
    for name, n, col in REGIONS:
        segw = int((W - 28) * n / total)
        d.rectangle([bx, ry, bx + segw - 1, ry + 18], fill=col)
        label = f"{name} {n}"
        fnt = SANSB(10)
        while fnt.getlength(label) > segw - 6 and fnt.size > 7:
            fnt = SANSB(fnt.size - 1)
        centre(d, bx + segw // 2, ry + 3, label, fnt, (255, 255, 255))
        bx += segw
    # leads
    lw, lgap = 326, 6
    for i, s in enumerate(LEADS):
        draw_lead(d, s, 14 + i * (lw + lgap), 206, lw, 218)
    # medium rows, 5 per row
    mw, mgap = 196, 5
    for i, s in enumerate(MED):
        row, col = divmod(i, 5)
        draw_med(d, s, 14 + col * (mw + mgap), 428 + row * 138, mw, 134)
    # section headers
    d.text((14, 704), "WHERE IT HAPPENED \u2014 pins 1\u201313",
           font=SANSB(11), fill=INK)
    d.text((350, 704), "ALSO ON SUNDAY 22 NOVEMBER \u2014 25 MORE STORIES",
           font=SANSB(11), fill=INK)
    d.line([14, 718, W - 14, 718], fill=INK, width=2)
    # map + ALSO list
    draw_map(d, 14, 722, 322, 162)
    colw = 324
    for i, (n, txt, _reg) in enumerate(ALSO):
        col, row = divmod(i, 13)
        x = 350 + col * (colw + 12)
        y = 724 + row * 12.5
        item = f"{n}  {txt}"
        fnt = SANS(9.5)
        while fnt.getlength(item) > colw - 2 and fnt.size > 7.5:
            fnt = SANS(fnt.size - 1)
        d.text((x, y), item, font=fnt, fill=INK)
    # DATE CHECK box
    d.rectangle([14, 884, W - 14, 956], outline=DARKRED, width=2)
    d.text((22, 890),
           "DATE CHECK \u2014 LATE EDITION \u00b7 WIRES AS OF 09:30 UTC, "
           "SUNDAY 22 NOVEMBER 2026", font=SANSB(11), fill=DARKRED)
    block(d, 22, 908, W - 44,
          "Left out as other days' news: Peru's 6.7 quake (20 Nov local) \u00b7 "
          "the 400-drone barrage (19\u201320 Nov) \u00b7 Russian missiles in "
          "Poland (Fri 20 Nov) \u00b7 the Shenzhen summit (Fri 20 Nov) \u00b7 "
          "\u201cEl Chapo Isidro\u201d seized (Fri 21 Nov) \u00b7 Roundup $7.25bn "
          "approved (Fri 20 Nov) \u00b7 BepiColombo at Mercury (Sat 18:24 UTC) "
          "\u00b7 Somalia orders the UAE envoy out (Thu 19 Nov).",
          SANS(10.5), leading=13, max_lines=2)
    block(d, 22, 936, W - 44,
          "Sparta II was hit Saturday morning \u2014 still ablaze Sunday. "
          "Not yet decided at press time: COP31's final approval \u00b7 the "
          "ATP final \u00b7 Liverpool v Man Utd.",
          SANS(10.5), leading=13, max_lines=1)
    # footer
    block(d, 14, 962, W - 28,
          "Every story here happened, or was first reported, on Sunday 22 November "
          "2026, or on Saturday night. Sources named beside each story. Pictures: "
          "original, drawn in code. HOW WE CHECKED \u2014 CONFIRMED = 2+ outlets "
          "\u00b7 REPORTED = one outlet \u00b7 FORECAST = scheduled today.",
          SANS(9), fill=GREY, leading=12, max_lines=2)
    return img


if __name__ == "__main__":
    im = draw()
    im.save("entry.png", optimize=True)
    print("wrote entry.png", im.size)
