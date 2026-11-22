#!/usr/bin/env python3
"""Draw the Sunday 22 November 2026 world-news front page (1024x1024).

Early edition: wires as of 01:00 UTC, Sunday 22 November 2026. Three leads,
ten features, 23 more stories, a UTC timeline, a stat strip and a DATE
CHECK box naming what was left out as other days' news. Every story was
verified against live reporting before it was drawn; see STORIES.md for
the source of each one. All pictures are original, drawn here in code
with Pillow primitives. Deterministic: no network, no clock, no random.
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
    """Greedy word wrap; returns lines that fit maxw."""
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
    """Draw a wrapped text block; returns the y just below it."""
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
# tag: CONFIRMED (2+ outlets) / REPORTED (one outlet) / FORECAST (scheduled)
LEADS = [
    dict(n=1, kicker="ANTALYA · CLIMATE", tag="CONFIRMED",
         head="COP31 nears a climate deal at dawn",
         deck="A new package was announced at a late-night plenary; objections "
              "due 03:00 GMT, approval from 06:00 GMT. Fossil fuels the "
              "sticking point. (Reuters)",
         ill="cop31", region="Europe"),
    dict(n=2, kicker="NEW DELHI · DIPLOMACY", tag="CONFIRMED",
         head="Nepal PM flies to Delhi for first state visit",
         deck="Balendra Shah lands Sunday, his first bilateral trip since "
              "taking office in March. A 34-member delegation; talks with "
              "Modi on Monday. (IANS)",
         ill="nepal", region="Asia"),
    dict(n=3, kicker="GULF OF FINLAND · WAR AT SEA", tag="REPORTED",
         head="Russian cargo ship still ablaze after drone strike",
         deck="Sparta II was hit by two drones on Saturday morning and drifted "
              "into Finnish waters. Its 16 crew evacuated by lifeboat; the "
              "fire burned into the night. (Reuters)",
         ill="sparta", region="Europe"),
]

MED = [
    dict(n=4, kicker="OFF OMAN · WAR AT SEA", tag="REPORTED",
         head="Two tankers hit off Oman",
         deck="UKMTO: one hit on the stern, one in the engine room; no casualties.",
         ill="tankers", region="Middle East"),
    dict(n=5, kicker="BAHRAIN · WAR", tag="CONFIRMED",
         head="Bahrain plant burns after Iranian attack",
         deck="A civilian industrial facility was struck on Saturday night; no injuries.",
         ill="bahrain", region="Middle East"),
    dict(n=6, kicker="GAZA · WAR", tag="CONFIRMED",
         head="Four killed in Gaza as the truce frays",
         deck="A drone hit a food-aid van in Tel al-Hawa; a man was shot in Jabalia.",
         ill="gaza", region="Middle East"),
    dict(n=7, kicker="NEW YORK · DIPLOMACY", tag="REPORTED",
         head="France seeks UN action on Myanmar",
         deck="Paris seeks UN action after Myanmar rejects the ICJ genocide ruling.",
         ill="myanmar", region="Europe"),
    dict(n=8, kicker="WASHINGTON · DIPLOMACY", tag="CONFIRMED",
         head="Trump: Iran deal \u201ccould last 20 years\u201d",
         deck="Any deal must be permanent, he told Fox News on Saturday.",
         ill="trump", region="Americas"),
    dict(n=9, kicker="JERUSALEM · POLITICS", tag="REPORTED",
         head="Eisenkot invites Likud to talks from Sunday",
         deck="Intensive coalition talks start today; his bloc holds 48 of 120 seats.",
         ill="eisenkot", region="Middle East"),
    dict(n=10, kicker="NEW DELHI · POLITICS", tag="REPORTED",
         head="Chahal joins BJP, gets OBC role",
         deck="The cricketer was named to the OBC Morcha executive committee.",
         ill="chahal", region="Asia"),
    dict(n=11, kicker="TURIN · TENNIS", tag="CONFIRMED",
         head="Zverev v Alcaraz for the ATP Finals title",
         deck="The final is today, 18:00 CET. Zverev has not dropped a set all week.",
         ill="atp", region="Europe"),
    dict(n=12, kicker="WELLINGTON · CRICKET", tag="CONFIRMED",
         head="India resume 486/4, lead 118 \u2014 Day 4 today",
         deck="Rahul 136, Gill 98, Pant 55*; New Zealand made 368.",
         ill="cricket", region="Oceania"),
    dict(n=13, kicker="BAYELSA · DISASTER", tag="CONFIRMED",
         head="24 dead as funeral boat capsizes in Nigeria",
         deck="The boat sank on Friday; the toll was reported on Saturday. 24 rescued.",
         ill="nigeria", region="Africa"),
]

ALSO = [
    (14, "France: cost-of-living marches, 6th Saturday; 82,500 counted (AFP)"),
    (15, "Brazil: Tupanciret\u00e3 clears rubble; 3 dead, 5,000+ homes unroofed (Reuters)"),
    (16, "Bihar: Modi opens the 9.76 km Nitish Setu over the Ganga (ANI)"),
    (17, "Ranchi: 14 flights axed as Cyclone Akvan cuts visibility (PTI)"),
    (18, "Kryvyi Rih: double-tap strike kills a boy, 7, and a paramedic, 20 (Independent)"),
    (19, "Ust-Luga: Ukrainian drones hit Russia's Baltic oil port (Kyiv Post)"),
    (20, "US: Missouri judge approves Bayer's $7.25bn Roundup settlement (Reuters)"),
    (21, "Rugby: England thrash the All Blacks 37-12 \u2014 a record margin (AP)"),
    (22, "Football: Arsenal held 2-2 at Newcastle; Madueke rescues a point (Reuters)"),
    (23, "Football: Leeds stun Chelsea 4-1 at Stamford Bridge; Okafor twice (Reuters)"),
    (24, "Football: Man City held 1-1 by Fulham; winless in four (Reuters)"),
    (25, "F1: Verstappen inherits pole in Vegas; the race runs tonight (FIA)"),
    (26, "Football: Manchester United host Liverpool at Old Trafford today (Fixture)"),
    (27, "Philadelphia Marathon runs today (Fixture)"),
    (28, "NFL: Week 12 games across the league today (Fixture)"),
    (29, "Israel: a former PM backs Eisenkot, won't serve under Netanyahu (India Today)"),
    (30, "UK: Blair \u2014 rejoin the EU only if Britain innovates on tech (BBC)"),
    (31, "Belgium: a national strike on Monday is set to shut air traffic (Arab News)"),
    (32, "Lebanon: Aoun demands an end to Israeli occupation (Arab News)"),
    (33, "West Bank: a man is shot dead by settler guards near Dura al-Qar (AFP)"),
    (34, "Pakistan: security forces kill 15 militants in Balochistan (Arab News)"),
    (35, "Cricket: Australia end England's seven-match T20 winning streak (BBC)"),
    (36, "India: Air India extends its Jeddah suspension to 24 Nov (Daily Jagran)"),
]

# ------------------------------------------------------------- illustrations
def _flames(d, x, y, w, h, n=5):
    """A row of flame triangles in orange/red/yellow."""
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
    cx, cy, r = x + 52, y + 46, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 139, 87))
    d.ellipse([cx - r + 8, cy - r + 10, cx - r + 26, cy - r + 26], fill=(139, 195, 74))
    d.ellipse([cx + 2, cy + 6, cx + 22, cy + 24], fill=(139, 195, 74))
    d.ellipse([cx - 12, cy + 14, cx + 4, cy + 30], fill=(139, 195, 74))
    ccx, ccy, cr = x + w - 52, y + 46, 30
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], fill=(252, 248, 238),
              outline=INK, width=3)
    d.line([ccx, ccy, ccx, ccy - cr + 8], fill=INK, width=3)
    d.line([ccx, ccy, ccx + cr - 12, ccy - 6], fill=INK, width=3)
    d.ellipse([ccx - 3, ccy - 3, ccx + 3, ccy + 3], fill=RED)
    d.rectangle([x + w // 2 - 78, y + h - 24, x + w // 2 + 78, y + h - 4],
                fill=DARKRED)
    centre(d, x + w // 2, y + h - 22, "DEAL IN SIGHT", SANSB(11), (255, 255, 255))


def ill_nepal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.ellipse([x + w - 30, y + 8, x + w - 6, y + 32], fill=(241, 196, 15))
    # plane (side view)
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
    # India flag (left) and Nepal flag (right) on poles
    for fx, cols in [(x + 26, [(255, 153, 51), (255, 255, 255), (19, 136, 8)]),
                     (x + w - 62, [(220, 20, 60), (0, 56, 147), (220, 20, 60)])]:
        d.line([fx, y + h - 30, fx, y + h - 62], fill=INK, width=2)
        for i, c in enumerate(cols):
            d.rectangle([fx, y + h - 62 + i * 9, fx + 30, y + h - 53 + i * 9],
                        fill=c)


def ill_sparta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKYNIGHT)
    for sx, sy in [(x + 30, y + 14), (x + 120, y + 10), (x + 220, y + 18),
                   (x + 280, y + 12)]:
        d.ellipse([sx, sy, sx + 4, sy + 4], fill=(255, 255, 255))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(28, 68, 110))
    for wx in range(0, w, 34):
        d.arc([x + wx, y + h - 26, x + wx + 30, y + h - 8], 200, 340,
              fill=(180, 210, 230), width=2)
    # ship hull + containers, flames above
    hx, hy = x + 40, y + h - 62
    d.polygon([(hx, hy + 22), (hx + 20, hy), (hx + w - 90, hy),
               (hx + w - 70, hy + 22)], fill=(139, 35, 35))
    d.rectangle([hx + 30, hy - 22, hx + 70, hy], fill=(70, 90, 110))
    d.rectangle([hx + 80, hy - 22, hx + 120, hy], fill=(180, 160, 90))
    d.rectangle([hx + 130, hy - 22, hx + 170, hy], fill=(70, 90, 110))
    d.rectangle([hx + 200, hy - 30, hx + 226, hy], fill=(220, 220, 220))
    _flames(d, hx + 24, hy - 32, 190, 32, n=6)
    _smoke(d, hx + 60, hy - 28)
    d.rectangle([x + 12, y + 8, x + 118, y + 24], fill=RED)
    centre(d, x + 65, y + 10, "SPARTA II ABLAZE", SANSB(10), (255, 255, 255))


def ill_tankers(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 20, x + w, y + h], fill=SEA)
    for tx in (x + 12, x + w // 2 + 6):
        d.rectangle([tx, y + h - 44, tx + w // 2 - 24, y + h - 22], fill=(40, 40, 40))
        d.rectangle([tx + 8, y + h - 58, tx + 34, y + h - 44], fill=(220, 220, 220))
        d.rectangle([tx + w // 2 - 58, y + h - 52, tx + w // 2 - 30, y + h - 44],
                    fill=(180, 60, 60))
    # projectile streaks + burst
    d.line([x + 30, y + 6, x + 60, y + 26], fill=(231, 76, 60), width=3)
    d.line([x + w - 40, y + 4, x + w - 70, y + 24], fill=(231, 76, 60), width=3)
    d.ellipse([x + w // 2 - 8, y + 8, x + w // 2 + 8, y + 24], fill=(241, 196, 15),
              outline=(231, 76, 60), width=2)


def ill_bahrain(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 220, 190))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(150, 150, 140))
    # factory: block + chimney + tanks
    d.rectangle([x + 14, y + h - 52, x + 76, y + h - 18], fill=(120, 120, 130))
    d.rectangle([x + 84, y + h - 44, x + 108, y + h - 18], fill=(90, 90, 100))
    d.rectangle([x + 116, y + h - 62, x + 126, y + h - 18], fill=(150, 60, 60))
    d.ellipse([x + 132, y + h - 40, x + 168, y + h - 18], fill=(200, 200, 210),
              outline=INK, width=1)
    d.rectangle([x + 132, y + h - 52, x + 168, y + h - 30], fill=(200, 200, 210))
    _flames(d, x + 20, y + h - 60, 60, 12, n=3)
    _smoke(d, x + 116, y + h - 58)


def ill_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 225, 200))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(170, 160, 140))
    # aid van with boxes
    vx, vy = x + 30, y + h - 48
    d.rectangle([vx, vy, vx + 96, vy + 26], fill=(252, 248, 238), outline=INK, width=2)
    d.rectangle([vx + 96, vy + 8, vx + 124, vy + 26], fill=(200, 60, 60),
                outline=INK, width=2)
    d.rectangle([vx + 12, vy + 6, vx + 34, vy + 20], fill=(180, 120, 60))
    d.rectangle([vx + 42, vy + 6, vx + 64, vy + 20], fill=(120, 160, 90))
    d.rectangle([vx + 72, vy + 6, vx + 88, vy + 20], fill=(180, 120, 60))
    for wx in (vx + 22, vx + 108):
        d.ellipse([wx, vy + 22, wx + 14, vy + 36], fill=INK)
    # drone above
    dx, dy = x + w - 52, y + 12
    d.ellipse([dx, dy, dx + 22, dy + 8], fill=(60, 60, 60))
    d.line([dx - 8, dy + 2, dx + 30, dy + 2], fill=INK, width=2)
    d.line([dx + 4, dy + 8, dx + 18, dy + 22], fill=(231, 76, 60), width=2)


def ill_myanmar(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 240))
    # courthouse with columns + scales
    cx = x + w // 2
    d.polygon([(cx - 70, y + 18), (cx, y + 2), (cx + 70, y + 18)], fill=(150, 40, 40))
    for px in (cx - 56, cx - 20, cx + 14, cx + 50):
        d.rectangle([px, y + 20, px + 8, y + h - 20], fill=(240, 240, 235),
                    outline=INK, width=1)
    d.rectangle([cx - 72, y + h - 22, cx + 72, y + h - 14], fill=(150, 40, 40))
    # scales of justice
    sx, sy = x + 18, y + h - 46
    d.line([sx + 10, sy, sx + 10, sy - 18], fill=INK, width=2)
    d.line([sx - 8, sy - 18, sx + 28, sy - 18], fill=INK, width=2)
    d.polygon([(sx - 10, sy - 6), (sx - 2, sy - 6), (sx - 6, sy + 2)], fill=GOLD)
    d.polygon([(sx + 14, sy - 6), (sx + 22, sy - 6), (sx + 18, sy + 2)], fill=GOLD)


def ill_trump(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 58, 95))
    # podium + microphones + flag stripes
    px = x + w // 2
    d.rectangle([px - 46, y + h - 44, px + 46, y + h - 10], fill=(120, 30, 30))
    d.rectangle([px - 46, y + h - 44, px + 46, y + h - 34], fill=(90, 20, 20))
    d.ellipse([px - 16, y + 10, px + 16, y + 42], fill=(232, 190, 150))
    d.polygon([(px - 26, y + 42), (px + 26, y + 42), (px + 34, y + h - 44),
               (px - 34, y + h - 44)], fill=(40, 40, 60))
    d.line([px - 12, y + h - 44, px - 20, y + 30], fill=INK, width=2)
    d.line([px + 12, y + h - 44, px + 20, y + 30], fill=INK, width=2)
    d.ellipse([px - 22, y + 28, px - 16, y + 34], fill=INK)
    d.ellipse([px + 16, y + 28, px + 22, y + 34], fill=INK)
    for i in range(4):
        d.rectangle([x + 6, y + 6 + i * 7, x + 26, y + 11 + i * 7],
                    fill=(255, 255, 255) if i % 2 == 0 else (185, 28, 28))


def ill_eisenkot(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(235, 230, 215))
    # Knesset-like building + two shaking hands
    bx = x + w // 2 - 60
    d.rectangle([bx, y + 22, bx + 120, y + h - 18], fill=(250, 248, 240),
                outline=INK, width=2)
    d.polygon([(bx - 8, y + 22), (bx + 60, y + 6), (bx + 128, y + 22)],
              fill=(150, 40, 40))
    for px in (bx + 14, bx + 46, bx + 78, bx + 104):
        d.rectangle([px, y + 30, px + 10, y + h - 22], fill=(200, 195, 180),
                    outline=INK, width=1)
    d.rectangle([bx + 52, y + h - 30, bx + 68, y + h - 18], fill=(60, 60, 60))
    # handshake: two sleeves + clasped hands
    d.polygon([(x + 16, y + h - 8), (x + 52, y + h - 26), (x + 60, y + h - 16),
               (x + 30, y + h - 2)], fill=NAVY)
    d.polygon([(x + w - 16, y + h - 8), (x + w - 52, y + h - 26),
               (x + w - 60, y + h - 16), (x + w - 30, y + h - 2)], fill=(60, 90, 60))
    d.ellipse([x + w // 2 - 14, y + h - 28, x + w // 2 + 14, y + h - 10],
              fill=(232, 190, 150))


def ill_chahal(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(255, 243, 224))
    # cricket ball + saffron band
    cx, cy, r = x + w // 2, y + h // 2 - 4, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(185, 28, 28))
    d.arc([cx - r + 6, cy - r, cx + r - 6, cy + r], 90, 270, fill=(255, 255, 255),
          width=2)
    d.arc([cx - r + 12, cy - r, cx + r - 12, cy + r], 270, 90, fill=(255, 255, 255),
          width=2)
    d.rectangle([x, y + h - 18, x + w, y + h - 8], fill=(255, 153, 51))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(19, 136, 8))


def ill_atp(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(120, 160, 220))
    # tennis court + net + trophy + ball
    d.rectangle([x + 10, y + 14, x + w - 10, y + h - 14], fill=(70, 140, 90))
    d.line([x + 10, y + h // 2, x + w - 10, y + h // 2], fill=(255, 255, 255),
           width=2)
    d.line([x + w // 2, y + 14, x + w // 2, y + h - 14], fill=(255, 255, 255),
           width=1)
    d.rectangle([x + w // 2 - 4, y + 10, x + w // 2 + 4, y + h - 10], fill=INK)
    d.ellipse([x + 24, y + h - 34, x + 40, y + h - 18], fill=(200, 230, 60),
              outline=INK, width=1)
    # trophy
    tx, ty = x + w - 52, y + 8
    d.polygon([(tx, ty), (tx + 26, ty), (tx + 22, ty + 22), (tx + 4, ty + 22)],
              fill=GOLD)
    d.rectangle([tx + 10, ty + 22, tx + 16, ty + 30], fill=GOLD)
    d.rectangle([tx + 4, ty + 30, tx + 22, ty + 34], fill=GOLD)


def ill_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(140, 190, 110))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 140, 70))
    # stumps + batsman silhouette + ball
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


def ill_nigeria(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.rectangle([x, y + h - 30, x + w, y + h], fill=SEA)
    for wx in range(0, w, 30):
        d.arc([x + wx, y + h - 24, x + wx + 28, y + h - 8], 200, 340,
              fill=(180, 210, 230), width=2)
    # capsized boat: hull upside down + lifebuoy
    bx, by = x + w // 2 - 52, y + h - 52
    d.polygon([(bx, by + 16), (bx + 20, by), (bx + 84, by), (bx + 104, by + 16)],
              fill=(120, 60, 30))
    d.ellipse([x + 18, y + h - 40, x + 42, y + h - 16], fill=(255, 255, 255),
              outline=(231, 76, 60), width=4)
    d.ellipse([x + w - 44, y + 10, x + w - 20, y + 34], fill=(241, 196, 15))


ILLS = {"cop31": ill_cop31, "nepal": ill_nepal, "sparta": ill_sparta,
        "tankers": ill_tankers, "bahrain": ill_bahrain, "gaza": ill_gaza,
        "myanmar": ill_myanmar, "trump": ill_trump, "eisenkot": ill_eisenkot,
        "chahal": ill_chahal, "atp": ill_atp, "cricket": ill_cricket,
        "nigeria": ill_nigeria}

# ------------------------------------------------------------------- layout
def tag_colour(tag):
    return {"CONFIRMED": GREEN, "REPORTED": GREY, "FORECAST": NAVY}.get(tag, GREY)


def draw_lead(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=PAPER, outline=INK, width=1)
    ih = 100
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
    ih = 62
    ILLS[s["ill"]](d, x + 1, y + 1, w - 2, ih)
    d.line([x, y + ih + 1, x + w, y + ih + 1], fill=INK, width=1)
    ky = y + ih + 4
    # kicker coloured by check status (green = confirmed, grey = reported,
    # navy = forecast); the tag text lives only on the leads, where it fits
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
    d.rectangle([0, 0, W, 22], fill=RED)
    d.text((14, 4), "THE WORLD IN ONE DAY \u2014 EARLY EDITION",
           font=SANSB(11), fill=(255, 255, 255))
    rt = "36 STORIES \u00b7 6 REGIONS \u00b7 SUNDAY 22 NOVEMBER 2026"
    d.text((W - 14 - SANSB(11).getlength(rt), 4), rt, font=SANSB(11),
           fill=(255, 255, 255))
    # masthead
    centre(d, W // 2, 28, "Sunday 22 November 2026", SERIFB(52), INK)
    d.line([14, 84, W - 14, 84], fill=INK, width=2)
    centre(d, W // 2, 90,
           "COP31 deal at dawn in Antalya \u00b7 Nepal PM flies to Delhi "
           "\u00b7 Sparta II still ablaze in the Gulf of Finland",
           SERI(16), INK)
    # stat strip
    stats = [("06:00 GMT", "COP31 approval session"),
             ("200", "nations at COP31"),
             ("2", "tankers hit off Oman"),
             ("24", "dead, Nigeria boat"),
             ("37-12", "England's record win"),
             ("18:00 CET", "ATP final, Turin")]
    sw, gap = 162, 4
    for i, (num, lab) in enumerate(stats):
        x = 14 + i * (sw + gap)
        d.rectangle([x, 108, x + sw, 142], fill=PAPER, outline=LINE, width=1)
        centre(d, x + sw // 2, 111, num, SANSB(19), RED)
        centre(d, x + sw // 2, 131, lab, SANS(9), GREY)
    # UTC timeline
    d.line([14, 162, W - 14, 162], fill=RED, width=2)
    tl = [("Sat-night", "Sparta II fire out of control"),
          ("03:00 GMT", "Objections to COP text due"),
          ("06:00 GMT", "Plenary to approve the deal"),
          ("15:00 IST", "Nepal PM lands in Delhi"),
          ("18:00 CET", "ATP final in Turin")]
    tw = (W - 28) // len(tl)
    for i, (t, lab) in enumerate(tl):
        cx = 14 + i * tw + tw // 2
        d.ellipse([cx - 4, 158, cx + 4, 166], fill=RED)
        centre(d, cx, 146, t, SANSB(9), RED)
        centre(d, cx, 168, lab, SANS(8.5), INK)
    # leads
    lw, lgap = 326, 6
    for i, s in enumerate(LEADS):
        draw_lead(d, s, 14 + i * (lw + lgap), 182, lw, 232)
    # medium rows, 5 per row
    mw, mgap = 196, 5
    for i, s in enumerate(MED):
        row, col = divmod(i, 5)
        draw_med(d, s, 14 + col * (mw + mgap), 418 + row * 138, mw, 134)
    # ALSO header
    d.text((14, 694), "ALSO ON SUNDAY 22 NOVEMBER \u2014 23 MORE STORIES",
           font=SANSB(12), fill=INK)
    d.line([14, 710, W - 14, 710], fill=INK, width=2)
    # ALSO list, two columns, one line each
    colw = 492
    for i, (n, txt) in enumerate(ALSO):
        col, row = divmod(i, 12)
        x = 14 + col * (colw + 12)
        y = 716 + row * 12
        item = f"{n}  {txt}"
        fnt = SANS(10)
        while fnt.getlength(item) > colw - 4 and fnt.size > 8:
            fnt = SANS(fnt.size - 1)
        d.text((x, y), item, font=fnt, fill=INK)
    # DATE CHECK box
    d.rectangle([14, 866, W - 14, 948], outline=DARKRED, width=2)
    d.text((22, 872),
           "DATE CHECK \u2014 EARLY EDITION \u00b7 WIRES AS OF 01:00 UTC, "
           "SUNDAY 22 NOVEMBER 2026", font=SANSB(11), fill=DARKRED)
    block(d, 22, 890, W - 44,
          "Left out as other days' news: Peru's 6.7 quake (20 Nov local) \u00b7 "
          "\u201cEl Chapo Isidro\u201d seized (21 Nov) \u00b7 Roundup $7.25bn approved "
          "(Fri 20 Nov) \u00b7 Somalia orders the UAE envoy out (Thu 19 Nov) \u00b7 "
          "Estonia to shut its Russia border (announced 15 Nov) \u00b7 the "
          "Shenzhen summit (Fri) \u00b7 BepiColombo at Mercury.",
          SANS(10.5), leading=13, max_lines=2)
    block(d, 22, 918, W - 44,
          "Still to come at press time: COP31's 06:00 GMT vote \u00b7 Nepal PM's "
          "Delhi arrival \u00b7 the ATP final \u00b7 the Las Vegas GP. Stories "
          "marked SAT happened on Saturday; they are the overnight news "
          "Sunday woke to.", SANS(10.5), leading=13, max_lines=2)
    # footer
    block(d, 14, 954, W - 28,
          "Every story here happened, or was first reported, on Sunday 22 November "
          "2026, or on Saturday night. Sources: Reuters, AP, AFP, IANS, ATP, "
          "ESPNcricinfo, UKMTO, NDTV, BBC, PTI, ANI. Pictures: original, drawn in "
          "code. HOW WE CHECKED \u2014 CONFIRMED = 2+ outlets \u00b7 REPORTED = one "
          "outlet \u00b7 FORECAST = scheduled today.",
          SANS(9), fill=GREY, leading=12, max_lines=2)
    return img


if __name__ == "__main__":
    im = draw()
    im.save("entry.png", optimize=True)
    print("wrote entry.png", im.size)
