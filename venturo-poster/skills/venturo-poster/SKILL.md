---
name: venturo-poster
description: Generate WhatsApp Business catalog images for Venturo software packages (Starter/Growth/Enterprise) using Qwen-Image-2.0-Pro via maxrouter.io API. Triggers: catalog wa, katalog whatsapp, buat katalog, catalog venturo, poster venturo.
---

# Venturo Poster Skill

Generate **WhatsApp Business catalog images** for Venturo software packages (Starter/Growth/Enterprise) using **Qwen-Image-2.0-Pro** via maxrouter.io API.

**Engine:** Qwen-Image-2.0-Pro — maxrouter.io (`https://maxrouter.io/llm-api/v1/chat/completions`)
**Output:** PNG, square 1:1 (1024x1024) — WhatsApp Business catalog format

## Design System (Venturo Brand)

| Element | Spec |
|---------|------|
| **Primary** | `#006D79` (teal gelap) |
| **Primary Light** | `#009BAD` (teal terang) |
| **Dark** | `#202020` |
| **Light BG** | `#F6F8F8` (abu sangat muda) |
| **Heading** | `#292929` |
| **Body** | `#4B5563` |
| **Background** | `#FFFFFF` (putih) |
| **Font style** | Bold condensed sans-serif headings, clean sans-serif body |

## Output Specs

- **Size:** 1024x1024 pixels (square 1:1 PERSENG SEMPURNA)
- **Format:** PNG
- **Style:** WhatsApp Business catalog — clean, professional, modern, minimal
- **Language:** Bahasa Indonesia

## Package Tiers

| Tier | Budget | Ideal for | Team | Timeline |
|------|--------|-----------|------|----------|
| **Starter** | Rp20M – Rp80M | UMKM, startup, website & mobile app sederhana | 1 BA + 1 Sr. Eng | 1–4 Minggu |
| **Growth** | Rp80M – Rp250M | Finance, HRIS, CRM, ERP, Inventory, WMS, Logistics, Sales, Production, Asset Management | 1 BA + 1 Sr. Eng + 1 UI/UX + 1 QA | 1–4.5 Bulan |
| **Enterprise** | Mulai Rp250M | AI, Big Data, cybersecurity, integrasi lintas sistem | 1 BA + 1 Sr. Eng + 1 Mid Eng + 1 UI/UX + 1 QA + 1 Pen Test | 2–8 Bulan |

## Workflow (4 phase — follow strictly)

### Phase 1: Interview User

Ask 3-5 questions in **Bahasa Indonesia**:

1. **Tier** — Starter / Growth / Enterprise
2. **Design Preferences** — Gaya visual tertentu? Preferensi warna?
3. **Logo** — Posisi logo Venturo? (opsional, AI atur natural)
4. **Custom Content** — Teks/statistik khusus yang mau ditampilkan?

### Phase 2: Build Detailed Prompt

Read `templates/packages_context.md` for tier themes and sales copy. Build a detailed prompt in **Bahasa Indonesia** with ALL sections below:

```
Buat gambar katalog WhatsApp Business untuk paket {TIER_NAME}.
FORMAT: SQUARE 1:1 (persegi sempurna 1024x1024 pixel). BUKAN BANNER LANDSCAPE.

KOMPOSISI — WAJIB SQUARE PERSEGI:
- Desain layout persegi. Header di atas = branding + judul paket. Body di bawah = konten.
- Layout 2 kolom di body: kiri = visual mockup/illustrasi, kanan = teks fitur.
- Header bar: Nama paket besar di tengah/kanan, logo di kiri atas.
- SEMUA elemen muat dalam frame PERSEGI. Jangan buat layout horizontal/banner.

VENTURO — Software House Malang
PAKET: {TIER_NAME}
BUDGET: {budget_range}
IDEAL UNTUK: {target_audience}
TIM DEDICATED: {team}
TIMELINE: {timeline}

MASALAH YANG DISELESAIKAN:
- {masalah_item_1}
- {masalah_item_2}
- {masalah_item_3}

SOLUSI:
- {solusi_item_1}
- {solusi_item_2}
- {solusi_item_3}

HASIL:
- {hasil_item_1}
- {hasil_item_2}
- {hasil_item_3}

TEXT YANG HARUS TERCETAK DI GAMBAR:
- Judul besar: PAKET {TIER_NAME}
- Subjudul: Ideal untuk {target_audience}
- Box berwarna teal: {budget_range}
- List 4-6 fitur utama singkat
- Footer: VENTURO — Software House Malang

VISUAL — SESUAI TIER:
- {5-6 visual theme dari templates/packages_context.md}

BRAND & DESAIN:
- Warna Primer: #006D79 (teal gelap) — dominan di elemen penting
- Warna Sekunder: #009BAD (teal terang) — aksen sekunder
- Background: #FFFFFF dengan gradasi ke #F6F8F8
- Heading: #292929 (hitam lembut)
- Body Text: #4B5563 (abu sedang)

STYLE: {style keywords dari templates/packages_context.md}

DESIGN RULES (WAJIB DIPATUHI):
1. FORMAT SQUARE 1:1 — PERSEGI SEMPURNA. BUKAN LANDSCAPE. BUKAN BANNER. BUKAN WIDE.
2. WhatsApp Business catalog — bersih, profesional, modern.
3. Bahasa Indonesia untuk semua teks.
4. Style "Default Venturo" — teal + putih + abu. Profesional dan korporat.
5. Logo Venturo dari referensi gambar, letakkan di kiri atas secara natural.
6. Hierarki visual: judul paket > harga > subjudul > list fitur > footer.
7. Whitespace cukup — design breathable, jangan padat.
8. (tambahkan preferensi user dari interview jika ada)
```

### Phase 3: Preview + Approval

Show the full prompt + ask approval:
> "Apakah spec ini sesuai? Saya akan generate via maxrouter.io API (Qwen-Image-2.0-Pro) dengan logo Venturo sebagai reference. Lanjut?"

### Phase 4: Generate & Deliver

Call MCP tool:
```
generate_catalog(prompt="{FULL_PROMPT}", tier="{starter|growth|enterprise}", image_size="1K", aspect_ratio="1:1")
```

Then deliver:
> ✔ Katalog berhasil! Tersimpan di `venturo-poster/output/venturo_{tier}_{timestamp}.png`

## Critical Rules

- **Interview FIRST** — jangan generate langsung. Tanya tier, style, preferensi.
- **Preview THEN generate** — tampilkan full prompt, tunggu approval.
- **SQUARE 1:1 WAJIB** — prompt harus tegas soal format persegi, bukan banner. Tulis "BUKAN BANNER LANDSCAPE".
- **Komposisi top-bottom**, bukan left-right. Header di atas, konten di bawah.
- **Whitespace cukup** — hindari desain terlalu padat.
- **Logo** selalu dikirim sebagai reference image ke API, AI-compose secara natural.
- **Post-processing** (crop + resize 1024x1024) dilakukan otomatis di server.py.
- **Bahasa Indonesia** untuk semua prompt dan output text.

## File Reference

| Path | Purpose |
|------|---------|
| `plugin.json` | Antigravity plugin manifest |
| `assets/image_1c155d.png` | Official Venturo logo (reference image ke API) |
| `mcp-playwright/server.py` | MCP server — FastMCP app + maxrouter.io integration |
| `mcp-playwright/requirements.txt` | Python deps |
| `templates/packages_context.md` | Tier themes, sales copy, visual mapping |
| `starter_prompt.txt` | Example prompt (Starter tier) |
| `output/` | Generated catalog images |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Gambar keluar landscape/banner | Prompt belum tegas soal "SQUARE 1:1" + "BUKAN BANNER". Tambahkan section KOMPOSISI dengan instruksi layout top-bottom. |
| Hasil crop terlalu sempit | Server otomatis crop-center. Prompt yang lebih baik = gambar dari API yang lebih square-native. |
| API key error | Set `IMAGE_ROUTER_API_KEY` di `.env` atau env var. |
| MCP module not found | Jalankan lewat venv: `.venv/bin/python` atau `pip install -r requirements.txt`. |
