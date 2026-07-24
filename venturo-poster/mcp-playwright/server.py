#!/usr/bin/env python3

import base64
import io
import logging
import os
import re
import sys
import time
from pathlib import Path

from PIL import Image, ImageFilter

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Venturo Poster — Cloudflare Workers AI")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("venturo-poster")

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PLUGIN_ROOT / "assets" / "image_1c155d.png"
OUTPUT_DIR = PLUGIN_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── .env loader ──────────────────────────────────────────────────────────────
_ENV_PATH = PLUGIN_ROOT.parent / ".env"
if _ENV_PATH.exists():
    with open(_ENV_PATH) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip("\"'"))

# ── Configuration ────────────────────────────────────────────────────────────
WORKER_URL = os.environ.get("CLOUDFLARE_WORKER_URL", "")
WORKER_API_KEY = os.environ.get("CLOUDFLARE_API_KEY", "")  # key used to authenticate with Worker
IMAGE_ROUTER_API_KEY = os.environ.get("IMAGE_ROUTER_API_KEY", "")  # legacy, kept for backwards compat

CANVAS_WIDTH = int(os.environ.get("CANVAS_WIDTH", "1400"))
CANVAS_HEIGHT = int(os.environ.get("CANVAS_HEIGHT", "1024"))


def _get_logo_b64() -> str:
    """Return Venturo logo as a base64 string for image_input."""
    if not LOGO_PATH.exists():
        raise FileNotFoundError(f"Logo not found at {LOGO_PATH}")
    return base64.b64encode(LOGO_PATH.read_bytes()).decode()


def _logo_data_uri() -> str:
    """Return Venturo logo as a data URI for image_input."""
    return f"data:image/png;base64,{_get_logo_b64()}"



def _call_cloudflare_ai(
    prompt: str,
    aspect_ratio: str = "1:1",
    resolution: str = "1K",
    include_logo: bool = True,
) -> bytes:
    """Call Cloudflare Worker and return image bytes."""
    if not WORKER_URL:
        raise ValueError("CLOUDFLARE_WORKER_URL not set.")

    payload = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "resolution": resolution,
    }

    if include_logo:
        try:
            payload["image_input"] = [_logo_data_uri()]
        except FileNotFoundError as exc:
            logger.warning("Logo not found, skipping image_input: %s", exc)

    headers = {"Content-Type": "application/json"}
    if WORKER_API_KEY:
        headers["X-API-Key"] = WORKER_API_KEY

    logger.info("Calling Worker: %s with prompt length=%d", WORKER_URL, len(prompt))
    resp = requests.post(WORKER_URL, json=payload, headers=headers, timeout=180)
    resp.raise_for_status()

    # Worker returns raw PNG bytes directly
    img_bytes = resp.content
    if not img_bytes:
        raise ValueError(f"Empty image bytes received from Worker")

    return img_bytes


def _create_padded_canvas(img: Image.Image, target_width: int, target_height: int) -> Image.Image:
    """Create a canvas with white space on the right side.

    The generated image is resized to fit the LEFT portion of the canvas.
    The RIGHT portion remains blank white for Pillow overlay later.
    """
    # Create white canvas
    canvas = Image.new("RGBA", (target_width, target_height), (255, 255, 255, 255))

    # Resize original image to fit left portion
    left_width = int(target_width * 0.65)  # 65% of canvas width
    # Maintain aspect ratio while fitting in left portion
    img_ratio = img.width / img.height
    paste_height = min(target_height, left_width)
    paste_width = int(paste_height * img_ratio)
    paste_width = min(paste_width, left_width)

    # Ensure we don't exceed left portion
    if paste_width > left_width:
        paste_width = left_width
        paste_height = int(paste_width / img_ratio)

    img_resized = img.resize((paste_width, paste_height), Image.LANCZOS)

    # Center vertically on left side of canvas
    x_offset = 0
    y_offset = (target_height - paste_height) // 2

    # Paste with alpha support
    canvas.paste(img_resized, (x_offset, y_offset), img_resized)

    logger.info(
        "Canvas %dx%d | Image pasted at (%d,%d) size %dx%d | Right space %d px free",
        target_width, target_height, x_offset, y_offset, paste_width, paste_height,
        target_width - paste_width,
    )
    return canvas


# ── MCP Tools ────────────────────────────────────────────────────────────────

@mcp.tool()
async def generate_catalog(
    prompt: str,
    tier: str = "starter",
    resolution: str = "1K",
    aspect_ratio: str = "1:1",
    include_logo: bool = True,
) -> str:
    """Generate a WhatsApp Business catalog image for a Venturo package tier.

    Sends the prompt + Venturo logo to Cloudflare Workers AI
    and returns a catalog image on a 1400x1024 canvas with a blank right-side space
    (~35%) ready for Pillow overlay (logo/text/QR code).
    """
    try:
        img_bytes = _call_cloudflare_ai(
            prompt=prompt,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            include_logo=include_logo,
        )
    except ValueError as exc:
        return f"Config error: {exc}"
    except requests.exceptions.Timeout:
        return "Error: Request timed out after 180s."
    except requests.exceptions.RequestException as exc:
        detail = ""
        if hasattr(exc, "response") and exc.response is not None:
            try:
                detail = exc.response.json()
            except Exception:
                detail = str(exc.response.text[:500])
        return f"Error calling Cloudflare AI API: {exc}\nResponse: {detail}"
    except Exception as exc:
        return f"Error: {exc}"

    # Open and process image
    try:
        img = Image.open(io.BytesIO(img_bytes)).convert("RGBA")
    except Exception as exc:
        return f"Error decoding image from API response: {exc}"

    # Create padded canvas with right-side white space
    canvas = _create_padded_canvas(img, CANVAS_WIDTH, CANVAS_HEIGHT)

    # Save
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"venturo-{tier}-{timestamp}.png"
    output_path = OUTPUT_DIR / filename
    canvas.save(output_path, "PNG")
    logger.info("Catalog saved to %s", output_path)
    return f"Catalog image generated: {output_path}"


@mcp.tool()
async def check_balance() -> str:
    """Check if the Worker is reachable and responding."""
    if not WORKER_URL:
        return "Config error: CLOUDFLARE_WORKER_URL not set."

    try:
        resp = requests.post(WORKER_URL, json={"prompt": "test"}, timeout=10)
        if resp.status_code == 200:
            # Got image bytes — worker is healthy
            size = len(resp.content)
            return f"Worker is healthy. Response size: {size} bytes."
        elif resp.status_code == 400:
            # Prompt empty error (expected for test prompt? maybe not)
            return f"Worker responded with {resp.status_code}. Might need a valid prompt for test."
        else:
            return f"Worker returned status {resp.status_code}: {resp.text[:300]}"
    except Exception as exc:
        return f"Error reaching Worker: {exc}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
