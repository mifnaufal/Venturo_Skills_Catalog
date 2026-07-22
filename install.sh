#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SRC="$SCRIPT_DIR/venturo-poster"
PLUGIN_DIR="$HOME/.gemini/config/plugins/venturo-poster"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Venturo Poster — Antigravity Plugin Install${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# 1. Validate
if [ ! -f "$PLUGIN_SRC/plugin.json" ]; then
    echo -e "${RED}ERROR: venturo-poster/plugin.json not found${NC}"
    exit 1
fi
if [ ! -f "$PLUGIN_SRC/assets/image_1c155d.png" ]; then
    echo -e "${RED}ERROR: assets/image_1c155d.png not found${NC}"
    exit 1
fi

# 2. Remove stale plugin
if [ -d "$PLUGIN_DIR" ]; then
    echo "Removing old plugin..."
    rm -rf "$PLUGIN_DIR"
fi

# 3. Copy fresh plugin
cp -r "$PLUGIN_SRC" "$PLUGIN_DIR"
echo -e "${GREEN}✔ Plugin copied to $PLUGIN_DIR${NC}"

# 4. Install Playwright
echo ""
echo "Installing Python dependencies..."
pip3 install playwright 2>/dev/null || pip install playwright 2>/dev/null || true
if python3 -c "from playwright.sync_api import sync_playwright; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✔ Playwright ready${NC}"
else
    echo "Installing Playwright browsers..."
    python3 -m playwright install chromium 2>/dev/null || echo -e "${RED}Run: playwright install chromium${NC}"
fi

# 5. Done
echo ""
echo -e "${GREEN}✔ Venturo Poster — siap digunakan!${NC}"
echo ""
echo "Cara pakai:"
echo "  agy"
echo "  → ketik: /venturo-poster"
echo "  → atau:  buat katalog WhatsApp buat Venturo"
echo ""
