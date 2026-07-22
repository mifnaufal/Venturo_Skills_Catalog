#!/usr/bin/env python3
"""
Generate a placeholder Venturo logo for development/testing.

Run this script to create a placeholder logo at assets/image_1c155d.png.
Replace it with the official Venturo logo before production use.
"""

from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

def generate():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Install Pillow: pip install Pillow")
        return False

    logo_path = SKILL_DIR / "assets" / "image_1c155d.png"
    logo_path.parent.mkdir(parents=True, exist_ok=True)

    w, h = 800, 200
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for y in range(h):
        ratio = y / h
        r = int(6 * (1 - ratio) + 16 * ratio)
        g = int(182 * (1 - ratio) + 185 * ratio)
        b = int(212 * (1 - ratio) + 129 * ratio)
        a = 255
        draw.line([(0, y), (w, y)], fill=(r, g, b, a))

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
    except:
        font = ImageFont.load_default()

    text = "VENTURO"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (w - tw) // 2
    ty = (h - th) // 2 - 5
    draw.text((tx, ty), text, fill="white", font=font)

    tagline = "SOLUTIONS"
    try:
        tag_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
    except:
        tag_font = ImageFont.load_default()
    tb = draw.textbbox((0, 0), tagline, font=tag_font)
    tgw, tgh = tb[2] - tb[0], tb[3] - tb[1]
    draw.text(((w - tgw) // 2, ty + th + 8), tagline, fill="white", font=tag_font)

    img.save(logo_path, "PNG")
    print(f"Placeholder logo generated: {logo_path}")
    print("REPLACE THIS with the official Venturo logo before production use!")
    return True

if __name__ == "__main__":
    generate()
