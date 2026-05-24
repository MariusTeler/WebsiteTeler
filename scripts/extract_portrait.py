"""One-off: extract the largest image from the CV PDF and save as portrait.jpg."""
import io
from pathlib import Path

import fitz
from PIL import Image

CV_PATH = "/Users/telermarius/Library/CloudStorage/Dropbox/My Stuff/CV - Teler Marius Adrian.pdf"
OUT_PATH = Path(__file__).resolve().parent.parent / "static" / "img" / "portrait.jpg"

doc = fitz.open(CV_PATH)
candidates = []
for page in doc:
    for info in page.get_images(full=True):
        xref = info[0]
        base = doc.extract_image(xref)
        img = Image.open(io.BytesIO(base["image"]))
        w, h = img.size
        if w < 100 or h < 100:
            continue
        aspect = w / h
        candidates.append((img, w * h, aspect))

if not candidates:
    raise SystemExit("No images found in PDF")

# Headshot heuristic: prefer images closer to square aspect ratio, then by size.
candidates.sort(key=lambda c: (abs(c[2] - 1.0), -c[1]))
biggest = candidates[0][0]
print(f"Picked image {biggest.size} (aspect {candidates[0][2]:.2f}) from {len(candidates)} candidates")

biggest = biggest.convert("RGB")
biggest.thumbnail((600, 600))
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
biggest.save(OUT_PATH, "JPEG", quality=85, optimize=True)
print(f"Saved {biggest.size} to {OUT_PATH}")
