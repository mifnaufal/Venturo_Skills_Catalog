# Venturo Poster — Antigravity Plugin

An **Antigravity CLI plugin** that generates branded marketing posters for Venturo's software development service packages (Starter, Growth, Enterprise).

## Prerequisites

- [Antigravity CLI](https://antigravity.google/docs/cli/install) installed & authenticated
- Python 3.8+
- Pillow: `pip install Pillow`
- (Optional) `OPENAI_API_KEY` env var for DALL-E 3 image generation

## Clone & Install

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/venturo-poster-plugin.git
cd venturo-poster-plugin

# 2. Install Python dependency
pip install Pillow

# 3. Run installer (interactive)
./install.sh

#    Or pick a mode directly:
#    ./install.sh --target plugin     → ~/.gemini/antigravity-cli/plugins/
#    ./install.sh --target skill      → ~/.gemini/antigravity-cli/skills/  (/venturo-poster)
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

### Manual Registration

If you installed as a plugin, register it with Antigravity CLI:

```bash
agy plugin install ~/.gemini/antigravity-cli/plugins/venturo-poster
```

Verify it's loaded:

```bash
agy plugin list
# → venturo-poster — Generate branded marketing posters for Venturo...
```

## Usage

### Via TUI Slash Command

```bash
agy
# Then type:  /venturo-poster
```

The agent will interview you with 3–5 questions about tier, visuals, lighting, and text, then generate the poster.

### Via Chat Prompt

```bash
agy
# Then type:
#   "buat poster untuk Venturo Enterprise"
#   "create a poster for Venturo Growth package"
#   "generate marketing poster Venturo Starter"
```

### Via Direct Script

```bash
# Generate base image (placeholder if no API key)
python3 venturo-poster/scripts/generate_base.py \
  --prompt "Modern ERP dashboard" \
  --tier growth \
  --aesthetics "Interconnected CRM dashboards" \
  --lighting "Professional studio lighting" \
  --bg-tone "Dark cybertech" \
  --output /tmp/base.png

# Composite logo onto it
python3 venturo-poster/scripts/composite_logo.py \
  --input /tmp/base.png \
  --output venturo-poster/output/poster.png \
  --position bottom-right
```

## Replace the Logo

A placeholder logo is auto-generated at `assets/image_1c155d.png`. Replace it with Venturo's official logo before production use.

## Project Structure

```
venturo-poster/                          # Plugin root
├── plugin.json                          # Manifest (agy plugin install)
├── skills/venturo-poster.md             # Skill def → /venturo-poster
├── agents/                              # Subagent templates
├── rules/                               # Codebase rules
├── assets/image_1c155d.png              # Venturo logo
├── scripts/
│   ├── generate_base.py                 # AI image generation
│   ├── composite_logo.py               # Logo overlay
│   └── generate_placeholder_logo.py     # Dev placeholder
├── templates/packages_context.md        # Service tier reference
└── output/                              # Generated posters
├── install.sh                           # Linux/macOS installer
├── install.ps1                          # Windows installer
└── README.md
```

Reference: [Antigravity CLI Plugins & Skills](https://antigravity.google/docs/cli/plugins)

## License

MIT
