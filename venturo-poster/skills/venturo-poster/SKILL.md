---
name: venturo-poster
description: Generate WhatsApp Business catalog images for Venturo software packages (Starter/Growth/Enterprise). HTML/CSS designs rendered to PNG via Playwright with Pillow logo overlay. Triggers: catalog wa, katalog whatsapp, buat katalog, catalog venturo, poster venturo.
---

# Venturo Poster Skill

Generate **WhatsApp Business catalog images** for Venturo software packages (Starter/Growth/Enterprise).

**Engine:** HTML/CSS templates rendered by Playwright → PNG 1400x1024
**Overlay:** Pillow adds Venturo logo on right-side white space automatically

## Integrated Design Skills

### canvas-design Principles
- **Visual-first communication**: Every design is 90% visual, 10% essential text. Text should be sparse and integrated as a visual element, never lengthy paragraphs.
- **Spatial expression**: Ideas communicate through space, form, color, composition — not explanation. Use generous breathing room.
- **Composition & balance**: Massive color blocks, sculptural typography, dramatic negative space. Everything placed with precision.
- **Expert craftsmanship**: Composition must look meticulously crafted — spacing, alignment, color choices, and typography are pixel-perfect. Nothing overlaps. Every detail refined.
- **Typography as art**: Bold condensed sans-serif headings can be treated as visual gestures — large single words, tiny labels. Fonts from `assets/canvas-fonts/` can be used when Playwright supports local fonts.

### theme-factory Integration
Use themes from `themes/` directory to generate variant designs per tier. Themes define cohesive palettes + font pairings that maintain consistency across all catalog pieces.

**Pre-matched themes per tier:**
| Tier | Recommended Theme |
|------|-------------------|
| Starter | modern-minimalist, arctic-frost |
| Growth | tech-innovation, ocean-depths |
| Enterprise | midnight-galaxy, tech-innovation |

When user wants "alternative designs" or "more options", swap to different themes or create custom ones.

### brand-guidelines
Apply consistent brand colors, typography hierarchy, and spacing rules. Primary teal `#006D79` always dominates. Brand feels professional and trustworthy.

## Design System (Venturo Brand)

| Element | Spec |
|---------|------|
| **Primary** | `#006D79` (teal gelap) |
| **Primary Light** | `#009BAD` (teal terang) |
| **Dark** | `#202020` (Enterprise dark mode bg) |
| **Light BG** | `#F6F8F8` (abu sangat muda) |
| **Heading** | `#292929` |
| **Body** | `#4B5563` |
| **Background** | `#FFFFFF` (putih) |
| **Font style** | Bold condensed sans-serif headings, clean sans-serif body |

## Output Specs

- **Size:** 1400x1024 pixels
- **Format:** PNG
- **Style:** WhatsApp Business catalog — clean, professional, modern
- **Right-side space:** Area kosong putih di KANAN (~490px) untuk overlay Pillow (logo Venturo auto-added, QR/text/manual)
- **Language:** Bahasa Indonesia

## Package Tiers

| Tier | Budget | Ideal for | Team | Timeline |
|------|--------|-----------|------|----------|
| **Starter** | Rp20M – Rp80M | UMKM, startup, website & mobile app sederhana | 1 BA + 1 Sr. Eng | 1–4 Minggu |
| **Growth** | Rp80M – Rp250M | Finance, HRIS, CRM, ERP, Inventory, WMS, Logistics, Sales, Production, Asset Management | 1 BA + 1 Sr. Eng + 1 UI/UX + 1 QA | 1–4.5 Bulan |
| **Enterprise** | Mulai Rp250M | AI, Big Data, cybersecurity, integrasi lintas sistem | 1 BA + 1 Sr. Eng + 1 Mid Eng + 1 UI/UX + 1 QA + 1 Pen Test | 2–8 Bulan |

## Style Per Tier

| Tier | Theme | Visual Style |
|------|-------|--------------|
| **Starter** | Light teal | Clean, minimalist, startup vibe, light gradient, approachable |
| **Growth** | Corporate teal | Professional, multi-device feel, data-rich but clean |
| **Enterprise** | Dark mode neon teal | High-tech, cybertech aesthetic, glowing accents, holographic feel |

## Workflow

### Phase 1: Interview User

Ask 3-5 questions in **Bahasa Indonesia**:

1. **Tier** — Starter / Growth / Enterprise
2. **Overlay Content** — Mau tambahin QR code atau teks custom di space kanan?
3. **Design Preferences** — Ada preferensi tambahan? (opsional)

### Phase 2: Show Preview + Theme Options

Display the tier summary + what the design will look like. Offer theme alternatives:
> "Design untuk **PAKET STARTER** — tema light teal, minimalis, cocok untuk UMKM.
> Alternatif tema tersedia: Modern Minimalist (grayscale), Arctic Frost (biru dingin).
> Output 1400x1024 PNG, logo Venturo otomatis di kanan bawah. Lanjut?"

To generate a different theme variant, pass `theme` parameter:
```
generate_catalog(tier="starter", theme="modern-minimalist")
```

If no theme specified, use default tier design. If theme name doesn't match built-in, create a custom one on-the-fly using theme-factory principles.

### Phase 3: Generate

Call MCP tool with optional theme:
```
generate_catalog(tier="starter")
# or with a theme variant
generate_catalog(tier="growth", theme="tech-innovation")
```

### Phase 4: Deliver

> ✔ Katalog berhasil! Tersimpan di `venturo-poster/output/venturo_{tier}_{timestamp}.png`
> Ukuran: 1400x1024 — logo Venturo sudah di-overlay di kanan bawah. Space kanan masih ada area kosong (~35%) jika perlu tambah QR code atau teks tambahan.

## Critical Rules

- **Interview FIRST** — tanya tier dan preferensi overlay sebelum generate.
- **No AI image generation** — semua design pakai HTML/CSS template, bukan generative AI.
- **Area KANAN KOSONG** — 35% kanan selalu putih, logo overlay otomatis via Pillow.
- **Bahasa Indonesia** untuk semua teks di desain dan komunikasi.
- Logo overlay otomatis dari `assets/image_1c155d.png` posisi kanan bawah.
- Jika user minta QR code atau teks manual di space kanan, bilang user bisa tambah sendiri setelah gambar jadi.

## Theme Files

| Path | Purpose |
|------|---------|
| `themes/starter/*.md` | Starter tier theme variants (arctic-frost, modern-minimalist) |
| `themes/growth/*.md` | Growth tier theme variants (tech-innovation, ocean-depths) |
| `themes/enterprise/*.md` | Enterprise tier theme variants (midnight-galaxy, tech-innovation) |
| `themes/custom/*.md` | Custom themes generated on-the-fly |

## File Reference

| Path | Purpose |
|------|---------|
| `plugin.json` | Plugin manifest |
| `assets/image_1c155d.png` | Official Venturo logo |
| `mcp-playwright/server.py` | MCP server — HTML/CSS render → PNG |
| `mcp-playwright/requirements.txt` | Python deps (playwright, pillow, mcp) |
| `templates/packages_context.md` | Full tier content reference (sales copy, visual mapping) |
| `output/` | Generated catalog images (1400x1024) |
