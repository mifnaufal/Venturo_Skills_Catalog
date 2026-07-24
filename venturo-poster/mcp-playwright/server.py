#!/usr/bin/env python3

import asyncio
import io
import logging
import sys
import time
from pathlib import Path

from PIL import Image

from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright

mcp = FastMCP("Venturo Poster — HTML/CSS to PNG")

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

CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 1024


def _render_tier_html(tier: str) -> str:
    """Return full HTML/CSS string for the given tier."""
    if tier == "starter":
        return _STARTER_HTML
    if tier == "growth":
        return _GROWTH_HTML
    if tier == "enterprise":
        return _ENTERPRISE_HTML
    raise ValueError(f"Unknown tier: {tier}")


def _with_logo_overlay(png_bytes: bytes, tier: str) -> bytes:
    """Open rendered PNG, overlay logo on right-side white space. Returns new PNG bytes."""
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    if img.size != (CANVAS_WIDTH, CANVAS_HEIGHT):
        img = img.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.LANCZOS)

    if LOGO_PATH.exists():
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            target_h = 120
            ratio = target_h / logo.height
            logo = logo.resize(
                (int(logo.width * ratio), target_h), Image.LANCZOS
            )
            margin = 30
            x = CANVAS_WIDTH - logo.width - margin
            y = CANVAS_HEIGHT - logo.height - margin
            img.paste(logo, (x, y), logo)
        except Exception as exc:
            logger.warning("Logo overlay skipped: %s", exc)

    out = io.BytesIO()
    img.save(out, "PNG")
    return out.getvalue()


async def _render_html_to_png(html: str) -> bytes:
    """Use Playwright to screenshot HTML at exactly CANVAS_WIDTH x CANVAS_HEIGHT."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": CANVAS_WIDTH, "height": CANVAS_HEIGHT},
            device_scale_factor=1,
        )
        page = await context.new_page()
        await page.set_content(html, wait_until="networkidle")
        png = await page.screenshot(
            type="png",
            clip={"x": 0, "y": 0, "width": CANVAS_WIDTH, "height": CANVAS_HEIGHT},
        )
        await browser.close()
        return png


@mcp.tool()
async def generate_catalog(tier: str = "starter") -> str:
    """Generate a WhatsApp Business catalog PNG for a Venturo package tier.

    Builds HTML/CSS design for the selected tier, renders to 1400x1024 PNG via Playwright,
    then overlays Venturo logo on the right-side white space using Pillow.
    """
    tier = tier.lower().strip()
    if tier not in ("starter", "growth", "enterprise"):
        return f"Error: tier must be starter/growth/enterprise, got '{tier}'"

    html = _render_tier_html(tier)
    logger.info("Rendering tier=%s via Playwright %dx%d", tier, CANVAS_WIDTH, CANVAS_HEIGHT)

    try:
        png_bytes = await _render_html_to_png(html)
    except Exception as exc:
        return f"Error rendering HTML: {exc}"

    final_bytes = _with_logo_overlay(png_bytes, tier)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"venturo-{tier}-{timestamp}.png"
    output_path = OUTPUT_DIR / filename
    output_path.write_bytes(final_bytes)
    logger.info("Saved %s (%d bytes)", output_path, len(final_bytes))
    return f"Catalog image generated: {output_path}"


# ─────────────────────────────────────────────────────────────────────────────
# Tier templates
# Right 35% (~490px) is intentionally blank white for further overlay.
# ─────────────────────────────────────────────────────────────────────────────

_BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 1400px;
  height: 1024px;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
  overflow: hidden;
}
.canvas {
  width: 1400px;
  height: 1024px;
  display: grid;
  grid-template-columns: 910px 490px;
  position: relative;
}
.content {
  width: 910px;
  height: 1024px;
  padding: 60px 60px 60px 70px;
  display: flex;
  flex-direction: column;
  position: relative;
}
.right-space {
  width: 490px;
  height: 1024px;
  background: #FFFFFF;
}
.brand {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-bottom: 12px;
}
.subbrand {
  font-size: 14px;
  margin-bottom: 40px;
  letter-spacing: 1px;
}
h1.tier-name {
  font-size: 88px;
  font-weight: 900;
  line-height: 1;
  letter-spacing: -2px;
  margin-bottom: 18px;
}
.budget-box {
  display: inline-block;
  padding: 12px 28px;
  border-radius: 8px;
  font-size: 32px;
  font-weight: 800;
  margin-bottom: 24px;
  letter-spacing: -0.5px;
}
.tagline {
  font-size: 22px;
  font-weight: 500;
  line-height: 1.3;
  margin-bottom: 36px;
  max-width: 720px;
}
.section-label {
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 12px;
}
.features {
  list-style: none;
  margin-bottom: 28px;
}
.features li {
  font-size: 18px;
  padding: 8px 0;
  display: flex;
  align-items: center;
}
.features li::before {
  content: "✓";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 900;
  margin-right: 14px;
  flex-shrink: 0;
}
.meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px 32px;
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid currentColor;
}
.meta-grid .meta-label {
  font-size: 11px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  opacity: 0.7;
  margin-bottom: 6px;
}
.meta-grid .meta-value {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.3;
}
.footer {
  position: absolute;
  bottom: 30px;
  left: 70px;
  font-size: 11px;
  letter-spacing: 1.5px;
  opacity: 0.5;
  text-transform: uppercase;
}
"""

_STARTER_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{ background: linear-gradient(180deg, #FFFFFF 0%, #F6F8F8 100%); color: #292929; }}
.brand {{ color: #006D79; }}
.subbrand {{ color: #4B5563; }}
h1.tier-name {{ color: #006D79; }}
.budget-box {{ background: #006D79; color: #FFFFFF; }}
.tagline {{ color: #4B5563; }}
.section-label {{ color: #006D79; }}
.features li::before {{ background: #009BAD; color: #FFFFFF; }}
.features li {{ color: #292929; }}
.meta-grid {{ color: #4B5563; border-top-color: #E5E7EB; }}
.footer {{ color: #4B5563; }}
</style></head><body><div class="canvas">
<div class="content">
  <div class="brand">VENTURO</div>
  <div class="subbrand">Software House Malang</div>
  <h1 class="tier-name">PAKET<br>STARTER</h1>
  <div class="budget-box">Rp20 Juta – Rp80 Juta</div>
  <div class="tagline">Ideal untuk UMKM, Usaha Mikro, dan Startup yang butuh website, mobile app, atau sistem operasional sederhana.</div>
  <div class="section-label">Yang Kamu Dapat</div>
  <ul class="features">
    <li>Website &amp; Mobile App Custom</li>
    <li>UI/UX Modern &amp; Responsif</li>
    <li>Sistem Scalable &amp; Fleksibel</li>
    <li>Efisiensi Operasional Naik</li>
    <li>Dukungan Tim Dedicated</li>
  </ul>
  <div class="meta-grid">
    <div><div class="meta-label">Tim Dedicated</div><div class="meta-value">1 BA + 1 Senior Engineer</div></div>
    <div><div class="meta-label">Timeline</div><div class="meta-value">1 – 4 Minggu</div></div>
  </div>
  <div class="footer">© Venturo Software House Malang</div>
</div>
<div class="right-space"></div>
</div></body></html>"""

_GROWTH_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{ background: linear-gradient(135deg, #FFFFFF 0%, #E8F4F5 50%, #F6F8F8 100%); color: #292929; }}
.brand {{ color: #006D79; }}
.subbrand {{ color: #4B5563; }}
h1.tier-name {{ color: #006D79; }}
.budget-box {{ background: linear-gradient(90deg, #006D79, #009BAD); color: #FFFFFF; }}
.tagline {{ color: #374151; }}
.section-label {{ color: #006D79; }}
.features li::before {{ background: #006D79; color: #FFFFFF; }}
.features li {{ color: #292929; }}
.meta-grid {{ color: #4B5563; border-top-color: rgba(0,109,121,0.2); }}
.footer {{ color: #4B5563; }}
</style></head><body><div class="canvas">
<div class="content">
  <div class="brand">VENTURO</div>
  <div class="subbrand">Software House Malang</div>
  <h1 class="tier-name">PAKET<br>GROWTH</h1>
  <div class="budget-box">Rp80 Juta – Rp250 Juta</div>
  <div class="tagline">Untuk perusahaan scaling yang butuh sistem custom: Finance, HRIS, CRM, ERP, Inventory, WMS, dan lainnya.</div>
  <div class="section-label">Modul Sistem</div>
  <ul class="features">
    <li>Finance &amp; Accounting System</li>
    <li>HRIS &amp; Payroll Management</li>
    <li>CRM &amp; Sales Management</li>
    <li>ERP &amp; Inventory System</li>
    <li>WMS &amp; Logistic Management</li>
    <li>Dashboard &amp; Reporting Analytics</li>
  </ul>
  <div class="meta-grid">
    <div><div class="meta-label">Tim Dedicated</div><div class="meta-value">BA + Sr. Eng + UI/UX + QA</div></div>
    <div><div class="meta-label">Timeline</div><div class="meta-value">1 – 4.5 Bulan</div></div>
  </div>
  <div class="footer">© Venturo Software House Malang</div>
</div>
<div class="right-space"></div>
</div></body></html>"""

_ENTERPRISE_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{
  background: linear-gradient(135deg, #0A1B1F 0%, #202020 50%, #0A1B1F 100%);
  color: #FFFFFF;
  position: relative;
}}
.content::before {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 30%, rgba(0,155,173,0.15) 0%, transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(0,109,121,0.2) 0%, transparent 40%);
  pointer-events: none;
}}
.content > * {{ position: relative; }}
.brand {{ color: #009BAD; text-shadow: 0 0 12px rgba(0,155,173,0.5); }}
.subbrand {{ color: #9CA3AF; }}
h1.tier-name {{
  color: #FFFFFF;
  text-shadow: 0 0 30px rgba(0,155,173,0.4);
}}
.budget-box {{
  background: #006D79;
  color: #FFFFFF;
  box-shadow: 0 0 24px rgba(0,155,173,0.4);
  border: 1px solid #009BAD;
}}
.tagline {{ color: #D1D5DB; }}
.section-label {{ color: #009BAD; }}
.features li::before {{
  background: #009BAD;
  color: #FFFFFF;
  box-shadow: 0 0 12px rgba(0,155,173,0.6);
}}
.features li {{ color: #E5E7EB; }}
.meta-grid {{
  color: #9CA3AF;
  border-top-color: rgba(0,155,173,0.3);
}}
.meta-grid .meta-value {{ color: #FFFFFF; }}
.footer {{ color: #6B7280; }}
</style></head><body><div class="canvas">
<div class="content">
  <div class="brand">VENTURO</div>
  <div class="subbrand">Software House Malang</div>
  <h1 class="tier-name">PAKET<br>ENTERPRISE</h1>
  <div class="budget-box">Mulai Rp250 Juta</div>
  <div class="tagline">Solusi enterprise-grade untuk AI, Big Data, cybersecurity, dan transformasi digital menyeluruh.</div>
  <div class="section-label">Solusi Enterprise</div>
  <ul class="features">
    <li>AI &amp; Big Data Integration</li>
    <li>Cybersecurity &amp; Pen Test</li>
    <li>Cross-System Integration</li>
    <li>Digital Transformation</li>
    <li>System Architecture Complex</li>
    <li>Holographic UI &amp; Real-time Dashboard</li>
  </ul>
  <div class="meta-grid">
    <div><div class="meta-label">Tim Dedicated</div><div class="meta-value">6 Orang (BA, Sr/Mid Eng, UI/UX, QA, Pen Test)</div></div>
    <div><div class="meta-label">Timeline</div><div class="meta-value">2 – 8 Bulan</div></div>
  </div>
  <div class="footer">© Venturo Software House Malang</div>
</div>
<div class="right-space"></div>
</div></body></html>"""


if __name__ == "__main__":
    mcp.run(transport="stdio")