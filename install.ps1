param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PluginSrc = Join-Path $ScriptDir "venturo-poster"
$PluginDir = "$env:USERPROFILE\.gemini\config\plugins\venturo-poster"
$PluginDirCli = "$env:USERPROFILE\.gemini\antigravity-cli\plugins\venturo-poster"
$Manifest  = Join-Path $PluginSrc "plugin.json"
$LogoPath  = Join-Path $PluginSrc "assets\image_1c155d.png"
$McpReq    = Join-Path $PluginSrc "mcp-playwright\requirements.txt"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Venturo Poster — Antigravity Plugin Install" -ForegroundColor Cyan
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

# 2. Remove stale plugin directories
$dirs = @($PluginDir, $PluginDirCli)
foreach ($dir in $dirs) {
    if (Test-Path $dir) {
        Write-Host "  Removing old plugin from $dir..."
        Remove-Item -Recurse -Force $dir
    }
}

# 3. Copy fresh plugin
New-Item -ItemType Directory -Path (Split-Path $PluginDir -Parent) -Force | Out-Null
New-Item -ItemType Directory -Path (Split-Path $PluginDirCli -Parent) -Force | Out-Null
Copy-Item -Recurse -Path $PluginSrc -Destination $PluginDir
Copy-Item -Recurse -Path $PluginSrc -Destination $PluginDirCli
Write-Host "✔ Plugin copied to:" -ForegroundColor Green
Write-Host "  • $PluginDir" -ForegroundColor Green
Write-Host "  • $PluginDirCli" -ForegroundColor Green

# 4. Install MCP + Playwright dependencies
Write-Host ""
Write-Host "  Installing Python dependencies..."
try {
    pip install -r $McpReq 2>&1 | Out-Null
    Write-Host "✔ Python dependencies installed" -ForegroundColor Green
} catch {
    Write-Host "  pip install failed: $_" -ForegroundColor Yellow
    Write-Host "  Run manually: pip install -r $McpReq" -ForegroundColor Yellow
}

# 5. Install Chromium
Write-Host ""
Write-Host "  Installing Chromium browser..."
try {
    $check = python -c "from playwright.sync_api import sync_playwright; print('OK')" 2>&1
    if ($check -eq "OK") {
        Write-Host "✔ Playwright ready" -ForegroundColor Green
    } else {
        playwright install chromium 2>&1 | Out-Null
        Write-Host "✔ Chromium installed" -ForegroundColor Green
    }
} catch {
    Write-Host "  Run: playwright install chromium" -ForegroundColor Yellow
}

# 6. Show MCP config instructions
$ServerPath = Resolve-Path (Join-Path $PluginSrc "mcp-playwright\server.py")
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  MCP Server Configuration" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Tambahkan ke Antigravity config (~\.gemini\config\antigravity.json):"
Write-Host ""
Write-Host '  {'
Write-Host '    "mcpServers": {'
Write-Host '      "venturo-poster-playwright": {'
Write-Host '        "command": "python",'
Write-Host "        `"args`": [`"$ServerPath`"],"
Write-Host '        "env": {}'
Write-Host '      }'
Write-Host '    }'
Write-Host '  }'
Write-Host ""

# 7. Done
Write-Host "✔ Venturo Poster — siap digunakan!" -ForegroundColor Green
Write-Host ""
Write-Host "Cara pakai:"
Write-Host "  agy"
Write-Host "  → ketik: /venturo-poster"
Write-Host "  → atau:  buat katalog WhatsApp buat Venturo"
Write-Host ""
