# Venturo Skills Catalog

Generate **WhatsApp Business catalog images** for Venturo's software development packages using **Qwen-Image-2.0-Pro** (via maxrouter.io API). Logo Venturo dikirim sebagai reference image, AI composite otomatis.

**Engine:** Qwen-Image-2.0-Pro — `$0.075/gambar` — maxrouter.io

## Prerequisites

- Python 3.8+
- Dependencies: `pip install -r venturo-poster/mcp-playwright/requirements.txt`
- API Key: daftar di https://maxrouter.io

## Project Structure

```
Venturo_Skills_Catalog/
├── AGENTS.md                          # OpenCode project rules
├── CLAUDE.md                          # Claude Code instructions
├── .mcp.json                          # MCP config (Claude Code + OpenCode)
├── opencode.json                      # OpenCode project config
├── .env / .env.example                # API key config
├── .claude/skills/venturo-poster/     # Skill discovery (Claude Code + OpenCode)
├── install.sh / install.ps1           # Installers
└── venturo-poster/
    ├── plugin.json                    # Antigravity plugin manifest
    ├── skills/venturo-poster/SKILL.md # Canonical skill definition
    ├── assets/image_1c155d.png        # Venturo logo (reference untuk AI)
    ├── mcp-playwright/
    │   ├── server.py                  # MCP server (API-based)
    │   └── requirements.txt           # Python dependencies
    ├── templates/packages_context.md  # Service tier reference
    └── output/                        # Generated images
```

## Setup per Platform

### Claude Code

```bash
# Install dependencies
pip install -r venturo-poster/mcp-playwright/requirements.txt

# Set API key
export IMAGE_ROUTER_API_KEY="sk-xxx..."

# Start Claude Code (auto-reads .mcp.json + .claude/skills/)
claude
```

Atau register global:
```bash
claude mcp add --scope user venturo-poster -- python3 venturo-poster/mcp-playwright/server.py
```

### OpenCode

```bash
# Install dependencies
pip install -r venturo-poster/mcp-playwright/requirements.txt

# Set API key
export IMAGE_ROUTER_API_KEY="sk-xxx..."

# Start OpenCode (auto-reads .mcp.json + AGENTS.md)
opencode
```

### Antigravity (agy)

```bash
# Quick install
pip install -r venturo-poster/mcp-playwright/requirements.txt
./install.sh          # Linux/macOS
.\install.ps1         # Windows

# Set API key di .env atau mcp_config.json
# Lalu:
agy
```

## Setup API Key

Pilih salah satu:

### Opsi 1 — `.env` file (recommended)
```bash
cp .env.example .env
# lalu edit .env, isi API key
```

### Opsi 2 — Environment variable
```bash
export IMAGE_ROUTER_API_KEY="sk-xxx..."
```

### Opsi 3 — MCP config
Isi `IMAGE_ROUTER_API_KEY` di `env` field `.mcp.json` atau `mcp_config.json`.

## Cara Pakai

Di agent prompt, bilang aja:
- "buat katalog WhatsApp Venturo"
- "catalog wa paket growth"
- "poster venturo buat client"

AI agent akan:
1. Wawancara user (tier, preferensi desain, konten custom)
2. Bangun prompt detail untuk Qwen-Image
3. Tampilkan preview spec untuk approval
4. Generate via maxrouter.io API — < 10 detik
5. Kirim hasil ke user

## Package Tiers

| Tier | Budget | Ideal untuk |
|------|--------|-------------|
| **Starter** | Rp20 Juta – Rp80 Juta | UMKM, startup |
| **Growth** | Rp80 Juta – Rp250 Juta | Finance, HRIS, CRM, ERP |
| **Enterprise** | Mulai Rp250 Juta | AI, Big Data, cybersecurity |

## License

MIT
