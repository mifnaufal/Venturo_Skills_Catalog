# Venturo Skills Catalog

Generate **WhatsApp Business catalog images** for Venturo's software development packages using **Cloudflare Workers AI** (SDXL Lightning). Output: 1400x1024 canvas with blank right-side space for Pillow overlay.

**Engine:** Cloudflare Workers AI — `FREE` (100K calls/day) — self-hosted Worker

## Prerequisites

- Python 3.8+
- Cloudflare account + Workers AI enabled
- Dependencies: `pip install -r venturo-poster/mcp-playwright/requirements.txt`
- Deployed Cloudflare Worker: `venturo-poster/cloudflare-worker.mjs`

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
    ├── cloudflare-worker.mjs          # Cloudflare Worker source code
    ├── skills/venturo-poster/SKILL.md # Canonical skill definition
    ├── assets/image_1c155d.png        # Venturo logo (untuk overlay Pillow manual)
    ├── mcp-playwright/
    │   ├── server.py                  # MCP server (Workers AI-based)
    │   └── requirements.txt           # Python dependencies
    ├── templates/packages_context.md  # Service tier reference
    ├── starter_prompt.txt             # Example prompt — Starter tier
    ├── growth_prompt.txt              # Example prompt — Growth tier
    ├── enterprise_prompt.txt          # Example prompt — Enterprise tier
    └── output/                        # Generated images (1400x1024)
```

## Setup per Platform

### Deploy Cloudflare Worker Pertama Kali

```bash
# 1. Install Wrangler CLI
npm install -g wrangler

# 2. Inisialisasi worker
cd venturo-poster
wrangler init venturo-img-gen

# 3. Copy cloudflare-worker.mjs ke index.mjs (atau update wrangler.toml)

# 4. Tambahkan AI binding di wrangler.toml:
#    [[services]]
#    binding = "AI"
#    service = "@cloudflare/workers-ai"

# 5. Deploy
wrangler deploy
# Output: https://venturo-img-gen.<subdomain>.workers.dev
```

### Setup MCP Server

```bash
# Install dependencies
pip install -r venturo-poster/mcp-playwright/requirements.txt

# Set environment variables (.env atau shell):
export CLOUDFLARE_WORKER_URL="https://venturo-img-gen.<your-subdomain>.workers.dev"
export CLOUDFLARE_API_KEY="your-secret-api-key"

# Start Claude Code (auto-reads .mcp.json + .claude/skills/)
claude
```

### OpenCode / Antigravity

Sama — set env vars di `mcp_config.json` atau `.env`, lalu jalankan sesuai platform.

## Environment Variables

| Variable | Purpose | Required |
|---|---|---|
| `CLOUDFLARE_WORKER_URL` | URL Cloudflare Worker endpoint | Yes |
| `CLOUDFLARE_API_KEY` | API key untuk auth Worker | Yes |
| `CANVAS_WIDTH` | Output canvas width (default: 1400) | No |
| `CANVAS_HEIGHT` | Output canvas height (default: 1024) | No |

## Cara Pakai

Di agent prompt, bilang aja:
- "buat katalog WhatsApp Venturo"
- "catalog wa paket growth"
- "poster venturo buat client"

AI agent akan:
1. Wawancara user (tier, preferensi desain, overlay content)
2. Bangun prompt detail (dengan instruksi ruang kosong kanan)
3. Tampilkan preview spec untuk approval
4. Generate via Cloudflare Workers AI — ~15-30 detik
5. Output: gambar 1400x1024 dengan space kanan kosong siap overlay Pillow
6. Kirim hasil ke user

## Package Tiers

| Tier | Budget | Ideal untuk |
|------|--------|-------------|
| **Starter** | Rp20 Juta – Rp80 Juta | UMKM, startup |
| **Growth** | Rp80 Juta – Rp250 Juta | Finance, HRIS, CRM, ERP |
| **Enterprise** | Mulai Rp250 Juta | AI, Big Data, cybersecurity |

## License

MIT
