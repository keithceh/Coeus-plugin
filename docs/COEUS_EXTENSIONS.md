# Coeus extensions beyond the official plugin spec

Coeus diverges from `anthropics/knowledge-work-plugins` in three deliberate ways. Each
extension exists because it solves a problem the official plugins do not face. Anything
not listed here that diverges from the official spec is a bug to be fixed.

## 1. `hooks/` — SessionStart cleanup hook

**What**: `hooks/hooks.json` registers a SessionStart hook that runs
`hooks/cleanup-stale-install.sh` (with a PowerShell mirror at `.ps1`) once per version.

**Why it exists**: Claude Desktop's "Add Plugin" performs an *overlay extract* — the new
ZIP's files are written over the existing install dir, but files that have been
*removed* between versions persist as stale leftovers. Without the hook, every upgrade
would leave behind the prior version's obsolete files (root-level `*.skill` baselines,
retired skill folders, renamed docs).

**What it does**: On the first session after an in-place upgrade:
1. Confirms it's running inside a real Coeus install (refuses if `.claude-plugin/plugin.json` is missing — safety guard).
2. Reads the current version from the manifest.
3. Writes `.coeus-cleaned-<version>` marker; if it already exists, exits early.
4. Iterates the install root and removes anything not in the canonical whitelist.
5. Garbage-collects old-version `.coeus-cleaned-*` markers.

**Whitelist** (any future addition to the canonical layout MUST also be added here):
`.claude-plugin`, `skills`, `hooks`, `scripts`, `docs`, `assets`,
`plugin.json`, `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CLA.md`, `LICENSE`,
`Coeus_LLM_HANDOVER.md`, `.gitattributes`, `.gitignore`.

**Official plugins don't need this** because their install path (Cowork plugin marketplace)
handles upgrades atomically. The desktop-app upload path that Coeus uses does not.

## 2. `Coeus_LLM_HANDOVER.md` — LLM cold-start brief

**What**: A single document at repo root describing the plugin's architecture, install
paths, packaging steps, and the rationale for every prior version's restructure.

**Why it exists**: Coeus is iterated frequently by an LLM (Claude). Each new session
otherwise has to re-derive the layout from scratch, which wastes tokens and risks
contradicting prior decisions. The handover acts as a deterministic context anchor.

**Mirror**: A snapshot is kept at
`//192.168.0.119/Big_Data_II/Claude/Archives/Coeus_LLM_HANDOVER.md` for offline reference.

## 3. Upstream-tracked skills (`caveman`, `prompt-master`)

**What**: Two of the six skills are vendored from public upstream repos and auto-synced
weekly by `.github/workflows/sync-upstream-skills.yml`, bundled fresh on every release
by `.github/workflows/release.yml`.

**Why it exists**: Official Anthropic plugins are authored entirely by Anthropic. Coeus
intentionally bundles two community-authored skills (`JuliusBrussee/caveman` and
`nidhinjs/prompt-master`) because they are dependencies of Coeus's `morpheus` and
`the-architect` skills. Bundling means end users get one install instead of three.

See `docs/PLUGIN_MANIFEST_EXTENSIONS.md` for the upstream provenance table.

---

## What is NOT a Coeus extension

These divergences from official were accidental and have been removed (v3.4.0):

- ~~`commands/` directory~~ — wrapper `.md` files were redundant. Skills auto-register as `/coeus:<skill>` from their SKILL.md `name` field.
- ~~Root-level `plugin.json` mirror~~ — only `.claude-plugin/plugin.json` is canonical.
- ~~`wiki/`~~ — duplicated `docs/EP-Council*.md`; the GitHub Wiki feature is the right home for that content.
- ~~`skill_downloader.py`~~ — obsolete once the official install path became `coeus.plugin` via "Add Plugin".
- ~~Extra `plugin.json` keys (`slug`, `homepage`, `license`, `skills[]`, `hooks`, `tracks_upstream`, `packaging`)~~ — moved to `docs/PLUGIN_MANIFEST_EXTENSIONS.md`. The canonical manifest now matches the official 4-key schema.
