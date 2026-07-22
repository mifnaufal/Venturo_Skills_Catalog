set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$SCRIPT_DIR/venturo-poster"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Venturo Poster — Antigravity Plugin Install${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

if [ ! -f "$PLUGIN_DIR/plugin.json" ]; then
    echo -e "${RED}ERROR: venturo-poster/plugin.json not found.${NC}"
    echo "Make sure install.sh is in the same directory as venturo-poster/"
    exit 1
fi

TARGET=""
INSTALL_MODE="plugin"

if [ $# -ge 2 ] && [ "$1" = "--target" ]; then
    TARGET="$2"
    case "$TARGET" in
        plugin|plugins) TARGET="$HOME/.gemini/antigravity-cli/plugins" ;;
        skill|skills)   TARGET="$HOME/.gemini/antigravity-cli/skills"; INSTALL_MODE="skill" ;;
    esac
fi

if [ -z "$TARGET" ]; then
    echo "Select install mode:"
    echo "  1) Plugin  → ~/.gemini/antigravity-cli/plugins/ (agy plugin install)"
    echo "  2) Skill   → ~/.gemini/antigravity-cli/skills/  (/venturo-poster command)"
    echo "  3) Project → .agents/skills/  (local to this dir)"
    echo "  4) Custom path"
    read -rp "Choice [1-4]: " choice
    case "$choice" in
        1) TARGET="$HOME/.gemini/antigravity-cli/plugins"; INSTALL_MODE="plugin" ;;
        2) TARGET="$HOME/.gemini/antigravity-cli/skills";  INSTALL_MODE="skill" ;;
        3) TARGET=".agents/skills";                         INSTALL_MODE="skill" ;;
        4) read -rp "Enter target path: " TARGET;            INSTALL_MODE="custom" ;;
        *) echo -e "${RED}Invalid choice.${NC}"; exit 1 ;;
    esac
fi

TARGET_DIR="$(eval echo "$TARGET")"
mkdir -p "$TARGET_DIR"

if [ "$INSTALL_MODE" = "skill" ]; then
    DEST="$TARGET_DIR/venturo-poster.md"
    SRC="$PLUGIN_DIR/skills/venturo-poster.md"
    if [ -f "$DEST" ]; then
        read -rp "Skill already exists. Overwrite? [y/N] " confirm
        [ "$confirm" != "y" ] && [ "$confirm" != "Y" ] && { echo "Cancelled."; exit 0; }
    fi
    cp "$SRC" "$DEST"
    echo -e "${GREEN}✔ Skill installed to $DEST${NC}"
else
    DEST="$TARGET_DIR/venturo-poster"
    if [ -d "$DEST" ]; then
        read -rp "Plugin already exists at $DEST. Overwrite? [y/N] " confirm
        [ "$confirm" != "y" ] && [ "$confirm" != "Y" ] && { echo "Cancelled."; exit 0; }
        rm -rf "$DEST"
    fi
    cp -r "$PLUGIN_DIR" "$DEST"
    echo -e "${GREEN}✔ Plugin installed to $DEST${NC}"
    echo "  Register with: agy plugin install $DEST"
fi

echo ""
echo "Checking Python dependencies..."
if command -v pip3 &>/dev/null; then
    pip3 install Pillow 2>/dev/null || true
elif command -v pip &>/dev/null; then
    pip install Pillow 2>/dev/null || true
else
    echo -e "${RED}Warning: pip not found. Run: pip install Pillow${NC}"
fi

if [ ! -f "$PLUGIN_DIR/assets/image_1c155d.png" ]; then
    echo -e "${RED}Warning: Venturo logo not found at assets/image_1c155d.png${NC}"
fi

echo ""
echo -e "${GREEN}✔ Venturo Poster Plugin ready!${NC}"
echo ""
echo "Quick start:"
echo "  agy plugin install $DEST"
echo "  agy  →  /venturo-poster"
echo ""
echo "Or use as a standalone skill:"
echo "  ./install.sh --target skill"
