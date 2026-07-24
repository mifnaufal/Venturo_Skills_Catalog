#!/usr/bin/env python3

import asyncio
import logging
import sys
import time
from pathlib import Path

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
OUTPUT_DIR = PLUGIN_ROOT / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 1024

# Venturo brand mark — rendered as inline SVG so it's pixel-perfect at any DPI
VENTURO_LOGO_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 29" '
    'class="venturo-logo" aria-label="Venturo">'
    '<text x="0" y="22" font-family="Inter, Arial, sans-serif" '
    'font-size="22" font-weight="800" letter-spacing="2" fill="currentColor">'
    'VENTURO'
    '</text>'
    '<circle cx="118" cy="14" r="4" fill="#FF6B35"/>'
    '</svg>'
)


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


async def _render_html_to_png(html: str) -> bytes:
    """Render HTML to a crisp PNG via Playwright at 2x DPI, then downscale."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": CANVAS_WIDTH, "height": CANVAS_HEIGHT},
            device_scale_factor=2,
        )
        page = await context.new_page()
        await page.set_content(html, wait_until="networkidle")
        png = await page.screenshot(
            type="png",
            clip={"x": 0, "y": 0, "width": CANVAS_WIDTH, "height": CANVAS_HEIGHT},
        )
        await browser.close()
        # Downscale 2x → 1x for sharp final output
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(png))
        if img.size != (CANVAS_WIDTH, CANVAS_HEIGHT):
            img = img.resize((CANVAS_WIDTH, CANVAS_HEIGHT), Image.LANCZOS)
        out = io.BytesIO()
        img.save(out, "PNG")
        return out.getvalue()


@mcp.tool()
async def generate_catalog(tier: str = "starter") -> str:
    """Generate a 1024x1024 WhatsApp Business catalog PNG for a Venturo package tier.

    Builds HTML/CSS design for the selected tier with Venturo brand styling,
    renders to a square PNG via Playwright at 2x DPI for crisp output.
    """
    tier = tier.lower().strip()
    if tier not in ("starter", "growth", "enterprise"):
        return f"Error: tier must be starter/growth/enterprise, got '{tier}'"

    html = _render_tier_html(tier)
    logger.info(
        "Rendering tier=%s via Playwright %dx%d",
        tier, CANVAS_WIDTH, CANVAS_HEIGHT,
    )

    try:
        final_bytes = await _render_html_to_png(html)
    except Exception as exc:
        return f"Error rendering HTML: {exc}"

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"venturo-{tier}-{timestamp}.png"
    output_path = OUTPUT_DIR / filename
    output_path.write_bytes(final_bytes)
    logger.info("Saved %s (%d bytes)", output_path, len(final_bytes))
    return f"Catalog image generated: {output_path}"


# ─────────────────────────────────────────────────────────────────────────────
# Theme variants — alternative designs driven by theme-factory skill
# Each theme maps: tier -> HTML string override.
# Visual treatment per theme documented in venturo-poster/themes/<tier>/<theme>.md
# ─────────────────────────────────────────────────────────────────────────────


# ── Core CSS shared by ALL templates (square 1024×1024 poster) ──
_BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 1024px;
  height: 1024px;
  font-family: 'Inter', 'Segoe UI', Arial, sans-serif;
  overflow: hidden;
}
.poster {
  width: 1024px;
  height: 1024px;
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 64px 64px 56px 64px;
}
.brand {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}
.venturo-logo {
  height: 28px;
  width: auto;
}
.tier-name {
  font-size: 112px;
  font-weight: 900;
  line-height: 1.0;
  letter-spacing: -4px;
  margin-bottom: 28px;
}
.budget-box {
  display: inline-block;
  padding: 14px 32px;
  border-radius: 10px;
  font-size: 28px;
  font-weight: 800;
  margin-bottom: 32px;
}
.tagline {
  font-size: 20px;
  font-weight: 400;
  line-height: 1.55;
  margin-bottom: 40px;
  max-width: 880px;
}
.section-label {
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 4px;
  margin-bottom: 20px;
}
.features {
  list-style: none;
  margin-bottom: 36px;
}
.features li {
  font-size: 18px;
  font-weight: 500;
  padding: 10px 0;
  display: flex;
  align-items: center;
  border-bottom: 1px solid rgba(128,128,128,0.1);
}
.features li:last-child {
  border-bottom: none;
}
.features li::before {
  content: "✓";
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  font-size: 14px;
  font-weight: 900;
  margin-right: 18px;
  flex-shrink: 0;
}
.detail-section {
  margin-bottom: 16px;
}
.detail-label {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 2.5px;
  opacity: 0.5;
  margin-bottom: 6px;
}
.detail-value {
  font-size: 16px;
  font-weight: 700;
  line-height: 1.4;
}
.meta-strip {
  margin-top: auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px 48px;
  padding-top: 28px;
  border-top: 1.5px solid currentColor;
}
.meta-strip .meta-item .detail-label {
  margin-bottom: 8px;
}
.meta-strip .meta-item .detail-value {
  font-size: 17px;
  font-weight: 700;
}
.footer-brand {
  position: absolute;
  bottom: 22px;
  left: 64px;
  font-size: 11px;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  opacity: 0.35;
  font-weight: 700;
}
.content-top {
  display: flex;
  flex-direction: column;
}
.content-body {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 48px 64px;
  margin-top: auto;
  padding-top: 24px;
}
.content-body-left {
  display: flex;
  flex-direction: column;
}
.content-body-right {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.highlight-card {
  background: rgba(128,128,128,0.04);
  border-radius: 12px;
  padding: 20px 24px;
  margin-bottom: 12px;
}
.highlight-card .detail-label {
  font-size: 9px;
  letter-spacing: 2px;
  margin-bottom: 6px;
}
.highlight-card .detail-value {
  font-size: 15px;
}
"""


_STARTER_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.poster {{
  background: #FFFFFF;
  color: #1F2937;
  position: relative;
}}
.poster::before {{
  content: "";
  position: absolute;
  inset: 0;
  background-image: radial-gradient(#006D79 1px, transparent 1px);
  background-size: 28px 28px;
  opacity: 0.06;
  pointer-events: none;
}}
.poster > * {{ position: relative; }}
.brand {{ color: #006D79; }}
.tier-name {{ color: #006D79; }}
.budget-box {{ background: #006D79; color: #FFFFFF; }}
.tagline {{ color: #374151; }}
.section-label {{ color: #006D79; }}
.features {{ color: #1F2937; }}
.features li {{ font-weight: 600; }}
.features li::before {{ background: #006D79; color: #FFFFFF; }}
.meta-strip {{ color: #006D79; }}
.highlight-card {{ background: rgba(0,109,121,0.04); border-left: 3px solid #006D79; }}
.highlight-card .detail-label {{ color: #006D79; }}
.highlight-card .detail-value {{ color: #1F2937; }}
.footer-brand {{ color: #006D79; }}
</style></head><body><div class="poster">
  <div class="brand">{VENTURO_LOGO_SVG}</div>
  <h1 class="tier-name">PAKET STARTER</h1>
  <div class="budget-box">Rp20 Juta – Rp80 Juta</div>
  <div class="tagline">Ideal untuk UMKM, Usaha Mikro, dan Startup yang butuh website, mobile app, atau sistem operasional sederhana.</div>
  <div class="content-top">
  <div class="section-label">Yang Kamu Dapat</div>
  <ul class="features">
    <li>Website &amp; Mobile App Custom</li>
    <li>UI/UX Modern &amp; Responsif</li>
    <li>Sistem Scalable &amp; Fleksibel</li>
    <li>Efisiensi Operasional Naik</li>
    <li>Dukungan Tim Dedicated</li>
  </ul>
  </div>
  <div class="content-body">
    <div class="content-body-left">
      <div class="detail-section">
        <div class="detail-label">Tim Dedicated</div>
        <div class="detail-value">1 BA + 1 Senior Engineer</div>
      </div>
      <div class="detail-section">
        <div class="detail-label">Timeline</div>
        <div class="detail-value">1 – 4 Minggu</div>
      </div>
    </div>
    <div class="content-body-right">
      <div class="highlight-card">
        <div class="detail-label">COCOK UNTUK</div>
        <div class="detail-value">UMKM, Usaha Mikro, Startup</div>
      </div>
      <div class="highlight-card">
        <div class="detail-label">FASE BISNIS</div>
        <div class="detail-value">Validasi Ide &amp; Early Traction</div>
      </div>
    </div>
  </div>
  <div class="footer-brand">© venturo.id</div>
</div></body></html>"""


_GROWTH_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.poster {{
  background: #FFFFFF;
  color: #1F2937;
  position: relative;
}}
.poster::before {{
  content: "";
  position: absolute;
  inset: 0;
  background-image: radial-gradient(#009BAD 1px, transparent 1px);
  background-size: 24px 24px;
  opacity: 0.05;
  pointer-events: none;
}}
.poster > * {{ position: relative; }}
.brand {{ color: #006D79; }}
.tier-name {{ color: #006D79; }}
.budget-box {{ background: linear-gradient(135deg, #006D79, #009BAD); color: #FFFFFF; }}
.tagline {{ color: #374151; }}
.section-label {{ color: #006D79; }}
.features {{ color: #1F2937; }}
.features li {{ font-weight: 600; }}
.features li::before {{ background: #006D79; color: #FFFFFF; }}
.meta-strip {{ color: #006D79; }}
.highlight-card {{ background: rgba(0,155,173,0.04); border-left: 3px solid #009BAD; }}
.highlight-card .detail-label {{ color: #009BAD; }}
.highlight-card .detail-value {{ color: #1F2937; }}
.footer-brand {{ color: #006D79; }}
</style></head><body><div class="poster">
  <div class="brand">{VENTURO_LOGO_SVG}</div>
  <h1 class="tier-name">PAKET GROWTH</h1>
  <div class="budget-box">Rp80 Juta – Rp250 Juta</div>
  <div class="tagline">Untuk perusahaan scaling yang butuh sistem custom: Finance, HRIS, CRM, ERP, Inventory, WMS, dan lainnya.</div>
  <div class="content-top">
  <div class="section-label">Modul Sistem</div>
  <ul class="features">
    <li>Finance &amp; Accounting System</li>
    <li>HRIS &amp; Payroll Management</li>
    <li>CRM &amp; Sales Management</li>
    <li>ERP &amp; Inventory System</li>
    <li>WMS &amp; Logistic Management</li>
    <li>Dashboard &amp; Reporting Analytics</li>
  </ul>
  </div>
  <div class="content-body">
    <div class="content-body-left">
      <div class="detail-section">
        <div class="detail-label">Tim Dedicated</div>
        <div class="detail-value">BA + Sr. Eng + UI/UX + QA</div>
      </div>
      <div class="detail-section">
        <div class="detail-label">Timeline</div>
        <div class="detail-value">1 – 4.5 Bulan</div>
      </div>
    </div>
    <div class="content-body-right">
      <div class="highlight-card">
        <div class="detail-label">COCOK UNTUK</div>
        <div class="detail-value">Perusahaan Scaling &amp; Mid-Market</div>
      </div>
      <div class="highlight-card">
        <div class="detail-label">FASE BISNIS</div>
        <div class="detail-value">Ekspansi Sistem &amp; Efisiensi</div>
      </div>
    </div>
  </div>
  <div class="footer-brand">© venturo.id</div>
</div></body></html>"""


_ENTERPRISE_HTML = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><style>{_BASE_CSS}
.poster {{
  background: linear-gradient(160deg, #0A1B1F 0%, #0D2229 40%, #112D35 100%);
  color: #FFFFFF;
  position: relative;
}}
.poster::before {{
  content: "";
  position: absolute;
  inset: 0;
  background-image: radial-gradient(#009BAD 1px, transparent 1px);
  background-size: 32px 32px;
  opacity: 0.08;
  pointer-events: none;
}}
.poster::after {{
  content: "";
  position: absolute;
  top: -200px;
  right: -200px;
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(0,155,173,0.12) 0%, transparent 70%);
  pointer-events: none;
}}
.poster > * {{ position: relative; }}
.brand {{ color: #009BAD; }}
.tier-name {{ color: #FFFFFF; }}
.budget-box {{
  background: rgba(0,109,121,0.5);
  color: #FFFFFF;
  border: 1.5px solid rgba(0,155,173,0.5);
}}
.tagline {{ color: #C7D5DA; }}
.section-label {{ color: #009BAD; }}
.features {{ color: #E5E7EB; }}
.features li {{ font-weight: 600; }}
.features li::before {{ background: #009BAD; color: #0A1B1F; }}
.meta-strip {{ color: #009BAD; }}
.highlight-card {{ background: rgba(0,155,173,0.08); border-left: 3px solid #009BAD; }}
.highlight-card .detail-label {{ color: #009BAD; }}
.highlight-card .detail-value {{ color: #FFFFFF; }}
.footer-brand {{ color: #009BAD; }}
</style></head><body><div class="poster">
  <div class="brand">{VENTURO_LOGO_SVG}</div>
  <h1 class="tier-name">PAKET ENTERPRISE</h1>
  <div class="budget-box">Mulai Rp250 Juta</div>
  <div class="tagline">Solusi enterprise-grade untuk AI, Big Data, cybersecurity, dan transformasi digital menyeluruh.</div>
  <div class="content-top">
  <div class="section-label">Solusi Enterprise</div>
  <ul class="features">
    <li>AI &amp; Big Data Integration</li>
    <li>Cybersecurity &amp; Pen Test</li>
    <li>Cross-System Integration</li>
    <li>Digital Transformation</li>
    <li>System Architecture Complex</li>
    <li>Holographic UI &amp; Real-time Dashboard</li>
  </ul>
  </div>
  <div class="content-body">
    <div class="content-body-left">
      <div class="detail-section">
        <div class="detail-label">Tim Dedicated</div>
        <div class="detail-value">6 Orang (BA, Sr/Mid Eng, UI/UX, QA, Pen Test)</div>
      </div>
      <div class="detail-section">
        <div class="detail-label">Timeline</div>
        <div class="detail-value">2 – 8 Bulan</div>
      </div>
    </div>
    <div class="content-body-right">
      <div class="highlight-card">
        <div class="detail-label">COCOK UNTUK</div>
        <div class="detail-value">Enterprise &amp; Large-Scale Org</div>
      </div>
      <div class="highlight-card">
        <div class="detail-label">FASE BISNIS</div>
        <div class="detail-value">Transformasi Digital Menyeluruh</div>
      </div>
    </div>
  </div>
  <div class="footer-brand">© venturo.id</div>
</div></body></html>"""


# ─────────────────────────────────────────────────────────────────────────────
# Theme variants (square 1024×1024)
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
