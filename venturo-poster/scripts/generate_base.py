#!/usr/bin/env python3

import argparse
import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

# ── Config ─────────────────────────────────────────────────────

def load_config():
    cfg_path = PLUGIN_ROOT / "config" / "cookies.json"
    if not cfg_path.exists():
        return {"session_ids": [], "region": "sg"}
    try:
        with open(cfg_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"session_ids": [], "region": "sg"}


def build_prompt(base_prompt, tier, aesthetics, lighting, bg_tone):
    tier_hints = {
        "starter": "Clean, minimalist, modern. Bright teal/green accents.",
        "growth": "Professional, interconnected dashboards. Corporate feel.",
        "enterprise": "High-tech, dark cyberpunk, data streams, cybersecurity.",
    }
    return (
        f"Background visual untuk katalog WhatsApp Business — jasa pengembangan software. "
        f"Service tier: {tier}. "
        f"Gaya visual: {tier_hints.get(tier.lower(), 'Modern, profesional')}. "
        f"Tema teknis: {aesthetics}. "
        f"Human elements: {lighting}. "
        f"Background tone: {bg_tone}. "
        f"CRITICAL: Hanya background visual — JANGAN ada teks, JANGAN ada logo, JANGAN ada tulisan apapun. "
        f"Area tengah 70% harus bersih/soft agar teks terbaca. "
        f"Gunakan gradient halus, jangan terlalu ramai di tengah. "
        f"Format kotak 1:1 untuk katalog WhatsApp. "
        f"Kualitas tinggi, lighting profesional."
    )


def parse_region(raw):
    r = raw.lower()
    for prefix, code in [("us-", "us"), ("sg-", "sg"), ("hk-", "hk"), ("jp-", "jp")]:
        if r.startswith(prefix):
            return code, r[3:]
    return "sg", raw


# ── Playwright generation ──────────────────────────────────────

def generate_via_playwright(prompt, output_path, session_token, region="sg"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1400, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0.0.0 Safari/537.36",
            locale="zh-CN",
        )

        # Inject session cookies
        context.add_cookies([
            {"name": "sessionid", "value": session_token, "domain": ".capcut.com", "path": "/"},
            {"name": "sessionid_ss", "value": session_token, "domain": ".capcut.com", "path": "/"},
            {"name": "sid_tt", "value": session_token, "domain": ".capcut.com", "path": "/"},
            {"name": "store-region", "value": "hk", "domain": ".capcut.com", "path": "/"},
        ])

        page = context.new_page()
        page.goto("https://dreamina.capcut.com/ai-tool/generate/?type=image&workspace=0",
                  wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)

        # Dismiss any initial dialog (upsell, etc.)
        _dismiss_dialogs(page)

        # ── Fill prompt into TipTap editor ──
        editor = page.locator(".tiptap").first()
        editor.wait_for(state="visible", timeout=10000)
        editor.click()
        page.wait_for_timeout(200)
        # Use keyboard to clear and type
        editor.fill("")
        editor.type(prompt, delay=15)
        page.wait_for_timeout(500)

        # ── Set ratio 1:1 ──
        _set_ratio_to_1_1(page)

        # ── Click Generate ──
        gen_btn = page.locator("button.lv-btn-primary").last
        gen_btn.wait_for(state="visible", timeout=5000)

        if gen_btn.is_disabled():
            return False, "Generate button disabled"

        gen_btn.click()
        page.wait_for_timeout(2000)

        # ── Dismiss any post-click dialogs ──
        _dismiss_dialogs(page)

        # ── Wait for result ──
        ok, reason = _wait_for_result(page, output_path, timeout=180)
        if not ok:
            # Try again: maybe dialog appeared mid-generation
            _dismiss_dialogs(page)
            ok, reason = _wait_for_result(page, output_path, timeout=120)

        browser.close()
        return ok, reason


def _dismiss_dialogs(page):
    for _ in range(3):
        dialog_count = page.locator("dialog, [role='dialog']").count()
        if dialog_count == 0:
            return
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)


def _set_ratio_to_1_1(page):
    try:
        btn = page.locator('button:has-text("ratio")')
        if btn.count() == 0:
            return
        btn.click()
        page.wait_for_timeout(500)

        # Click "1:1" in the popover
        one_one = page.locator('text="1:1"').first
        if one_one.count() > 0:
            one_one.click()
            page.wait_for_timeout(300)

        # Close popover by clicking somewhere else
        page.locator(".tiptap").first.click()
        page.wait_for_timeout(300)
    except Exception:
        pass


def _wait_for_result(page, output_path, timeout=180):
    deadline = time.time() + timeout

    # Count initial history cards
    initial_cards = _count_image_cards(page)

    while time.time() < deadline:
        page.wait_for_timeout(3000)
        _dismiss_dialogs(page)

        cards = _count_image_cards(page)
        if cards > initial_cards:
            # New card appeared — get the image
            img_url = _get_latest_image_url(page)
            if img_url:
                page.goto(img_url, wait_until="networkidle")
                page.screenshot(path=output_path, full_page=False)
                # Ensure it's PNG
                _ensure_png(output_path)
                return True, f"OK (generated)"

        # Also check for any visible image in the DOM
        img_url = _get_latest_image_url(page)
        if img_url:
            try:
                resp = page.goto(img_url, wait_until="networkidle", timeout=15000)
                if resp and resp.ok:
                    page.screenshot(path=output_path, full_page=False)
                    _ensure_png(output_path)
                    return True, f"OK (from DOM)"
            except Exception:
                pass

    return False, "timeout"


def _count_image_cards(page):
    return page.evaluate("""
        () => document.querySelectorAll('[class*="image-card"], [class*="ImageCard"], [class*="card"] img').length
    """)


def _get_latest_image_url(page):
    return page.evaluate("""
        () => {
            const imgs = document.querySelectorAll('img[src*="ibyteimg"], img[src*="capcut"], img[src*="dreamina"]');
            for (const img of imgs) {
                if (img.src && img.src.startsWith('http') && img.naturalWidth > 100) return img.src;
            }
            return null;
        }
    """)


def _ensure_png(path):
    try:
        from PIL import Image
        img = Image.open(path)
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        if img.size != (1080, 1080):
            img = img.resize((1080, 1080), Image.LANCZOS)
        img.save(path, "PNG", quality=95)
    except ImportError:
        pass


# ── Fallback: placeholder ──────────────────────────────────────

def generate_placeholder(output_path, width=1080, height=1080, tier="starter"):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Pillow required. pip install Pillow")
        return False, "no pillow"

    img = Image.new("RGB", (width, height), "#0f172a")
    draw = ImageDraw.Draw(img)

    colors = {
        "starter": ("#06b6d4", "#10b981"),
        "growth": ("#3b82f6", "#8b5cf6"),
        "enterprise": ("#ef4444", "#f59e0b"),
    }
    c1, c2 = colors.get(tier.lower(), ("#06b6d4", "#10b981"))

    for y in range(height):
        ratio = y / height
        r = int(int(c1[1:3], 16) * (1 - ratio) + int(c2[1:3], 16) * ratio)
        g = int(int(c1[3:5], 16) * (1 - ratio) + int(c2[3:5], 16) * ratio)
        b = int(int(c1[5:7], 16) * (1 - ratio) + int(c2[5:7], 16) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    for y in range(int(height * 0.15)):
        a = int(80 * (1 - y / (height * 0.15)))
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, a))
    for y in range(int(height * 0.85), height):
        ratio = (y - height * 0.85) / (height * 0.15)
        a = int(80 * ratio)
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, a))

    for i in range(2):
        cx = width // 4 + i * width // 2
        cy = height // 2
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for r in range(200, 0, -10):
            a = max(0, 12 - (200 - r) // 17)
            gd.ellipse([cx - r, cy - r, cx + r, cy + r],
                       fill=(int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16), a))
        img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
        draw = ImageDraw.Draw(img)

    img.save(output_path, "PNG", quality=95)
    print("  placeholder fallback")
    return True, "OK (placeholder)"


# ── Main ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate Venturo catalog background via Dreamina browser automation")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1080)
    parser.add_argument("--tier", default="starter", choices=["starter", "growth", "enterprise"])
    parser.add_argument("--aesthetics", default="modern UI design")
    parser.add_argument("--lighting", default="professional studio lighting")
    parser.add_argument("--bg-tone", default="dark cybertech")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    enriched = build_prompt(args.prompt, args.tier, args.aesthetics, args.lighting, args.bg_tone)
    print(f"Prompt ({len(enriched)} chars)")
    print(f"Size: {args.width}x{args.height}")

    config = load_config()
    sessions = config.get("session_ids", [])
    region = config.get("region", "sg")

    ok = False
    reason = ""

    # ── Playwright Dreamina ─────────────────────────────────────
    if sessions:
        print(f"\nRegion: {region}")
        print(f"Sessions: {len(sessions)} loaded")

        for session in sessions:
            sid = session.strip()
            if not sid:
                continue
            r, token = parse_region(sid)
            print(f"\nLaunching browser...")
            print(f"  session={token[:12]}... region={region or r}")
            try:
                ok, reason = generate_via_playwright(enriched, str(output_path), token, region or r)
            except Exception as e:
                reason = f"exception: {e}"
                ok = False
            if ok:
                print(f"  ✓ {reason}")
                break
            print(f"  ✗ {reason}")
    else:
        print("\nNo Dreamina config. config/cookies.json not found or empty.")

    # ── Fallback: placeholder ───────────────────────────────────
    if not ok:
        print("  fallback → placeholder gradient")
        ok, reason = generate_placeholder(str(output_path), args.width, args.height, args.tier)
        if ok:
            print(f"  ✓ {reason}")

    if ok:
        print(f"\nDone: {output_path}")
    else:
        print(f"\nFAILED: {reason}")
        sys.exit(1)


if __name__ == "__main__":
    main()
