---
name: venturo-opencode
description: "Gunakan OpenCode CLI untuk tugas marketing, dokumentasi, dan paket layanan Venturo (venturo.id)."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [OpenCode, Venturo, Marketing, Documentation, Service-Packages, AI-Coding-Agent]
    related_skills: [venturo-poster, venturo-claude-code, venturo-hermes-agent]
---

# Venturo — OpenCode Skill Guide (v2.1)

Gunakan **OpenCode** untuk tugas marketing Venturo: generate poster iklan HD, dokumentasi paket layanan, dan konten promosi.

**HD Poster Rule:** Semua poster di-render di **2048×2048px** container dengan **Device Scale Factor 2** → output **4096×4096px** (super tajam, scalable ke 1024px tanpa pecah).

Reference file: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/packages_context.md`

Opsi konten poster: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/opsi-poster.md` — 4 format konten berbeda (Opsi 1-4)

---

## Trigger Behavior — WAJIB INTERAKTIF

Ketika skill ini dimuat, **LANGSUNG MULAI Q&A**. Jangan diam — tanya user step by step.

**Aturan Bertanya:**
1. Tanya **1 pertanyaan dulu**, tunggu jawaban user
2. Baru lanjut pertanyaan berikutnya
3. Jangan tanya semua sekaligus
4. Jangan generate apapun sebelum user jawab semua

**Flow Wajib:**
- Tanya tier dulu (Starter/Growth/Enterprise/All)
- Tanya konten (Masalah/Solusi/Hasil/Paket Details)
- Tanya custom messaging (ada yg diubah atau pakai default?)
- Konfirmasi sebelum eksekusi

---

## CRITICAL: One-Shot Mode (Prefered) — Task Satu Kali

Cocok untuk task terukur cepat, satukali execute, tanpa interaktif:

```
terminal(command="opencode run 'Buat dokumentasi Paket Growth dari packages_context.md dalam format Markdown table'", workdir="/path/to/venturo-project", timeout=90)
```

Bisa dengan file context:

```
terminal(command="opencode run 'Review packages_context.md dan sarankan perbaikan dokumentasi' -f packages_context.md --thinking")
```

Atau force model spesifik:

```
terminal(command="opencode run 'Generate Dokumentasi Paket Enterprise dengan tabel komposisi tim dan timeline' --model openrouter/anthropic/claude-sonnet-4", workdir="/path/to/venturo-project")
```

### JSON Output

Ambil output mesin-readable:

```
terminal(command="cat packages_context.md | opencode run 'Ekstrak info semua paket ke format JSON' --format json", workdir="/path/to/venturo-project")
```

---

## Mode Interaktif (Background TUI) — Multi-Turn Session

Pakai background mode kalau butuh iterative banyak putaran:

```
# Start OpenCode in background
terminal(command="opencode", workdir="/path/to/venturo-project", background=true, pty=true)
# Returns session_id, misalnya ses_abc123

# Kirim task pertama
process(action="submit", session_id="ses_abc123", data="Baca packages_context.md dan buat rangkuman paket-paket Venturo dalam format table")

# Cek progress
process(action="poll", session_id="ses_abc123")
process(action="log", session_id="ses_abc123", limit=50)

# Lanjutkan task berikutnya
process(action="submit", session_id="ses_abc123", data="Ekstrak data komposisi tim dan timeline dari setiap tier format tabel perbandingan")

# Exit benar-benar — JANGAN PAKAI /exit!
process(action="write", session_id="ses_abc123", data="\x03")
# Atau kill: process(action="kill", session_id="ses_abc123")
```

**PENTING:** `/exit` bukanlah perintah valid di OpenCode — akan membuka dialog pemilihan agen. Gunakan Ctrl+C (`\x03`) atau `kill` saja.

---

## Interactive Workflow (WAJIB PAKAI INI)

### Flow A: Poster Iklan (HD — 4096×4096px output)
1. **Tanya tier** → Starter / Growth / Enterprise / All
2. **Tanya konten** → Masalah? Solusi? Hasil? Paket Details? (default: semua)
3. **Tanya illustrasi** → User minta gaya tertentu? Biarin AI tentuin?
4. **Tanya custom** → Ada copy yg diubah? Atau pakai default?
5. **Generate** → Eksekusi poster via Playwright (viewport 2048×2048, DSF 2)

### Flow B: Dokumentasi
1. **Tanya tujuan** → Dokumentasi internal atau client-facing?
2. **Tanya format** → Markdown table, PDF, atau apa?
3. **Generate** → Eksekusi dokumentasi

---

## Complete Playwright Integration — Generate Poster via OpenCode

Membuat poster 1024x1024px PNG langsung dari OpenCode via Playwright MCP:

```
terminal(command="opencode run '''
Membuat poster Venturo Starter via Playwright:
1. Buat HTML file dengan struktur doodle-block style
2. Gunakan font Inter dari Google Fonts
3. Embed logo dari image.png base64
4. Render ke PNG 1024x1024px
5. Simpan di /tmp/venturo-starter.png
''' --max-turns 20", workdir="/home/alxyz/Downloads/Project/Venturo_Skills_Catalog", timeout=180)
```

---

## Multi-Agent Pattern: Claude Code + OpenCode Cooperating

Workflow hybrid di mana Claude Code + OpenCode bekerja sama:

```
# Phase 1: Claude Code review docs & generate structure
terminal(command="claude -p 'Review packages_context.md, generate JSON structure untuk poster Enterprise' --max-turns 5 --output-format json")

# Phase 2: OpenCode render berdasarkan JSON structure
terminal(command="opencode run 'Render poster Enterprise dari JSON structure di fase 1' --model openrouter/anthropic/claude-sonnet-4")

# Phase 3: Claude Code validate output
terminal(command="claude -p 'Validate venturo-enterprise.png: pastikan ukuran 1024x1024, warna #006D79 ada, text legible' --max-turns 3")
```

Alternative: Parallel execution for independent tasks:

```
# Task 1: Generate starter poster via Claude
terminal(command="claude -p 'Generate poster starter PNG 1024x1024' --max-turns 15 &")

# Task 2: Generate growth poster via OpenCode
terminal(command="opencode run 'Generate growth poster PNG 1024x1024' --max-turns 15 &")

# Wait both
sleep 30
ls -la /home/alxyz/Downloads/Project/Venturo_Skills_Catalog/*.png
```

---

## Flags Penting (OpenCode v1.x+)

| Flag | Digunakan Untuk |
|------|----------------|
| `run 'prompt'` | Satu eksekusi dan exit |
| `--continue / -c` | Lanjut sesi terakhir OpenCode |
| `--session <id>` / `-s` | Lanjut sesi tertentu |
| `--agent <name>` | Pilih agen (build atau plan) |
| `--model provider/model` | Pakai model spesifik |
| `--format json` | Output mesin-readbale |
| `--file <path>` / `-f` | Lampirkan file |
| `--thinking` | Tampilkan thinking blocks model |
| `--variant <level>` | Tingkat reasoning (high, max, minimal) |
| `--title <name>` | Namai sesi |

---

## Environment Variables

| Variable | Fungsi |
|----------|--------|
| `OPENROUTER_API_KEY` | Auth lewat OpenRouter |
| `ANTHROPIC_API_KEY` | Alternatif auth kalau perlu |
| `VENTURO_WORKDIR` | Path default project Venturo (opsional) |
| `VENTURO_POSTER_DIR` | Output directory untuk poster (default: ./) |

---

## Checklist Usage

1. Pastikan OpenCode terinstall: `opencode --version` ✓
2. Authentication valid: `opencode auth list` ✓
3. Workdir benar (project Venturo) ✓
4. Pakai `opencode run` buat task cepat, background mode buat interaktif ✓
5. Sesuaikan session ID di `process()` saat mode interaktif ✓
6. Setelah selesai, beri ringkasan hasil ke user ✓

---

## Error Handling & Fallback Logic

**Jika OpenCode command gagal:**

1. **Retry dengan model berbeda**: Ganti dari `sonnet` ke `haiku` atau lain
   ```
   terminal(command="opencode run 'retry task' --model openrouter/anthropic/claude-haiku")
   ```

2. **Fallback ke Claude Code**: Kalau OpenCode error, coba Claude Code
   ```
   terminal(command="claude -p 'task yang sama' --max-turns 5")
   ```

3. **One-shot vs Interactive**: Kalau interactive mode stuck, pindah ke one-shot
   ```
   # Dari interactive ke one-shot
   terminal(command="opencode run 'task'")
   ```

4. **Verify resource availability**: Pastikan packages_context.md tersedia
   ```
   test -f packages_context.md || echo "File tidak ada!"
   ```

---

## Verification (Smoke Test)

```
terminal(command="opencode run 'Verify: OPENCODE_VENTURO_OK'")
```

Success criteria: Output mengandung `OPENCODE_VENTURO_OK`, command exit without error.

**Poster Generation Verification:**
```bash
# Validate PNG dimensions
file venturo-*.png  # Should say "PNG 1024 x 1024"
# Check color presence
grep -c "#006D79" venturo-growth.html > /dev/null && echo "Primary teal found" || echo "Missing primary color"
```

---

## Pitfall & Solusi

- **TUI butuh `pty=true`** → Kalau pake background mode, wajib set `pty=true`
- **PATH salah binaries OpenCode** → Cek dengan `which -a opencode`, atau pin explicit path (`$HOME/.opencode/bin/opencode run...`)
- **Mode interaktif ngangguk** → Use `process(action="poll")` dulu lihat status
- **Muncul dialog信任** → Handle via tmux send-keys kalau interaktif
- **Session tak bertahan** → Pastikan workdir sama waktu resume
- **OpenCode server tidak merespons** → Kill session dengan `process(action="kill")` lalu restart

---

## What NOT to Do

- **Do NOT** generate poster without completing the Q&A flow first
- **Do NOT** use `/exit` to close TUI — it opens agent selector! Use Ctrl+C instead.
- **Do NOT** forget `pty=true` for interactive sessions
- **Do NOT** share one working directory across parallel OpenCode sessions
- **Do NOT** forget to press Enter twice in TUI (once to finalize, once to send)

---

### Poster Design Rules (WAJIB saat generate poster)
- **Do NOT** skip illustrasi SVG/p5.js — setiap poster WAJIB punya vector elements di background
- **Do NOT** lupa CTA button "Konsultasi Gratis" di kanan-bawah, pake accent color `#10B981`
- **Do NOT** buat illustrasi compete dengan tier name 224px — taruh di z-index 0, opacity max 0.15
- **Do NOT** leave EMPTY GAPS — canvas 2048×2048 WAJIB 100% full
- **Do NOT** pake gap terlalu longgar — gap antar section **24–32px** aja
- **Do NOT** kasih checkmark cuma 3-4 — minimal 8, tambah dari default set kalo perlu
- **Do NOT** pakai warna lebih dari 4: background, primary, secondary, CTA accent

**Catatan:** Skill ini bekerja sama dengan `venturo-poster`, `venturo-claude-code`, dan `venturo-hermes-agent` di katalog Venturo. Semua skill mengacu pada `packages_context.md` sebagai sumber data tunggal. Siap dipakai via Hermes Agent, Claude Code MCP, atau OpenCode CLI.
