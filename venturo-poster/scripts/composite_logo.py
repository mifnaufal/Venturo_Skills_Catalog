#!/usr/bin/env python3
"""
composite_logo.py — Venturo WhatsApp Catalog Card Renderer

Renders package info text + tech icons onto a background image,
then composites the official Venturo logo.

Output: 1080x1080 PNG — WhatsApp Business catalog ready.

Usage:
    python composite_logo.py \
        --input /path/to/background.png \
        --output /path/to/catalog.png \
        --tier starter \
        --position bottom-right
"""

import argparse
import os
import sys
import time
from pathlib import Path

TIER_DATA = {
    "starter": {
        "name": "STARTER",
        "tagline": "Cocok untuk UMKM & Startup",
        "budget": "Rp20 Juta – Rp80 Juta",
        "ideal": "UMKM, usaha mikro, perusahaan kecil, dan startup yang membutuhkan website, mobile application, atau sistem operasional sederhana.",
        "team": ["1 Business Analyst", "1 Senior Software Engineer"],
        "timeline": ["Analysis & Design: 1–2 Minggu", "Development: 2 Minggu–1 Bulan", "Testing & Go-Live: 1–2 Minggu"],
        "color": "#06b6d4",
    },
    "growth": {
        "name": "GROWTH",
        "tagline": "Cocok untuk Perusahaan Bertumbuh",
        "budget": "Rp80 Juta – Rp250 Juta",
        "ideal": "Perusahaan yang membutuhkan sistem custom: Finance, HRIS, CRM, ERP, Inventory, WMS, Logistic, Sales, Production, Asset Management.",
        "team": ["1 Business Analyst", "1 Senior Software Engineer", "1 UI/UX Designer", "1 QA Engineer"],
        "timeline": ["Analysis & Design: 2 Minggu–1 Bulan", "Development: 1–2 Bulan", "Testing & Go-Live: 2 Minggu–1 Bulan"],
        "color": "#3b82f6",
    },
    "enterprise": {
        "name": "ENTERPRISE",
        "tagline": "Cocok untuk Perusahaan Besar",
        "budget": "Mulai Rp250 Juta",
        "ideal": "Perusahaan menengah hingga enterprise yang membutuhkan sistem skala besar, integrasi lintas sistem, keamanan tinggi, AI, Big Data, transformasi digital.",
        "team": ["1 Business Analyst", "1 Senior Software Engineer", "1 Intermediate Software Engineer", "1 UI/UX Designer", "1 QA Engineer", "1 Penetration Tester"],
        "timeline": ["Analysis & Design: 1–2 Bulan", "Development: 2–4 Bulan", "Testing & Go-Live: 2 Bulan"],
        "color": "#8b5cf6",
    },
}

def get_plugin_root():
    return Path(__file__).resolve().parent.parent

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def render_catalog(input_path, output_path, tier_name, logo_position):
    start = time.time()

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("ERROR: Pillow required. pip install Pillow")
        return False

    if not os.path.exists(input_path):
        print(f"ERROR: Input not found: {input_path}")
        return False

    tier = TIER_DATA.get(tier_name.lower())
    if not tier:
        print(f"ERROR: Unknown tier '{tier_name}'. Use: starter, growth, enterprise")
        return False

    logo_path = get_plugin_root() / "assets" / "image_1c155d.png"
    if not logo_path.exists():
        print(f"ERROR: Logo not found at {logo_path}")
        return False

    # Load images
    bg = Image.open(input_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    W, H = bg.size

    # Find fonts
    font_dirs = [
        "/usr/share/fonts/truetype/dejavu/",
        "/usr/share/fonts/",
        "/usr/share/fonts/truetype/",
        str(Path.home() / ".fonts"),
    ]
    bold_path, reg_path = None, None
    for d in font_dirs:
        p = Path(d)
        candidates = list(p.rglob("DejaVuSans-Bold.ttf")) + list(p.rglob("DejaVuSans.ttf"))
        for c in candidates:
            if "Bold" in c.name and not bold_path:
                bold_path = str(c)
            elif "Bold" not in c.name and not reg_path:
                reg_path = str(c)

    # Try canvas-design fonts
    canvas_fonts = Path("/home/alxyz/.agents/skills/canvas-design/canvas-fonts")
    if canvas_fonts.exists():
        candidates = list(canvas_fonts.glob("*.ttf"))
        for c in candidates:
            name = c.name.lower()
            if "bold" in name or "bigshoulders" in name or "geistmono" in name:
                if not bold_path:
                    bold_path = str(c)
            elif not reg_path:
                reg_path = str(c)

    FONT_BOLD = ImageFont.truetype(bold_path, 48) if bold_path else ImageFont.load_default()
    FONT_TAG = ImageFont.truetype(reg_path, 24) if reg_path else ImageFont.load_default()
    FONT_BUDGET = ImageFont.truetype(bold_path, 40) if bold_path else ImageFont.load_default()
    FONT_BODY = ImageFont.truetype(reg_path, 20) if reg_path else ImageFont.load_default()
    FONT_SMALL = ImageFont.truetype(reg_path, 18) if reg_path else ImageFont.load_default()
    FONT_TEAM_TITLE = ImageFont.truetype(bold_path, 22) if bold_path else ImageFont.load_default()
    FONT_TEAM = ImageFont.truetype(reg_path, 18) if reg_path else ImageFont.load_default()

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Semi-transparent overlay for text readability
    draw.rectangle([(0, int(H*0.55)), (W, H)], fill=(0, 0, 0, 160))
    draw.rectangle([(0, 0), (W, int(H*0.12))], fill=(0, 0, 0, 100))

    # === TEXT RENDERING ===

    def center_text(d, text, font, y, color="white", max_w=None):
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        if max_w and tw > max_w:
            # Scale down
            scale = max_w / tw
            new_size = max(12, int(font.size * scale))
            try:
                font = ImageFont.truetype(font.path, new_size)
                bbox = d.textbbox((0, 0), text, font=font)
                tw = bbox[2] - bbox[0]
            except:
                pass
        x = (W - tw) // 2
        d.text((x, y), text, fill=color, font=font)
        return font

    def draw_text(d, text, font, x, y, color="white", max_w=None):
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        if max_w and tw > max_w:
            scale = max_w / tw
            new_size = max(10, int(font.size * scale))
            try:
                font = ImageFont.truetype(font.path, new_size)
            except:
                pass
        d.text((x, y), text, fill=color, font=font)
        return font

    # -- TOP SECTION: Package name + tagline --
    center_text(draw, tier["name"], FONT_BOLD, 30, tier["color"])
    center_text(draw, tier["tagline"], FONT_TAG, 88, "#94a3b8")

    # -- BOTTOM SECTION: Full package details --
    base_y = int(H * 0.58)
    padding_x = 50
    col_width = (W - 2 * padding_x - 30) // 2  # two columns with gap

    # LEFT COLUMN: Budget + Ideal
    draw_text(draw, "BUDGET PROYEK", FONT_TEAM_TITLE, padding_x, base_y, "#facc15")
    draw_text(draw, tier["budget"], FONT_BUDGET, padding_x, base_y + 30, "#ffffff", col_width)

    draw_text(draw, "IDEAL UNTUK", FONT_TEAM_TITLE, padding_x, base_y + 80, "#94a3b8")
    draw_text(draw, tier["ideal"], FONT_BODY, padding_x, base_y + 110, "#cbd5e1", col_width)

    # RIGHT COLUMN: Team + Timeline
    right_x = padding_x + col_width + 30

    draw_text(draw, "DEDICATED TEAM", FONT_TEAM_TITLE, right_x, base_y, "#facc15")
    for i, member in enumerate(tier["team"]):
        draw_text(draw, f"• {member}", FONT_TEAM, right_x, base_y + 30 + i * 26, "#cbd5e1", col_width)

    team_count = len(tier["team"])
    tl_y = base_y + 30 + team_count * 26 + 10
    draw_text(draw, "ESTIMASI TIMELINE", FONT_TEAM_TITLE, right_x, tl_y, "#facc15")
    for i, t in enumerate(tier["timeline"]):
        draw_text(draw, f"• {t}", FONT_TEAM, right_x, tl_y + 26 + i * 24, "#cbd5e1", col_width)

    # Bottom accent line
    accent_color = hex_to_rgb(tier["color"])
    draw.rectangle([(40, int(H * 0.94)), (W - 40, int(H * 0.94) + 4)], fill=(*accent_color, 255))

    # WhatsApp catalog label
    center_text(draw, "Katalog WhatsApp Business — Venturo Solutions", FONT_SMALL, int(H * 0.96), "#64748b")

    # Merge overlay with background
    bg = Image.alpha_composite(bg, overlay)

    # === LOGO COMPOSITING ===
    logo_scale = 0.15
    new_logo_w = int(W * logo_scale)
    aspect = logo.height / logo.width
    new_logo_h = int(new_logo_w * aspect)
    logo_resized = logo.resize((new_logo_w, new_logo_h), Image.LANCZOS)

    padding = int(W * 0.04)
    if logo_position == "bottom-right":
        lx, ly = W - new_logo_w - padding, H - new_logo_h - padding
    else:
        lx, ly = W - new_logo_w - padding, padding

    if logo_resized.mode == "RGBA":
        bg.paste(logo_resized, (lx, ly), logo_resized)
    else:
        bg.paste(logo_resized, (lx, ly))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    bg.save(output_path, "PNG", optimize=True)

    elapsed = time.time() - start
    print(f"Catalog card rendered in {elapsed:.2f}s")
    print(f"Saved: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Render Venturo catalog card")
    parser.add_argument("--input", required=True, help="Background image path")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--tier", required=True, choices=["starter", "growth", "enterprise"],
                        help="Package tier")
    parser.add_argument("--position", default="bottom-right",
                        choices=["bottom-right", "top-right"],
                        help="Logo position")
    args = parser.parse_args()

    ok = render_catalog(args.input, args.output, args.tier, args.position)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
