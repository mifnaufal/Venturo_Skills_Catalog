#!/usr/bin/env python3
"""
generate_base.py — Venturo WhatsApp Catalog Background Generator

Generates a 1080x1080 background via Dreamina (CapCut AI) API.
Fallback chain: dreamina-5.0 → dreamina-4.5 → dreamina-4.1 → gpt-image-2 → placeholder
Multi-session rotation: jika session kena limit, otomatis pindah session berikutnya.

Config: config/cookies.json — isi dengan session ID dari cookies dreamina.capcut.com

Usage:
    python generate_base.py \
        --prompt "..." \
        --tier starter \
        --output /path/to/output.png
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

MODEL_CHAIN = ["dreamina-5.0", "dreamina-4.5", "dreamina-4.1", "gpt-image-2"]
POLL_INTERVAL = 3
POLL_TIMEOUT = 180

def get_plugin_root():
    return Path(__file__).resolve().parent.parent

def load_config():
    cfg_path = get_plugin_root() / "config" / "cookies.json"
    if not cfg_path.exists():
        return {"api_url": "", "session_ids": []}

    try:
        with open(cfg_path) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"api_url": "", "session_ids": []}

def build_prompt(base_prompt, tier, aesthetics, lighting, bg_tone):
    tier_hints = {
        "starter": "Clean, minimalist, modern, approachable. Bright teal/green accents.",
        "growth": "Professional, interconnected, data-driven dashboards. Corporate feel.",
        "enterprise": "High-tech, dark cyberpunk, data streams, cybersecurity, holographic.",
    }

    prompt = (
        f"Background visual untuk katalog WhatsApp Business — jasa pengembangan software. "
        f"Service tier: {tier}. "
        f"Gaya visual: {tier_hints.get(tier.lower(), 'Modern, profesional')}. "
        f"Tema teknis: {aesthetics}. "
        f"Human elements: {lighting}. "
        f"Background tone: {bg_tone}. "
        f"CRITICAL: Hanya background visual — JANGAN ada teks, JANGAN ada logo, JANGAN ada tulisan apapun. "
        f"Area tengah 70% harus bersih/soft agar teks bisa dibaca ketika ditimpa. "
        f"Gunakan gradient halus, jangan terlalu ramai di bagian tengah. "
        f"Format kotak 1:1 untuk katalog WhatsApp. "
        f"Kualitas tinggi, resolusi 8K, lighting profesional."
    )
    return prompt

def call_dreamina(api_url, session_id, prompt, output_path, model="dreamina-5.0", ratio="1:1"):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {session_id}",
    }
    body = json.dumps({
        "prompt": prompt,
        "model": model,
        "ratio": ratio,
        "resolution": "2k",
    }).encode()

    submit_url = api_url.rstrip("/") + "/v1/images/generations"
    req = urllib.request.Request(submit_url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
    except Exception as e:
        return False, f"submit failed: {e}"

    task_id = result.get("task_id")
    if not task_id:
        return False, f"no task_id in response: {result}"

    status_url = api_url.rstrip("/") + f"/v1/images/tasks/{task_id}"
    deadline = time.time() + POLL_TIMEOUT

    while time.time() < deadline:
        time.sleep(POLL_INTERVAL)
        try:
            poll_req = urllib.request.Request(status_url, headers=headers)
            with urllib.request.urlopen(poll_req, timeout=15) as resp:
                status = json.loads(resp.read())
        except Exception as e:
            return False, f"poll failed: {e}"

        s = status.get("status", "")
        if s == "completed":
            images = status.get("images", [])
            if not images:
                return False, "completed but no images"
            try:
                urllib.request.urlretrieve(images[0], output_path)
                return True, f"OK (model={model})"
            except Exception as e:
                return False, f"download failed: {e}"
        elif s in ("failed", "error"):
            msg = status.get("error", status.get("message", "unknown error"))
            return False, f"generation failed: {msg}"
        elif s == "processing":
            progress = status.get("progress", 0)
            print(f"  progress: {progress}%")

    return False, "timeout"

def call_dalle(api_key, prompt, output_path, width=1080, height=1080):
    try:
        import openai
    except ImportError:
        return False, "openai not installed"

    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3", prompt=prompt,
            size="1024x1024", quality="hd", n=1,
        )
        urllib.request.urlretrieve(response.data[0].url, output_path)
        try:
            from PIL import Image
            img = Image.open(output_path)
            if img.size != (width, height):
                img = img.resize((width, height), Image.LANCZOS)
                img.save(output_path, "PNG", quality=95)
        except ImportError:
            pass
        return True, "OK (DALL-E)"
    except Exception as e:
        return False, f"DALL-E error: {e}"

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
    print(f"  placeholder fallback")
    return True, "OK (placeholder)"

def main():
    parser = argparse.ArgumentParser(description="Generate Venturo catalog background via Dreamina")
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
    api_url = config.get("api_url", "").strip()

    ok = False
    reason = ""

    # ── Dreamina API chain ──────────────────────────────────────
    if api_url and sessions:
        print(f"\nDreamina API: {api_url}")
        print(f"Sessions: {len(sessions)} loaded")

        for session in sessions:
            sid = session.strip()
            if not sid:
                continue
            for model in MODEL_CHAIN:
                print(f"  trying model={model} session={sid[:20]}...")
                ok, reason = call_dreamina(api_url, sid, enriched, str(output_path), model=model)
                if ok:
                    print(f"  ✓ {reason}")
                    break
                print(f"  ✗ {reason}")
            if ok:
                break
    else:
        print("\nNo Dreamina config. config/cookies.json not found or empty.")

    # ── Fallback: DALL-E ────────────────────────────────────────
    if not ok:
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            print("  fallback → DALL-E 3")
            ok, reason = call_dalle(api_key, enriched, str(output_path), args.width, args.height)
            if ok:
                print(f"  ✓ {reason}")

    # ── Final fallback: placeholder ─────────────────────────────
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
