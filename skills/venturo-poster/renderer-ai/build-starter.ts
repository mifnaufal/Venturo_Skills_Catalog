import * as fs from 'fs';
import * as path from 'path';

const logoPath = path.resolve(__dirname, '..', '..', '..', 'image.png');
const logoB64 = fs.readFileSync(logoPath).toString('base64');
const logoDataUri = 'data:image/png;base64,' + logoB64;

const html = `<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<title>Venturo Starter Poster</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body {
    width: 2048px;
    height: 2048px;
    overflow: hidden;
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background: #FFFFFF;
    color: #0F172A;
  }
  .poster {
    position: relative;
    width: 2048px;
    height: 2048px;
    overflow: hidden;
    background: #FFFFFF;
  }
  /* Dot grid background — covers entire canvas */
  .poster::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: radial-gradient(circle, #006D79 1.5px, transparent 1.5px);
    background-size: 64px 64px;
    opacity: 0.06;
    pointer-events: none;
    z-index: 0;
  }
  .bg-svg {
    position: absolute;
    top: 0; left: 0;
    width: 2048px;
    height: 2048px;
    pointer-events: none;
    z-index: 0;
  }
  .content {
    position: relative;
    z-index: 2;
    width: 2048px;
    height: 2048px;
    padding: 64px 64px 56px 64px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* Header row */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    width: 100%;
  }
  .logo-wrap {
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  .logo-img {
    width: 384px;
    height: auto;
    display: block;
  }
  .tier-badge {
    display: inline-flex;
    align-items: center;
    gap: 14px;
    padding: 14px 28px;
    border-radius: 999px;
    border: 2px solid #006D79;
    background: #FFFFFF;
  }
  .tier-badge-dot {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    background: #006D79;
  }
  .tier-badge-text {
    font-size: 28px;
    font-weight: 800;
    color: #006D79;
    letter-spacing: 4px;
  }

  .tier-name {
    font-size: 224px;
    font-weight: 900;
    letter-spacing: -8px;
    line-height: 0.95;
    color: #006D79;
    text-align: right;
    text-transform: uppercase;
    max-width: 1300px;
  }

  /* Budget section */
  .budget-row {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 28px;
    margin-top: 16px;
  }
  .section-label {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: 8px;
    color: #006D79;
    text-transform: uppercase;
  }
  .budget-pill {
    display: inline-flex;
    align-items: center;
    gap: 24px;
    padding: 24px 56px;
    background: #006D79;
    color: #FFFFFF;
    border-radius: 999px;
    font-size: 56px;
    font-weight: 800;
    letter-spacing: 2px;
    box-shadow: 0 16px 32px rgba(0, 109, 121, 0.25);
  }
  .tagline {
    font-size: 40px;
    font-weight: 400;
    color: #374151;
    line-height: 1.4;
    max-width: 1600px;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }
  .tagline em {
    font-style: italic;
    color: #006D79;
    font-weight: 600;
  }

  /* Highlights — 4 minimal value props */
  .highlights {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 28px 48px;
    margin-top: 8px;
  }
  .hl-item {
    display: flex;
    align-items: center;
    gap: 28px;
  }
  .check {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: #006D79;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: 800;
    flex-shrink: 0;
  }
  .hl-text {
    font-size: 36px;
    font-weight: 600;
    color: #0F172A;
    line-height: 1.25;
    word-wrap: break-word;
    overflow-wrap: break-word;
  }

  /* Timeline row */
  .timeline {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 24px;
    margin-top: 8px;
  }
  .phase {
    background: linear-gradient(135deg, #F0F9FA 0%, #E0F2F4 100%);
    border: 2px solid #B8E0E5;
    border-radius: 28px;
    padding: 32px 36px;
    display: flex;
    flex-direction: column;
    gap: 12px;
    position: relative;
  }
  .phase-num {
    font-size: 24px;
    font-weight: 800;
    color: #006D79;
    letter-spacing: 4px;
  }
  .phase-name {
    font-size: 32px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1.2;
  }
  .phase-dur {
    font-size: 36px;
    font-weight: 800;
    color: #006D79;
    line-height: 1.1;
  }
  .phase-desc {
    font-size: 24px;
    font-weight: 400;
    color: #64748B;
    line-height: 1.35;
  }

  /* Bottom row: team + CTA */
  .bottom-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 48px;
    margin-top: 8px;
  }
  .team {
    display: flex;
    align-items: center;
    gap: 32px;
  }
  .team-icon {
    width: 96px;
    height: 96px;
    border-radius: 50%;
    background: #006D79;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }
  .team-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .team-label {
    font-size: 22px;
    font-weight: 800;
    letter-spacing: 6px;
    color: #006D79;
    text-transform: uppercase;
  }
  .team-detail {
    font-size: 32px;
    font-weight: 600;
    color: #0F172A;
    line-height: 1.3;
  }
  .cta {
    display: inline-flex;
    align-items: center;
    gap: 20px;
    padding: 28px 56px;
    background: #10B981;
    color: #FFFFFF;
    border-radius: 999px;
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 1px;
    box-shadow: 0 16px 32px rgba(16, 185, 129, 0.3);
  }
  .cta-arrow {
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    font-weight: 800;
  }

  /* Footer */
  .footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 8px;
    padding-top: 16px;
    border-top: 1px solid rgba(0, 109, 121, 0.15);
  }
  .footer-text {
    font-size: 24px;
    font-weight: 500;
    color: #64748B;
    letter-spacing: 2px;
  }
  .footer-text strong {
    color: #006D79;
    font-weight: 800;
  }
</style>
</head>
<body>
<div class="poster">
  <!-- Background SVG decorations -->
  <svg class="bg-svg" viewBox="0 0 2048 2048" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#006D79" stop-opacity="0.08"/>
        <stop offset="100%" stop-color="#009BAD" stop-opacity="0.15"/>
      </linearGradient>
      <radialGradient id="glow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#009BAD" stop-opacity="0.12"/>
        <stop offset="100%" stop-color="#009BAD" stop-opacity="0"/>
      </radialGradient>
    </defs>
    <!-- Top wave -->
    <path d="M0,0 C400,120 800,40 1200,160 S1800,80 2048,160 L2048,0 Z" fill="url(#waveGrad)"/>
    <!-- Bottom wave -->
    <path d="M0,2048 C400,1928 800,2008 1200,1888 S1800,1968 2048,1888 L2048,2048 Z" fill="url(#waveGrad)" opacity="0.6"/>
    <!-- Glow accents -->
    <circle cx="320" cy="1024" r="600" fill="url(#glow)"/>
    <circle cx="1720" cy="1400" r="500" fill="url(#glow)"/>
    <!-- Network nodes cluster top-right -->
    <circle cx="1820" cy="180" r="12" fill="#006D79" opacity="0.25"/>
    <circle cx="1920" cy="280" r="8" fill="#009BAD" opacity="0.3"/>
    <circle cx="1880" cy="340" r="6" fill="#006D79" opacity="0.2"/>
    <line x1="1820" y1="180" x2="1920" y2="280" stroke="#009BAD" stroke-width="2" opacity="0.2"/>
    <line x1="1920" y1="280" x2="1880" y2="340" stroke="#006D79" stroke-width="2" opacity="0.2"/>
    <!-- Hexagon bottom-left -->
    <polygon points="120,1820 180,1790 240,1820 240,1880 180,1910 120,1880" fill="none" stroke="#006D79" stroke-width="2" opacity="0.2"/>
    <polygon points="200,1880 260,1850 320,1880 320,1940 260,1970 200,1940" fill="none" stroke="#009BAD" stroke-width="2" opacity="0.15"/>
    <!-- Small circles scattered -->
    <circle cx="160" cy="600" r="8" fill="#006D79" opacity="0.2"/>
    <circle cx="100" cy="700" r="4" fill="#009BAD" opacity="0.3"/>
    <circle cx="1900" cy="900" r="6" fill="#006D79" opacity="0.25"/>
    <circle cx="1980" cy="980" r="4" fill="#009BAD" opacity="0.3"/>
    <circle cx="80" cy="1500" r="6" fill="#009BAD" opacity="0.2"/>
  </svg>

  <div class="content">
    <!-- Header -->
    <div class="header">
      <div class="logo-wrap">
        <img class="logo-img" src="${logoDataUri}" alt="Venturo"/>
        <div class="tier-badge">
          <span class="tier-badge-dot"></span>
          <span class="tier-badge-text">PAKET STARTER</span>
        </div>
      </div>
      <div class="tier-name">Paket<br/>Starter</div>
    </div>

    <!-- Budget + tagline -->
    <div class="budget-row">
      <div class="section-label">Estimasi Investasi</div>
      <div class="budget-pill">Rp20 Juta – Rp80 Juta</div>
      <div class="tagline">Solusi digital <em>terjangkau</em> untuk UMKM, usaha mikro, perusahaan kecil, dan startup yang baru mulai go digital.</div>
    </div>

    <!-- Highlights (minimal — 4 value props) -->
    <div class="highlights">
      <div class="hl-item">
        <div class="check">✓</div>
        <div class="hl-text">Website &amp; Mobile App sesuai kebutuhan</div>
      </div>
      <div class="hl-item">
        <div class="check">✓</div>
        <div class="hl-text">UI/UX modern, responsif, mudah dipakai</div>
      </div>
      <div class="hl-item">
        <div class="check">✓</div>
        <div class="hl-text">Integrasi WhatsApp, Payment, API</div>
      </div>
      <div class="hl-item">
        <div class="check">✓</div>
        <div class="hl-text">Dashboard monitoring &amp; reporting</div>
      </div>
    </div>

    <!-- Timeline -->
    <div class="timeline">
      <div class="phase">
        <div class="phase-num">FASE 01</div>
        <div class="phase-name">Analysis &amp; Design</div>
        <div class="phase-dur">1 – 2 Minggu</div>
        <div class="phase-desc">Riset kebutuhan &amp; perancangan sistem</div>
      </div>
      <div class="phase">
        <div class="phase-num">FASE 02</div>
        <div class="phase-name">Development</div>
        <div class="phase-dur">2 Minggu – 1 Bulan</div>
        <div class="phase-desc">Pembangunan website &amp; aplikasi</div>
      </div>
      <div class="phase">
        <div class="phase-num">FASE 03</div>
        <div class="phase-name">Testing &amp; Go-Live</div>
        <div class="phase-dur">1 – 2 Minggu</div>
        <div class="phase-desc">SIT, UAT, deployment &amp; peluncuran</div>
      </div>
    </div>

    <!-- Bottom: team + CTA -->
    <div class="bottom-row">
      <div class="team">
        <div class="team-icon">
          <svg width="56" height="56" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="9" cy="8" r="3"/>
            <circle cx="17" cy="9" r="2.5"/>
            <path d="M3 20c0-3 3-5 6-5s6 2 6 5"/>
            <path d="M15 20c0-2 2-3.5 4-3.5s2 1 2 1"/>
          </svg>
        </div>
        <div class="team-info">
          <div class="team-label">Dedicated Team</div>
          <div class="team-detail">1 Business Analyst · 1 Senior Software Engineer</div>
        </div>
      </div>
      <div class="cta">
        <span>Konsultasi Gratis</span>
        <span class="cta-arrow">→</span>
      </div>
    </div>

    <!-- Footer -->
    <div class="footer">
      <div class="footer-text">© <strong>venturo.id</strong> — Build your digital future</div>
      <div class="footer-text">Custom Software · Web · Mobile</div>
    </div>
  </div>
</div>
</body>
</html>`;

const outDir = path.resolve(__dirname, '..', '..', '..', '..', 'output');
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, 'starter-poster.html');
fs.writeFileSync(outPath, html);
console.log('HTML written:', outPath, 'size:', fs.statSync(outPath).size);
