# Coeus -- reproducible local coeus.plugin build (PowerShell wrapper).
#
# Delegates to scripts/build-plugin.py, which is the single source of truth
# for the bundle. Reason: PowerShell's Compress-Archive does NOT set the
# UTF-8 filename flag (0x800) on zip entries, and Claude Cowork's strict
# validator rejects such archives with:
#     "zip file contains path with invalid characters"
# The Python builder writes properly flagged, POSIX-permissioned entries
# that pass both Claude Desktop and Claude Cowork.
#
# Run from the repo root:
#   pwsh .\scripts\build-plugin.ps1     (or powershell .\scripts\build-plugin.ps1)

$ErrorActionPreference = 'Stop'

$RepoRoot = Split-Path -Parent $PSScriptRoot
Push-Location $RepoRoot
try {
  if (-not (Test-Path '.claude-plugin/plugin.json')) {
    throw 'must be run from the Coeus repo root (.claude-plugin/plugin.json not found)'
  }

  $py = $null
  foreach ($name in @('python','python3','py')) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if ($cmd) { $py = $cmd; break }
  }
  if (-not $py) {
    throw 'python not found on PATH -- install Python 3 to build the plugin'
  }

  & $py.Source 'scripts/build-plugin.py'
  if ($LASTEXITCODE -ne 0) { throw "build-plugin.py failed (exit $LASTEXITCODE)" }
}
finally {
  Pop-Location
}
