# Venturo Skills Catalog

Project ini adalah **WhatsApp Business catalog image generator** untuk Venturo Software House.
Gunakan **Qwen-Image-2.0-Pro** via maxrouter.io API untuk generate gambar katalog.

## Skill: Venturo Poster

Skill ini ada di `venturo-poster/skills/venturo-poster/SKILL.md` dan `.claude/skills/venturo-poster/SKILL.md`.
Agent: Load skill ini via `skill` tool saat user minta bikin katalog WhatsApp, poster Venturo, atau catalog wa.

## MCP Server

Ada MCP server Python di `venturo-poster/mcp-playwright/server.py` dengan 2 tools:
- `generate_catalog(prompt, tier, image_size, aspect_ratio)` — generate via Qwen-Image-2.0-Pro
- `check_balance()` — verify API key

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

Set `IMAGE_ROUTER_API_KEY` di `.env` file atau environment variable.
Dapatkan API key di: https://maxrouter.io
