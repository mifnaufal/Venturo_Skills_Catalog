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
    "brand": {
        "name": "VENTURO",
        "tagline": "Software House Malang",
        "description": "Jasa Programmer & IT Outsourcing Profesional"
    },
    "color_palette": {
        "primary": "#006D79",
        "primary_light": "#009BAD",
        "primary_glow": "rgba(0, 155, 173, 0.15)",
        "dark": "#202020",
        "light_bg": "#F6F8F8",
        "white": "#FFFFFF",
        "heading": "#292929",
        "body": "#4B5563",
        "accent_gold": "#F59E0B",
        "footer_bg": "#202020",
        "footer_text": "#FFFFFF"
    },
    "layout_structure": {
        "header": {
            "style": "brand_bar",
            "height": "compact",
            "logo_text": "VENTURO",
            "logo_subtext": "Software House Malang",
            "cta_button": {
                "text": "Hubungi Kami",
                "color": "#FFFFFF",
                "bg_color": "#006D79",
                "shape": "rounded_pill"
            }
        },
        "hero": {
            "title": "Software House\nMalang dengan Talenta\nProgrammer Terbesar",
            "subtitle": "130+ talenta programmer siap membantu proyek IT Anda",
            "stat_1_label": "Dedicated IT Experts",
            "stat_1_value": "130+",
            "stat_2_label": "Successful Projects",
            "stat_2_value": "100+",
            "cta_text": "Mulai Konsultasi",
            "badge_text": "50% OFF hiring fee"
        },
        "service_sections": {
            "count": 3,
            "layout": "cards_vertical",
            "each_card": {
                "icon_style": "rounded_square",
                "icon_bg": "rgba(0, 155, 173, 0.12)",
                "card_bg": "#F6F8F8",
                "card_radius": 12
            }
        },
        "footer": {
            "background_color": "#202020",
            "height": "medium",
            "company": "Venturo Pro",
            "copyright": "© 2026 - The Biggest Programmer Resource in Malang, Jawa Timur",
            "elements": [
                {"type": "cta_button", "text": "Hubungi Kami", "background_color": "#006D79", "text_color": "#FFFFFF"},
                {"type": "contact_info", "icon": "phone", "icon_color": "#006D79", "label": "Kontak", "value": "0812-3456-7890", "text_color": "#FFFFFF"},
                {"type": "website_info", "icon": "globe", "icon_color": "#006D79", "label": "Website", "value": "www.venturo.id", "text_color": "#FFFFFF"}
            ],
            "layout": "horizontal_flex"
        }
    },
    "design_elements": {
        "accent_shapes": {"type": "rounded_blobs", "color": "#006D79", "opacity": 0.08, "usage": "section_decoration"},
        "typography": {"headings": "Montserrat Bold", "body": "sans-serif", "weights": {"bold": 800, "semibold": 600, "regular": 400}}
    }
}

TIER_DATA = [
    {
        "type": "starter",
        "label": "COCOK UNTUK UMKM",
        "name": "Starter Package",
        "price": "Rp20 Juta – Rp80 Juta",
        "description": "Website & mobile app sederhana. Sistem operasional untuk usaha mikro, kecil, dan startup. 1 Business Analyst + 1 Senior Software Engineer.",
        "timeline": "1–2 Bulan",
        "features": ["Website/Mobile App", "Sistem Operasional", "2 Tim Dedikasi"],
        "color": "#006D79"
    },
    {
        "type": "growth",
        "label": "COCOK UNTUK BERTUMBUH",
        "name": "Growth Package",
        "price": "Rp80 Juta – Rp250 Juta",
        "description": "Finance, HRIS, CRM, ERP, Inventory, WMS, Logistic, Sales, Production, Asset Management. 4 tim spesialis.",
        "timeline": "2–3 Bulan",
        "features": ["Finance/HRIS/CRM/ERP", "Inventory/WMS/Logistic", "4 Tim Spesialis"],
        "color": "#009BAD"
    },
    {
        "type": "enterprise",
        "label": "COCOK UNTUK ENTERPRISE",
        "name": "Enterprise Package",
        "price": "Mulai Rp250 Juta",
        "description": "AI, Big Data, cybersecurity, integrasi lintas sistem. Transformasi digital menyeluruh dengan 6 tim ahli + Penetration Tester.",
        "timeline": "3–6 Bulan",
        "features": ["AI & Big Data", "Cybersecurity", "6 Tim Ahli + Pentest"],
        "color": "#006D79"
    }
]


def hr(col):
    if col.startswith("rgba"):
        parts = col.replace("rgba(", "").replace(")", "").split(",")
        return (int(parts[0]), int(parts[1]), int(parts[2]), int(float(parts[3]) * 255))
    col = col.lstrip("#")
    if len(col) == 6:
        return tuple(int(col[i:i+2], 16) for i in (0, 2, 4)) + (255,)
    return (0, 0, 0, 255)


def find_fonts():
    bold_path = reg_path = None
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
            elif "geistmono" in n and not reg_path:
                reg_path = str(c)

    if not bold_path:
        for d in ["/System/Library/Fonts", "/Library/Fonts"]:
            for c in Path(d).rglob("*.ttf"):
                if "Helvetica-Bold" in c.name or "Arial Bold" in c.name:
                    bold_path = str(c)
                    break
    if not reg_path:
        for d in ["/System/Library/Fonts", "/Library/Fonts"]:
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


def draw_organic_blob(draw, cx, cy, w, h, color, alpha=20):
    base = hr(color)
    c = (base[0], base[1], base[2], min(alpha, 255))
    steps = 36
    pts = []
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        rx = w // 2 + int(w * 0.08 * math.sin(angle * 3))
        ry = h // 2 + int(h * 0.08 * math.cos(angle * 2.5))
        x = cx + int(rx * math.cos(angle))
        y = cy + int(ry * math.sin(angle))
        pts.append((x, y))
    if pts:
        draw.polygon(pts, fill=c)


def draw_icon_placeholder(draw, x, y, size, color, icon_type="code"):
    base = hr(color)
    bg = (base[0], base[1], base[2], 30)
    draw_rounded_rect(draw, (x, y, x + size, y + size), radius=10, fill=bg)
    cx, cy = x + size // 2, y + size // 2
    r = size // 5
    solid = (base[0], base[1], base[2], 255)
    if icon_type == "code":
        draw.line([cx - r, cy - r, cx - r, cy + r], fill=solid, width=3)
        draw.line([cx + r, cy - r, cx + r, cy + r], fill=solid, width=3)
        draw.line([cx - r, cy - r, cx + r, cy], fill=solid, width=3)
        draw.line([cx - r, cy + r, cx + r, cy], fill=solid, width=3)
    elif icon_type == "team":
        head_r = r // 2
        draw.ellipse([cx - head_r, cy - r, cx + head_r, cy - r + head_r * 2], fill=solid)
        body_top = cy - r + head_r * 2
        draw.arc([cx - r, body_top, cx + r, cy + r], 0, 180, fill=solid, width=2)
    elif icon_type == "chart":
        bar_w = r // 2
        gap = bar_w // 2
        heights = [int(r * 1.8), int(r * 1.2), int(r * 0.8)]
        for i, h in enumerate(heights):
            bx = cx - r + i * (bar_w + gap)
            draw.rectangle([bx, cy + r - h, bx + bar_w, cy + r], fill=solid)


def render_design(spec, output_path, product_data=None, width=1080):
    start = time.time()

    aspect = spec["canvas"]["aspect_ratio"]
    ratio_parts = [int(x) for x in aspect.split(":")]
    height = int(width * ratio_parts[1] / ratio_parts[0])

    bg_color = hr(spec["canvas"]["background_color"])
    cp = spec["color_palette"]
    ls = spec["layout_structure"]

    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    bold_path, reg_path = find_fonts()

    FONT_LOGO = get_font(bold_path, reg_path, int(width * 0.04))
    FONT_LOGO_SUB = get_font(bold_path, reg_path, int(width * 0.016), bold=False)
    FONT_HERO_TITLE = get_font(bold_path, reg_path, int(width * 0.05))
    FONT_HERO_SUB = get_font(bold_path, reg_path, int(width * 0.02), bold=False)
    FONT_STAT_NUM = get_font(bold_path, reg_path, int(width * 0.045))
    FONT_STAT_LABEL = get_font(bold_path, reg_path, int(width * 0.016), bold=False)
    FONT_SECTION = get_font(bold_path, reg_path, int(width * 0.032))
    FONT_CARD_TITLE = get_font(bold_path, reg_path, int(width * 0.024))
    FONT_CARD_PRICE = get_font(bold_path, reg_path, int(width * 0.022))
    FONT_CARD_BODY = get_font(bold_path, reg_path, int(width * 0.016), bold=False)
    FONT_CARD_LABEL = get_font(bold_path, reg_path, int(width * 0.014), bold=False)
    FONT_FEATURE = get_font(bold_path, reg_path, int(width * 0.015))
    FONT_BADGE = get_font(bold_path, reg_path, int(width * 0.018))
    FONT_CTA = get_font(bold_path, reg_path, int(width * 0.02))
    FONT_FOOTER = get_font(bold_path, reg_path, int(width * 0.016), bold=False)
    FONT_FOOTER_CP = get_font(bold_path, reg_path, int(width * 0.012), bold=False)

    margin = int(width * 0.055)
    primary = hr(cp["primary"])
    dark = hr(cp["dark"])

    tiers = product_data or TIER_DATA

    # ── HEADER BAR ─────────────────────────────────────────────
    header_h = int(width * 0.12)
    draw.rectangle([(0, 0), (width, header_h)], fill=(255, 255, 255, 255))
    draw.line([(0, header_h), (width, header_h)], fill=(*primary[:3], 30), width=1)

    logo_y = int(header_h * 0.25)
    draw.text((margin, logo_y), "VENTURO", fill=(*primary[:3], 255), font=FONT_LOGO)
    draw.text((margin, logo_y + int(FONT_LOGO.size * 0.9)),
              "Software House Malang", fill=(*primary[:3], 180), font=FONT_LOGO_SUB)

    cta = ls["header"]["cta_button"]
    cta_w = int(width * 0.22)
    cta_h = int(header_h * 0.45)
    cta_x = width - margin - cta_w
    cta_y = int((header_h - cta_h) / 2)
    draw_rounded_rect(draw, (cta_x, cta_y, cta_x + cta_w, cta_y + cta_h),
                      radius=cta_h // 2, fill=hr(cta["bg_color"]))
    bbox = draw.textbbox((0, 0), cta["text"], font=FONT_CTA)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cta_x + cta_w // 2 - tw // 2, cta_y + cta_h // 2 - th // 2),
              cta["text"], fill=hr(cta["color"]), font=FONT_CTA)

    # ── HERO SECTION ───────────────────────────────────────────
    hero = ls["hero"]
    hero_top = header_h + int(width * 0.04)
    hero_h = int(height * 0.28)

    # Decorative blob
    draw_organic_blob(draw, int(width * 0.7), hero_top + hero_h // 2,
                      width // 2, hero_h, cp["primary"], alpha=15)

    # Title
    title_lines = hero["title"].split("\n")
    ty = hero_top
    for line in title_lines:
        draw.text((margin, ty), line, fill=hr(cp["heading"]), font=FONT_HERO_TITLE)
        ty += int(FONT_HERO_TITLE.size * 1.15)

    # Subtitle
    ty += int(width * 0.01)
    draw.text((margin, ty), hero["subtitle"], fill=hr(cp["body"]), font=FONT_HERO_SUB)

    # Badge
    badge_y = ty + int(FONT_HERO_SUB.size * 1.5)
    badge_w = int(width * 0.32)
    badge_h = int(width * 0.05)
    draw_rounded_rect(draw, (margin, badge_y, margin + badge_w, badge_y + badge_h),
                      radius=badge_h // 2, fill=(*hr(cp["primary"])[:3], 255))
    bbox = draw.textbbox((0, 0), hero["badge_text"], font=FONT_BADGE)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((margin + badge_w // 2 - tw // 2, badge_y + badge_h // 2 - th // 2),
              hero["badge_text"], fill=(255, 255, 255, 255), font=FONT_BADGE)

    # Stats
    stats_top = badge_y + badge_h + int(width * 0.04)
    stat_w = (width - 2 * margin) // 2
    for i, (val, lbl) in enumerate([(hero["stat_1_value"], hero["stat_1_label"]),
                                     (hero["stat_2_value"], hero["stat_2_label"])]):
        sx = margin + i * stat_w
        draw.text((sx, stats_top), val, fill=(*primary[:3], 255), font=FONT_STAT_NUM)
        draw.text((sx, stats_top + int(FONT_STAT_NUM.size * 0.8)),
                  lbl, fill=hr(cp["body"]), font=FONT_STAT_LABEL)

    # ── PACKAGE CARDS SECTION ─────────────────────────────────
    cards_top = stats_top + int(FONT_STAT_NUM.size) + int(FONT_STAT_LABEL.size) + int(width * 0.05)
    card_h = int((height - cards_top - int(height * 0.14)) / 3) - int(width * 0.02)
    card_gap = int(width * 0.018)

    for idx, tier in enumerate(tiers[:3]):
        cy = cards_top + idx * (card_h + card_gap)
        card_color = hr(tier.get("color", cp["primary"]))

        # Card background
        draw_rounded_rect(draw, (margin, cy, width - margin, cy + card_h),
                          radius=10, fill=hr(cp["light_bg"]))

        # Left accent bar
        bar_w = int(width * 0.008)
        draw_rounded_rect(draw, (margin, cy, margin + bar_w, cy + card_h),
                          radius=3, fill=(*card_color[:3], 255))

        # Content
        cx = margin + int(width * 0.04)

        # Icon
        icon_sz = int(card_h * 0.35)
        icon_types = ["code", "team", "chart"]
        draw_icon_placeholder(draw, cx, cy + int(card_h * 0.15), icon_sz, tier.get("color", cp["primary"]), icon_types[idx])

        # Label
        ix = cx + icon_sz + int(width * 0.03)
        draw.text((ix, cy + int(card_h * 0.08)), tier["label"],
                  fill=(*card_color[:3], 200), font=FONT_CARD_LABEL)

        # Name
        draw.text((ix, cy + int(card_h * 0.08) + int(FONT_CARD_LABEL.size * 1.1)),
                  tier["name"], fill=(*card_color[:3], 255), font=FONT_CARD_TITLE)

        # Price
        draw.text((ix, cy + int(card_h * 0.08) + int(FONT_CARD_LABEL.size * 1.1) + int(FONT_CARD_TITLE.size * 1.15)),
                  tier["price"], fill=(*card_color[:3], 255), font=FONT_CARD_PRICE)

        # Description (2 lines)
        desc_words = tier["description"].split()
        desc_line1 = " ".join(desc_words[:min(len(desc_words), 12)])
        desc_line2 = " ".join(desc_words[min(len(desc_words), 12):])
        desc_y = cy + int(card_h * 0.08) + int(FONT_CARD_LABEL.size * 1.1) + int(FONT_CARD_TITLE.size * 1.15) + int(FONT_CARD_PRICE.size * 1.1)
        draw.text((ix, desc_y), desc_line1, fill=hr(cp["body"]), font=FONT_CARD_BODY)
        if desc_line2:
            draw.text((ix, desc_y + int(FONT_CARD_BODY.size * 1.2)),
                      desc_line2, fill=hr(cp["body"]), font=FONT_CARD_BODY)

        # Features with dots
        feat_x = cx + icon_sz + int(width * 0.03)
        feat_y = cy + card_h - int(card_h * 0.2)
        dot_r = int(width * 0.004)
        for fi, feat in enumerate(tier.get("features", [])):
            fx = feat_x + fi * int(width * 0.2)
            draw.ellipse([fx, feat_y - dot_r, fx + 2 * dot_r, feat_y + dot_r],
                         fill=(*card_color[:3], 255))
            draw.text((fx + int(width * 0.012), feat_y - int(FONT_FEATURE.size * 0.3)),
                      feat, fill=(*card_color[:3], 255), font=FONT_FEATURE)

    # ── FOOTER ────────────────────────────────────────────────
    footer = ls["footer"]
    footer_h = int(height * 0.13)
    footer_y = height - footer_h
    draw.rectangle([(0, footer_y), (width, height)], fill=hr(footer["background_color"]))

    fe = footer["elements"]
    elem_w = (width - 2 * margin) // len(fe)
    elem_h = footer_h // 2

    for i, el in enumerate(fe):
        ex = margin + i * elem_w
        ey = footer_y + (footer_h - elem_h) // 2

        if el["type"] == "cta_button":
            btn_w = int(elem_w * 0.75)
            btn_h = int(footer_h * 0.4)
            btn_x = ex + (elem_w - btn_w) // 2
            btn_y = ey + (elem_h - btn_h) // 2
            draw_rounded_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
                              radius=btn_h // 2, fill=hr(el["background_color"]))
            bbox = draw.textbbox((0, 0), el["text"], font=FONT_CTA)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text((btn_x + btn_w // 2 - tw // 2, btn_y + btn_h // 2 - th // 2),
                      el["text"], fill=hr(el["text_color"]), font=FONT_CTA)

        elif el["type"] == "contact_info":
            icon_r = int(width * 0.012)
            icon_cx = ex + int(elem_w * 0.2)
            icon_cy = ey + int(elem_h * 0.3)
            draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
                         outline=(*hr(el["icon_color"])[:3], 255), width=2)
            draw.line([icon_cx, icon_cy - icon_r, icon_cx, icon_cy + icon_r],
                      fill=(*hr(el["icon_color"])[:3], 255), width=1)
            label_x = ex + int(elem_w * 0.35)
            draw.text((label_x, ey), el["label"], fill=(255, 255, 255, 200), font=FONT_FOOTER)
            draw.text((label_x, ey + int(FONT_FOOTER.size * 1.2)),
                      el["value"], fill=hr(el["text_color"]), font=FONT_FOOTER)

        elif el["type"] == "website_info":
            icon_r = int(width * 0.012)
            icon_cx = ex + int(elem_w * 0.2)
            icon_cy = ey + int(elem_h * 0.3)
            draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
                         outline=(*hr(el["icon_color"])[:3], 255), width=2)
            label_x = ex + int(elem_w * 0.35)
            draw.text((label_x, ey), el["label"], fill=(255, 255, 255, 200), font=FONT_FOOTER)
            draw.text((label_x, ey + int(FONT_FOOTER.size * 1.2)),
                      el["value"], fill=hr(el["text_color"]), font=FONT_FOOTER)

    # Copyright line
    cp_y = footer_y + footer_h - int(FONT_FOOTER_CP.size * 1.5)
    cp_text = footer.get("copyright", "")
    bbox = draw.textbbox((0, 0), cp_text, font=FONT_FOOTER_CP)
    tw = bbox[2] - bbox[0]
    draw.text((width // 2 - tw // 2, cp_y), cp_text,
              fill=(255, 255, 255, 150), font=FONT_FOOTER_CP)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")

    elapsed = time.time() - start
    print(f"Design rendered in {elapsed:.2f}s")
    print(f"Saved: {output_path}")
    print(f"Size: {width}x{height} ({aspect})")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate Venturo-branded catalog design illustration")
    parser.add_argument("--spec", help="JSON spec string (default: Venturo brand spec)")
    parser.add_argument("--spec-file", type=Path, help="Path to JSON spec file")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--width", type=int, default=1080, help="Base width (height auto from aspect ratio)")
    parser.add_argument("--product-data", type=Path, help="JSON file with tier/package data array")
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
