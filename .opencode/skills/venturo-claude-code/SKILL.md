---
name: venturo-claude-code
description: "Gunakan Claude Code CLI untuk tugas marketing, dokumentasi, dan paket layanan Venturo (venturo.id)."
version: 2.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Claude, Venturo, Marketing, Documentation, Service-Packages, AI-Coding-Agent]
    related_skills: [venturo-poster, venturo-opencode, venturo-hermes-agent]
---

# Venturo — Claude Code Skill Guide (v2.1)

Gunakan **Claude Code** untuk tugas Venturo: generate poster HD, dokumentasi, dan konten marketing.

**HD Rule:** Container **2048×2048px** + Device Scale Factor 2 → output **4096×4096px**. Semua font/padding/spacing di-double.

Reference file: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/packages_context.md`

Style reference: `/home/alxyz/Downloads/Project/Venturo_Skills_Catalog/image.png` (logo Venturo)

---

## Trigger Behavior

Ketika skill ini dimuat via `skill_view()` atau Claude Code MCP, **langsung mulai flow Q&A di bawah**. Jangan pernah generate poster atau dokumentasi sampai user menjawab pertanyaan penting. Jangan asumsi pilihan tier atau preferensi konten.

---

## CRITICAL: Print Mode (Prefered) — Task Satu Kali

Cocok untuk task terukur cepat, satukali execute, tanpa interaktif:

```
terminal(command="claude -p 'Buat dokumentasi Paket Growth dari packages_context.md dalam format Markdown table' --max-turns 8", workdir="/path/to/venturo-project", timeout=120)
```

Bisa pipe kontex file:

```
terminal(command="cat packages_context.md | claude -p 'Ringkas Masalah + Solusi + Hasil untuk dokumentasi klien' --max-turns 5")
```

### JSON Output Terstruktur

Ambil data terstruktur via `--json-schema`:

```
terminal(command="cat packages_context.md | claude -p 'Ekstrak semua info paket starter/growth/enterprise ke format JSON' --output-format json --json-schema '{\"type\":\"object\",\"properties\":{\"packages\":{\"type\":\"array\",\"items\":{\"type\":\"object\",\"properties\":{\"tier\":{\"type\":\"string\"},\"budget\":{\"type\":\"string\"},\"team\":{\"type\":\"array\"}}}},\"required\":[\"packages\"]}' --max-turns 10", workdir="/path/to/venturo-project")
```

Output akan punya field `session_id`, `num_turns`, `total_cost_usd` untuk tracking.

---

## Mode Interaktif (Tmux) — Multi-Turn Session

Pakai tmux kalau butuh iterative banyak putaran:

```
# Start tmux session
terminal(command="tmux new-session -d -s venturo-claude -x 140 -y 40")

# Launch Claude
terminal(command="tmux send-keys -t venturo-claude 'cd /path/to/venturo-project && claude' Enter")

sleep 4

# Handle trust dialog (Enter = Yes default)
tmux send-keys -t venturo-claude Enter

# Send task
tmux send-keys -t venturo-claude 'Review packages_context.md, lalu generate markdown docs untuk Paket Enterprise dengan semua detail tim dan timeline.' Enter

# Monitor progress
tmux capture-pane -t venturo-claude -p -S -50

# Continue iteration
tmux send-keys -t venturo-claude 'Tambahkan section custom messaging untuk banner utama' Enter

# Clean up
tmux kill-session -t venturo-claude
```

---

## Task Spesifik Venturo (Trigger Flow Style)

### Step 1: Pilih Tier

```
terminal(command="claude -p 'Generate poster starter HD 2048x2048 + DSF 2 (4096x4096 output) dengan palet Venturo (#006D79, #009BAD) via Playwright' --max-turns 15")
```

### Step 2: Pilih Content Sections

Default: Masalah + Solusi + Hasil + Paket Details (jika user tidak spesifikasi).

### Step 3: Custom Messaging (Opsional)

Atau minta user modifikasi wording, tagline, tambahkan/remove item.

---

## Complete Playwright Integration — Generate Poster HD via Claude Code

Membuat poster **4096×4096px HD** langsung dari Claude Code via Playwright MCP:

```
terminal(command="claude -p '''
Membuat poster Venturo Starter HD via Playwright:
1. Container 2048x2048px (double size untuk HD)
2. Semua ukuran font/padding di-double
3. Gunakan font Inter dari Google Fonts
4. Embed logo dari image.png base64
5. SVG illustrations (circle, path, polygon) di background
6. Opsional: p5.js efek generatif (noise wave, random dots)
7. Render DSF 2 → output 4096x4096px
8. Simpan di /tmp/venturo-starter.png
''' --max-turns 20", workdir="/home/alxyz/Downloads/Project/Venturo_Skills_Catalog", timeout=180)
```

Or with explicit Playwright commands (HD version):

```
# Via Playwright browser automation (HD)
mcp__playwright__browser_navigate(url="about:blank")
mcp__playwright__browser_resize(width=2048, height=2048)
mcp__playwright__browser_evaluate(function="(page) => { page.setContent('<html>...</html>'); }")
mcp__playwright__browser_wait_for(time=3)
mcp__playwright__browser_take_screenshot(type="png", scale="device", filename="venturo-starter.png")
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
terminal(command="claude -p 'Validate venturo-enterprise.png: pastikan ukuran 4096x4096 (HD), warna #006D79 ada, text legible, illustrasi SVG/p5.js ada' --max-turns 3")
```

Alternative: Parallel execution for independent tasks:

```
# Task 1: Generate starter poster HD via Claude
terminal(command="claude -p 'Generate poster starter HD 2048x2048 + DSF 2' --max-turns 15 &")

# Task 2: Generate growth poster HD via OpenCode
terminal(command="opencode run 'Generate growth poster HD 2048x2048 + DSF 2' --max-turns 15 &")

# Wait both
sleep 30
ls -la /home/alxyz/Downloads/Project/Venturo_Skills_Catalog/*.png
```

---

## Flags Penting (Claude Code v2.x+)

| Flag | Digunakan Untuk |
|------|----------------|
| `-p 'task'` | Print mode, non-interaktif, cepat |
| `--max-turns N` | Batasi putaran |
| `--model sonnet/opus/haiku` | Pilih model spesifik |
| `--allowedTools Read,Bash,Browser` | Batas hak akses tool |
| `--dangerously-skip-permissions` | Lewat permission prompt (hati-hati!) |
| `--from-pr 42` | Resume sesi tied PR GitHub |
| `--fallback-model haiku` | Auto fallback kalau model overload |
| `--bare` | Skip hooks/plugins, tercepat untuk CI |
| `--settings <file>` | Load settings JSON inline |

---

## Environment Variables

| Variable | Fungsi |
|----------|--------|
| `ANTHROPIC_API_KEY` | Auth alternatif jika OAuth gagal |
| `CLAUDE_CODE_EFFORT_LEVEL` | Default effort (low/medium/high/xhigh/max) |
| `VENTURO_WORKDIR` | Path default project Venturo (opsional) |
| `VENTURO_POSTER_DIR` | Output directory untuk poster (default: ./) |

---

## Checklist Usage

1. Pastikan Claude Code terinstall: `claude --version` ✓
2. Authentication valid: `claude auth status` ✓
3. Workdir benar (project Venturo) ✓
4. Gunakan `-p` buat task singkat, tmux buat interaktif ✓
5. Set `--max-turns` agar ga over budget ✓
6. Setelah selesai, beri ringkasan hasil ke user ✓

---

## Error Handling & Fallback Logic

**Jika Claude Code command gagal:**

1. **Retry dengan model berbeda**: Ganti dari `opus` ke `sonnet` atau `haiku`
   ```
   terminal(command="claude -p 'retry task' --model haiku --max-turns 5")
   ```

2. **Fallback ke OpenCode**: Kalau Claude Code error, coba OpenCode
   ```
   terminal(command="opencode run 'task yang sama'")
   ```

3. **Print mode vs Interactive**: Kalau interactive mode dialog muncul, pindah ke print mode
   ```
   # Dari interactive ke print
   terminal(command="claude -p 'task' --max-turns 5")
   ```

4. **Verify resource availability**: Pastikan packages_context.md tersedia
   ```
   test -f packages_context.md || echo "File tidak ada!"
   ```

---

## Verification (Smoke Test)

```
terminal(command="claude -p 'Verify: CLAUDE_VENTURO_OK' --max-turns 2")
```

Success criteria: Output mengandung `CLAUDE_VENTURO_OK`, command exit without error.

**Poster Generation Verification:**
```bash
# Validate PNG dimensions (HD — DSF 2 x 2048 viewport = 4096)
file venturo-*.png  # Should say "PNG 4096 x 4096"
identify venturo-*.png | awk '{print $3}'  # Alternative: should output "4096x4096"
# Check color presence
grep -c "#006D79" venturo-starter.html > /dev/null && echo "Primary teal found" || echo "Missing primary color"
```

---

## Pitfall & Solusi

- **Trust dialog pertama kali** → Press Enter (default Yes) atau pakai `--dangerously-skip-permissions`
- **Workspace error** → First-time only; after accepted, cached for that directory
- **Performance lambat** → Coba `--model haiku` untuk task sederhana
- **Modal dialog muncul di interactive mode** → Pakai print mode (`-p`) kalau bisa
- **Session tidak persisten** → Pastikan workdir sama saat resume
- **Playwright not available** → Alternatif pake headless browser via Puppeteer/Chromium
- **Image not found** → Make sure image.path exists and is readable

---

## What NOT to Do

- **Do NOT** generate poster without completing the Q&A flow first
- **Do NOT** use 1024×1024 container — always **2048×2048** (HD)
- **Do NOT** lupa double semua ukuran font, padding, spacing
- **Do NOT** skip illustrasi SVG/p5.js — setiap poster WAJIB punya vector elements
- **Do NOT** use wrong font family — always use Inter
- **Do NOT** clip text at 2048×2048 boundary — all content must fit
- **Do NOT** use JPEG — always PNG for crisp text

---

**Catatan:** Skill ini bekerja sama dengan `venturo-poster`, `venturo-opencode`, dan `venturo-hermes-agent` di katalog Venturo. Semua skill mengacu pada `packages_context.md` sebagai sumber data tunggal. Siap dipakai via Hermes Agent, Claude Code MCP, atau OpenCode.
