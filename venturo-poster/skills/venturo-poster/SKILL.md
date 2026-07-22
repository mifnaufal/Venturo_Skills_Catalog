---
name: venturo-poster
description: Generate WhatsApp Business catalog images for Venturo's software development service packages. Triggers on "catalog wa", "katalog whatsapp", "buat katalog", "catalog venturo", "Dreamina catalog". Enforces an interactive Art Director interview before any image generation.
---

# Venturo WhatsApp Business Catalog Generator

Generate **WhatsApp Business catalog images** for Venturo — an Indonesian software development company — using **Dreamina AI** via Playwright MCP browser automation.

**Engine:** Dreamina AI (online, via Playwright MCP browser automation)

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

## Prerequisites (AI Agent)

Sebelum memulai generation, pastikan:

1. **MCP server `venturo-poster-playwright` sudah terdaftar** di Antigravity config:
   ```json
   {
     "mcpServers": {
       "venturo-poster-playwright": {
         "command": "python3",
         "args": ["<plugin_path>/mcp-playwright/server.py"],
         "env": {}
       }
     }
   }
   ```
2. **Dependencies sudah terinstall** (`pip install -r <plugin_path>/mcp-playwright/requirements.txt`)
3. **Chromium sudah terinstall** (`playwright install chromium`)

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `browser_start` | Launch Chromium browser |
| `browser_stop` | Close browser and cleanup |
| `browser_navigate(url)` | Go to a URL |
| `browser_click(selector)` | Click first visible element matching CSS selector |
| `browser_fill(selector, text)` | Fill an input/textarea with text |
| `browser_upload_file(file_path)` | Upload file via file input |
| `browser_screenshot(output_path)` | Take full-page screenshot |
| `browser_wait(duration_ms)` | Wait for N milliseconds |
| `browser_wait_for_url(pattern, timeout_ms)` | Wait until URL matches regex |
| `browser_evaluate(script)` | Run JavaScript in page |
| `dreamina_login(email, password)` | Login to Dreamina with email (NOT Google). Multi-fallback selectors. |
| `dreamina_upload_reference()` | Upload Venturo logo as reference image. Multi-fallback. |
| `dreamina_fill_prompt(prompt)` | Fill Dreamina prompt textarea. Multi-fallback. |
| `dreamina_click_generate()` | Click "Generate" button. Multi-fallback. |

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

### Phase 5: Generation via Playwright MCP

1. Minta user input Dreamina **email & password** (login via email, BUKAN Google).
   Gunakan environment variable `DREAMINA_EMAIL` dan `DREAMINA_PASSWORD` jika tersedia.

2. Panggil MCP tools secara berurutan:

   **Step 1 — Start browser:**
   ```
   browser_start(headless=false)
   ```
   Jika gagal: "Gagal launch browser. Pastikan Chromium sudah terinstall."

   **Step 2 — Navigate to login page:**
   ```
   browser_navigate("https://dreamina.capcut.com/ai-tool/home?need_login=true&type=image&workspace=0")
   ```
   Jika gagal: coba `browser_navigate("https://dreamina.capcut.com/")` lalu cari tombol sign in manual.

   **Step 3 — Login to Dreamina (email only, NOT Google):**
   ```
   dreamina_login(email, password)
   ```
   Tool ini akan auto-fill email & password form dan submit.
   Jika gagal: "Auto-login gagal. Silakan login manual di browser, lalu beri tahu saya setelah selesai." Lanjut ke step 4 setelah user konfirmasi.

   **Step 4 — Navigate to AI image tool:**
   ```
   browser_navigate("https://dreamina.capcut.com/ai-tool/image")
   browser_wait(3000)
   ```

   **Step 5 — Upload logo reference:**
   ```
   dreamina_upload_reference()
   ```
   Jika gagal: minta user upload logo manual dari `assets/image_1c155d.png`, lalu `browser_wait(30000)`.

   **Step 6 — Fill prompt:**
   ```
   dreamina_fill_prompt("{full prompt dari Phase 2/3 — LENGKAP, jangan dipotong}")
   ```
   Jika gagal: "Tolong paste prompt ini ke Dreamina: {prompt}"
   Lalu `browser_wait(30000)`.

   **Step 7 — Click Generate:**
   ```
   dreamina_click_generate()
   ```
   Jika gagal: "Tolong klik tombol Generate di browser."

   **Step 8 — Wait for generation:**
   ```
   browser_wait(180000)
   ```
   Tunggu ±3 menit. Jika user merasa sudah selesai, bisa lanjut lebih cepat.

   **Step 9 — Screenshot:**
   ```
   browser_screenshot("venturo-poster/output/dreamina_{tier}.png")
   ```

   **Step 10 — Cleanup:**
   ```
   browser_stop()
   ```

> **CRITICAL:** Kirim prompt LENGKAP ke Dreamina via `dreamina_fill_prompt`. Jangan dipotong/diringkas. Semua section (Masalah, Solusi, Hasil, Visual Themes, Brand, Design Rules, preferensi user) harus masuk semua ke prompt.

### Phase 6: Delivery

```
✔ Katalog berhasil dibuat! Tersimpan di:
  venturo-poster/output/dreamina_starter.png

  Resolusi: 1:1 square (Dreamina)
  Engine: Dreamina AI (Playwright MCP)
  Logo: AI-composited from reference image
```

## Critical Rules

- **Always** run the interview phase first. Never skip to generation.
- **Never generate immediately after interview.** Show preview spec and get approval first.
- **Do NOT generate or composite the logo separately.** The Venturo logo is uploaded as a reference image to Dreamina and AI composites it naturally into the design.
- **Do NOT use Pillow or other local rendering.** The Dreamina AI engine handles ALL visual generation.
- **Always** include the Venturo logo reference in the prompt instructions.
- **Always use Bahasa Indonesia** untuk konten catalog.
- **Login via email, NOT Google.** Jangan klik tombol Google login. Gunakan `dreamina_login()` yang sudah auto-fill email + password.
- **Prompt harus LENGKAP & DETAIL.** Jangan pernah menyingkat atau meringkas prompt. Semua section (Masalah, Solusi, Hasil, Visual Themes, Brand, Design Rules) + preferensi user harus masuk semua. Jika user request spesifik (warna, layout, teks), incorporate ke dalam prompt.
- **Jika MCP tool gagal**, coba sekali lagi. Jika tetap gagal, minta user melakukan step tersebut manual di browser.

## MCP Server Configuration

Tambahkan MCP server ini ke Antigravity config (`~/.gemini/config/antigravity.json` atau sesuai setup):

```json
{
  "mcpServers": {
    "venturo-poster-playwright": {
      "command": "python3",
      "args": ["<absolute_path>/mcp-playwright/server.py"],
      "env": {}
    }
  }
}
```

Ganti `<absolute_path>` dengan path lengkap ke `venturo-poster/mcp-playwright/server.py`.

## File Reference

| Path | Purpose |
|------|---------|
| `plugin.json` | Plugin manifest |
| `skills/venturo-poster/SKILL.md` | This skill definition |
| `assets/image_1c155d.png` | Official Venturo logo (uploaded as reference to Dreamina) |
| `mcp-playwright/server.py` | Playwright MCP server — browser automation tools |
| `mcp-playwright/requirements.txt` | Python dependencies for MCP server |
| `templates/packages_context.md` | Venturo service tier reference with sales copy |
| `output/` | Generated catalog images |
