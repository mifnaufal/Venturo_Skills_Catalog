#!/usr/bin/env python3

import argparse
import json
import math
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DEFAULT_SPEC = {
    "canvas": {
        "orientation": "portrait",
        "background_color": "#FFFFFF",
        "aspect_ratio": "3:4"
    },
    "color_palette": {
        "primary_accent": "#7CB518",
        "secondary_accent": "#4A8C2A",
        "text_primary": "#1A1A1A",
        "text_highlight": "#7CB518",
        "price_color": "#E63946",
        "banner_bg": "#F8D7DA",
        "banner_text": "#C0392B",
        "footer_bg": "#1A1A1A",
        "footer_text": "#FFFFFF",
        "dot_pattern": "#2C2C2C"
    },
    "layout_structure": {
        "header": {
            "position": "top-left",
            "title": {
                "text": "ELECTRONIC DISCOUNT CATALOGUE",
                "font_weight": "bold",
                "font_size": "large",
                "line_breaks": 3,
                "color_alternation": ["#1A1A1A", "#7CB518", "#1A1A1A"]
            },
            "discount_badge": {
                "position": "top-right",
                "shape": "irregular_pentagon",
                "background_color": "#7CB518",
                "text": "50% DISCOUNT",
                "text_color": "#FFFFFF",
                "font_size": "x-large"
            }
        },
        "sub_header_banner": {
            "position": "below-header",
            "shape": "rounded_rectangle",
            "background_color": "#F8D7DA",
            "text": "CREATE YOUR DESIGN TODAY",
            "text_color": "#C0392B",
            "font_style": "handwritten"
        },
        "product_sections": {
            "count": 3,
            "arrangement": "alternating_left_right",
            "each_section": {
                "green_blob": {
                    "shape": "rounded_organic",
                    "color": "#7CB518",
                    "position": "behind_product"
                },
                "dot_pattern": {
                    "style": "grid_dots",
                    "color": "#2C2C2C",
                    "position": "adjacent_to_green_blob"
                },
                "product_image": {
                    "style": "realistic_photo",
                    "background": "transparent_or_white"
                },
                "label": {
                    "text": "LIMITED OFFER",
                    "font_size": "small",
                    "color": "#1A1A1A"
                },
                "product_name": {
                    "font_weight": "bold",
                    "font_size": "large",
                    "color": "#1A1A1A"
                },
                "price": {
                    "text": "$49.9",
                    "color": "#E63946",
                    "font_size": "x-large",
                    "font_weight": "bold"
                },
                "description": {
                    "text": "lorem_ipsum",
                    "font_size": "small",
                    "color": "#555555",
                    "lines": 4
                }
            },
            "section_1": {"product_position": "left", "text_position": "right"},
            "section_2": {"product_position": "right", "text_position": "left"},
            "section_3": {"product_position": "left", "text_position": "right"}
        },
        "footer": {
            "background_color": "#1A1A1A",
            "height": "small",
            "elements": [
                {"type": "cta_button", "text": "SHOP NOW", "background_color": "#7CB518", "text_color": "#1A1A1A", "font_weight": "bold"},
                {"type": "contact_info", "icon": "globe", "icon_color": "#7CB518", "label": "CONTACT US", "value": "123-456-7890", "text_color": "#FFFFFF"},
                {"type": "website_info", "icon": "globe", "icon_color": "#7CB518", "label": "VISIT OUR WEBSITE", "value": "www.reallygreatsite.com", "text_color": "#FFFFFF"}
            ],
            "layout": "horizontal_flex"
        }
    },
    "design_elements": {
        "organic_shapes": {"type": "rounded_blobs", "color": "#7CB518", "usage": "background_for_products"},
        "dot_patterns": {"type": "regular_grid", "color": "#2C2C2C", "size": "small", "usage": "decorative_accent"},
        "typography": {"headings": "sans-serif_bold", "body": "sans-serif_regular", "banner": "handwritten_script"}
    }
}

PRODUCT_DATA = [
    {
        "label": "LIMITED OFFER",
        "name": "Wireless Headphone Pro",
        "price": "$49.9",
        "description": "Premium wireless headphones with active noise cancelling, 30-hour battery life, and comfortable over-ear design.",
        "color": "#4A90D9"
    },
    {
        "label": "LIMITED OFFER",
        "name": "Smart Watch Ultra",
        "price": "$79.9",
        "description": "Advanced fitness tracking, heart rate monitoring, GPS, and 7-day battery life in a sleek waterproof design.",
        "color": "#E67E22"
    },
    {
        "label": "LIMITED OFFER",
        "name": "Bluetooth Speaker X",
        "price": "$34.9",
        "description": "Portable waterproof speaker with 360-degree sound, 20-hour playtime, and built-in microphone.",
        "color": "#2ECC71"
    }
]


def hr(col):
    col = col.lstrip("#")
    return tuple(int(col[i:i+2], 16) for i in (0, 2, 4))


def find_fonts():
    bold_path = reg_path = script_path = None
    dirs = [
        "/usr/share/fonts/truetype/dejavu/",
        "/usr/share/fonts/",
        "/usr/share/fonts/truetype/",
        str(Path.home() / ".fonts"),
    ]
    for d in dirs:
        p = Path(d)
        if not p.exists():
            continue
        for c in p.rglob("*.ttf"):
            if "DejaVuSans-Bold" in c.name and not bold_path:
                bold_path = str(c)
            elif "DejaVuSans.ttf" == c.name and not reg_path:
                reg_path = str(c)

    canvas_fonts = Path("/home/alxyz/.agents/skills/canvas-design/canvas-fonts")
    if canvas_fonts.exists():
        for c in canvas_fonts.glob("*.ttf"):
            n = c.name.lower()
            if "bold" in n or "bigshoulders" in n:
                if not bold_path:
                    bold_path = str(c)
            elif "geistmono" in n:
                if not reg_path:
                    reg_path = str(c)

    if not bold_path:
        dirs2 = ["/System/Library/Fonts", "/Library/Fonts"]
        for d in dirs2:
            for c in Path(d).rglob("*.ttf"):
                if "Helvetica-Bold" in c.name or "Arial Bold" in c.name:
                    bold_path = str(c)
                    break
    if not reg_path:
        dirs2 = ["/System/Library/Fonts", "/Library/Fonts"]
        for d in dirs2:
            for c in Path(d).rglob("*.ttf"):
                if "Helvetica" in c.name and "Bold" not in c.name:
                    reg_path = str(c)
                    break

    return bold_path or "DejaVuSans-Bold.ttf", reg_path or "DejaVuSans.ttf"


def get_font(bold_path, reg_path, size, bold=True):
    try:
        return ImageFont.truetype(bold_path if bold else reg_path, size)
    except Exception:
        return ImageFont.load_default()


def draw_rounded_rect(draw, xy, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = xy
    r = min(radius, (x2 - x1) // 2, (y2 - y1) // 2)
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def draw_organic_blob(draw, cx, cy, w, h, color, alpha=180):
    base = hr(color)
    c = (*base, alpha)
    steps = 36
    pts = []
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        rx = w // 2 + int(30 * math.sin(angle * 3))
        ry = h // 2 + int(25 * math.cos(angle * 2.5))
        x = cx + int(rx * math.cos(angle))
        y = cy + int(ry * math.sin(angle))
        pts.append((x, y))
    if pts:
        draw.polygon(pts, fill=c)


def draw_irregular_pentagon(draw, cx, cy, size, color):
    base = hr(color)
    pts = []
    for i in range(5):
        angle = 2 * math.pi * i / 5 - math.pi / 2
        r = size + (20 if i % 2 == 0 else -15)
        x = cx + int(r * math.cos(angle))
        y = cy + int(r * math.sin(angle))
        pts.append((x, y))
    draw.polygon(pts, fill=(*base, 255))


def draw_dot_pattern(draw, x, y, w, h, color, spacing=20, radius=3):
    c = hr(color)
    for dx in range(0, w, spacing):
        for dy in range(0, h, spacing):
            draw.ellipse([x + dx - radius, y + dy - radius, x + dx + radius, y + dy + radius],
                         fill=(*c, 80))


def draw_product_placeholder(draw, x, y, w, h, color):
    base = hr(color)
    lighter = tuple(min(v + 60, 255) for v in base)
    draw_rounded_rect(draw, (x, y, x + w, y + h), radius=12, fill=(*lighter, 255))
    draw_rounded_rect(draw, (x + 2, y + 2, x + w - 2, y + h - 2), radius=10, fill=(*base, 255))
    cx, cy = x + w // 2, y + h // 2
    icon_sz = min(w, h) // 4
    draw.ellipse([cx - icon_sz, cy - icon_sz, cx + icon_sz, cy + icon_sz],
                 outline=(255, 255, 255, 200), width=3)
    draw.line([cx - icon_sz + 5, cy, cx + icon_sz - 5, cy],
              fill=(255, 255, 255, 200), width=3)
    draw.line([cx, cy - icon_sz + 5, cx, cy + icon_sz - 5],
              fill=(255, 255, 255, 200), width=3)


def render_design(spec, output_path, product_data=None, width=1080):
    start = time.time()

    aspect = spec["canvas"]["aspect_ratio"]
    ratio_parts = [int(x) for x in aspect.split(":")]
    height = int(width * ratio_parts[1] / ratio_parts[0])

    bg_color = hr(spec["canvas"]["background_color"])
    cp = spec["color_palette"]
    ls = spec["layout_structure"]

    img = Image.new("RGBA", (width, height), (*bg_color, 255))
    draw = ImageDraw.Draw(img)

    bold_path, reg_path = find_fonts()

    FONT_HUGE = get_font(bold_path, reg_path, int(width * 0.045))
    FONT_LARGE = get_font(bold_path, reg_path, int(width * 0.035))
    FONT_MED = get_font(bold_path, reg_path, int(width * 0.025))
    FONT_SMALL = get_font(bold_path, reg_path, int(width * 0.018))
    FONT_BANNER = get_font(bold_path, reg_path, int(width * 0.028))
    FONT_PRICE = get_font(bold_path, reg_path, int(width * 0.04))
    FONT_FOOTER_BTN = get_font(bold_path, reg_path, int(width * 0.022))
    FONT_FOOTER_LABEL = get_font(bold_path, reg_path, int(width * 0.016), bold=False)
    FONT_FOOTER_VAL = get_font(bold_path, reg_path, int(width * 0.016))

    products = product_data or PRODUCT_DATA

    # ── HEADER ────────────────────────────────────────────────
    header_margin = int(width * 0.06)
    header_top = int(width * 0.05)
    title = ls["header"]["title"]
    colors_alt = title["color_alternation"]
    title_text = title["text"]

    # Split title into 3 lines with color alternation
    words = title_text.split()
    n = len(words)
    lines = [" ".join(words[:max(1, n//3)]),
             " ".join(words[max(1, n//3):max(1, 2*n//3)]),
             " ".join(words[max(1, 2*n//3):])]

    y_offset = header_top
    for i, line_text in enumerate(lines):
        c = colors_alt[i % len(colors_alt)]
        draw.text((header_margin, y_offset), line_text, fill=c, font=FONT_HUGE)
        y_offset += int(FONT_HUGE.size * 1.15)

    # ── DISCOUNT BADGE (pentagon) ─────────────────────────────
    badge = ls["header"]["discount_badge"]
    badge_sz = int(width * 0.09)
    bx = width - header_margin - badge_sz * 2
    by = header_top + badge_sz // 2
    draw_irregular_pentagon(draw, bx + badge_sz, by, badge_sz, badge["background_color"])

    badge_font = get_font(bold_path, reg_path, int(width * 0.025))
    bbox = draw.textbbox((0, 0), badge["text"], font=badge_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((bx + badge_sz - tw // 2, by - th // 2), badge["text"],
              fill=hr(badge["text_color"]), font=badge_font)

    # ── SUB-HEADER BANNER ─────────────────────────────────────
    banner = ls["sub_header_banner"]
    banner_y = y_offset + int(width * 0.04)
    banner_h = int(width * 0.07)
    banner_x = int(width * 0.04)
    banner_w = width - 2 * banner_x
    draw_rounded_rect(draw, (banner_x, banner_y, banner_x + banner_w, banner_y + banner_h),
                      radius=int(width * 0.015), fill=hr(banner["background_color"]))

    bbox = draw.textbbox((0, 0), banner["text"], font=FONT_BANNER)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((width // 2 - tw // 2, banner_y + (banner_h - th) // 2),
              banner["text"], fill=hr(banner["text_color"]), font=FONT_BANNER)

    # ── PRODUCT SECTIONS ──────────────────────────────────────
    section_top = banner_y + banner_h + int(width * 0.05)
    section_h = int(height * 0.2)
    section_gap = int(width * 0.03)
    margin_x = int(width * 0.06)

    sec_configs = ls["product_sections"]
    positions = [
        sec_configs["section_1"],
        sec_configs["section_2"],
        sec_configs["section_3"],
    ]

    for idx, prod in enumerate(products[:3]):
        pos = positions[idx]
        sy = section_top + idx * (section_h + section_gap)
        is_left = pos["product_position"] == "left"

        prod_x = margin_x if is_left else width // 2
        text_x = width // 2 + margin_x if is_left else margin_x
        prod_w = width // 2 - 2 * margin_x
        text_w = width // 2 - 2 * margin_x

        # Green blob behind product
        blob_cx = int(prod_x + prod_w // 2)
        blob_cy = int(sy + section_h // 2)
        draw_organic_blob(draw, blob_cx, blob_cy, prod_w, section_h,
                          cp["primary_accent"], alpha=140)

        # Dot pattern adjacent to blob
        dot_x = text_x + int(text_w * 0.3)
        dot_y = sy + int(section_h * 0.1)
        draw_dot_pattern(draw, dot_x, dot_y, int(text_w * 0.6), int(section_h * 0.4),
                         cp["dot_pattern"], spacing=int(width * 0.02),
                         radius=int(width * 0.003))

        # Product image placeholder
        pad = int(width * 0.025)
        ph = section_h - 2 * pad
        pw = int(ph * 1.1)
        draw_product_placeholder(draw,
                                  prod_x + (prod_w - pw) // 2,
                                  sy + pad, pw, ph,
                                  prod.get("color", "#7CB518"))

        # Text content
        tx = text_x + int(width * 0.02)
        ty = sy + int(width * 0.01)

        label_font = get_font(bold_path, reg_path, int(width * 0.016))
        draw.text((tx, ty), prod["label"], fill=hr(cp["text_primary"]), font=label_font)

        name_font = get_font(bold_path, reg_path, int(width * 0.028))
        draw.text((tx, ty + int(width * 0.035)), prod["name"],
                  fill=hr(cp["text_primary"]), font=name_font)

        price_font = get_font(bold_path, reg_path, int(width * 0.035))
        draw.text((tx, ty + int(width * 0.075)), prod["price"],
                  fill=hr(cp["price_color"]), font=price_font)

        desc_font = get_font(bold_path, reg_path, int(width * 0.016), bold=False)
        desc = prod["description"]
        words_d = desc.split()
        desc_lines = []
        for i in range(0, len(words_d), 10):
            desc_lines.append(" ".join(words_d[i:i+10]))
        dl_y = ty + int(width * 0.12)
        for dl in desc_lines[:4]:
            draw.text((tx, dl_y), dl, fill=hr(prod.get("color", "#555555")), font=desc_font)
            dl_y += int(desc_font.size * 1.3)

    # ── FOOTER ────────────────────────────────────────────────
    footer = ls["footer"]
    footer_h = int(height * 0.12)
    footer_y = height - footer_h
    draw.rectangle([(0, footer_y), (width, height)], fill=hr(footer["background_color"]))

    fe = footer["elements"]
    total_w = width - 2 * margin_x
    elem_w = total_w // len(fe)
    elem_h = footer_h // 2

    for i, el in enumerate(fe):
        ex = margin_x + i * elem_w
        ey = footer_y + (footer_h - elem_h) // 2

        if el["type"] == "cta_button":
            btn_w = int(elem_w * 0.7)
            btn_h = int(footer_h * 0.45)
            btn_x = ex + (elem_w - btn_w) // 2
            btn_y = ey + (elem_h - btn_h) // 2
            draw_rounded_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
                              radius=6, fill=hr(el["background_color"]))
            bbox = draw.textbbox((0, 0), el["text"], font=FONT_FOOTER_BTN)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text((btn_x + btn_w // 2 - tw // 2, btn_y + btn_h // 2 - th // 2),
                      el["text"], fill=hr(el["text_color"]), font=FONT_FOOTER_BTN)

        elif el["type"] == "contact_info":
            # Globe icon (simple circle)
            icon_r = int(width * 0.012)
            icon_cx = ex + int(elem_w * 0.2)
            icon_cy = ey + int(elem_h * 0.3)
            draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
                         outline=hr(el["icon_color"]), width=2)
            draw.line([icon_cx, icon_cy - icon_r, icon_cx, icon_cy + icon_r],
                      fill=hr(el["icon_color"]), width=1)
            draw.arc([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
                     0, 360, fill=hr(el["icon_color"]), width=1)

            label_x = ex + int(elem_w * 0.35)
            draw.text((label_x, ey), el["label"], fill=hr(el["text_color"]), font=FONT_FOOTER_LABEL)
            draw.text((label_x, ey + int(FONT_FOOTER_LABEL.size * 1.1)),
                      el["value"], fill=hr(el["text_color"]), font=FONT_FOOTER_VAL)

        elif el["type"] == "website_info":
            icon_r = int(width * 0.012)
            icon_cx = ex + int(elem_w * 0.2)
            icon_cy = ey + int(elem_h * 0.3)
            draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
                         outline=hr(el["icon_color"]), width=2)
            draw.line([icon_cx, icon_cy - icon_r, icon_cx, icon_cy + icon_r],
                      fill=hr(el["icon_color"]), width=1)
            draw.arc([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
                     0, 360, fill=hr(el["icon_color"]), width=1)

            label_x = ex + int(elem_w * 0.35)
            draw.text((label_x, ey), el["label"], fill=hr(el["text_color"]), font=FONT_FOOTER_LABEL)
            draw.text((label_x, ey + int(FONT_FOOTER_LABEL.size * 1.1)),
                      el["value"], fill=hr(el["text_color"]), font=FONT_FOOTER_VAL)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")

    elapsed = time.time() - start
    print(f"Design rendered in {elapsed:.2f}s")
    print(f"Saved: {output_path}")
    print(f"Size: {width}x{height} ({aspect})")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate catalog design illustration from JSON spec")
    parser.add_argument("--spec", help="JSON spec string (default: built-in discount catalogue spec)")
    parser.add_argument("--spec-file", type=Path, help="Path to JSON spec file")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--width", type=int, default=1080, help="Base width (height auto from aspect ratio)")
    parser.add_argument("--product-data", type=Path, help="JSON file with product data array")
    args = parser.parse_args()

    spec = DEFAULT_SPEC
    if args.spec:
        spec = json.loads(args.spec)
    elif args.spec_file:
        with open(args.spec_file) as f:
            spec = json.load(f)

    products = None
    if args.product_data:
        with open(args.product_data) as f:
            products = json.load(f)

    ok = render_design(spec, args.output, products, args.width)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
