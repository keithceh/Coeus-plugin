# Coeus plugin manifest — extensions outside the official schema

The canonical Claude Code plugin manifest schema (per `anthropics/knowledge-work-plugins`)
contains only four keys: `name`, `version`, `description`, `author`. Coeus historically
carried additional fields in `plugin.json` to encode upstream-tracking provenance,
packaging instructions, and a literal `skills[]` array.

As of **v3.4.0**, the canonical manifest at `.claude-plugin/plugin.json` is slim and
spec-compliant. This document preserves the displaced metadata for maintainers.

## Upstream-tracked skills

Two Coeus skills are vendored from public upstream repositories. They are auto-synced
weekly by `.github/workflows/sync-upstream-skills.yml` and bundled fresh on every
release by `.github/workflows/release.yml`.

| Coeus skill | Upstream source | Branch | Upstream path | Local path |
|---|---|---|---|---|
| `caveman` | https://github.com/JuliusBrussee/caveman | `main` | `skills/caveman` | `skills/caveman` |
| `prompt-master` | https://github.com/nidhinjs/prompt-master | `main` | `.` (repo root) | `skills/prompt-master` |

`prompt-master` latest known version: **1.7.0**. Required by `morpheus` and `the-architect`.

The sync workflow includes a post-sync normalisation step that pins each skill's
frontmatter `name:` field to the Coeus folder name, so upstream renames don't break
slash-command resolution.

## Packaging

The plugin bundle (`coeus.plugin`) is a ZIP containing the canonical layout. Build it
with the reproducible script:

```bash
bash scripts/build-plugin.sh
# or, on Windows:
powershell .\scripts\build-plugin.ps1
```

Output: `dist/coeus.plugin`. The ZIP contents are:

```
.claude-plugin/plugin.json
skills/<6 skills>/...
hooks/{hooks.json, cleanup-stale-install.sh, cleanup-stale-install.ps1}
scripts/build-plugin.{sh,ps1}
README.md, CHANGELOG.md, Coeus_LLM_HANDOVER.md, CONTRIBUTING.md, CLA.md, LICENSE
```

Manual one-liner (mirrors the build script):

```bash
zip -r coeus.plugin \
  .claude-plugin/ skills/ hooks/ scripts/ \
  README.md CHANGELOG.md Coeus_LLM_HANDOVER.md CONTRIBUTING.md CLA.md LICENSE
```

```powershell
Compress-Archive -Path .claude-plugin,skills,hooks,scripts,README.md,CHANGELOG.md,Coeus_LLM_HANDOVER.md,CONTRIBUTING.md,CLA.md,LICENSE -DestinationPath coeus.plugin
```

## Skills enumeration

Auto-discovered from `skills/`. The six skills are:

- `caveman` — token-compression mode
- `ep-council` — adversarial 9-supermajor E&P decision council
- `llm-council` — multi-LLM consensus + tri-team red-team
- `morpheus` — prompt-engineering + caveman compression pipeline
- `prompt-master` — precision prompt engineering for 25+ AI tools
- `the-architect` — adaptive combo chaining prompt-master → caveman → council
