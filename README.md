# Venturo WhatsApp Business Catalog — Antigravity Plugin

Generate **WhatsApp Business catalog images** (3840x3840) for Venturo's software development service packages. Programmatic Pillow design + Venturo brand identity + auto logo compositing.

## Prerequisites

- [Antigravity CLI](https://antigravity.google/docs/cli/install)
- Python 3.8+, Pillow: `pip install Pillow`

## Clone & Install

```bash
git clone https://github.com/<username>/venturo-catalog-plugin.git
cd Venturo_Skills_Catalog

# Install Python dependencies
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
# 1. Generate programmatic catalog design (4K)
python3 venturo-poster/scripts/generate_design.py \
  --output /tmp/design.png

# 2. Composite Venturo logo (auto position)
python3 venturo-poster/scripts/composite_logo.py \
  --input /tmp/design.png \
  --output venturo-poster/output/katalog.png \
  --tier growth \
  --position auto \
  --logo-only
```

## Output Specs

| Item | Spec |
|------|------|
| Ukuran | 3840 x 3840 px (4K, 1:1) |
| Format | PNG |
| Konten | Hero, stat counters, 3 package cards, CTA footer, logo Venturo |
| Bahasa | Indonesia |

## Project Structure

```
venturo-poster/                          # Plugin root
├── plugin.json                          # Manifest (agy plugin install)
├── skills/venturo-poster.md             # Skill def → /venturo-poster
├── assets/image_1c155d.png              # Venturo logo (asli)
├── scripts/
│   ├── generate_design.py               # Programmatic design renderer (Pillow)
│   └── composite_logo.py                # Logo compositing + auto positioning
├── templates/packages_context.md        # Service tier reference
└── output/                              # Generated catalog images
├── install.sh                           # Linux/macOS installer
├── install.ps1                          # Windows installer
└── README.md
```

## License

MIT
