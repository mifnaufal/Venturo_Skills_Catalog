param(
    [string]$Target = ""
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PluginDir = Join-Path $ScriptDir "venturo-poster"
$Manifest  = Join-Path $PluginDir "plugin.json"
$InstallMode = "plugin"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Venturo Poster — Antigravity Plugin Install" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path $Manifest)) {
    Write-Host "ERROR: venturo-poster/plugin.json not found." -ForegroundColor Red
    exit 1
}

if ($Target -ne "") {
    switch ($Target) {
        "plugin"  { $Target = "$env:USERPROFILE\.gemini\antigravity-cli\plugins" }
        "skill"   { $Target = "$env:USERPROFILE\.gemini\antigravity-cli\skills"; $InstallMode = "skill" }
    }
}

if ($Target -eq "") {
    Write-Host "Select install mode:"
    Write-Host "  1) Plugin  → ~\.gemini\antigravity-cli\plugins\"
    Write-Host "  2) Skill   → ~\.gemini\antigravity-cli\skills\"
    Write-Host "  3) Project → .agents\skills\ (local)"
    Write-Host "  4) Custom path"
    $choice = Read-Host "Choice [1-4]"
    switch ($choice) {
        "1" { $Target = "$env:USERPROFILE\.gemini\antigravity-cli\plugins" }
        "2" { $Target = "$env:USERPROFILE\.gemini\antigravity-cli\skills"; $InstallMode = "skill" }
        "3" { $Target = ".agents\skills"; $InstallMode = "skill" }
        "4" { $Target = Read-Host "Enter target path" }
        default { Write-Host "Invalid choice." -ForegroundColor Red; exit 1 }
    }
}

$TargetDir = [System.Environment]::ExpandEnvironmentVariables($Target)
New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null

if ($InstallMode -eq "skill") {
    $Dest = Join-Path $TargetDir "venturo-poster.md"
    $Src  = Join-Path $PluginDir "skills\venturo-poster.md"
    if (Test-Path $Dest) {
        $confirm = Read-Host "Skill already exists. Overwrite? [y/N]"
        if ($confirm -ne "y" -and $confirm -ne "Y") { Write-Host "Cancelled."; exit 0 }
    }
    Copy-Item -Path $Src -Destination $Dest
    Write-Host "✔ Skill installed to $Dest" -ForegroundColor Green
} else {
    $Dest = Join-Path $TargetDir "venturo-poster"
    if (Test-Path $Dest) {
        $confirm = Read-Host "Plugin already exists at $Dest. Overwrite? [y/N]"
        if ($confirm -ne "y" -and $confirm -ne "Y") { Write-Host "Cancelled."; exit 0 }
        Remove-Item -Recurse -Force $Dest
    }
    Copy-Item -Recurse -Path $PluginDir -Destination $Dest
    Write-Host "✔ Plugin installed to $Dest" -ForegroundColor Green
    Write-Host "  Register with: agy plugin install $Dest"
}

Write-Host ""
Write-Host "Checking Python dependencies..."
try {
    pip install Pillow 2>&1 | Out-Null
    Write-Host "Dependencies OK." -ForegroundColor Green
} catch {
    Write-Host "Warning: pip install Pillow" -ForegroundColor Yellow
}

$LogoPath = Join-Path $PluginDir "assets\image_1c155d.png"
if (-not (Test-Path $LogoPath)) {
    Write-Host "Warning: Venturo logo not found at $LogoPath" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✔ Venturo Poster Plugin ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Quick start:"
Write-Host "  agy plugin install $Dest"
Write-Host "  agy  →  /venturo-poster"
Write-Host ""
Write-Host "Or use as a standalone skill:"
Write-Host "  .\install.ps1 -Target skill"
