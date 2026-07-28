# Venturo Skills Catalog

Kumpulan skill untuk **Claude Code** dan **OpenCode** — AI coding agents — untuk membuat materi marketing dan katalog layanan **Venturo** (venturo.id).

## Isi

### [`skills/venturo-poster`](./skills/venturo-poster/SKILL.md)

Skill untuk generate poster paket layanan Venturo berformat **PNG 1024×1024px** via Playwright. Mendukung tiga tier:

- **Starter** — Rp20 Juta – Rp80 Juta, untuk UMKM & startup
- **Growth** — Rp80 Juta – Rp250 Juta, untuk perusahaan yang butuh sistem custom
- **Enterprise** — Mulai Rp250 Juta, untuk sistem skala besar & transformasi digital

Style desain: **doodle-block** (teal color blocks, dotted dividers, dashed-outline cards, ilustrasi ikon, layout left-aligned). Mengikuti palet warna brand Venturo (`#006D79`, `#009BAD`, `#0A1B1F`).

Satu poster = satu tier. Kalau minta "ketiganya", di-render jadi tiga file terpisah:
`venturo-starter.png`, `venturo-growth.png`, `venturo-enterprise.png`.

## Referensi Konten

[`packages_context.md`](./packages_context.md) — copy paket layanan, deskripsi tier, rentang budget, komposisi tim, timeline, palet warna, dan design specs lengkap.

## Penggunaan

Panggil skill-nya lewat Claude Code atau OpenCode, lalu ikuti Q&A flow di SKILL.md:

1. Pilih tier (Starter / Growth / Enterprise / All Three)
2. Pilih section konten (Masalah, Solusi, Hasil, Paket Details, Custom)
3. Optional: custom messaging
4. Skill render poster via Playwright → output PNG

## Repository

Single-purpose: berisi skill file + reference data, tanpa build step. Clone langsung, buka dengan AI coding agent, panggil skill-nya.

OpenCode akan auto-discover skill dari `.opencode/skills/` atau `.claude/skills/`.