# Venturo Skills Catalog

Skill untuk generate **poster promosi** sebagai **gambar AI** lewat [chat.qwen.ai](https://chat.qwen.ai/)
(Qwen-Image 3.0) menggunakan otomasi Playwright. Terintegrasi dengan data paket layanan Venturo
(`pure_context.md`) dan tema design Venturo (`theme_context.md`).

Skill ini tersedia di **dua platform sekaligus** — Claude Code dan opencode — dan portabel:
semua file berada di dalam folder project ini, jadi siapa pun yang memegang folder ini bisa langsung
menggunakannya tanpa konfigurasi global.

---

## Struktur Folder

```
Venturo_Skills_Catalog/
├── .claude/skills/qwen-poster/        # skill untuk Claude Code
│   ├── SKILL.md                       # instruksi agent
│   ├── commands/                      # → slash command /qwen-poster (Claude Code)
│   └── scripts/
│       ├── qwen-poster.mjs            # subcommand: login | detect | record | generate
│       ├── selectors.json             # tabel selector (update saat UI Qwen berubah)
│       └── prompts.js                 # buildPrompt() — template prompt promo
├── .opencode/skills/qwen-poster/      # salinan identik untuk opencode
│   └── (scripts/ sama, commands/ terpisah)
├── pure_context.md                    # konten paket Venturo (Starter/Growth/Enterprise)
├── theme_context.md                   # tema design (palette + style + typography)
├── opencode.json                      # register skills.paths untuk opencode
├── .qwen-profile/                     # persistent browser profile + storage state (auto, jangan di-commit)
└── output/                            # hasil PNG + debug-screenshot (auto, jangan di-commit)
```

> **Penting:** `.claude/skills/qwen-poster/` dan `.opencode/skills/qwen-poster/` harus **selalu sinkron**.
> Setiap perubahan pada salah satu, salin ke yang lain (`cp -r`).

---

## Prasyarat

- **Node.js** (v18+, direkomendasikan v20/v22+)
- **Playwright** + browser Chromium
- **Akun chat.qwen.ai** (login manual sekali)

### Setup

```bash
# 1. Install dependency (di root project)
npm install

# 2. Install browser Chromium untuk Playwright
npx playwright install chromium

# 3. Login manual sekali (muncul jendela browser chat.qwen.ai)
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs login
```

Saat `login`, jendela browser terbuka — login manual ke akun Qwen kamu, selesaikan captcha/challenge
jika ada, lalu tekan **Enter** di terminal. Sesi tersimpan di `.qwen-profile/storage-state.json`.

---

## Tutorial Penggunaan

### Cara 1 — Via AI (disarankan)

Di **Claude Code** atau **opencode**, ketik dari root project:

```
/qwen-poster
```

AI akan membuka alur wawancara wajib (dalam urutan ini, tidak bisa dilewati):

1. **Cek login** — apakah `.qwen-profile/storage-state.json` ada. Belum login → AI menawarkan menjalankan `login`.
2. **Tanya paket** — `A. Starter` / `B. Growth` / `C. Enterprise` (default: Starter).
3. **Tanya deskripsi** — tampilkan **13 opsi** (user pilih nomor, atau pilih 13 = ketik sendiri).

Setelah kedua jawaban terkumpul, AI membaca `pure_context.md` + `theme_context.md`, menyusun prompt,
dan menjalankan generate otomatis. Poster tersimpan ke `output/qwen-poster-<timestamp>.png`.

### Cara 2 — Via CLI langsung (tanpa AI)

```bash
# Login (sekali, atau saat sesi expired)
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs login

# Generate poster dengan flag
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs generate \
  --title "PAKET STARTER" \
  --subtitle "Website & Aplikasi Custom" \
  --event "Venturo" \
  --cta "Konsultasi Gratis"
```

---

## Reference Command

Semua dijalankan dari **root project**.

### `login`

```
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs login
```

Login manual sekali. Jendela browser terbuka → login → tekan Enter → `storage-state.json` tersimpan.
Ulangi hanya jika sesi expired.

### `detect`

```
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs detect [--url "https://..."]
```

Dump UI saat selector gagal: screenshot ke `output/debug-screenshot.png` + daftar visible buttons,
inputs, dan 5 gambar terakhir. Dipakai untuk update `selectors.json`.

### `record`

```
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs record
```

Rekam klik user **setelah login** (aktivasi otomatis saat chat input terdeteksi). Hasilnya ditulis ke
`output/click-record.jsonl`. Dipakai untuk menangkap ulang alur UI ketika antarmuka Qwen berubah.

### `generate`

```
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs generate [flags]
```

Generate poster via mode Create Image (Qwen-Image 3.0, rasio 1:1).

| Flag | Fungsi | Contoh |
|---|---|---|
| `--title "..."` | Judul utama (wajib) | `--title "PAKET GROWTH"` |
| `--subtitle "..."` | Subjudul | `--subtitle "HRIS & CRM Terintegrasi"` |
| `--event "..."` | Nama event/produk | `--event "Venturo"` |
| `--date "..."` | Tanggal | `--date "2026-08-31"` |
| `--venue "..."` | Lokasi/venue | `--venue "Jakarta"` |
| `--cta "..."` | Call to action | `--cta "Konsultasi Gratis"` |
| `--style "..."` | Gaya visual (warna/mood/font) | `--style "modern teal, bold"` |
| `--ratio 1:1` | Rasio (default 1:1) | `--ratio 1:1` |
| `--prompt "..."` | Prompt bebas (override template) | `--prompt "Design a poster..."` |
| `--out path.png` | Lokasi output | `--out output/kustom.png` |
| `--headless` | Jalan tanpa jendela browser (risiko kena anti-bot) | `--headless` |
| `--url "https://..."` | Target URL (untuk `detect`) | `--url "https://chat.qwen.ai"` |

Contoh lengkap:

```bash
node .claude/skills/qwen-poster/scripts/qwen-poster.mjs generate \
  --title "PAKET STARTER" \
  --subtitle "Website & Mobile App Custom" \
  --event "Venturo" \
  --cta "Konsultasi Gratis" \
  --out output/starter.png
```

---

## Mode Venturo Package Poster

Saat user meminta poster paket Venturo, AI menyusun prompt dari dua file:

| File | Isi yang dipakai | Cara pakai |
|---|---|---|
| `pure_context.md` | `Ideal untuk`, `Budget Proyek`, `Dedicated Team`, `Timeline` | **verbatim** (tidak diubah wording) |
| `theme_context.md` | Color Palette hex, Style Direction, Typography Direction | **verbatim** |

Aturan:
- **Rasio 1:1**.
- **Satu tier per eksekusi** (Starter/Growth/Enterprise).
- Semua teks dalam poster **harus persis seperti di file** — Qwen-Image tidak boleh mengarang wording.
- Data diambil dari `pure_context.md` (bukan `VENTURO.md`).

### Contoh shape prompt

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

---

## Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| Generate gagal di langkah input chat | Login expired | Jalankan ulang `login` |
| Captcha/challenge muncul | Anti-bot | Selesaikan manual di jendela browser; script menunggu otomatis. Jangan restart. |
| Selector tidak ketemu (FAIL...) | UI Qwen berubah | `detect` → update `selectors.json` → ulangi `generate` |
| Timeout gambar (5 menit) | Generation gagal / UI berubah | Cek browser, jalankan `detect` |
| Dua generate jalan bersamaan | Profile browser dipakai bersama | Hanya jalankan **satu instance** sekaligus |

### Alur manual yang dikunci script

Jika harus melakukannya manual di browser: thinking `Auto → Thinking` → klik `+` → **Create Image** →
pilih **Qwen-Image 3.0** → pilih ukuran **1:1** → ketik prompt → tombol send.

---

## Maintenance

### Jika UI chat.qwen.ai berubah

1. Jalankan `node .claude/skills/qwen-poster/scripts/qwen-poster.mjs detect`
2. Cek `output/debug-screenshot.png` + dump button/input.
3. Update `scripts/selectors.json` sesuai selector baru.
4. Ulangi `generate`. Kalau masih gagal, jalankan `record` dan ikuti alur manual sekali — hasilnya
   tersimpan di `output/click-record.jsonl` sebagai referensi selector.

### Sinkronisasi dua salinan skill

```bash
cp -r .claude/skills/qwen-poster/ .opencode/skills/qwen-poster/
```

Pastikan `SKILL.md` dan `scripts/` identik di kedua folder.

### Yang wajib di-commit vs di-ignore

**Commit:** `.claude/`, `.opencode/skills/`, `.opencode/commands/`, `opencode.json`, `pure_context.md`,
`theme_context.md`, `package.json`, `package-lock.json`, `docs/`.

**Ignore (jangan commit):** `node_modules/`, `.qwen-profile/` (session login = rahasia), `output/`
(file generate), `conversations/` (log sesi), `.opencode/package*.json` (workspace npm lokal).

---

## Ringkasan Alur UI (terverifikasi 2026-07-31)

Thinking `Auto → Thinking` → buka mode menu (`div.mode-select-open`) → **Create Image** →
`div.image-model-selector-button` → **Qwen-Image 3.0** → `div.size-selector` → **1:1** →
`textarea.message-input-textarea` → `button.send-button` → tunggu gambar → simpan PNG.
