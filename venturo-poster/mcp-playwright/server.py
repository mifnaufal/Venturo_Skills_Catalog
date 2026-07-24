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
CLOUDFLARE_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
CLOUDFLARE_AUTH_TOKEN = os.environ.get("CLOUDFLARE_AUTH_TOKEN", "")
CLOUDFLARE_MODEL = os.environ.get("CLOUDFLARE_MODEL", "google/nano-banana-2-lite")
IMAGE_ROUTER_API_KEY = os.environ.get("IMAGE_ROUTER_API_KEY", "")  # legacy, kept for backwards compat

CANVAS_WIDTH = int(os.environ.get("CANVAS_WIDTH", "1400"))
CANVAS_HEIGHT = int(os.environ.get("CANVAS_HEIGHT", "1024"))

AI_API_BASE = "https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"


def _get_api_url() -> str:
    if not CLOUDFLARE_ACCOUNT_ID or not CLOUDFLARE_MODEL:
        raise ValueError("CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_MODEL must be set.")
    return AI_API_BASE.format(account_id=CLOUDFLARE_ACCOUNT_ID, model=CLOUDFLARE_MODEL)


def _get_auth_headers() -> dict:
    if not CLOUDFLARE_AUTH_TOKEN:
        raise ValueError("CLOUDFLARE_AUTH_TOKEN not set.")
    return {"Authorization": f"Bearer {CLOUDFLARE_AUTH_TOKEN}", "Content-Type": "application/json"}


def _logo_data_uri() -> str:
    """Return Venturo logo as a data URI for image_input."""
    if not LOGO_PATH.exists():
        raise FileNotFoundError(f"Logo not found at {LOGO_PATH}")
    data = LOGO_PATH.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:image/png;base64,{b64}"


def _parse_image_from_response(content_value) -> bytes | None:
    """Extract image bytes from Cloudflare AI response value field.

    Possible formats depending on model:
    - { image: "base64string" } (binary image returned as base64)
    - A base64 string directly
    """
    if isinstance(content_value, str):
        # Might be base64-encoded image
        try:
            return base64.b64decode(content_value)
        except Exception:
            return None
    if isinstance(content_value, dict):
        if "image" in content_value:
            return base64.b64decode(content_value["image"])
        if "data" in content_value:
            return base64.b64decode(content_value["data"]) if isinstance(content_value["data"], str) else None
    return None


def _call_cloudflare_ai(
    prompt: str,
    aspect_ratio: str = "1:1",
    resolution: str = "1K",
    include_logo: bool = True,
) -> bytes:
    """Call Cloudflare Workers AI HTTP API and return image bytes."""
    api_url = _get_api_url()
    auth_headers = _get_auth_headers()

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

    logger.info("Calling Cloudflare AI: %s with prompt length=%d", api_url, len(prompt))
    resp = requests.post(api_url, json=payload, headers=auth_headers, timeout=180)
    resp.raise_for_status()

    data = resp.json()

    # Cloudflare AI API returns structured response:
    # { success: true, result: { ... }, errors: [...], messages: [...] }
    # Image models typically put image data in result.data or result.result
    if not data.get("success"):
        errors = data.get("errors", [])
        error_msgs = "; ".join(e.get("message", "") for e in errors) if errors else "Unknown error"
        raise ValueError(f"Cloudflare AI API failed: {error_msgs}\nFull response: {data}")

    result = data.get("result", {})
    # Cloudflare AI image models return image as result.image (base64)
    # Sometimes nested in result.data or as a list
    content_value = result.get("image") or result.get("data") or result.get("result")
    if isinstance(content_value, list) and len(content_value) > 0:
        content_value = content_value[0]

    img_bytes = _parse_image_from_response(content_value)
    if img_bytes is None:
        # Fallback: treat as base64 directly
        raw_str = str(content_value) if content_value else str(result)
        try:
            img_bytes = base64.b64decode(raw_str)
        except Exception:
            raise ValueError(f"Could not extract image from response: {data}")

    if not img_bytes:
        raise ValueError(f"Empty image bytes received from API")

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
    """Check if Cloudflare AI API is reachable and the model is available."""
    if not CLOUDFLARE_AUTH_TOKEN:
        return "Config error: CLOUDFLARE_AUTH_TOKEN not set."
    if not CLOUDFLARE_ACCOUNT_ID:
        return "Config error: CLOUDFLARE_ACCOUNT_ID not set."

    try:
        auth_headers = {"Authorization": f"Bearer {CLOUDFLARE_AUTH_TOKEN}", "Content-Type": "application/json"}

        # Check if model is available
        model_url = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/models/{CLOUDFLARE_MODEL}"
        resp = requests.get(model_url, headers=auth_headers, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            status = data.get("result", {}).get("status", "unknown")
            return f"Model '{CLOUDFLARE_MODEL}' is available. Status: {status}."
        elif resp.status_code == 404:
            return f"Model '{CLOUDFLARE_MODEL}' not found. Available models: check Cloudflare dashboard > Workers & Pages > AI > Models."
        else:
            return f"Cloudflare AI API returned status {resp.status_code}. Make sure your account has Workers AI enabled."
    except Exception as exc:
        return f"Error reaching Cloudflare AI API: {exc}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
