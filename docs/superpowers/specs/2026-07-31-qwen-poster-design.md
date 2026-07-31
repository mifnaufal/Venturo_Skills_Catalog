# Design: Skill qwen-poster (Qwen AI Poster Generation via Playwright)

Tanggal: 2026-07-31
Status: Implemented

## Ringkasan

Skill Claude/opencode untuk mengotomasi `chat.qwen.ai` (Qwen Chat web) memakai Playwright
(Node script standalone) dengan tujuan menghasilkan **gambar poster promosi** via mode
Create image (Qwen-Image 3.0, resolusi 1:1), lalu mengunduh PNG-nya ke folder `output/`.

## Konteks & Keputusan (hasil tanya-jawab user)

1. **Target**: chat.qwen.ai (web app), bukan API DashScope.
2. **Mode generate**: user login akun sendiri; alur UI manual yang diikuti:
   klik tombol `+` → pilih **Create image** → mode **Qwen-Image 3.0** → resolusi **1:1**.
   Tidak memilih model tambahan. Jika UI berubah, agent/script pakai `detect` untuk
   menemukan selector baru.
3. **Login**: user punya akun, login manual di session skill (storage state dipersist).
4. **Runtime**: Node script standalone (`playwright` npm), bukan MCP browser.
5. **Prompt**: template promo terstruktur (judul, subjudul, event, tanggal, venue, CTA,
   gaya visual, rasio) — selaras dengan skill poster-design.
6. **Anti-bot**: pendekatan sederhana (persistent profile + navigasi wajar), fallback
   manual saat captcha/challenge. Tanpa stealth plugin.
7. **Dual-platform**: skill disalin ke `.claude/skills/qwen-poster/` dan
   `.opencode/skills/qwen-poster/` — keduanya load otomatis tanpa config.
8. **Integrasi Venturo** (update 2026-07-31): skill mengambil **isi** `pure_context.md`
   (data paket + masalah/solusi/hasil) sebagai konten prompt Qwen untuk poster paket
   Venturo, dan **`theme_context.md`** (tema design: palette + style + typography).
   Tidak mengikuti workflow `VENTURO.md` (canvas-design 1048×1048).
   AI bertanya preset: **paket** (default Starter) + **deskripsi via 13 opsi pendek**
   (dari `pure_context.md`, user pilih nomor/abjad, opsi 13 = kustom) → susun prompt
   (data paket verbatim + Style/Typography verbatim) → `generate --prompt`. Rasio 1:1.
9. **Alur UI asli (hasil rekaman klik 2026-07-31)**: thinking `Auto→Thinking` →
   `div.mode-select-open` → menu **Create Image** → `div.image-model-selector-button`
   → **Qwen-Image 3.0** → `div.size-selector` → **1:1** → `.message-input-textarea`
   → `button.send-button`.

## Arsitektur

```
Venturo_Skills_Catalog/
├── package.json                       # playwright dep, type=module
├── .claude/skills/qwen-poster/        # skill untuk Claude Code
│   ├── SKILL.md                       # instruksi agent
│   └── scripts/
│       ├── qwen-poster.mjs            # subcommand: login | detect | generate
│       ├── selectors.json             # tabel selector (update saat UI berubah)
│       └── prompts.js                 # buildPrompt() template promo
├── .opencode/skills/qwen-poster/      # salinan identik untuk opencode
├── .qwen-profile/                     # persistent browser profile + storage state (auto)
└── output/                            # hasil PNG + debug-screenshot.png
```

## Alur Script

- **login**: launch persistent context → buka chat.qwen.ai → tunggu input chat editable
  (polling 3s, timeout 10 menit; deteksi challenge text → minta selesaikan manual) →
  simpan `storageState.json`.
- **generate**: buka browser → jika belum login, jalankan alur login → `enterImageMode`
  (thinking `Auto→Thinking`; klik `modeButton` `div.mode-select-open` → pilih `menuCreateImage`
  "Create Image"; klik `imageModelButton` → pilih `imageModelOption` "Qwen-Image 3.0";
  klik `sizeSelector` → pilih `sizeOption1to1` "1:1"; tiap langkah gagal → print FAIL +
  arahan `detect`) → isi chat input dengan prompt dari `buildPrompt()` (atau `--prompt`)
  → klik `button.send-button` → `waitForImage` (polling 3s, deteksi img naturalWidth>100,
  jumlah img stabil 2 poll, tunggu `generatingIndicator` hilang, timeout 5 menit) → simpan:
  prefer `fetch(src)` → base64 (menghindari blob CORS), fallback screenshot elemen → tulis
  ke `output/qwen-poster-<ts>.png`.
- **detect**: buka chat.qwen.ai → screenshot ke `output/debug-screenshot.png` → dump
  visible buttons (text/aria/title), inputs (placeholder/aria), 5 img terakhir (src/size).
- **record**: buka browser headed + persistent profile, rekam klik user **setelah login**
  (flag `localStorage.__qrec_active` di-set hanya setelah chat input editable terdeteksi),
  tulis ke `output/click-record.jsonl` — dipakai untuk menangkap alur UI saat berubah.

## Selector (selectors.json)

Berbasis peran/teks, bukan class. Hasil rekaman klik 2026-07-31:

| Fungsi | Selector |
|---|---|
| `thinkingSelector` | `.qwen-select-thinking-label` |
| `thinkingOption` | `div.ant-select-item-option-content:has-text('Thinking')` |
| `modeButton` | `div.mode-select-open` |
| `menuCreateImage` | `div.mode-select-dropdown-item:has-text('Create Image')` |
| `imageModelButton` | `div.image-model-selector-button` |
| `imageModelOption` | `li.ant-dropdown-menu-item:has-text('Qwen-Image 3.0')` |
| `sizeSelector` | `div.size-selector` |
| `sizeOption1to1` | `li.ant-dropdown-menu-item:has-text('1:1')` |
| `chatInput` | `textarea.message-input-textarea` |
| `sendButton` | `button.send-button` |
| `generatingIndicator` | text Generating/绘制中/生成中 |

## Error Handling

| Skenario | Aksi |
|---|---|
| Captcha/challenge | Print peringatan, tunggu user selesaikan manual di browser |
| Selector tidak ketemu | FAIL + sarankan `detect`, update selectors.json, retry |
| Timeout generate (5 mnt) | Throw error, saran: cek UI / jalankan detect |
| Login expired | `waitLoggedIn` gagal → ulangi `login` |
| Dua instance sekaligus | Dilarang (profile browser dipakai bersama) |

## Verifikasi

- `node scripts/qwen-poster.mjs` → help tercetak. ✓
- `node scripts/qwen-poster.mjs detect --headless` → konek ke chat.qwen.ai, dump UI
  berhasil (URL/title/buttons/inputs/images), screenshot tersimpan. ✓
- Alur login + generate penuh membutuhkan user (login manual + interaksi) — belum
  diverifikasi end-to-end, menunggu user menjalankan pertama kali.
