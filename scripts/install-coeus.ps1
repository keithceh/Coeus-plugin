# Coeus one-line installer (Windows / PowerShell)
#
# Usage from any terminal:
#   iwr https://raw.githubusercontent.com/keithceh/Coeus-plugin/main/install-coeus.ps1 | iex
#
# Sets up Coeus across the three Claude surfaces in one pass:
#   1. Claude Code (CLI)   -- /plugin install via marketplace
#   2. Cowork              -- downloads .skill files to Downloads\Coeus-skills\
#                             and opens the folder for drag-into-chat
#   3. Claude Desktop chat -- downloads paste prompts to the same folder
#
# Anthropic doesn't share a plugin runtime across these three surfaces, so a
# truly single-install path isn't structurally possible today. This script
# does the next-best thing: one command, every surface ready.

$ErrorActionPreference = 'Stop'

$Mirror    = 'keithceh/Coeus-plugin'
$Release   = "https://api.github.com/repos/$Mirror/releases/latest"
$DropDir   = Join-Path $env:USERPROFILE 'Downloads\Coeus-skills'

Write-Host ""
Write-Host "Coeus installer" -ForegroundColor Cyan
Write-Host "==============="

# --- 1. Claude Code (CLI) ----------------------------------------------------
$claude = Get-Command claude -ErrorAction SilentlyContinue
if ($claude) {
    Write-Host "`n[1/3] Claude Code: installing via marketplace..." -ForegroundColor Yellow
    Write-Host "      Run inside a claude session:" -ForegroundColor DarkGray
    Write-Host "        /plugin marketplace add $Mirror"
    Write-Host "        /plugin install coeus@coeus"
    Write-Host "        /reload-plugins"
} else {
    Write-Host "`n[1/3] Claude Code: 'claude' not on PATH -- skipping." -ForegroundColor DarkYellow
    Write-Host "      Install Claude Code first: https://docs.claude.com/en/docs/claude-code/setup"
}

# --- 2 + 3. Download .skill + paste artifacts for Cowork / Desktop -----------
Write-Host "`n[2/3] Cowork + [3/3] Desktop chat: fetching latest release artifacts..." -ForegroundColor Yellow

New-Item -ItemType Directory -Force -Path $DropDir | Out-Null

try {
    $rel = Invoke-RestMethod -Uri $Release -Headers @{ 'User-Agent' = 'coeus-installer' }
} catch {
    Write-Host "      Could not reach $Release" -ForegroundColor Red
    Write-Host "      The public mirror may not be bootstrapped yet. Skipping artifact download."
    return
}

$wanted = @('.skill', '.paste.md', 'coeus.plugin')
$assets = $rel.assets | Where-Object {
    $n = $_.name
    $wanted | Where-Object { $n.EndsWith($_) }
}

foreach ($a in $assets) {
    $out = Join-Path $DropDir $a.name
    Write-Host ("      -> {0}" -f $a.name) -ForegroundColor DarkGray
    Invoke-WebRequest -Uri $a.browser_download_url -OutFile $out -UseBasicParsing
}

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host "  .skill files (drag into Cowork chat): $DropDir"
Write-Host "  .paste.md files (paste into Desktop chat): $DropDir"
Write-Host ""

# Open the folder so the user can drag straight from Explorer.
Start-Process explorer.exe $DropDir
