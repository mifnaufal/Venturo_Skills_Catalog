#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_SRC="$SCRIPT_DIR/venturo-poster"
VENV_DIR="$SCRIPT_DIR/.venv"
VENV_PYTHON="$VENV_DIR/bin/python3"
VENV_PIP="$VENV_DIR/bin/pip"

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Venturo Poster — Multi-Platform Install${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# ──────────────────────────────────────
# 1. Validate dependencies
# ──────────────────────────────────────
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

# ──────────────────────────────────────
# 2. Validate project files
# ──────────────────────────────────────
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

# ──────────────────────────────────────
# 3. Install Python dependencies (shared venv)
# ──────────────────────────────────────
echo ""
echo "  Creating Python virtual environment..."
python3 -m venv "$VENV_DIR" >/dev/null 2>&1
echo -e "${GREEN}✔ Virtual environment at $VENV_DIR${NC}"

echo ""
echo "  Installing Python dependencies..."
"$VENV_PIP" install -r "$PLUGIN_SRC/mcp-playwright/requirements.txt" >/dev/null 2>&1
echo -e "${GREEN}✔ Python dependencies installed${NC}"

# ──────────────────────────────────────
# 4. Register MCP server for Claude Code (user scope)
# ──────────────────────────────────────
echo ""
echo -e "${CYAN}--- Claude Code ---${NC}"
if command -v claude &>/dev/null; then
    # Check if already registered
    if claude mcp list 2>/dev/null | grep -q "venturo-poster"; then
        echo -e "  MCP server 'venturo-poster' already registered."
    else
        echo "  Registering MCP server 'venturo-poster'..."
        claude mcp add --scope user venturo-poster \
            -- "$VENV_PYTHON" "$PLUGIN_SRC/mcp-playwright/server.py" 2>/dev/null || {
            echo -e "${YELLOW}  ⚠ Could not auto-register. Register manually:${NC}"
            echo "    claude mcp add --scope user venturo-poster -- $VENV_PYTHON $PLUGIN_SRC/mcp-playwright/server.py"
        }
        echo -e "${GREEN}✔ MCP server registered for Claude Code${NC}"
    fi
else
    echo -e "  Claude Code CLI not found. Skip auto-register."
    echo "  Manual: claude mcp add --scope user venturo-poster -- $VENV_PYTHON $PLUGIN_SRC/mcp-playwright/server.py"
fi

# ──────────────────────────────────────
# 5. Install for Antigravity (agy) — copy plugin + register
# ──────────────────────────────────────
echo ""
echo -e "${CYAN}--- Antigravity (agy) ---${NC}"

ANTIGRAVITY_PLUGIN_DIR="$HOME/.gemini/config/plugins/venturo-poster"
ANTIGRAVITY_CLI_PLUGIN_DIR="$HOME/.gemini/antigravity-cli/plugins/venturo-poster"

# Remove stale directories
for dir in "$ANTIGRAVITY_PLUGIN_DIR" "$ANTIGRAVITY_CLI_PLUGIN_DIR"; do
    if [ -d "$dir" ]; then
        echo "  Removing old plugin from $dir..."
        rm -rf "$dir"
    fi
done

# Copy plugin
cp -r "$PLUGIN_SRC" "$ANTIGRAVITY_PLUGIN_DIR"
cp -r "$PLUGIN_SRC" "$ANTIGRAVITY_CLI_PLUGIN_DIR"
echo -e "${GREEN}✔ Plugin copied to${NC}"
echo -e "${GREEN}  • $ANTIGRAVITY_PLUGIN_DIR${NC}"
echo -e "${GREEN}  • $ANTIGRAVITY_CLI_PLUGIN_DIR${NC}"

# Create mcp_config.json for Antigravity (uses plugin-local venv structure)
for dir in "$ANTIGRAVITY_PLUGIN_DIR" "$ANTIGRAVITY_CLI_PLUGIN_DIR"; do
    cat > "$dir/mcp_config.json" << MCPEOF
{
  "mcpServers": {
    "venturo-poster": {
      "command": "$VENV_PYTHON",
      "args": ["$dir/mcp-playwright/server.py"],
      "env": {
        "IMAGE_ROUTER_API_KEY": ""
      }
    }
  }
}
MCPEOF
done
echo -e "${GREEN}✔ MCP config registered for Antigravity plugin${NC}"

# ──────────────────────────────────────
# 6. OpenCode — already configured via repo files
# ──────────────────────────────────────
echo ""
echo -e "${CYAN}--- OpenCode ---${NC}"
echo -e "  ${GREEN}✔ Already configured!${NC}"
echo "  • .mcp.json      — auto-load MCP server"
echo "  • AGENTS.md       — project rules"
echo "  • opencode.json   — project config"
echo "  • .claude/skills/ — skill discovery"
echo "  OpenCode auto-reads these at startup."

# ──────────────────────────────────────
# 7. Summary
# ──────────────────────────────────────
echo ""
echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  Install Complete${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""
echo -e "  Engine: Qwen-Image-2.0-Pro (maxrouter.io)"
echo -e "  Python: $VENV_PYTHON"
echo ""
echo -e "  ${YELLOW}⚠ Jangan lupa set API key:${NC}"
echo "    1. cp .env.example .env"
echo "    2. Isi IMAGE_ROUTER_API_KEY di .env"
echo "    Dapatkan di: https://maxrouter.io"
echo ""
echo -e "  ${GREEN}Cara pakai:${NC}"
echo "    Claude Code:  claude  →  'buat katalog WhatsApp'"
echo "    OpenCode:     opencode  →  'buat katalog WhatsApp'"
echo "    Antigravity:  agy  →  'buat katalog WhatsApp'"
echo ""
