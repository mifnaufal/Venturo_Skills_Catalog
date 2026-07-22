# Venturo WhatsApp Business Catalog — Antigravity Plugin

Generate **WhatsApp Business catalog images** (1080x1080) for Venturo's software development service packages. AI-generated backgrounds + auto text rendering + logo compositing.

## Prerequisites

- [Antigravity CLI](https://antigravity.google/docs/cli/install)
- Python 3.8+, Pillow: `pip install Pillow`
- Playwright + Chromium: `pip install playwright && python3 -m playwright install chromium`
- Akun [Dreamina (CapCut)](https://dreamina.capcut.com) — gratis, 225 credits/hari

## Clone & Install

```bash
git clone https://github.com/<username>/venturo-catalog-plugin.git
cd Venturo_Skills_Catalog

# Install Python dependency
pip install Pillow

# Install sebagai Antigravity plugin
./install.sh
# atau: ./install.sh --target plugin
# atau: ./install.sh --target skill (slash command /venturo-poster)
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

Register plugin:
```bash
agy plugin install ~/.gemini/antigravity-cli/plugins/venturo-poster
```

## Setup Dreamina

Before generating, you need a Dreamina session ID:

1. Buka [dreamina.capcut.com](https://dreamina.capcut.com), login (Google/Facebook/TikTok)
2. Buka DevTools (F12) → **Application** tab → **Cookies** → `dreamina.capcut.com`
3. Cari cookie `sessionid` atau `sessionid_ss`, copy nilainya
4. Edit `venturo-poster/config/cookies.json`:
```json
{
  "api_url": "https://j.aisk.de5.net",
  "session_ids": ["us-paste_session_id_disini"],
  "region": "us"
}
```
   Tambahkan prefix region (`us-`, `hk-`, `sg-`, `jp-`) sesuai lokasi akunmu.
   Bisa tambah multiple session ID (dipisah koma) biar auto-rotate jika limit habis.

> `config/cookies.json` sudah di `.gitignore` — tidak akan ter-commit.

## Cara Pakai

**Via TUI:**
```bash
agy
# lalu ketik:  /venturo-poster
# atau chat:   "buat katalog WhatsApp buat Venturo Enterprise"
#              "bikin catalog gambar paket Growth"
```

**Via script langsung:**
```bash
# 1. Generate background
python3 venturo-poster/scripts/generate_base.py \
  --prompt "ERP dashboard modern dengan tim developer" \
  --tier growth \
  --aesthetics "Interconnected CRM dashboards" \
  --lighting "Asian developers, natural lighting" \
  --bg-tone "Dark cybertech" \
  --output /tmp/bg.png

# 2. Render catalog card + logo
python3 venturo-poster/scripts/composite_logo.py \
  --input /tmp/bg.png \
  --output venturo-poster/output/catalog_growth.png \
  --tier growth \
  --position bottom-right
```

## Output Specs

| Item | Spec |
|------|------|
| Ukuran | 1080 x 1080 px (1:1) |
| Format | PNG |
| Konten | Nama paket, budget, deskripsi, tim, timeline, logo Venturo |
| Bahasa | Indonesia |

## Project Structure

```
venturo-poster/                          # Plugin root
├── plugin.json                          # Manifest (agy plugin install)
├── skills/venturo-poster.md             # Skill def → /venturo-poster
├── agents/                              # Subagent templates
├── rules/                               # Codebase rules
├── config/
│   ├── cookies.json                     # Dreamina session ID (gitignored)
│   └── cookies.example.json             # Template referensi
├── assets/image_1c155d.png              # Venturo logo (asli)
├── scripts/
│   ├── generate_base.py                 # Dreamina API + fallback chain
│   ├── composite_logo.py               # Text rendering + logo overlay
│   └── generate_placeholder_logo.py     # Dev placeholder
├── templates/packages_context.md        # Service tier reference
└── output/                              # Generated catalog images
├── install.sh                           # Linux/macOS installer
├── install.ps1                          # Windows installer
└── README.md
```

Referensi: [Antigravity CLI Plugins & Skills](https://antigravity.google/docs/cli/plugins)

## License

MIT
