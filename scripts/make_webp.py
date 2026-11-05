#!/usr/bin/env python3
"""Write a .webp copy next to each page image in assets/logo and assets/img, kept only when it is smaller.

Opaque PNG logos are encoded lossy at quality 90 (visually identical, about 10 KB instead of about 100 KB);
PNGs with transparency stay lossless. JPG photos at quality 75. hero.jpg also gets an 800px-wide
hero-800.webp for phones (styles.css / preload). The originals stay in place:
pages serve the WebP through <picture> with the PNG/JPG as fallback, and og:image keeps the JPG.
Run by hand after adding or changing an image (needs Pillow), then run build.py:
    python3 scripts/make_webp.py && python3 build.py
"""
import glob, io, os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = {"logo/mark.png"}  # not used on any page

def main():
    before = after = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "assets", "logo", "*")) + glob.glob(os.path.join(ROOT, "assets", "img", "*"))):
        rel = os.path.relpath(path, os.path.join(ROOT, "assets"))
        if rel in SKIP or not path.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        im = Image.open(path)
        buf = io.BytesIO()
        if path.lower().endswith(".png"):
            opaque = im.mode == "RGB" or (im.mode == "RGBA" and im.getchannel("A").getextrema() == (255, 255))
            if opaque:
                im.convert("RGB").save(buf, "WEBP", quality=90, method=6)
            else:
                im.save(buf, "WEBP", lossless=True, quality=100, method=6)
        else:
            im.convert("RGB").save(buf, "WEBP", quality=75, method=6)
        out = os.path.splitext(path)[0] + ".webp"
        size = os.path.getsize(path)
        if buf.tell() < size:
            with open(out, "wb") as fh:
                fh.write(buf.getvalue())
            before += size; after += buf.tell()
            print(f"{rel}: {size} -> {buf.tell()} bytes")
        elif os.path.exists(out):
            os.remove(out)
    hero = Image.open(os.path.join(ROOT, "assets", "img", "hero.jpg")).convert("RGB")
    hero.resize((800, round(hero.height * 800 / hero.width)), Image.LANCZOS).save(
        os.path.join(ROOT, "assets", "img", "hero-800.webp"), "WEBP", quality=75, method=6)
    print(f"total: {before} -> {after} bytes")

if __name__ == "__main__":
    main()
