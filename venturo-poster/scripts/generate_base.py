#!/usr/bin/env python3
"""
generate_base.py — LEGACY / DEPRECATED

Use generate_design.py instead (programmatic Pillow illustration).
This file kept for reference only — Dreamina browser automation path.
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


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


def generate_via_playwright(prompt, output_path, session_token, region="sg", reference_path=None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1400, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0.0.0 Safari/537.36",
            locale="zh-CN",
        )

        context.add_cookies([
            {"name": "sessionid", "value": session_token, "domain": ".capcut.com", "path": "/"},
            {"name": "sessionid_ss", "value": session_token, "domain": ".capcut.com", "path": "/"},
            {"name": "sid_tt", "value": session_token, "domain": ".capcut.com", "path": "/"},
            {"name": "store-region", "value": "hk", "domain": ".capcut.com", "path": "/"},
        ])

        page = context.new_page()
        page.goto("https://dreamina.capcut.com/ai-tool/home",
                  wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)

        _dismiss_dialogs(page)

        # ── Upload reference image ──
        if reference_path:
            ref_abs = str(Path(reference_path).resolve())
            if not Path(ref_abs).exists():
                print(f"  reference file not found: {ref_abs}")
            else:
                print(f"  uploading reference: {ref_abs}")
                uploaded = _upload_reference(page, ref_abs)
                if uploaded:
                    print(f"  ✓ reference uploaded")
                else:
                    print(f"  ✗ reference upload failed (skipped)")

        page.wait_for_timeout(1000)

        # ── Fill prompt into TipTap editor ──
        editor_ok = page.evaluate("""
            () => !!document.querySelector('.tiptap')
        """)
        if not editor_ok:
            return False, "editor not found"
        page.evaluate("""
            (prompt) => {
                const el = document.querySelector('.tiptap');
                if (el) {
                    el.focus();
                    if (el._tiptapEditor) {
                        el._tiptapEditor.commands.setContent(prompt);
                    } else {
                        el.innerHTML = '<p>' + prompt.replace(/\\n/g, '<br>') + '</p>';
                    }
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                }
            }
        """, prompt)
        page.wait_for_timeout(1000)

        # ── Set ratio 1:1 ──
        page.evaluate("""
            () => {
                const btns = document.querySelectorAll('button');
                for (const btn of btns) {
                    if (btn.textContent.includes('ratio') || btn.textContent.includes('Auto')) {
                        btn.click();
                        break;
                    }
                }
            }
        """)
        page.wait_for_timeout(500)

        page.evaluate("""
            () => {
                const items = document.querySelectorAll('[class*="option"], div, span');
                for (const el of items) {
                    if (el.textContent.trim() === '1:1' && el.offsetParent !== null) {
                        el.click();
                        break;
                    }
                }
            }
        """)
        page.wait_for_timeout(300)
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)

        # ── Click Generate ──
        clicked = page.evaluate("""
            () => {
                const btns = document.querySelectorAll('button');
                for (const btn of btns) {
                    if (btn.className.includes('primary') && !btn.disabled && btn.offsetParent !== null) {
                        btn.click();
                        return true;
                    }
                }
                return false;
            }
        """)
        if not clicked:
            return False, "Generate button not found or disabled"

        page.wait_for_timeout(2000)
        _dismiss_dialogs(page)

        # ── Wait for result ──
        ok, reason = _wait_for_result(page, output_path, timeout=180)
        if not ok:
            _dismiss_dialogs(page)
            ok, reason = _wait_for_result(page, output_path, timeout=120)

        browser.close()
        return ok, reason


def _upload_reference(page, filepath):
    try:
        file_input = page.query_selector('input[type="file"]')
        if file_input:
            file_input.set_input_files(filepath)
            page.wait_for_timeout(2000)
            return True

        btns = page.query_selector_all("button")
        for btn in btns:
            text = (btn.inner_text() or "").lower()
            if "image" in text or "upload" in text or "referen" in text:
                with page.expect_file_chooser() as fc_info:
                    btn.click()
                file_chooser = fc_info.value
                file_chooser.set_files(filepath)
                page.wait_for_timeout(2000)
                return True

        page.evaluate("""
            () => {
                const inp = document.createElement('input');
                inp.type = 'file';
                inp.accept = 'image/*';
                inp.style.display = 'none';
                document.body.appendChild(inp);
                inp.click();
            }
        """)
        with page.expect_file_chooser() as fc_info:
            page.evaluate("() => document.body.querySelector('input[type=\"file\"]').click()")
        file_chooser = fc_info.value
        file_chooser.set_files(filepath)
        page.wait_for_timeout(2000)
        return True

    except Exception as e:
        print(f"  upload error: {e}")
        return False


def _dismiss_dialogs(page):
    for _ in range(3):
        has_dialog = page.evaluate("() => !!document.querySelector('dialog, [role=\"dialog\"]')")
        if not has_dialog:
            return
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)


def _wait_for_result(page, output_path, timeout=180):
    deadline = time.time() + timeout

    while time.time() < deadline:
        page.wait_for_timeout(3000)
        _dismiss_dialogs(page)

        result = page.evaluate("""
            () => {
                const imgs = document.querySelectorAll('img');
                let best = null;
                let bestArea = 0;
                for (const img of imgs) {
                    const src = (img.src || '').toLowerCase();
                    if (!src) continue;
                    if (src.includes('avatar')) continue;
                    if (src.includes('icon')) continue;
                    const w = img.naturalWidth || 0;
                    const h = img.naturalHeight || 0;
                    const area = w * h;
                    if (area > 50000 && area > bestArea &&
                        (src.includes('ibyteimg.com') || src.includes('capcut') || src.includes('dreamina'))) {
                        best = img.src;
                        bestArea = area;
                    }
                }
                return best;
            }
        """)
        if result:
            try:
                import requests
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/142.0.0.0 Safari/537.36",
                    "Referer": "https://dreamina.capcut.com/",
                }
                resp = requests.get(result, headers=headers, timeout=30)
                if resp.status_code == 200:
                    with open(output_path, "wb") as f:
                        f.write(resp.content)
                    _ensure_png(output_path)
                    return True, "OK"
            except Exception:
                pass

    return False, "timeout"


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
    parser.add_argument("--reference", default=None,
                        help="Path to reference image (e.g. assets/image_1c155d.png) to upload before generation")
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
                ok, reason = generate_via_playwright(enriched, str(output_path), token, region or r, args.reference)
            except Exception as e:
                reason = f"exception: {e}"
                ok = False
            if ok:
                print(f"  ✓ {reason}")
                break
            print(f"  ✗ {reason}")
    else:
        print("\nNo Dreamina config. config/cookies.json not found or empty.")

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
