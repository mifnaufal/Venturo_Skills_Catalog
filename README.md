# Venturo WhatsApp Business Catalog — Antigravity Plugin

Generate **WhatsApp Business catalog images** for Venturo's software development packages using **Dreamina AI** (via Playwright browser automation). Logo Venturo diupload sebagai reference image, AI composite otomatis.

## Prerequisites

- Python 3.8+
- Playwright: `pip install playwright && playwright install chromium`

## Install

```bash
git clone https://github.com/<username>/venturo-catalog-plugin.git
cd Venturo_Skills_Catalog
pip install playwright && playwright install chromium
./install.sh
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

## Quick Start

```bash
# Generate satu paket
python3 venturo-poster/scripts/generate_base.py --tier starter

# Generate semua paket sekaligus
python3 venturo-poster/scripts/generate_base.py --tier all

# Custom prompt
python3 venturo-poster/scripts/generate_base.py \
  --tier growth \
  --prompt "Buat katalog WhatsApp untuk Venturo Growth Package dengan tema profesional"

# Custom output
python3 venturo-poster/scripts/generate_base.py \
  --tier enterprise \
  --output venturo-poster/output/katalog_enterprise.png
```

## Cara Kerja

1. Script membuka Chromium (non-headless) ke Dreamina
2. **Login manual** — user login ke akun ByteDance/Dreamina
3. Script upload `assets/image_1c155d.png` (logo Venturo) sebagai reference image
4. Script isi prompt text otomatis (dengan fallback manual)
5. AI generate gambar katalog dengan logo Venturo sudah ter-composite
6. Hasil disimpan sebagai PNG

## Package Tiers

| Tier | Budget | Ideal untuk |
|------|--------|-------------|
| **Starter** | Rp20 Juta – Rp80 Juta | UMKM, startup |
| **Growth** | Rp80 Juta – Rp250 Juta | Finance, HRIS, CRM, ERP |
| **Enterprise** | Mulai Rp250 Juta | AI, Big Data, cybersecurity |

## Project Structure

```
venturo-poster/
├── plugin.json
├── skills/venturo-poster/SKILL.md
├── assets/image_1c155d.png          # Venturo logo (reference untuk AI)
├── scripts/
│   └── generate_base.py             # Dreamina AI + Playwright manual login
├── templates/packages_context.md    # Service tier reference
├── output/                          # Generated images
├── install.sh
├── install.ps1
└── README.md
```

## License

MIT
