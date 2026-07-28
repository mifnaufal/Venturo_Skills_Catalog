# Venturo Service Packages — Context for Catalog Generation (HD)

Use this reference to understand tier content and design specs. All posters are rendered at **2048×2048px** container with **Device Scale Factor 2** → output **4096×4096px** via Playwright.

---

## Masalah yang Sering Terjadi

- Perusahaan membutuhkan website atau aplikasi yang benar-benar sesuai dengan proses bisnisnya.
- Sudah menggunakan aplikasi berlangganan, namun fitur yang tersedia belum mampu memenuhi kebutuhan operasional.
- Proses bisnis harus menyesuaikan aplikasi, bukan aplikasi yang mengikuti kebutuhan perusahaan.
- Sulit melakukan kustomisasi karena keterbatasan sistem yang digunakan.
- Sistem yang ada tidak dapat terintegrasi dengan aplikasi atau layanan lain yang sudah dimiliki.
- Tampilan aplikasi kurang user-friendly dan tidak mencerminkan identitas perusahaan.
- Seiring pertumbuhan bisnis, sistem yang digunakan tidak lagi mampu mendukung kebutuhan operasional.

---

## Solusi yang Kami Bangun

- Pengembangan Website dan Mobile Application (Android & iOS) yang dirancang khusus sesuai kebutuhan perusahaan.
- Analisis kebutuhan bisnis untuk memastikan setiap fitur mendukung proses operasional.
- Desain UI/UX modern, responsif, dan mudah digunakan.
- Pengembangan fitur yang fleksibel sesuai kebutuhan saat ini maupun pengembangan di masa mendatang.
- Integrasi dengan ERP, CRM, HRIS, Payment Gateway, WhatsApp, API, dan sistem existing.
- Dashboard monitoring dan reporting untuk mendukung pengambilan keputusan.
- Sistem yang aman, scalable, dan siap berkembang mengikuti pertumbuhan bisnis.

---

## Hasil yang Didapat

- Website atau aplikasi yang dirancang sesuai kebutuhan dan proses bisnis perusahaan.
- Meningkatkan efisiensi operasional melalui digitalisasi dan otomatisasi proses kerja.
- Sistem yang fleksibel dan mudah dikembangkan seiring pertumbuhan bisnis.
- Integrasi data yang lebih baik sehingga proses bisnis menjadi lebih cepat dan akurat.
- Pengalaman pengguna yang lebih baik dengan UI/UX yang modern dan intuitif.
- Mendukung pengambilan keputusan melalui dashboard dan laporan yang terintegrasi.

---

# Paket Pengembangan Sistem

| **Starter** | **Growth** | **Enterprise** |
| --- | --- | --- |
| **Ideal untuk** UMKM, usaha mikro, perusahaan kecil, dan startup yang membutuhkan website, mobile application, atau sistem operasional sederhana untuk mendukung proses bisnis. **Budget Proyek** Rp20 Juta – Rp80 Juta | **Ideal untuk** perusahaan yang membutuhkan website atau aplikasi custom sesuai proses bisnis, seperti Finance System, HRIS, CRM, ERP, Inventory, Procurement, Warehouse Management System (WMS), Logistic Management System, Sales Management, Production Management, Asset Management, maupun sistem operasional lainnya untuk meningkatkan efisiensi operasional dan mendukung pertumbuhan bisnis. **Budget Proyek** Rp80 Juta – Rp250 Juta | **Ideal untuk** perusahaan menengah hingga enterprise yang membutuhkan sistem berskala besar, integrasi lintas sistem, keamanan tingkat tinggi, AI, Big Data, maupun transformasi digital secara menyeluruh. **Budget Proyek** Mulai dari Rp250 Juta |
| **Dedicated Team** | **Dedicated Team** | **Dedicated Team** |
| • 1 Business Analyst<br>• 1 Senior Software Engineer | • 1 Business Analyst<br>• 1 Senior Software Engineer<br>• 1 UI/UX Designer<br>• 1 QA Engineer | • 1 Business Analyst<br>• 1 Senior Software Engineer<br>• 1 Intermediate Software Engineer<br>• 1 UI/UX Designer<br>• 1 QA Engineer<br>• 1 Penetration Tester |
| **Timeline**<br>• Requirement Analysis & System Design : **1 – 2 Minggu**<br>• System Development : **2 Minggu – 1 Bulan**<br>• Testing (SIT & UAT), Deployment & Go-Live : **1 – 2 Minggu** | **Timeline**<br>• Requirement Analysis & System Design : **2 Minggu – 1 Bulan**<br>• System Development : **1 ��� 2 Bulan**<br>• Testing (SIT & UAT), Deployment & Go-Live : **2 Minggu – 1 Bulan** | **Timeline**<br>• Requirement Analysis & System Design : **1 – 2 Bulan**<br>• System Development : **2 – 4 Bulan**<br>• Testing (SIT & UAT), Deployment & Go-Live : **2 Bulan** |

- Durasi pengembangan dapat menyesuaikan kompleksitas fitur, integrasi sistem, dan ruang lingkup proyek.

---

## Color Palette Reference

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Teal | `#006D79` | Brand primary, checkmarks |
| Primary Light | `#009BAD` | Brand secondary / accents |
| Dark BG | `#0A1B1F` | Enterprise dark background |
| Dark Surface | `#142A2F` | Enterprise gradient mid-tone |
| Light BG | `#FFFFFF` | Starter / Growth background |
| Subtle BG | `#F4F8F8` | Very light teal tint |
| Heading | `#006D79` | Tier headings (Starter/Growth) |
| Body Text | `#374151` | Description text |
| Grid Color | `#009BAD` | Subtle dot grid accent |
| **CTA Green** | **`#10B981`** | **CTA button — "Konsultasi Gratis" / "Hubungi Kami"** |
| **CTA Gold** | **`#F59E0B`** | **Alternative CTA accent** |

---

## Design Specs — All Templates (HD Edition)

Every catalog follows the same visual language, matching venturo.id branding. **Semua ukuran di-double untuk HD (2048×2048 container).**

### Layout Structure
- **Canvas:** 2048×2048px square (bukan 1024)
- **Layout Pattern:** Z-Pattern — Logo (kiri-atas) → Tier name (kanan-atas) → Content (kiri-bawah) → CTA (kanan-bawah)
- **Focal Point:** Tier **224px** adalah raja. Ilustrasi SVG/p5.js di z-index 0, opacity max 0.15 — jangan compete dengan tier name.
- **Header:** Venturo logo small (72–96px) + "PAKET [TIER]" in massive bold typography (**224px**, weight 900, tracking -8px)
- **Budget Box:** Solid color pill with price range (**56px**)
- **Tagline:** **40px** description paragraph under budget
- **Section Label:** Uppercase, **24px**, letter-spacing 8px
- **Feature List:** Full-width checkmarks — solid teal circle **56×56px** with white ✓
- **CTA Button:** WAJIB — "Konsultasi Gratis" atau "Hubungi Kami" di kanan-bawah. Posisi ikuti Z-pattern.
- **CTA Color:** `#10B981` (hijau) atau `#F59E0B` (kuning emas) — kontras terhadap palette teal.
- **CTA Size:** **32px** font, weight 700, pill shape (border-radius 32px), padding 20px 48px.
- **Illustrations:** WAJIB — SVG elements (circle/path/polygon/pattern) dan/atau p5.js generative effects
- **Design approach:** "Rame tapi simple" — visually rich dengan SVG shapes, pattern, gradient, tapi tetap clean
- **Bottom Grid:** 2-column layout
- **Footer:** "© venturo.id" subtly placed, **24px**
- **White Space:** Margin luar **64px**, gap antar section **48–64px**, padding internal card **48px**.

### Background Treatment
- **Starter:** White with dot grid (`#006D79` 6% opacity), spacing **64px**
- **Growth:** White with dot grid (`#009BAD` 5% opacity), spacing **48px**, teal gradient budget box
- **Enterprise:** Dark teal gradient (#0A1B1F → #112D35) with dot grid overlay + radial glow radius **800px**

### Checkmarks
- Solid filled circles (accent color per tier)
- White checkmark symbol inside (✓ / U+2713)
- **56×56px** diameter (double from 28px)

### Typography
- All using Google Fonts Inter (loaded via import)
- Tier name: **224px**, weight 900, tracking -8px (double from 112px)
- Budget: **56px**, weight 800, rounded corners **22px** (double from 28px/10px)
- Feature items: **36px**, weight 600 (double from 18px)
- Section labels: **24px**, weight 800, uppercase, letter-spacing 8px (double from 12px/4px)
