#!/usr/bin/env python3
"""
generate_base.py — Venturo Poster Base Image Generator

Calls an AI image generation API to create the base poster artwork
based on an enriched prompt. Saves raw output to a temp path.

Usage:
    python generate_base.py --prompt "..." --output /path/to/output.png [--width 1024] [--height 1024]

Supports multiple backends:
    1. OpenAI DALL-E 3
    2. Anthropic (if available)
    3. Local fallback (generates a gradient placeholder)

The script resolves its own location so all paths are relative to the skill directory.
"""

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path

def get_skill_dir():
    return Path(__file__).resolve().parent.parent

def resolve_path(relative):
    return str(get_skill_dir() / relative)

def build_enriched_prompt(base_prompt, tier, aesthetics, lighting, bg_tone, text_copy):
    safe_zone = (
        "CRITICAL: The top 20% and bottom 20% of the image MUST be an uncluttered "
        "dark gradient area with no text, no detailed elements, no faces, and no logos. "
        "This space is reserved for branding overlay. "
        "Keep the center 60% visually rich with the main subject."
    )

    tier_keywords = {
        "starter": "Clean, minimalist, modern, approachable. Bright accents on dark background.",
        "growth": "Professional, interconnected, multi-device, data-driven dashboards. Corporate feel.",
        "enterprise": "High-tech, dark cyberpunk, data streams, network security, holographic elements."
    }

    enriched = (
        f"Professional marketing poster design for a software development company. "
        f"Service tier: {tier}. "
        f"Visual style: {tier_keywords.get(tier.lower(), 'Modern, professional')}. "
        f"Technical theme: {aesthetics}. "
        f"Human elements: {lighting}. "
        f"Background tone: {bg_tone}. "
        f"Safe zone instruction: {safe_zone} "
    )

    if text_copy and text_copy.strip():
        enriched += f"Text to feature in the design: '{text_copy}'. "

    enriched += (
        "High resolution, 8K quality, professional lighting, photorealistic details, "
        "cinematic composition. No watermarks. No text in safe zones."
    )

    return enriched

def call_openai_dalle(api_key, prompt, output_path, width=1024, height=1024):
    try:
        import openai
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai")
        return False

    try:
        client = openai.OpenAI(api_key=api_key)
        size_map = {(1024, 1024): "1024x1024", (1024, 1792): "1024x1792", (1792, 1024): "1792x1024"}
        size_str = size_map.get((width, height), "1024x1024")

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size_str,
            quality="hd",
            n=1,
        )

        image_url = response.data[0].url

        import urllib.request
        urllib.request.urlretrieve(image_url, output_path)
        print(f"Base image saved to {output_path}")
        return True

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return False

def call_anthropic(api_key, prompt, output_path, width=1024, height=1024):
    """Call Anthropic API for image generation if available."""
    try:
        import anthropic
    except ImportError:
        print("Anthropic SDK not available, trying curl fallback...")
        return False

    try:
        client = anthropic.Anthropic(api_key=api_key)
        # Anthropic image generation endpoint — adapt based on available API
        response = client.messages.create(
            model="claude-3-sonnet-image-20260601" if False else "claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        # Note: Actual implementation depends on API capabilities
        print("Anthropic generation attempted. Check output.")
        return False
    except Exception as e:
        print(f"Anthropic API error: {e}")
        return False

def generate_placeholder(output_path, width, height, tier="starter"):
    """Generate a gradient placeholder when no API is configured."""
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install Pillow")
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

    for i in range(3):
        center_x = width // 2 + (i - 1) * 200
        center_y = height // 2
        glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow)
        for r in range(300, 0, -10):
            alpha = max(0, 15 - (300 - r) // 20)
            glow_draw.ellipse(
                [center_x - r, center_y - r, center_x + r, center_y + r],
                fill=(int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16), alpha)
            )
        img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
        draw = ImageDraw.Draw(img)

    safe_zone = ImageDraw.Draw(img)
    safe_zone.rectangle([(0, 0), (width, int(height * 0.2))], fill=(0, 0, 0, 180))
    safe_zone.rectangle([(0, int(height * 0.85)), (width, height)], fill=(0, 0, 0, 180))

    img.save(output_path, "PNG", quality=95)
    print(f"Placeholder base image saved to {output_path} ({width}x{height})")
    return True

def main():
    parser = argparse.ArgumentParser(description="Generate Venturo poster base image")
    parser.add_argument("--prompt", required=True, help="Base prompt from the user interview")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--width", type=int, default=1024, help="Image width")
    parser.add_argument("--height", type=int, default=1024, help="Image height")
    parser.add_argument("--tier", default="starter", choices=["starter", "growth", "enterprise"],
                        help="Service tier for context mapping")
    parser.add_argument("--aesthetics", default="modern UI design", help="Technical aesthetics description")
    parser.add_argument("--lighting", default="professional studio lighting", help="Lighting & human elements")
    parser.add_argument("--bg-tone", default="dark cybertech", help="Background tone preference")
    parser.add_argument("--text-copy", default="", help="Headline or promo text")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    enriched = build_enriched_prompt(
        args.prompt, args.tier, args.aesthetics,
        args.lighting, args.bg_tone, args.text_copy
    )

    print(f"[generate_base] Enriched prompt ({len(enriched)} chars)")
    print(f"[generate_base] Tier: {args.tier}, Size: {args.width}x{args.height}")

    api_key_openai = os.environ.get("OPENAI_API_KEY")
    api_key_anthropic = os.environ.get("ANTHROPIC_API_KEY")

    success = False

    if api_key_openai:
        print("[generate_base] Using OpenAI DALL-E 3...")
        success = call_openai_dalle(api_key_openai, enriched, str(output_path), args.width, args.height)
    elif api_key_anthropic:
        print("[generate_base] Using Anthropic...")
        success = call_anthropic(api_key_anthropic, enriched, str(output_path), args.width, args.height)

    if not success:
        print("[generate_base] No API key found or API calls failed. Generating placeholder...")
        success = generate_placeholder(str(output_path), args.width, args.height, args.tier)

    if success:
        print(f"[generate_base] Done: {output_path}")
    else:
        print("[generate_base] FAILED to generate base image")
        sys.exit(1)

if __name__ == "__main__":
    main()
