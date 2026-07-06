# Coeus vs `anthropics/knowledge-work-plugins` — Conformance Report

**Reference**: https://github.com/anthropics/knowledge-work-plugins (commit `main`, fetched 2026-06-20).
**Coeus baseline**: v3.3.1.
**Goal**: bring Coeus in line with official plugin conventions; remove bloat; keep only Coeus-specific extensions that solve real problems.

## Reference structure (canonical per official)

A plugin directory in `anthropics/knowledge-work-plugins` contains:

```
<plugin>/
├── .claude-plugin/plugin.json     # Manifest — only 4 keys: name, version, description, author{name}
├── .mcp.json                       # Optional — MCP server bundle (omit if no MCPs)
├── CONNECTORS.md                   # Optional — lists which MCPs the plugin uses (omit if no MCPs)
├── LICENSE                         # Per-plugin license (often plain copy of root LICENSE)
├── README.md                       # Short plugin overview (no install instructions, no badges)
└── skills/
    └── <skill>/
        ├── SKILL.md                # Frontmatter: name, description, argument-hint. Body starts with "# /<skill>"
        ├── LICENSE.txt             # Optional per-skill license (when skill code has its own dependencies)
        ├── references/             # Optional — markdown references used by the skill
        └── scripts/                # Optional — code the skill executes
```

**What official plugins DO NOT have**:
- `commands/` directory — slash commands are auto-registered from each skill's `name` + `argument-hint`
- `hooks/` directory — no per-plugin lifecycle hooks observed
- `scripts/` at *plugin* root — scripts live inside individual skills only
- Top-level `plugin.json` mirror outside `.claude-plugin/`
- Per-plugin `CHANGELOG.md`, `CONTRIBUTING.md`, `CLA.md`, `HANDOVER.md`
- `assets/`, `docs/`, `wiki/` directories
- README badges (no shields.io)

## Discrepancy matrix

Verdict legend: **HARD** = breaks loading or conformance check / **SOFT** = style or bloat / **KEEP** = Coeus-specific need with rationale.

| # | Axis | Reference | Coeus v3.3.1 | Verdict | Action |
|---|---|---|---|---|---|
| 1 | **Manifest schema** | `{name, version, description, author{name}}` | Adds `slug`, `homepage`, `license`, `skills[]`, `hooks`, `tracks_upstream`, `packaging` | SOFT | **Slim** to canonical 4 keys + `homepage`. Move `tracks_upstream` + `packaging` notes to internal docs. |
| 2 | **Root `plugin.json` mirror** | Not present | Present (`./plugin.json` duplicating `.claude-plugin/plugin.json`) | SOFT | **Delete** root copy. `.claude-plugin/plugin.json` is canonical. |
| 3 | **`commands/` directory** | Not present | 6 wrapper `.md` files | SOFT | **Delete** (verify `/coeus:<name>` still resolves via skill auto-registration; revert if Cowork surface needs them) |
| 4 | **`hooks/` directory** | Not present | Cleanup-stale-install hook (SessionStart) | KEEP | Coeus-specific: solves real desktop-app overlay-install bug. **Document** as a deliberate extension. |
| 5 | **Plugin-root `scripts/`** | Not present | `build-plugin.{sh,ps1}` | SOFT | **Move** to `.github/scripts/` or keep at root with a clarifying comment. Decision: keep at root since this IS a single-plugin repo and the script is for repo maintainers. |
| 6 | **`skill_downloader.py`** | Not present | Present | SOFT | **Delete** — install path is now `coeus.plugin` via Add Plugin; the downloader is obsolete since v3.2.0 when the official channel became `release.yml`. |
| 7 | **`assets/coeus-header.jpg`** | Not present | Used only by README header `<img>` tag | SOFT | **Keep** — directly referenced by `README.md` `<img src="assets/...">`. |
| 8 | **`wiki/`** | Not present | 5 files duplicating `docs/EP-Council*.md` | SOFT | **Delete** — wiki content belongs in GitHub Wiki feature, not in the plugin tree. The four `docs/EP-Council*.md` are the canonical copies. |
| 9 | **Plugin-root `CHANGELOG.md`** | Not present per-plugin | Present | SOFT (KEEP for single-plugin repo) | Keep — Coeus is single-plugin; repo root = plugin root. |
| 10 | **Plugin-root `CONTRIBUTING.md`, `CLA.md`** | Not present per-plugin | Present | SOFT (KEEP) | Keep — Coeus is single-plugin repo. |
| 11 | **`Coeus_LLM_HANDOVER.md`** | Not present | Present | KEEP | Coeus-specific extension — explicitly for LLM continuation. Document as extension. |
| 12 | **SKILL.md `description` style** | One-line scalar | `description: >` folded block, multi-paragraph triggers | SOFT | Leave as-is — folded scalars are valid YAML and the multi-paragraph format is more readable for triggers. |
| 13 | **SKILL.md body opening** | Starts with `# /<skill>` heading | Most start with `# SYSTEM SKILL:` or similar | SOFT | Leave — content is well-written; the heading style is a convention not a requirement. |
| 14 | **`author` field shape** | Object `{name: "Anthropic"}` | String `"ENERGEIA SERVICES PTE. LTD."` | SOFT | **Convert** to object form. |
| 15 | **Skill body `LICENSE`/`CONTRIBUTING`/`CLA`/`README` inside `skills/caveman/`** | Per-skill `LICENSE.txt` only when skill is independently licensed | Coeus has 4 extra files inside `skills/caveman/` from upstream JuliusBrussee/caveman | SOFT | **Decide**: the sync workflow excludes these from being overwritten. They're upstream's vendor docs. Move to `skills/caveman/upstream/` subdir or leave — official plugins do allow `LICENSE.txt` per skill. **Keep** as-is, they're scoped to that skill. |
| 16 | **`.github/workflows/sync-upstream-caveman.yml`** | N/A | Present but marked "RETIRED" in comments | HARD-LITE | **Delete** — superseded by `sync-upstream-skills.yml`. Dead workflow file. |

## Plan (fix order)

1. **#16 delete retired workflow** (cleanup)
2. **#6 delete `skill_downloader.py`** (cleanup)
3. **#8 delete `wiki/`** (cleanup)
4. **#2 delete root `plugin.json`** (cleanup; only `.claude-plugin/plugin.json` is canonical)
5. **#1 + #14 slim canonical `plugin.json`** to official schema; move excess fields to `docs/PLUGIN_MANIFEST_EXTENSIONS.md`
6. **#3 delete `commands/`** (test `/coeus:*` still resolves; revert if Cowork breaks)
7. **#4 + #5 + #11 — document Coeus extensions** in `docs/COEUS_EXTENSIONS.md` so the divergence from official is intentional and traceable
8. Update `README.md`, `CHANGELOG.md`, `Coeus_LLM_HANDOVER.md`, `.gitignore`, build script, release workflow to reflect the new layout
9. Conformance script: pass against the official schema

## Out of scope

- The MCP-server `.mcp.json` + `CONNECTORS.md` pattern — Coeus has no bundled MCPs.
- Per-skill `references/`, `scripts/` subdirs — Coeus skills don't currently need them; adding empty ones would be cargo-culting.
