# Plugin-Creator — Ideas Into Installable Plugins

> The Autobot Transformer — converts a raw idea, prompt, workflow, or skill folder into a spec-compliant Claude Code / Cowork plugin bundle. Encodes the knowledge-work-plugins standard plus Coeus's own conformance lessons: 4-key manifest, SKILL.md auto-registration, UTF-8 hygiene.

**Version:** 1.0 (current) | **Triggers:** `/plugin-creator` · `/plugin-quick [name]` · `"plugin this"` · `"make plugin"` · `"autobot transform"` · `"package this as a plugin"` · `"turn this into a plugin"` · `"scaffold a plugin"`

---

## What This Is

Plugin-Creator's output is a directory tree and a built `<name>.plugin` ZIP that installs cleanly via Claude Desktop **Settings → Capabilities → Customize → Add Plugin** on any machine. The reference standard is `https://github.com/anthropics/knowledge-work-plugins` — every choice the skill makes should trace either to that standard or to a documented Coeus-style extension (a cleanup hook, a vendored upstream skill, an LLM handover note).

### Inputs It Accepts

| Input type | Treatment |
|---|---|
| Single prompt / persona | One skill: `skills/<kebab-name>/SKILL.md` |
| Workflow with steps | One skill with phased structure, mirroring the `llm-council` pattern |
| Multiple related prompts | Multi-skill plugin: one folder per skill under `skills/` |
| Existing folder of `.md` files | Each file audited — becomes a SKILL.md if it has a clear trigger, else becomes a `references/*.md` |
| Existing non-spec plugin | Conformance audit + migration (see migration table below) |

Plugin-Creator asks the user at most 3–5 questions during intake: plugin name (lowercase-kebab), author (name + optional URL), a one-paragraph description, trigger phrases per skill, and whether a SessionStart cleanup hook is needed (default no — only add one if the plugin will be re-uploaded via Desktop "Add Plugin", since overlay-extract installs leave stale files behind without one).

**Express lane:** `/plugin-quick [name]`, or handing it a single prompt, skips discovery and produces a minimum-viable plugin — `.claude-plugin/plugin.json` + `skills/<name>/SKILL.md` + `README.md` — with the build artifact optional.

---

## The Conformance Standard

Plugin-Creator encodes `anthropics/knowledge-work-plugins` as a canonical layout it generates exactly:

```
<plugin-name>/
├── .claude-plugin/
│   └── plugin.json              # CANONICAL manifest — 4 keys only
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md             # frontmatter: name, version, argument-hint, description
│       └── references/          # optional supporting docs the skill reads
├── hooks/                       # OPTIONAL — only if cleanup or lifecycle needed
├── scripts/                     # OPTIONAL — reproducible local build
├── README.md
├── CHANGELOG.md
└── LICENSE
```

No `commands/` directory (deprecated — slash commands auto-register from each `SKILL.md`'s `name:` field, which must equal the folder name or the command will not resolve). No root-level `plugin.json` mirror. The manifest itself is exactly 4 keys — `name`, `version`, `description`, `author` (an object with at least `name`) — with any other metadata routed to a docs note instead of the manifest.

---

## Build and Validation Steps

Six phases, run in order, each a failable gate:

1. **Intake & Classification** — determine input type, ask the intake questions.
2. **Canonical Layout** — generate the tree above; write the 4-key manifest and every `SKILL.md`'s frontmatter (`name`, `version`, `argument-hint`, `description` with at least one `Trigger on:` line, `dependencies`).
3. **Optional Cleanup Hook** — only for plugins meant for repeated Desktop re-upload. The cleanup script must read the version from `plugin.json`, refuse to run if that file is missing (defense against wiping the wrong directory), check for a `.<plugin>-cleaned-<version>` marker before acting, remove anything off the whitelist, garbage-collect older markers, and write the new one. PowerShell scripts must use `[Console]::Error.WriteLine` rather than `Write-Error`, since the latter exits non-zero under `$ErrorActionPreference='Stop'` and breaks the session.
4. **Build Scripts** — `scripts/build-plugin.sh` / `.ps1`, generated from the shared recipes in [`skills/_shared/plugin_build_recipes.md`](../skills/_shared/plugin_build_recipes.md); for production-grade builds the skill points users at Coeus's own `scripts/build-plugin.py` (a `Utf8ZipInfo` subclass) as the only fully Cowork-safe builder.
5. **Conformance Check (failable)** — before declaring done, Plugin-Creator runs a checklist covering: the manifest parses and has only the 4 canonical keys; `author` is an object; no root-level manifest mirror; no `commands/` directory; every `SKILL.md`'s frontmatter parses and its `name:` matches its folder; every skill has a `description:` with a `Trigger on:` line and an `argument-hint:`; no UTF-8 BOM on any `SKILL.md`; no CRLF line endings on any `.sh`; every `hooks.json` command resolves to a real file; and the built `.plugin` unzips back to the same tree. A Python conformance-harness template mirroring the Coeus harness (45 assertions) is available at `references/conformance_check.py`. Each check must pass; failures are fixed and re-run, never self-attested.
6. **Documentation** — a concise `README.md` (what it does, both install options, a skills table with slash commands and triggers, license, repo link), a Keep-a-Changelog-style `CHANGELOG.md`, and a `LICENSE` (MIT by default unless the user specifies otherwise).

### Migration Patterns for Existing Non-Spec Plugins

| Smell | Fix |
|---|---|
| Skills at repo root | `git mv <skill>/ skills/<skill>/` |
| Root-level `plugin.json` mirror | Delete; keep only `.claude-plugin/plugin.json` |
| `commands/<x>.md` wrappers | Delete; ensure each `SKILL.md` has `argument-hint:` + a `Trigger on:` line |
| `name:` doesn't match folder | Rename one to match the other |
| Manifest has `skills[]`, `hooks`, `slug`, etc. | Strip to 4 canonical keys; move displaced metadata to a docs note |
| `author: "Name"` (string) | Convert to `author: {name: "Name", url: "..."}` |
| Re-upload leaves stale files | Add a SessionStart cleanup hook |
| Build artifacts committed to git | Add `*.plugin`, `*.skill`, `dist/` to `.gitignore` |

---

## Lessons Encoded from Coeus's Own Conformance History

Plugin-Creator's Phase 5 checklist and the migration table above are not abstract — they are the fixes Coeus's own repository needed at various points, folded back in so a new plugin never repeats them:

- The **4-key manifest** and **no-`commands/`** rules trace directly to Coeus's own v3.0/v3.1 restructure onto the canonical `skills/<name>/SKILL.md` layout.
- The **frontmatter `name:` must equal the folder name** rule traces to a real Coeus bug: `LLM-council` and `caveman-protocol` didn't match their folders, so `/coeus:caveman` and `/coeus:llm-council` failed to resolve on install.
- The **description-cannot-contain-XML-tags** lesson is load-bearing enough to have shaped Plugin-Creator's own frontmatter once: an early `skills/plugin-creator/SKILL.md` failed Claude Desktop install because its description literally contained the string `skills/<name>/SKILL.md`, which the desktop validator parsed as an XML tag. It was reworded to `per-skill SKILL.md auto-registration`.
- The **SessionStart cleanup hook** pattern exists because Desktop's "Add Plugin" does an overlay-extract that leaves deleted files behind on re-upload — a real Coeus install-hygiene bug, now offered as an optional extension rather than baked in everywhere.
- The **weekly upstream-skill sync** and **LLM handover note** extensions listed as optional Coeus-only patterns mirror Coeus's own vendored-skill (`caveman`, `prompt-master`) and handover practices.

---

## Hard Rules

- Never invent capabilities: if a skill needs a tool the runtime doesn't expose, say so in the `SKILL.md` and degrade gracefully.
- Never put secrets in the bundle — no tokens, API keys, or `.env` files.
- Never ship build artifacts (`dist/`, `*.plugin`, `*.skill`) in git.
- One source of truth for the version: `.claude-plugin/plugin.json` only.
- Skills auto-register from frontmatter; never create `commands/` wrappers.
- The conformance check must pass before delivery — self-attestation is not a check.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [Coeus Architecture →](Coeus-Architecture.md)
- [PLUGIN_MANIFEST_EXTENSIONS.md →](PLUGIN_MANIFEST_EXTENSIONS.md) (where Coeus documents its own manifest deviations)
- [COEUS_EXTENSIONS.md →](COEUS_EXTENSIONS.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.0** (current) | 2026-Jun-21 | Initial release (v3.5.0). Six phases — Intake & Classification → Canonical Layout → Optional Cleanup Hook → Build Scripts → Conformance Check → Documentation — plus a migration-patterns table for existing non-spec plugins. |
| — | 2026-Jun-21 | v3.5.1 fix: the skill's own description tripped the Claude Desktop XML-tag validator (`skills/<name>/SKILL.md` read as a tag); reworded to `per-skill SKILL.md auto-registration`. |

Go back to the [Main README](../README.md).
