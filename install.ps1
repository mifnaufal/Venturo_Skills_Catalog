param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PluginSrc = Join-Path $ScriptDir "venturo-poster"
$VenvDir   = Join-Path $ScriptDir ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvPip   = Join-Path $VenvDir "Scripts\pip.exe"
$Manifest  = Join-Path $PluginSrc "plugin.json"
$LogoPath  = Join-Path $PluginSrc "assets\image_1c155d.png"
$McpReq    = Join-Path $PluginSrc "mcp-playwright\requirements.txt"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Venturo Poster — Multi-Platform Install" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# 1. Validate
if (-not (Test-Path $Manifest)) {
    Write-Host "ERROR: venturo-poster/plugin.json not found" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $LogoPath)) {
    Write-Host "ERROR: assets/image_1c155d.png not found" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $McpReq)) {
    Write-Host "ERROR: mcp-playwright/requirements.txt not found" -ForegroundColor Red
    exit 1
}

# 2. Install Python dependencies (shared venv)
Write-Host ""
Write-Host "  Creating Python virtual environment..."
python -m venv $VenvDir 2>&1 | Out-Null
Write-Host "✔ Virtual environment at $VenvDir" -ForegroundColor Green

Write-Host ""
Write-Host "  Installing Python dependencies..."
& $VenvPip install -r $McpReq 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "  pip install failed" -ForegroundColor Yellow
    Write-Host "  Run manually: $VenvPip install -r $McpReq" -ForegroundColor Yellow
} else {
    Write-Host "✔ Python dependencies installed" -ForegroundColor Green
}

# 3. Register for Claude Code
Write-Host ""
Write-Host "--- Claude Code ---" -ForegroundColor Cyan
$claudeCmd = Get-Command "claude" -ErrorAction SilentlyContinue
if ($claudeCmd) {
    Write-Host "  Claude Code CLI found. Register manually:"
    Write-Host "    claude mcp add --scope user venturo-poster -- $VenvPython $PluginSrc\mcp-playwright\server.py"
} else {
    Write-Host "  Claude Code CLI not found. Skip."
    Write-Host "  Manual: claude mcp add --scope user venturo-poster -- $VenvPython $PluginSrc\mcp-playwright\server.py"
}

# 4. Install for Antigravity (agy)
Write-Host ""
Write-Host "--- Antigravity (agy) ---" -ForegroundColor Cyan

$PluginDir = "$env:USERPROFILE\.gemini\config\plugins\venturo-poster"
$PluginDirCli = "$env:USERPROFILE\.gemini\antigravity-cli\plugins\venturo-poster"

# Remove stale
$dirs = @($PluginDir, $PluginDirCli)
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Host "  Removing old plugin from $dir..."
        Remove-Item -Recurse -Force $dir
    }
}

# Copy plugin
New-Item -ItemType Directory -Path (Split-Path $PluginDir -Parent) -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $PluginDirCli -Parent) -Force | Out-Null
Copy-Item -Recurse -Path $PluginSrc -Destination $PluginDir
Copy-Item -Recurse -Path $PluginSrc -Destination $PluginDirCli
Write-Host "✔ Plugin copied to:" -ForegroundColor Green
Write-Host "  • $PluginDir" -ForegroundColor Green
Write-Host "  • $PluginDirCli" -ForegroundColor Green

# Create mcp_config.json
$mcpDirs = @($PluginDir, $PluginDirCli)
foreach ($d in $mcpDirs) {
    $mcpConfig = Join-Path $d "mcp_config.json"
    $serverPy  = Join-Path $d "mcp-playwright/server.py"
    @"
{
  "mcpServers": {
    "venturo-poster": {
      "command": "$VenvPython",
      "args": ["$serverPy"],
      "env": {
        "IMAGE_ROUTER_API_KEY": ""
      }
    }
  }
}
"@ | Set-Content -Path $mcpConfig
}
Write-Host "✔ MCP config registered for Antigravity plugin" -ForegroundColor Green

# 5. OpenCode
Write-Host ""
Write-Host "--- OpenCode ---" -ForegroundColor Cyan
Write-Host "✔ Already configured!" -ForegroundColor Green
Write-Host "  • .mcp.json      — auto-load MCP server"
Write-Host "  • AGENTS.md       — project rules"
Write-Host "  • opencode.json   — project config"
Write-Host "  • .claude/skills/ — skill discovery"

# 6. Summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Install Complete" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Engine: Qwen-Image-2.0-Pro (maxrouter.io)"
Write-Host "  Python: $VenvPython"
Write-Host ""
Write-Host "  ⚠ Jangan lupa set API key:" -ForegroundColor Yellow
Write-Host "    1. Copy .env.example to .env"
Write-Host "    2. Isi IMAGE_ROUTER_API_KEY"
Write-Host "    Dapatkan di: https://maxrouter.io"
Write-Host ""
Write-Host "  Cara pakai:" -ForegroundColor Green
Write-Host "    Claude Code:  claude  →  'buat katalog WhatsApp'"
Write-Host "    OpenCode:     opencode  →  'buat katalog WhatsApp'"
Write-Host "    Antigravity:  agy  →  'buat katalog WhatsApp'"
Write-Host ""
