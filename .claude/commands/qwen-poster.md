---
description: Buat poster paket Venturo via Qwen AI (login → paket → deskripsi → generate).
allowed-tools: Bash, Read
---

Baca skill `qwen-poster`: `.claude/skills/qwen-poster/SKILL.md` lalu ikuti workflow **PERTANYAAN WAJIB** di dalamnya PERSIS, mulai dari pesan pertama ini. JANGAN tanya "mau bantuan apa?", "poster apa yang mau dibuat?", atau mengulang daftar perintah.

1. **Langkah 0 — Cek login**: jalankan `ls .qwen-profile/storage-state.json`. Jika file tidak ada → tanya user: "Belum login. Mau login sekarang?" Jika setuju → jalankan `node .claude/skills/qwen-poster/scripts/qwen-poster.mjs login` (user login manual di jendela browser, tekan Enter), tunggu selesai, lalu lanjut. Jika file ada → katakan "Login terdeteksi ✓" → lanjut.
2. **Langkah 1 — Tanya paket**: A. Starter / B. Growth / C. Enterprise (default: Starter).
3. **Langkah 2 — Tanya deskripsi**: tampilkan SEMUA 13 opsi (jangan diringkas jadi 2–3). Pilihan terakhir: Kustom (ketik sendiri).
4. Setelah kedua jawaban terkumpul: baca `pure_context.md` + `theme_context.md`, susun prompt, jalankan `node .claude/skills/qwen-poster/scripts/qwen-poster.mjs generate --prompt "<prompt>"`.

Satu tier per eksekusi. Jangan generate sebelum kedua jawaban (paket + deskripsi) terkumpul.
