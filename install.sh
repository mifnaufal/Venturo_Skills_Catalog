#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SRC="$SCRIPT_DIR/venturo-poster"
PLUGIN_DIR="$HOME/.gemini/config/plugins/venturo-poster"
PLUGIN_DIR_CLI="$HOME/.gemini/antigravity-cli/plugins/venturo-poster"
VENV_DIR="$PLUGIN_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python3"
VENV_PIP="$VENV_DIR/bin/pip"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Venturo Poster — Antigravity Plugin Install${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# 1. Validate dependencies
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}ERROR: Python 3 not found. Install Python 3.8+ first.${NC}"
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo -e "  Python ${PY_VERSION} — OK"
else
    echo -e "${RED}ERROR: Python 3.8+ required (found ${PY_VERSION})${NC}"
    exit 1
fi

# 2. Validate plugin files
if [ ! -f "$PLUGIN_SRC/plugin.json" ]; then
    echo -e "${RED}ERROR: venturo-poster/plugin.json not found${NC}"
    exit 1
fi
if [ ! -f "$PLUGIN_SRC/assets/image_1c155d.png" ]; then
    echo -e "${RED}ERROR: assets/image_1c155d.png not found${NC}"
    exit 1
fi
if [ ! -f "$PLUGIN_SRC/mcp-playwright/requirements.txt" ]; then
    echo -e "${RED}ERROR: mcp-playwright/requirements.txt not found${NC}"
    exit 1
fi

# 3. Remove stale plugin directories
for dir in "$PLUGIN_DIR" "$PLUGIN_DIR_CLI"; do
    if [ -d "$dir" ]; then
        echo "  Removing old plugin from $dir..."
        rm -rf "$dir"
    fi
done

# 4. Copy fresh plugin
cp -r "$PLUGIN_SRC" "$PLUGIN_DIR"
cp -r "$PLUGIN_SRC" "$PLUGIN_DIR_CLI"
echo -e "${GREEN}✔ Plugin copied to${NC}"
echo -e "${GREEN}  • $PLUGIN_DIR${NC}"
echo -e "${GREEN}  • $PLUGIN_DIR_CLI${NC}"

# 5. Create Python virtual environment
echo ""
echo "  Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"
echo -e "${GREEN}✔ Virtual environment created at $VENV_DIR${NC}"

# 6. Install MCP + Playwright dependencies
echo ""
echo "  Installing Python dependencies..."
"$VENV_PIP" install -r "$PLUGIN_DIR/mcp-playwright/requirements.txt"
echo -e "${GREEN}✔ Python dependencies installed${NC}"

# 7. Install Chromium
echo ""
echo "  Installing Chromium browser..."
if "$VENV_PYTHON" -c "from playwright.sync_api import sync_playwright; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✔ Playwright ready${NC}"
else
    "$VENV_PYTHON" -m playwright install chromium
    echo -e "${GREEN}✔ Chromium installed${NC}"
fi

# 8. Create mcp_config.json for auto-MCP registration
echo ""
echo "  Registering MCP server..."
for dir in "$PLUGIN_DIR" "$PLUGIN_DIR_CLI"; do
    cat > "$dir/mcp_config.json" << MCPEOF
{
  "mcpServers": {
    "venturo-poster-playwright": {
      "command": "$VENV_PYTHON",
      "args": ["$dir/mcp-playwright/server.py"],
      "env": {}
    }
  }
}
MCPEOF
done
echo -e "${GREEN}✔ MCP config registered for plugin${NC}"

# 9. Show MCP status
echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  MCP Server Auto-Registered${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""
echo "  Plugin mcp_config.json sudah dibuat di:"
echo "    $PLUGIN_DIR/mcp_config.json"
echo "    $PLUGIN_DIR_CLI/mcp_config.json"
echo ""
echo "  Menggunakan Python: $VENV_PYTHON"
echo ""
echo "  Antigravity akan auto-load MCP server saat plugin aktif."
echo ""
echo "  Jika ingin manual, tambahkan ke antigravity.json:"
echo '  {'
echo '    "mcpServers": {'
echo '      "venturo-poster-playwright": {'
echo "        \"command\": \"$VENV_PYTHON\","
echo '        "args": ["'"$PLUGIN_DIR/mcp-playwright/server.py"'"],'
echo '        "env": {}'
echo '      }'
echo '    }'
echo '  }'
echo ""
echo "  Verifikasi: agy plugin list"
echo ""

# 10. Done
echo -e "${GREEN}✔ Venturo Poster — siap digunakan!${NC}"
echo ""
echo "Cara pakai:"
echo "  agy"
echo "  → ketik: /venturo-poster"
echo "  → atau:  buat katalog WhatsApp buat Venturo"
echo ""
