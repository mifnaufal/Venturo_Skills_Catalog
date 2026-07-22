param()

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PluginSrc = Join-Path $ScriptDir "venturo-poster"
$PluginDir = "$env:USERPROFILE\.gemini\antigravity-cli\plugins\venturo-poster"
$Manifest  = Join-Path $PluginSrc "plugin.json"
$LogoPath  = Join-Path $PluginSrc "assets\image_1c155d.png"

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

# 2. Remove stale plugin
if (Test-Path $PluginDir) {
    Write-Host "Removing old plugin..."
    Remove-Item -Recurse -Force $PluginDir
}

# 3. Copy fresh plugin
New-Item -ItemType Directory -Path (Split-Path $PluginDir -Parent) -Force | Out-Null
Copy-Item -Recurse -Path $PluginSrc -Destination $PluginDir
Write-Host "✔ Plugin copied to $PluginDir" -ForegroundColor Green

# 4. Register via agy
Write-Host ""
Write-Host "Registering plugin..."
$output = & agy plugin install "$PluginDir" 2>&1 | Out-String
Write-Host $output

# 5. Install Playwright
Write-Host "Installing Python dependencies..."
try {
    pip install playwright 2>&1 | Out-Null
    $check = python -c "from playwright.sync_api import sync_playwright; print('OK')" 2>&1
    if ($check -eq "OK") {
        Write-Host "✔ Playwright ready" -ForegroundColor Green
    } else {
        Write-Host "Installing Playwright browsers..."
        python -m playwright install chromium 2>&1 | Out-Null
    }
} catch {
    Write-Host "Run: pip install playwright && playwright install chromium" -ForegroundColor Yellow
}

# 6. Done
Write-Host ""
Write-Host "✔ Venturo Poster — siap digunakan!" -ForegroundColor Green
Write-Host ""
Write-Host "Cara pakai:"
Write-Host "  agy"
Write-Host "  → ketik: /venturo-poster"
Write-Host "  → atau:  buat katalog WhatsApp buat Venturo"
Write-Host ""
