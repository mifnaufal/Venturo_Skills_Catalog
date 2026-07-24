---
name: venturo-poster
description: Generate WhatsApp Business catalog images for Venturo software packages (Starter/Growth/Enterprise). HTML/CSS designs rendered to 1024x1024 PNG via Playwright with inline SVG logo. Triggers: catalog wa, katalog whatsapp, buat katalog, catalog venturo, poster venturo.
---

# Venturo Poster Skill

Generate **WhatsApp Business catalog images** for Venturo software packages (Starter/Growth/Enterprise).

**Engine:** HTML/CSS templates rendered by Playwright → PNG 1024x1024 square
**Logo:** Inline SVG (pixel-perfect, no blur)

## Design System (Venturo Brand)

All templates follow a unified design language matching venturo.id:

| Element | Spec |
|---------|------|
| **Primary** | `#006D79` (teal gelap) |
| **Primary Light** | `#009BAD` (teal terang) |
| **Dark BG** | `#0A1B1F` → `#112D35` (Enterprise gradient) |
| **Light BG** | `#FFFFFF` (clean white) |
| **Dot Grid** | Subtle background texture (teal at low opacity) |
| **Font** | Inter (Google Fonts), weight 900 for headings |
| **Canvas** | 1024×1024px square |

### Layout Pattern (all tiers)
1. **Top:** Logo SVG + "PAKET [TIER]" (massive 112px bold) + budget pill + tagline
2. **Body:** Section label + feature list with solid teal checkmarks
3. **Bottom Grid:** Left = team dedicated + timeline; Right = 2 highlight cards (cocok untuk + fase bisnis)
4. **Footer:** © venturo.id bottom-left

## Output Specs

- **Size:** 1024×1024 pixels (square 1:1)
- **Format:** PNG
- **Style:** Clean, professional, venturo.id branding, dense layout with dot grid background
- **Language:** Bahasa Indonesia

## Package Tiers

| Tier | Budget | Ideal for | Team | Timeline |
|------|--------|-----------|------|----------|
| **Starter** | Rp20M – Rp80M | UMKM, startup, website & mobile app | 1 BA + 1 Sr. Eng | 1–4 Minggu |
| **Growth** | Rp80M – Rp250M | Finance, HRIS, CRM, ERP, Inventory, WMS, Logistics | 1 BA + 1 Sr. Eng + 1 UI/UX + 1 QA | 1–4.5 Bulan |
| **Enterprise** | Mulai Rp250M | AI, Big Data, cybersecurity, integrasi lintas sistem | 1 BA + 1 Sr. Eng + 1 Mid Eng + 1 UI/UX + 1 QA + 1 Pen Test | 2–8 Bulan |

## Style Per Tier

| Tier | Background | Accent | Vibe |
|------|-----------|--------|------|
| **Starter** | White + subtle dot grid | Teal `#006D79` | Clean, approachable, UMKM-friendly |
| **Growth** | White + dot grid | Teal gradient | Corporate, data-rich, professional |
| **Enterprise** | Dark teal gradient | Neon teal glow | High-tech, cybertech, holographic |

## Workflow

### Phase 1: Interview User

Ask 2-3 questions in **Bahasa Indonesia**:

1. **Tier** — Starter / Growth / Enterprise
2. **Design Preferences** — Ada preferensi khusus? (opsional)

### Phase 2: Show Preview

Display the tier summary + what the design will look like:
> "Design untuk **PAKET STARTER** — tema clean white dengan dot grid, cocok untuk UMKM.
> 1024x1024 PNG. Lanjut?"

### Phase 3: Generate

Call MCP tool:
```
generate_catalog(tier="starter")
```

### Phase 4: Deliver

> ✔ Katalog berhasil! Tersimpan di `venturo-poster/output/venturo_{tier}_{timestamp}.png`
> Ukuran: 1024x1024 — logo Venturo sudah di-render sebagai inline SVG (sharp, tidak blur).

## Critical Rules

- **Interview FIRST** — tanya tier sebelum generate.
- **No AI image generation** — semua design pakai HTML/CSS template, bukan generative AI.
- **Square 1024x1024** — canvas selalu 1:1.
- **Inline SVG logo** — tidak pernah pakai Pillow overlay (no blur).
- **Bahasa Indonesia** untuk semua teks di desain dan komunikasi.
- **Brand colors** — selalu gunakan teal `#006D79` sebagai warna utama.

## File Reference

| Path | Purpose |
|------|---------|
| `assets/image_1c155d.png` | Official Venturo logo (fallback) |
| `mcp-playwright/server.py` | MCP server — HTML/CSS render → PNG |
| `mcp-playwright/requirements.txt` | Python deps (playwright, pillow, mcp) |
| `templates/packages_context.md` | Full tier content reference |
| `output/` | Generated catalog images (1024x1024) |
