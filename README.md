# Venturo Skills Catalog

Kumpulan skill untuk **Claude Code**, **OpenCode**, dan **Hermes Agent** — AI coding agents — untuk membuat materi marketing dan katalog layanan **Venturo** (venturo.id).

---

## Skills

Semua skill bodies tersimpan di [`skills/`](./skills/) sebagai **single source of truth**. Baik Claude Code maupun OpenCode auto-discover lewat symlink ke folder yang sama, jadi **edit cukup di satu tempat**.

### Marketing & Visual

| Skill | Tujuan |
|-------|--------|
| [`venturo-poster`](./skills/venturo-poster/SKILL.md) | Generate poster HD **4096×4096px** untuk paket layanan Venturo (Starter / Growth / Enterprise) via Playwright. SVG + p5.js generative effects. |
| [`venturo-claude-code`](./skills/venturo-claude-code/SKILL.md) | Marketing & dokumentasi untuk Venturo via Claude Code CLI. |
| [`venturo-opencode`](./skills/venturo-opencode/SKILL.md) | Marketing & dokumentasi untuk Venturo via OpenCode CLI. |

### Context & Authoring

| Skill | Tujuan |
|-------|--------|
| [`venturo-claude-context`](./skills/venturo-claude-context/SKILL.md) | Project context & guidelines untuk kerja dengan Venturo di Claude Code. |
| [`venturo-hermes-agent`](./skills/venturo-hermes-agent/SKILL.md) | Manage Claude Code & OpenCode skills (create / patch / delete / batch validate) via Hermes Agent CLI. |

---

## Struktur Repository

```
skills/                                      ← single source of truth (5 SKILL.md)
├── venturo-poster/SKILL.md
├── venturo-claude-code/SKILL.md
├── venturo-claude-context/SKILL.md
├── venturo-hermes-agent/SKILL.md            (v2.0: Create / Patch / Delete / Batch Validate)
└── venturo-opencode/SKILL.md

.claude/skills/                              ← Claude Code discovery
├── venturo-poster           -> ../../skills/venturo-poster
├── venturo-claude-code      -> ../../skills/venturo-claude-code
├── venturo-claude-context   -> ../../skills/venturo-claude-context
├── venturo-hermes-agent     -> ../../skills/venturo-hermes-agent
└── venturo-opencode         -> ../../skills/venturo-opencode

.opencode/skills/                            ← OpenCode discovery (sama, plus tooling)
├── venturo-poster           -> ../../skills/venturo-poster
├── venturo-claude-code      -> ../../skills/venturo-claude-code
├── venturo-claude-context   -> ../../skills/venturo-claude-context
├── venturo-hermes-agent     -> ../../skills/venturo-hermes-agent
└── venturo-opencode/                        ← real dir (memuat tooling artifacts)
    ├── SKILL.md -> ../../skills/venturo-opencode/SKILL.md
    ├── .playwright-mcp/                     ← Playwright cache (gitignored)
    └── conversations/                       ← session logs
```

**Edit cukup di `skills/<name>/SKILL.md`** — kedua harnesses otomatis ikut ter-update via symlink.

### Kenapa symlink, bukan copy?

- **Satu sumber kebenaran** — perubahan isi skill langsung sampai ke Claude Code & OpenCode.
- **Zero drift** — tidak ada lagi skill body yang outdated karena lupa update.
- **Git-trackable** — symlink tersimpan sebagai `mode 120000` blob; portable antar clone.

> **Catatan Windows**: symlink butuh Developer Mode atau admin. Fallback: `cp -r skills/<name> .claude/skills/` atau `.opencode/skills/`.

---

## Service Packages (Poster Skill)

Skill [`venturo-poster`](./skills/venturo-poster/SKILL.md) generate poster HD untuk tiga tier Venturo:

| Tier | Budget | Target |
|------|--------|--------|
| **Starter** | Rp20 Juta – Rp80 Juta | UMKM, usaha mikro, perusahaan kecil, startup |
| **Growth** | Rp80 Juta – Rp250 Juta | Perusahaan berkembang (ERP, CRM, HRIS, Finance, Inventory, WMS) |
| **Enterprise** | Mulai Rp250 Juta | Perusahaan menengah hingga enterprise |

Style: **"rame tapi simple"** — dense tapi hierarkis. SVG (`circle`, `path`, `polygon`, `pattern`) + p5.js (`noise wave`, `random dots`, `particle`) + dot grid + gradient overlay.

Satu poster = satu tier. Minta "ketiganya" → render tiga file terpisah: `venturo-starter.png`, `venturo-growth.png`, `venturo-{tier}.png`.

### Flow Penggunaan

1. Pilih tier — Starter / Growth / Enterprise / All Three.
2. Pilih section konten — Masalah, Solusi, Hasil, Paket Details, Custom.
3. Optional: custom messaging.
4. Skill render poster via Playwright → output PNG **4096×4096px**.

---

## Tutorial

Panduan cepat untuk tiga alur umum. Tidak perlu copy skill ke folder config — symlink di `.claude/skills/` dan `.opencode/skills/` sudah cukup untuk auto-discovery.

### Prasyarat

- Repo sudah ter-clone dan kamu berada di root project.
- Salah satu: **Claude Code** (`claude` CLI) **atau** **OpenCode** (`opencode` CLI). Hermes Agent optional (untuk authoring).
- Linux/macOS (symlink native). Windows: aktifkan Developer Mode, atau lihat fallback di "Development Notes".

```bash
# Verifikasi symlink hidup
ls -la .claude/skills/ .opencode/skills/
# Output: semua entry adalah symlink (-> ../../skills/...), tidak ada file real kecuali dir kosong.
```

---

### Tutorial 1 — Generate poster (Starter / Growth / Enterprise)

Lewat **Claude Code**:

```bash
claude
```

Di prompt:

```
/venturo-poster
```

Skill akan Q&A satu per satu:

```
Q: Mau poster buat tier mana?
A: Starter

Q: Konten apa aja yang pengen ditampilin?
A: Masalah, Solusi, Paket Details  (atau "all")

Q: Ada copy yang diganti? Atau aman pake default?
A: Default aja
```

Skill render via Playwright → file PNG **4096×4096px**:

- `venturo-starter.png`
- `venturo-growth.png`
- `venturo-enterprise.png`

Minta "ketiganya" → tiga file di-render terpisah.

Lewat **OpenCode**:

```bash
opencode
```

```
> /venturo-poster
# Q&A flow sama, output identik.
```

> Output ada di working directory. Untuk save ke subfolder: jawab `Q: Simpan di mana? (default: cwd)` → ketik `./posters/`.

---

### Tutorial 2 — Pakai Venturo context di project baru

Skill [`venturo-claude-context`](./skills/venturo-claude-context/SKILL.md) membawa konteks brand, palet warna, dan copy paket ke session — supaya tiap prompt baru tidak perlu paste ulang.

**Cara invoke:**

- **Otomatis (recommended)** — Claude Code match berdasarkan deskripsi skill. Cukup ketik seperti: *"bikin tweet untuk paket Growth Venturo"* atau *"tulis caption Instagram untuk Starter"*.
- **Manual** — di prompt:
  ```
  > /venturo-claude-context
  > Tulis caption LinkedIn untuk paket Growth.
  ```

Skill menambahkan konteks brand (tone, palet, layout, terminology) di belakang layar, lalu menulis output sesuai brief.

**Verifikasi dia loaded:**

```bash
claude --list-skills | grep venturo
# Harus muncul 5: venturo-poster, venturo-claude-code, venturo-claude-context, venturo-hermes-agent, venturo-opencode
```

---

### Tutorial 3 — Bikin skill baru via Hermes Agent

[**`venturo-hermes-agent`**](./skills/venturo-hermes-agent/SKILL.md) ngurusin create / patch / delete / batch validate skill di catalog ini — tanpa kamu harus bikin file manual.

**Step 1** — invoke:

```
/venturo-hermes-agent
```

**Step 2** — pilih action. Contoh flow bikin skill baru:

```
Q: Mau ngapain? [Create / Patch / Delete / Validate]
A: Create

Q: Nama skill?
A: venturo-blog-writer

Q: Deskripsi (untuk trigger matching)?
A: Write blog posts for Venturo service packages matching their brand voice.

Q: Tags?
A: Venturo, blog, marketing, content

Q: Use multi-agent orchestration pattern? [y/n]
A: n

Q: Simpan di mana? [skills/venturo-blog-writer]
A: (enter — default)

Q: Generate symlinks ke .claude/skills/ dan .opencode/skills/? [y/n]
A: y
```

Hermes akan:

1. Bikin `skills/venturo-blog-writer/SKILL.md` dengan frontmatter sesuai.
2. Bikin symlinks di kedua harness roots.
3. Validasi frontmatter (cek `name`, `description`, `version`, valid YAML).
4. Report file yang berubah.

**Step 3** — verifikasi:

```bash
ls -la .claude/skills/venturo-blog-writer .opencode/skills/venturo-blog-writer
# Both should be symlinks -> ../../skills/venturo-blog-writer

md5sum skills/venturo-blog-writer/SKILL.md \
       .claude/skills/venturo-blog-writer/SKILL.md \
       .opencode/skills/venturo-blog-writer/SKILL.md
# Ketiga hash harus sama.
```

**Batch validate semua skill** (opsional, bagus setelah edit banyak):

```
/venturo-hermes-agent
Q: Mau ngapain?
A: Validate
```

Output: daftar skill dengan status (✓ valid / ⚠ missing field / ✗ broken symlink / ⚡ duplicate hash).

---

### Tips Lintas Tutorial

| Masalah | Solusi |
|---------|--------|
| Skill gak nge-trigger pas aku butuh | Cek description di SKILL.md — tambah frasa yang kamu pake. Misal kamu bilang "bikin IG story" tapi description cuma sebut "poster". Tambah `"social story"`. |
| Edit skill, perubahan gak nongol | Pastikan edit di `skills/<nama>/SKILL.md`, bukan di file dalam `.claude/skills/...` (itu symlink, jangan edit). |
| Symlink putus (relokasi repo) | Semua symlink relatif (`../../skills/...`), jadi `git mv` di dalam repo aman. Kalo pindah ke parent folder baru: `git mv` repo + rekreate symlink path-nya. |
| Liat skill yang tersedia | `claude --list-skills` (atau `/skills` di prompt) — harus nongol 5 Venturo skills. |
| Tambah/edit skill manual | Pakai Hermes (`venturo-hermes-agent`) atau lihat "Pengembangan Skill" di bawah. |

---

## Referensi

| File | Fungsi |
|------|--------|
| [`packages_context.md`](./packages_context.md) | Copy paket layanan, deskripsi tier, rentang budget, komposisi tim, timeline, palet warna, design specs. |
| [`image.png`](./image.png) | Logo Venturo — dipakai skill untuk branding. |
| [`opsi-poster.md`](./opsi-poster.md) | 4 format layout alternatif untuk konten poster. |
| [`README.md`](./README.md) | File ini. |

---

## Pengembangan Skill

Tambah skill baru:

1. Bikin folder di `skills/<skill-name>/SKILL.md` dengan frontmatter `name`, `description`, `version`.
2. Buat symlink di `.claude/skills/<skill-name> -> ../../skills/<skill-name>`.
3. Buat symlink di `.opencode/skills/<skill-name> -> ../../skills/<skill-name>`.
4. Test trigger di kedua harnesses.

Atau pakai [`venturo-hermes-agent`](./skills/venturo-hermes-agent/SKILL.md) untuk automate steps 1–4 via Hermes CLI.

---

## Development Notes

- **No build step** — `git clone`, buka dengan AI coding agent, panggil skill-nya.
- **git-tracked symlinks**: didaftarkan sebagai `mode 120000`. Saat clone, symlinks tersimpan utuh.
- **Tooling artifacts** (`.playwright-mcp/`, `conversations/`) di-gitignore — tidak ikut commit.
- **Linux/macOS supported out of the box**. Windows: enable Developer Mode untuk symlink support.
