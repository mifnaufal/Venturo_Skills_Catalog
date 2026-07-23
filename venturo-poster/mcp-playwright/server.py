#!/usr/bin/env python3

import base64
import logging
import os
import sys
import time
from pathlib import Path

import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Venturo Poster — ImageRouter")

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

IMAGE_ROUTER_API_KEY = os.environ.get("IMAGE_ROUTER_API_KEY", "")
IMAGE_ROUTER_URL = "https://api.imagerouter.io/v1/openai/images/generations"
MODEL = "qwen/qwen-image-2-pro"


def _logo_data_uri() -> str:
    if not LOGO_PATH.exists():
        raise FileNotFoundError(f"Logo not found at {LOGO_PATH}")
    data = LOGO_PATH.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:image/png;base64,{b64}"


@mcp.tool()
async def generate_catalog(prompt: str, tier: str = "starter") -> str:
    if not IMAGE_ROUTER_API_KEY:
        return (
            "Error: IMAGE_ROUTER_API_KEY not set. "
            "Set it as an environment variable or in your MCP server config."
        )

    logo_uri = _logo_data_uri()

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "image": logo_uri,
        "size": "1024x1024",
        "response_format": "url",
        "n": 1,
    }

    headers = {
        "Authorization": f"Bearer {IMAGE_ROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(IMAGE_ROUTER_URL, json=payload, headers=headers, timeout=120)
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.Timeout:
        return "Error: Request timed out after 120s. The API may be slow."
    except requests.exceptions.RequestException as exc:
        detail = ""
        if exc.response is not None:
            try:
                detail = exc.response.json()
            except Exception:
                detail = exc.response.text[:500]
        return f"Error calling ImageRouter API: {exc}\nResponse: {detail}"
    except Exception as exc:
        return f"Error: {exc}"

    try:
        image_url = data["data"][0]["url"]
    except (KeyError, IndexError) as exc:
        return f"Error: Unexpected API response format: {data}"

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"venturo-{tier}-{timestamp}.png"
    output_path = OUTPUT_DIR / filename

    try:
        img_resp = requests.get(image_url, timeout=60)
        img_resp.raise_for_status()
        output_path.write_bytes(img_resp.content)
        logger.info("Image saved to %s", output_path)
        return f"Catalog image generated: {output_path}"
    except Exception as exc:
        return f"Error downloading image from {image_url}: {exc}"


@mcp.tool()
async def check_balance() -> str:
    if not IMAGE_ROUTER_API_KEY:
        return "Error: IMAGE_ROUTER_API_KEY not set."
    headers = {"Authorization": f"Bearer {IMAGE_ROUTER_API_KEY}"}
    try:
        resp = requests.get(
            "https://api.imagerouter.io/v1/credits", headers=headers, timeout=10
        )
        resp.raise_for_status()
        return f"Credit balance: {resp.json()}"
    except Exception as exc:
        return f"Error checking balance: {exc}"


if __name__ == "__main__":
    mcp.run(transport="stdio")
