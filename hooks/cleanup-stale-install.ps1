# Coeus — clean-install hook (PowerShell mirror of cleanup-stale-install.sh)
#
# Use this on Windows if the plugin runtime invokes a PS hook instead of the
# bash one. Same behaviour: purges anything outside the canonical v3.x layout
# from the plugin install root, idempotent per version.

$ErrorActionPreference = 'Stop'

$Root = if ($env:CLAUDE_PLUGIN_ROOT) {
  $env:CLAUDE_PLUGIN_ROOT
} else {
  Split-Path -Parent $PSScriptRoot
}

if (-not (Test-Path (Join-Path $Root '.claude-plugin/plugin.json'))) {
  # Soft-skip: not a real plugin install dir. Use Write-Host (not Write-Error)
  # so $LASTEXITCODE stays 0 and Claude Cowork's hook runner does not flag
  # this as a hook failure — the bash counterpart does the same via `echo >&2`.
  [Console]::Error.WriteLine("[coeus] cleanup-stale-install: not a plugin install; skipping")
  exit 0
}

# Guard 2: refuse to run inside a git repo. Install dirs never contain .git;
# source repos do. Caught a real incident in v3.7.x where running the hook
# against the source tree wiped .git, .github, dist, index.html, vercel.json.
if ((Test-Path (Join-Path $Root '.git')) -or (Test-Path (Join-Path $Root '.github'))) {
  [Console]::Error.WriteLine("[coeus] cleanup-stale-install: refusing to run inside a git repo (.git or .github present); skipping")
  exit 0
}

$manifest = Get-Content (Join-Path $Root '.claude-plugin/plugin.json') -Raw | ConvertFrom-Json
$version = $manifest.version
$marker = Join-Path $Root ".coeus-cleaned-$version"

if (Test-Path $marker) { exit 0 }

$keep = @(
  '.claude-plugin','skills','hooks','scripts','docs','assets',
  'README.md','CHANGELOG.md','CONTRIBUTING.md','CLA.md','LICENSE','Coeus_LLM_HANDOVER.md',
  '.gitattributes','.gitignore'
)

$removed = 0
$currentMarkerName = (Split-Path -Leaf $marker)
Get-ChildItem -LiteralPath $Root -Force | ForEach-Object {
  # Keep ONLY the current-version marker. Old version markers from prior
  # upgrades are treated as stale and removed so they do not accumulate.
  if ($_.Name -eq $currentMarkerName) { return }
  if ($keep -notcontains $_.Name) {
    Remove-Item -LiteralPath $_.FullName -Recurse -Force
    Write-Host "[coeus] cleanup-stale-install: removed stale '$($_.Name)'"
    $script:removed++
  }
}

New-Item -ItemType File -Path $marker -Force | Out-Null

if ($removed -gt 0) {
  Write-Host "[coeus] cleanup-stale-install: $removed stale entries removed for v$version"
}

# Opt-in available-skills banner. Default OFF -- enable with $env:COEUS_STARTUP_BANNER='1'
# in the shell that launches Claude. Plain ASCII, single line via Write-Host
# (NOT Write-Error -- see v3.3.1 fix where Write-Error flipped exit code under
# ErrorActionPreference=Stop). Write-Host is the safe stdout path.
if ($env:COEUS_STARTUP_BANNER -eq '1') {
  $skillsDir = Join-Path $root 'skills'
  if (Test-Path $skillsDir) {
    $skills = (Get-ChildItem -Path $skillsDir -Directory | Where-Object { $_.Name -notlike '_*' } | Sort-Object Name | ForEach-Object { $_.Name }) -join ', '
    Write-Host "[coeus v$version] available skills: $skills"
  }
}

exit 0
