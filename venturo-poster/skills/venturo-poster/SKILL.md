---
name: venturo-poster
description: Generate WhatsApp Business catalog images for Venturo's software development service packages. Triggers on "catalog wa", "katalog whatsapp", "buat katalog", "catalog venturo". Enforces an interactive Art Director interview before any image generation.
---

# Venturo WhatsApp Business Catalog Generator

Generate **WhatsApp Business catalog images** for Venturo — an Indonesian software development company — using **Qwen-Image-2.0-Pro** via maxrouter.io Chat Completions API.

**Engine:** Qwen-Image-2.0-Pro (via maxrouter.io — OpenAI-compatible Chat Completions)

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

1. **MCP server sudah terdaftar** — pilih sesuai platform:
   - **Claude Code**: `.mcp.json` (project scope, sudah include di repo) atau `claude mcp add --scope user venturo-poster -- python3 venturo-poster/mcp-playwright/server.py`
   - **OpenCode**: `.mcp.json` (project scope, auto-load) atau via `opencode.json`
   - **Antigravity**: Plugin auto-register via `mcp_config.json` di `~/.gemini/config/plugins/venturo-poster/`
2. **Dependencies sudah terinstall** (`pip install -r venturo-poster/mcp-playwright/requirements.txt`)
3. **API key maxrouter.io sudah diisi** di `.env`, environment variable `IMAGE_ROUTER_API_KEY`, atau MCP config

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `generate_catalog(prompt, tier, image_size, aspect_ratio)` | Generate catalog image via Qwen-Image-2.0-Pro. Sends prompt + Venturo logo (as reference) to maxrouter.io Chat Completions API, saves result PNG to output/. |
| `check_balance()` | Verify API key and connection to maxrouter.io. |

## Workflow (mandatory — follow in order)

### Phase 1: Art Director Interview

**Do NOT generate anything immediately.** Ask 3-5 targeted questions:

1. **Package Tier** — Starter (Rp20M-80M), Growth (Rp80M-250M), or Enterprise (Rp250M+)
2. **Design Preferences** — Any specific visual style, color emphasis, or layout they want
3. **Logo Instructions** — Where should the Venturo logo appear? (optional, AI places naturally)
4. **Custom Content** — Any specific text, stats, or info to highlight beyond the defaults

Frame questions in **Bahasa Indonesia**. Show you understand their business context.

### Phase 2: Build Detailed Prompt

Read `templates/packages_context.md` for tier-specific themes and sales copy.

Generate a **long, detailed prompt** in **Bahasa Indonesia** untuk dikirim ke Qwen-Image-2.0-Pro via maxrouter.io API. The prompt MUST follow this structure and include ALL sections:

```
Buat gambar katalog WhatsApp Business untuk paket {TIER}.
Ukuran: square 1:1 (khusus WhatsApp Business catalog).

VENTURO — Software House Malang
Paket: {tier}
Budget: {budget}
Ideal untuk: {target_audience}
Tim: {team_composition}

MASALAH YANG DISELESAIKAN (Masalah Terbesar di Indonesia):
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
- Dark: #202020
- Light BG: #F6F8F8
- Heading: #292929
- Body Text: #4B5563
- Background: #FFFFFF

DESIGN RULES:
- WhatsApp Business catalog image, square 1:1
- Clean, professional, modern, minimal
- Bahasa Indonesia
- Gunakan style "Default Venturo" yang profesional dan korporat.
- Logo Venturo diambil dari referensi yang diupload, silakan AI menempatkan posisinya secara natural agar terlihat elegan dan menyatu dengan desain.
- (include user preferences dari interview)
```

**Wajib incorporate hasil interview user:**
- If user specified color preferences → tambahkan ke design rules
- If user wanted specific layout/placement → tambahkan ke visual themes
- If user has custom text/stats → sisipkan di konten

### Phase 3: Preview Spec (NO GENERATION)

Tampilkan **full prompt** yang akan dikirim ke API, plus reference images:

1. **Full prompt** (tampilkan LENGKAP, jangan dipotong — pastikan ada "square 1:1" di dalamnya)
2. The Venturo logo (`assets/image_1c155d.png`) — dikirim sebagai reference image ke API, AI composites naturally
3. **Ask for approval:** "Apakah spec ini sesuai? Saya akan generate via maxrouter.io Chat Completions API dengan model Qwen-Image-2.0-Pro dan referensi logo Venturo. Lanjut?"

### Phase 4: User Approval

Wait for explicit "lanjut" / "yes" / "setuju" before proceeding.

### Phase 5: Generation via maxrouter.io API

Panggil MCP tools secara berurutan:

**Step 1 — Generate:**
```
generate_catalog(prompt="{full prompt dari Phase 2/3 — LENGKAP, jangan dipotong}", tier="{starter|growth|enterprise}", image_size="2K", aspect_ratio="1:1")
```

Tool ini akan:
1. Load logo Venturo as data URI
2. Kirim POST request ke maxrouter.io Chat Completions API dengan model `qwen-image-2.0-pro`
3. Download hasil gambar ke `venturo-poster/output/`
4. Return path file

Jika gagal:
- "IMAGE_ROUTER_API_KEY not set" → "API key belum diatur. Set environment variable IMAGE_ROUTER_API_KEY."
- Error API lain → tampilkan detail error dari respons

> **CRITICAL:** Kirim prompt LENGKAP (dalam Bahasa Indonesia, format detail dengan Masalah/Solusi/Hasil) via `generate_catalog()`. Jangan dipotong/diringkas. Pastikan semua section (Masalah, Solusi, Hasil, Visual Themes, Brand & Desain, Design Rules) + preferensi user masuk semua. WAJIB sertakan "square 1:1" di prompt.

### Phase 6: Delivery

```
✔ Katalog berhasil dibuat! Tersimpan di:
  venturo-poster/output/venturo_{tier}_{timestamp}.png

  Resolusi: {image_size} ({aspect_ratio})
  Engine: Qwen-Image-2.0-Pro (via maxrouter.io Chat Completions API)
  Logo: AI-composited from reference image
```

## Critical Rules

- **Always** run the interview phase first. Never skip to generation.
- **Never generate immediately after interview.** Show preview spec and get approval first.
- **Do NOT generate or composite the logo separately.** The Venturo logo is sent as a reference image to the API and AI composites it naturally into the design.
- **Do NOT use Pillow or other local rendering.** The Qwen-Image model handles ALL visual generation.
- **Always** include the Venturo logo reference in the prompt instructions.
- **Gunakan Bahasa Indonesia untuk prompt** (Qwen-Image-2.0-Pro handle Bahasa Indonesia dengan baik).
- **Prompt harus detail dengan Masalah/Solusi/Hasil** — ini memberikan konteks bisnis yang kuat untuk menghasilkan gambar yang relevan. Jangan dipotong.
- **WAJIB sertakan "square 1:1"** atau "ukuran 1:1" di setiap prompt karena ini khusus WhatsApp Business catalog.
- **Jika MCP tool gagal**, tampilkan error detailnya ke user dan tawarkan untuk coba lagi.

## MCP Server Configuration

Project ini support 3 platform. Pilih sesuai kebutuhan:

### Claude Code
`.mcp.json` di project root sudah include — auto-load saat startup.
Atau register global:
```bash
claude mcp add --scope user venturo-poster -- python3 venturo-poster/mcp-playwright/server.py
```

### OpenCode
`.mcp.json` di project root — OpenCode auto-load pas startup.
Atau via `opencode.json`:

### Antigravity (agy)
Plugin auto-register lewat installer (`./install.sh`).
Atau manual di `~/.gemini/config/mcp_config.json`:
```json
{
  "mcpServers": {
    "venturo-poster": {
      "command": "python3",
      "args": ["<absolute_path>/venturo-poster/mcp-playwright/server.py"],
      "env": {
        "IMAGE_ROUTER_API_KEY": "<your_api_key>"
      }
    }
  }
}
```

Ganti `<absolute_path>` dengan path lengkap ke project.
Ganti `<your_api_key>` dengan maxrouter.io API key.

## File Reference

| Path | Purpose |
|------|---------|
| `plugin.json` | Plugin manifest |
| `skills/venturo-poster/SKILL.md` | This skill definition |
| `assets/image_1c155d.png` | Official Venturo logo (sent as reference to maxrouter.io API) |
| `mcp-playwright/server.py` | MaxRouter MCP server — Chat Completions API-based image generation |
| `mcp-playwright/requirements.txt` | Python dependencies for MCP server |
| `templates/packages_context.md` | Venturo service tier reference with sales copy |
| `output/` | Generated catalog images |
