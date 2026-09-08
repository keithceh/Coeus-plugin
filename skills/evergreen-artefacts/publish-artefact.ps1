# Publish an artefact (any file type, or a folder) to the NAS as an immutable
# version with a stable evergreen link that always shows the latest version.
# Agent-neutral: any LLM/agent/human runs this same script. Contract: HANDOVER.md.
#
# ponytail: set these two defaults once, then verify against Web Station:
#   -Root    = SMB path to the web-served artefacts folder
#   -BaseUrl = the URL Web Station serves that folder at
param(
  [string]$Path,
  [string]$Name,
  [string]$Publisher = "$env:USERNAME@$env:COMPUTERNAME",
  [int]$RevertTo = 0,
  [string]$Root = "\\192.168.0.119\web\artefacts",
  [string]$BaseUrl = "http://192.168.0.119/artefacts"
)
$ErrorActionPreference = "Stop"

function HtmlEnc([string]$s) { [System.Net.WebUtility]::HtmlEncode($s) }

$item = $null
if ($RevertTo) {
  if (-not $Name) { throw "-RevertTo requires -Name to identify the artefact" }
} else {
  if (-not $Path) { throw "Provide -Path to publish, or -Name with -RevertTo to revert" }
  if (-not (Test-Path $Path)) { throw "Not found: $Path" }
  $item = Get-Item $Path
  if (-not $Name) { $Name = [IO.Path]::GetFileNameWithoutExtension($item.Name) }
}
$slug = ($Name.ToLower() -replace '[^a-z0-9]+', '-').Trim('-')
if (-not $slug) { throw "Name '$Name' produces an empty slug" }

$dir = Join-Path $Root $slug
New-Item -ItemType Directory -Force $dir | Out-Null

# Keep the agent-neutral contract next to the data (never overwrite an edited copy).
$handoverSrc = Join-Path $PSScriptRoot 'HANDOVER.md'
$handoverDst = Join-Path $Root 'HANDOVER.md'
if ((Test-Path $handoverSrc) -and -not (Test-Path $handoverDst)) {
  Copy-Item $handoverSrc $handoverDst
}

# Clean stale temp dirs from crashed runs, then pick the next version number.
Get-ChildItem $dir -Directory -Filter '.v*.tmp' | Remove-Item -Recurse -Force
$versions = @(Get-ChildItem $dir -Directory -Filter 'v*' |
  ForEach-Object { if ($_.Name -match '^v(\d+)$') { [int]$Matches[1] } })
$next = if ($versions) { ($versions | Measure-Object -Maximum).Maximum + 1 } else { 1 }

# Copy into a temp dir, then rename — collaborators never see a half-copied version.
# Revert = re-publish old content as a NEW version; nothing is ever deleted.
$tmp = Join-Path $dir ".v$next.tmp"
if ($RevertTo) {
  $src = Join-Path $dir "v$RevertTo"
  if (-not (Test-Path $src)) { throw "No v$RevertTo exists for '$slug'" }
  Copy-Item $src $tmp -Recurse
  Remove-Item (Join-Path $tmp 'publish.json') -ErrorAction SilentlyContinue
} elseif ($item.PSIsContainer) {
  Copy-Item $item.FullName $tmp -Recurse
  if (-not (Test-Path (Join-Path $tmp 'index.html'))) {
    $firstHtml = Get-ChildItem $tmp -Filter *.htm* -File | Select-Object -First 1
    if ($firstHtml) { Copy-Item $firstHtml.FullName (Join-Path $tmp 'index.html') }
  }
} else {
  New-Item -ItemType Directory $tmp | Out-Null
  if ($item.Extension -in '.html', '.htm') { Copy-Item $item.FullName (Join-Path $tmp 'index.html') }
  else { Copy-Item $item.FullName $tmp }
}

# Markdown gets a small in-browser viewer (marked via CDN, <pre> fallback offline).
$md = Get-ChildItem $tmp -Filter *.md -File | Select-Object -First 1
if ($md -and -not (Test-Path (Join-Path $tmp 'index.html'))) {
  $mdUrl = [uri]::EscapeDataString($md.Name)
  @"
<!doctype html><meta charset="utf-8"><title>$slug</title>
<style>body{max-width:52rem;margin:2rem auto;padding:0 1rem;font-family:system-ui,sans-serif;line-height:1.6}</style>
<div id="c">Loading&hellip;</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/12.0.2/marked.min.js"></script>
<script>
fetch('./$mdUrl').then(r => r.text()).then(t => {
  var c = document.getElementById('c');
  if (window.marked) { c.innerHTML = marked.parse(t); }
  else { var p = document.createElement('pre'); p.textContent = t; c.replaceChildren(p); }
});
</script>
"@ | Set-Content (Join-Path $tmp 'index.html') -Encoding utf8
}

# Publish record: attribution + per-file SHA-256 (tamper evidence between collaborators).
$files = Get-ChildItem $tmp -File -Recurse | ForEach-Object {
  [ordered]@{
    path   = $_.FullName.Substring($tmp.Length + 1).Replace('\', '/')
    sha256 = (Get-FileHash $_.FullName -Algorithm SHA256).Hash.ToLower()
    bytes  = $_.Length
  }
}
$record = [ordered]@{
  artefact    = $slug
  version     = "v$next"
  publisher   = $Publisher
  publishedAt = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
  source      = if ($RevertTo) { "revert of v$RevertTo" } else { $item.Name }
}
if ($RevertTo) { $record.revertOf = "v$RevertTo" }
$record.files = @($files)
$record | ConvertTo-Json -Depth 4 | Set-Content (Join-Path $tmp 'publish.json') -Encoding utf8

Rename-Item $tmp (Join-Path $dir "v$next")
$vdir = Join-Path $dir "v$next"

# The evergreen link: a redirect stub that always points at the latest version.
# HTML/MD render in the browser; any other type downloads the latest file.
$target = if (Test-Path (Join-Path $vdir 'index.html')) { "v$next/" }
else {
  $firstFile = Get-ChildItem $vdir -File | Where-Object Name -ne 'publish.json' | Select-Object -First 1
  "v$next/$([uri]::EscapeDataString($firstFile.Name))"
}
@"
<!doctype html><meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=./$target">
<title>$slug</title>
<p><a href="./$target">latest (v$next)</a> &middot; <a href="./versions.html">all versions</a></p>
"@ | Set-Content (Join-Path $dir 'index.html') -Encoding utf8

# Version history page.
$rows = Get-ChildItem $dir -Directory -Filter 'v*' |
  Sort-Object { [int]($_.Name.Substring(1)) } -Descending |
  ForEach-Object { "<li><a href=""./$($_.Name)/"">$($_.Name)</a> &mdash; $($_.LastWriteTime.ToString('yyyy-MM-dd HH:mm')) &mdash; <a href=""./$($_.Name)/publish.json"">record</a></li>" }
@"
<!doctype html><meta charset="utf-8"><title>$(HtmlEnc $slug) versions</title>
<h1>$(HtmlEnc $slug)</h1><ul>
$($rows -join "`n")
</ul>
"@ | Set-Content (Join-Path $dir 'versions.html') -Encoding utf8

# Gallery of all artefacts at the root.
$cards = Get-ChildItem $Root -Directory |
  Sort-Object LastWriteTime -Descending |
  ForEach-Object { "<li><a href=""./$($_.Name)/"">$(HtmlEnc $_.Name)</a></li>" }
@"
<!doctype html><meta charset="utf-8"><title>Artefacts</title>
<h1>Artefacts</h1><ul>
$($cards -join "`n")
</ul>
"@ | Set-Content (Join-Path $Root 'index.html') -Encoding utf8

Write-Host "Evergreen link: $BaseUrl/$slug/"
Write-Host "This version:   $BaseUrl/$slug/v$next/"
