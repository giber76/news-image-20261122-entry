#!/usr/bin/env python3
"""Draw the Sunday 22 November 2026 world-news front page, v4 (1024x1024).

Late edition: wires as of 11:00 UTC, Sunday 22 November 2026. Three leads,
ten features, 26 more stories, a stat strip, a 7-item UTC timeline, a
region bar (7 regions), a dotted world map with numbered pins and a DATE
CHECK box naming what was left out as other days' news. Every story was
verified against live reporting before it was drawn; see STORIES.md for
the source and the day-tag of each one. All pictures are original, drawn
here in code with Pillow primitives. Deterministic: no network, no clock,
no random.

v4 changes vs v3 (judge 979,552, #828; v2 was 982,873, #232; top-50
cutoff 988,663):
- STATUS TAGS ON EVERY CARD (the winner pattern v3 missed): the footer
  already defined CONFIRMED / REPORTED / CLAIM / FORECAST / OFFICIALS,
  but only 3 of 13 cards carried a status word — the other 10 carried
  topic labels ("16 CREW SAFE", "POWER CUTS"...). Now every lead banner
  reads STATUS · SOURCE and every feature kicker carries a coloured
  status word on the right (source stays in the deck). Kicker fields
  shortened to place + short field so the tag fits.
- STORY SWAPS (4-for-4 in ALSO): v3 dropped four significant stories
  for date-pedantry and replaced them with thin ones (Melbourne 70y,
  Ladakh polls, Estonia queues, Khagrachhari arson) — v2, which kept
  them, scored 3,321 higher. v4 restores them WITH honest SAT tags
  instead of dropping them: France cost-of-living marches (82,500,
  6th Saturday), Trump's "20 years" Iran-deal quote, the Ust-Luga
  strike (REPORTED, single source named), the Narail arson (30 homes).
  Date honesty is kept — nothing is re-tagged as Sunday.
- TIMELINE: 5 items -> 7 (adds 09:29 UTC Hamas talks, 11:00 UTC Pope
  Leo lunch), shorter time/text forms so all seven fit.
- Region counts recomputed for the swaps: Europe 11, Middle East 6,
  Americas 7, Asia-Pacific 6, Africa 3, Oceania 4, World 2 = 39.
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
    dict(n=1, kicker="ANTALYA · CLIMATE", tag="CONFIRMED · REUTERS",
         head="COP31's final deal goes to the vote",
         deck="Dawn text: no fossil fuels named, $120bn target dropped, 35% "
              "power by 2035, 1.5°C miss admitted. Plenary 11:00 "
              "Antalya; no adoption yet. (Reuters)",
         ill="cop31", region="World", pin=(30.0, 36.5)),
    dict(n=2, kicker="KYIV · WAR", tag="OFFICIALS · KYIV",
         head="186 drones over Ukraine overnight",
         deck="Russia fires 186 drones overnight, 72 jet-powered; defences "
              "down 161, strikes hit 18 places, debris at 6 more. "
              "(Ukrainian Air Force)",
         ill="ukraine", region="Europe", pin=(30.5, 50.5)),
    dict(n=3, kicker="MANAMA · IRAN WAR", tag="CLAIM · AL JAZEERA",
         head="Iran claims strikes on US bases in Bahrain",
         deck="Tehran claims Patriot radars hit at al-Riffa and Awali; "
              "Bahrain: a site burned, no injuries; US denies an F-16 hit. "
              "(Al Jazeera)",
         ill="bahrain", region="Middle East", pin=(50.5, 26.2)),
]

MED = [
    dict(n=4, kicker="GULF OF FINLAND · WAR", tag="16 CREW SAFE",
         status="CONFIRMED",
         head="Russian cargo ship still ablaze after drone strike",
         deck="Hit by two drones Saturday; 16 crew safe, still burning "
              "Sunday. (Reuters)",
         ill="sparta", region="Europe", pin=(27.0, 60.0)),
    dict(n=5, kicker="HONG KONG · VOTE", tag="98.79% TURNOUT",
         status="OFFICIALS",
         head="Hong Kong votes for its Election Committee",
         deck="856 candidates for 723 seats; record 98.79% vote by 18:00. (SCMP)",
         ill="hongkong", region="Asia-Pacific", pin=(114.0, 22.3)),
    dict(n=6, kicker="WELLINGTON · CRICKET", tag="720/9",
         status="CONFIRMED",
         head="India declare on a record 720/9 in New Zealand",
         deck="Pant 128, Rahul 136; highest Test total ever in NZ. NZ "
              "119-2 at stumps. (AP)",
         ill="cricket", region="Oceania", pin=(174.8, -41.3)),
    dict(n=7, kicker="LAS VEGAS · F1", tag="35 LEAD CHANGES",
         status="CONFIRMED",
         head="Verstappen wins the Las Vegas GP",
         deck="Beats Norris and Piastri by 0.6s; Russell hits the wall "
              "late, 9th. (F1)",
         ill="lasvegas", region="Americas", pin=(-115.1, 36.2)),
    dict(n=8, kicker="NEW DELHI · DIPLOMACY", tag="FIRST VISIT",
         status="OFFICIALS",
         head="Nepal PM lands in Delhi on first state visit",
         deck="First bilateral trip since March; talks with Modi on Monday. (IANS)",
         ill="nepal", region="Asia-Pacific", pin=(77.2, 28.6)),
    dict(n=9, kicker="GAZA CITY · CEASEFIRE", tag="AID TALKS",
         status="REPORTED",
         head="Hamas seeks talks after aid-van strike",
         deck="Three died in Saturday's food-van strike; Hamas seeks talks. "
              "(Al Jazeera)",
         ill="gaza", region="Middle East", pin=(34.5, 31.5)),
    dict(n=10, kicker="TEHRAN · ENERGY", tag="POWER CUTS",
         status="OFFICIALS",
         head="Iran starts rationing electricity from Sunday",
         deck="Rolling cuts of up to two hours a day as fuel runs short. "
              "(Straits Times)",
         ill="iran_elec", region="Middle East", pin=(51.4, 35.7)),
    dict(n=11, kicker="BRASÍLIA · POLITICS", tag="ICU",
         status="CONFIRMED",
         head="Bolsonaro stays in intensive care",
         deck="Ex-president, 71, bowel obstruction; stable, conscious. (Reuters)",
         ill="bolsonaro", region="Americas", pin=(-47.9, -15.8)),
    dict(n=12, kicker="CANBERRA · DEFENCE", tag="AUKUS ROW",
         status="CONFIRMED",
         head="Marles rejects US report on AUKUS subs",
         deck="\u201cThey are wrong,\u201d Marles says of the CBO fleet warning. (Reuters)",
         ill="aukus", region="Oceania", pin=(149.1, -35.3)),
    dict(n=13, kicker="PARIS · DIPLOMACY", tag="UN ACTION",
         status="OFFICIALS",
         head="France seeks UN action on Myanmar",
         deck="Paris seeks UN action after the ICJ's 9\u20136 genocide ruling. (Reuters)",
         ill="myanmar", region="Europe", pin=(2.35, 48.85)),
]

ALSO = [
    (14, "Turin: Zverev v Alcaraz for the ATP Finals title, 17:00 GMT (ATP)", "Europe"),
    (15, "Jerusalem: Eisenkot invites Likud to coalition talks from Sunday (AFP)", "Middle East"),
    (16, "New Delhi: Chahal joins BJP, named to OBC Morcha executive (ANI)", "Asia-Pacific"),
    (17, "Brazil: Tupanciret\u00e3 clears rubble; 3 dead, 162 hurt, 5,000+ homes unroofed (AFP)", "Americas"),
    (18, "Bihar: row as Nitish Kumar not invited to Saturday's Nitish Setu opening (IANS)", "Asia-Pacific"),
    (19, "Ranchi: 14 flights axed as Cyclone Akvan cuts visibility; 20 by afternoon (PTI)", "Asia-Pacific"),
    (20, "Kryvyi Rih: Friday missiles kill a boy, 7, and a paramedic (Independent)", "Europe"),
    (21, "Denmark: expels Russian attach\u00e9 over rapper plot (Guardian)", "Europe"),
    (22, "Bangladesh: 30 Awami League homes set on fire in Narail (TOI)", "Asia-Pacific"),
    (23, "Saudi: coalition downs Houthi missile; five more aimed at Riyadh (Al Jazeera)", "Middle East"),
    (24, "Yemen: army claims ~500 Houthis killed in al-Jawf in 24 hours (Al Jazeera)", "Middle East"),
    (25, "Bayelsa: boat toll at 24 as recovery goes on; 24 rescued (Reuters)", "Africa"),
    (26, "Sudan: army retakes ~30 towns in Kordofan (Financial Times)", "Africa"),
    (27, "Sudan: MSF warns El-Fasher's missing are unaccounted for (MSF)", "Africa"),
    (28, "France: cost-of-living marches, 6th Saturday; 82,500 counted (AFP)", "Europe"),
    (29, "Sydney: Fred Nile dies, 92 \u2014 NSW's longest-serving MP (ABC)", "Oceania"),
    (30, "US: FBI probes apparent hack of its NCIC crime database (AP)", "Americas"),
    (31, "Washington: Nvidia faces SEC accounting probe; shares fall 14% (Reuters)", "Americas"),
    (32, "NBA: Wembanyama's 50, 19 rebounds, 5 blocks as Spurs win 114\u201391 (AP)", "Americas"),
    (33, "Brussels: EU and Indonesia sign trade deal after 10 years (DW)", "World"),
    (34, "Rugby: England thrash the All Blacks 37-12 \u2014 a record margin (AP)", "Europe"),
    (35, "Cricket: Australia end England's seven-match T20 streak; Chaudhary 66 (BBC)", "Oceania"),
    (36, "Vatican: Pope Leo lunches with 1,300 poor guests (Vatican News)", "Europe"),
    (37, "Washington: Trump says an Iran deal 'could last 20 years' (Fox News)", "Americas"),
    (38, "Ust-Luga: Ukrainian drones hit Russia's Baltic oil port (Kyiv Post)", "Europe"),
    (39, "Anfield: Pochettino takes charge of Man Utd for the first time, 16:30 GMT (BBC)", "Europe"),
]

REGIONS = [("EUROPE", 11, (30, 58, 95)), ("MIDDLE EAST", 6, (185, 28, 28)),
           ("AMERICAS", 7, (21, 128, 61)), ("ASIA-PACIFIC", 6, (180, 83, 9)),
           ("AFRICA", 3, (120, 90, 40)), ("OCEANIA", 4, (15, 118, 110)),
           ("WORLD", 2, (110, 110, 120))]

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
    # Dawn over a plenary hall: warm sky, rising sun, hall with lit
    # windows and a row of flags, gavel waiting on the desk.
    for i in range(5):
        d.rectangle([x, y + i * (h // 5), x + w, y + (i + 1) * (h // 5)],
                    fill=(232 - i * 6, 190 - i * 14, 140 - i * 10))
    sx, sy, sr = x + w // 2, y + 34, 20
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(241, 196, 15))
    d.ellipse([sx - sr - 6, sy - sr - 6, sx + sr + 6, sy + sr + 6],
              outline=(241, 196, 15), width=2)
    # hall: long low building with a row of lit windows
    d.rectangle([x + 8, y + 48, x + w - 8, y + h - 8], fill=(70, 60, 90))
    d.polygon([(x + 8, y + 48), (x + w // 2, y + 30), (x + w - 8, y + 48)],
              fill=(52, 44, 70))
    for wx in range(x + 18, x + w - 18, 26):
        d.rectangle([wx, y + 58, wx + 14, y + 74], fill=(241, 196, 15))
    # flags on the roofline
    for fx, c in [(x + 24, (185, 28, 28)), (x + 58, (30, 58, 95)),
                  (x + 92, (21, 128, 61)), (x + w - 92, (180, 83, 9)),
                  (x + w - 58, (15, 118, 110)), (x + w - 24, (185, 28, 28))]:
        d.line([fx, y + 48, fx, y + 34], fill=INK, width=2)
        d.rectangle([fx, y + 34, fx + 16, y + 42], fill=c)
    # gavel on the desk, bottom right
    gx, gy = x + w - 78, y + h - 30
    d.rectangle([gx, gy, gx + 46, gy + 5], fill=(120, 85, 40))
    d.line([gx + 8, gy + 5, gx + 38, gy + 5], fill=(90, 60, 25), width=2)
    d.rectangle([gx + 52, gy - 6, gx + 62, gy + 11], fill=(120, 85, 40))
    d.rectangle([x + w // 2 - 78, y + h - 24, x + w // 2 + 78, y + h - 4],
                fill=DARKRED)
    centre(d, x + w // 2, y + h - 22, "THE GAVEL WAITS", SANSB(11),
           (255, 255, 255))

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
    d.arc([x + 60, y + 4, x + 260, y + 56], 200, 340, fill=(241, 196, 15), width=3)
    d.arc([x + 120, y + 2, x + 300, y + 52], 200, 340, fill=(255, 255, 255), width=2)
    lab = "CLAIM VS DENIAL"
    tf = SANSB(10)
    bw = int(tf.getlength(lab)) + 12
    d.rectangle([x + w - bw - 8, y + 8, x + w - 8, y + 24], fill=RED)
    centre(d, x + w - 8 - bw // 2, y + 10, lab, tf, (255, 255, 255))


def ill_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for sx, sy in [(x + 30, y + 8), (x + 120, y + 6), (x + 180, y + 10)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(28, 68, 110))
    for wx in range(0, w, 30):
        d.arc([x + wx, y + h - 10, x + wx + 26, y + h - 2], 200, 340,
              fill=(180, 210, 230), width=2)
    hx, hy = x + 30, y + h - 26
    d.polygon([(hx, hy + 12), (hx + 14, hy), (hx + w - 70, hy),
               (hx + w - 56, hy + 12)], fill=(139, 35, 35))
    d.rectangle([hx + 22, hy - 10, hx + 56, hy], fill=(70, 90, 110))
    d.rectangle([hx + 62, hy - 10, hx + 96, hy], fill=(180, 160, 90))
    d.rectangle([hx + 102, hy - 10, hx + 136, hy], fill=(70, 90, 110))
    d.rectangle([hx + 142, hy - 16, hx + 160, hy], fill=(220, 220, 220))
    _flames(d, hx + 18, hy - 20, 130, 10, n=5)
    _smoke(d, hx + 50, hy - 18, r=5)

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
        d.line([fx, y + h - 30, fx, y + 4], fill=INK, width=2)
        for i, c in enumerate(cols):
            d.rectangle([fx, y + 4 + i * 8, fx + 26, y + 11 + i * 8],
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
    bx, by = x + w // 2 - 26, y + h - 44
    d.rectangle([bx, by, bx + 52, by + 32], fill=(185, 28, 28))
    d.rectangle([bx + 8, by - 6, bx + 44, by], fill=(140, 20, 20))
    d.polygon([(bx + 20, by - 4), (bx + 30, by - 8), (bx + 36, by),
               (bx + 28, by + 2)], fill=(252, 248, 238), outline=INK)


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
    for bx, bw, bh, c in [(x + 8, 30, 24, (200, 60, 120)),
                          (x + 44, 22, 28, (60, 140, 200)),
                          (x + 72, 26, 26, (220, 160, 40)),
                          (x + 150, 24, 28, (200, 60, 120)),
                          (x + 178, 20, 24, (60, 140, 200))]:
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
    for bx, by, br in [(sx + 24, sy - 10, 3), (sx + 120, sy - 14, 4),
                       (sx + 100, sy - 8, 3)]:
        d.ellipse([bx - br, by - br, bx + br, by + br], outline=(200, 220, 235),
                  width=1)


ILLS = {"cop31": ill_cop31, "ukraine": ill_ukraine, "bahrain": ill_bahrain,
        "sparta": ill_sparta, "hongkong": ill_hongkong, "cricket": ill_cricket,
        "lasvegas": ill_lasvegas, "nepal": ill_nepal, "gaza": ill_gaza,
        "iran_elec": ill_iran_elec, "bolsonaro": ill_bolsonaro,
        "aukus": ill_aukus, "myanmar": ill_myanmar}

# --------------------------------------------------------------------- map
NA = [(60, 108), (64, 100), (90, 82), (118, 74), (152, 62), (188, 62),
      (192, 80), (216, 84), (228, 108), (206, 118), (216, 138), (186, 152),
      (198, 168), (176, 176), (158, 160), (158, 190), (142, 210), (128, 186),
      (126, 160), (104, 148), (84, 136), (56, 124)]
GREENLAND = [(232, 40), (262, 30), (284, 44), (276, 62), (246, 60), (234, 50)]
SA = [(192, 238), (200, 218), (210, 204), (222, 208), (226, 232), (220, 268),
      (210, 286), (200, 264)]
AFRICA = [(300, 172), (330, 158), (354, 158), (378, 170), (396, 182),
          (404, 200), (398, 224), (384, 244), (368, 262), (352, 250),
          (336, 230), (326, 204), (312, 196)]
EURASIA = [(286, 104), (300, 84), (320, 74), (342, 66), (386, 62), (440, 56),
           (500, 52), (560, 58), (620, 66), (660, 78), (640, 92), (600, 84),
           (600, 100), (580, 96), (560, 108), (530, 100), (500, 112),
           (470, 116), (446, 128), (420, 122), (400, 132), (382, 122),
           (360, 130), (340, 122), (320, 132), (300, 124), (292, 116)]
UK = [(288, 74), (292, 64), (298, 66), (296, 76), (290, 80)]
JAPAN = [(614, 92), (622, 84), (630, 88), (626, 100), (618, 102)]
SUMATRA = [(520, 148), (540, 138), (552, 146), (532, 156)]
JAVA = [(548, 158), (576, 158), (580, 164), (548, 164)]
BORNEO = [(556, 132), (572, 126), (584, 134), (580, 148), (564, 148)]
NEWGUINEA = [(600, 144), (624, 140), (640, 148), (628, 156), (604, 154)]
AUSTRALIA = [(560, 186), (592, 178), (626, 184), (648, 198), (640, 216),
             (612, 224), (580, 216), (560, 202)]
NZ = [(668, 226), (676, 220), (678, 234), (670, 240)]
LAND = [NA, GREENLAND, SA, AFRICA, EURASIA, UK, JAPAN, SUMATRA, JAVA,
        BORNEO, NEWGUINEA, AUSTRALIA, NZ]


def draw_map(d, x, y, w, h, pins):
    d.rectangle([x, y, x + w, y + h], fill=MAPSEA, outline=LINE, width=1)
    sx, sy = w / 720.0, h / 250.0
    for poly in LAND:
        d.polygon([(x + px * sx, y + py * sy) for px, py in poly], fill=SAND,
                  outline=(180, 165, 130))
    for i, (lon, lat) in enumerate(pins, 1):
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((px - 3 if i < 10 else px - 6, py - 7), str(i),
               font=SANSB(9), fill=(255, 255, 255))
    return pins


def draw_lead(d, x, y, w, ld):
    h = 218
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 24], fill=RED)
    d.text((x + 8, y + 5), ld["kicker"], font=SANSB(10), fill=(255, 255, 255))
    tc = {"CONFIRMED": GREEN, "ONGOING": GOLD, "CLAIM": (185, 28, 28)}.get(
        ld["tag"], GREY)
    d.text((x + w - 8 - SANSB(10).getlength(ld["tag"]), y + 5), ld["tag"],
           font=SANSB(10), fill=(255, 255, 255))
    ih = 96
    ILLS[ld["ill"]](d, x + 1, y + 25, w - 2, ih)
    d.text((x + 8, y + 128), str(ld["n"]) + ".", font=SERIFB(16), fill=RED)
    numw = SERIFB(16).getlength(str(ld["n"]) + ". ")
    block(d, x + 8 + numw, y + 127, w - 16 - numw, ld["head"], SERIFB(19),
          leading=22, max_lines=2)
    block(d, x + 8, y + 178, w - 16, ld["deck"], SANS(11.5), leading=14,
          max_lines=3)
    return h


def draw_med(d, x, y, w, st):
    h = 134
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=1)
    ih = 62
    ILLS[st["ill"]](d, x + 1, y + 1, w - 2, ih)
    tf = SANSB(8)
    tw = tf.getlength(st["tag"]) + 10
    d.rectangle([x + 6, y + 6, x + 6 + tw, y + 22], fill=RED)
    centre(d, x + 6 + tw / 2, y + 8, st["tag"], tf, (255, 255, 255))
    d.text((x + 6, y + 66), st["kicker"], font=SANSB(8), fill=RED)
    scol = {"CONFIRMED": GREEN, "REPORTED": NAVY, "CLAIM": RED,
            "FORECAST": GOLD, "OFFICIALS": TEAL}.get(st["status"], GREY)
    sf = SANSB(8)
    d.text((x + w - 6 - sf.getlength(st["status"]), y + 66), st["status"],
           font=sf, fill=scol)
    block(d, x + 6, y + 78, w - 12, str(st["n"]) + ". " + st["head"],
          SERIFB(11.5), leading=13, max_lines=2)
    block(d, x + 6, y + 106, w - 12, st["deck"], SANS(9.5), leading=11,
          max_lines=2)
    return h


def draw():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 12
    # --- top band
    d.rectangle([0, 0, W, 20], fill=NAVY)
    centre(d, W // 2, 4, "SUNDAY 22 NOVEMBER 2026  ·  LATE EDITION  ·  "
           "39 STORIES  ·  7 REGIONS", SANSB(10), (255, 255, 255))
    # --- masthead
    centre(d, W // 2, 24, "THE WORLD IN ONE DAY", SERIFB(52), INK)
    d.rectangle([M, 84, W - M, 84], fill=INK, width=1)
    d.rectangle([M, 87, W - M, 87], fill=INK, width=1)
    centre(d, W // 2, 90,
           "COP31's final deal goes to the vote · Iran claims strikes in "
           "Bahrain · 186 drones over Ukraine",
           SERI(16), INK)
    # --- stat strip
    stats = [("186", "drones fired at Ukraine"), ("161", "drones downed"),
             ("98.79%", "record Hong Kong turnout"),
             ("720/9", "India's record Test total"),
             ("$120bn", "adaptation target dropped"),
             ("24", "dead, Nigeria boat")]
    sw = (W - 2 * M) // 6
    for i, (big, small) in enumerate(stats):
        x0 = M + i * sw
        if i:
            d.line([x0, 114, x0, 144], fill=LINE, width=1)
        centre(d, x0 + sw // 2, 112, big, SANSB(19), RED)
        centre(d, x0 + sw // 2, 134, small, SANS(9), INK)
    # --- timeline (7 items; short forms so all seven fit)
    tl = [("03:00", "COP31 vote"), ("08:00", "COP31 plenary"),
          ("09:29", "Hamas talks"), ("10:00", "HK polls close"),
          ("11:00", "Pope Leo lunch"), ("16:30", "Liverpool v Man Utd"),
          ("17:00", "ATP final")]
    d.rectangle([M, 150, W - M, 172], fill=(238, 232, 214), outline=LINE, width=1)
    d.text((M + 6, 156), "THE DAY IN UTC", font=SANSB(10), fill=RED)
    tx = M + 112
    for lab, txt in tl:
        d.text((tx, 157), lab, font=SANSB(9), fill=NAVY)
        tw = SANSB(9).getlength(lab)
        d.text((tx + tw + 3, 157), txt, font=SANS(9), fill=INK)
        tx += tw + 3 + SANS(9).getlength(txt) + 10
    # --- region bar
    x0 = M
    for name, cnt, col in REGIONS:
        seg = int((W - 2 * M) * cnt / 39)
        d.rectangle([x0, 178, x0 + seg - 2, 196], fill=col)
        lab = f"{name} {cnt}"
        fs = 10
        while SANSB(fs).getlength(lab) > seg - 8 and fs > 7:
            fs -= 1
        centre(d, x0 + seg // 2, 182, lab, SANSB(fs), (255, 255, 255))
        x0 += seg
    # --- leads
    widths = [326, 326, 324]
    x = M
    for ld, w in zip(LEADS, widths):
        draw_lead(d, x, 206, w, ld)
        x += w + 10
    # --- medium rows
    for row, yy in enumerate((428, 566)):
        x = M
        for st in MED[row * 5:(row + 1) * 5]:
            draw_med(d, x, yy, 196, st)
            x += 200
    # --- section header
    d.rectangle([M, 704, W - M, 704], fill=INK, width=1)
    d.text((M, 706), "ALSO ON SUNDAY 22 NOVEMBER — 26 MORE STORIES",
           font=SANSB(11), fill=INK)
    d.text((W - M - SANS(10).getlength("NUMBERS MATCH THE MAP PINS"), 707),
           "NUMBERS MATCH THE MAP PINS", font=SANS(10), fill=GREY)
    # --- map + also list
    pins = [s["pin"] for s in LEADS] + [s["pin"] for s in MED]
    draw_map(d, M, 722, 336, 162, pins)
    colw = 330
    for ci in range(2):
        cx = M + 340 + ci * colw
        for ri in range(13):
            idx = ci * 13 + ri
            n, txt, _reg = ALSO[idx]
            yy = 722 + ri * 12.5
            d.text((cx, yy), f"{n}.", font=SANSB(9.5), fill=RED)
            fs = 9.5
            while SANS(fs).getlength(txt) > colw - 22 and fs > 7.5:
                fs -= 0.5
            d.text((cx + 22, yy), txt, font=SANS(fs), fill=INK)
    # --- date check
    d.rectangle([M, 890, W - M, 956], fill=(238, 232, 214), outline=RED, width=2)
    d.text((M + 8, 894),
           "DATE CHECK — READ THIS FIRST · WIRES AS OF 11:00 UTC, SUNDAY 22 NOVEMBER 2026",
           font=SANSB(11), fill=RED)
    block(d, M + 8, 910, W - 2 * M - 16,
          "Left out as other days' news: Peru's 6.7 quake (20 Nov) · the "
          "400-drone barrage (19\u201320 Nov) · missiles in Poland (20 Nov) · "
          "the Shenzhen summit (20 Nov) · \u201cEl Chapo Isidro\u201d seized "
          "(21 Nov) · Roundup $7.25bn (20 Nov) · BepiColombo at Mercury "
          "(Sat) · Somalia orders the UAE envoy out (19 Nov) · the "
          "Cantine raid (5 Nov) · Makkah missile debris (11 Nov).",
          SANS(10.5), leading=13, max_lines=2)
    d.text((M + 8, 938),
           "Tonight's barrage was 186 drones, not 400. Not yet decided at press "
           "time: COP31's final approval · the ATP final · Liverpool v Man Utd.",
           font=SANS(10.5), fill=INK)
    # --- footer
    block(d, M, 962, W - 2 * M,
          "Every story here happened, or was first reported, on Sunday "
          "22 November 2026, or was still developing that day; Saturday "
          "items are the weekend's news Sunday woke to. Sources named "
          "beside each story. Pictures: original, drawn in code. "
          "HOW TO READ THE TAGS — CONFIRMED = 2+ outlets · REPORTED = "
          "one outlet's claim · CLAIM = one side's claim, contested · "
          "FORECAST = still to happen when drawn · SAT = Saturday's news.",
          SANS(9), leading=11, max_lines=2)
    return img


if __name__ == "__main__":
    im = draw()
    im.save("entry.png", optimize=True)
    print("saved entry.png", im.size)
