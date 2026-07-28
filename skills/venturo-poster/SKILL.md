---
name: venturo-poster
description: Generate professional HD service package posters for Venturo (venturo.id) matching their brand aesthetic. Produces 4096×4096px PNG (2048×2048 container, Device Scale Factor 2). Always produces ONE poster per tier via Playwright rendering with SVG illustrations and/or p5.js generative effects.
---

# Venturo Poster Generation — HD Edition

Generate branded **2048×2048px** marketing posters for Venturo service packages (resizable to 1024px without quality loss). Each poster follows the visual identity of venturo.id — dense, bold, professional, and visually rich (**"rame"**). Rendered as PNG via Playwright browser screenshot at **2x Device Scale Factor** for crisp HD output.

Reference file: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/packages_context.md` contains all content data, color palette, and design specs.
Style reference: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/image.png` (logo Venturo)

---

## Trigger Behavior

When loaded, **immediately begin the Q&A flow below**. Do NOT generate any poster until the user has answered the required questions. Never assume tier selections or content preferences.

---

## CRITICAL: ONE DESIGN = ONE TIER

**IMPORTANT RULE: Every poster must contain ONLY ONE tier.**

Each poster shows exactly ONE package tier with ALL its details in a single cohesive layout.

If the user requests "all three tiers", generate **three separate poster files** — one per tier. Each file is its own complete design.

---

## Q&A Flow

### Step 1: Choose Tier(s)

Ask the user which tier(s) they want posters for:

| Option | Description |
|--------|-------------|
| Starter | White background, single-tier poster |
| Growth | White/off-white background with dot grid, single-tier poster |
| Enterprise | Dark teal gradient background, single-tier poster |
| All Three | One poster per tier, rendered sequentially |

If the user says "all three" or lists multiple tiers, create **separate PNGs** for each — one file per tier. Name them `venturo-starter.png`, `venturo-growth.png`, `venturo-enterprise.png` respectively.

### Step 2: Select Content Sections

Ask which content sections should appear on the poster:

- **Masalah** — Problems/pain points that Venturo solves
- **Solusi** — Solutions Venturo builds
- **Hasil** — Results clients get
- **Paket Details** — Tier name, ideal-for description, budget range, dedicated team members, timeline breakdown *(always included by default unless explicitly excluded)*
- **Custom Text** — User may provide their own copy for any section

> If the user does not specify sections, include ALL of them (Masalah + Solusi + Hasil + Paket Details).

### Step 3: Custom Messaging (Optional)

Ask if the user wants to modify any existing copy.

If the user says "no changes" or skips this step, use the **default content from the reference data below**.

---

## Design Rules

After the Q&A completes, the AI handles ALL design decisions autonomously. The user trusts you to make visual choices.

### Rame Tapi Simple

Visually rich dengan SVG shapes, pattern, gradient — tapi tetap clean dengan hierarchy jelas. Banyak elemen visual tapi teratur, gak chaotic. Ibaratnya: banyak bumbu tapi rasanya seimbang.

### CRITICAL: HD Double Size Rule

**Container & viewport HARUS 2048×2048px** (bukan 1024px). Semua ukuran CSS, font, padding, spacing, dan koordinat SVG harus DI-DOUBLE dari target 1024px.

| Item | Target | HD Value |
|------|--------|----------|
| Container | 1024×1024 | **2048×2048** |
| Tier name font | 112px | **224px** |
| Budget label font | 28px | **56px** |
| Feature text font | 18px | **36px** |
| Section label font | 12px | **24px** |
| Tagline font | 20px | **40px** |
| Footer font | 12px | **24px** |
| Checkmark circle | 28×28px | **56×56px** |
| Padding container | 32px | **64px** |
| Dot grid spacing | 32px | **64px** |
| Section gap | 16px | **32px** |

### Canvas Setup

- Exact size: **2048×2048px** (double for HD)
- Render HTML/CSS inside a fixed container sized exactly **2048×2048px**
- CSS `overflow: hidden` on root, no scrollbars
- Everything fits within the canvas — no content clipped
- **Device Scale Factor 2** saat init browser & screenshot `scale="device"` → output 4096×4096px

### Typography

Always load fonts from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
```

Font family: `'Inter', system-ui, -apple-system, sans-serif`

| Element | 1024 target | 2048 HD | Weight | Notes |
|---------|-------------|---------|--------|-------|
| Tier name | 112px | **224px** | 900 | Massive, tight tracking -8px |
| Budget label | 28px | **56px** | 800 | Rounded pill box |
| Feature / bullet text | 18px | **36px** | 600 | Checkmark icon + text |
| Section labels | 12px | **24px** | 800 | Uppercase, letter-spacing 8px |
| Tagline / description | 20px | **40px** | 400–500 | Under budget box |
| Footer | 12px | **24px** | 400 | Muted color, subtle |

**CRITICAL — Text Wrapping:** Long sentences must wrap gracefully onto multiple lines. Never let text overflow. Use `word-wrap: break-word` and `overflow-wrap: break-word` on all text containers. No text should be clipped, cut off, or overlap.

### Color Assignment Per Tier

| Tier | Background | Primary Accent | Budget Pill |
|------|-----------|---------------|-------------|
| **Starter** | `#FFFFFF` (white) | `#006D79` | `#006D79` solid pill, white text |
| **Growth** | `#FFFFFF` + dot grid (`#009BAD` 5% opacity) | `#006D79` | Teal gradient (`#006D79` → `#009BAD`), white text |
| **Enterprise** | Gradient `#0A1B1F` → `#112D35` | `#009BAD` | `#009BAD` solid pill, dark text |

**Checkmark circles** use the same accent color: **56×56px** filled circle with a white checkmark character (✓ / U+2713) inside.

### Illustrations — SVG Elements (WAJIB)

Setiap poster WAJIB punya illustrasi vector via elemen SVG. Bikin poster iklan — bukan poster brosur biasa.

| Tag | Fungsi | Contoh (nilai HD 2x) |
|-----|--------|----------------------|
| `<circle>` | Lingkaran | `<circle cx="200" cy="160" r="80" fill="#006D79" opacity="0.1"/>` |
| `<rect>` | Persegi | `<rect x="100" y="100" width="400" height="200" rx="20" fill="url(#grad)"/>` |
| `<path>` | Garis/kurva bebas | `<path d="M0,400 Q400,200 800,400 T1600,400" stroke="#009BAD" fill="none"/>` |
| `<polygon>` | Segitiga/hexagon | `<polygon points="200,0 400,100 400,300 200,400 0,300 0,100" fill="none" stroke="#006D79"/>` |
| `<polyline>` | Garis bersambung | `<polyline points="0,200 200,100 400,160 600,40" fill="none" stroke="#009BAD"/>` |
| `<line>` | Garis lurus | `<line x1="0" y1="200" x2="2048" y2="200" stroke="#006D79" opacity="0.1"/>` |
| `<pattern>` | Pola berulang | buat dot grid / hex grid via `<defs>` |
| `<linearGradient>` | Gradien linear | buat di `<defs>`, dipake di `fill="url(#id)"` |
| `<radialGradient>` | Gradien radial | cocok buat glow effect |

**Teknik Implementasi:**
1. **Pattern (dot grid / hex grid):** Pakai `<pattern>` di `<svg>` atau CSS `background-image`
2. **Abstract shapes:** Taruh `<circle>`, `<polygon>`, `<rect>` dengan `opacity` rendah di background
3. **Network nodes:** Kombinasi `<circle>` + `<line>` yang connect
4. **Wave / flow:** Pakai `<path>` dengan bezier curve (`C`, `Q`, `S`)
5. **Gradient overlay:** `<rect width="2048" height="2048" fill="url(#grad)" opacity="0.1"/>`

**Contoh implementasi di HTML (nilai HD 2x):**
```html
<style>
  .container::before {
    content: ''; position: absolute; inset: 0;
    background-image: radial-gradient(circle, #006D79 1.5px, transparent 1.5px);
    background-size: 64px 64px;
    opacity: 0.06; pointer-events: none;
  }
</style>
<svg style="position:absolute;top:0;left:0;width:2048px;height:2048px;pointer-events:none;z-index:0;">
  <defs>
    <linearGradient id="wave" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#006D79" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#009BAD" stop-opacity="0.15"/>
    </linearGradient>
  </defs>
  <path d="M0,400 C400,300 800,560 1200,400 S1600,600 2048,400 L2048,0 L0,0 Z" fill="url(#wave)"/>
  <circle cx="1600" cy="240" r="12" fill="#006D79" opacity="0.2"/>
  <circle cx="1720" cy="180" r="8" fill="#009BAD" opacity="0.3"/>
  <line x1="1600" y1="240" x2="1720" y2="180" stroke="#009BAD" stroke-width="2" opacity="0.2"/>
  <polygon points="1800,500 1850,470 1900,500 1900,560 1850,590 1800,560" fill="none" stroke="#006D79" stroke-width="2" opacity="0.15"/>
</svg>
```

**Penerapan per tier:**
| Tier | Ilustrasi |
|------|-----------|
| Starter | Dot grid subtle (CSS) + 2-3 circle abstract + 1 wave path tipis |
| Growth | Dot grid medium + network nodes (circle+line) + 1 hexagon polygon decoratif |
| Enterprise | Dark gradient bg + radial glow (radialGradient) + abstract wave path besar + geometric diamond (polygon) |

### Pendekatan Generatif dengan p5.js

Selain SVG, bisa juga pake **p5.js** untuk efek-efek generatif yang lebih random/organic. Dua approach bisa dikombinasi dalam 1 HTML yang sama.

**Cara pake:**
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
<script>
function setup() {
  let c = createCanvas(2048, 2048);
  c.position(0, 0);
  c.style('z-index', '0');
  c.style('pointer-events', 'none');
  noLoop();
}
function draw() {
  // Contoh 1: Noise wave
  noFill();
  stroke('#006D79');
  strokeWeight(1);
  for (let y = 0; y < 2048; y += 40) {
    beginShape();
    for (let x = 0; x < 2048; x += 10) {
      let n = noise(x * 0.005, y * 0.005) * 60;
      vertex(x, y + n);
    }
    endShape();
  }

  // Contoh 2: Random dot clusters
  for (let i = 0; i < 60; i++) {
    let x = random(2048);
    let y = random(2048);
    let r = random(4, 16);
    let alpha = random(0.04, 0.12);
    fill('#006D79');
    noStroke();
    circle(x, y, r);
  }
}
</script>
```

**Efek yang bisa dibikin p5.js:**
- Noise wave / flowing lines (organic background)
- Random dot clusters dengan variasi size & opacity
- Geometric grid dengan rotasi acak
- Particle system sebagai background texture
- Gradient mesh yang smooth

**Catatan:** Canvas p5.js harus di z-index 0 (di belakang konten). Konten HTML tetaplah di atas via z-index lebih tinggi.

## CRITICAL: FULL CANVAS RULE — NO EMPTY SPACE

The 2048×2048 canvas MUST be 100% filled. **Zero empty gaps.** If content sections don't reach the bottom, add visual density elements to fill remaining space. A poster with empty gaps = failed poster.

### Anti-Gap System

| Problem | Solution |
|---------|----------|
| Fitur cuma 3-4 item | Tambah item dari default set sampai minimal 8 checkmark (acak urutan, jangan duplikat) |
| Timeline pendek | Full-width progress bar 2048px, breakdown tiap fase dengan box besar |
| Team cuma 2 orang | Kartu team full-width dengan icon + role + deskripsi detail |
| Masih ada space kosong | Tambah SVG decorative cluster (lingkaran, garis, dot) di area kosong |
| Bener2 mentok | Tambah "Mengapa Memilih Venturo?" section dengan 3-4 bullet point ekstra |

### Layout Structure (Flexible Height — semua nilai double)

Pakai **flexbox column** dengan `justify-content: space-between` biar konten terdistribusi merata dari atas ke bawah. Jangan pake fixed-height zones yang rigid.

```
┌──────────────┬──────────────┐
│   LOGO       │  TIER NAME   │  ← Z-Pattern 1
│   (72-96px)  │  224px bold  │
├──────────────┴──────────────┤
│   BUDGET PILL + TAGLINE     │  ← Full-width
│   56px pill, 40px tagline   │
├─────────────────────────────┤
│   SECTION: FEATURES         │  ← Full-width
│   8-12 checkmark items      │     item per baris
│   36px text + 56px circle   │
├─────────────────────────────┤
│   TIMELINE (3-phase)        │  ← Full-width
│   Progress bar 2048px       │     fase box besar
├─────────────────────────────┤
│   TEAM CARDS +              │  ← 2 column
│   BOTTOM GRID               │     or full-width
├──────────────┬──────────────┤
│   EXTRA       │  CTA BUTTON │  ← Z-Pattern 4
│   DECORATION  │  #10B981    │
└──────────────┴──────────────┘
│   FOOTER © venturo.id       │
└─────────────────────────────┘
```

1. **Header row** — Logo (kiri, 72-96px) + Tier name "PAKET [TIER]" (kanan, 224px)
   - **WAJIB: pakai Venturo logo dari `image.png`.** Jangan tulis "VENTURO" plain text.
   - Gap antar logo & tier: auto (flexbox justify-between)

2. **Budget & Tagline** — Full-width row
   - Pill budget **56px**, rounded penuh
   - Tagline **40px** di bawah pill

3. **Features / Checkmarks** — Full-width, 1 item per baris
   - Label uppercase **24px**, letter-spacing 8px
   - Tiap item: **56×56px** checkmark + teks **36px**
   - MINIMAL 8 item. Kalau data cuma 4-5, tambah dari set default (Masalah/Solusi/Hasil)

4. **Timeline 3-Phase** — Full-width progress bar
   - 3 fase horizontal, box masing-masing diberi background ringan
   - Duration bold (**40px**), deskripsi (**28px**)
   - Panah/connector antar fase

5. **Team + Bottom Content** — 2-column atau full-width
   - Nama role (**32px**) + jumlah orang + ikon
   - Grid cards untuk bottom section

6. **CTA Row** — Full-width baris terakhir sebelum footer
   - CTA button "Konsultasi Gratis" di kanan
   - Bisa ada dekorasi SVG di kiri kalau ada space

7. **Footer** — "© venturo.id" **24px**, center atau kanan

### Background Texture (the "rame" factor) — nilai double

| Tier | Background Texture |
|------|-------------------|
| **Starter** | Dot grid (`#006D79` at 6% opacity), spacing ~**64px** |
| **Growth** | Dot grid (`#009BAD` at 5% opacity), spacing ~**48px** |
| **Enterprise** | Dot grid overlay + radial glow radius ~**800px** |

### Visual Density Checklist

- [ ] Canvas **2048×2048 100% terisi** — ga ada celah kosong di manapun
- [ ] Ada illustrasi SVG ATAU p5.js (bukan cuma CSS doang)
- [ ] Ukuran container **2048×2048** (bukan 1024)
- [ ] Semua ukuran font/padding/spacing sudah di-double
- [ ] **Tier name 224px = satu-satunya focal point** — illustrasi di background, opacity max 0.15
- [ ] **CTA button ada** — "Konsultasi Gratis" / "Hubungi Kami", accent color (`#10B981` atau `#F59E0B`)
- [ ] **Z-Pattern layout** — Logo ki-atas → Tier ka-atas → Content ki-bawah → CTA ka-bawah
- [ ] Margin luar container: **64px** kiri & kanan (konsisten)
- [ ] Gap antar section: **24–32px** (ketat biar rapet, bukan 48-64)
- [ ] **Minimal 8 checkmark items** — tambah dari default set kalo data sedikit
- [ ] Dot grid or texture covers the entire canvas background
- [ ] **224px** tier name anchors the composition
- [ ] Budget pill is prominent and colorful
- [ ] Multiple visual elements: pills, cards, icons, gradients, SVG/p5.js
- [ ] Bottom grid cards + footer anchor

### "Rame" vs "Rumput"

| "Rame" (Good) | "Rumput" (Bad) |
|---------------|----------------|
| Information-dense but organized | Chaotic, messy clutter |
| Clear hierarchy through size & weight | No visual distinction |
| Consistent vertical rhythm | Random spacing |
| Background textures + SVG/p5.js add depth | Flat, boring backgrounds |

### Design Principles from Research

**1. Satu Focal Point — Tier Name = Raja**
- Tier name **224px** adalah satu-satunya elemen dominan. Jangan ada yang compete.
- Ilustrasi SVG/p5.js di `z-index: 0` dengan `opacity` max **0.15** — background doang.
- Logo Venturo kecil (72–96px) di pojok kiri atas — jangan gede-gedein.

**2. Z-Pattern Layout**
Mata viewer scan dalam pola Z: **kiri-atas → kanan-atas → kiri-bawah → kanan-bawah**.
```
1. Logo (kiri-atas, x=64, y=48)   →   2. Tier name (kanan-atas, 224px)
                                        ↓
3. Content sections (kiri-bawah)   →   4. CTA / Footer (kanan-bawah)
```
- Gunakan pola ini untuk posisi semua elemen.
- Content sections rata kiri semua (F-pattern di dalam Z-pattern).

**3. CTA Button — WAJIB Ada**
- "© venturo.id" di footer aja **tidak cukup**. Setiap poster butuh **Call to Action**.
- **CTA button:** "Konsultasi Gratis" atau "Hubungi Kami" berbentuk pill / rounded rectangle.
- Posisi: **kanan-bawah** (mengikuti Z-pattern), atau **center-bottom**.
- Warna CTA: pilih 1 accent color yang kontras — misal **#10B981** (hijau) atau **#F59E0B** (kuning emas).
- Ukuran: font **32px**, weight 700, padding internal 20px 48px, border-radius 32px.

**4. White Space & Grid Alignment**
- Margin luar container: **64px** kiri & kanan (konsisten).
- Gap antar section: **48–64px** (jangan kurang dari 48px).
- Semua konten teks **rata kiri** — jangan center alignment kecuali CTA.
- Padding internal card/block: **48px**.
- Gunakan jarak napas di sekitar tier name dan budget pill — mereka harus punya "ruang" untuk bernapas.

**5. Color Limit — Max 4 Warna**
| Peran | Contoh |
|-------|--------|
| Background | #FFFFFF atau #0A1B1F gradient |
| Primary accent | #006D79 |
| Secondary accent | #009BAD |
| CTA accent | #10B981 atau #F59E0B |
- Jangan pakai warna lain di luar 4 ini.
- Checkmark circles pake primary accent.
- Text body pake #374151 (dark gray) atau putih di dark bg.

---

## Rendering Instructions

### File Format

- **Format:** PNG image, starting from **2048×2048px** canvas
- **Method:** Render HTML/CSS via headless browser (Playwright), then capture screenshot with **Device Scale Factor 2**
- **File naming:** `venturo-{tier}.png` (e.g., `venturo-starter.png`)
- **Output size:** **4096×4096px** (2048 viewport × 2 DSF) — super HD

### Playwright Tool Chain

Preferred sequence using MCP tools:

1. `mcp__playwright__browser_navigate(url="about:blank")` — start fresh page
2. `mcp__playwright__browser_resize(width=2048, height=2048)` — set viewport to double size
3. `mcp__playwright__browser_evaluate(function="(page) => { return page.setContent(htmlString); }")` — inject complete HTML with all sizes doubled
4. `mcp__playwright__browser_wait_for(time=3)` — wait for fonts and p5.js to load
5. `mcp__playwright__browser_take_screenshot(type="png", scale="device", filename="venturo-{tier}.png")` — capture at device resolution (2x)

### HTML Construction Guidelines

- Build the complete HTML document as a single string
- Include `<link>` or `@import` for Google Font Inter
- Include `<style>` block with all CSS inline
- Use **the Venturo logo image** embedded as base64 data URI in an `<img>` tag
- Container: **2048×2048px** with `position: relative; overflow: hidden`
- All sizes: **DOUBLE** from target 1024px design
- Embed SVG elements via `<svg>` absolute dengan `pointer-events:none; z-index:0;`
- **Opsional:** Load p5.js via CDN untuk efek generatif, canvas di z-index 0
- Background dot grid as absolutely-positioned div with CSS radial-gradient pattern
- Text containers must have `word-wrap: break-word; overflow-wrap: break-word; white-space: normal;`

### Key CSS Properties for Text Safety

```css
.content-text {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal !important;
  max-width: calc(100% - 100px);
}
.card-section {
  word-break: break-word;
  overflow: hidden;
}
```

---

## Content Mapping Reference

Gunakan `opsi-poster.md` untuk 4 format konten berbeda (Opsi 1–4).

Default content blocks:

### Masalah (Problems) — 7 items
1. Perusahaan membutuhkan website atau aplikasi yang benar-benar sesuai dengan proses bisnisnya.
2. Sudah menggunakan aplikasi berlangganan, namun fitur yang tersedia belum mampu memenuhi kebutuhan operasional.
3. Proses bisnis harus menyesuaikan aplikasi, bukan aplikasi yang mengikuti kebutuhan perusahaan.
4. Sulit melakukan kustomisasi karena keterbatasan sistem yang digunakan.
5. Sistem yang ada tidak dapat terintegrasi dengan aplikasi atau layanan lain yang sudah dimiliki.
6. Tampilan aplikasi kurang user-friendly dan tidak mencerminkan identitas perusahaan.
7. Seiring pertumbuhan bisnis, sistem yang digunakan tidak lagi mampu mendukung kebutuhan operasional.

### Solusi (Solutions) — 7 items
1. Pengembangan Website dan Mobile Application (Android & iOS) yang dirancang khusus sesuai kebutuhan perusahaan.
2. Analisis kebutuhan bisnis untuk memastikan setiap fitur mendukung proses operasional.
3. Desain UI/UX modern, responsif, dan mudah digunakan.
4. Pengembangan fitur yang fleksibel sesuai kebutuhan saat ini maupun pengembangan di masa mendatang.
5. Integrasi dengan ERP, CRM, HRIS, Payment Gateway, WhatsApp, API, dan sistem existing.
6. Dashboard monitoring dan reporting untuk mendukung pengambilan keputusan.
7. Sistem yang aman, scalable, dan siap berkembang mengikuti pertumbuhan bisnis.

### Hasil (Results) — 6 items
1. Website atau aplikasi yang dirancang sesuai kebutuhan dan proses bisnis perusahaan.
2. Meningkatkan efisiensi operasional melalui digitalisasi dan otomatisasi proses kerja.
3. Sistem yang fleksibel dan mudah dikembangkan seiring pertumbuhan bisnis.
4. Integrasi data yang lebih baik sehingga proses bisnis menjadi lebih cepat dan akurat.
5. Pengalaman pengguna yang lebih baik dengan UI/UX yang modern dan intuitif.
6. Mendukung pengambilan keputusan melalui dashboard dan laporan yang terintegrasi.

### Tier Package Details

#### Starter
- **Ideal untuk:** UMKM, usaha mikro, perusahaan kecil, dan startup
- **Budget Proyek:** Rp20 Juta – Rp80 Juta
- **Dedicated Team:** 1 Business Analyst, 1 Senior Software Engineer
- **Timeline:** Analysis & Design: 1–2 Minggu | Development: 2 Minggu–1 Bulan | Testing & Go-Live: 1–2 Minggu

#### Growth
- **Ideal untuk:** Perusahaan berkembang (ERP, CRM, HRIS, Finance, Inventory, WMS, dll)
- **Budget Proyek:** Rp80 Juta – Rp250 Juta
- **Dedicated Team:** 1 BA, 1 SSE, 1 UI/UX Designer, 1 QA Engineer
- **Timeline:** Analysis & Design: 2 Minggu–1 Bulan | Development: 1–2 Bulan | Testing & Go-Live: 2 Minggu–1 Bulan

#### Enterprise
- **Ideal untuk:** Perusahaan menengah hingga enterprise
- **Budget Proyek:** Mulai dari Rp250 Juta
- **Dedicated Team:** 1 BA, 1 SSE, 1 Intermediate SE, 1 UI/UX, 1 QA, 1 Penetration Tester
- **Timeline:** Analysis & Design: 1–2 Bulan | Development: 2–4 Bulan | Testing & Deployment: 2 Bulan

---

## Quality Checklist

### Content Accuracy
- [ ] Poster shows exactly ONE tier (not multiple tiers combined)
- [ ] Tier name matches what user requested
- [ ] Budget range is correct
- [ ] Team members are listed correctly for the selected tier
- [ ] Timeline phases and durations match the reference data
- [ ] No content sections accidentally omitted

### Layout & Design Principles
- [ ] **Canvas 2048×2048 100% FULL** — zero empty gaps
- [ ] Kalau content kurang, **wajib tambah filler** (SVG deco / extra checkmark items / extra section)
- [ ] **Tier name 224px = satu-satunya focal point** — tidak ada elemen lain yang compete
- [ ] **CTA button "Konsultasi Gratis" atau "Hubungi Kami" ada** di kanan-bawah
- [ ] **CTA pake accent color** (`#10B981` / `#F59E0B`) — bukan teal
- [ ] **Z-Pattern layout** diikuti: Logo → Tier name → Content → CTA
- [ ] Margin luar **64px**, gap antar section **24–32px** (rapet, jangan longgar)
- [ ] **Minimal 8 checkmark items** per poster
- [ ] Warna max 4: background, primary, secondary, CTA accent

### Visual Completeness
- [ ] Ada illustrasi via SVG ATAU p5.js (jangan cuma CSS)
- [ ] Container **2048×2048**, semua ukuran sudah di-double
- [ ] Venturo logo image embedded in header (not plain text)
- [ ] Background texture covers the entire canvas
- [ ] Budget pill has strong color contrast
- [ ] Checkmarks consistently **56×56px** per tier
- [ ] Bottom grid cards have visual distinction
- [ ] Footer "© venturo.id" is present
- [ ] No clipping — everything fits within 2048×2048

### Readability
- [ ] **224px** tier name clearly visible at top
- [ ] Budget pill legible at **56px**
- [ ] Feature text at **36px** not overlapping
- [ ] Enough contrast between text and background
- [ ] All text wraps properly — no clipping

### Technical
- [ ] Screenshot captured at **scale="device"** (DSF 2 → 4096×4096)
- [ ] Image is saved as PNG (not JPEG)
- [ ] Google Font Inter loads correctly
- [ ] No scrollbar or overflow artifacts visible

---

## When User Provides Custom Content

If the user supplies their own text (custom problems, solutions, taglines, budget figures, etc.):
1. Insert the custom text exactly as provided (do not rephrase unless asked)
2. If custom text is very long, allow text to wrap to multiple lines — don't truncate or clip
3. If custom text is very short for a section, pad with related items from the default set to maintain visual density
4. Always confirm before rendering if custom content significantly alters the expected layout

---

## After Poster Is Generated

1. Confirm completion — state file names and output size (4096×4096px)
2. Display screenshot thumbnail
3. Ask: *"Mau direvisi atau lanjut tier lain?"*

---

## What NOT to Do

- **Do NOT** use 1024×1024 container — always use **2048×2048** for HD
- **Do NOT** forget to double all sizes (font, padding, SVG coordinates)
- **Do NOT** generate poster without completing Q&A first
- **Do NOT** put multiple tiers on one poster — ONE poster = ONE tier only
- **Do NOT** skip background texture / SVG / p5.js illustration
- **Do NOT** use colors outside Venturo palette
- **Do NOT** use the Venturo wordmark as plain text — always embed the logo image
- **Do NOT** change font family — always use Inter
- **Do NOT** render as JPEG — always PNG
- **Do NOT** let text overflow, clip, or overlap
- **Do NOT** mix tier content in one poster
- **Do NOT** lupa CTA button — setiap poster WAJIB punya "Konsultasi Gratis" atau "Hubungi Kami"
- **Do NOT** buat elemen lain compete dengan tier name 224px — illustrasi harus di background
- **Do NOT** lupa white space — margin luar **64px**, gap antar section **24–32px**
- **Do NOT** leave EMPTY GAPS — canvas 2048×2048 WAJIB 100% full, tambah filler kalo perlu
- **Do NOT** kasih checkmark cuma 3-4 — minimal 8, tambah dari default set kalo perlu
