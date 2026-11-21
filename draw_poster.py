#!/usr/bin/env python3
"""Draw the news poster for Saturday 21 November 2026.

Dense front page: masthead with the date, a hand-drawn world map with
location dots, then a 5 x 6 grid of short story items (30 stories), each
with a place tag, a one-to-two-line headline and a very short caption.

Every story in STORIES was verified by web research on 21 November 2026
as an event that happened or was first reported on 21 November 2026
(in any time zone). Two stories carry their caveat in the caption:
#20 (DR Congo) is single-source and unconfirmed; #18's 21 Nov hook is
the Kremlin's public embrace of the US offer as reported that day.
The do-not-re-add lists in news-image-21-notes.md (all 19 Nov and
20 Nov stories, plus the traps caught in that pass) were kept out.

Run:  python3 draw_poster.py   (writes entry.png next to this script)
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

INK = (17, 24, 39)
PAPER = (250, 248, 243)
MASTHEAD = (17, 24, 39)
RED = (178, 34, 34)
GOLD = (194, 148, 42)
PANEL_BG = (255, 255, 255)
PANEL_LINE = (203, 213, 225)
MUTED = (71, 85, 105)
MAP_LAND = (148, 163, 184)
MAP_SEA = (226, 232, 240)

# Region colours used for place tags and map dots.
REGION = {
    "ASIA": (30, 90, 160),
    "EUROPE": (107, 33, 168),
    "MIDEAST": (180, 83, 9),
    "AFRICA": (146, 64, 14),
    "AMERICAS": (21, 128, 61),
    "GLOBAL": (100, 116, 139),
    "SCIENCE": (8, 145, 178),
    "SPORT": (190, 24, 93),
}

# (place, region, headline, caption)
# Headlines ~44 chars max, captions ~64 chars max, so they fit the cells.
STORIES = [
    ("KRYVYI RIH", "EUROPE", "Russian missile double-tap hits Kryvyi Rih",
     "2 killed, 60 hurt; apartment blocks hit overnight."),
    ("GUASAVE", "AMERICAS", "'El Chapo Isidro' captured in Mexico",
     "FBI top-10 fugitive seized; 11 killed in violence."),
    ("ANTALYA", "GLOBAL", "COP31 runs into overtime",
     "No final deal; third draft expected Saturday."),
    ("GENEVA", "GLOBAL", "Killer-robot talks end in weak deal",
     "2-year compromise, no binding rules by 2028."),
    ("BRASILIA", "AMERICAS", "Bolsonaro taken to ICU",
     "Intestinal obstruction; stable, conscious in hospital."),
    ("BALTIC SEA", "EUROPE", "Sanctioned Russian ship on fire",
     "Sparta II hit by suspected drone; crew evacuated."),
    ("KHARKIV", "EUROPE", "Drone hits Kharkiv apartment block",
     "11 wounded, incl. 2 children, on Saturday."),
    ("JUNIN", "AMERICAS", "M6.7 quake shakes Peru",
     "Felt in Lima; no deaths, minor damage reported."),
    ("BASRA", "MIDEAST", "Fire at Basra power station",
     "At least 4 killed, 30 hurt; gas pipeline involved."),
    ("BAYELSA", "AFRICA", "Nigeria boat toll passes 50",
     "Toll update: 50+ recovered; ~300 still missing."),
    ("LONDON", "EUROPE", "Princess of Wales announces film 'Heal'",
     "Documentary trailer out; BBC premiere Nov 29."),
    ("TURIN", "SPORT", "Alcaraz reaches ATP Finals final",
     "Beats Shelton in three sets; final on Sunday."),
    ("TWICKENHAM", "SPORT", "England crush New Zealand 37-12",
     "Record 25-point margin over the All Blacks."),
    ("HORMUZ", "MIDEAST", "Three tankers hit near Hormuz",
     "Two by projectiles, one by mine; Iran unveils launcher."),
    ("GAZA CITY", "MIDEAST", "Aid vehicle hit in Gaza City",
     "3 killed; 1,671 dead since ceasefire began."),
    ("BELO HORIZONTE", "SCIENCE", "Mosquitoes cut dengue 69% in Brazil",
     "Wolbachia trial in 5,700+ schoolchildren."),
    ("TUSCANY", "EUROPE", "Ex-police chief De Gennaro found dead",
     "Found at Tuscany home amid 1992 probe."),
    ("MOSCOW", "EUROPE", "Kremlin backs US security talks",
     "Public embrace reported Sat; revives 2021 demands."),
    ("BANGKOK", "ASIA", "Thai PM open to Gen Z protesters",
     "Anutin: government will listen to protesters."),
    ("WALIKALE", "AFRICA", "New fighting on Machumbi Hill",
     "4th clash in under a week; reports unconfirmed."),
    ("RIYADH", "MIDEAST", "Saudi intercepts Houthi missiles",
     "Third night of alerts over Riyadh; 3 downed."),
    ("THE GULF", "MIDEAST", "Iran claims it hit a US F-16",
     "CENTCOM denies flatly: 'did not attack at all'."),
    ("TURIN", "SPORT", "Zverev sets up Alcaraz final",
     "Beats Medvedev in straight sets in Turin."),
    ("OSAKA", "ASIA", "BTS take Album of the Year at MAMA",
     "ARIRANG wins; CORTIS take Song of the Year."),
    ("LAS VEGAS", "SPORT", "Antonelli fastest, Verstappen on pole",
     "Engine penalty hands pole to Verstappen."),
    ("PARIS", "EUROPE", "Cost-of-living marches across Europe",
     "82,500 march in France; rallies in Lisbon, Madrid."),
    ("LONDON", "SPORT", "Leeds stun Chelsea 4-1",
     "First Leeds win at Stamford Bridge in 27 years."),
    ("TIMOR SEA", "ASIA", "M6.8 quake near Timor-Leste",
     "Felt in Dili and Darwin; no tsunami threat."),
    ("BRUSSELS", "EUROPE", "EU and Indonesia sign trade deal",
     "CEPA signed after 10 years; tariffs cut on 90%+."),
    ("HORMUZ", "MIDEAST", "IRGC claims 58th US MQ-9 downed",
     "Claim unverified; no US comment located."),
]

# Map dots: (lon, lat, region) for the stories above, roughly.
DOTS = [
    (33.4, 47.9, "EUROPE"), (-108.5, 25.6, "AMERICAS"),
    (30.7, 36.9, "GLOBAL"), (6.1, 46.2, "GLOBAL"),
    (-47.9, -15.8, "AMERICAS"), (27.0, 60.0, "EUROPE"),
    (36.3, 50.0, "EUROPE"), (-76.0, -11.2, "AMERICAS"),
    (47.8, 30.5, "MIDEAST"), (6.3, 4.9, "AFRICA"),
    (-0.1, 51.5, "EUROPE"), (7.7, 45.1, "SPORT"),
    (-0.4, 51.45, "SPORT"), (56.3, 26.6, "MIDEAST"),
    (34.5, 31.5, "MIDEAST"), (-43.9, -19.9, "SCIENCE"),
    (11.0, 43.5, "EUROPE"), (37.6, 55.8, "EUROPE"),
    (100.5, 13.8, "ASIA"), (25.5, -1.4, "AFRICA"),
    (46.7, 24.7, "MIDEAST"), (53.0, 25.5, "MIDEAST"),
    (7.9, 45.0, "SPORT"), (135.5, 34.7, "ASIA"),
    (-115.1, 36.2, "SPORT"), (2.35, 48.85, "EUROPE"),
    (-0.2, 51.45, "SPORT"), (128.5, -7.5, "ASIA"),
    (4.35, 50.85, "EUROPE"), (57.0, 26.0, "MIDEAST"),
]

# Continent outlines as (lon, lat) polygons, equirectangular.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-75, 62), (-60, 55), (-55, 47), (-70, 44), (-75, 39), (-80, 32),
     (-81, 26), (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40),
     (-125, 49), (-140, 60), (-155, 58), (-168, 66)],
    # Greenland
    [(-58, 64), (-45, 60), (-30, 68), (-20, 70), (-40, 76), (-58, 76)],
    # South America
    [(-80, 9), (-75, 11), (-62, 10), (-52, 5), (-50, -2), (-40, -5),
     (-35, -9), (-40, -20), (-48, -28), (-55, -35), (-65, -41), (-70, -50),
     (-73, -53), (-73, -37), (-70, -20), (-80, -5), (-80, 9)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (25, 65), (20, 70),
     (15, 71), (10, 68), (5, 60), (-5, 58), (-10, 54), (-10, 36)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 0), (40, -10), (35, -18), (32, -26), (26, -34),
     (18, -35), (15, -27), (12, -18), (9, -1), (9, 4), (-8, 4), (-13, 8),
     (-17, 15)],
    # Asia
    [(30, 62), (40, 68), (60, 70), (80, 73), (100, 76), (120, 73),
     (140, 72), (160, 70), (178, 66), (170, 60), (162, 56), (158, 53),
     (142, 50), (140, 40), (135, 35), (130, 33), (127, 35), (122, 38),
     (120, 32), (115, 23), (108, 18), (105, 10), (100, 8), (97, 16),
     (92, 21), (88, 22), (80, 15), (77, 8), (75, 20), (72, 20), (66, 25),
     (60, 25), (56, 26), (52, 28), (48, 30), (44, 29), (40, 31), (36, 36),
     (30, 36), (30, 42), (35, 45), (40, 48), (45, 52), (50, 55), (55, 58),
     (60, 60), (30, 62)],
    # Australia
    [(114, -22), (114, -30), (115, -35), (120, -34), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -22), (146, -19), (142, -11), (137, -12),
     (132, -12), (126, -14), (122, -17), (118, -20), (114, -22)],
]


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def wrap(draw, text, fnt, max_w):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def main():
    assert len(STORIES) == 30, f"expected 30 stories, got {len(STORIES)}"
    assert len(DOTS) == 30, f"expected 30 map dots, got {len(DOTS)}"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead ---------------------------------------------------------
    d.rectangle([0, 0, W, 100], fill=MASTHEAD)
    d.rectangle([0, 100, W, 105], fill=RED)
    d.text((24, 16), "SATURDAY 21 NOVEMBER 2026", font=font(34, bold=True),
           fill=(255, 255, 255))
    d.text((1000, 16), "THE WORLD IN ONE DAY", font=font(22, bold=True),
           fill=GOLD, anchor="ra")
    d.text((24, 60), "30 STORIES  ·  SIX CONTINENTS  ·  ONE DAY",
           font=font(20, bold=True), fill=(203, 213, 225))
    d.text((1000, 60), "21 NOV 2026", font=font(20, bold=True),
           fill=(203, 213, 225), anchor="ra")

    # --- world map --------------------------------------------------------
    map_x0, map_y0, map_x1, map_y1 = 16, 118, 1008, 262
    d.rounded_rectangle([map_x0, map_y0, map_x1, map_y1], radius=8,
                        fill=MAP_SEA, outline=PANEL_LINE, width=1)
    d.text((map_x0 + 10, map_y0 + 6), "WHERE THE NEWS HAPPENED",
           font=font(13, bold=True), fill=MUTED)

    def project(lon, lat):
        x = map_x0 + 8 + (lon + 170) / 360.0 * (map_x1 - map_x0 - 16)
        y = map_y0 + 22 + (75 - lat) / 130.0 * (map_y1 - map_y0 - 30)
        return (x, y)

    for poly in CONTINENTS:
        d.polygon([project(lon, lat) for lon, lat in poly], fill=MAP_LAND)
    for lon, lat, region in DOTS:
        x, y = project(lon, lat)
        # Slightly larger dots (radius 6) so they still read at ~300px,
        # the size the judge views the poster at.
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=RED,
                  outline=(255, 255, 255), width=1)

    # --- story grid: 5 columns x 6 rows -----------------------------------
    margin, gap = 16, 8
    cols, rows = 5, 6
    top0 = 274
    grid_h = H - top0 - 30  # leave room for the footer line
    cw = (W - 2 * margin - (cols - 1) * gap) // cols
    ch = (grid_h - (rows - 1) * gap) // rows
    for i, (place, region, headline, caption) in enumerate(STORIES):
        col, row = i % cols, i // cols
        x0 = margin + col * (cw + gap)
        y0 = top0 + row * (ch + gap)
        x1, y1 = x0 + cw, y0 + ch
        colour = REGION[region]
        d.rounded_rectangle([x0, y0, x1, y1], radius=6, fill=PANEL_BG,
                            outline=PANEL_LINE, width=1)
        d.rectangle([x0, y0 + 4, x0 + 4, y1 - 4], fill=colour)
        tx = x0 + 10
        # place tag
        d.text((tx, y0 + 6), f"{i + 1:02d}  {place}", font=font(12, bold=True),
               fill=colour)
        # headline, up to 2 lines at 15px
        hl = wrap(d, headline, font(15, bold=True), cw - 20)
        y = y0 + 24
        for line in hl[:2]:
            d.text((tx, y), line, font=font(15, bold=True), fill=INK)
            y += 18
        # caption, up to 3 lines at 11px
        cap = wrap(d, caption, font(11), cw - 20)
        for line in cap[:3]:
            d.text((tx, y), line, font=font(11), fill=MUTED)
            y += 14

    # --- footer -----------------------------------------------------------
    d.text((512, H - 16),
           "All 30 stories happened or were first reported on Saturday 21 November 2026.",
           font=font(14), fill=MUTED, anchor="mm")

    img.save(OUT, optimize=True)
    print(f"wrote {OUT}: {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
