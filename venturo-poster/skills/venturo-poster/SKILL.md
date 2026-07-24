---
name: venturo-poster
description: Generate WhatsApp Business catalog images for Venturo software packages (Starter/Growth/Enterprise) using Cloudflare Workers AI. Triggers: catalog wa, katalog whatsapp, buat katalog, catalog venturo, poster venturo.
---

# Venturo Poster Skill

Generate **WhatsApp Business catalog images** for Venturo software packages (Starter/Growth/Enterprise) using **Cloudflare Workers AI**.

**Engine:** Self-hosted Cloudflare Worker (Workers AI — SDXL Lightning)
**Output:** PNG, 1400x1024 — WhatsApp Business catalog + right-side blank space for Pillow overlay

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

- **Size:** 1400x1024 pixels (canvas lebar — gambar di kiri 65%, ruang kosong putih di kanan 35%)
- **Format:** PNG
- **Style:** WhatsApp Business catalog — clean, professional, modern, minimal
- **Right-side space:** Area kosong putih di sisi KANAN (~490px) untuk overlay Pillow (logo, teks, QR code) oleh user
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
3. **Overlay Content** — Apa yang mau ditaruh di space kanan? (logo Venturo, QR code, teks custom, dll?)
4. **Custom Content** — Teks/statistik khusus yang mau ditampilkan di bagian desain?

### Phase 2: Build Detailed Prompt

Read `templates/packages_context.md` for tier themes and sales copy. Build a detailed prompt in **Bahasa Indonesia** with ALL sections below:

```
Buat gambar katalog WhatsApp Business untuk paket {TIER_NAME}.
FORMAT: GAMBAR CATATAN PROFESIONAL DENGAN RUANG KOSONG DI KANAN.
Bagian KIRI (65% lebar) = desain katalog. Bagian KANAN (35% lebar) = RUANG KOSONG PUTIH.

KOMPOSISI:
- Desain layout 2 bagian: KIRI = konten katalog, KANAN = ruang kosong putih.
- Konten katalog di sisi kiri (maks 65% dari lebar gambar).
- JANGAN isi area sisi kanan dengan apapun — biarkan putih/kosong.
- Layout vertikal di area kiri: header di atas, body di bawah.
- Area kanan SEMPURNA PUTIH/KOSONG untuk overlay konten afterward.

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

ATURAN SPASI KANAN:
- SISAKAN RUANG KOSONG PUTIH di SISI KANAN sekitar 35% dari lebar gambar.
- Design harus muat penuh di sisi KIRI (65% width).
- Area kanan harus BERSIH TANPA apa pun.
- Ini untuk overlay Pillow nanti (bisa diisi logo, teks, QR code, dll).

DESIGN RULES (WAJIB DIPATUHI):
1. KONTRAKSI SPASI KANAN — Area KANAN 35% harus KOSONG PUTIH.
2. Konten katalog HARUS muat di area KIRI saja (65% width).
3. WhatsApp Business catalog — bersih, profesional, modern.
4. Bahasa Indonesia untuk semua teks di area desain.
5. Style "Default Venturo" — teal + putih + abu. Profesional dan korporat.
6. Hierarki visual: judul paket > harga > subjudul > list fitur > footer.
7. Whitespace cukup di area desain — design breathable, jangan padat.
8. (tambahkan preferensi user dari interview jika ada)
```

### Phase 3: Preview + Approval

Show the full prompt + ask approval:
> "Apakah spec ini sesuai? Saya akan generate via Cloudflare Workers AI (SDXL Lightning). Output 1400x1024 dengan ruang kosong di kanan untuk overlay Pillow. Lanjut?"

### Phase 4: Generate & Deliver

Call MCP tool:
```
generate_catalog(prompt="{FULL_PROMPT}", tier="{starter|growth|enterprise}")
```

Then deliver:
> ✔ Katalog berhasil! Tersimpan di `venturo-poster/output/venturo_{tier}_{timestamp}.png`
> Ukuran: 1400x1024 — sisi KANAN kosong putih (~35%) siap untuk overlay Pillow (logo/teks/QR code).

## Critical Rules

- **Interview FIRST** — jangan generate langsung. Tanya tier, style, preferensi overlay.
- **Preview THEN generate** — tampilkan full prompt, tunggu approval.
- **Area KANAN KOSONG** — prompt HARUS instruksikan ruang kosong putih di kanan (~35%).
- **Konten di KIRI saja** — semua elemen katalog muat di 65% kiri gambar.
- **Whitespace cukup** — hindari desain terlalu padat di area kiri.
- **Logo** tidak dikirim ke API lagi (Workers AI ga support multi-modal). Logo overlay dilakukan manual via Pillow setelah generate.
- **Post-processing** (resize + paste ke canvas 1400x1024) dilakukan otomatis di server.py.
- **Bahasa Indonesia** untuk semua prompt dan output text.

## File Reference

| Path | Purpose |
|------|---------|
| `plugin.json` | Antigravity plugin manifest |
| `cloudflare-worker.mjs` | Cloudflare Worker source code |
| `assets/image_1c155d.png` | Official Venturo logo (untuk overlay Pillow manual) |
| `mcp-playwright/server.py` | MCP server — FastMCP app + Cloudflare Workers AI integration |
| `mcp-playwright/requirements.txt` | Python deps |
| `templates/packages_context.md` | Tier themes, sales copy, visual mapping |
| `starter_prompt.txt` | Example prompt (Starter tier) |
| `growth_prompt.txt` | Example prompt (Growth tier) |
| `enterprise_prompt.txt` | Example prompt (Enterprise tier) |
| `output/` | Generated catalog images (1400x1024) |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Area kanan terisi konten (tidak kosong) | Prompt belum tegas "RUANG KOSONG DI KANAN". Tambahkan section ATURAN SPASI KANAN di prompt. |
| Konten overflow area kiri | Prompt terlalu padat. Kurangi item teks atau perkecil visual theme keywords. |
| Image generation failed / timeout | Cek CLOUDFLARE_WORKER_URL dan CLOUDFLARE_API_KEY. Pastikan Workers AI binding sudah di-set di dashboard Cloudflare. |
| MCP module not found | Jalankan lewat venv: `.venv/bin/python` atau `pip install -r requirements.txt`. |
