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
