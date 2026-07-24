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


def _render_tier_html(tier: str, theme: str = "default") -> str:
    """Return full HTML/CSS string for the given tier + theme combination."""
    if theme != "default":
        themed = _THEME_VARIANTS.get(theme)
        if themed and tier in themed:
            return themed[tier]
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
async def generate_catalog(tier: str = "starter", theme: str = "default") -> str:
    """Generate a WhatsApp Business catalog PNG for a Venturo package tier.

    Builds HTML/CSS design for the selected tier and optional theme variant,
    renders to 1400x1024 PNG via Playwright, then overlays Venturo logo
    on the right-side white space using Pillow.
    """
    tier = tier.lower().strip()
    theme = theme.lower().strip()
    if tier not in ("starter", "growth", "enterprise"):
        return f"Error: tier must be starter/growth/enterprise, got '{tier}'"
    if theme != "default" and theme not in _THEME_VARIANTS:
        available = ", ".join(sorted(_THEME_VARIANTS.keys()))
        return f"Error: theme must be 'default' or one of: {available}"

    html = _render_tier_html(tier, theme)
    logger.info(
        "Rendering tier=%s theme=%s via Playwright %dx%d",
        tier, theme, CANVAS_WIDTH, CANVAS_HEIGHT,
    )

    try:
        png_bytes = await _render_html_to_png(html)
    except Exception as exc:
        return f"Error rendering HTML: {exc}"

    final_bytes = _with_logo_overlay(png_bytes, tier)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    suffix = f"-{theme}" if theme != "default" else ""
    filename = f"venturo-{tier}{suffix}-{timestamp}.png"
    output_path = OUTPUT_DIR / filename
    output_path.write_bytes(final_bytes)
    logger.info("Saved %s (%d bytes)", output_path, len(final_bytes))
    return f"Catalog image generated: {output_path}"


# ─────────────────────────────────────────────────────────────────────────────
# Theme variants — alternative designs driven by theme-factory skill
# Each theme maps: tier -> HTML string override. Visual treatment + colors
# per theme are documented in venturo-poster/themes/<tier>/<theme>.md
# ─────────────────────────────────────────────────────────────────────────────

# NOTE: canvas-fonts/ has OpenType fonts but Playwright headless
# Chromium on this Linux machine cannot load them without an external
# file-server. The themed variants below rely solely on system fonts
# (system sans-serif, monospace).  For local-dev with installed fonts,
# the _BASE_CSS can be augmented with a real @font-face block pointing
# to assets/canvas-fonts/*.ttf via a dev HTTP server.


# ── Core CSS shared by ALL templates (default + themed) ──
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

_STARTER_MINIMALIST_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{
  background: linear-gradient(180deg, #f9f9f9 0%, #ffffff 100%);
  color: #36454f;
  border-left: 4px solid #006D79;
  position: relative;
}}
.content::after {{
  content: "";
  position: absolute; inset: 0;
  background-image: radial-gradient(#708090 1px, transparent 1px);
  background-size: 28px 28px;
  opacity: 0.05;
  pointer-events: none;
}}
.content > * {{ position: relative; }}
.brand {{ color: #006D79; font-family: 'Outfit', sans-serif; }}
.subbrand {{ color: #708090; }}
h1.tier-name {{ color: #36454f; font-family: 'Outfit', sans-serif; }}
.budget-box {{ background: #36454f; color: #ffffff; font-family: 'Outfit', sans-serif; }}
.tagline {{ color: #4b5563; font-family: 'InstrumentSans', sans-serif; }}
.section-label {{ color: #006D79; letter-spacing: 3px; }}
.features li::before {{ background: transparent; color: #006D79; border: 2px solid #006D79; }}
.features li {{ color: #36454f; font-family: 'InstrumentSans', sans-serif; }}
.meta-grid {{ color: #708090; border-top-color: #d3d3d3; }}
.meta-grid .meta-value {{ color: #36454f; }}
.footer {{ color: #708090; }}
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

_STARTER_ARCTIC_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{ background: linear-gradient(180deg, #fafafa 0%, #d4e4f7 100%); color: #1a2332; }}
.brand {{ color: #006D79; }}
.subbrand {{ color: #4a6fa5; }}
h1.tier-name {{ color: #4a6fa5; }}
.budget-box {{ background: linear-gradient(90deg, #4a6fa5, #006D79); color: #ffffff; }}
.tagline {{ color: #2d3b50; }}
.section-label {{ color: #006D79; }}
.features li::before {{ background: #4a6fa5; color: #ffffff; }}
.features li {{ color: #1a2332; }}
.meta-grid {{ color: #4a6fa5; border-top-color: #c0c0c0; }}
.meta-grid .meta-value {{ color: #1a2332; }}
.footer {{ color: #708090; }}
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

_GROWTH_TECH_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{
  background: linear-gradient(135deg, #ffffff 0%, #f5f9ff 50%, #ffffff 100%);
  color: #1e1e1e;
  position: relative;
}}
.content::before {{
  content: "";
  position: absolute; inset: 0;
  background-image:
    linear-gradient(to right, rgba(0, 102, 255, 0.04) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0, 102, 255, 0.04) 1px, transparent 1px);
  background-size: 32px 32px;
  pointer-events: none;
}}
.content > * {{ position: relative; }}
.brand {{
  color: #0066ff;
  font-family: 'Boldonse', sans-serif;
  border-bottom: 3px solid #00ffff;
  display: inline-block;
  padding-bottom: 4px;
}}
.subbrand {{ color: #4a6fa5; font-family: 'JetBrainsMono', monospace; }}
h1.tier-name {{ color: #0066ff; font-family: 'Boldonse', sans-serif; }}
.budget-box {{
  background: linear-gradient(90deg, #0066ff, #00ffff);
  color: #ffffff;
  font-family: 'JetBrainsMono', monospace;
}}
.tagline {{ color: #1e1e1e; }}
.section-label {{ color: #0066ff; letter-spacing: 3px; }}
.features li::before {{ background: #0066ff; color: #00ffff; }}
.features li {{ color: #1e1e1e; font-family: 'JetBrainsMono', monospace; }}
.meta-grid {{ color: #4a6fa5; border-top-color: rgba(0, 102, 255, 0.3); font-family: 'JetBrainsMono', monospace; }}
.meta-grid .meta-value {{ color: #1e1e1e; }}
.footer {{ color: #708090; font-family: 'JetBrainsMono', monospace; }}
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

_GROWTH_OCEAN_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{ background: linear-gradient(180deg, #f1faee 0%, #a8dadc 100%); color: #1a2332; }}
.brand {{ color: #006D79; }}
.subbrand {{ color: #2d8b8b; }}
h1.tier-name {{ color: #1a2332; }}
.budget-box {{ background: linear-gradient(90deg, #1a2332, #2d8b8b); color: #ffffff; }}
.tagline {{ color: #1a2332; }}
.section-label {{ color: #006D79; }}
.features li::before {{ background: #2d8b8b; color: #ffffff; width: 28px; height: 28px; }}
.features li {{ color: #1a2332; }}
.meta-grid {{ color: #2d8b8b; border-top-color: rgba(45, 139, 139, 0.3); }}
.meta-grid .meta-value {{ color: #1a2332; }}
.footer {{ color: #4a6fa5; }}
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

_ENTERPRISE_MIDNIGHT_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{
  background: linear-gradient(135deg, #2b1e3e 0%, #4a4e8f 100%);
  color: #e6e6fa;
  position: relative;
}}
.content::before {{
  content: "";
  position: absolute; inset: 0;
  background:
    radial-gradient(circle at 25% 20%, rgba(164, 144, 194, 0.25) 0%, transparent 45%),
    radial-gradient(circle at 75% 80%, rgba(0, 109, 121, 0.3) 0%, transparent 45%);
  pointer-events: none;
}}
.content::after {{
  content: "";
  position: absolute; inset: 0;
  background-image: radial-gradient(#e6e6fa 1px, transparent 1px);
  background-size: 80px 80px;
  opacity: 0.15;
  pointer-events: none;
}}
.content > * {{ position: relative; }}
.brand {{
  color: #006D79;
  font-family: 'BricolageGrotesque', sans-serif;
  text-shadow: 0 0 16px rgba(0, 109, 121, 0.7);
}}
.subbrand {{ color: #a490c2; }}
h1.tier-name {{
  color: #e6e6fa;
  font-family: 'BricolageGrotesque', sans-serif;
  text-shadow: 0 0 30px rgba(74, 78, 143, 0.6);
}}
.budget-box {{
  background: #006D79;
  color: #ffffff;
  box-shadow: 0 0 28px rgba(0, 109, 121, 0.6);
  border: 1px solid #a490c2;
}}
.tagline {{ color: #d4cce6; }}
.section-label {{ color: #a490c2; letter-spacing: 3px; }}
.features li::before {{
  background: transparent;
  color: #a490c2;
  border: 2px solid #a490c2;
}}
.features li {{ color: #e6e6fa; }}
.meta-grid {{
  color: #a490c2;
  border-top-color: rgba(164, 144, 194, 0.4);
}}
.meta-grid .meta-value {{ color: #e6e6fa; }}
.footer {{ color: #708090; }}
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

_ENTERPRISE_TECH_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.content {{
  background: linear-gradient(135deg, #0a0a0a 0%, #1e1e1e 100%);
  color: #ffffff;
  position: relative;
}}
.content::before {{
  content: "";
  position: absolute; inset: 0;
  background:
    linear-gradient(to right, rgba(0, 102, 255, 0.04) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0, 102, 255, 0.04) 1px, transparent 1px),
    linear-gradient(to right, rgba(0, 255, 255, 0.03) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
  background-size: 80px 80px, 80px 80px, 16px 16px, 16px 16px;
  pointer-events: none;
}}
.content > * {{ position: relative; }}
.brand {{
  color: #00ffff;
  font-family: 'Boldonse', sans-serif;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.7), 0 0 40px rgba(0, 102, 255, 0.4);
  border-bottom: 3px solid #0066ff;
  display: inline-block;
  padding-bottom: 4px;
}}
.subbrand {{ color: #00ffff; font-family: 'JetBrainsMono', monospace; opacity: 0.7; }}
h1.tier-name {{ color: #ffffff; font-family: 'Boldonse', sans-serif; text-shadow: 0 0 30px rgba(0, 102, 255, 0.5); }}
.budget-box {{
  background: #0066ff;
  color: #00ffff;
  font-family: 'JetBrainsMono', monospace;
  box-shadow: 0 0 30px rgba(0, 102, 255, 0.6);
  border: 1px solid #00ffff;
}}
.tagline {{ color: #e0e0e0; font-family: 'JetBrainsMono', monospace; }}
.section-label {{ color: #00ffff; letter-spacing: 3px; font-family: 'JetBrainsMono', monospace; }}
.features li::before {{
  background: transparent;
  color: #00ffff;
  border: 2px solid #00ffff;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.4);
}}
.features li {{ color: #ffffff; }}
.meta-grid {{ color: #00ffff; border-top-color: rgba(0, 255, 255, 0.3); font-family: 'JetBrainsMono', monospace; }}
.meta-grid .meta-value {{ color: #ffffff; }}
.footer {{ color: #00ffff; opacity: 0.6; font-family: 'JetBrainsMono', monospace; }}
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


_THEME_VARIANTS: dict[str, dict[str, str]] = {
    "modern-minimalist": {
        "starter": _STARTER_MINIMALIST_HTML,
    },
    "arctic-frost": {
        "starter": _STARTER_ARCTIC_HTML,
    },
    "tech-innovation": {
        "growth": _GROWTH_TECH_HTML,
        "enterprise": _ENTERPRISE_TECH_HTML,
    },
    "ocean-depths": {
        "growth": _GROWTH_OCEAN_HTML,
    },
    "midnight-galaxy": {
        "enterprise": _ENTERPRISE_MIDNIGHT_HTML,
    },
}


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