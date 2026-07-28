---
name: venturo-claude-context
description: "Project context and guidelines for working with Venturo using Claude Code."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Venturo, Claude, Service-Packages, Marketing, Documentation]
    related_skills: [venturo-poster, venturo-claude-code, venturo-opencode, venturo-hermes-agent]
---

# Venturo — CLAUDE.md Context untuk Claude Code (v2.0)

Gunakan konteks ini ketika bekerja dengan proyek Venturo via Claude Code. Skill ini membantu Claude memahami struktur paket layanan, warna brand, dan pola komunikasi yang konsisten.

Reference file: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/packages_context.md`

Style reference: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/image.png` (logo Venturo)

---

## Trigger Behavior

Ketika skill ini dimuat di direktori `.claude/skills/venturo/`, Claude Code akan otomatis menemukan dan load konteks ini saat user memberikan perintah terkait Venturo (generate poster, buat dokumentasi, review kode). **Claude akan otomatis merujuk ke info paket, color palette, dan layout specs ini**.

**PENTING:** Gunakan spesifikasi spesifik — jangan hanya bilang "buat dokumentasi" tapi berikan detail apa yang dibutuhkan (format, section mana yang muncul, target audiens).

---

## Paket Pengembangan Sistem (Perbandingan Tier)

| | **Starter** | **Growth** | **Enterprise** |
|---|---|---|---|
| **Ideal untuk** | UMKM, usaha mikro, startup | Perusahaan custom | Enterprise skala besar |
| **Budget** | Rp20 Juta – Rp80 Juta | Rp80 Juta – Rp250 Juta | Mulai Rp250 Juta |
| **Tim** | 1 BA + 1 Senior Engineer | 1 BA + 1 Senior Engineer + UI/UX + QA | 1 BA + 1 Senior + 1 Intermediate + UI/UX + QA + Pen Tester |
| **Timeline Analysis** | 1-2 Minggu | 2 Minggu - 1 Bulan | 1-2 Bulan |
| **Development** | 2 Minggu - 1 Bulan | 1 - 2 Bulan | 2 - 4 Bulan |
| **Testing & Deploy** | 1-2 Minggu | 2 Minggu - 1 Bulan | 2 Bulan |

---

### Masalah yang Sering Terjadi Perusahaan

1. Perusahaan butuh website/app sesuai proses bisnis actual
2. Berlanganan tapi fitur belum cukup operasional
3. Bisnis harus menyesuaikan sistem, bukan sebaliknya
4. Sulit kustomisasi karena keterbatasan system
5. Integrasi sulit dengan system existing
6. Tampilan kurang user-friendly
7. System tidak support saat bisnis bertumbuh

---

### Solusi Venturo

1. Pengembangan Website & Mobile (Android & iOS) custom
2. Analisis kebutuhan bisnis
3. Desain UI/UX modern & responsif
4. Fitur fleksibel untuk masa depan
5. Integrasi ERP, CRM, HRIS, Payment Gateway, WhatsApp, API
6. Dashboard monitoring & reporting
7. System aman, scalable, siap berkembang

---

### Hasil yang Didapat

1. Website/app sesuai kebutuhan & proses bisnis
2. Efisiensi operasional via digitalisasi
3. Sistem fleksibel & mudah dikembangkan
4. Integrasi data lebih baik
5. Pengalaman pengguna lebih baik
6. Support pengambilan keputusan via dashboard

---

## Brand Guidelines

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Teal | `#006D79` | Brand primary, section blocks |
| Light Teal | `#009BAD` | Secondary accents, gradients |
| Dark BG | `#0A1B1F` | Enterprise dark background |
| Dark Surface | `#142A2F` | Enterprise gradient mid-tone |
| Light BG | `#FFFFFF` | Starter / Growth background |
| Subtle BG | `#F4F8F8` | Off-white card backgrounds |
| Body Text | `#374151` | Primary description text |
| Muted Gray | `#9ca3af` | Footer, decorative elements |

### Color Assignment Per Tier

| Tier | Background | Accent | Budget Pill |
|------|-----------|--------|-------------|
| **Starter** | `#FFFFFF` | `#006D79` | `#006D79` capsule, white text |
| **Growth** | `#FFFFFF` + dot grid | `#006D79` | Gradient `#006D79` → `#009BAD` |
| **Enterprise** | Gradient `#0A1B1F` → `#112D35` | `#009BAD` | `#009BAD` capsule, dark text |

Checkmark circles: **56×56px** filled circle, white ✓ inside (double dari 28px).

**CTA accent:** `#10B981` (hijau) untuk button "Konsultasi Gratis" — kontras terhadap palette teal.

---

### Layout Specs (HD — 2048×2048px, 1:1)

- **Layout Pattern**: Z-Pattern — Logo (ki-atas) → Tier name (ka-atas) → Content (ki-bawah) → CTA (ka-bawah)
- **Focal Point**: Tier **224px** adalah satu-satunya elemen dominan. Illustrasi di z-index 0, opacity max 0.15.
- **Header**: Logo small 72–96px + "PAKET [TIER]" massive (**224px**, weight 900, tracking -8px)
- **Budget Box**: Solid color pill with price range (**56px**)
- **CTA Button**: WAJIB — "Konsultasi Gratis" di kanan-bawah, `#10B981`, font **32px** weight 700, pill shape
- **Typography**: Google Font Inter (all weights 300-900)
- **Section Label**: Uppercase, **24px**, letter-spacing 8px, weight 800
- **Feature/Bullet**: **36px** weight 600 with **56×56px** checkmark circles
- **Illustrations**: WAJIB SVG/p5.js di background (jangan compete dengan konten)
- **White Space**: Margin luar **64px**, gap antar section **48–64px**
- **Footer**: "© venturo.id" subtle muted gray, **24px**
- **Output**: 4096×4096px (DSF 2 × 2048 viewport)

---

## Content Mapping Reference (Default Text Blocks — Untuk Poster Generation)

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

---

## Task Recommendations (Claude Code Usage Patterns)

### Saat Bekerja dengan Claude Code

1. **Baca dulu packages_context.md** sebelum mulai task — berisi data lengkap tentang paket Venturo
2. **Gunakan print mode (`-p`)** buat task terukur cepat seperti generate dokumen atau format ulang data
3. **Pakai tmux session** kalau perlu multi-turn iteration (contoh: review kode panjang, refactor bertahap)
4. **Ambil data dari packages_context.md** via pipe atau file attachment agar Claude punya context akurat
5. **Verify output** dengan membandingkan ke specs di documentation

### Contoh Command Pattern

```bash
# Generate dokumentasi service package
terminal(command="cat packages_context.md | claude -p 'Buat table perbandingan Starter vs Growth vs Enterprise untuk dokumentasi klien' --max-turns 5")

# Review tugas dengan model tertentu
terminal(command="claude -p 'Review docs paket enterprise dan tambahkan contoh integrasi system' --model sonnet --max-turns 8")

# Print mode kerja satu kali cepat
terminal(command="claude -p 'Ringkas 3 paket Venturo dalam 3 paragraf masing-masing' --max-turns 3")

# Generate poster HD via Playwright (gunakan venturo-poster skill)
terminal(command="claude -p 'Generate poster starter HD: 2048x2048 container + DSF 2 → 4096x4096 output, SVG illustrations, warna #006D79' --max-turns 20")
```

---

## CLAUDE.md Rules Tambahan (untuk Project Context)

- Gunakan palet warna `#006D79`, `#009BAD`, `#0A1B1F` + CTA accent `#10B981` untuk semua desain/konten terkait Venturo
- Format tabel perbandingan harus jelas dan mudah dibaca
- Timeline tetap pakai format minggu/bulan dalam Bahasa Indonesia (misal: "1-2 Minggu", "1-2 Bulan")
- Sebutkan budget dalam format "RpXX Juta" atau rentang budget
- Untuk poster/png generation, gunakan **2048×2048px** container + DSF 2 → output **4096×4096px HD**
- Gunakan konsep **"rame tapi simple"** — visually rich dengan SVG/p5.js, tapi hierarchy jelas
- WAJIB ada illustrasi SVG (circle/path/polygon) ATAU p5.js (noise wave, random dots, particle) — di z-index 0, opacity max 0.15
- Tone: profesional namun accessible, cocok untuk UMKM hingga enterprise
- Always embed the Venturo logo (`image.png`) — DO NOT use plain text "VENTURO"
- All text must wrap properly — no clipping at 2048×2048 boundary
- Double semua ukuran font, padding, dan spacing (refer ke tabel di packages_context.md)
- WAJIB ada CTA button "Konsultasi Gratis" di kanan-bawah, pake accent color `#10B981`
- Gunakan Z-Pattern layout: Logo(ki-atas) → Tier name(ka-atas) → Content(ki-bawah) → CTA(ka-bawah)
- Palet max 4 warna: background + `#006D79` + `#009BAD` + CTA accent

---

## Multi-Agent Pattern Reference (Claude + OpenCode)

Workflow koordinatif antar skill:

```
# Claude Code review docs → generate JSON structure
claude_output = terminal(command="claude -p 'Review packages_context.md, generate JSON structure untuk poster Enterprise' --output-format json --max-turns 5")

# OpenCode render berdasarkan JSON
opencode_output = terminal(command="opencode run 'Render poster Enterprise dari JSON structure' --max-turns 15")

# Claude Code validate output
validation = terminal(command="claude -p 'Validate venturo-enterprise.png: pastikan ukuran 4096x4096 (HD), CTA button ada, Z-Pattern layout benar' --max-turns 3")
```

---

## Verification (Smoke Test)

```python
# Test CLAUDE context loading via Claude Code
test_result = terminal(command="claude -p 'Test: CLAUDE_VENTURO_CONTEXT_LOADED v2.0 OK — Package tiers: Starter, Growth, Enterprise; Colors: #006D79, #009BAD, #0A1B1F' --max-turns 3")
```

Success criteria: Output mengandung `CLAUDE_VENTURO_CONTEXT_LOADED v2.0 OK`, semua info paket dan warna disebut benar.

---

**Catatan:** Skill ini bekerja sama dengan `venturo-poster`, `venturo-claude-code`, `venturo-opencode`, dan `venturo-hermes-agent` di katalog Venturo. Semua skill mengacu pada `packages_context.md` sebagai sumber data tunggal. Ready untuk Claude Code auto-discovery via `.claude/skills/venturo/SKILL.md`.
