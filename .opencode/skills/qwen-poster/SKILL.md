---
name: qwen-poster
description: >
  Use when the user wants to generate promotional poster images via Qwen AI chat
  (chat.qwen.ai) using Playwright automation — e.g. "buat poster pakai Qwen",
  "generate poster promosi dari Qwen", "Qwen-Image", "scrape/otomasi chat Qwen",
  "login qwen", or when a poster should be rendered as an AI-generated image
  instead of HTML/CSS. Covers login persistence, the Create-image mode
  (Qwen-Image 3.0, 1:1), prompt building from structured promo fields, and
  downloading the generated PNG.
license: MIT
---

# Qwen Poster — Generate Poster Promosi via chat.qwen.ai

Otomasi chat.qwen.ai dengan Playwright untuk generate poster promosi sebagai **gambar AI** (Qwen-Image), bukan HTML/CSS.

## Prasyarat

- Node.js + Playwright terinstall di project root: `npm install`
- Folder skill ada di **dua tempat** (sinkronkan selalu):
  - `.claude/skills/qwen-poster/` (Claude Code)
  - `.opencode/skills/qwen-poster/` (opencode)

## Commands

Semua dijalankan dari project root:

| Perintah | Fungsi |
|---|---|
| `node .claude/skills/qwen-poster/scripts/qwen-poster.mjs login` | Login manual sekali (storage state tersimpan, diulang hanya kalau sesi expired) |
| `node .claude/skills/qwen-poster/scripts/qwen-poster.mjs generate --title "..." [flags]` | Generate poster |
| `node .claude/skills/qwen-poster/scripts/qwen-poster.mjs detect` | Dump UI (button/input/image) saat selector gagal |

## Workflow

1. **Cek login**: `.qwen-profile/storage-state.json` ada? Kalau tidak (atau generate gagal di langkah input chat), jalankan `login` dulu — user login manual di jendela browser, tekan Enter.
2. **Kumpulkan info promo** (tanya user bila belum lengkap): title (wajib), subtitle, event, date, venue, cta, style, ratio (default 1:1).
3. **Generate**: jalankan `generate` dengan flag dari info promo. Script otomatis (alur terverifikasi via rekaman klik 2026-07-31): ubah thinking mode **Auto → Thinking** → buka mode menu → **Create Image** → pilih model **Qwen-Image 3.0** → pilih ukuran **1:1** → kirim prompt → tunggu gambar (max 5 menit) → simpan PNG ke `output/qwen-poster-<timestamp>.png`.
4. **Verifikasi**: cek file PNG ada dan size wajar (>50KB). Laporkan path ke user.
5. Flag `--prompt "..."` dipakai untuk prompt bebas; `--headless` hanya jika user minta.

## Mode Venturo Package Poster

Dipakai saat user minta poster paket Venturo (Starter / Growth / Enterprise). **Ambil isi/prompt material dari `pure_context.md` (konten) dan `theme_context.md` (tema design) — JANGAN ikuti workflow `VENTURO.md`** (itu milik skill `venturo-poster` yang render via canvas-design 1048×1048; kita tetap pakai alur Qwen 1:1).

1. Baca `pure_context.md` dan `theme_context.md` di project root. Jika salah satu hilang → refuse dan beri tahu user.
2. **Tanya 1 — Paket**: Starter / Growth / Enterprise (default: **Starter**).
3. **Tanya 2 — Deskripsi poster**: tampilkan **opsi pendek** (1 baris), user cukup pilih nomor/abjad. Bangun opsinya dari isi `pure_context.md`:

   | # | Opsi (1 baris) | Sumber |
   |---|---|---|
   | 1 | Website & aplikasi custom sesuai proses bisnis | Solusi |
   | 2 | Integrasi ERP, CRM, HRIS, Payment Gateway, WhatsApp | Solusi |
   | 3 | Dashboard monitoring & reporting real-time | Solusi |
   | 4 | UI/UX modern, responsif, mudah digunakan | Solusi |
   | 5 | Sistem aman, scalable, siap berkembang | Solusi |
   | 6 | Efisiensi operasional lewat digitalisasi & otomatisasi | Hasil |
   | 7 | Data terintegrasi — proses lebih cepat & akurat | Hasil |
   | 8 | Keputusan bisnis berbasis data & laporan terintegrasi | Hasil |
   | 9 | Bebas dari keterbatasan aplikasi berlangganan | Masalah |
   | 10 | Aplikasi mengikuti bisnis, bukan sebaliknya | Masalah |
   | 11 | Budget transparan + timeline jelas | Paket |
   | 12 | Dedicated team siap bantu dari analisis sampai go-live | Paket |
   | 13 | Kustom (ketik sendiri) | — |

   Biasakan menampilkan semua 13 opsi agar user tinggal pilih tanpa cek manual.
4. Ambil verbatim dari `pure_context.md` untuk paket terpilih: `Ideal untuk`, `Budget Proyek`, `Dedicated Team`, `Timeline`.
5. Ambil **Style Direction + Typography Direction** verbatim dari `theme_context.md`.
6. Susun prompt → `generate --prompt "<prompt>".` Rasio tetap 1:1.
7. Satu tier per eksekusi — jika user minta tier lain, ulangi workflow.

Contoh shape prompt (draf; isi mengikuti jawaban user & data dari file):

```
Design a premium, bold, modern Indonesian service-package poster, square 1:1.
Headline (dominant, uppercase, italic on the key word): "PAKET <TIER>".
Description tagline: <opsi deskripsi yang dipilih user>.
Ideal untuk: <isi dari pure_context.md>
Budget Proyek: <isi>
Dedicated Team: <isi>
Timeline: <isi>
--- TYPOGRAPHY (follow exactly) ---
<copy Typography Direction verbatim dari theme_context.md>
--- COLORS (keep exactly) ---
<copy Color Palette hex verbatim dari theme_context.md>
CTA button: "<Konsultasi Gratis|Hubungi Kami>".
All text exactly as provided — no invented wording.
```

## Kalau Gagal (UI berubah / selector tua)

1. Jalankan `detect` → screenshot + dump button/input/image yang terlihat disimpan ke `output/debug-screenshot.png`
2. Update `selectors.json` sesuai hasil dump
3. Ulangi `generate`. Kalau masih gagal, minta user menjalankan langkah manual dan catat URL/element yang muncul.

## Common Mistakes

- **Jangan jalankan 2 instance sekaligus** — profile browser (`~/.qwen-profile` di project) dipakai bersama.
- **Captcha/challenge**: selesaikan manual di jendela browser; script menunggu otomatis. Jangan restart.
- **Login expired** → gejala: generate tidak menemukan chat input → ulangi `login`.
- **Jangan pilih model lain** di UI Qwen — script sudah dikunci ke mode **Qwen-Image 3.0** + **1:1** (hasil rekaman klik user).
- **Alur exact** (jika manual): thinking `Auto`→`Thinking` → `Create Image` → `Qwen-Image 3.0` → `1:1` → ketik prompt → tombol send.
- **Prompt harus menyertakan teks persis** judul/tanggal/CTA — Qwen-Image kadang mengubah wording; cek hasil sebelum dikirim ke user.
