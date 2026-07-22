#!/usr/bin/env python3

import argparse
import getpass
import os
import re
import sys
import time
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PLUGIN_ROOT / "assets" / "image_1c155d.png"
CONTEXT_PATH = PLUGIN_ROOT / "templates" / "packages_context.md"
OUTPUT_DIR = PLUGIN_ROOT / "output"


def load_context():
    raw = CONTEXT_PATH.read_text(encoding="utf-8")
    return raw


def extract_tier_themes(raw, tier_key):
    lines = raw.split("\n")
    in_tier = False
    themes = []
    keywords = ""
    capture_until_header = False
    for line in lines:
        stripped = line.strip()
        header_marker = f"### {tier_key} Package"
        if header_marker in stripped:
            in_tier = True
            continue
        if in_tier:
            if stripped.startswith("### ") and "Package" in stripped and header_marker not in stripped:
                break
            if stripped.startswith("## "):
                break
            if "**Prompt Keywords:**" in stripped:
                keywords = stripped.split("**Prompt Keywords:**")[-1].strip().strip("`")
                continue
            if stripped.startswith("- ") and "**" not in stripped:
                themes.append(stripped.lstrip("- "))
    return themes, keywords


def build_prompt(tier_name):
    tier_label = {"starter": "Starter", "growth": "Growth", "enterprise": "Enterprise"}
    team_info = {
        "starter": "1 Business Analyst + 1 Senior Software Engineer",
        "growth": "1 Business Analyst + 1 Senior Software Engineer + 1 UI/UX Designer + 1 QA Engineer",
        "enterprise": "1 Business Analyst + 1 Senior Software Engineer + 1 Intermediate Software Engineer + 1 UI/UX Designer + 1 QA Engineer + 1 Penetration Tester",
    }
    budget = {"starter": "Rp20 Juta – Rp80 Juta", "growth": "Rp80 Juta – Rp250 Juta", "enterprise": "Mulai Rp250 Juta"}
    ideal = {
        "starter": "UMKM, usaha mikro, perusahaan kecil, dan startup yang membutuhkan website, mobile application, atau sistem operasional sederhana",
        "growth": "Perusahaan bertumbuh yang membutuhkan Finance System, HRIS, CRM, ERP, Inventory, WMS, atau sistem operasional lainnya",
        "enterprise": "Perusahaan menengah hingga enterprise yang membutuhkan sistem berskala besar, integrasi lintas sistem, AI, Big Data, dan keamanan tingkat tinggi",
    }

    raw = load_context()
    themes, keywords = extract_tier_themes(raw, tier_label[tier_name])

    prompt = f"""Buat gambar katalog WhatsApp Business untuk paket {tier_label[tier_name]}.

VENTURO — Software House Malang
Paket: {tier_label[tier_name]}
Budget: {budget[tier_name]}
Ideal untuk: {ideal[tier_name]}
Tim: {team_info[tier_name]}

MASALAH YANG DISELESAIKAN:
- Perusahaan membutuhkan website/aplikasi yang sesuai dengan proses bisnisnya
- Aplikasi berlangganan tidak mampu memenuhi kebutuhan operasional
- Sulit melakukan kustomisasi karena keterbatasan sistem
- Sistem tidak dapat terintegrasi dengan layanan lain
- Tampilan aplikasi kurang user-friendly

SOLUSI:
- Pengembangan Website & Mobile Application (Android & iOS) khusus sesuai kebutuhan
- Analisis bisnis untuk memastikan fitur mendukung proses operasional
- Desain UI/UX modern, responsif, dan mudah digunakan
- Integrasi dengan ERP, CRM, HRIS, Payment Gateway, WhatsApp, API
- Dashboard monitoring dan reporting

HASIL:
- Aplikasi sesuai kebutuhan dan proses bisnis perusahaan
- Efisiensi operasional melalui digitalisasi dan otomatisasi
- Sistem fleksibel dan mudah dikembangkan
- Pengalaman pengguna yang lebih baik

VISUAL THEMES:"""

    for theme in themes:
        prompt += f"\n- {theme}"

    if keywords:
        prompt += f"\n\nSTYLE KEYWORDS: {keywords}"

    prompt += """

BRAND & DESAIN:
- Nama: Venturo — Software House Malang
- Warna Primer: #006D79 (teal)
- Warna Sekunder: #009BAD (light teal)
- Warna Gelap: #202020
- Background: #FFFFFF
- Heading: #292929
- Body Text: #4B5563

DESIGN RULES:
- WhatsApp Business catalog image, square 1:1
- Clean, professional, modern, minimal
- Bahasa Indonesia untuk semua teks
- Gunakan referensi logo yang diupload — tempatkan logo Venturo secara natural di area yang bersih
- Tampilkan: nama paket, range harga, tim, fitur utama
- Tidak boleh ada elemen 3D, foto stok, atau gambar generik
- Flat design dengan tipografi bold condensed sans-serif yang jelas"""

    return prompt


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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return str(OUTPUT_DIR / f"dreamina_{tier_name}.png")


def prompt_credentials():
    print("=" * 60)
    print("  DREAMINA LOGIN CREDENTIALS")
    print("=" * 60)
    email = input("  Email: ").strip()
    password = getpass.getpass("  Password: ").strip()
    return email, password


def auto_login(page, email, password):
    print("\n" + "=" * 60)
    print("  AUTO-LOGIN")
    print("=" * 60)

    sign_in_selectors = [
        "button:has-text('Sign in')",
        "button:has-text('Log in')",
        "button:has-text('Login')",
        "button:has-text('Masuk')",
        "button:has-text('Sign In')",
        "a:has-text('Sign in')",
        "a:has-text('Log in')",
        "span:has-text('Sign in')",
        "div[class*='login'] button",
        "div[class*='sign-in'] button",
        "div[class*='signin'] button",
    ]

    clicked_signin = False
    for sel in sign_in_selectors:
        try:
            btn = page.query_selector(sel)
            if btn and btn.is_visible():
                btn.click()
                clicked_signin = True
                print(f"  Clicked sign-in button: {sel}")
                break
        except Exception:
            continue

    if not clicked_signin:
        print("  Could not find sign-in button. Trying to detect login form directly...")

    page.wait_for_timeout(5000)

    login_fields_found = False
    current_url = page.url
    print(f"  Current URL: {current_url}")

    email_selectors = [
        "input[type='email']",
        "input[name='email']",
        "input[name='account']",
        "input[placeholder*='email']",
        "input[placeholder*='Email']",
        "input[placeholder*='Email']",
        "input[placeholder*='account']",
        "input[autocomplete='username']",
        "input[autocomplete='email']",
    ]

    password_selectors = [
        "input[type='password']",
        "input[name='password']",
        "input[placeholder*='password']",
        "input[placeholder*='Password']",
        "input[placeholder*='Kata Sandi']",
        "input[autocomplete='current-password']",
    ]

    email_el = None
    for sel in email_selectors:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                email_el = el
                print(f"  Found email field: {sel}")
                break
        except Exception:
            continue

    password_el = None
    for sel in password_selectors:
        try:
            el = page.query_selector(sel)
            if el and el.is_visible():
                password_el = el
                print(f"  Found password field: {sel}")
                break
        except Exception:
            continue

    if email_el and password_el:
        login_fields_found = True
        try:
            email_el.click()
            page.wait_for_timeout(300)
            email_el.fill(email)
            print("  Email filled")
        except Exception as e:
            print(f"  Failed to fill email: {e}")

        try:
            password_el.click()
            page.wait_for_timeout(300)
            password_el.fill(password)
            print("  Password filled")
        except Exception as e:
            print(f"  Failed to fill password: {e}")

        submit_selectors = [
            "button[type='submit']",
            "button:has-text('Sign in')",
            "button:has-text('Log in')",
            "button:has-text('Login')",
            "button:has-text('Masuk')",
            "button:has-text('Continue')",
            "button:has-text('Lanjutkan')",
            "button:has-text('Submit')",
            "button[class*='submit']",
            "button[class*='login']",
            "button[class*='sign-in']",
        ]

        for sel in submit_selectors:
            try:
                btn = page.query_selector(sel)
                if btn and btn.is_visible():
                    btn.click()
                    print(f"  Submit clicked: {sel}")
                    break
            except Exception:
                continue

        page.wait_for_timeout(5000)

    try:
        page.wait_for_url(re.compile(r"/ai-tool/"), timeout=30000)
        print("  Login successful! Detected at /ai-tool/")
        return True
    except Exception:
        pass

    try:
        page.wait_for_url(re.compile(r"dreamina\.capcut\.com/(home|ai-tool|create)"), timeout=30000)
        print("  Login detected! Redirected to Dreamina.")
        return True
    except Exception:
        pass

    if login_fields_found:
        print("  Auto-login attempted but could not verify success.")
    else:
        print("  Could not find login form.")

    return False


def process_tier(browser, tier_name, output_path, prompt, timeout_ms, email=None, password=None):
    page = browser.new_page()
    page.set_viewport_size({"width": 1280, "height": 800})

    print(f"\n{'=' * 60}")
    print(f"  Tier: {tier_name.upper()}")
    print(f"  Output: {output_path}")
    print(f"{'=' * 60}")

    page.goto("https://dreamina.capcut.com/", wait_until="domcontentloaded")

    if email and password:
        logged_in = auto_login(page, email, password)
        if not logged_in:
            print("\n  Auto-login gagal. Silakan login manual.")
            input("  Press Enter once logged in...")
    else:
        print("\n" + "=" * 60)
        print("  MANUAL LOGIN")
        print("=" * 60)
        print("  1. A browser window is open to Dreamina")
        print("  2. Log in with your ByteDance/Dreamina account")
        print("  3. Press Enter once logged in")
        print("=" * 60 + "\n")
        input("  Press Enter once logged in...")

    page.goto("https://dreamina.capcut.com/ai-tool/image", wait_until="domcontentloaded")
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
        description="Generate Dreamina catalog image with auto-login + logo reference"
    )
    parser.add_argument("--tier", choices=["starter", "growth", "enterprise", "all"],
                        default="starter", help="Which tier to generate")
    parser.add_argument("--output", "-o", default=None,
                        help="Output PNG path (default: venturo-poster/output/dreamina_<tier>.png)")
    parser.add_argument("--prompt", "-p", default=None,
                        help="Custom prompt (overrides auto-generated)")
    parser.add_argument("--prompt-file", type=Path,
                        help="Read prompt from text file")
    parser.add_argument("--timeout", type=int, default=180000,
                        help="Max wait in ms for generation (default: 180000 = 3 min)")
    parser.add_argument("--no-logo", action="store_true",
                        help="Skip logo reference upload")
    parser.add_argument("--manual-login", action="store_true",
                        help="Skip auto-login, user logs in manually")
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

    email = password = None
    if not args.manual_login:
        email, password = prompt_credentials()
        print()

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
                    prompt = build_prompt(tier)

            out_path = resolve_output_path(tier, args.output)
            process_tier(browser, tier, out_path, prompt, args.timeout, email, password)

        browser.close()

    print("\nDone!")


if __name__ == "__main__":
    main()
