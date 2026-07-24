# Venturo Skills Catalog

Project ini adalah **WhatsApp Business catalog image generator** untuk Venturo Software House.
Gunakan **Cloudflare Workers AI (SDXL Lightning)** via self-hosted Worker untuk generate gambar katalog. Output: 1400x1024 dengan ruang kosong di kanan untuk overlay Pillow.

## Skill: Venturo Poster

Skill ini ada di `venturo-poster/skills/venturo-poster/SKILL.md` dan `.claude/skills/venturo-poster/SKILL.md`.
Agent: Load skill ini via `skill` tool saat user minta bikin katalog WhatsApp, poster Venturo, atau catalog wa.

## MCP Server

Ada MCP server Python di `venturo-poster/mcp-playwright/server.py` dengan 2 tools:
- `generate_catalog(prompt, tier)` — generate catalog via Cloudflare Workers AI
- `check_balance()` — verify endpoint connectivity

Konfigurasi MCP ada di `.mcp.json` (project scope, shared untuk Claude Code + OpenCode).

### Setup MCP untuk OpenCode

Pastikan dependensi terinstall:
```bash
pip install -r venturo-poster/mcp-playwright/requirements.txt
```

`.mcp.json` udah ada di root project — OpenCode auto-load pas startup.

## Instalasi Cepat

```bash
pip install -r venturo-poster/mcp-playwright/requirements.txt
# lalu jalankan:
./install.sh          # Linux/macOS
.\install.ps1         # Windows
```

## API Key

Set `CLOUDFLARE_WORKER_URL` dan `CLOUDFLARE_API_KEY` di `.env` file atau environment variable.
Deploy Worker dari `venturo-poster/cloudflare-worker.mjs`.
