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

### Phase 2: Build Detailed Prompt

Read `templates/packages_context.md` and `scripts/generate_base.py` (see `build_prompt()` function) to understand the prompt structure.

Generate a **long, detailed Dreamina prompt** in Bahasa Indonesia. The prompt MUST follow this structure and include ALL sections:

```
Buat gambar katalog WhatsApp Business untuk paket {TIER}.

VENTURO — Software House Malang
Paket: {tier}
Budget: {budget}
Ideal untuk: {target_audience}
Tim: {team_composition}

MASALAH YANG DISELESAIKAN:
- (dari templates/packages_context.md — sesuaikan dengan konteks tier)

SOLUSI:
- (dari templates/packages_context.md — sesuaikan dengan konteks tier)

HASIL:
- (dari templates/packages_context.md — sesuaikan dengan konteks tier)

VISUAL THEMES:
- (dari templates/packages_context.md — pilih yang sesuai tier)

STYLE KEYWORDS: (dari templates/packages_context.md)

BRAND & DESAIN:
- Warna Primer: #006D79 (teal)
- Warna Sekunder: #009BAD
(include color palette lengkap)

DESIGN RULES:
- WhatsApp Business catalog image, square 1:1
- Clean, professional, modern, minimal
- Bahasa Indonesia
- Logo Venturo dari referensi yang diupload
- (include user preferences dari interview)
```

**Wajib incorporate hasil interview user:**
- If user specified color preferences → tambahkan ke design rules
- If user wanted specific layout/placement → tambahkan ke visual themes
- If user has custom text/stats → sisipkan di konten

### Phase 3: Preview Spec (NO GENERATION)

Tampilkan **full prompt** yang akan dikirim ke Dreamina, plus reference images:

1. **Full prompt** (tampilkan LENGKAP, jangan dipotong)
2. The Venturo logo (`assets/image_1c155d.png`) — uploaded as reference, AI composites it naturally
3. **Ask for approval:** "Apakah spec ini sesuai? Saya akan generate via Dreamina dengan referensi logo Venturo. Lanjut?"

### Phase 4: User Approval

Wait for explicit "lanjut" / "yes" / "setuju" before proceeding.

### Phase 5: Generation via Dreamina

Write the full prompt (from Phase 2/3) to a temporary file, then run:

```bash
cat > /tmp/venturo_prompt_starter.txt << 'PROMPT_EOF'
{full prompt dari Phase 2 — jangan dipotong, tulis LENGKAP}
PROMPT_EOF

python3 venturo-poster/scripts/generate_base.py \
  --tier starter \
  --prompt-file /tmp/venturo_prompt_starter.txt
```
*(Run from `Venturo_Skills_Catalog/` directory)*

The script:
1. Prompts for Dreamina email & password in terminal
2. Launches Chromium with `headless=false` — browser window appears
3. Navigates to Dreamina — **auto-fills email & password**, clicks Sign in
4. If auto-login fails, falls back to manual login
5. After login, navigates to AI image generation page
6. Uploads `assets/image_1c155d.png` as reference image (auto, with fallback to manual)
7. Fills the prompt text from the file (auto, with fallback to manual)
8. Waits for generation to complete
9. Saves screenshot as `output/dreamina_<tier>.png`

> **CRITICAL:** Kirim prompt LENGKAP ke Dreamina. Jangan dipotong/diringkas. Semua section (Masalah, Solusi, Hasil, Visual Themes, Brand, Design Rules, preferensi user) harus masuk semua ke prompt.

### Phase 6: Delivery

```
✔ Katalog berhasil dibuat! Tersimpan di:
  venturo-poster/output/dreamina_starter.png

  Resolusi: 1:1 square (Dreamina)
  Engine: Dreamina AI (Playwright auto-login)
  Logo: AI-composited from reference image
```

## Critical Rules

- **Always** run the interview phase first. Never skip to generation.
- **Never generate immediately after interview.** Show preview spec and get approval first.
- **Do NOT generate or composite the logo separately.** The Venturo logo is uploaded as a reference image to Dreamina and AI composites it naturally into the design.
- **Do NOT use Pillow or other local rendering.** The Dreamina AI engine handles ALL visual generation.
- **Always** include the Venturo logo reference in the prompt instructions.
- **Always use Bahasa Indonesia** untuk konten catalog.
- **Auto-login** — script prompts for email & password and fills the Dreamina login form. Falls back to manual if auto-login fails.
- **Use `--manual-login` flag** to skip auto-login and log in manually.
- **Prompt harus LENGKAP & DETAIL.** Jangan pernah menyingkat atau meringkas prompt. Semua section (Masalah, Solusi, Hasil, Visual Themes, Brand, Design Rules) + preferensi user harus masuk semua. Jika user request spesifik (warna, layout, teks), incorporate ke dalam prompt.

## File Reference

| Path | Purpose |
|------|---------|
| `plugin.json` | Plugin manifest |
| `skills/venturo-poster/SKILL.md` | This skill definition |
| `assets/image_1c155d.png` | Official Venturo logo (uploaded as reference to Dreamina) |
| `scripts/generate_base.py` | Dreamina AI generation via Playwright (manual login + logo reference upload) |
| `templates/packages_context.md` | Venturo service tier reference with sales copy |
| `output/` | Generated catalog images |
