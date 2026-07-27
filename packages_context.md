# Venturo Service Packages — Context for Catalog Generation

Use this reference to understand tier content and design specs. All catalogs are rendered as **square 1024x1024** PNG via Playwright.

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
| Primary Teal | `#006D79` | Brand primary |
| Primary Light | `#009BAD` | Brand secondary / accents |
| Dark BG | `#0A1B1F` | Enterprise dark background |
| Dark Surface | `#142A2F` | Enterprise gradient mid-tone |
| Light BG | `#FFFFFF` | Starter / Growth background |
| Subtle BG | `#F4F8F8` | Very light teal tint |
| Heading | `#006D79` | Tier headings (Starter/Growth) |
| Body Text | `#374151` | Description text |
| Grid Color | `#009BAD` | Subtle dot grid accent |

---

## Design Specs — All Templates

Every catalog follows the same visual language, matching venturo.id branding:

### Layout Structure
- **Canvas:** 1024×1024px square
- **Header:** Venturo logo SVG + "PAKET [TIER]" in massive bold typography (112px, weight 900)
- **Budget Box:** Solid color pill with price range
- **Tagline:** 20px description paragraph under budget
- **Section Label:** Uppercase, letter-spacing 4px
- **Feature List:** Full-width checkmarks (solid teal circle with white ✓)
- **Bottom Grid:** 2-column layout — left = team + timeline details, right = 2 highlight cards (cocok untuk + fase bisnis)
- **Footer:** "© venturo.id" subtly placed bottom-left

### Background Treatment
- **Starter:** White with very subtle dot grid (teal 6% opacity)
- **Growth:** White with medium dot grid (teal 5% opacity), teal gradient budget box
- **Enterprise:** Dark teal gradient (#0A1B1F → #112D35) with dot grid overlay + radial glow top-right

### Checkmarks
- Solid filled circles (`#006D79` for Starter, `#006D79` for Growth, `#009BAD` for Enterprise)
- White checkmark symbol inside
- 28×28px diameter

### Typography
- All using Google Fonts Inter (loaded via import)
- Tier name: 112px, weight 900, tight tracking -4px
- Budget: 28px, weight 800, rounded corners 10px
- Feature items: 18px, weight 600
- Section labels: 12px, weight 800, uppercase, letter-spacing 4px
