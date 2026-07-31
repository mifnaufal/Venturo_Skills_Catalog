# Dokumentasi Project: Venturo Skill Project

> **Dibangun berdasarkan analisis graph pengetahuan** oleh Graphify (2026-07-30)

---

## 1. Pendahulian

Project ini merupakan sekumpulan dokumen dan definisi skill untuk membangun **poster Paket Pengembangan System Venturo** (Starter, Growth, Enterprise). Poster-produksi ini berformat 1048×1048px dengan palet warna branding konsisten.

### Tujuan
Menyediakan struktur data dan workflow untuk generating poster layanan Venturo yang konsisten secara visual dan konten, dengan memanfaatkan `packages_context.md` sebagai sumber fakta tunggal (single source of truth).

---

## 2. Struktur Direktori

```
Venturo Skill Project/
├── README.md                 → Dokumentasi utama project
├── packages_context.md       → Sumber data paket & palet warna (Single Source of Truth)
├── skills/
│   └── venturo-poster/
│       └── SKILL.md        → Definisi skill untuk generating poster
├── .gitignore              → Direktori yang diabaikan (.playwright-mcp, conversations/, graphify-out/)
└── PROJECT_DOCUMENTATION.md  → Dokumentasi ini
```

---

## 3. Arsitektur Pengetahuan

Analisis graph menunjukkan pola arsitektur **star topology** (bintang) di mana satu dokumen berperan sebagai sentra:

```
                [packages_context.md]
                           │
                   (references • 100% terambil)
                         ╱     ╲
               (Line 9)  ╲      ╱ (Line 13)
                        ▼      ▼
          [SKILL.md]    ──┼──► [README.md]
      (venturo-poster)   │ (Venturo Skill)
```

### Node Utama: God Nodes

| No | Label | Type | Source File | Edges |
|----|-------|------|-------------|-------|
| 1 | Venturo Service Packages Context | Document | packages_context.md | **2** (pusat) |
| 2 | Venturo Skill Project | Document | README.md | 1 |
| 3 | venturo-poster Skill Definition | Code | SKILL.md | 1 |

### Komunitas
- **Venturo Skill Packages** (Cohesion: 0.67) — Semua node termasuk dalam komunitas satu-satunya ini.

### Hubungan yang Ditemukan
- `README.md` merujuk ke `packages_context.md` (baris 13): *"packages_context.md — Contains tier descriptions..."*
- `SKILL.md` merujuk ke `packages_context.md` (baris 9): *"Brand context lives in `packages_context.md`"*

---

## 4. Dokumen Sumber: `packages_context.md`

Ini adalah **dokumen otoritatif** yang menyimpan semua data paket dan palet warna yang digunakan oleh seluruh sistem.

### Masalah yang Sering Terjadi
Perusahaan mengalami berbagai tantangan:
- Aplikasi tidak sesuai proses bisnis
- Fitur langganan belum memadai
- Proses bisnis menyesuaikan aplikasi, bukan sebaliknya
- Keterbatasan kustomisasi
- Kesulitan integrasi dengan sistem lain
- Tampilan kurang user-friendly & tak mencerminkan identitas
- Sistem skalabilitas terbatas saat bisnis tumbuh

### Solusi
Venturo menawarkan:
- Pengembangan website & mobile application (Android & iOS) disesuaikan
- Analisis kebutuhan bisnis
- UI/UX modern, responsif
- Fitur fleksibel sesuai kebutuhan saat ini & masa depan
- Integrasi (ERP, CRM, HRIS, Payment Gateway, WhatsApp, API, sistem existing)
- Dashboard monitoring & reporting
- Sistem aman, scalable, siap berkembang

### Hasil
- Aplikasi sesuai kebutuhan proses bisnis
- Efisiensi operasional meningkat
- Fleksibilitas pengembangan berkelanjutan
- Integrasi data lebih baik
- Pengalaman pengguna lebih baik
- Keputusan didukung data terintegrasi

### Paket Pengembangan System

| Starter | Growth | Enterprise |
|---------|--------|------------|
| **Ideal untuk** UMKM, usaha mikro, perusahaan kecil, startup — kebutuhan website/app sederhana. <br>**Budget:** Rp20 Juta – Rp80 Juta | **Ideal untuk** perusahaan custom (Finance, HRIS, CRM, ERP, Inventory, WMS, Logistic, Sales, Production, Asset). <br>**Budget:** Rp80 Juta – Rp250 Juta | **Ideal untuk** perusahaan menengah–enterprise, skala besar, integrasi lintas sistem, keamanan tinggi, AI, Big Data, transformasi digital menyeluruh. <br>**Budget:** Mulai Rp250 Juta |

#### Tim Dipersembahkan

| Starter | Growth | Enterprise |
|---------|--------|------------|
| • 1 Business Analyst<br>• 1 Senior Software Engineer | • 1 BA<br>• 1 Senior Engineer<br>• 1 UI/UX Designer<br>• 1 QA Engineer | • 1 BA<br>• 1 Senior Engineer<br>• 1 Intermediate Engineer<br>• 1 UI/UX Designer<br>• 1 QA Engineer<br>• 1 Penetration Tester |

#### Timeline

| Starter | Growth | Enterprise |
|---------|--------|------------|
| • Requirement & Design: 1–2 Minggu<br>• Development: 2 Minggu–1 Bulan<br>• Testing & Go-Live: 1–2 Minggu | • Requirement & Design: 2 Minggu–1 Bulan<br>• Development: 1–2 Bulan<br>• Testing & Go-Live: 2 Minggu–1 Bulan | • Requirement & Design: 1–2 Bulan<br>• Development: 2–4 Bulan<br>• Testing & Go-Live: 2 Bulan |

> Durasi dapat disesuaikan dengan kompleksitas fitur, integrasi, dan ruang lingkup proyek.

### Palet Warna

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Teal | `#006D79` | Brand primary, checkmarks |
| Primary Light | `#009BAD` | Brand secondary / accents |
| Dark BG | `#0A1B1F` | Enterprise dark background |
| Dark Surface | `#142A2F` | Enterprise gradient mid-tone |
| Light BG | `#FFFFFF` | Starter / Growth background |
| Subtle BG | `#F4F8F8` | Very light teal tint |
| Heading | `#006D79` | Tier headings |
| Body Text | `#374151` | Description text |
| Grid Color | `#009BAD` | Subtle dot grid accent |
| CTA Green | `#10B981` | CTA button — "Konsultasi Gratis" / "Hubungi Kami" |
| CTA Gold | `#F59E0B` | Alternative CTA accent |

---

## 5. Skill Venturo-Poster

### Deskripsi
Skill `venturo-poster` menghasilkan poster premium untuk salah satu paket Venturo (Starter, Growth, atau Enterprise). Poster diproduksi dengan filosofi desain museum-level, output PNG/PDF berukuran 1048×1048px.

### Trigger Phrases
- `design venturo poster starter` → Generate Starter package poster
- `create venturo growth package poster` → Generate Growth package poster  
- `design venturo enterprise poster` → Generate Enterprise package poster
- `buatkan poster paket venturo` (Indonesian variant)

### Workflow

1. **Temukan dokumen kontekstual** — Baca `packages_context.md` di root project relatif terhadap direkturi kerja.
2. **Konfirmasi tier** — Jika ambigous, tanyakan kepada pengguna. Default: **Starter**.
3. **Ekstraksi data dari `packages_context.md`**:
   - Untuk tier terpilih: baris *"Ideal untuk"*, *"Budget Proyek"*, *"Dedicated Team"*, *"Timeline"*
   - Tabel *Color Palette Reference* seluruhnya (termasuk palet hex codes)
4. **Susun instruksi bebas-formulir** yang berisi:
   - Field konten paket (verbatim bila mungkin)
   - Palet warna (anchoring tones, bukan komposisi keseluruhan)
   - Kanvas persegi 1048 × 1048 PNG
   - Arah gaya: poster layanan Indonesia tema teal modern, layout Z-pattern, CTA *"Konsultasi Gratis"* dalam `#10B981` (atau *"Hubungi Kami"* dalam `#F59E0B` untuk Enterprise)
   - Judul spesifik tier: *"PAKET STARTER"* / *"PAKET GROWTH"* / *"PAKET ENTERPRISE"*
5. **Invoke skill `canvas-design`** via Skill tool — kirim instruksi yang disusun tadi **verbatim**. Jangan parafrasa fakta paket.
6. **Canvas-design** menangani+filosofi + render kanvas → output `.md` (filosofi) + `.png` atau `.pdf` (poster) di direktori kerja.
7. **Jika user minta tier ulangan**, ulangi workflow — jangan batch multiple tier dalam satu panggilan `canvas-design`.

### Catatan Penting
- Skill ini **TIDAK melakukan rendering langsung**. Semua rendering ditugaskan ke `canvas-design` skill yang dipasang secara global.
- Jika `packages_context.md` tidak ada, tolak panggilan dan arahkan pengguna ke file tersebut terlebih dahulu.
- Jika `canvas-design` belum terinstal globally, instruksikan pengguna menginstallnya dulu sebelum ulang eksekusi.

### Dependensi
- Memerlukan `canvas-design` skill (terpasang secara global sebagai foundation)
- Layout mengikuti pola **Z-pattern**: Logo (kiri atas) → Nama Tier (kanan atas) → Content (kiri tengah) → Tombol CTA (kanan bawah)

---

## 6. Data Output Graphify

Output otomatis dari analisis pengetahuan:

| File | Deskripsi |
|------|-----------|
| `graphify-out/graph.json` | Data raw graph dalam format JSON (3 nodes, 2 edges, 1 community) |
| `graphify-out/GRAPH_REPORT.md` | Laporan audit lengkap (seperti di sini!) |
| `graphify-out/graph.html` | Visualisasi interaktif — buka di browser |
| `graphify-out/.graphify_analysis.json` | Metadata komunitas dan koheksi |

**Graph Health**: OK (tidak ada edge dangling/kehilangan/collapsed)

---

## 7. Maintaining Graph yang Mutakhir

Setelah perubahan pada file sumber, lakukan pembaruhan:

```bash
# Perbarui graph tanpa biaya API (hanya ekstrak file yang baru/berubah)
graphify update .
```

Periksa keausan graph dengan membandingkan commit terkini:

```bash
git rev-parse HEAD
```

---

## 8. Referensi

- [Poster Design Skill](sketch://skill/poster-design) — Skill global yang mendasari workflow
- [Canvas Design Skill](sketch://skill/canvas-design) — Engine rendering sebenarnya
- [graphify](https://github.com/safishamsi/graphify) — Alat pembuktian graf pengetahuan yang digunakan di sini

---

*Generated by Knowledge Graph Analysis | Commit: deb35b7d | Date: 2026-07-30*