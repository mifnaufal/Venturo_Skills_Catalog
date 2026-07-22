#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/venturo-poster/skills/venturo-poster.md"
SKILL_DEST="$HOME/.gemini/antigravity-cli/skills/venturo-poster.md"
ASSETS_DIR="$SCRIPT_DIR/venturo-poster/assets/image_1c155d.png"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Venturo Poster — Antigravity Skill Install ${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# 1. Validate files
if [ ! -f "$SKILL_SRC" ]; then
    echo -e "${RED}ERROR: skills/venturo-poster.md not found${NC}"
    exit 1
fi
if [ ! -f "$ASSETS_DIR" ]; then
    echo -e "${RED}ERROR: assets/image_1c155d.png not found${NC}"
    exit 1
fi

# 2. Copy skill
mkdir -p "$(dirname "$SKILL_DEST")"
cp "$SKILL_SRC" "$SKILL_DEST"
echo -e "${GREEN}✔ Skill installed:${NC} $SKILL_DEST"

# 3. Install Playwright
echo ""
echo "Installing Python dependencies..."
pip3 install playwright 2>/dev/null || pip install playwright 2>/dev/null || true
if python3 -c "from playwright.sync_api import sync_playwright; print('OK')" 2>/dev/null; then
    echo -e "${GREEN}✔ Playwright already installed${NC}"
else
    echo "Installing Playwright browsers..."
    python3 -m playwright install chromium 2>/dev/null || echo -e "${RED}Run: playwright install chromium${NC}"
fi

# 4. Done
echo ""
echo -e "${GREEN}✔ Venturo Poster — Antigravity Skill ready!${NC}"
echo ""
echo "Cara pakai:"
echo "  agy"
echo "  → ketik: /venturo-poster"
echo "  → atau:  buat katalog WhatsApp buat Venturo"
echo ""
echo "Script path untuk skill:"
echo "  $SCRIPT_DIR/venturo-poster/scripts/generate_base.py"
echo ""
