"""Draw the front page of THE WORLD TODAY for Sunday 22 November 2026.

Deterministic: fixed fonts, fixed coordinates, no randomness, no clock,
no network. Renders a 1024x1024 PNG with Pillow and writes it next to
this file as news_image.png. Run: python3 render.py
"""

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
EDGE = 36
INNER = SIDE - 2 * EDGE  # 952 px of content

PAPER = (248, 244, 234)
INK = (20, 20, 20)
FAINT = (118, 108, 92)
SOFT = (92, 86, 74)
CRIMSON = (176, 32, 32)
MIDNIGHT = (14, 24, 46)
OCEAN = (44, 90, 126)
SAND = (214, 162, 46)
LEAF = (72, 138, 72)

FONTS = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONTS + "DejaVuSerif.ttf"
SERIF_BOLD = FONTS + "DejaVuSerif-Bold.ttf"
SANS = FONTS + "DejaVuSans.ttf"
SANS_BOLD = FONTS + "DejaVuSans-Bold.ttf"


def face(path, size):
    return ImageFont.truetype(path, size)


def text_wrap(draw, words, fnt, width):
    """Break a string into lines that fit width pixels."""
    out = []
    for chunk in words.split("\n"):
        parts = chunk.split()
        if not parts:
            out.append("")
            continue
        line = parts[0]
        for word in parts[1:]:
            test = line + " " + word
            if draw.textlength(test, font=fnt) <= width:
                line = test
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def block(draw, x, y, words, fnt, width, step, colour=INK):
    """Draw a wrapped block of text; return the y just below it."""
    for line in text_wrap(draw, words, fnt, width):
        draw.text((x, y), line, font=fnt, fill=colour)
        y += step
    return y


def banner(draw, x, y, words, size, width, step=None):
    """Draw a bold serif headline; return the y just below it."""
    fnt = face(SERIF_BOLD, size)
    step = step or int(size * 1.1)
    return block(draw, x, y, words, fnt, width, step)


def tag(draw, x, y, words, width, colour=CRIMSON):
    """Section label in small caps with a hairline under it."""
    fnt = face(SANS_BOLD, 15)
    draw.text((x, y), words.upper(), font=fnt, fill=colour)
    y += 22
    draw.line([(x, y), (x + width, y)], fill=FAINT, width=1)
    return y + 8


def rule_across(draw, y, weight=2):
    draw.line([(EDGE, y), (SIDE - EDGE, y)], fill=INK, width=weight)
    return y + weight


def art_box(canvas, scene, x, y, w, h):
    """Paint a scene on its own layer, clipped to its box."""
    layer = Image.new("RGB", (w, h), PAPER)
    pen = ImageDraw.Draw(layer)
    scene(pen, 0, 0, w, h)
    canvas.paste(layer, (x, y))


def raid_scene(pen, x, y, w, h):
    """Night raid over the Sinaloa desert: helicopter, beam, ridge."""
    pen.rectangle([x, y, x + w, y + h], fill=MIDNIGHT)
    for sx, sy in [(30, 14), (120, 30), (260, 12), (420, 26), (560, 10),
                   (700, 28), (840, 12), (920, 26), (180, 44), (640, 42)]:
        pen.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                    fill=(225, 225, 205))
    pen.ellipse([x + w - 130, y + 10, x + w - 94, y + 46], fill=(235, 225, 200))
    hx, hy = x + 300, y + 46
    pen.ellipse([hx - 26, hy - 12, hx + 26, hy + 12], fill=(8, 12, 18))
    pen.rectangle([hx - 60, hy - 16, hx + 60, hy - 12], fill=(8, 12, 18))
    pen.rectangle([hx + 22, hy - 4, hx + 74, hy + 4], fill=(8, 12, 18))
    pen.polygon([(hx - 10, hy + 8), (hx - 46, y + h - 30),
                 (hx + 34, y + h - 30)], fill=(255, 244, 190))
    pen.polygon([(hx - 46, y + h - 30), (hx + 34, y + h - 30),
                 (hx + 34, y + h - 22), (hx - 46, y + h - 22)],
                fill=(255, 244, 190))
    ridge = h - 26
    pen.polygon([(x, y + h), (x, y + ridge), (x + 180, y + ridge - 16),
                 (x + 380, y + ridge + 2), (x + 620, y + ridge - 12),
                 (x + w, y + ridge + 2), (x + w, y + h)], fill=(10, 16, 12))
    vx, vy = x + 700, y + h - 44
    pen.rectangle([vx, vy, vx + 64, vy + 16], fill=(16, 20, 16))
    pen.rectangle([vx + 12, vy - 12, vx + 44, vy], fill=(16, 20, 16))
    pen.ellipse([vx + 56, vy + 2, vx + 64, vy + 10], fill=(255, 220, 120))
    pen.ellipse([vx + 8, vy + 12, vx + 20, vy + 24], fill=(30, 30, 30))
    pen.ellipse([vx + 40, vy + 12, vx + 52, vy + 24], fill=(30, 30, 30))
    pen.text((x + 10, y + h - 20),
             "A helicopter searchlight sweeps the Sinaloa hills, Saturday night.",
             font=face(SANS, 12), fill=(205, 200, 185))


def lock_scene(pen, x, y, w, h):
    """A breached database: keypad grid and a broken padlock."""
    pen.rectangle([x, y, x + w, y + h], fill=(232, 228, 218))
    for r in range(2):
        for c in range(3):
            bx = x + 16 + c * 30
            by = y + 8 + r * 22
            pen.rectangle([bx, by, bx + 22, by + 16], outline=FAINT, width=1)
            pen.text((bx + 7, by + 2), str(r * 3 + c + 1),
                     font=face(SANS_BOLD, 11), fill=SOFT)
    lx, ly = x + w - 96, y + 8
    pen.arc([lx, ly, lx + 40, ly + 32], start=180, end=330, fill=CRIMSON,
            width=4)
    pen.arc([lx + 26, ly - 2, lx + 40, ly + 12], start=300, end=360,
            fill=CRIMSON, width=4)
    pen.rectangle([lx - 2, ly + 26, lx + 42, ly + 48], fill=CRIMSON)
    pen.ellipse([lx + 14, ly + 32, lx + 26, ly + 44], fill=PAPER)
    pen.text((x + 14, y + h - 15), "FBI crime database",
             font=face(SANS_BOLD, 12), fill=CRIMSON)


def summit_scene(pen, x, y, w, h):
    """Dawn over the Antalya talks: sun, globe, flags."""
    pen.rectangle([x, y, x + w, y + h], fill=(240, 234, 216))
    cx = x + w // 2
    for a in range(0, 360, 30):
        import math
        x1 = cx + 22 * math.cos(math.radians(a))
        y1 = y + 30 + 22 * math.sin(math.radians(a))
        x2 = cx + 32 * math.cos(math.radians(a))
        y2 = y + 30 + 32 * math.sin(math.radians(a))
        pen.line([(x1, y1), (x2, y2)], fill=SAND, width=2)
    pen.ellipse([cx - 15, y + 15, cx + 15, y + 45], fill=SAND)
    pen.ellipse([cx - 40, y + h - 34, cx + 40, y + h + 6], fill=OCEAN)
    pen.polygon([(cx - 28, y + h - 14), (cx - 6, y + h - 24),
                 (cx + 10, y + h - 8), (cx - 2, y + h + 2),
                 (cx - 22, y + h - 4)], fill=LEAF)
    for i, col in enumerate([(176, 32, 32), (44, 90, 126), (72, 138, 72),
                             (214, 162, 46)]):
        fx = x + 16 + i * 26
        pen.line([(fx, y + h - 26), (fx, y + h - 44)], fill=INK, width=2)
        pen.polygon([(fx, y + h - 44), (fx + 16, y + h - 39),
                     (fx, y + h - 34)], fill=col)


def city_scene(pen, x, y, w, h):
    """City skyline under a missile burst."""
    pen.rectangle([x, y, x + w, y + h], fill=(226, 224, 214))
    base = y + h - 12
    for bx, bw, bh in [(8, 34, 26), (48, 26, 40), (80, 40, 30),
                       (126, 30, 48), (162, 34, 24), (202, 28, 36),
                       (236, 40, 28)]:
        pen.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(60, 58, 52))
    bx, by = x + w - 42, y + 26
    for r, col in [(22, (255, 190, 60)), (15, (255, 140, 40)),
                   (9, (255, 230, 140))]:
        pen.ellipse([bx - r, by - r, bx + r, by + r], fill=col)
    for dx, dy in [(-30, -8), (-24, 12), (26, -12), (30, 10), (0, -24)]:
        pen.line([(bx, by), (bx + dx, by + dy)], fill=(255, 180, 60), width=2)


def river_scene(pen, x, y, w, h):
    """A capsized boat on a wide river."""
    pen.rectangle([x, y, x + w, y + h], fill=(206, 224, 232))
    pen.rectangle([x, y + h - 20, x + w, y + h], fill=OCEAN)
    cx, cy = x + w // 2, y + h - 34
    pen.pieslice([cx - 46, cy - 26, cx + 46, cy + 26], start=180, end=360,
                 fill=(70, 60, 50))
    pen.rectangle([cx - 46, cy - 4, cx + 46, cy + 4], fill=(70, 60, 50))
    for wy in (y + h - 14, y + h - 6):
        for wx in range(x + 8, x + w - 24, 40):
            pen.line([(wx, wy), (wx + 20, wy)], fill=(255, 255, 255), width=2)
    pen.ellipse([x + 18, y + 10, x + 54, y + 46], fill=SAND)


def march_scene(pen, x, y, w, h):
    """A street march: placards above a crowd."""
    pen.rectangle([x, y, x + w, y + h], fill=(238, 232, 220))
    for px, pw, ph, col in [(20, 64, 22, CRIMSON), (110, 58, 22, OCEAN),
                            (196, 66, 22, SAND)]:
        pen.line([(x + px + pw // 2, y + 8 + ph),
                  (x + px + pw // 2, y + 44)], fill=INK, width=2)
        pen.rectangle([x + px, y + 8, x + px + pw, y + 8 + ph], fill=col)
    for i in range(9):
        hx = x + 14 + i * 30
        pen.ellipse([hx, y + h - 26, hx + 18, y + h - 8], fill=(52, 48, 44))
        pen.polygon([(hx, y + h - 8), (hx + 18, y + h - 8),
                     (hx + 22, y + h), (hx - 4, y + h)], fill=(52, 48, 44))


def front_page():
    img = Image.new("RGB", (SIDE, SIDE), PAPER)
    pen = ImageDraw.Draw(img)

    # ---- masthead ----
    pen.text((EDGE, 16), "THE WORLD TODAY", font=face(SERIF_BOLD, 60),
             fill=INK)
    y = 90
    y = rule_across(pen, y, 3)
    y += 6
    line = "SUNDAY, 22 NOVEMBER 2026  ·  ONE DAY'S WORLD NEWS IN ONE PAGE"
    pen.text((EDGE, y), line, font=face(SANS_BOLD, 17), fill=INK)
    no = "No. 327"
    pen.text((SIDE - EDGE - pen.textlength(no, font=face(SANS_BOLD, 17)), y),
             no, font=face(SANS_BOLD, 17), fill=INK)
    y += 28
    y = rule_across(pen, y, 1)

    # ---- lead story ----
    y += 8
    y = banner(pen, EDGE, y, "MEXICO CAPTURES EL CHAPO ISIDRO", 44, INNER)
    y += 2
    y = block(pen, EDGE, y,
              "Cartel boss seized in Sinaloa raid on a U.S. tip; 11 killed as gunmen hit back",
              face(SERIF, 20), INNER, 26, SOFT)
    y += 8
    art_box(img, raid_scene, EDGE, y, INNER, 118)
    y += 118 + 6
    half_w = (INNER - 24) // 2
    left = ("Mexican special forces stormed a hideout in Sinaloa and "
            "captured Fausto Isidro Meza Flores, the cartel boss known "
            "as El Chapo Isidro, acting on intelligence from the United "
            "States. Video showed troops escorting him to an army vehicle.")
    right = ("Gunmen struck back across northern Mexico after the raid, "
             "killing 11 people in a burst of violence. Meza Flores, one "
             "of the FBI's most wanted, once led the Beltran-Leyva cartel "
             "and later ran his own trafficking group.")
    y1 = block(pen, EDGE, y, left, face(SERIF, 15), half_w, 19)
    y2 = block(pen, EDGE + half_w + 24, y, right, face(SERIF, 15), half_w, 19)
    y = max(y1, y2) + 6
    y = rule_across(pen, y, 1)
    y += 8

    # ---- middle row: FBI hack + COP31 ----
    y_top = y
    y = tag(pen, EDGE, y, "United States · Cyberattack", half_w)
    y = banner(pen, EDGE, y, "FBI CRIME DATABASE HACKED", 24, half_w, 26)
    y = block(pen, EDGE, y + 4,
              "President Trump confirmed the breach of the National Crime "
              "Information Center. The FBI is hunting for how intruders "
              "got in; what was taken is not yet clear.",
              face(SERIF, 14), half_w, 17)
    art_box(img, lock_scene, EDGE, y + 6, half_w, 64)
    left_end = y + 6 + 64
    yr = tag(pen, EDGE + half_w + 24, y_top, "Climate · Antalya", half_w)
    yr = banner(pen, EDGE + half_w + 24, yr, "COP31 NEARS A FINAL DEAL",
                24, half_w, 26)
    yr = block(pen, EDGE + half_w + 24, yr + 4,
               "The climate summit is close to agreement, its president "
               "said, offering a refined package after talks missed their "
               "deadline. The draft had dropped fossil fuels.",
               face(SERIF, 14), half_w, 17)
    art_box(img, summit_scene, EDGE + half_w + 24, yr + 6, half_w, 64)
    y = max(left_end, yr + 6 + 64) + 6
    y = rule_across(pen, y, 1)
    y += 8

    # ---- bottom row: three tiles ----
    third = (INNER - 48) // 3
    xs = [EDGE, EDGE + third + 24, EDGE + 2 * (third + 24)]
    tiles = [
        ("War · Ukraine", "MISSILE HITS ZELENSKY'S HOMETOWN",
         "A Russian ballistic missile struck Kryvyi Rih, killing 2 and "
         "wounding scores, as Moscow hit bridges in Kyiv.",
         city_scene),
        ("Disaster · Nigeria", "BOAT CAPSIZES, 24 DEAD",
         "A boat carrying mourners to a funeral overturned in Nigeria, "
         "killing 24 people on board.",
         river_scene),
        ("Europe · France", "SIXTH WEEKEND OF PROTESTS",
         "Cost-of-living marches filled French streets for a sixth "
         "Saturday, with lower turnout than before.",
         march_scene),
    ]
    y_top = y
    y_bottom = y_top
    for (kick, head, body, scene), x in zip(tiles, xs):
        yy = tag(pen, x, y_top, kick, third)
        yy = banner(pen, x, yy, head, 20, third, 22)
        yy = block(pen, x, yy + 4, body, face(SERIF, 13), third, 16)
        art_box(img, scene, x, yy + 6, third, 48)
        y_bottom = max(y_bottom, yy + 6 + 48)
    y = y_bottom + 8
    y = rule_across(pen, y, 1)
    y += 6

    # ---- briefs ----
    pen.text((EDGE, y), "IN BRIEF", font=face(SANS_BOLD, 15), fill=CRIMSON)
    y += 22
    briefs = [
        "G20 opens in Johannesburg, the first summit on African soil.",
        "Japan and India agree deeper defence and arms-industry ties.",
        "Russian cargo ship hit by drones in the Baltic; Finland on alert.",
        "Four killed in a landslide in Sri Lanka's Central Province.",
        "TikTok launches a global deepfake-detection tool for public figures.",
        "Two tanker incidents near Oman; Iran says a vessel hit a mine.",
    ]
    fnt = face(SERIF, 13)
    row = 17
    for i, item in enumerate(briefs):
        bx = EDGE if i % 2 == 0 else EDGE + half_w + 24
        by = y + (i // 2) * row
        pen.text((bx, by), "•  " + item, font=fnt, fill=INK)
    y = y + ((len(briefs) + 1) // 2) * row + 4
    y = rule_across(pen, y, 1)

    # ---- footer ----
    pen.text((EDGE, y + 8),
             "THE WORLD TODAY  ·  Sunday, 22 November 2026  ·  Sources: AP, France 24, Arab News, Xinhua, Dunya News",
             font=face(SANS, 13), fill=SOFT)

    img.save("news_image.png")
    print("wrote news_image.png", img.size)


if __name__ == "__main__":
    front_page()
