---
name: venturo-poster
description: Generate WhatsApp Business catalog images for Venturo's software development service packages. Triggers on "catalog wa", "katalog whatsapp", "buat katalog", "catalog venturo". Enforces an interactive Art Director interview before any image generation.
---

# Venturo WhatsApp Business Catalog Generator

Generate **WhatsApp Business catalog images** for Venturo — an Indonesian software development company — using **Qwen-Image-2.0-Pro** via ImageRouter API.

**Engine:** Qwen-Image-2.0-Pro (via ImageRouter API — imagerouter.io)

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

- **Size:** 1024x1024 (square 1:1)
- **Format:** PNG
- **Style:** WhatsApp Business catalog — clean, professional, modern, minimal
- **Language:** Bahasa Indonesia

## Package Tiers

| Tier | Budget | Ideal for |
|------|--------|-----------|
| **Starter** | Rp20 Juta – Rp80 Juta | UMKM, startup, website & mobile app sederhana |
| **Growth** | Rp80 Juta – Rp250 Juta | Finance, HRIS, CRM, ERP, Inventory, WMS |
| **Enterprise** | Mulai Rp250 Juta | AI, Big Data, cybersecurity, integrasi lintas sistem |

## Prerequisites (AI Agent)

Sebelum memulai generation, pastikan:

1. **MCP server `venturo-poster-playwright` sudah terdaftar** di Antigravity config:
   ```json
   {
     "mcpServers": {
       "venturo-poster-playwright": {
         "command": "python3",
         "args": ["<plugin_path>/mcp-playwright/server.py"],
         "env": {
           "IMAGE_ROUTER_API_KEY": "ir_xxx..."
         }
       }
     }
   }
   ```
2. **Dependencies sudah terinstall** (`pip install -r <plugin_path>/mcp-playwright/requirements.txt`)
3. **API key ImageRouter sudah diisi** di environment variable `IMAGE_ROUTER_API_KEY`

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `generate_catalog(prompt, tier)` | Generate catalog image via Qwen-Image-2.0-Pro. Sends prompt + Venturo logo (as reference) to ImageRouter API, saves result PNG to output/. |
| `check_balance()` | Check remaining ImageRouter credit balance. |

## Workflow (mandatory — follow in order)

### Phase 1: Art Director Interview

**Do NOT generate anything immediately.** Ask 3-5 targeted questions:

1. **Package Tier** — Starter (Rp20M-80M), Growth (Rp80M-250M), or Enterprise (Rp250M+)
2. **Design Preferences** — Any specific visual style, color emphasis, or layout they want
3. **Logo Instructions** — Where should the Venturo logo appear? (optional, AI places naturally)
4. **Custom Content** — Any specific text, stats, or info to highlight beyond the defaults

Frame questions in **Bahasa Indonesia**. Show you understand their business context.

### Phase 2: Build Detailed Prompt

Read `templates/packages_context.md` for tier-specific themes and visual mapping.

Generate a **detail-rich prompt in English** (Qwen renders text better in English). The prompt MUST follow this structure:

```
WhatsApp Business catalog image, square 1:1, {tier} package.

TITLE: "{TIER}" — VENTURO Software House Malang
BUDGET: {budget}

MAIN VISUAL:
{dari templates/packages_context.md — visual theme sesuai tier}

COMPOSITION:
- Top area: clean space for "VENTURO" logo + title
- Center: {main focal element sesuai tier}
- Bottom: budget info + tagline

TEXT ON IMAGE (minimal, English):
- "{TIER}" in bold modern font
- "VENTURO"
- "Mulai {budget}"

COLOR PALETTE:
- Background: {dark/light sesuai tier}
- Accent primary: #006D79 (teal)
- Accent secondary: #009BAD (cyan)
- Text: white (on dark) / dark (on light)

MOOD: {mood sesuai tier}

STYLE KEYWORDS: {dari templates/packages_context.md}

DO NOT include: people faces, long paragraphs, busy backgrounds, cartoonish elements.
```

**Wajib incorporate hasil interview user:**
- If user specified color preferences → tambahkan ke color palette
- If user wanted specific layout/placement → tambahkan ke composition
- If user has custom text/stats → tambahkan ke TEXT ON IMAGE

### Phase 3: Preview Spec (NO GENERATION)

Tampilkan **final prompt** yang akan dikirim (English, visual-focused), plus reference images:

1. **Final prompt** (tampilkan LENGKAP, jangan dipotong)
2. The Venturo logo (`assets/image_1c155d.png`) — dikirim sebagai reference image ke API, AI composites naturally
3. **Ask for approval:** "Apakah spec ini sesuai? Saya akan generate via ImageRouter API dengan model Qwen-Image-2.0-Pro dan referensi logo Venturo. Lanjut?"

### Phase 4: User Approval

Wait for explicit "lanjut" / "yes" / "setuju" before proceeding.

### Phase 5: Generation via ImageRouter API

Panggil MCP tools secara berurutan:

**Step 1 — Generate:**
```
generate_catalog(prompt="{full prompt dari Phase 2/3 — LENGKAP, jangan dipotong}", tier="{starter|growth|enterprise}")
```

Tool ini akan:
1. Load logo Venturo as data URI
2. Kirim POST request ke ImageRouter API dengan model `qwen/qwen-image-2-pro`
3. Download hasil gambar ke `venturo-poster/output/`
4. Return path file

Jika gagal:
- "IMAGE_ROUTER_API_KEY not set" → "API key belum diatur. Set environment variable IMAGE_ROUTER_API_KEY."
- Error API lain → tampilkan detail error dari respons

> **CRITICAL:** Kirim prompt final (English, visual-focused) via `generate_catalog()`. Jangan dipotong/diringkas. Pastikan semua elemen (Main Visual, Composition, Text, Color, Mood, preferensi user) masuk semua.

### Phase 6: Delivery

```
✔ Katalog berhasil dibuat! Tersimpan di:
  venturo-poster/output/venturo_{tier}_{timestamp}.png

  Resolusi: 1024x1024 (1:1)
  Engine: Qwen-Image-2.0-Pro (via ImageRouter API)
  Logo: AI-composited from reference image
```

## Critical Rules

- **Always** run the interview phase first. Never skip to generation.
- **Never generate immediately after interview.** Show preview spec and get approval first.
- **Do NOT generate or composite the logo separately.** The Venturo logo is sent as a reference image to the API and AI composites it naturally into the design.
- **Do NOT use Pillow or other local rendering.** The Qwen-Image model handles ALL visual generation.
- **Always** include the Venturo logo reference in the prompt instructions.
- **Gunakan English untuk prompt** (Qwen render teks lebih baik dalam English), tapi konten katalog tetap Bahasa Indonesia.
- **Prompt harus visual-focused, bukan business copy.** Fokus pada deskripsi visual, komposisi, warna, dan mood. Jangan menyertakan blok teks panjang (Masalah/Solusi/Hasil) — itu bukan untuk image prompt. Incorporate preferensi user ke bagian composition/color/mood.
- **Jika MCP tool gagal**, tampilkan error detailnya ke user dan tawarkan untuk coba lagi.

## MCP Server Configuration

Tambahkan MCP server ini ke Antigravity config (`~/.gemini/config/antigravity.json` atau sesuai setup):

```json
{
  "mcpServers": {
    "venturo-poster-playwright": {
      "command": "python3",
      "args": ["<absolute_path>/mcp-playwright/server.py"],
      "env": {
        "IMAGE_ROUTER_API_KEY": "<your_api_key>"
      }
    }
  }
}
```

Ganti `<absolute_path>` dengan path lengkap ke `venturo-poster/mcp-playwright/server.py`.
Ganti `<your_api_key>` dengan ImageRouter API key (dapatkan di https://imagerouter.io/api-keys).

## File Reference

| Path | Purpose |
|------|---------|
| `plugin.json` | Plugin manifest |
| `skills/venturo-poster/SKILL.md` | This skill definition |
| `assets/image_1c155d.png` | Official Venturo logo (sent as reference to ImageRouter API) |
| `mcp-playwright/server.py` | ImageRouter MCP server — API-based image generation |
| `mcp-playwright/requirements.txt` | Python dependencies for MCP server |
| `templates/packages_context.md` | Venturo service tier reference with sales copy |
| `output/` | Generated catalog images |
