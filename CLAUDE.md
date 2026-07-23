# Venturo Skills Catalog — Claude Code Instructions

Project ini adalah WhatsApp Business catalog image generator untuk Venturo Software House.
Menggunakan Qwen-Image-2.0-Pro via maxrouter.io API.

## Skill: Venturo Poster

Skill ini terdaftar di `.claude/skills/venturo-poster/SKILL.md` — akan auto-load oleh Claude Code.
Untuk workflow lengkap, skill akan membaca canonical file di `venturo-poster/skills/venturo-poster/SKILL.md`.

Trigger: "catalog wa", "katalog whatsapp", "buat katalog", "catalog venturo", "poster venturo"

## MCP Server Setup

Project ini punya MCP server Python di `venturo-poster/mcp-playwright/server.py`.

### Option 1 — Project scope (via .mcp.json, sudah include):
`.mcp.json` udah ada di root. Claude Code auto-read pas startup.

### Option 2 — User scope (global untuk semua project):
```bash
claude mcp add --scope user venturo-poster -- python3 venturo-poster/mcp-playwright/server.py
```

### Install dependencies:
```bash
pip install -r venturo-poster/mcp-playwright/requirements.txt
```

## API Key

Set `IMAGE_ROUTER_API_KEY` di `.env` atau environment variable.
Dapatkan di: https://maxrouter.io
