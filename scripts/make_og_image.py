"""One-off: generate a 1200x630 Open Graph preview image."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT_PATH = Path(__file__).resolve().parent.parent / "static" / "img" / "og-image.png"

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

# Try to load a nice serif font; fall back to default if not present.
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

# Eyebrow (gold uppercase)
draw.text((80, 200), "EXECUTIVE DIRECTOR  ·  COURIER IT & OPERATIONS", fill=GOLD, font=sans_label)

# Headline (large serif, two lines)
draw.text((80, 250), "Marius Teler", fill=CREAM, font=serif)
draw.text((80, 330), "Self-taught. Optimizing", fill=CREAM, font=serif)
draw.text((80, 410), "businesses since 2008.", fill=CREAM, font=serif)

# Subtitle
draw.text((80, 510), "teler.net  ·  18+ years in logistics IT", fill=LIGHT, font=serif_small)

# Right-side decoration: gold dotted route + node
for x in range(900, 1140, 20):
    draw.ellipse([(x, 313), (x + 6, 319)], fill=GOLD)
draw.ellipse([(1140, 305), (1162, 327)], fill=GOLD)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT_PATH, "PNG", optimize=True)
print(f"Saved {img.size} to {OUT_PATH}")
