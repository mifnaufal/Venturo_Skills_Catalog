#!/usr/bin/env python3
"""
composite_logo.py — Venturo Logo Compositing Script

Overlays the official Venturo logo (image_1c155d.png) onto a base poster image.
Positioning: Bottom-Right (default) or Top-Right, with 5% dynamic padding.

Usage:
    python composite_logo.py --input /path/to/base.png --output /path/to/final.png
                            [--position bottom-right] [--logo-scale 0.12]

The script resolves its own location so all asset paths are relative.
Completes in under 3 seconds on modern hardware.
"""

import argparse
import os
import sys
import time
from pathlib import Path

def get_skill_dir():
    return Path(__file__).resolve().parent.parent

def resolve_asset(relative):
    return str(get_skill_dir() / relative)

def composite_logo(
    base_path: str,
    output_path: str,
    position: str = "bottom-right",
    logo_scale: float = 0.12,
) -> bool:
    """
    Overlay the Venturo logo onto the base image.

    Args:
        base_path: Path to the generated base poster
        output_path: Where to save the composited result
        position: 'bottom-right' or 'top-right'
        logo_scale: Logo width relative to base image width (0.0-1.0)

    Returns:
        True on success, False on failure
    """
    start = time.time()

    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow is required. Install with: pip install Pillow")
        return False

    logo_path = resolve_asset("assets/image_1c155d.png")

    if not os.path.exists(logo_path):
        print(f"ERROR: Logo not found at {logo_path}")
        print("Place the Venturo logo PNG at assets/image_1c155d.png")
        return False

    if not os.path.exists(base_path):
        print(f"ERROR: Base image not found at {base_path}")
        return False

    try:
        base = Image.open(base_path).convert("RGBA")
        logo = Image.open(logo_path).convert("RGBA")
    except Exception as e:
        print(f"ERROR: Failed to open images: {e}")
        return False

    base_w, base_h = base.size

    new_logo_w = int(base_w * logo_scale)
    aspect = logo.height / logo.width
    new_logo_h = int(new_logo_w * aspect)

    logo_resized = logo.resize((new_logo_w, new_logo_h), Image.LANCZOS)

    padding = int(base_w * 0.05)

    if position == "bottom-right":
        x = base_w - new_logo_w - padding
        y = base_h - new_logo_h - padding
    elif position == "top-right":
        x = base_w - new_logo_w - padding
        y = padding
    elif position == "bottom-left":
        x = padding
        y = base_h - new_logo_h - padding
    elif position == "top-left":
        x = padding
        y = padding
    else:
        print(f"Unknown position: {position}. Using bottom-right.")
        x = base_w - new_logo_w - padding
        y = base_h - new_logo_h - padding

    if logo_resized.mode == "RGBA":
        base.paste(logo_resized, (x, y), logo_resized)
    else:
        base.paste(logo_resized, (x, y))

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    base.save(output_path, "PNG", optimize=True)

    elapsed = time.time() - start
    print(f"Logo composited at {position} (x={x}, y={y}) in {elapsed:.2f}s")
    print(f"Final poster saved to: {output_path}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Composite Venturo logo onto poster")
    parser.add_argument("--input", required=True, help="Path to base image")
    parser.add_argument("--output", required=True, help="Path for final composited image")
    parser.add_argument("--position", default="bottom-right",
                        choices=["bottom-right", "top-right", "bottom-left", "top-left"],
                        help="Logo anchor position")
    parser.add_argument("--logo-scale", type=float, default=0.12,
                        help="Logo width relative to base image (0.0-1.0)")
    args = parser.parse_args()

    success = composite_logo(args.input, args.output, args.position, args.logo_scale)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
