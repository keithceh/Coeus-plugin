# Plugin Build Recipes (shared)

> Build-script templates for spec-compliant Claude plugins. Used by `plugin-creator` Phase 4 (fires once per plugin scaffold). Load when generating the scripts directory.

---

## `scripts/build-plugin.sh` (Bash)

```sh
#!/usr/bin/env bash
set -eu
NAME="$(jq -r .name .claude-plugin/plugin.json)"
OUT="dist/${NAME}.plugin"
mkdir -p dist
rm -f "$OUT"
zip -r "$OUT" .claude-plugin skills hooks scripts README.md CHANGELOG.md LICENSE 2>/dev/null
echo "built $OUT"
```

---

## `scripts/build-plugin.ps1` (PowerShell — `Compress-Archive` rejects `.plugin`)

```powershell
$ErrorActionPreference = 'Stop'
$name = (Get-Content .claude-plugin/plugin.json | ConvertFrom-Json).name
$zip  = "dist/$name.zip"
$out  = "dist/$name.plugin"
New-Item -ItemType Directory -Force dist | Out-Null
Remove-Item -Force -ErrorAction SilentlyContinue $zip, $out
Compress-Archive -Path .claude-plugin, skills, hooks, scripts, README.md, CHANGELOG.md, LICENSE -DestinationPath $zip
Move-Item $zip $out
Write-Host "built $out"
```

---

## Notes

- **Cowork compatibility:** `Compress-Archive` does NOT set the 0x800 UTF-8 filename flag. Cowork validators may reject. Prefer a Python builder (subclass `ZipInfo` to override `_encodeFilenameFlags`) for production — see Coeus's own `scripts/build-plugin.py` for reference.
- **POSIX permissions:** set `external_attr = mode << 16` and `create_system = 3` for `.sh` / `.ps1` / `.py` (0o755 mode) so they survive unzip on Unix.
