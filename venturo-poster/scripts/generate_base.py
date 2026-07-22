#!/usr/bin/env python3

import argparse
import os
import re
import sys
import time
from pathlib import Path


def get_plugin_root():
    return Path(__file__).resolve().parent.parent


LOGO_PATH = get_plugin_root() / "assets" / "image_1c155d.png"

DREAMINA_CONTEXT = {
    "starter": (
        "Paket STARTER (Rp20-80 Juta). "
        "Ideal untuk UMKM dan startup. "
        "Tim: 1 Business Analyst + 1 Senior Software Engineer. "
        "Layanan: website & mobile app sederhana, sistem operasional."
    ),
    "growth": (
        "Paket GROWTH (Rp80-250 Juta). "
        "Ideal untuk perusahaan bertumbuh. "
        "Tim: 1 BA + 1 Senior SE + 1 UI/UX Designer + 1 QA Engineer. "
        "Sistem: Finance, HRIS, CRM, ERP, Inventory, WMS."
    ),
    "enterprise": (
        "Paket ENTERPRISE (Mulai Rp250 Juta). "
        "Ideal untuk enterprise. "
        "Tim: 6 ahli + Penetration Tester. "
        "Layanan: AI, Big Data, cybersecurity, integrasi lintas sistem."
    ),
}

BRAND_PROMPT = """
BRAND: Venturo — Software House Malang
PRIMARY COLOR: #006D79 (teal)
SECONDARY: #009BAD (light teal)
DARK: #202020

DESIGN RULES:
- WhatsApp Business catalog image, square 1:1
- Clean, professional, modern, minimal
- Bahasa Indonesia untuk semua teks
- Sertakan: nama paket, range harga, fitur utama, tim, timeline
- Gunakan referensi logo yang diupload — tempatkan logo Venturo secara natural di area yang bersih
- Tidak boleh ada elemen 3D, foto stok, atau gambar generik
- Flat design dengan tipografi yang jelas
"""


def build_prompt(tier_name, context):
    return (
        f"Buat gambar katalog WhatsApp Business untuk {tier_name.upper()}.\n\n"
        f"KONTEN:\n{context}\n"
        f"{BRAND_PROMPT}"
    )


def find_file_input(page):
    selectors = [
        "input[type='file']",
        "input[accept*='image']",
        "input[accept*='png']",
    ]
    for sel in selectors:
        try:
            el = page.query_selector(sel)
            if el:
                return el
        except Exception:
            continue
    return None


def try_upload_reference(page, logo_path):
    if not logo_path.exists():
        print(f"  Logo not found at {logo_path}, skipping auto-upload")
        return False

    upload_selectors = [
        "input[type='file']",
        "div[class*='upload'] input",
        "div[class*='reference'] input",
        "div[class*='image-input'] input",
        "button[class*='upload']",
        "div[class*='img-input']",
        "div[role='button']:has-text('upload')",
        "div[aria-label*='upload']",
    ]

    for sel in upload_selectors:
        try:
            el = page.query_selector(sel)
            if el:
                tag = el.evaluate("el => el.tagName.toLowerCase()")
                if tag == "input":
                    el.set_input_files(str(logo_path))
                    print(f"  Logo uploaded via file input: {sel}")
                    return True
                else:
                    el.click()
                    page.wait_for_timeout(1000)
                    file_input = find_file_input(page)
                    if file_input:
                        file_input.set_input_files(str(logo_path))
                        print(f"  Logo uploaded after clicking: {sel}")
                        return True
        except Exception:
            continue
    return False


def resolve_output_path(tier_name, output_arg):
    if output_arg:
        return output_arg
    return f"dreamina_{tier_name}.png"


def process_tier(browser, tier_name, output_path, prompt, timeout_ms):
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 800})

    print(f"\n{'=' * 60}")
    print(f"  Tier: {tier_name.upper()}")
    print(f"  Output: {output_path}")
    print(f"{'=' * 60}")

    page.goto("https://dreamina.jianying.com/", wait_until="domcontentloaded")

    print("\n" + "=" * 60)
    print("  MANUAL LOGIN")
    print("=" * 60)
    print("  1. A browser window is open to Dreamina")
    print("  2. Log in with your ByteDance/Dreamina account")
    print("  3. Script auto-detects login, or press Enter to continue")
    print("=" * 60 + "\n")

    try:
        page.wait_for_url(re.compile(r"/ai-tool/"), timeout=120000)
        print("  Login detected!")
    except Exception:
        print("  Login timeout (2min). Continuing...")
        input("  Press Enter once logged in...")

    page.goto("https://dreamina.jianying.com/ai-tool/image", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)

    print("\n" + "=" * 60)
    print("  UPLOAD LOGO REFERENCE")
    print("=" * 60)
    uploaded = try_upload_reference(page, LOGO_PATH)
    if not uploaded:
        print("  Could not auto-upload logo.")
        print(f"  Please upload this file manually as reference image:")
        print(f"    {LOGO_PATH}")
        input("  Press Enter after uploading the logo...")
    else:
        print("  Logo reference uploaded successfully!")

    print("\n" + "=" * 60)
    print("  PROMPT")
    print("=" * 60)
    print(f"  {prompt[:200]}...")
    print("=" * 60 + "\n")

    prompt_filled = False
    selectors = [
        "textarea",
        "[contenteditable='true']",
        ".ql-editor",
        "div[class*='prompt'] div[contenteditable]",
        "div[class*='input'] textarea",
        "div[class*='editor'] div[contenteditable]",
    ]
    for sel in selectors:
        try:
            el = page.query_selector(sel)
            if el:
                el.click()
                page.wait_for_timeout(500)
                el.fill(prompt)
                prompt_filled = True
                print(f"  Prompt filled via: {sel}")
                break
        except Exception:
            continue

    if not prompt_filled:
        print("  Could not auto-fill prompt.")
        print(f"  Paste this prompt manually:\n")
        print(f"  {prompt}\n")
        input("  Press Enter after pasting...")

    gen_selectors = [
        "button:has-text('Generate')",
        "button:has-text('Buat')",
        "button:has-text('Create')",
        "button[class*='generate']",
        "button[class*='submit']",
        "div[class*='generate'] button",
    ]
    clicked = False
    if prompt_filled:
        for sel in gen_selectors:
            try:
                btn = page.query_selector(sel)
                if btn:
                    btn.click()
                    clicked = True
                    print(f"  Generate clicked via: {sel}")
                    break
            except Exception:
                continue

    if not clicked:
        print("  Could not auto-click Generate.")
        print("  Please paste prompt + upload logo + click Generate manually.")
        input("  Press Enter after starting generation...")

    print(f"\n  Waiting up to {timeout_ms // 1000}s for generation...")
    try:
        page.wait_for_timeout(timeout_ms)
    except Exception:
        pass

    print("\n  Saving result...")
    try:
        page.screenshot(path=output_path, full_page=True)
        print(f"  Saved: {output_path}")
    except Exception as e:
        print(f"  Screenshot failed: {e}")

    page.close()


def main():
    parser = argparse.ArgumentParser(
        description="Generate Dreamina catalog image with manual login + logo reference"
    )
    parser.add_argument("--tier", choices=["starter", "growth", "enterprise", "all"],
                        default="starter", help="Which tier to generate")
    parser.add_argument("--output", "-o", default=None,
                        help="Output PNG path (default: ./dreamina_<tier>.png)")
    parser.add_argument("--prompt", "-p", default=None,
                        help="Custom prompt (overrides auto-generated)")
    parser.add_argument("--prompt-file", type=Path,
                        help="Read prompt from text file")
    parser.add_argument("--timeout", type=int, default=180000,
                        help="Max wait in ms for generation (default: 180000 = 3 min)")
    parser.add_argument("--no-logo", action="store_true",
                        help="Skip logo reference upload")
    args = parser.parse_args()

    if not LOGO_PATH.exists():
        print(f"WARNING: Venturo logo not found at {LOGO_PATH}")
        print("  The AI won't be able to include the logo automatically.")
        print("  Upload it manually or use --no-logo to skip.\n")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: Playwright not installed.")
        print("  pip install playwright && playwright install chromium")
        sys.exit(1)

    tiers_to_run = ["starter", "growth", "enterprise"] if args.tier == "all" else [args.tier]

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ]
        )

        for tier in tiers_to_run:
            prompt = args.prompt
            if not prompt:
                if args.prompt_file and args.prompt_file.exists():
                    prompt = args.prompt_file.read_text()
                else:
                    prompt = build_prompt(tier, DREAMINA_CONTEXT.get(tier, ""))

            out_path = resolve_output_path(tier, args.output)
            process_tier(browser, tier, out_path, prompt, args.timeout)

        browser.close()

    print("\nDone!")


if __name__ == "__main__":
    main()
