# news-image-20261124 v3 — "The World in One Day"
# Broadsheet front page: 40 stories, all dated Tuesday 24 November 2026.
# Self-contained: stdlib + PIL only, no local imports. Run: python3 -P -s main.py
# Writes entry.png next to this file and (when available) a copy to /output.
import json
import os
import shutil

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 10
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
PAPER = (253, 246, 227)
INK = (26, 26, 46)
NAVY = (18, 38, 74)
RED = (176, 30, 30)
GOLD = (184, 134, 11)
GREY = (90, 90, 90)
LINE = (200, 190, 165)

REGION_COLORS = {
    "AFRICA": (34, 139, 34),
    "EAST ASIA": (178, 34, 34),
    "SOUTH ASIA": (220, 110, 0),
    "SE ASIA": (0, 128, 128),
    "EUROPE": (31, 58, 147),
    "MID EAST": (128, 0, 128),
    "N. AMERICA": (0, 100, 180),
    "S. AMERICA": (190, 110, 0),
    "OCEANIA": (0, 120, 80),
}
BADGE_COLORS = {
    "CONFIRMED": (0, 120, 60),
    "OFFICIAL": (25, 80, 180),
    "REPORTED": (176, 120, 0),
}
# region strip: (label, count) — 9 regions, 40 stories incl. the hero (South Asia)
REGIONS = [
    ("AFRICA", 5), ("EAST ASIA", 4), ("SOUTH ASIA", 2), ("SE ASIA", 2),
    ("EUROPE", 6), ("MID EAST", 6), ("N. AMERICA", 5), ("S. AMERICA", 5),
    ("OCEANIA", 5),
]


def _font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    except Exception:
        return ImageFont.load_default()


F_SERIF_B = lambda s: _font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
F_SERIF = lambda s: _font("DejaVuSerif.ttf", s)  # noqa: E731
F_SANS_B = lambda s: _font("DejaVuSans-Bold.ttf", s)  # noqa: E731
F_SANS = lambda s: _font("DejaVuSans.ttf", s)  # noqa: E731

# ---------------------------------------------------------------- data
# badge rule: CONFIRMED = 2+ outlets; OFFICIAL = agency/court on record;
# REPORTED = single outlet. Every attribution below was verified 24 Nov 2026.
HERO = {
    "head": "NEPAL QUAKE 5.6 ROCKS BORDER",
    "sub": "Taplejung tremor near Tibet border; no casualties reported",
    "src": "Xinhua · NCS", "badge": "CONFIRMED",
}

# 13 feature cards. body = two-line summary. lon/lat = map pin.
FEATURES = [
    {"n": 1, "band": "MID EAST", "lon": 56.3, "lat": 26.6,
     "head": "HORMUZ: 4TH TANKER HIT",
     "body": "IRGC says a fourth tanker hit a mine east of the strait; the US stays silent. Fourth claim in two days.",
     "src": "Tasnim · IRIB", "badge": "REPORTED", "scene": "tanker"},
    {"n": 2, "band": "N. AMERICA", "lon": -74.0, "lat": 40.7,
     "head": "HUAWEI GUILTY: 10 OF 12",
     "body": "Brooklyn jury convicts Huawei on fraud and sanctions counts. Acquitted on racketeering; sentencing 14 Sep 2027.",
     "src": "US DOJ", "badge": "OFFICIAL", "scene": "court"},
    {"n": 3, "band": "EAST ASIA", "lon": 121.5, "lat": 31.2,
     "head": "SHANGHAI BOSS PROBED",
     "body": "Chen Jining probed for \u201cserious violations of discipline and law\u201d. Fourth Politburo member to fall since 2025.",
     "src": "Xinhua · Reuters", "badge": "CONFIRMED", "scene": "shanghai"},
    {"n": 4, "band": "S. AMERICA", "lon": -73.6, "lat": 4.15,
     "head": "COLOMBIA BLAST: 23 HURT",
     "body": "Blast outside the Meta HQ injures 23 in Villavicencio. Ex-FARC blamed.",
     "src": "AP", "badge": "REPORTED", "scene": "carbomb"},
    {"n": 5, "band": "EUROPE", "lon": 35.2, "lat": 47.85,
     "head": "ZAPORIZHZHIA HIT",
     "body": "Overnight strikes kill 2, wound 40 in the city. Four children hurt.",
     "src": "Reuters", "badge": "REPORTED", "scene": "zaporizhzhia"},
    {"n": 6, "band": "EUROPE", "lon": 2.35, "lat": 48.86,
     "head": "SANOFI BUYS INSMED",
     "body": "$41bn cash at $175 a share, the year\u2019s top biopharma deal.",
     "src": "Sanofi", "badge": "OFFICIAL", "scene": "sanofi"},
    {"n": 7, "band": "EAST ASIA", "lon": 100.3, "lat": 39.7,
     "head": "TIANGONG OPENS UP",
     "body": "First foreign astronaut named for Tiangong: Pakistan\u2019s Ali.",
     "src": "Xinhua · AP", "badge": "CONFIRMED", "scene": "tiangong"},
    {"n": 8, "band": "AFRICA", "lon": 29.6, "lat": 1.8,
     "head": "EBOLA TEAM FREED",
     "body": "WHO staff freed from Akwe hospital after 3 days trapped.",
     "src": "UN News · WHO", "badge": "OFFICIAL", "scene": "ebola"},
    {"n": 9, "band": "MID EAST", "lon": 34.45, "lat": 31.5,
     "head": "HAMAS CHIEF KILLED",
     "body": "Strikes kill Hamas security chief Abu Nahel and six others.",
     "src": "Just Security", "badge": "REPORTED", "scene": "gaza"},
    {"n": 10, "band": "OCEANIA", "lon": 149.1, "lat": -35.3,
     "head": "AUSTRALIA FINES BIG TECH",
     "body": "Fines up to 5% of global revenue in a digital duty of care.",
     "src": "Reuters", "badge": "REPORTED", "scene": "fines"},
    {"n": 11, "band": "S. AMERICA", "lon": -47.9, "lat": -15.8,
     "head": "LULA\u2019S FISCAL PLAN #2",
     "body": "Lula backs a second round of spending curbs for Congress.",
     "src": "Reuters", "badge": "REPORTED", "scene": "lula"},
    {"n": 12, "band": "EAST ASIA", "lon": 130.9, "lat": 37.5,
     "head": "JETS OVER KOREA",
     "body": "Russian jets enter the ADIZ; F-15Ks scramble to Ulleung.",
     "src": "Yonhap · SBS", "badge": "CONFIRMED", "scene": "jets"},
    {"n": 13, "band": "OCEANIA", "lon": 160.0, "lat": -9.4,
     "head": "SOLOMONS CUT CHINA",
     "body": "Honiara to end its 2022 security pact with Beijing.",
     "src": "Reuters", "badge": "REPORTED", "scene": "solomons"},
]

# 26 numbered briefs: headline + one-line sub + source + badge.
BRIEFS = [
    {"n": 14, "band": "AFRICA", "lon": 13.15, "lat": 11.85,
     "head": "BORNO BACK TO SCHOOL", "sub": "Enrolment nearly doubles",
     "src": "Al Jazeera", "badge": "REPORTED"},
    {"n": 15, "band": "AFRICA", "lon": 39.5, "lat": 12.4,
     "head": "AMNESTY: WAR CRIMES", "sub": "Alamata killings probed in new report",
     "src": "Amnesty · Reuters", "badge": "CONFIRMED"},
    {"n": 16, "band": "AFRICA", "lon": -0.2, "lat": 5.6,
     "head": "GHANA EYES INVESTORS", "sub": "Business reform bill unveiled in Accra",
     "src": "Ghana Guardian", "badge": "REPORTED"},
    {"n": 17, "band": "AFRICA", "lon": 5.8, "lat": 5.5,
     "head": "DELTA CLASH: 6 DEAD", "sub": "Police confirm 6 dead in Uduere rally attack",
     "src": "Police", "badge": "OFFICIAL"},
    {"n": 18, "band": "SE ASIA", "lon": 103.85, "lat": 1.29,
     "head": "WONG: NO BACKDOOR", "sub": "S\u2019pore bars chip evasion; \u201cno backdoor\u201d for US curbs",
     "src": "PMO Singapore", "badge": "OFFICIAL"},
    {"n": 19, "band": "SE ASIA", "lon": 101.7, "lat": 3.13,
     "head": "MALAYSIA CUTS FIRMS", "sub": "Data hubs told to drop 7 US-blacklisted firms",
     "src": "MITI", "badge": "OFFICIAL"},
    {"n": 20, "band": "EAST ASIA", "lon": 125.75, "lat": 39.03,
     "head": "N. KOREA THREATENS", "sub": "Swiss office closure vowed over camp sanctions",
     "src": "AP · Reuters", "badge": "CONFIRMED"},
    {"n": 21, "band": "SOUTH ASIA", "lon": 90.4, "lat": 23.8,
     "head": "HASINA TO RETURN", "sub": "Ex-PM eyes Dec 16 comeback; Dhaka says \u201cin handcuffs\u201d",
     "src": "Reuters", "badge": "REPORTED"},
    {"n": 22, "band": "EUROPE", "lon": 4.35, "lat": 50.85,
     "head": "NUCLEAR SATELLITE FEAR", "sub": "NATO vows space defence as Russia arms orbit",
     "src": "BBC", "badge": "REPORTED"},
    {"n": 23, "band": "EUROPE", "lon": 2.9, "lat": 48.4,
     "head": "FARTHEST QUASAR", "sub": "Euclid finds quasar 630m years after the Big Bang",
     "src": "ESA", "badge": "OFFICIAL"},
    {"n": 24, "band": "EUROPE", "lon": 4.9, "lat": 50.4,
     "head": "EU CAR SALES +3.4%", "sub": "Ninth straight monthly rise to 1.13m cars",
     "src": "ACEA", "badge": "OFFICIAL"},
    {"n": 25, "band": "EUROPE", "lon": 13.4, "lat": 52.5,
     "head": "GERMANY GETS DELTA", "sub": "First foreign access to Ukraine\u2019s battlefield system",
     "src": "Kyiv Independent", "badge": "REPORTED"},
    {"n": 26, "band": "MID EAST", "lon": 35.0, "lat": 31.9,
     "head": "\u2018TOXIC LAND\u2019", "sub": "Oxfam\u2019s verdict on Gaza after two years of war",
     "src": "Oxfam", "badge": "OFFICIAL"},
    {"n": 27, "band": "MID EAST", "lon": 44.9, "lat": 13.0,
     "head": "LAHJ STRIKE KILLS 25", "sub": "Toll disputed as sides trade blame",
     "src": "Saba · AFP", "badge": "REPORTED"},
    {"n": 28, "band": "MID EAST", "lon": 55.9, "lat": 25.8,
     "head": "RAK CRASH KILLS 11", "sub": "Bus-truck smash in Ras al-Khaimah",
     "src": "The National", "badge": "REPORTED"},
    {"n": 29, "band": "MID EAST", "lon": 44.4, "lat": 33.3,
     "head": "IRAQ SEIZES BORDERS", "sub": "Baghdad takes Kurd crossings; Barzani rejects move",
     "src": "Reuters", "badge": "REPORTED"},
    {"n": 30, "band": "N. AMERICA", "lon": -107.4, "lat": 24.8,
     "head": "\u2018EL CHAPO ISIDRO\u2019", "sub": "Mexico to try him at home despite US request",
     "src": "Al Jazeera", "badge": "REPORTED"},
    {"n": 31, "band": "N. AMERICA", "lon": -66.1, "lat": 18.47,
     "head": "MISS UNIVERSE FINAL", "sub": "Crown night in San Juan; 116 compete",
     "src": "Telemundo", "badge": "REPORTED"},
    {"n": 32, "band": "N. AMERICA", "lon": -73.7, "lat": 40.8,
     "head": "47,000 WOMEN KILLED", "sub": "UN: 5 an hour killed by kin in 2025",
     "src": "UN News", "badge": "OFFICIAL"},
    {"n": 33, "band": "N. AMERICA", "lon": -76.6, "lat": 39.3,
     "head": "MLB\u2019S $125M ACE", "sub": "Peralta to Orioles; Sato $120m to Cubs",
     "src": "USA Today", "badge": "REPORTED"},
    {"n": 34, "band": "S. AMERICA", "lon": -58.4, "lat": -34.6,
     "head": "ARGENTINA AXES PRIMARIES", "sub": "Milei seeks to suspend PASO to cut spending",
     "src": "MercoPress", "badge": "REPORTED"},
    {"n": 35, "band": "S. AMERICA", "lon": -66.9, "lat": 10.5,
     "head": "VENEZUELA POLL: 65.7%", "sub": "Two-thirds say leadership \u201cdoes not work\u201d",
     "src": "Daily Journal", "badge": "REPORTED"},
    {"n": 36, "band": "S. AMERICA", "lon": -47.4, "lat": -15.4,
     "head": "BRAZIL HIKES INFLATION CALL", "sub": "2027 forecast raised to 4.5%; growth cut to 1.8%",
     "src": "MercoPress", "badge": "REPORTED"},
    {"n": 37, "band": "OCEANIA", "lon": 151.2, "lat": -33.9,
     "head": "KOALA AIRLINE", "sub": "Watchdog met carrier twice over new flights",
     "src": "Bloomberg", "badge": "REPORTED"},
    {"n": 38, "band": "OCEANIA", "lon": 149.6, "lat": -35.0,
     "head": "AU\u2013SG CO2 PACT", "sub": "Offshore storage deal signed in Canberra",
     "src": "PMO Australia", "badge": "OFFICIAL"},
    {"n": 39, "band": "OCEANIA", "lon": 148.6, "lat": -35.6,
     "head": "AU\u2013SG AI PACT", "sub": "Deeper data and chip cooperation agreed",
     "src": "DailyFoxNews", "badge": "REPORTED"},
]

DATE_CHECK = (
    "DATE CHECK \u2014 Every story above happened, or was first reported, on Tuesday "
    "24 November 2026 (00:00\u201324:00 UTC). Excluded as not 24 Nov: Merkury sinking "
    "(22 Nov) \u00b7 COP31 collapse (22 Nov) \u00b7 Argentina 7\u20130 (17 Nov) \u00b7 Paredes "
    "collapse (21 Nov) \u00b7 Tupanciret\u00e3 storm (20 Nov) \u00b7 Bolsonaro ICU admission "
    "(20 Nov) \u00b7 Gaza strikes (23 Nov) \u00b7 Huang reinstatement (23 Nov) \u00b7 "
    "Measles 9th death (23 Nov) \u00b7 SpaceX suits filed (23 Nov) \u00b7 Hegseth "
    "Caracas deal (18 Nov)."
)


# ---------------------------------------------------------------- helpers
def text_w(d, text, font):
    return d.textlength(text, font=font)


def wrap(d, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if text_w(d, trial, font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_max(d, text, font, max_w, max_lines):
    """Wrap to at most max_lines; ellipsize the last line if it overflows."""
    lines = wrap(d, text, font, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and text_w(d, lines[-1] + "\u2026", font) > max_w:
        lines[-1] = lines[-1][:-1]
    lines[-1] = lines[-1] + "\u2026"
    return lines


def vgrad(d, x0, y0, x1, y1, top, bot):
    """Vertical gradient fill of a rectangle."""
    h = max(1, y1 - y0)
    for i in range(h):
        t = i / h
        c = tuple(int(top[c] + (bot[c] - top[c]) * t) for c in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def sun(d, cx, cy, r, color=(255, 214, 90)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def mountains(d, x, y, w, h, color, peaks):
    """Jagged mountain range across a box; peaks = list of (fx, fh)."""
    pts = [(x, y + h)]
    for fx, fh in peaks:
        pts.append((x + int(fx * w), y + h - int(fh * h)))
    pts.append((x + w, y + h))
    d.polygon(pts, fill=color)


def house(d, x, y, s, wall, roof):
    d.rectangle([x, y, x + s, y + int(s * 0.7)], fill=wall)
    d.polygon([(x - 2, y), (x + s / 2, y - int(s * 0.45)),
               (x + s + 2, y)], fill=roof)


def building(d, x, y, w, h, color, lit=(255, 220, 120)):
    d.rectangle([x, y, x + w, y + h], fill=color)
    for wy in range(y + 6, y + h - 4, 9):
        for wx in range(x + 4, x + w - 4, 9):
            if (wx * 7 + wy * 13) % 5 < 2:
                d.rectangle([wx, wy, wx + 4, wy + 5], fill=lit)


def skyline(d, x, y, w, h, color, seed=1):
    """Row of towers with lit windows."""
    n = 7
    bw = w // n
    for i in range(n):
        bh = int(h * (0.45 + ((i * 37 + seed * 11) % 50) / 100.0))
        bx = x + i * bw + 1
        building(d, bx, y + h - bh, bw - 2, bh, color)


def flame(d, cx, cy, s):
    d.polygon([(cx, cy - s), (cx + int(s * 0.55), cy - int(s * 0.1)),
               (cx + int(s * 0.35), cy + int(s * 0.5)),
               (cx - int(s * 0.35), cy + int(s * 0.5)),
               (cx - int(s * 0.55), cy - int(s * 0.1))],
              fill=(230, 110, 20))
    d.polygon([(cx, cy - int(s * 0.55)), (cx + int(s * 0.3), cy),
               (cx, cy + int(s * 0.4)), (cx - int(s * 0.3), cy)],
              fill=(255, 200, 40))


def smoke(d, cx, cy, s, color=(120, 120, 120)):
    for dx, dy, r in ((-1, 0, 0.55), (0, -1, 0.7), (1, -0.4, 0.5)):
        d.ellipse([cx + dx * s - r * s, cy + dy * s - r * s,
                   cx + dx * s + r * s, cy + dy * s + r * s], fill=color)


# ------------------------------------------------------- vector scenes
# Each scene draws inside the box (x, y, x+w, y+h) on draw d.

def sc_quake(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (255, 196, 120), (250, 226, 170))
    sun(d, x + int(w * 0.78), y + int(h * 0.22), max(6, h // 9))
    mountains(d, x, y + int(h * 0.15), w, int(h * 0.55), (90, 110, 140),
              [(0.1, 0.9), (0.3, 0.55), (0.5, 1.0), (0.7, 0.6), (0.9, 0.85)])
    mountains(d, x, y + int(h * 0.45), w, int(h * 0.4), (70, 130, 80),
              [(0.15, 0.7), (0.4, 1.0), (0.65, 0.6), (0.85, 0.9)])
    mountains(d, x, y + int(h * 0.68), w, int(h * 0.32), (46, 96, 58),
              [(0.2, 0.8), (0.5, 1.0), (0.8, 0.75)])
    gy = y + h - int(h * 0.18)
    d.rectangle([x, gy, x + w, y + h], fill=(120, 150, 90))
    s = max(10, h // 6)
    house(d, x + int(w * 0.12), gy - int(s * 0.7), s, (210, 180, 140), (140, 60, 40))
    house(d, x + int(w * 0.30), gy - int(s * 0.7), s, (200, 170, 130), (140, 60, 40))
    # cracked, leaning house
    d.polygon([(x + int(w * 0.55), gy), (x + int(w * 0.55), gy - int(s * 0.7)),
               (x + int(w * 0.55) + s, gy - int(s * 0.45)),
               (x + int(w * 0.55) + s, gy)], fill=(190, 160, 120))
    d.line([(x + int(w * 0.55), gy - int(s * 0.7)),
            (x + int(w * 0.55) + s, gy - int(s * 0.45))], fill=(90, 40, 20), width=2)
    smoke(d, x + int(w * 0.62), gy - int(s * 0.9), max(8, h // 10),
          color=(200, 190, 170))


def sc_tanker(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (30, 60, 110), (120, 170, 210))
    sun(d, x + int(w * 0.82), y + int(h * 0.2), max(6, h // 10),
        color=(255, 230, 150))
    sea = y + int(h * 0.62)
    d.rectangle([x, sea, x + w, y + h], fill=(16, 80, 140))
    d.line([(x, sea), (x + w, sea)], fill=(200, 220, 240), width=2)
    # tanker hull + containers
    d.rectangle([x + int(w * 0.08), sea - int(h * 0.16), x + int(w * 0.92),
                 sea], fill=(40, 40, 50))
    for i, c in enumerate([(200, 60, 40), (40, 120, 180), (220, 160, 40)]):
        cx = x + int(w * (0.16 + i * 0.24))
        d.rectangle([cx, sea - int(h * 0.30), cx + int(w * 0.18),
                     sea - int(h * 0.16)], fill=c)
    # flames on two containers + smoke
    flame(d, x + int(w * 0.25), sea - int(h * 0.38), max(8, h // 7))
    flame(d, x + int(w * 0.72), sea - int(h * 0.34), max(7, h // 8))
    smoke(d, x + int(w * 0.25), sea - int(h * 0.55), max(7, h // 9))
    smoke(d, x + int(w * 0.72), sea - int(h * 0.5), max(7, h // 9))


def sc_court(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (200, 215, 235), (240, 238, 225))
    # courthouse: pediment + columns
    bx, by, bw, bh = x + int(w * 0.14), y + int(h * 0.18), int(w * 0.72), int(h * 0.72)
    d.polygon([(bx - 4, by), (bx + bw / 2, by - int(h * 0.14)),
               (bx + bw + 4, by)], fill=(120, 110, 95))
    d.rectangle([bx, by, bx + bw, by + bh], fill=(190, 180, 160))
    for i in range(4):
        cx = bx + int(bw * (0.14 + i * 0.24))
        d.rectangle([cx - 3, by + 4, cx + 3, by + bh - 4], fill=(245, 240, 225))
    d.rectangle([bx - 4, by + bh - 4, bx + bw + 4, by + bh], fill=(120, 110, 95))
    # scales of justice above the door
    sx, sy = x + int(w * 0.5), y + int(h * 0.52)
    d.line([(sx, sy - 12), (sx, sy + 10)], fill=(60, 50, 40), width=2)
    d.line([(sx - 12, sy - 8), (sx + 12, sy - 8)], fill=(60, 50, 40), width=2)
    d.polygon([(sx - 16, sy - 2), (sx - 8, sy - 2), (sx - 12, sy + 6)],
              fill=(200, 160, 40))
    d.polygon([(sx + 8, sy - 2), (sx + 16, sy - 2), (sx + 12, sy + 6)],
              fill=(200, 160, 40))


def sc_shanghai(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (250, 190, 120), (200, 120, 90))
    sun(d, x + int(w * 0.2), y + int(h * 0.24), max(6, h // 10),
        color=(255, 240, 180))
    gy = y + h - int(h * 0.12)
    d.rectangle([x, gy, x + w, y + h], fill=(90, 80, 90))
    # Oriental Pearl-style tower
    tx = x + int(w * 0.62)
    d.rectangle([tx - 3, y + int(h * 0.18), tx + 3, gy], fill=(70, 60, 80))
    d.ellipse([tx - 10, y + int(h * 0.30), tx + 10, y + int(h * 0.30) + 16],
              fill=(200, 60, 60))
    d.ellipse([tx - 7, y + int(h * 0.58), tx + 7, y + int(h * 0.58) + 12],
              fill=(200, 60, 60))
    skyline(d, x, y + int(h * 0.35), int(w * 0.55), int(h * 0.53),
            (60, 55, 75), seed=3)
    # red flag
    d.line([(x + int(w * 0.88), y + int(h * 0.3)), (x + int(w * 0.88), gy)],
           fill=(60, 50, 60), width=2)
    d.polygon([(x + int(w * 0.88), y + int(h * 0.3)),
               (x + int(w * 0.88) + 16, y + int(h * 0.3) + 5),
               (x + int(w * 0.88), y + int(h * 0.3) + 10)], fill=(200, 30, 30))


def sc_carbomb(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (210, 220, 235), (245, 240, 225))
    gy = y + h - int(h * 0.2)
    skyline(d, x, y + int(h * 0.1), w, int(h * 0.55), (110, 105, 100), seed=5)
    d.rectangle([x, gy, x + w, y + h], fill=(90, 85, 80))
    d.line([(x, gy + int(h * 0.1)), (x + w, gy + int(h * 0.1))],
           fill=(220, 200, 60), width=2)
    # explosion starburst + smoke
    import math as _m
    cx, cy = x + int(w * 0.55), gy - int(h * 0.12)
    for r, c in ((26, (255, 200, 40)), (17, (230, 110, 20)), (9, (255, 240, 120))):
        pts = []
        for k in range(16):
            ang = k * _m.pi / 8
            rr = r if k % 2 == 0 else r // 2
            pts.append((cx + int(rr * _m.cos(ang)), cy + int(rr * _m.sin(ang))))
        d.polygon(pts, fill=c)
    smoke(d, cx, cy - 18, 12)
    d.rectangle([x + int(w * 0.12), gy - 8, x + int(w * 0.32), gy], fill=(40, 40, 60))
    d.ellipse([x + int(w * 0.15), gy - 3, x + int(w * 0.18), gy + 1], fill=(10, 10, 10))
    d.ellipse([x + int(w * 0.27), gy - 3, x + int(w * 0.30), gy + 1], fill=(10, 10, 10))


def sc_zaporizhzhia(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (20, 25, 60), (70, 80, 120))
    for sx, sy in ((0.15, 0.2), (0.7, 0.12), (0.85, 0.35), (0.4, 0.08)):
        d.ellipse([x + int(w * sx) - 1, y + int(h * sy) - 1,
                   x + int(w * sx) + 1, y + int(h * sy) + 1], fill=(255, 255, 255))
    gy = y + h - int(h * 0.1)
    d.rectangle([x, gy, x + w, y + h], fill=(30, 30, 40))
    building(d, x + int(w * 0.1), y + int(h * 0.3), int(w * 0.34), gy - (y + int(h * 0.3)),
             (70, 70, 90))
    building(d, x + int(w * 0.55), y + int(h * 0.42), int(w * 0.34), gy - (y + int(h * 0.42)),
             (60, 60, 80))
    # fire + smoke on the left block
    flame(d, x + int(w * 0.27), y + int(h * 0.32), max(8, h // 7))
    smoke(d, x + int(w * 0.27), y + int(h * 0.16), max(8, h // 8))
    # drone silhouette
    dx, dy = x + int(w * 0.78), y + int(h * 0.2)
    d.line([(dx - 10, dy - 6), (dx + 10, dy + 6)], fill=(220, 220, 220), width=2)
    d.line([(dx - 10, dy + 6), (dx + 10, dy - 6)], fill=(220, 220, 220), width=2)
    d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(220, 220, 220))


def sc_sanofi(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (225, 240, 250), (250, 248, 240))
    # lab flask
    fx, fy = x + int(w * 0.3), y + int(h * 0.2)
    d.polygon([(fx - 4, fy), (fx + 4, fy), (fx + 14, fy + int(h * 0.5)),
               (fx - 14, fy + int(h * 0.5))], outline=(40, 90, 140), width=2)
    d.polygon([(fx - 11, fy + int(h * 0.32)), (fx + 11, fy + int(h * 0.32)),
               (fx + 14, fy + int(h * 0.5)), (fx - 14, fy + int(h * 0.5))],
              fill=(80, 160, 220))
    # molecule
    mx, my = x + int(w * 0.72), y + int(h * 0.35)
    for ox, oy in ((-12, -8), (12, -8), (0, 10)):
        d.line([(mx, my), (mx + ox, my + oy)], fill=(90, 90, 110), width=2)
    d.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(40, 90, 140))
    for ox, oy in ((-12, -8), (12, -8), (0, 10)):
        d.ellipse([mx + ox - 4, my + oy - 4, mx + ox + 4, my + oy + 4],
                  fill=(200, 60, 60))
    # pills
    d.ellipse([x + int(w * 0.14), y + int(h * 0.68), x + int(w * 0.14) + 16,
               y + int(h * 0.68) + 8], fill=(220, 80, 80))
    d.ellipse([x + int(w * 0.62), y + int(h * 0.72), x + int(w * 0.62) + 16,
               y + int(h * 0.72) + 8], fill=(80, 140, 220))


def sc_tiangong(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 12, 40))
    for i in range(14):
        sx = x + ((i * 53 + 11) % w)
        sy = y + ((i * 29 + 7) % int(h * 0.7))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # earth arc (kept inside the scene box)
    import math as _m
    pts = [(x, y + h)]
    for k in range(21):
        t = k / 20.0
        pts.append((x + int(t * w),
                    y + int(h * 0.94) - int(_m.sin(t * _m.pi) * h * 0.06)))
    pts.append((x + w, y + h))
    d.polygon(pts, fill=(40, 110, 190))
    # station: core + solar panels
    cx, cy = x + int(w * 0.5), y + int(h * 0.38)
    d.rectangle([cx - 26, cy - 6, cx + 26, cy + 6], fill=(200, 200, 210))
    d.rectangle([cx - 44, cy - 3, cx - 28, cy + 3], fill=(40, 80, 180))
    d.rectangle([cx + 28, cy - 3, cx + 44, cy + 3], fill=(40, 80, 180))
    d.rectangle([cx - 6, cy - 16, cx + 6, cy - 6], fill=(180, 180, 190))
    d.rectangle([cx - 6, cy + 6, cx + 6, cy + 16], fill=(180, 180, 190))
    # rocket trail
    rx = x + int(w * 0.16)
    d.polygon([(rx, y + int(h * 0.55)), (rx + 6, y + int(h * 0.62)),
               (rx + 12, y + int(h * 0.55)), (rx + 6, y + int(h * 0.42))],
              fill=(230, 230, 230))
    flame(d, rx + 6, y + int(h * 0.68), 6)


def sc_ebola(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (250, 230, 180), (240, 210, 150))
    sun(d, x + int(w * 0.8), y + int(h * 0.2), max(6, h // 10))
    mountains(d, x, y + int(h * 0.4), w, int(h * 0.3), (120, 140, 90),
              [(0.2, 0.8), (0.5, 1.0), (0.8, 0.7)])
    gy = y + h - int(h * 0.14)
    d.rectangle([x, gy, x + w, y + h], fill=(150, 120, 80))
    # medical tent + red cross
    tx = x + int(w * 0.32)
    d.polygon([(tx, gy - int(h * 0.5)), (tx + int(w * 0.3), gy),
               (tx - int(w * 0.02), gy)], fill=(245, 242, 230))
    d.rectangle([tx + int(w * 0.1), gy - int(h * 0.22),
                 tx + int(w * 0.1) + 14, gy - int(h * 0.22) + 5], fill=(200, 30, 30))
    d.rectangle([tx + int(w * 0.1) + 4, gy - int(h * 0.22) - 4,
                 tx + int(w * 0.1) + 10, gy - int(h * 0.22) + 9], fill=(200, 30, 30))
    # ambulance-ish van
    d.rectangle([x + int(w * 0.66), gy - 12, x + int(w * 0.92), gy], fill=(255, 255, 255))
    d.rectangle([x + int(w * 0.66) + 4, gy - 9, x + int(w * 0.66) + 10, gy - 4],
                fill=(200, 30, 30))


def sc_gaza(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (250, 200, 140), (230, 170, 110))
    sun(d, x + int(w * 0.82), y + int(h * 0.2), max(6, h // 10),
        color=(255, 220, 130))
    gy = y + h - int(h * 0.12)
    d.rectangle([x, gy, x + w, y + h], fill=(110, 95, 75))
    skyline(d, x, y + int(h * 0.25), int(w * 0.7), int(h * 0.6),
            (100, 85, 70), seed=7)
    # minaret
    mx = x + int(w * 0.8)
    d.rectangle([mx - 3, y + int(h * 0.18), mx + 3, gy], fill=(140, 120, 95))
    d.polygon([(mx - 6, y + int(h * 0.18)), (mx, y + int(h * 0.08)),
               (mx + 6, y + int(h * 0.18))], fill=(90, 70, 55))
    smoke(d, x + int(w * 0.3), y + int(h * 0.3), max(9, h // 7))


def sc_fines(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (215, 230, 245), (245, 242, 230))
    gy = y + h - int(h * 0.12)
    d.rectangle([x, gy, x + w, y + h], fill=(100, 110, 120))
    # parliament-like building
    bx = x + int(w * 0.1)
    d.rectangle([bx, y + int(h * 0.42), bx + int(w * 0.8), gy], fill=(180, 175, 160))
    d.polygon([(bx - 4, y + int(h * 0.42)), (bx + int(w * 0.4), y + int(h * 0.22)),
               (bx + int(w * 0.8) + 4, y + int(h * 0.42))], fill=(150, 140, 125))
    for i in range(5):
        cx = bx + int(w * (0.16 + i * 0.14))
        d.rectangle([cx - 3, y + int(h * 0.46), cx + 3, gy - 4], fill=(245, 240, 225))
    # chip + percent
    d.rectangle([x + int(w * 0.68), y + int(h * 0.14), x + int(w * 0.68) + 22,
                 y + int(h * 0.14) + 22], fill=(30, 60, 120))
    for k in range(3):
        d.line([(x + int(w * 0.68) + 4 + k * 7, y + int(h * 0.14) - 4),
                (x + int(w * 0.68) + 4 + k * 7, y + int(h * 0.14))],
               fill=(30, 60, 120), width=2)
    d.text((x + int(w * 0.68) + 4, y + int(h * 0.14) + 5), "%",
           font=F_SANS_B(13), fill=(255, 255, 255))


def sc_lula(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (200, 225, 245), (250, 244, 225))
    gy = y + h - int(h * 0.12)
    d.rectangle([x, gy, x + w, y + h], fill=(90, 130, 70))
    # Brasilia congress: twin towers + dome + bowl
    bx = x + int(w * 0.18)
    d.rectangle([bx, y + int(h * 0.2), bx + 8, gy], fill=(235, 230, 215))
    d.rectangle([bx + 14, y + int(h * 0.2), bx + 22, gy], fill=(235, 230, 215))
    d.rectangle([bx, y + int(h * 0.34), bx + 22, y + int(h * 0.34) + 4],
                fill=(220, 215, 200))
    d.pieslice([bx + int(w * 0.3), gy - 22, bx + int(w * 0.3) + 26, gy + 2],
               180, 360, fill=(235, 230, 215))
    d.polygon([(bx + int(w * 0.52), gy), (bx + int(w * 0.52) + 24, gy),
               (bx + int(w * 0.52) + 12, gy - 14)], fill=(235, 230, 215))
    # rising chart arrow
    pts = [(x + int(w * 0.6), gy - 8), (x + int(w * 0.72), gy - 22),
           (x + int(w * 0.82), gy - 14), (x + int(w * 0.94), gy - 30)]
    d.line(pts, fill=(0, 140, 60), width=3)
    d.polygon([(x + int(w * 0.94), gy - 30), (x + int(w * 0.94) - 8, gy - 28),
               (x + int(w * 0.94) - 2, gy - 20)], fill=(0, 140, 60))


def sc_jets(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (140, 180, 225), (225, 235, 245))
    sun(d, x + int(w * 0.85), y + int(h * 0.18), max(5, h // 11),
        color=(255, 240, 190))
    # sea + island
    sea = y + int(h * 0.72)
    d.rectangle([x, sea, x + w, y + h], fill=(40, 110, 170))
    ix = x + int(w * 0.62)
    d.ellipse([ix - 22, sea - 8, ix + 22, sea + 6], fill=(90, 140, 90))
    d.polygon([(ix - 14, sea - 8), (ix, sea - 26), (ix + 14, sea - 8)],
              fill=(70, 120, 70))
    # fighter jet silhouette
    jx, jy = x + int(w * 0.3), y + int(h * 0.34)
    d.polygon([(jx - 26, jy), (jx + 18, jy - 6), (jx + 30, jy),
               (jx + 18, jy + 6)], fill=(60, 60, 75))
    d.polygon([(jx - 6, jy - 4), (jx - 2, jy - 16), (jx + 4, jy - 4)],
              fill=(60, 60, 75))
    d.polygon([(jx - 6, jy + 4), (jx - 2, jy + 14), (jx + 4, jy + 4)],
              fill=(60, 60, 75))
    # alert triangle
    ax, ay = x + int(w * 0.82), y + int(h * 0.55)
    d.polygon([(ax, ay - 12), (ax + 11, ay + 8), (ax - 11, ay + 8)],
              fill=(230, 180, 0))
    d.text((ax - 2, ay - 6), "!", font=F_SANS_B(11), fill=(0, 0, 0))


def sc_solomons(d, x, y, w, h):
    vgrad(d, x, y, x + w, y + h, (150, 205, 240), (235, 245, 250))
    sun(d, x + int(w * 0.8), y + int(h * 0.18), max(6, h // 10))
    sea = y + int(h * 0.66)
    d.rectangle([x, sea, x + w, y + h], fill=(30, 120, 170))
    # island + palm
    ix = x + int(w * 0.3)
    d.ellipse([ix - 30, sea - 6, ix + 30, sea + 8], fill=(220, 200, 130))
    d.line([(ix, sea - 6), (ix, sea - 30)], fill=(110, 80, 40), width=3)
    for ang, ln in ((-50, 16), (-15, 18), (20, 18), (55, 15)):
        import math as _m
        ex = ix + int(ln * _m.sin(_m.radians(ang)))
        ey = sea - 30 - int(ln * _m.cos(_m.radians(ang)) * 0.6)
        d.line([(ix, sea - 30), (ex, ey)], fill=(40, 130, 60), width=2)
    # treaty paper + pen
    px, py = x + int(w * 0.62), y + int(h * 0.4)
    d.rectangle([px, py, px + 26, py + 34], fill=(255, 255, 255),
                outline=(120, 120, 120))
    for k in range(3):
        d.line([(px + 4, py + 8 + k * 7), (px + 22, py + 8 + k * 7)],
               fill=(120, 120, 120), width=1)
    d.line([(px + 26, py + 34), (px + 36, py + 18)], fill=(30, 60, 120), width=2)


SCENES = {
    "quake": sc_quake, "tanker": sc_tanker, "court": sc_court,
    "shanghai": sc_shanghai, "carbomb": sc_carbomb,
    "zaporizhzhia": sc_zaporizhzhia, "sanofi": sc_sanofi,
    "tiangong": sc_tiangong, "ebola": sc_ebola, "gaza": sc_gaza,
    "fines": sc_fines, "lula": sc_lula, "jets": sc_jets,
    "solomons": sc_solomons,
}


# ---------------------------------------------------------------- drawing
def badge_pill(d, x, y, badge):
    """Small colored badge label; returns its width."""
    f = F_SANS_B(8)
    w = int(text_w(d, badge, f)) + 10
    d.rounded_rectangle([x, y, x + w, y + 13], radius=6,
                        fill=BADGE_COLORS[badge])
    d.text((x + 5, y + 2), badge, font=f, fill=(255, 255, 255))
    return w


def feature_card(d, x, y, w, h, st, big):
    d.rectangle([x, y, x + w, y + h], fill=(255, 252, 244),
                outline=(210, 200, 175))
    scene_h = 78 if big else 54
    SCENES[st["scene"]](d, x + 1, y + 1, w - 2, scene_h)
    _bf = F_SANS_B(8)
    _bw = int(text_w(d, st["badge"], _bf)) + 10
    badge_pill(d, x + w - _bw - 5, y + 5, st["badge"])
    ty = y + scene_h + 5
    tag_f = F_SANS_B(8)
    d.text((x + 6, ty), st["band"], font=tag_f,
           fill=REGION_COLORS[st["band"]])
    d.text((x + 6 + text_w(d, st["band"], tag_f) + 6, ty),
           "#" + str(st["n"]), font=F_SANS(8), fill=GREY)
    hy = ty + 12
    head_f = F_SERIF_B(14 if big else 11)
    for i, ln in enumerate(wrap_max(d, st["head"], head_f, w - 12, 2)):
        d.text((x + 6, hy + i * (17 if big else 13)), ln, font=head_f, fill=INK)
    by = hy + (2 * (17 if big else 13))
    body_f = F_SANS(10 if big else 9)
    blines = wrap_max(d, st["body"], body_f, w - 12, 2)
    for i, ln in enumerate(blines):
        d.text((x + 6, by + i * (12 if big else 11)), ln, font=body_f,
               fill=(60, 60, 70))
    d.text((x + 6, y + h - 12), st["src"], font=F_SANS(8), fill=GREY)


def hero_band(d, x, y, w, h):
    SCENES["quake"](d, x, y, w, h)
    # top-left label + top-right badge
    lab = "ASIA \u00b7 THE LEAD STORY"
    lf = F_SANS_B(9)
    lw = int(text_w(d, lab, lf)) + 12
    d.rectangle([x, y, x + lw, y + 16], fill=(18, 38, 74))
    d.text((x + 6, y + 3), lab, font=lf, fill=(255, 210, 90))
    _bf = F_SANS_B(8)
    _bw = int(text_w(d, HERO["badge"], _bf)) + 10
    badge_pill(d, x + w - _bw - 6, y + 2, HERO["badge"])
    # bottom caption band
    band_h = 56
    d.rectangle([x, y + h - band_h, x + w, y + h], fill=(18, 38, 74))
    hf = F_SERIF_B(25)
    d.text((x + 10, y + h - band_h + 5), HERO["head"], font=hf,
           fill=(255, 255, 255))
    sf = F_SANS(11)
    d.text((x + 10, y + h - 15), HERO["sub"], font=sf, fill=(220, 220, 220))
    srf = F_SANS(9)
    sw = text_w(d, HERO["src"], srf)
    d.text((x + w - sw - 10, y + h - 14), HERO["src"], font=srf,
           fill=(200, 200, 200))


def brief_line(d, x, y, max_w, st):
    """One brief line; returns nothing. Truncates the sub first, then head."""
    nf = F_SANS_B(9)
    hf = F_SANS_B(9)
    rf = F_SANS(9)
    num = str(st["n"])
    badge = st["badge"]
    bf = F_SANS_B(8)
    bcol = BADGE_COLORS[badge]
    bw = int(text_w(d, badge, bf)) + 8
    # available width excludes number, badge pill
    head = st["head"]
    sub = st["sub"]
    src = st["src"]
    num_w = text_w(d, num + "  ", nf)
    avail = max_w - num_w - bw - 6
    full = head + " \u2014 " + sub + " \u00b7 " + src
    if text_w(d, full, hf) > avail:
        full = head + " \u00b7 " + src
    if text_w(d, full, hf) > avail:
        while full and text_w(d, full + "\u2026", hf) > avail:
            full = full[:-1]
        full = full + "\u2026"
    d.text((x, y), num, font=nf, fill=RED)
    d.text((x + num_w, y), full, font=hf, fill=INK)
    bx = x + max_w - bw
    d.rounded_rectangle([bx, y, bx + bw, y + 11], radius=5, fill=bcol)
    d.text((bx + 4, y + 1), badge, font=bf, fill=(255, 255, 255))


# display nudges for crowded map spots (story n -> (lon, lat))
MAP_NUDGE = {
    6: (0.0, 48.86), 22: (6.5, 51.8), 23: (1.0, 47.0), 24: (8.0, 49.5),
    26: (36.0, 32.8), 32: (-72.5, 41.5), 36: (-46.0, -14.5),
    38: (150.6, -34.2), 39: (147.8, -36.4),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(205, 225, 240),
                outline=(180, 180, 160))
    geo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "countries.geo.json")
    try:
        with open(geo_path, "r", encoding="utf-8") as fh:
            geo = json.load(fh)
        for feat in geo["features"]:
            geom = feat["geometry"]
            polys = []
            if geom["type"] == "Polygon":
                polys = [geom["coordinates"]]
            elif geom["type"] == "MultiPolygon":
                polys = geom["coordinates"]
            for poly in polys:
                for ring in poly:
                    pts = []
                    for lon, lat in ring:
                        px = x + (lon + 180.0) / 360.0 * w
                        py = y + (90.0 - lat) / 180.0 * h
                        pts.append((px, py))
                    if len(pts) > 2:
                        d.polygon(pts, fill=(226, 224, 208),
                                  outline=(175, 172, 150))
    except Exception:
        pass

    def proj(lon, lat):
        return (x + (lon + 180.0) / 360.0 * w,
                y + (90.0 - lat) / 180.0 * h)

    # hero star (Taplejung, Nepal)
    hx, hy = proj(87.9, 27.4)
    d.ellipse([hx - 7, hy - 7, hx + 7, hy + 7], fill=(200, 160, 20),
              outline=(120, 90, 0))
    d.text((hx - 4, hy - 6), "\u2605", font=F_SANS_B(9), fill=(255, 255, 255))
    # feature pins 1-13
    for st in FEATURES:
        lon, lat = MAP_NUDGE.get(st["n"], (st["lon"], st["lat"]))
        px, py = proj(lon, lat)
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=RED,
                  outline=(255, 255, 255))
        tf = F_SANS_B(7)
        tw = text_w(d, str(st["n"]), tf)
        d.text((px - tw / 2, py - 5), str(st["n"]), font=tf,
               fill=(255, 255, 255))
    # brief dots 14-39
    for st in BRIEFS:
        lon, lat = MAP_NUDGE.get(st["n"], (st["lon"], st["lat"]))
        px, py = proj(lon, lat)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=NAVY)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # top strip
    lf = F_SANS_B(10)
    d.text((MARGIN, 4), "ONE DAY OF WORLD NEWS ON ONE PAGE", font=lf, fill=RED)
    right = "40 STORIES \u00b7 9 REGIONS \u00b7 EVERY ONE DATED TUE 24 NOV 2026"
    d.text((W - MARGIN - text_w(d, right, lf), 4), right, font=lf, fill=RED)
    # masthead
    mf = F_SERIF_B(52)
    title = "Tuesday 24 November 2026"
    d.text(((W - text_w(d, title, mf)) / 2, 20), title, font=mf, fill=INK)
    d.line([(MARGIN, 80), (W - MARGIN, 80)], fill=INK, width=2)
    # kicker
    kf = F_SERIF(15)
    kick = ("Fourth tanker hit in Hormuz \u00b7 Huawei guilty on 10 of 12 counts "
            "\u00b7 Shanghai party boss probed")
    d.text(((W - text_w(d, kick, kf)) / 2, 86), kick, font=kf, fill=RED)
    # region strip
    rx, ry, rh = MARGIN, 106, 20
    cw = (W - 2 * MARGIN - 8 * 6) // 9
    for i, (label, count) in enumerate(REGIONS):
        cx = rx + i * (cw + 6)
        d.rounded_rectangle([cx, ry, cx + cw, ry + rh], radius=4,
                            fill=REGION_COLORS[label])
        tf = F_SANS_B(9)
        txt = "%s %d" % (label, count)
        d.text((cx + (cw - text_w(d, txt, tf)) / 2, ry + 5), txt, font=tf,
               fill=(255, 255, 255))
    # UTC strip
    d.rectangle([MARGIN, 130, W - MARGIN, 150], fill=NAVY)
    uf = F_SANS(10)
    utc = ("UTC    01:32 Nepal quake  \u00b7  02:30 Colombia blast  \u00b7  "
           "14:28 Lula fiscal plan  \u00b7  16:38 Hormuz 4th tanker  \u00b7  "
           "22:27 Huawei verdict")
    d.text(((W - text_w(d, utc, uf)) / 2, 135), utc, font=uf,
           fill=(255, 255, 255))
    # hero
    hero_band(d, MARGIN, 154, W - 2 * MARGIN, 140)
    # feature cards: row 1 big x3, rows 2-3 small x5
    big_w, big_gap = 330, 7
    for i, st in enumerate(FEATURES[:3]):
        feature_card(d, MARGIN + i * (big_w + big_gap), 300, big_w, 168, st,
                     big=True)
    sm_w, sm_gap = 196, 6
    for row, chunk in enumerate((FEATURES[3:8], FEATURES[8:13])):
        for i, st in enumerate(chunk):
            feature_card(d, MARGIN + i * (sm_w + sm_gap), 474 + row * 138,
                         sm_w, 132, st, big=False)
    # bottom section headers
    hf = F_SANS_B(11)
    d.text((MARGIN, 748), "ALSO ON TUESDAY 24 NOVEMBER 2026", font=hf, fill=INK)
    d.text((700, 748), "WHERE IT HAPPENED", font=hf, fill=INK)
    d.line([(MARGIN, 763), (690, 763)], fill=RED, width=2)
    d.line([(700, 763), (W - MARGIN, 763)], fill=RED, width=2)
    # briefs: two columns of 13
    col_w = 336
    for col in range(2):
        for r in range(13):
            st = BRIEFS[col * 13 + r]
            brief_line(d, MARGIN + col * (col_w + 8), 768 + r * 14, col_w, st)
    # map + legend
    draw_map(d, 700, 768, W - MARGIN - 700, 148)
    lg = F_SANS(8)
    d.text((700, 922), "Pins 1\u201313 pictured  \u00b7  dots 14\u201339  \u00b7  \u2605 hero",
           font=lg, fill=GREY)
    d.text((700, 934), "Numbers follow the story order on this page.",
           font=lg, fill=GREY)
    # date check footer
    d.rectangle([MARGIN, 952, W - MARGIN, 996], fill=(250, 232, 226))
    d.rectangle([MARGIN, 952, MARGIN + 4, 996], fill=RED)
    df = F_SANS(9)
    dlines = wrap(d, DATE_CHECK, df, W - 2 * MARGIN - 16)
    for i, ln in enumerate(dlines[:4]):
        d.text((MARGIN + 10, 955 + i * 11), ln, font=df, fill=(90, 20, 20))
    # credit line
    cf = F_SANS(8)
    credit = ("HOW SURE: CONFIRMED 2+ outlets \u00b7 OFFICIAL agency / court on "
              "record \u00b7 REPORTED single outlet \u2014 Pictures and map drawn "
              "in code for this page; no photographs. \u00b7 1024\u00d71024 \u00b7 "
              "news-image-20261124")
    d.text(((W - text_w(d, credit, cf)) / 2, 1002), credit, font=cf, fill=GREY)
    return img


def main():
    img = build()
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or here
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, format="JPEG", quality=90)
    import hashlib
    with open(out_path, "rb") as fh:
        data = fh.read()
    print("entry.png bytes=%d sha256=%s" % (len(data),
                                            hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
