---
name: venturo-poster
description: Generate professional 1024x1024px service package posters for Venturo (venturo.id) matching their brand aesthetic. Uses the "doodle-block" design style (solid teal blocks, dotted underlines, dashed-outline cards, left-aligned layout with illustration icons). Use when the user asks to create a Venturo service catalog poster, generate pricing package visual, produce tier marketing assets, or mentions "poster Venturo", "generate poster", "venturo catalog", "paket design". Always produces ONE poster per tier via Playwright rendering.
---

# Venturo Poster Generation

Generate branded 1024x1024px marketing posters for Venturo service packages. Each poster uses a **"doodle-block" design style** — reminiscent of editorial infographic layouts: solid color blocks, dotted dividers, dashed-outline cards, illustration icons, and left-aligned flowing content. Rendered as PNG via Playwright browser screenshot.

Reference file: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/packages_context.md` contains all content data, color palette, and design specs.
Style reference: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/design_style.png`

---

## Trigger Behavior

When loaded, **immediately begin the Q&A flow below**. Do NOT generate any poster until the user has answered the required questions. Never assume tier selections or content preferences.

---

## CRITICAL: ONE DESIGN = ONE TIER

**IMPORTANT RULE: Every poster must contain ONLY ONE tier.**

Each poster shows exactly ONE package tier with ALL its details in a single cohesive layout. There are NO multi-card grids or 2×2 layouts.

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

Ask if the user wants to modify any existing copy:

- Any specific wording changes?
- Different tagline or headline?
- Additional features or bullet points to add?
- Remove any existing items?

If the user says "no changes" or skips this step, use the **default content from the reference data below**.

---

## Design Language — The "Doodle-Block" Style

This is the KEY design principle for every poster. Inspired by editorial infographic layouts (see `design_style.png`), the style combines:

1. **Solid teal color blocks** — Full-width background panels in primary teal that define section zones
2. **Dotted/hand-drawn dividers** — Dashed lines, dotted horizontal rules instead of solid borders
3. **Dashed-outline cards** — Cards with dashed strokes (`border-style: dashed`) instead of solid borders
4. **Illustration icons** — Small illustrative icon drawings at the top-left of each section, like doodles
5. **Left-aligned content** — Most text content aligns left, creating clean reading rhythm
6. **Annotation elements** — Bubbles, arrows, callouts with hand-drawn feel around key information
7. **Varied line weights** — Mix of bold headings and light body text for hierarchy

This style replaces the previous "corporate card grid" look. The result is more playful, informative, and visually distinctive — while still being professional and on-brand for Venturo.

### Color Palette (from packages_context.md)

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Teal | `#006D79` | Brand primary, section blocks, accents |
| Light Teal | `#009BAD` | Secondary accents, gradients, highlights |
| Dark BG | `#0A1B1F` | Enterprise dark background |
| Dark Surface | `#142A2F` | Enterprise gradient mid-tone |
| Light BG | `#FFFFFF` | Starter / Growth poster background |
| Subtle BG | `#F4F8F8` | Off-white card backgrounds, content areas |
| Body Text | `#374151` | Primary description text |
| Muted Gray | `#9ca3af` | Footer, decorative elements |
| Green | `#10B981` | Hasil/results accent color |
| Green Mid | `#059669` | Hasil section label |

### Color Assignment Per Tier

| Tier | Background | Accent Blocks | Budget Pill |
|------|-----------|---------------|-------------|
| **Starter** | `#FFFFFF` white | Solid teal blocks (`#006D79`) | `#006D79` capsule, white text |
| **Growth** | `#FFFFFF` + dot grid (`#009BAD` 5% opacity) | Gradient teal blocks (`#006D79` → `#009BAD`) | Gradient capsule |
| **Enterprise** | Gradient `#0A1B1F` → `#112D35` | Solid light-teal blocks (`#009BAD`) | `#009BAD` capsule, dark text |

Capsule button shape: `border-radius: 22px` (fully rounded pill/capsule).
Checkmark circles: radius 14px filled circle, white checkmark inside.

---

### Canvas Setup

- Exact size: **1024×1024px**
- Render HTML/CSS inside a fixed container sized exactly 1024×1024px
- CSS `overflow: hidden` on root/body, no scrollbars visible
- Everything fits within the canvas — no content clipped outside bounds

### Typography

Always load fonts from Google Fonts. Use:

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
```

Font family: `'Inter', system-ui, -apple-system, sans-serif`

| Element | Size | Weight | Notes |
|---------|------|--------|-------|
| Section title | 112px | 900 | Massive, tight tracking -4px |
| Section label | 28px | 800 | Inside bold section block header |
| Feature / bullet text | 14px | 500 | Dash icon + text, ~1.4x line-height |
| Sub-label | 11px | 800 | Uppercase, letter-spacing 3px |
| Tagline / description | 17px | 400 | Under budget pill |
| Timeline badge | 11px | 700 | Duration pills on right side |
| Bottom grid title | 10px | 800 | Card headers |
| Bottom grid text | 13px | 500 | Card body |
| Footer | 11px | 400 | Muted color, subtle |

**CRITICAL — Text Wrapping:** All text elements must handle word boundaries properly. Long sentences should wrap gracefully onto multiple lines. Never let text overflow the container. Use CSS `word-wrap: break-word` and `overflow-wrap: break-word` on all text containers. No text should be clipped, cut off, or overlap.

---

## Layout Structure — Doodle-Block Vertical Flow

Every poster follows a **vertical stacking of solid teal blocks with dotted dividers**. Think: infographics / editorial layouts where each major section gets its own "colored panel" rather than floating cards.

### Zone 1: Header (~y=30 to ~y=130)

**MANDATORY: Use the Venturo logo image from `image.png` in this project.** Do NOT type out "VENTURO" as plain text. Render the actual logo.

- Inject the **Venturo logo image** (`image.png`) as the brand mark. Place it prominently in the top-left area of the poster.
  - Render it at approximately 36–48px height so it matches the poster scale
  - Scale proportionally — maintain aspect ratio, no distortion
  - Position at ~x=32, ~y=48 with comfortable padding from edges
  - Logo must be crisp and clearly visible
- Large **solid teal color block** across the top area (height ~100px, full width) — like the green "bullet journaling" header block in the reference
- White text inside the teal block: massive tier name (e.g., "Starter" at 112px weight 900, tight tracking -4px)
- Smaller subtitle text beneath tier name: "PAKET [TIER_NAME]"
- Bold dotted/dashed divider line at bottom of header block (use CSS dotted border-bottom)

### Zone 2: Budget & Tagline (~y=140 to ~y=210)

- Large **capsule-shaped pill** with budget range in white/contrast text
- `border-radius: 22` for fully rounded ends
- 17px tagline paragraph underneath ("Ideal untuk...") — wraps naturally into 2–3 lines
- Dotted underline beneath the entire budget section

### Zone 3: MASALAH — Solid Teal Block Section (~y=230 to ~y=410)

Full-width **teal color block** spanning almost entire poster width (~920px), with content inside it. This is the signature "doodle-block" element.

Layout INSIDE the block:
- **Top-left**: small illustration icon (exclamation mark, thought bubble, or problem-sphere doodle) drawn with SVG paths or CSS shapes
- **Section label**: "MASALAH" — uppercase, 11px, letter-spacing, in contrast color
- **Dotted divider line** below label (`border-bottom: 2px dotted`)
- List of problem items — each item on its own row with checkmark/dash icon on the left
- Each item wrapped properly — text can be 2–3 lines per item, no clipping
- Items left-aligned inside the block
- Full-width block: use `<section class="teal-block">` with background: #006D79 and white text

```css
.teal-block {
  background: #006D79;
  color: #fff;
  border-radius: 10px;
  padding: 28px 32px;
  margin: 16px 0;
}
/* For Enterprise (dark bg): invert colors */
.teal-block.enterprise {
  background: #009BAD;
  color: #0A1B1F;
}
```

### Zone 4: SOLUSI VENTURO — Dashed-Outline Card (~y=430 to ~y=600)

**Dashed-outline card** style — white card with dashed teal border, sitting on a light background band.

Layout:
- Section label: "SOLUSI VENTURO" — uppercase, accent color, letter-spacing
- **Illustration icon** at top-left (arrow up, gear, or solution bulb doodle)
- **Dotted divider** below label
- Solution items — checkmark icons, wrapped text, left-aligned
- Card borders: `border: 2px dashed #006D79` with `border-radius: 10px`
- Inner rows have dotted separators: `border-bottom: 1px dotted rgba(0,109,121,0.2)`

```css
.dashed-card {
  border: 2px dashed #006D79;
  border-radius: 12px;
  padding: 24px 28px;
  background: rgba(255,255,255,0.9);
}
```

### Zone 5: HASIL — Solid Teal Block Section (~y=620 to ~y=740)

Another full-width teal color block, similar structure to Masalah but with different accent (green).

- **Illustration icon**: star, lightning bolt, or celebration mark drawn with CSS/SVG
- Section label: "HASIL" — green accent color
- Dotted divider
- Result items — star/good outcome icons, wrapped text
- Full-width `teal-block` with green background: `background: #059669` for enterprise dark variant

### Zone 6: DEDICATED TEAM & TIMELINE (~y=760 to ~y=880)

**Dashed-outline card** with team & timeline info:
- Section label: "DEDICATED TEAM & TIMELINE"
- Team member list with numbered circular badges (one per row, left-aligned)
- Timeline phases — each on its own row
- Duration badges positioned on the right side of each phase row
- Dotted separators between items

### Zone 7: Cocok Untuk & Fase Bisnis (~y=895 to ~y=940)

Two smaller highlight boxes side by side (but narrow enough to not crowd):
- Left: "**COCOK UNTUK**" box — short descriptive text
- Right: "**FASE BISNIS**" box — short descriptive text
- Box style: dashed border, filled background, height ~40px each
- Gap ~16px between boxes

### Zone 8: Footer (~y=950 to ~y=970)

- Small dotted divider line above footer
- "© venturo.id" contact info in muted gray
- Positioned bottom-center or bottom-left

---

## Visual Elements — The Doodle-Block Details

### Illustration Icons (SVG Inline)

Each major section needs a small illustrative icon at the top-left corner. These should feel hand-drawn/doodle-like, not generic emojis or FontAwesome. Use inline SVG paths or pure-CSS shapes:

| Section | Icon Type | Implementation |
|---------|-----------|----------------|
| **Masalah** | Exclamation mark in a circle or worried face bubble | Inline SVG |
| **Solusi** | Arrow pointing up/right, gear, or lightbulb | Inline SVG |
| **Hasil** | Star, trophy, or checkmark burst | Inline SVG |
| **Team/Timeline** | Calendar icon, people cluster, or clock | Inline SVG |
| **Header** | Venturo logo image (mandatory, from `image.png`) | `<img src="data:image/png;base64,...">` |

### Dotted/Dashed Dividers Throughout

Replace ALL solid divider lines with dotted or dashed variants:
- Section-to-section separators: `border-bottom: 2px dotted #006D79`
- Item row separators inside cards: `border-bottom: 1px dotted rgba(0,109,121,0.2)`
- Bottom-of-header divider: same dotted style
- No solid lines allowed as separators (solid lines only for bold header/background blocks)

### Annotation Elements & Callouts

Add hand-drawn-feeling annotations for emphasis:
- Small **arrow pointers** pointing at key budget/timeline figures
- **Bubble callouts** with brief captions (e.g., "✓ Includes UAT", "★ Core features")
- **Hand-drawn style rectangles** around the budget pill (using `border-style: dashed` and slight `transform: rotate(-1deg)` for organic feel)
- **Underline annotations** with short labels floating near important content

### Checkmarks & Dashes

- Feature items use filled circle icons (radius 14px) with checkmark or dash symbols inside
- Circle fill: `#006D79` (teal) for Masalah/Solusi, `#10B981` (green) for Hasil, `#009BAD` for Enterprise
- White checkmark symbol (`✓`) centered in circle using flexbox
- Icon placed left-aligned, text flows next to it

---

## Background Design — Layered But Organized

Background should feel like an editorial spread — structured blocks, not random clutter.

### Mandatory Background Elements:

**1. Dot Grid Pattern** (required for all light-background tiers)
```css
.dot-grid {
  position: absolute; top: 0; left: 0;
  width: 100%; height: 100%;
  pointer-events: none;
  background-image: radial-gradient(circle, #006D79 1px, transparent 1px);
  background-size: 32px 32px;
  opacity: 0.06;
}
```

**2. Corner Decorations** (at least 2 corner accent clusters)

Use absolutely-positioned divs with:
- Concentric circles (CSS shapes, not images)
- Diagonal dot sequences (rows of small dots)
- Hand-drawn style brackets or corner marks

Place these at:
- Top-right corner: concentric rings + arc shapes
- Bottom-left corner: staggered dots forming diagonal pattern

**3. Gradient Overlays** (enterprise tier especially)

Add soft gradient washes:
- Radial gradient from brand color behind header block
- Fading gradient toward footer area

**4. Light Background Bands Between Sections**

Alternate between:
- White band (plain, where teal blocks sit)
- Very subtle teal-tinted band (`rgba(0, 109, 121, 0.03)`)

This creates a visual "page" rhythm — white sections broken by colored teal blocks.

**5. Floating Geometric Accents**

Between teal blocks, add thin decorative elements:
- Short diagonal lines (`div` with `height: 2px; transform: rotate(45deg)`)
- Small triangle markers
- Faded brand-colored circles (diameter 20–40px, opacity 0.08)

---

## Rendering Instructions

### File Format

- **Format:** PNG image, exactly 1024×1024 pixels
- **Method:** Render HTML/CSS via headless browser (Playwright), then capture screenshot
- **File naming:** `venturo-{tier}.png` (e.g., `venturo-starter.png`)
- **Save location:** Current working directory

### Playwright Tool Chain

Preferred sequence using MCP tools:

1. `mcp__playwright__browser_navigate(url="about:blank")` — start fresh page
2. `mcp__playwright__browser_resize(width=1024, height=1024)` — set viewport to poster dimensions
3. `mcp__playwright__browser_evaluate(function="(page) => { return page.setContent(htmlString); }")` — inject complete HTML document with inline CSS styling
4. `mcp__playwright__browser_wait_for(time=2)` — wait for Google Fonts to load and styles to settle
5. `mcp__playwright__browser_take_screenshot(type="png", scale="device", filename="venturo-{tier}.png")` — capture the poster

### HTML Construction Guidelines

Build a complete HTML document as a single string injected via `browser_evaluate`:

- Include `<link>` tag to load Inter font from Google Fonts
- Include `<style>` block with all CSS inline — no external CSS files
- Use **the Venturo logo image** embedded as base64 data URI in an `<img>` tag
- Layout: solid teal blocks + dashed-outline cards + dotted dividers alternating vertically
- Set `body { margin: 0; padding: 0; overflow: hidden; }`
- Container must be exactly 1024×1024px with `position: relative` and `overflow: hidden`
- Background dot grid as absolutely-positioned div with CSS radial-gradient pattern
- Each section uses its own structural element (`teal-block` for Masalah/Hasil, `dashed-card` for Solusi/Team)
- Text containers must have `word-wrap: break-word; overflow-wrap: break-word; white-space: normal;`

### Key CSS Properties for Text Safety

```css
.content-text {
  word-wrap: break-word;
  overflow-wrap: break-word;
  white-space: normal !important;
  max-width: calc(100% - 50px); /* leave room for icon */
}
.card-section {
  word-break: break-word;
  overflow: hidden;
}
```

---

## Example Visual Rhythm

Think of the poster like this (reading top to bottom):

```
┌──────────────────────────────────────┐
│  [VENTURO LOGO]                      │  ← Solid teal header block
│  STARTER                              │  ← 112px white text, dashed line at bottom
│  PAKET STARTER                        │
├──────────────────────────────────────┤  ← Dotted divider
│  ╔══════════════════╗               │
│  ║ Rp20Jt – Rp80Jt ║  ← Capsule pill  │
│  ╚══════════════════╝               │  ← Dotted underline
│  Ideal untuk UMKM...                │
├──────────────────────────────────────┤
│  ┌──────────────────────────────┐    │  ← SOLID TEAL BLOCK
│  │ ☹ Masalah: ...               │    │  ← White text, icon top-left
│  │ ● item 1                     │    │
│  │ ● item 2                     │    │  ← Dotted row separators
│  │ ● item 3                     │    │
│  └──────────────────────────────┘    │
├──────────────────────────────────────┤  ← Dotted divider
│  ┌──────────────────────────────┐    │  ← DASHED-OUTLINE CARD
│  │ 💡 Solusi: ...               │    │  ← Teal dashed border
│  │ ✓ item 1                     │    │  ← Dashed inner row lines
│  │ ✓ item 2                     │    │
│  └──────────────────────────────┘    │
├──────────────────────────────────────┤
│  ┌──────────────────────────────┐    │  ← SOLID GREEN BLOCK (Hasil)
│  │ ★ Hasil: ...                 │    │
│  │ ✓ item 1                     │    │
│  │ ✓ item 2                     │    │
│  └──────────────────────────────┘    │
├──────────────────────────────────────┤
│  ┌──────────────────────────────┐    │  ← DASHED CARD (Team)
│  │ 👥 Team & Timeline          │    │
│  │ ① BA  ② SE                  │    │
│  │ ▸ Phase 1: 1-2 minggu        │    │
│  └──────────────────────────────┘    │
└──────────────────────────────────────┘
```

---

## Content Mapping Reference

Use these default content blocks when the user accepts defaults:

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

- **Budget Proyek:** Rp20 Juta – Rp80 Juta
- **Dedicated Team:** 1 Business Analyst, 1 Senior Software Engineer
- **Timeline:** Requirement Analysis & System Design: 1 – 2 Minggu | System Development: 2 Minggu – 1 Bulan | Testing (SIT & UAT), Deployment & Go-Live: 1 – 2 Minggu
- **Cocok Untuk:** UMKM, Usaha Mikro, Perusahaan Kecil, Startup
- **Fase Bisnis:** Initial Digitalization — fondasi sistem operasional

#### Growth

- **Budget Proyek:** Rp80 Juta – Rp250 Juta
- **Dedicated Team:** 1 Business Analyst, 1 Senior Software Engineer, 1 UI/UX Designer, 1 QA Engineer
- **Timeline:** Requirement Analysis & System Design: 2 Minggu – 1 Bulan | System Development: 1 – 2 Bulan | Testing (SIT & UAT), Deployment & Go-Live: 2 Minggu – 1 Bulan
- **Cocok Untuk:** Perusahaan yang butuh custom system (Finance, HRIS, CRM, ERP, WMS, dll)
- **Fase Bisnis:** Operational Expansion — scaling sistem sesuai pertumbuhan

#### Enterprise

- **Budget Proyek:** Mulai dari Rp250 Juta
- **Dedicated Team:** 1 Business Analyst, 1 Senior Software Engineer, 1 Intermediate Software Engineer, 1 UI/UX Designer, 1 QA Engineer, 1 Penetration Tester
- **Timeline:** Requirement Analysis & System Design: 1 – 2 Bulan | System Development: 2 – 4 Bulan | Testing (SIT & UAT), Deployment & Go-Live: 2 Bulan
- **Cocok Untuk:** Perusahaan menengah hingga enterprise, transformasi digital menyeluruh
- **Fase Bisnis:** Enterprise Scale — big data, AI, multi-system integration

---

## Quality Checklist

### Content Accuracy
- [ ] Poster shows exactly ONE tier (not multiple tiers combined)
- [ ] Tier name matches what user requested
- [ ] Budget range is correct (no typos in numbers or currency format)
- [ ] Team members are listed correctly for the selected tier
- [ ] Timeline phases and durations match the reference data
- [ ] Bahasa Indonesia spelling is correct throughout
- [ ] No content sections were accidentally omitted

### Design Style (Doodle-Block)
- [ ] Header is a SOLID teal color block (not white/transparent)
- [ ] Masalah & Hasil sections use SOLID teal/green blocks
- [ ] Solusi & Team sections use DASHED-outline cards
- [ ] All dividers use DOT or DASH style (no solid lines as separators)
- [ ] Each section has an ILLUSTRATION ICON at top-left
- [ ] Annotation elements present (callouts, arrows, highlighted boxes)
- [ ] Budget pill has dashed/hand-drawn style rectangle around it
- [ ] Content is LEFT-ALIGNED throughout

### Visual Completeness
- [ ] Venturo logo image embedded in header (not plain text)
- [ ] Background has dot grid texture (for light-bg tiers)
- [ ] Budget capsule has strong color contrast with its text
- [ ] Checkmarks are consistently sized (14px radius circles) and colored per tier
- [ ] No text is clipped, cut off, or overlapping — all words wrap properly
- [ ] Footer "© venturo.id" is present and subtly styled
- [ ] No clipping — everything fits within 1024×1024

### Readability
- [ ] 112px section title is clearly visible at top
- [ ] Budget capsule text is legible at 28px
- [ ] Feature text at 14px wraps naturally — not squashed into one long line
- [ ] Sufficient contrast between text and background (WCAG AA minimum)
- [ ] Section labels stand out from body text

### Technical
- [ ] Screenshot is exactly 1024×1024 pixels
- [ ] Image is saved as PNG (not JPEG — PNG preserves sharp text edges better)
- [ ] Google Font Inter loads correctly (no fallback to system font)
- [ ] No scrollbar or overflow artifacts visible
- [ ] No text wrapping issues — all lines readable and complete

---

## When User Provides Custom Content

If the user supplies their own text (custom problems, solutions, taglines, budget figures, etc.):

1. Insert the custom text exactly as provided (do not rephrase unless asked)
2. If custom text is very long, allow text to wrap to multiple lines — don't truncate or clip
3. If custom text is very short for a section, pad with related items from the default set to maintain visual density
4. Always confirm before rendering if custom content significantly alters the expected layout

---

## After Poster Is Generated

1. Confirm completion — state how many poster files were generated and their names
2. Display the screenshot thumbnail so the user can see the result
3. Ask if they want:
   - Any revisions to content or design
   - Different tier combinations (still one poster per tier)
   - Additional sections or removed sections
   - Different messaging tone or wording
   - More/less annotation elements

---

## What NOT to Do

- **Do NOT** generate a poster without completing the Q&A flow first
- **Do NOT** put multiple tiers on one poster — ONE poster = ONE tier only
- **Do NOT** use corporate card-grid layouts (the old 2-column × 2-row style is REMOVED)
- **Do NOT** skip the solid teal block sections — this is the core "doodle-block" style
- **Do NOT** skip dashed-outline cards — these define the secondary section style
- **Do NOT** use solid lines as section dividers — always dotted or dashed
- **Do NOT** skip illustration icons — each section MUST have a doodle-style icon
- **Do NOT** right-align content — all main content is left-aligned
- **Do NOT** use the Venturo wordmark as plain text — always embed the logo image
- **Do NOT** let text overflow, clip, or overlap — all text must wrap properly
- **Do NOT** use colors outside the established Venturo palette (see Color Palette table above)
- **Do NOT** change font family — always use Inter
- **Do NOT** clip or cut off any content at the 1024×1024 boundary
- **Do NOT** render as JPEG — always PNG for crisp text
- **Do NOT** produce landscape or portrait orientations — always square 1024×1024
- **Do NOT** skip sections that the user confirmed
- **Do NOT** invent content that is not in the reference data unless the user explicitly requests it
