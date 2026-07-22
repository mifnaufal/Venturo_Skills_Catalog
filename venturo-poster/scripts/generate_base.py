#!/usr/bin/env python3
"""
generate_base.py — Venturo WhatsApp Catalog Background Generator

Generates a 1080x1080 background image for WhatsApp Business catalog cards
using an AI image generation API (DALL-E 3 / Anthropic), with a fallback
to a gradient placeholder.

Usage:
    python generate_base.py \
        --prompt "..." \
        --tier starter \
        --output /path/to/output.png

The script resolves its own location so all paths are relative to the plugin root.
"""

import argparse
import os
import sys
import urllib.request
from pathlib import Path

def get_plugin_root():
    return Path(__file__).resolve().parent.parent

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

def call_dalle(api_key, prompt, output_path, width=1080, height=1080):
    try:
        import openai
    except ImportError:
        return False

    try:
        client = openai.OpenAI(api_key=api_key)
        size_str = "1024x1024"  # DALL-E only supports specific sizes, we'll resize later

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size_str,
            quality="hd",
            n=1,
        )
        image_url = response.data[0].url
        urllib.request.urlretrieve(image_url, output_path)

        # Resize to 1080x1080 if needed
        try:
            from PIL import Image
            img = Image.open(output_path)
            if img.size != (width, height):
                img = img.resize((width, height), Image.LANCZOS)
                img.save(output_path, "PNG", quality=95)
        except ImportError:
            pass

        print(f"AI background saved: {output_path} ({width}x{height})")
        return True
    except Exception as e:
        print(f"DALL-E error: {e}")
        return False

def generate_placeholder(output_path, width=1080, height=1080, tier="starter"):
    """Gradient placeholder for dev/testing."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        print("Pillow required. pip install Pillow")
        return False

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

    # Darken edges for text readability
    for y in range(int(height * 0.15)):
        alpha = int(80 * (1 - y / (height * 0.15)))
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
    for y in range(int(height * 0.85), height):
        ratio = (y - height * 0.85) / (height * 0.15)
        alpha = int(80 * ratio)
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

    # Surface glow
    for i in range(2):
        cx, cy = width // 4 + i * width // 2, height // 2
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        for r in range(200, 0, -10):
            a = max(0, 12 - (200 - r) // 17)
            gd.ellipse([cx - r, cy - r, cx + r, cy + r],
                       fill=(int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16), a))
        img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
        draw = ImageDraw.Draw(img)

    # Vignette
    for r in range(max(width, height) // 2, 0, -3):
        a = max(0, 60 - (max(width, height) // 2 - r) // 8)
        center = (width // 2, height // 2)
        draw.ellipse([center[0] - r, center[1] - r, center[0] + r, center[1] + r],
                     outline=(0, 0, 0, 0), fill=None)

    img.save(output_path, "PNG", quality=95)
    print(f"Placeholder background: {output_path} ({width}x{height})")
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate Venturo catalog background")
    parser.add_argument("--prompt", required=True, help="Base prompt")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--width", type=int, default=1080, help="Image width")
    parser.add_argument("--height", type=int, default=1080, help="Image height")
    parser.add_argument("--tier", default="starter", choices=["starter", "growth", "enterprise"])
    parser.add_argument("--aesthetics", default="modern UI design")
    parser.add_argument("--lighting", default="professional studio lighting")
    parser.add_argument("--bg-tone", default="dark cybertech")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    enriched = build_prompt(args.prompt, args.tier, args.aesthetics, args.lighting, args.bg_tone)
    print(f"Prompt ({len(enriched)} chars)")

    api_key = os.environ.get("OPENAI_API_KEY")
    ok = call_dalle(api_key, enriched, str(output_path), args.width, args.height) if api_key else False

    if not ok:
        print("No API key. Generating placeholder...")
        ok = generate_placeholder(str(output_path), args.width, args.height, args.tier)

    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
