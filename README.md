# Venturo WhatsApp Business Catalog — Antigravity Plugin

Generate **WhatsApp Business catalog images** for Venturo's software development packages using **Qwen-Image-2.0-Pro** (via ImageRouter API). Logo Venturo dikirim sebagai reference image, AI composite otomatis.

**Engine:** Qwen-Image-2.0-Pro — `$0.075/gambar` — imagerouter.io

## Prerequisites

- Python 3.8+
- ImageRouter API key: daftar di https://imagerouter.io/api-keys

## Install

```bash
git clone <repo-url>
cd Venturo_Skills_Catalog
pip install -r venturo-poster/mcp-playwright/requirements.txt
./install.sh
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

## Setup API Key

Pilih salah satu:

### Opsi 1 — `.env` file (recommended)

```bash
cp .env.example .env
# lalu edit .env, isi API key:
#   IMAGE_ROUTER_API_KEY=ir_xxx...
```

File `.env` auto-detect — server.py membaca otomatis. Aman di `.gitignore`.

### Opsi 2 — Environment variable

```bash
export IMAGE_ROUTER_API_KEY="ir_xxx..."
agy
```

### Opsi 3 — MCP config

Di `~/.gemini/config/antigravity.json` atau `mcp_config.json`:

```json
{
  "mcpServers": {
    "venturo-poster-playwright": {
      "command": "python3",
      "args": ["<path>/venturo-poster/mcp-playwright/server.py"],
      "env": {
        "IMAGE_ROUTER_API_KEY": "ir_xxx..."
      }
    }
  }
}
```

## Cara Pakai via Antigravity CLI

```bash
agy
# lalu ketik: /venturo-poster
# atau:      buat katalog WhatsApp buat Venturo
```

AI agent akan:
1. Wawancara user (tier, preferensi desain, konten custom)
2. Bangun prompt detail untuk Qwen-Image
3. Tampilkan preview spec untuk approval
4. Generate via ImageRouter API (Qwen-Image-2.0-Pro) — < 10 detik
5. Kirim hasil ke user

## Package Tiers

| Tier | Budget | Ideal untuk |
|------|--------|-------------|
| **Starter** | Rp20 Juta – Rp80 Juta | UMKM, startup |
| **Growth** | Rp80 Juta – Rp250 Juta | Finance, HRIS, CRM, ERP |
| **Enterprise** | Mulai Rp250 Juta | AI, Big Data, cybersecurity |

## Project Structure

```
venturo-poster/
├── plugin.json                       # Plugin manifest
├── skills/venturo-poster/SKILL.md    # AI agent skill definition
├── assets/image_1c155d.png           # Venturo logo (reference untuk AI)
├── mcp-playwright/
│   ├── server.py                     # ImageRouter MCP server (API-based)
│   └── requirements.txt              # Python dependencies
├── templates/packages_context.md     # Service tier reference
├── output/                           # Generated images
├── install.sh                        # Linux/macOS installer
├── install.ps1                       # Windows PowerShell installer
└── README.md
```

Root files:
- `.env.example` — Template API key config
- `.env` — API key (gitignored, tidak ke-commit)
- `.gitignore` — Ignores venv, __pycache__, .env, output/

## License

MIT
