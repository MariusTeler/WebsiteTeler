"""One-off: generate a 1200x630 Open Graph preview image."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = ROOT / "static" / "img" / "og-image.png"
ALLURA_PATH = ROOT / "static" / "fonts" / "Allura-Regular.ttf"

INK = (11, 29, 54)
INK_2 = (20, 42, 74)
GOLD = (201, 161, 74)
CREAM = (247, 243, 236)
LIGHT = (205, 213, 224)

img = Image.new("RGB", (1200, 630), INK)
draw = ImageDraw.Draw(img)

# Gradient background (vertical wash)
for y in range(630):
    t = y / 630
    r = int(INK[0] * (1 - t) + INK_2[0] * t)
    g = int(INK[1] * (1 - t) + INK_2[1] * t)
    b = int(INK[2] * (1 - t) + INK_2[2] * t)
    draw.line([(0, y), (1200, y)], fill=(r, g, b))

# Decorative top accent bar
draw.rectangle([(0, 0), (1200, 6)], fill=GOLD)


def load_font(size, families):
    for family in families:
        try:
            return ImageFont.truetype(family, size)
        except OSError:
            continue
    return ImageFont.load_default()


serif = load_font(64, ["/System/Library/Fonts/Supplemental/Georgia.ttf", "Georgia.ttf"])
serif_small = load_font(28, ["/System/Library/Fonts/Supplemental/Georgia.ttf", "Georgia.ttf"])
sans_label = load_font(20, ["/System/Library/Fonts/Helvetica.ttc", "Helvetica.ttf"])
allura_t = ImageFont.truetype(str(ALLURA_PATH), 340)
allura_m = ImageFont.truetype(str(ALLURA_PATH), 150)

# Eyebrow (gold uppercase)
draw.text((80, 200), "EXECUTIVE DIRECTOR  ·  COURIER IT & OPERATIONS", fill=GOLD, font=sans_label)

# Headline (large serif, three lines)
draw.text((80, 250), "Marius Teler", fill=CREAM, font=serif)
draw.text((80, 330), "Self-taught. Optimizing", fill=CREAM, font=serif)
draw.text((80, 410), "businesses since 2008.", fill=CREAM, font=serif)

# Subtitle
draw.text((80, 510), "teler.net  ·  18+ years in logistics IT", fill=LIGHT, font=serif_small)

# ----- Logo mark on right (T + m + serpentine ligature) -----
MARK_BASELINE = 430
T_CX = 870
M_CX = 1090

draw.text((T_CX, MARK_BASELINE), "T", fill=GOLD, font=allura_t, anchor="ms")
draw.text((M_CX, MARK_BASELINE), "m", fill=CREAM, font=allura_m, anchor="ms")


def cubic_bezier_points(p0, p1, p2, p3, n=30):
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        x = u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0]
        y = u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1]
        pts.append((x, y))
    return pts


# Three serpentine cubic segments undulating around the baseline between T and m
ligature_segments = [
    [(940, 448), (953, 478), (965, 410), (977, 448)],
    [(977, 448), (989, 478), (1001, 410), (1013, 444)],
    [(1013, 444), (1025, 472), (1040, 400), (1030, 405)],
]

ligature_points = []
for seg in ligature_segments:
    pts = cubic_bezier_points(*seg, n=25)
    if ligature_points:
        ligature_points.extend(pts[1:])
    else:
        ligature_points.extend(pts)

draw.line(ligature_points, fill=GOLD, width=4, joint="curve")

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT_PATH, "PNG", optimize=True)
print(f"Saved {img.size} to {OUT_PATH}")
