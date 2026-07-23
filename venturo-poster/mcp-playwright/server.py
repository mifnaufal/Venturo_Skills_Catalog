#!/usr/bin/env python3

import base64
import logging
import os
import re
import sys
import time
from pathlib import Path

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Venturo Poster — MaxRouter")

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

_ENV_PATH = PLUGIN_ROOT.parent / ".env"
if _ENV_PATH.exists():
    with open(_ENV_PATH) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip().strip("\"'"))

API_KEY = os.environ.get("IMAGE_ROUTER_API_KEY", "")
API_URL = "https://maxrouter.io/llm-api/v1/chat/completions"
MODEL = "qwen-image-2.0-pro"


def _logo_data_uri() -> str:
    if not LOGO_PATH.exists():
        raise FileNotFoundError(f"Logo not found at {LOGO_PATH}")
    data = LOGO_PATH.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:image/png;base64,{b64}"


def _extract_image_url(content: str) -> str | None:
    m = re.search(r"!\[.*?\]\((https?://[^\s)]+)\)", content)
    if m:
        return m.group(1)
    m = re.search(r"(https?://[^\s)]+\.(?:png|jpg|jpeg|webp))", content)
    if m:
        return m.group(1)
    return None


def _extract_base64_bytes(content: str) -> bytes | None:
    m = re.search(r"data:image/[a-z]+;base64,([A-Za-z0-9+/=]+)", content)
    if m:
        return base64.b64decode(m.group(1))
    return None


@mcp.tool()
async def generate_catalog(
    prompt: str,
    tier: str = "starter",
    image_size: str = "1K",
    aspect_ratio: str = "1:1",
) -> str:
    if not API_KEY:
        return (
            "Error: IMAGE_ROUTER_API_KEY not set. "
            "Set it as an environment variable or in your MCP server config."
        )

    logo_uri = _logo_data_uri()

    payload = {
        "model": MODEL,
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": logo_uri}},
                ],
            }
        ],
        "image_size": image_size,
        "aspect_ratio": aspect_ratio,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=180)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        return "Error: Request timed out after 180s."
    except requests.exceptions.RequestException as exc:
        detail = ""
        if exc.response is not None:
            try:
                detail = exc.response.json()
            except Exception:
                detail = exc.response.text[:500]
        return f"Error calling API: {exc}\nResponse: {detail}"
    except Exception as exc:
        return f"Error: {exc}"

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as exc:
        return f"Error: Unexpected API response format: {data}"

    img_bytes = _extract_base64_bytes(content)
    if img_bytes is None:
        image_url = _extract_image_url(content)
        if image_url is None:
            return (
                f"Error: No image found in response.\n"
                f"Response content: {content[:500]}"
            )
        try:
            img_resp = requests.get(image_url, timeout=60)
            img_resp.raise_for_status()
            img_bytes = img_resp.content
        except Exception as exc:
            return f"Error downloading image from {image_url}: {exc}"

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"venturo-{tier}-{timestamp}.png"
    output_path = OUTPUT_DIR / filename
    output_path.write_bytes(img_bytes)
    logger.info("Image saved to %s", output_path)
    return f"Catalog image generated: {output_path}"


@mcp.tool()
async def check_balance() -> str:
    if not API_KEY:
        return "Error: IMAGE_ROUTER_API_KEY not set."
    try:
        resp = requests.get(
            "https://maxrouter.io/llm-api/v1/models",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10,
        )
        resp.raise_for_status()
        return "API key is valid. Connected to maxrouter.io."
    except Exception as exc:
        return f"Error: {exc}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
