param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PluginSrc = Join-Path $ScriptDir "venturo-poster"
$PluginDir = "$env:USERPROFILE\.gemini\config\plugins\venturo-poster"
$PluginDirCli = "$env:USERPROFILE\.gemini\antigravity-cli\plugins\venturo-poster"
$VenvDir   = Join-Path $PluginDir ".venv"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$VenvPip   = Join-Path $VenvDir "Scripts\pip.exe"
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

# 4. Create Python virtual environment
Write-Host ""
Write-Host "  Creating Python virtual environment..."
python -m venv $VenvDir
Write-Host "✔ Virtual environment created at $VenvDir" -ForegroundColor Green

# 5. Install MCP + Playwright dependencies
$InstalledReq = Join-Path $PluginDir "mcp-playwright/requirements.txt"
Write-Host ""
Write-Host "  Installing Python dependencies..."
& $VenvPip install -r $InstalledReq
if ($LASTEXITCODE -ne 0) {
    Write-Host "  pip install failed" -ForegroundColor Yellow
    Write-Host "  Run manually: $VenvPip install -r $InstalledReq" -ForegroundColor Yellow
} else {
    Write-Host "✔ Python dependencies installed" -ForegroundColor Green
}

# 6. Install Chromium
Write-Host ""
Write-Host "  Installing Chromium browser..."
try {
    $check = & $VenvPython -c "from playwright.sync_api import sync_playwright; print('OK')" 2>&1
    if ($check -eq "OK") {
        Write-Host "✔ Playwright ready" -ForegroundColor Green
    } else {
        & $VenvPython -m playwright install chromium 2>&1 | Out-Null
        Write-Host "✔ Chromium installed" -ForegroundColor Green
    }
} catch {
    Write-Host "  Run: $VenvPython -m playwright install chromium" -ForegroundColor Yellow
}

# 7. Create mcp_config.json for auto-MCP registration
Write-Host ""
Write-Host "  Registering MCP server..."
$mcpDirs = @($PluginDir, $PluginDirCli)
foreach ($d in $mcpDirs) {
    $mcpConfig = Join-Path $d "mcp_config.json"
    $serverPy  = Join-Path $d "mcp-playwright/server.py"
    @"
{
  "mcpServers": {
    "venturo-poster-playwright": {
      "command": "$VenvPython",
      "args": ["$serverPy"],
      "env": {}
    }
  }
}
"@ | Set-Content -Path $mcpConfig
}
Write-Host "✔ MCP config registered for plugin" -ForegroundColor Green

# 8. Show MCP status
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  MCP Server Auto-Registered" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Plugin mcp_config.json sudah dibuat di:"
Write-Host "    $PluginDir\mcp_config.json"
Write-Host "    $PluginDirCli\mcp_config.json"
Write-Host ""
Write-Host "  Menggunakan Python: $VenvPython"
Write-Host ""
Write-Host "  Antigravity akan auto-load MCP server saat plugin aktif."
Write-Host ""
Write-Host "  Jika ingin manual, tambahkan ke antigravity.json:"
Write-Host '  {'
Write-Host '    "mcpServers": {'
Write-Host '      "venturo-poster-playwright": {'
Write-Host "        \`"command\`": \`"$VenvPython\`","
Write-Host "        \`"args\`": [\`"$PluginDir\mcp-playwright\server.py\`"],"
Write-Host '        "env": {}'
Write-Host '      }'
Write-Host '    }'
Write-Host '  }'
Write-Host ""
Write-Host "  Verifikasi: agy plugin list"
Write-Host ""

# 9. Done
Write-Host "✔ Venturo Poster — siap digunakan!" -ForegroundColor Green
Write-Host ""
Write-Host "Cara pakai:"
Write-Host "  agy"
Write-Host "  → ketik: /venturo-poster"
Write-Host "  → atau:  buat katalog WhatsApp buat Venturo"
Write-Host ""
