---
name: venturo-poster
description: Generate WhatsApp Business catalog images for Venturo's software development service packages. Triggers on "catalog wa", "katalog whatsapp", "buat katalog", "catalog venturo", "Dreamina catalog". Enforces an interactive Art Director interview before any image generation.
---

# Venturo WhatsApp Business Catalog Generator

Generate **WhatsApp Business catalog images** for Venturo — an Indonesian software development company — using **Dreamina AI** via Playwright (manual login).

**Engine:** Dreamina AI (online, via Playwright browser automation)

## Design System (Venturo Brand)

| Element | Spec |
|---------|------|
| **Primary** | `#006D79` (teal) |
| **Primary Light** | `#009BAD` |
| **Dark** | `#202020` |
| **Light BG** | `#F6F8F8` |
| **Heading** | `#292929` |
| **Body** | `#4B5563` |
| **Background** | `#FFFFFF` |
| **Font style** | Bold condensed sans-serif headings, clean body text |

## Output Specs

- **Size:** Square 1:1 (Dreamina default aspect ratio)
- **Format:** PNG
- **Style:** WhatsApp Business catalog — clean, professional, modern, minimal
- **Language:** Bahasa Indonesia

## Package Tiers

| Tier | Budget | Ideal for |
|------|--------|-----------|
| **Starter** | Rp20 Juta – Rp80 Juta | UMKM, startup, website & mobile app sederhana |
| **Growth** | Rp80 Juta – Rp250 Juta | Finance, HRIS, CRM, ERP, Inventory, WMS |
| **Enterprise** | Mulai Rp250 Juta | AI, Big Data, cybersecurity, integrasi lintas sistem |

## Workflow (mandatory — follow in order)

### Phase 1: Art Director Interview

**Do NOT generate anything immediately.** Ask 3-5 targeted questions:

1. **Package Tier** — Starter (Rp20M-80M), Growth (Rp80M-250M), or Enterprise (Rp250M+)
2. **Design Preferences** — Any specific visual style, color emphasis, or layout they want
3. **Logo Instructions** — Where should the Venturo logo appear? (optional, AI places naturally)
4. **Custom Content** — Any specific text, stats, or info to highlight beyond the defaults

Frame questions in **Bahasa Indonesia**. Show you understand their business context.

### Phase 2: Context Enrichment

Read `templates/packages_context.md` to enrich the AI prompt with Venturo-specific data:

| Tier | Themes to emphasize |
|------|-------------------|
| Starter | Clean storefronts, modern mobile UIs, 2-person team, minimalist |
| Growth | ERP/CRM/HRIS dashboards, multi-device, 4-person team |
| Enterprise | Data centers, AI/Big Data, cybersecurity, 6-person team + pentest |

### Phase 3: Preview Spec (NO GENERATION)

Show the prompt that will be sent to Dreamina, plus which reference images will be uploaded:

1. The Venturo logo (`assets/image_1c155d.png`) — uploaded as reference, AI composites it naturally
2. The prompt text (auto-generated from tier + packages_context.md)
3. **Ask for approval:** "Apakah spec ini sesuai? Saya akan generate via Dreamina dengan referensi logo Venturo. Lanjut?"

### Phase 4: User Approval

Wait for explicit "lanjut" / "yes" / "setuju" before proceeding.

### Phase 5: Generation via Dreamina

```bash
python3 venturo-poster/scripts/generate_base.py --tier starter
```
*(Run from the directory where you cloned `Venturo_Skills_Catalog/`)*

The script:
1. Launches Chromium with `headless=false` — browser window appears
2. Navigates to Dreamina — **user logs in manually**
3. After login, navigates to AI image generation page
4. Uploads `assets/image_1c155d.png` as reference image (auto, with fallback to manual)
5. Fills the prompt text (auto, with fallback to manual)
6. Waits for generation to complete
7. Saves screenshot as `dreamina_<tier>.png`

**Key flags:**
| Flag | Description |
|------|-------------|
| `--tier starter|growth|enterprise|all` | Which tier(s) to generate |
| `--prompt "custom"` | Override auto-generated prompt |
| `--prompt-file path.txt` | Read p
]\=======================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================




























































































































































































































































































































































































































































































=rompt from file |
| `--timeout 180000` | Max wait in ms (default 3 min) |
| `--no-logo` | Skip logo reference upload |
| `--output path.png` | Custom output path |

### Phase 6: Delivery

```
✔ Katalog berhasil dibuat! Tersimpan di:
  dreamina_starter.png

  Resolusi: 1:1 square (Dreamina)
  Engine: Dreamina AI (Playwright manual login)
  Logo: AI-composited from reference image
```

## Critical Rules

- **Always** run the interview phase first. Never skip to generation.
- **Never generate immediately after interview.** Show preview spec and get approval first.
- **Do NOT generate or composite the logo separately.** The Venturo logo is uploaded as a reference image to Dreamina and AI composites it naturally into the design.
- **Do NOT use Pillow or other local rendering.** The Dreamina AI engine handles ALL visual generation.
- **Always** include the Venturo logo reference in the prompt instructions.
- **Always use Bahasa Indonesia** untuk konten catalog.
- **Manual login required** — the user must log into Dreamina manually in the visible browser.

## File Reference

| Path | Purpose |
|------|---------|
| `plugin.json` | Plugin manifest |
| `skills/venturo-poster.md` | This skill definition |
| `assets/image_1c155d.png` | Official Venturo logo (uploaded as reference to Dreamina) |
| `scripts/generate_base.py` | Dreamina AI generation via Playwright (manual login + logo reference upload) |
| `templates/packages_context.md` | Venturo service tier reference with sales copy |
| `output/` | Generated catalog images |
