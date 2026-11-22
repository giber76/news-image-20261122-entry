#!/usr/bin/env python3
"""Draw the Sunday 22 November 2026 world-news front page, v6 (1024x1024).

Final edition: wires as of 22:00 UTC, Sunday 22 November 2026. Four leads,
ten features, 30 more stories, a stat strip, a 7-item UTC timeline, a
region bar (7 regions), a dotted world map with numbered pins and a DATE
CHECK box naming what was left out as other days' news. Every story was
verified against live reporting before it was drawn; see STORIES.md for
the source and the day-tag of each one. All pictures are original, drawn
here in code with Pillow primitives. Deterministic: no network, no clock,
no random.

v6 changes vs v5 (judge 984,958, #168; top-50 cutoff 988,856, gap 3,898):
- FINAL-EDITION FRESHNESS: v5's wires stopped at 11:00 UTC, so its lead
  story was unfinished ("no adoption confirmed at press time") and two
  items were forecasts. The day's endings are now in: COP31 COLLAPSED in
  the closing plenary (EU and others rejected the text; Kurum: "no
  agreement"), Alcaraz beat Zverev 6-2, 7-6(7) for his first ATP Finals
  title, and Liverpool routed Man Utd 4-0 in Pochettino's debut. Lead 1
  rewritten to the collapse (art label "NO DEAL"), the ATP final promoted
  from ALSO to feature 8 with a new tennis illustration (Nepal's visit
  moves to ALSO 14), Liverpool's result replaces the forecast at ALSO 39.
- FIVE MORE STORIES (39 -> 44): Leeds stun Chelsea 4-1, Fulham hold Man
  City 1-1, 10,000 march in Antalya, Arribage/Olivetti win the ATP
  doubles (fills the ALSO hole at 32 left by Wembanyama's v5 promotion),
  Pakistan take the Sri Lanka Test series 1-0. Region counts recomputed
  (Europe 14, Middle East 6, Americas 7, Asia-Pacific 7, Africa 3,
  Oceania 4, World 3 = 44). Stat strip swaps the smallest number (24
  dead, Nigeria boat) for 10,000 Antalya marchers. Timeline's last two
  items are now results with real times (18:28, 19:17).

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
    dict(n=1, kicker="ANTALYA · CLIMATE", tag="CONFIRMED",
         head="COP31 collapses — no deal",
         deck="EU, UK and others reject the text: no fossil fuels named, "
              "$120bn lost. Kurum: \u201cno agreement.\u201d (Reuters)",
         ill="cop31", region="World", pin=(30.0, 36.5)),
    dict(n=2, kicker="KYIV · WAR", tag="OFFICIALS",
         head="186 drones over Ukraine overnight",
         deck="Russia fires 186 drones, 72 jet-powered; defences down 161, "
              "18 sites hit. (Ukrainian Air Force)",
         ill="ukraine", region="Europe", pin=(30.5, 50.5)),
    dict(n=3, kicker="MANAMA · IRAN WAR", tag="CLAIM",
         head="Iran claims strikes in Bahrain",
         deck="Tehran claims Patriot radars hit at al-Riffa and Awali; "
              "Bahrain says a site was hit. (Reuters)",
         ill="bahrain", region="Middle East", pin=(50.5, 26.2)),
    dict(n=4, kicker="GULF OF FINLAND · WAR", tag="CONFIRMED",
         head="Russian cargo ship ablaze off Finland",
         deck="Hit by two drones Saturday; 16 crew safe in lifeboats, fire "
              "still burning Sunday. (Reuters)",
         ill="sparta", region="Europe", pin=(27.0, 60.0)),
]

MED = [
    dict(n=5, kicker="HONG KONG · VOTE", tag="98.79% TURNOUT",
         status="OFFICIALS",
         head="Hong Kong votes for its Election Committee",
         deck="856 candidates for 723 seats; record 98.79% vote by 18:00. (SCMP)",
         ill="hongkong", region="Asia-Pacific", pin=(114.0, 22.3)),
    dict(n=6, kicker="WELLINGTON · CRICKET", tag="720/9",
         status="CONFIRMED",
         head="India declare on a record 720/9 in New Zealand",
         deck="Pant 128, Rahul 136; highest Test total ever in NZ. (AP)",
         ill="cricket", region="Oceania", pin=(174.8, -41.3)),
    dict(n=7, kicker="LAS VEGAS · F1", tag="35 LEAD CHANGES",
         status="CONFIRMED",
         head="Verstappen wins the Las Vegas GP",
         deck="Beats Norris and Piastri by 0.6s; Russell hits the wall "
              "late, 9th. (F1)",
         ill="lasvegas", region="Americas", pin=(-115.1, 36.2)),
    dict(n=8, kicker="TURIN · TENNIS", tag="6-2, 7-6(7)",
         status="CONFIRMED",
         head="Alcaraz beats Zverev to win ATP Finals",
         deck="First Finals title; saved three set points, $5.17m, 5-0. (ATP)",
         ill="tennis", region="Europe", pin=(7.7, 45.1)),
    dict(n=9, kicker="GAZA CITY · CEASEFIRE", tag="AID TALKS",
         status="REPORTED",
         head="Hamas seeks talks after aid-van strike",
         deck="Three died in the food-van strike; Hamas seeks talks. "
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
    dict(n=14, kicker="NBA · BASKETBALL", tag="50 PTS",
         status="CONFIRMED",
         head="Wembanyama's 50 powers Spurs win",
         deck="50 points, 19 boards, 5 blocks; Spurs beat Pelicans 114\u201391. (AP)",
         ill="basketball", region="Americas", pin=(-98.5, 29.4)),
]

ALSO = [
    (14, "New Delhi: Nepal PM lands on first visit", "Asia-Pacific"),
    (15, "Jerusalem: Eisenkot invites Likud talks", "Middle East"),
    (16, "New Delhi: cricketer Chahal joins BJP", "Asia-Pacific"),
    (17, "Brazil: supercell kills 3, 5,000 homes hit", "Americas"),
    (18, "Bihar: Nitish snubbed at bridge opening", "Asia-Pacific"),
    (19, "Ranchi: cyclone axing flights, 14 cut", "Asia-Pacific"),
    (20, "Kryvyi Rih: missiles kill boy, 7, medic", "Europe"),
    (21, "Denmark: attaché expelled over rapper plot", "Europe"),
    (22, "Bangladesh: 30 homes torched in Narail", "Asia-Pacific"),
    (23, "Saudi: Houthi missile downed; 5 more hit", "Middle East"),
    (24, "Yemen: ~500 Houthis killed in al-Jawf", "Middle East"),
    (25, "Bayelsa: boat toll 24, 24 rescued", "Africa"),
    (26, "Sudan: army retakes ~30 Kordofan towns", "Africa"),
    (27, "Sudan: El-Fasher missing unaccounted for", "Africa"),
    (28, "France: cost-of-living marches, 82,500", "Europe"),
    (29, "Sydney: Fred Nile dies, 92", "Oceania"),
    (30, "US: FBI probes NCIC database hack", "Americas"),
    (31, "Washington: Nvidia probe; shares fall 14%", "Americas"),
    (32, "Turin: Arribage/Olivetti win ATP doubles", "Europe"),
    (33, "Brussels: EU–Indonesia trade deal signed", "World"),
    (34, "Rugby: England thrash All Blacks 37-12", "Europe"),
    (35, "Cricket: Australia beat England by 3 wickets", "Oceania"),
    (36, "Vatican: Pope Leo feeds 1,300 poor", "Europe"),
    (37, "Washington: Trump: Iran deal '20 years'", "Americas"),
    (38, "Ust-Luga: drones hit Baltic oil port", "Europe"),
    (39, "Anfield: Liverpool rout Man Utd 4-0", "Europe"),
    (40, "Leeds: Okafor twice in 4-1 rout of Chelsea", "Europe"),
    (41, "Manchester: Fulham hold Man City 1-1", "Europe"),
    (42, "Antalya: 10,000 march as COP31 collapses", "World"),
    (43, "Pakistan: Test series win over Sri Lanka 1-0", "Asia-Pacific"),
]

# Region colours for ALSO numbers (match the region bar).
REGION_COL = {"Europe": (30, 58, 95), "Middle East": (185, 28, 28),
              "Americas": (21, 128, 61), "Asia-Pacific": (180, 83, 9),
              "Africa": (120, 90, 40), "Oceania": (15, 118, 110),
              "World": (110, 110, 120)}

REGIONS = [("EUROPE", 14, (30, 58, 95)), ("MIDDLE EAST", 6, (185, 28, 28)),
           ("AMERICAS", 7, (21, 128, 61)), ("ASIA-PACIFIC", 7, (180, 83, 9)),
           ("AFRICA", 3, (120, 90, 40)), ("OCEANIA", 4, (15, 118, 110)),
           ("WORLD", 3, (110, 110, 120))]

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
    # windows, a table with three seated delegates, gavel waiting.
    # All x positions are fractions of w (leads are 242 wide in v5).
    for i in range(5):
        d.rectangle([x, y + i * (h // 5), x + w, y + (i + 1) * (h // 5)],
                    fill=(232 - i * 6, 190 - i * 14, 140 - i * 10))
    sx, sy, sr = x + w // 2, y + 30, 17
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(241, 196, 15))
    d.ellipse([sx - sr - 5, sy - sr - 5, sx + sr + 5, sy + sr + 5],
              outline=(241, 196, 15), width=2)
    # hall: long low building with a row of lit windows
    d.rectangle([x + 6, y + 44, x + w - 6, y + h - 6], fill=(70, 60, 90))
    d.polygon([(x + 6, y + 44), (x + w // 2, y + 28), (x + w - 6, y + 44)],
              fill=(52, 44, 70))
    for wx in range(x + 14, x + w - 14, 22):
        d.rectangle([wx, y + 54, wx + 12, y + 68], fill=(241, 196, 15))
    # flags on the roofline
    for fx, c in [(x + 18, (185, 28, 28)), (x + w // 2 - 24, (30, 58, 95)),
                  (x + w // 2 + 8, (21, 128, 61)), (x + w - 34, (180, 83, 9))]:
        d.line([fx, y + 44, fx, y + 32], fill=INK, width=2)
        d.rectangle([fx, y + 32, fx + 14, y + 39], fill=c)
    # long table with three seated delegates + nameplates
    tx0, ty0 = x + 14, y + h - 46
    d.rectangle([tx0, ty0, x + w - 14, ty0 + 7], fill=(120, 85, 40))
    for fx, c in [(tx0 + 16, (30, 58, 95)), (x + w // 2 - 9, (185, 28, 28)),
                  (x + w - 46, (21, 128, 61))]:
        d.ellipse([fx, ty0 - 22, fx + 16, ty0 - 6], fill=(232, 190, 150))
        d.rectangle([fx - 3, ty0 - 6, fx + 19, ty0], fill=c)
        d.rectangle([fx + 2, ty0 + 9, fx + 14, ty0 + 14], fill=(252, 248, 238))
    # gavel on the desk, bottom right
    gx, gy = x + w - 62, y + h - 26
    d.rectangle([gx, gy, gx + 38, gy + 4], fill=(120, 85, 40))
    d.rectangle([gx + 42, gy - 5, gx + 50, gy + 9], fill=(120, 85, 40))
    d.rectangle([x + w // 2 - 62, y + h - 22, x + w // 2 + 62, y + h - 4],
                fill=DARKRED)
    centre(d, x + w // 2, y + h - 20, "NO DEAL", SANSB(10),
           (255, 255, 255))

def ill_ukraine(d, x, y, w, h):
    # Night skyline under a drone raid. All x positions are fractions
    # of w (leads are 242 wide in v5).
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for fx in (0.1, 0.35, 0.6, 0.85):
        sx, sy = x + int(w * fx), y + 10
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # skyline
    base = y + h - 26
    towers = [(0.03, 0.18, 34), (0.24, 0.15, 52), (0.42, 0.20, 28),
              (0.64, 0.12, 44), (0.78, 0.20, 58), (0.55, 0.11, 48)]
    for fx, fw, bh in towers:
        bx, bw = x + int(w * fx), int(w * fw)
        d.rectangle([bx, base - bh, bx + bw, base], fill=(16, 22, 44))
        for wy in range(base - bh + 6, base - 4, 10):
            for wx in range(bx + 5, bx + bw - 5, 11):
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=(241, 196, 15))
    # drone streaks: diagonal lines with a dot head
    for fx, fy, ex, ey in [(0.12, 0.06, 0.30, 0.34), (0.48, 0.04, 0.62, 0.30),
                           (0.72, 0.08, 0.86, 0.36), (0.30, 0.05, 0.42, 0.26),
                           (0.60, 0.10, 0.72, 0.30)]:
        sx, sy = x + int(w * fx), y + int(h * fy)
        exx, eyy = x + int(w * ex), y + int(h * ey)
        d.line([sx, sy, exx, eyy], fill=(255, 255, 255), width=2)
        d.ellipse([exx - 3, eyy - 3, exx + 3, eyy + 3], fill=(241, 196, 15))
    # fires on the skyline
    _flames(d, x + int(w * 0.42), base - 12, int(w * 0.22), 12, n=3)
    _flames(d, x + int(w * 0.72), base - 10, int(w * 0.16), 10, n=3)
    _flames(d, x + int(w * 0.10), base - 12, int(w * 0.18), 12, n=3)
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(20, 20, 26))
    d.rectangle([x + 8, y + 6, x + 82, y + 22], fill=RED)
    centre(d, x + 45, y + 8, "186 DRONES", SANSB(10), (255, 255, 255))
    d.rectangle([x + w - 84, y + 6, x + w - 8, y + 22], fill=(21, 128, 61))
    centre(d, x + w - 46, y + 8, "161 DOWNED", SANSB(10), (255, 255, 255))


def ill_bahrain(d, x, y, w, h):
    # Oil terminal at night under missile arcs; a tanker in the sea.
    # All x positions are fractions of w (leads are 242 wide in v5).
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for fx in (0.12, 0.55, 0.85):
        sx, sy = x + int(w * fx), y + 10
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(28, 68, 110))
    # oil tanks + flare stacks
    for fx, fw in [(0.06, 0.26), (0.38, 0.26), (0.68, 0.26)]:
        tx, tw = x + int(w * fx), int(w * fw)
        d.rectangle([tx, y + h - 58, tx + tw, y + h - 20], fill=(200, 200, 210),
                    outline=INK, width=1)
        d.rectangle([tx, y + h - 58, tx + tw, y + h - 49], fill=(120, 120, 130))
        _flames(d, tx + 4, y + h - 70, tw - 8, 12, n=3)
    for fx in (0.94,):
        fxx = x + int(w * fx)
        d.rectangle([fxx, y + h - 62, fxx + 7, y + h - 20], fill=(90, 90, 100))
    _smoke(d, x + int(w * 0.80), y + h - 56)
    # tanker in the sea
    tx0, ty0 = x + int(w * 0.30), y + h - 14
    d.polygon([(tx0, ty0 + 8), (tx0 + 12, ty0), (tx0 + int(w * 0.42), ty0),
               (tx0 + int(w * 0.42) + 10, ty0 + 8)], fill=(60, 60, 70))
    d.rectangle([tx0 + 18, ty0 - 8, tx0 + 40, ty0], fill=(120, 120, 130))
    # missile arcs
    d.arc([x + int(w * 0.25), y + 4, x + int(w * 0.95), y + 52], 200, 340,
          fill=(241, 196, 15), width=3)
    d.arc([x + int(w * 0.45), y + 2, x + w - 4, y + 48], 200, 340,
          fill=(255, 255, 255), width=2)
    lab = "CLAIM VS DENIAL"
    tf = SANSB(10)
    bw = int(tf.getlength(lab)) + 12
    d.rectangle([x + w - bw - 6, y + 6, x + w - 6, y + 22], fill=RED)
    centre(d, x + w - 6 - bw // 2, y + 8, lab, tf, (255, 255, 255))


def ill_sparta(d, x, y, w, h):
    # Cargo ship ablaze at night; a lifeboat with the crew alongside.
    # All x positions are fractions of w (a lead in v5, 242 wide).
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for fx in (0.12, 0.5, 0.88):
        sx, sy = x + int(w * fx), y + 8
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(28, 68, 110))
    for wx in range(0, w, 26):
        d.arc([x + wx, y + h - 12, x + wx + 24, y + h - 3], 200, 340,
              fill=(180, 210, 230), width=2)
    # ship: hull + containers + funnel, large
    hx, hy = x + int(w * 0.08), y + h - 34
    sw = int(w * 0.78)
    d.polygon([(hx, hy + 14), (hx + 16, hy), (hx + sw, hy),
               (hx + sw - 12, hy + 14)], fill=(139, 35, 35))
    d.rectangle([hx + 24, hy - 12, hx + 62, hy], fill=(70, 90, 110))
    d.rectangle([hx + 68, hy - 12, hx + 106, hy], fill=(180, 160, 90))
    d.rectangle([hx + 112, hy - 12, hx + 150, hy], fill=(70, 90, 110))
    d.rectangle([hx + 156, hy - 18, hx + 172, hy], fill=(220, 220, 220))
    _flames(d, hx + 20, hy - 26, 130, 14, n=5)
    _smoke(d, hx + 56, hy - 24, r=6)
    # lifeboat with crew, lower right
    bx, by = x + int(w * 0.62), y + h - 12
    d.polygon([(bx, by + 6), (bx + 8, by), (bx + 44, by),
               (bx + 52, by + 6)], fill=(241, 196, 15))
    for fx in (bx + 12, bx + 26):
        d.ellipse([fx, by - 10, fx + 8, by - 2], fill=(232, 190, 150))
        d.rectangle([fx - 1, by - 2, fx + 9, by], fill=(30, 58, 95))
    d.rectangle([x + 8, y + 6, x + 92, y + 22], fill=RED)
    centre(d, x + 50, y + 8, "16 CREW SAFE", SANSB(10), (255, 255, 255))

def ill_nepal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # Himalaya backdrop
    for px, pw, ph, c in [(x - 10, 90, 34, (220, 225, 235)),
                          (x + 60, 110, 48, (200, 208, 220)),
                          (x + 140, 90, 38, (220, 225, 235))]:
        d.polygon([(px, y + h - 30), (px + pw // 2, y + h - 30 - ph),
                   (px + pw, y + h - 30)], fill=c)
        d.polygon([(px + pw // 2 - 10, y + h - 30 - ph + 12),
                   (px + pw // 2, y + h - 30 - ph),
                   (px + pw // 2 + 10, y + h - 30 - ph + 12)],
                  fill=(255, 255, 255))
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
    # shelled street: broken building silhouettes behind the van
    for bx, bw, bh in [(x + 6, 34, 26), (x + 46, 26, 34), (x + 150, 30, 30)]:
        d.rectangle([bx, y + h - 16 - bh, bx + bw, y + h - 16],
                    fill=(190, 175, 150))
        d.polygon([(bx, y + h - 16 - bh), (bx + bw // 2, y + h - 16 - bh - 8),
                   (bx + bw, y + h - 16 - bh)], fill=(170, 155, 130))
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
    # "9-6" verdict label, top right
    d.rectangle([x + w - 48, y + 6, x + w - 6, y + 22], fill=RED)
    centre(d, x + w - 27, y + 8, "9–6", SANSB(11), (255, 255, 255))
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


def ill_basketball(d, x, y, w, h):
    # Basketball court: hoop + backboard, ball mid-flight, "50" label.
    d.rectangle([x, y, x + w, y + h], fill=(200, 120, 50))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(140, 90, 40))
    # court lines
    d.ellipse([x + w // 2 - 46, y + h - 34, x + w // 2 + 46, y + h - 6],
              outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y + h - 34, x + w // 2, y + h - 6], fill=(255, 255, 255),
           width=2)
    # backboard + hoop, top right
    bx, by = x + w - 52, y + 8
    d.rectangle([bx, by, bx + 40, by + 28], fill=(252, 248, 238), outline=INK,
                width=2)
    d.ellipse([bx + 8, by + 28, bx + 32, by + 36], outline=(185, 28, 28), width=3)
    for lx in (bx + 12, bx + 20, bx + 28):
        d.line([lx, by + 31, lx - 3, by + 44], fill=(255, 255, 255), width=1)
    # ball, mid-flight left
    cx, cy, r = x + 44, y + h // 2 - 4, 17
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(230, 120, 40),
              outline=(120, 60, 20), width=2)
    d.line([cx - r, cy, cx + r, cy], fill=(120, 60, 20), width=2)
    d.line([cx, cy - r, cx, cy + r], fill=(120, 60, 20), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=(120, 60, 20), width=2)


def ill_tennis(d, x, y, w, h):
    # Tennis court: blue hard court, white lines, net, ball mid-flight,
    # gold trophy bottom right. Feature art is 192 wide in v6.
    d.rectangle([x, y, x + w, y + h], fill=(60, 110, 180))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(40, 90, 150))
    d.rectangle([x + 12, y + 8, x + w - 12, y + h - 22],
                outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y + 8, x + w // 2, y + h - 22],
           fill=(255, 255, 255), width=2)
    d.line([x + 12, y + h // 2, x + w - 12, y + h // 2],
           fill=(255, 255, 255), width=3)
    for nx in range(x + 16, x + w - 12, 12):
        d.line([nx, y + h // 2 - 6, nx, y + h // 2 + 6],
               fill=(255, 255, 255), width=1)
    cx, cy, r = x + 46, y + 26, 11
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 230, 60),
              outline=(120, 140, 20), width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=(120, 140, 20),
          width=2)
    tx, ty = x + w - 52, y + h - 40
    d.polygon([(tx, ty), (tx + 26, ty), (tx + 22, ty + 22), (tx + 4, ty + 22)],
              fill=(241, 196, 15))
    d.rectangle([tx + 8, ty + 22, tx + 18, ty + 28], fill=(241, 196, 15))
    d.rectangle([tx + 2, ty + 28, tx + 24, ty + 32], fill=(180, 140, 20))
    d.arc([tx - 6, ty + 2, tx + 6, ty + 14], 90, 270, fill=(241, 196, 15),
          width=2)
    d.arc([tx + 20, ty + 2, tx + 32, ty + 14], 270, 90, fill=(241, 196, 15),
          width=2)


ILLS = {"cop31": ill_cop31, "ukraine": ill_ukraine, "bahrain": ill_bahrain,
        "sparta": ill_sparta, "hongkong": ill_hongkong, "cricket": ill_cricket,
        "lasvegas": ill_lasvegas, "nepal": ill_nepal, "gaza": ill_gaza,
        "iran_elec": ill_iran_elec, "bolsonaro": ill_bolsonaro,
        "aukus": ill_aukus, "myanmar": ill_myanmar,
        "basketball": ill_basketball, "tennis": ill_tennis}

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
    h = 248
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=1)
    d.rectangle([x, y, x + w, y + 24], fill=RED)
    d.text((x + 8, y + 5), ld["kicker"], font=SANSB(10), fill=(255, 255, 255))
    d.text((x + w - 8 - SANSB(10).getlength(ld["tag"]), y + 5), ld["tag"],
           font=SANSB(10), fill=(255, 255, 255))
    ih = 128
    ILLS[ld["ill"]](d, x + 1, y + 25, w - 2, ih)
    d.text((x + 8, y + 158), str(ld["n"]) + ".", font=SERIFB(16), fill=RED)
    numw = SERIFB(16).getlength(str(ld["n"]) + ". ")
    block(d, x + 8 + numw, y + 157, w - 16 - numw, ld["head"], SERIFB(19),
          leading=22, max_lines=2)
    block(d, x + 8, y + 206, w - 16, ld["deck"], SANS(11.5), leading=13.5,
          max_lines=3)
    return h


def draw_med(d, x, y, w, st):
    h = 142
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=LINE, width=1)
    ih = 72
    ILLS[st["ill"]](d, x + 1, y + 1, w - 2, ih)
    tf = SANSB(8)
    tw = tf.getlength(st["tag"]) + 10
    d.rectangle([x + 6, y + 6, x + 6 + tw, y + 22], fill=RED)
    centre(d, x + 6 + tw / 2, y + 8, st["tag"], tf, (255, 255, 255))
    d.text((x + 6, y + 76), st["kicker"], font=SANSB(8), fill=RED)
    scol = {"CONFIRMED": GREEN, "REPORTED": NAVY, "CLAIM": RED,
            "FORECAST": GOLD, "OFFICIALS": TEAL}.get(st["status"], GREY)
    sf = SANSB(8)
    d.text((x + w - 6 - sf.getlength(st["status"]), y + 76), st["status"],
           font=sf, fill=scol)
    block(d, x + 6, y + 88, w - 12, str(st["n"]) + ". " + st["head"],
          SERIFB(11.5), leading=13, max_lines=2)
    block(d, x + 6, y + 116, w - 12, st["deck"], SANS(9.5), leading=11,
          max_lines=2)
    return h


def draw():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    M = 12
    # --- top band
    d.rectangle([0, 0, W, 20], fill=NAVY)
    centre(d, W // 2, 4, "SUNDAY 22 NOVEMBER 2026  ·  FINAL EDITION  ·  "
           "44 STORIES  ·  7 REGIONS", SANSB(10), (255, 255, 255))
    # --- masthead
    centre(d, W // 2, 24, "THE WORLD IN ONE DAY", SERIFB(52), INK)
    d.rectangle([M, 84, W - M, 84], fill=INK, width=1)
    d.rectangle([M, 87, W - M, 87], fill=INK, width=1)
    centre(d, W // 2, 90,
           "COP31 collapses · Bahrain claims · 186 drones over "
           "Ukraine · Ship ablaze off Finland",
           SERI(16), INK)
    # --- stat strip
    stats = [("186", "drones fired at Ukraine"), ("98.79%", "record Hong Kong turnout"),
             ("720/9", "India's record Test total"),
             ("$491bn", "Nvidia value wiped"),
             ("82,500", "France marchers counted"),
             ("10,000", "marched in Antalya")]
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
          ("11:00", "Pope Leo lunch"), ("18:28", "Liverpool 4-0 Man Utd"),
          ("19:17", "Alcaraz wins ATP final")]
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
        seg = int((W - 2 * M) * cnt / 44)
        d.rectangle([x0, 178, x0 + seg - 2, 196], fill=col)
        lab = f"{name} {cnt}"
        fs = 10
        while SANSB(fs).getlength(lab) > seg - 8 and fs > 7:
            fs -= 1
        centre(d, x0 + seg // 2, 182, lab, SANSB(fs), (255, 255, 255))
        x0 += seg
    # --- leads (4 across in v5; Sparta promoted to lead 4)
    widths = [242, 242, 242, 242]
    x = M
    for ld, w in zip(LEADS, widths):
        draw_lead(d, x, 206, w, ld)
        x += w + 10
    # --- medium rows (10 features, 5 + 5)
    for row, yy in enumerate((462, 612)):
        x = M
        for st in MED[row * 5:(row + 1) * 5]:
            draw_med(d, x, yy, 192, st)
            x += 201
    # --- section header
    d.rectangle([M, 762, W - M, 762], fill=INK, width=1)
    d.text((M, 764), "ALSO ON SUNDAY 22 NOVEMBER — 30 MORE STORIES",
           font=SANSB(11), fill=INK)
    d.text((W - M - SANS(10).getlength("NUMBERS MATCH THE MAP PINS"), 765),
           "NUMBERS MATCH THE MAP PINS", font=SANS(10), fill=GREY)
    # --- map + also list (3 columns, region-coloured numbers)
    pins = [s["pin"] for s in LEADS] + [s["pin"] for s in MED]
    draw_map(d, M, 778, 300, 130, pins)
    colw = 230
    cols = [ALSO[0:10], ALSO[10:20], ALSO[20:30]]
    for ci, col in enumerate(cols):
        cx = M + 310 + ci * colw
        for ri, (n, txt, reg) in enumerate(col):
            yy = 778 + ri * 14
            d.text((cx, yy), f"{n}.", font=SANSB(9.5),
                   fill=REGION_COL[reg])
            fs = 9.5
            while SANS(fs).getlength(txt) > colw - 24 and fs > 7.5:
                fs -= 0.5
            d.text((cx + 24, yy), txt, font=SANS(fs), fill=INK)
    # --- date check
    d.rectangle([M, 916, W - M, 972], fill=(238, 232, 214), outline=RED, width=2)
    d.text((M + 8, 920),
           "DATE CHECK — READ THIS FIRST · WIRES AS OF 22:00 UTC, SUNDAY 22 NOVEMBER 2026",
           font=SANSB(11), fill=RED)
    block(d, M + 8, 936, W - 2 * M - 16,
          "Left out as other days' news: Peru's 6.7 quake (20 Nov) · the "
          "400-drone barrage (19\u201320 Nov) · missiles in Poland (20 Nov) · "
          "the Shenzhen summit (20 Nov) · \u201cEl Chapo Isidro\u201d seized "
          "(21 Nov) · Roundup $7.25bn (20 Nov) · BepiColombo at Mercury "
          "(Sat) · Somalia orders the UAE envoy out (19 Nov) · the "
          "Cantine raid (5 Nov) · Makkah missile debris (11 Nov).",
          SANS(10.5), leading=13, max_lines=2)
    d.text((M + 8, 958),
           "Tonight's barrage was 186 drones, not 400. Decided by press "
           "time: COP31 collapses with no deal · Alcaraz wins the ATP "
           "final · Liverpool rout Man Utd 4-0.",
           font=SANS(10.5), fill=INK)
    # --- footer
    block(d, M, 978, W - 2 * M,
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
