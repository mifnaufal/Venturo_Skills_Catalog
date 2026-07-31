# Session: Otomasi poster Qwen via Playwright

**Created:** 2026-07-31 09:59:48

---

## Conversation

### 🤖 Assistant
*2026-07-31 10:00:00*

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

Dipakai saat user minta poster paket Venturo (Starter / Growth / Enterprise). **Ambil isi/prompt material dari `packages_context.md` saja — JANGAN ikuti workflow `VENTURO.md`** (itu milik skill `venturo-poster` yang render via canvas-design 1048×1048; kita tetap pakai alur Qwen 1:1).

1. Baca `packages_context.md` di project root. Jika file hilang → refuse dan beri tahu user.
2. Tanya pertanyaan valid (preset Venturo):
   - **Tier**: Starter / Growth / Enterprise (default: **Starter**)
   - **CTA**: "Konsultasi Gratis" (`#10B981`) atau "Hubungi Kami" (`#F59E0B`) — untuk Enterprise default CTA Gold
   - **Gaya/arah visual tambahan** (opsional): mis. mood, aksen, layout
3. Susun prompt dari data tier (`Ideal untuk`, `Budget Proyek`, `Dedicated Team`) verbatim + tabel `Color Palette Reference` (hex) + headline `PAKET STARTER` / `PAKET GROWTH` / `PAKET ENTERPRISE` + CTA yang dipilih + jawaban gaya.
4. Jalankan `generate --prompt "<prompt>"`. Rasio tetap 1:1.
5. Satu tier per eksekusi — jika user minta tier lain, ulangi workflow.

Contoh shape prompt (draf; isi mengikuti jawaban user & data tier dari file):

```
Design a premium Indonesian service-package poster, square 1:1.
Headline (dominant): "PAKET STARTER".
Ideal untuk: <isi dari packages_context.md>
Budget Proyek: <isi>
Dedicated Team: <isi>
Brand colors: Primary Teal #006D79, Primary Light #009BAD,
Light BG #FFFFFF, Subtle BG #F4F8F8, Body #374151, CTA Green #10B981.
CTA button: "Konsultasi Gratis".
Style: clean, modern, teal-themed, Z-pattern, generous whitespace.
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


Base directory for this skill: /home/alxyz/Downloads/Project/2/Venturo_Skills_Catalog/.claude/skills/qwen-poster
Relative paths in this skill (e.g., scripts/, references/) are relative to this base directory.

### 🤖 Assistant
*2026-07-31 10:00:00*

*[step-start part]*

💭 **Reasoning:**

<details>
<summary>Click to expand reasoning</summary>

The user is asking about a Qwen Poster skill for generating promotional posters via chat.qwen.ai. They've given me the skill instructions. The task appears to be about generating a poster promo for Venturo packages.

The skill says this is the qwen-poster skill. The user message just contains the skill content. Let me understand what the user wants. Actually, the message seems to be just the skill content being loaded — but wait, there's no actual user request yet beyond the skill. Let me look at what's being asked.

Actually, the human turn contains the skill content. There's no explicit question. The user probably wants me to generate a poster. Let me check the context — the working directory is /home/alxyz/Downloads/Project/2/Venturo_Skills_Catalog.

Wait, the human message only contains the skill content without a specific request. Hmm. But per the skill workflow, I should check if there's a request. The message might be truncated or the user's actual request is missing. 

Actually, looking at this more carefully - the entire "human" message is the skill content for qwen-poster. This could be the user asking me to do something with this skill, or just providing it. Since there's no explicit task, I should ask the user what they want.

But wait - the skill says "Trigger whenever the user mentions 'deck,' 'slides,'..." no that's pptx. For qwen-poster, the trigger is when user wants to generate promotional poster images via Qwen AI chat.

The human message contains only the skill content. There's no actual user request. I should ask the user what they'd like to do. However, the instructions say to be proactive but not surprising.

Actually, since this is the qwen-poster skill content being presented as the user message, and the user hasn't given a specific request, I should ask what poster they want. But the instructions say I shouldn't be too verbose.

Hmm, but maybe the user intends for me to acknowledge the skill is loaded and ask what they want. Let me ask concisely what poster they want to generate, using the question tool maybe.

Actually, let me re-read. The system reminder says the skill is already loaded. The human message is just the skill. There's no task. The most reasonable response is to ask the user what poster they'd like to create. Let me use the question tool to clarify.

Let me first check if the project has the necessary files - packages_context.md, the script, etc. Actually, let me just ask what they want first, since no request was given. But maybe I can be helpful by checking the state of the project.

Given the ambiguity, I'll ask the user what they want to do. Keep it short.

</details>

The qwen-poster skill is loaded. What would you like to do? For example, generate a Venturo package poster (Starter/Growth/Enterprise) or a free-form promo poster. I'll need the promo details (title, event, date, venue, CTA, style) or the Venturo tier to get started.

*[step-finish part]*
