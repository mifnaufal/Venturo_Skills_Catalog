---
name: qwen-poster
description: >
  Use when the user wants to generate promotional poster images via Qwen AI chat
  (chat.qwen.ai) using Playwright automation — e.g. "buat poster pakai Qwen",
  "generate poster promosi dari Qwen", "Qwen-Image", "scrape/otomasi chat Qwen",
  "login qwen", "poster paket venturo", "poster venturo starter/growth/enterprise",
  "buatkan poster paket venturo", or when a poster should be rendered as an
  AI-generated image instead of HTML/CSS. Covers login persistence, the
  Create-image mode (Qwen-Image 3.0, 1:1), prompt building from structured
  promo fields, and downloading the generated PNG.
license: MIT
---

# Qwen Poster — Generate Poster Promosi via chat.qwen.ai

Otomasi chat.qwen.ai dengan Playwright untuk generate poster promosi sebagai **gambar AI** (Qwen-Image), bukan HTML/CSS.

## PERTANYAAN WAJIB — BACA DULU SEBELUM BICARA

**Kapan berlaku:** SETIAP kali skill ini dijalankan — lewat `/qwen-poster`, `/qwen-poster ...`, atau saat user minta poster Qwen/Venturo. Pesan pertama kamu HARUS membuka alur wawancara di bawah. **JANGAN** tanya "mau bantuan apa?", "kamu mau buat poster apa?", "mau login/generate/detect yang mana?", atau mengulang daftar perintah.

**Alur wawancara (harus berurutan, jangan dilewati):**

### Langkah 0 — Cek login (selalu pertama)
Cek status login lewat bash: `ls .qwen-profile/storage-state.json`.
- **File tidak ada** → sampaikan: *"Belum login. Mau login sekarang? Nanti muncul jendela browser chat.qwen.ai — kamu login manual, lalu aku lanjutkan otomatis."* Tunggu jawaban user. Kalau setuju → jalankan `node .claude/skills/qwen-poster/scripts/qwen-poster.mjs login` (user login manual di jendela browser, tekan Enter). Setelah selesai → lanjut ke Langkah 1.
- **File ada** → sampaikan: *"Login terdeteksi ✓"* → langsung lanjut ke Langkah 1.

### Langkah 1 — Tanya paket
```
1) Paket mana?
   A. Starter   B. Growth   C. Enterprise   (default: Starter)
```

### Langkah 2 — Tanya deskripsi (13 opsi, tampilkan SEMUA)
```
2) Deskripsi poster — pilih nomor:
   1. Website & aplikasi custom sesuai proses bisnis
   2. Integrasi ERP, CRM, HRIS, Payment Gateway, WhatsApp
   3. Dashboard monitoring & reporting real-time
   4. UI/UX modern, responsif, mudah digunakan
   5. Sistem aman, scalable, siap berkembang
   6. Efisiensi operasional lewat digitalisasi & otomatisasi
   7. Data terintegrasi — proses lebih cepat & akurat
   8. Keputusan bisnis berbasis data & laporan terintegrasi
   9. Bebas dari keterbatasan aplikasi berlangganan
   10. Aplikasi mengikuti bisnis, bukan sebaliknya
   11. Budget transparan + timeline jelas
   12. Dedicated team siap bantu dari analisis sampai go-live
   13. Kustom (ketik sendiri)
```

Jangan ringkas jadi "opsi A/B/C" atau hanya 2–3 opsi — user harus melihat semua 13.

**No exceptions:** meskipun user sudah menyebut paketnya ("buat poster paket growth"), tetap tanyakan deskripsi (opsi 1–13). Baru berhenti bertanya saat kedua jawaban terkumpul.

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

> **Langkah 0–2 (pesan pertama):** ikuti alur **PERTANYAAN WAJIB** di atas — cek login → tanya paket (A/B/C, default Starter) → tanya deskripsi (opsi 1–13). Jangan tanya apa-apa lain.

1. Setelah jawaban terkumpul, baca `pure_context.md` dan `theme_context.md` di project root. Jika salah satu hilang → refuse dan beri tahu user.
2. Ambil verbatim dari `pure_context.md` untuk paket terpilih: `Ideal untuk`, `Budget Proyek`, `Dedicated Team`, `Timeline`.
3. Ambil **Style Direction + Typography Direction** verbatim dari `theme_context.md`.
4. Susun prompt → `generate --prompt "<prompt>".` Rasio tetap 1:1.
5. Satu tier per eksekusi — jika user minta tier lain, ulangi workflow.

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

- **Tanya generik dulu** ("mau bantuan apa?", "poster apa yang mau dibuat?", "mau login/generate/detect?") saat skill dijalankan → SALAH. Pesan pertama harus membuka alur wawancara wajib: **cek login → paket → deskripsi**. Ini pelanggaran paling sering.
- **Lewati cek login** → sebelum tanya paket, cek dulu `storage-state.json` ada atau tidak (Langkah 0). Login belum → user tidak bisa generate.
- **Ringkas opsi deskripsi** jadi 2–3 pilihan → SALAH, user harus melihat semua 13 opsi.
- **Jangan jalankan 2 instance sekaligus** — profile browser (`~/.qwen-profile` di project) dipakai bersama.
- **Captcha/challenge**: selesaikan manual di jendela browser; script menunggu otomatis. Jangan restart.
- **Login expired** → gejala: generate tidak menemukan chat input → ulangi `login`.
- **Jangan pilih model lain** di UI Qwen — script sudah dikunci ke mode **Qwen-Image 3.0** + **1:1** (hasil rekaman klik user).
- **Alur exact** (jika manual): thinking `Auto`→`Thinking` → `Create Image` → `Qwen-Image 3.0` → `1:1` → ketik prompt → tombol send.
- **Prompt harus menyertakan teks persis** judul/tanggal/CTA — Qwen-Image kadang mengubah wording; cek hasil sebelum dikirim ke user.
