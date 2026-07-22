# Venturo WhatsApp Business Catalog — Antigravity Plugin

Generate **WhatsApp Business catalog images** for Venturo's software development packages using **Dreamina AI** (via Playwright MCP browser automation). Logo Venturo diupload sebagai reference image, AI composite otomatis.

## Prerequisites

- Python 3.8+
- Playwright + Chromium: `pip install -r venturo-poster/mcp-playwright/requirements.txt && playwright install chromium`

## Install

```bash
git clone <repo-url>
cd Venturo_Skills_Catalog
pip install -r venturo-poster/mcp-playwright/requirements.txt
playwright install chromium
./install.sh
```

**Windows (PowerShell):**
```powershell
.\install.ps1
```

## Cara Pakai via Antigravity CLI

```bash
agy
# lalu ketik: /venturo-poster
# atau:      buat katalog WhatsApp buat Venturo
```

AI agent akan:
1. Wawancara user (tier, preferensi desain, konten custom)
2. Bangun prompt detail untuk Dreamina
3. Tampilkan preview spec untuk approval
4. Jalankan Playwright MCP untuk login, upload logo, generate, screenshot
5. Kirim hasil ke user

## MCP Server Configuration

Daftarkan MCP server di Antigravity config (`~/.gemini/config/antigravity.json`):

```json
{
  "mcpServers": {
    "venturo-poster-playwright": {
      "command": "python3",
      "args": ["<absolute_path>/mcp-playwright/server.py"],
      "env": {}
    }
  }
}
```

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
│   ├── server.py                     # Playwright MCP server
│   └── requirements.txt              # Python dependencies
├── templates/packages_context.md     # Service tier reference
├── output/                           # Generated images
├── install.sh                        # Linux/macOS installer
├── install.ps1                       # Windows PowerShell installer
└── README.md
```

## License

MIT
