#!/usr/bin/env python3

import argparse
import os
import sys
import time
from pathlib import Path

from PIL import Image as PILImage, ImageDraw, ImageFont

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


def _find_best_logo_position(bg, logo_w, logo_h, grid_size=16):
    W, H = bg.size
    cell_w = W // grid_size
    cell_h = H // grid_size

    scores = []
    for gy in range(grid_size):
        for gx in range(grid_size):
            l = gx * cell_w
            r = min(l + cell_w, W)
            t = gy * cell_h
            b = min(t + cell_h, H)

            pixels = 0
            brightness_total = 0
            var_total = 0
            sample_step = max(1, cell_w // 4)
            vals = []

            for y in range(t, b, sample_step):
                for x in range(l, r, sample_step):
                    try:
                        px = bg.getpixel((x, y))
                        if len(px) >= 3:
                            lum = 0.299 * px[0] + 0.587 * px[1] + 0.114 * px[2]
                            brightness_total += lum
                            vals.append(lum)
                            pixels += 1
                    except Exception:
                        pass

            if pixels == 0:
                continue

            avg_brightness = brightness_total / pixels
            variance = sum((v - avg_brightness) ** 2 for v in vals) / pixels

            # Score: high brightness = good (clean space), low variance = good (uniform)
            # Penalize dark cells (< 128 brightness) — logo won't show
            if avg_brightness < 120:
                score = -1
            else:
                score = avg_brightness - variance * 0.5

            scores.append((score, gx, gy, avg_brightness))

    if not scores:
        return None, None

    scores.sort(key=lambda x: x[0], reverse=True)

    # Find the best scoring cell that's not too close to edge
    margin_cells = 2
    for score, gx, gy, _ in scores:
        if score < 0:
            break
        if (margin_cells <= gx < grid_size - margin_cells and
            margin_cells <= gy < grid_size - margin_cells):
            # Found a good interior position
            lx = gx * cell_w + (cell_w - logo_w) // 2
            ly = gy * cell_h + (cell_h - logo_h) // 2
            lx = max(0, min(lx, W - logo_w))
            ly = max(0, min(ly, H - logo_h))
            return lx, ly

    # No good interior position found — scan for any bright cell
    for score, gx, gy, _ in scores:
        if score >= 0:
            lx = gx * cell_w + (cell_w - logo_w) // 2
            ly = gy * cell_h + (cell_h - logo_h) // 2
            lx = max(0, min(lx, W - logo_w))
            ly = max(0, min(ly, H - logo_h))
            return lx, ly

    return None, None


def _overlay_logo(bg, logo, logo_position):
    W, H = bg.size
    logo_scale = 0.12
    new_logo_w = int(W * logo_scale)
    aspect = logo.height / logo.width
    new_logo_h = int(new_logo_w * aspect)
    logo_resized = logo.resize((new_logo_w, new_logo_h), PILImage.LANCZOS)
    padding = int(W * 0.035)

    if logo_position == "auto":
        lx, ly = _find_best_logo_position(bg, new_logo_w, new_logo_h)
        if lx is None:
            lx, ly = W - new_logo_w - padding, padding
    elif logo_position == "top-left":
        lx, ly = padding, padding
    elif logo_position == "top-right":
        lx, ly = W - new_logo_w - padding, padding
    elif logo_position == "bottom-left":
        lx, ly = padding, H - new_logo_h - padding
    elif logo_position == "bottom-right":
        lx, ly = W - new_logo_w - padding, H - new_logo_h - padding
    elif "," in logo_position:
        parts = logo_position.split(",")
        try:
            lx, ly = int(parts[0]), int(parts[1])
        except (ValueError, IndexError):
            lx, ly = W - new_logo_w - padding, H - new_logo_h - padding
    else:
        lx, ly = W - new_logo_w - padding, H - new_logo_h - padding

    if logo_resized.mode == "RGBA":
        bg.paste(logo_resized, (lx, ly), logo_resized)
    else:
        bg.paste(logo_resized, (lx, ly))

    print(f"  logo: {logo_position} → ({lx}, {ly})")


def render_catalog(input_path, output_path, tier_name, logo_position, logo_only=False):
    start = time.time()

    try:
        from PIL import Image
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

    bg = Image.open(input_path).convert("RGBA")
    logo = Image.open(logo_path).convert("RGBA")
    W, H = bg.size

    if logo_only:
        _overlay_logo(bg, logo, logo_position)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        bg.save(output_path, "PNG", optimize=True)
        elapsed = time.time() - start
        print(f"Logo composited in {elapsed:.2f}s")
        print(f"Saved: {output_path}")
        return True

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

    s = max(W, H)
    FONT_BOLD = ImageFont.truetype(bold_path, int(s * 0.04)) if bold_path else ImageFont.load_default()
    FONT_TAG = ImageFont.truetype(reg_path, int(s * 0.02)) if reg_path else ImageFont.load_default()
    FONT_BUDGET = ImageFont.truetype(bold_path, int(s * 0.035)) if bold_path else ImageFont.load_default()
    FONT_BODY = ImageFont.truetype(reg_path, int(s * 0.017)) if reg_path else ImageFont.load_default()
    FONT_SMALL = ImageFont.truetype(reg_path, int(s * 0.015)) if reg_path else ImageFont.load_default()
    FONT_TEAM_TITLE = ImageFont.truetype(bold_path, int(s * 0.02)) if bold_path else ImageFont.load_default()
    FONT_TEAM = ImageFont.truetype(reg_path, int(s * 0.015)) if reg_path else ImageFont.load_default()

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    draw.rectangle([(0, int(H * 0.55)), (W, H)], fill=(0, 0, 0, 160))
    draw.rectangle([(0, 0), (W, int(H * 0.1))], fill=(0, 0, 0, 100))

    def center_text(d, text, font, y, color="white", max_w=None):
        bbox = d.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        if max_w and tw > max_w:
            scale = max_w / tw
            new_size = max(12, int(font.size * scale))
            try:
                font = ImageFont.truetype(font.path, new_size)
                bbox = d.textbbox((0, 0), text, font=font)
                tw = bbox[2] - bbox[0]
            except Exception:
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
            except Exception:
                pass
        d.text((x, y), text, fill=color, font=font)
        return font

    center_text(draw, tier["name"], FONT_BOLD, int(s * 0.025), tier["color"])
    center_text(draw, tier["tagline"], FONT_TAG, int(s * 0.07), "#94a3b8")

    padding_x = int(s * 0.04)
    col_width = (W - 2 * padding_x - int(s * 0.025)) // 2
    base_y = int(H * 0.58)

    draw_text(draw, "BUDGET PROYEK", FONT_TEAM_TITLE, padding_x, base_y, "#facc15")
    draw_text(draw, tier["budget"], FONT_BUDGET, padding_x, base_y + int(s * 0.025), "#ffffff", col_width)
    draw_text(draw, "IDEAL UNTUK", FONT_TEAM_TITLE, padding_x, base_y + int(s * 0.07), "#94a3b8")
    draw_text(draw, tier["ideal"], FONT_BODY, padding_x, base_y + int(s * 0.095), "#cbd5e1", col_width)

    right_x = padding_x + col_width + int(s * 0.025)
    draw_text(draw, "DEDICATED TEAM", FONT_TEAM_TITLE, right_x, base_y, "#facc15")
    for i, member in enumerate(tier["team"]):
        draw_text(draw, f"• {member}", FONT_TEAM, right_x, base_y + int(s * 0.025) + i * int(s * 0.022), "#cbd5e1", col_width)

    team_count = len(tier["team"])
    tl_y = base_y + int(s * 0.025) + team_count * int(s * 0.022) + int(s * 0.008)
    draw_text(draw, "ESTIMASI TIMELINE", FONT_TEAM_TITLE, right_x, tl_y, "#facc15")
    for i, t in enumerate(tier["timeline"]):
        draw_text(draw, f"• {t}", FONT_TEAM, right_x, tl_y + int(s * 0.022) + i * int(s * 0.02), "#cbd5e1", col_width)

    accent_color = hex_to_rgb(tier["color"])
    draw.rectangle([(int(s * 0.035), int(H * 0.94)), (W - int(s * 0.035), int(H * 0.94) + max(2, s // 270))],
                   fill=(*accent_color, 255))
    center_text(draw, "Katalog WhatsApp Business — Venturo Solutions", FONT_SMALL, int(H * 0.965), "#64748b")

    bg = Image.alpha_composite(bg, overlay)
    _overlay_logo(bg, logo, logo_position)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    bg.save(output_path, "PNG", optimize=True)

    elapsed = time.time() - start
    print(f"Catalog card rendered in {elapsed:.2f}s")
    print(f"Saved: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Composite Venturo logo onto catalog design")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--tier", required=True, choices=["starter", "growth", "enterprise"])
    parser.add_argument("--position", default="auto",
                        help="Logo position: auto, top-left, top-right, bottom-left, bottom-right, or x,y")
    parser.add_argument("--logo-only", action="store_true")
    args = parser.parse_args()

    ok = render_catalog(args.input, args.output, args.tier, args.position, args.logo_only)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
