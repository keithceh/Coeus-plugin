# Coeus Skill Registry

> Canonical registry of all skills shipped in `coeus.plugin`. Required by
> `docs/SKILL_ARCHITECTURE.md` (FM-03 mitigation — orphan-skill prevention).
>
> **Protocol:** Any new skill added under `skills/` MUST be registered here in
> the same commit. Any skill removed MUST be moved to the deprecated section,
> never silently deleted.

---

## Active Skills

| Skill | Family | Tier | Tokens (approx.) | Trigger (primary) | Delegates To |
|---|---|---|---|---|---|
| `llm-council` | decision | 1 | ~1,834 | `/coeus:llm-council` | — |
| `ep-council` | decision | 1 | ~2,007 | `/coeus:ep-council` | — |
| `prompt-master` | decision | 1 | ~5,408 ⚠ | `/coeus:prompt-master` | — (vendored, exempt from cap) |
| `caveman` | decision | 1 | ~892 | `/coeus:caveman` | — (vendored) |
| `morpheus` | decision | 2 | ~2,097 | `/coeus:morpheus` | prompt-master, caveman |
| `the-architect` | decision | 2 | ~2,334 | `/coeus:the-architect` | prompt-master, caveman, llm-council (v1.1 adds ROUTE D diagnostic mode) |
| `plugin-creator` | decision | 1 | ~2,151 | `/coeus:plugin-creator` | — |
| `ooxml-repair` | tools | 1 | ~2,019 | `/coeus:ooxml-repair` | — |
| `ooxml-fields` | tools | 1 | ~1,548 | `/coeus:ooxml-fields` | — |
| `docx-inventory` | tools | 1 | ~1,168 | `/coeus:docx-inventory` | — |
| `project-lifecycle` | tools | 2 | ~1,853 | `/coeus:project-lifecycle` | the-architect (cluster: kickoff + cadence + resume + handover + audit + close + telemetry-log + artefacts-index, v1.3.0 — three core files created once at kickoff, updated in place; detail in _shared/lifecycle_{frequency,artefacts,handover,close,audit,resume}.md) |
| `dug_projdb` | seismic | 1 | ~2,137 | `/coeus:dug_projdb` | — (3-script pipeline in `scripts/`: 01_build_inventory.py → 02_extract_parameters.py → 03_resolve_uuids.py. Read-only SQLite parse of DUG Insight project.dugprj into multi-sheet xlsx) |
| `coeus-router` | meta | 3 | ~822 | `/coeus:router` | (routes only — picks the right Tier 1/2 skill across decision / tools / seismic families) |

**Families.** Coeus skills group into three intent families plus a meta layer:

- **decision** — multi-model deliberation, prompt engineering, plugin authoring. Always invoked deliberately by the user.
- **tools** — DOCX mechanics and project lifecycle (a.k.a. "Office Tools" in the website navigation). Invoked when the user has a concrete file or session-management task.
- **seismic** — upstream O&G subsurface project artefacts (a.k.a. "Seismic Tools" in the website navigation). Invoked when the user has a DUG Insight project, well-log set, or other geophysical artefact to audit / extract.
- **meta** — routing only. No domain logic.

The router uses `family` as its first split point (see `skills/coeus-router/SKILL.md` Tie-Breaker 0). New skills MUST declare a family in this table at registration time.

Token counts are author estimates from `wc -w` × 1.33; verify with a tokenizer before
relying on the number for budget decisions. The 3,000-token cap from
`docs/SKILL_ARCHITECTURE.md` applies to every entry in this table.

**Exception:** `prompt-master` is vendored from `nidhinjs/prompt-master@main`
and refreshed by the weekly sync workflow. Its size is outside Coeus's
control. Splitting it would conflict with the upstream-sync contract. If
Claude's positional bias starts degrading prompt-master output, fork the
upstream and submit a split-PR there rather than patching it locally.

## Shared Convention Files

| File | Used By |
|---|---|
| `skills/_shared/uncertainty_rules.md` | All skills producing analysis |
| `skills/_shared/output_formats.md` | All skills producing artifacts |
| `skills/_shared/SKILL_REGISTRY.md` | (this file) |

## Deprecated Skills

*(None.)*

When a cluster supersedes a standalone skill, move the standalone's directory to
`Templates/deprecated-skills/<skill-name>/` and add a row here with the
deprecation date and replacement.
