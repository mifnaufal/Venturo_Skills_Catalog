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
        "orientation": "square",
        "background_color": "#FFFFFF",
        "aspect_ratio": "1:1"
    },
    "brand": {
        "name": "VENTURO",
        "tagline": "Software House Malang",
        "description": "Jasa Programmer & IT Outsourcing Profesional"
    },
    "color_palette": {
        "primary": "#006D79",
        "primary_light": "#009BAD",
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
        "features": ["Finance/HRIS/CRM", "Inventory/WMS", "4 Tim Spesialis"],
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
            p = Path(d)
            if p.exists():
                for c in p.rglob("*.ttf"):
                    if "Helvetica-Bold" in c.name or "Arial Bold" in c.name:
                        bold_path = str(c)
                        break
    if not reg_path:
        for d in ["/System/Library/Fonts", "/Library/Fonts"]:
            p = Path(d)
            if p.exists():
                for c in p.rglob("*.ttf"):
                    if "Helvetica" in c.name and "Bold" not in c.name:
                        reg_path = str(c)
                        break
    return bold_path or "DejaVuSans-Bold.ttf", reg_path or "DejaVuSans.ttf"


def get_font(bold_path, reg_path, size, bold=True):
    try:
        return ImageFont.truetype(bold_path if bold else reg_path, size)
    except Exception:
        return ImageFont.load_default()


def text_wrap(draw, text, font, max_w):
    words = text.split()
    if not words:
        return [""]
    lines = []
    current = words[0]
    for w in words[1:]:
        test = current + " " + w
        bbox = draw.textbbox((0, 0), test, font=font)
        tw = bbox[2] - bbox[0]
        if tw <= max_w:
            current = test
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


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


def draw_icon_placeholder(draw, x, y, size, color, icon_type="code", lw=3):
    base = hr(color)
    bg = (base[0], base[1], base[2], 30)
    draw_rounded_rect(draw, (x, y, x + size, y + size), radius=size // 6, fill=bg)
    cx, cy = x + size // 2, y + size // 2
    r = size // 5
    solid = (base[0], base[1], base[2], 255)
    if icon_type == "code":
        draw.line([cx - r, cy - r, cx - r, cy + r], fill=solid, width=lw)
        draw.line([cx + r, cy - r, cx + r, cy + r], fill=solid, width=lw)
        draw.line([cx - r, cy - r, cx + r, cy], fill=solid, width=lw)
        draw.line([cx - r, cy + r, cx + r, cy], fill=solid, width=lw)
    elif icon_type == "team":
        head_r = r // 2
        draw.ellipse([cx - head_r, cy - r, cx + head_r, cy - r + head_r * 2], fill=solid)
        body_top = cy - r + head_r * 2
        draw.arc([cx - r, body_top, cx + r, cy + r], 0, 180, fill=solid, width=lw)
    elif icon_type == "chart":
        bar_w = r // 2
        gap = bar_w // 2
        heights = [int(r * 1.8), int(r * 1.2), int(r * 0.8)]
        for i, h in enumerate(heights):
            bx = cx - r + i * (bar_w + gap)
            draw.rectangle([bx, cy + r - h, bx + bar_w, cy + r], fill=solid)


def render_design(spec, output_path, product_data=None, size=3840):
    start = time.time()

    width = height = size
    bg_color = hr(spec["canvas"]["background_color"])
    cp = spec["color_palette"]
    ls = spec["layout_structure"]

    img = Image.new("RGBA", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    bold_path, reg_path = find_fonts()

    s = width
    FONT_LOGO = get_font(bold_path, reg_path, int(s * 0.04))
    FONT_LOGO_SUB = get_font(bold_path, reg_path, int(s * 0.016), bold=False)
    FONT_HERO_TITLE = get_font(bold_path, reg_path, int(s * 0.05))
    FONT_HERO_SUB = get_font(bold_path, reg_path, int(s * 0.02), bold=False)
    FONT_STAT_NUM = get_font(bold_path, reg_path, int(s * 0.045))
    FONT_STAT_LABEL = get_font(bold_path, reg_path, int(s * 0.016), bold=False)
    FONT_CARD_TITLE = get_font(bold_path, reg_path, int(s * 0.024))
    FONT_CARD_PRICE = get_font(bold_path, reg_path, int(s * 0.022))
    FONT_CARD_BODY = get_font(bold_path, reg_path, int(s * 0.016), bold=False)
    FONT_CARD_LABEL = get_font(bold_path, reg_path, int(s * 0.014), bold=False)
    FONT_FEATURE = get_font(bold_path, reg_path, int(s * 0.015))
    FONT_BADGE = get_font(bold_path, reg_path, int(s * 0.018))
    FONT_CTA = get_font(bold_path, reg_path, int(s * 0.02))
    FONT_FOOTER_LBL = get_font(bold_path, reg_path, int(s * 0.016), bold=False)
    FONT_FOOTER_VAL = get_font(bold_path, reg_path, int(s * 0.016))
    FONT_FOOTER_CP = get_font(bold_path, reg_path, int(s * 0.012), bold=False)

    margin = int(s * 0.055)
    primary = hr(cp["primary"])
    lw_base = max(2, s // 360)

    tiers = product_data or TIER_DATA

    # ── HEADER BAR ─────────────────────────────────────────────
    header_h = int(s * 0.12)
    draw.rectangle([(0, 0), (width, header_h)], fill=(255, 255, 255, 255))
    draw.line([(0, header_h), (width, header_h)], fill=(*primary[:3], 30), width=lw_base)

    logo_y = int(header_h * 0.22)
    draw.text((margin, logo_y), "VENTURO", fill=(*primary[:3], 255), font=FONT_LOGO)
    sub_y = logo_y + FONT_LOGO.size
    if sub_y + FONT_LOGO_SUB.size < header_h:
        draw.text((margin, sub_y), "Software House Malang",
                  fill=(*primary[:3], 180), font=FONT_LOGO_SUB)

    cta = ls["header"]["cta_button"]
    cta_w = int(s * 0.18)
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

    # ── HERO SECTION (dynamic) ─────────────────────────────────
    hero = ls["hero"]
    hero_top = header_h + int(s * 0.04)
    gy = hero_top

    # Title
    title_lines = hero["title"].split("\n")
    for line in title_lines:
        draw.text((margin, gy), line, fill=hr(cp["heading"]), font=FONT_HERO_TITLE)
        gy += int(FONT_HERO_TITLE.size * 1.15)

    # Subtitle
    gy += int(s * 0.01)
    draw.text((margin, gy), hero["subtitle"], fill=hr(cp["body"]), font=FONT_HERO_SUB)
    gy += int(FONT_HERO_SUB.size * 1.6)

    # Badge
    badge_w = int(s * 0.22)
    badge_h = int(s * 0.04)
    draw_rounded_rect(draw, (margin, gy, margin + badge_w, gy + badge_h),
                      radius=badge_h // 2, fill=(*primary[:3], 255))
    bbox = draw.textbbox((0, 0), hero["badge_text"], font=FONT_BADGE)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((margin + badge_w // 2 - tw // 2, gy + badge_h // 2 - th // 2),
              hero["badge_text"], fill=(255, 255, 255, 255), font=FONT_BADGE)
    gy += badge_h + int(s * 0.05)

    # Stats
    stat_w = (width - 2 * margin) // 2
    for i, (val, lbl) in enumerate([(hero["stat_1_value"], hero["stat_1_label"]),
                                     (hero["stat_2_value"], hero["stat_2_label"])]):
        sx = margin + i * stat_w
        draw.text((sx, gy), val, fill=(*primary[:3], 255), font=FONT_STAT_NUM)
        draw.text((sx, gy + int(FONT_STAT_NUM.size * 0.8)),
                  lbl, fill=hr(cp["body"]), font=FONT_STAT_LABEL)
    gy += int(FONT_STAT_NUM.size) + int(FONT_STAT_LABEL.size) + int(s * 0.04)

    # Decorative blob (hero right side)
    hero_content_h = gy - hero_top
    draw_organic_blob(draw, int(s * 0.75), hero_top + hero_content_h // 2,
                      s // 2, hero_content_h, cp["primary"], alpha=15)

    # ── PACKAGE CARDS SECTION (dynamic) ────────────────────────
    cards_top = gy
    footer_h = int(s * 0.12)
    cards_bottom = height - footer_h - int(s * 0.03)
    avail_h = cards_bottom - cards_top
    card_gap = int(s * 0.015)
    num_cards = min(len(tiers[:3]), 3)
    card_h = int((avail_h - card_gap * (num_cards - 1)) / num_cards)

    for idx, tier in enumerate(tiers[:num_cards]):
        cy = cards_top + idx * (card_h + card_gap)
        card_color = hr(tier.get("color", cp["primary"]))
        accent = (card_color[0], card_color[1], card_color[2], 255)

        # Card bg
        draw_rounded_rect(draw, (margin, cy, width - margin, cy + card_h),
                          radius=12, fill=hr(cp["light_bg"]))

        # Left accent bar
        bar_w = max(3, int(s * 0.006))
        draw_rounded_rect(draw, (margin, cy, margin + bar_w, cy + card_h),
                          radius=3, fill=accent)

        cx = margin + int(s * 0.035)

        # Icon (clamped)
        icon_sz = min(int(card_h * 0.35), int(s * 0.055))
        icon_types = ["code", "team", "chart"]
        draw_icon_placeholder(draw, cx, cy + int(card_h * 0.12), icon_sz,
                              tier.get("color", cp["primary"]), icon_types[idx], lw=max(2, lw_base))

        # Text column
        ix = cx + icon_sz + int(s * 0.025)
        content_right = width - margin - int(s * 0.035)
        text_max_w = content_right - ix

        # Label
        draw.text((ix, cy + int(card_h * 0.07)), tier["label"],
                  fill=(*card_color[:3], 200), font=FONT_CARD_LABEL)
        ty = cy + int(card_h * 0.07) + int(FONT_CARD_LABEL.size * 1.2)

        # Name
        draw.text((ix, ty), tier["name"], fill=accent, font=FONT_CARD_TITLE)
        ty += int(FONT_CARD_TITLE.size * 1.2)

        # Price
        draw.text((ix, ty), tier["price"], fill=accent, font=FONT_CARD_PRICE)
        ty += int(FONT_CARD_PRICE.size * 1.2)

        # Description (width-wrapped)
        desc_lines = text_wrap(draw, tier["description"], FONT_CARD_BODY, text_max_w)
        for dl in desc_lines[:4]:
            draw.text((ix, ty), dl, fill=hr(cp["body"]), font=FONT_CARD_BODY)
            ty += int(FONT_CARD_BODY.size * 1.3)

        # Feature tags (below description, with dynamic gap)
        ty += int(s * 0.008)
        dot_r = max(3, s // 240)
        for fi, feat in enumerate(tier.get("features", [])):
            fx = ix + fi * int(s * 0.18)
            draw.ellipse([fx - dot_r, ty - dot_r // 2, fx + dot_r, ty + dot_r // 2],
                         fill=accent)
            draw.text((fx + int(s * 0.01), ty - int(FONT_FEATURE.size * 0.4)),
                      feat, fill=accent, font=FONT_FEATURE)

    # ── FOOTER ────────────────────────────────────────────────
    footer = ls["footer"]
    footer_y = height - footer_h
    draw.rectangle([(0, footer_y), (width, height)], fill=hr(footer["background_color"]))

    fe = footer["elements"]
    elem_w = (width - 2 * margin) // len(fe)

    for i, el in enumerate(fe):
        ex = margin + i * elem_w
        ey = footer_y + int(footer_h * 0.12)

        if el["type"] == "cta_button":
            btn_w = int(elem_w * 0.6)
            btn_h = int(footer_h * 0.4)
            btn_x = ex + (elem_w - btn_w) // 2
            btn_y = ey + int(footer_h * 0.05)
            draw_rounded_rect(draw, (btn_x, btn_y, btn_x + btn_w, btn_y + btn_h),
                              radius=btn_h // 2, fill=hr(el["background_color"]))
            bbox = draw.textbbox((0, 0), el["text"], font=FONT_CTA)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            draw.text((btn_x + btn_w // 2 - tw // 2, btn_y + btn_h // 2 - th // 2),
                      el["text"], fill=hr(el["text_color"]), font=FONT_CTA)

        elif el["type"] == "contact_info":
            icon_r = int(s * 0.01)
            icon_cx = ex + int(elem_w * 0.18)
            icon_cy = ey + int(footer_h * 0.15)
            col = hr(el["icon_color"])
            draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
                         outline=(*col[:3], 255), width=lw_base)
            draw.line([icon_cx, icon_cy - icon_r, icon_cx, icon_cy + icon_r],
                      fill=(*col[:3], 255), width=lw_base)
            label_x = ex + int(elem_w * 0.28)
            draw.text((label_x, ey), el["label"], fill=(255, 255, 255, 200), font=FONT_FOOTER_LBL)
            draw.text((label_x, ey + int(FONT_FOOTER_LBL.size * 1.3)),
                      el["value"], fill=hr(el["text_color"]), font=FONT_FOOTER_VAL)

        elif el["type"] == "website_info":
            icon_r = int(s * 0.01)
            icon_cx = ex + int(elem_w * 0.18)
            icon_cy = ey + int(footer_h * 0.15)
            draw.ellipse([icon_cx - icon_r, icon_cy - icon_r, icon_cx + icon_r, icon_cy + icon_r],
                         outline=(*hr(el["icon_color"])[:3], 255), width=lw_base)
            label_x = ex + int(elem_w * 0.28)
            draw.text((label_x, ey), el["label"], fill=(255, 255, 255, 200), font=FONT_FOOTER_LBL)
            draw.text((label_x, ey + int(FONT_FOOTER_LBL.size * 1.3)),
                      el["value"], fill=hr(el["text_color"]), font=FONT_FOOTER_VAL)

    # Copyright
    cp_y = footer_y + footer_h - int(FONT_FOOTER_CP.size * 1.6)
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
    print(f"Size: {width}x{height}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate Venturo-branded catalog design illustration")
    parser.add_argument("--spec", help="JSON spec string")
    parser.add_argument("--spec-file", type=Path, help="Path to JSON spec file")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--size", type=int, default=3840, help="Canvas width/height in px (default 3840 = 4K)")
    parser.add_argument("--product-data", type=Path, help="JSON file with tier/package data")
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

    ok = render_design(spec, args.output, products, args.size)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
