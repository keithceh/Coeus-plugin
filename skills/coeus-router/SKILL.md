---
name: coeus-router
version: 1.1.0
argument-hint: "[task — a decision, plan, prompt, deal, file, or skill question]"
description: >-
  Trigger on: /coeus:router, /coeus-router, "route this", "which coeus skill", "pick the right coeus skill", "coeus help me decide", "not sure which coeus".
  Tier-3 meta-skill router across three families: decision (llm-council, ep-council, morpheus, the-architect, prompt-master, caveman, plugin-creator), tools (ooxml-repair, ooxml-fields, docx-inventory, project-lifecycle), seismic (dug_projdb). Use when the user wants a Coeus skill but doesn't know which.
dependencies:
  - llm-council
  - ep-council
  - morpheus
  - the-architect
  - prompt-master
  - caveman
  - plugin-creator
  - ooxml-repair
  - ooxml-fields
  - docx-inventory
  - project-lifecycle
  - dug_projdb
---

# Coeus Router — Tier-3 Meta-Skill

This is a **router-only** skill. It has no analysis, no compression, no
deliberation logic. Its sole job is to read the user's request and hand off to
the correct Coeus skill.

If you find yourself producing analysis here, stop — you have routed to the
wrong skill. Re-route.

---

## Routing — Two-Step Decision

The router decides in two steps. **Step 1: which family.** **Step 2: which skill inside that family.** This keeps the table O(n) per family rather than O(n²) across the whole plugin and lets new families be added without rewriting existing rules.

### Step 1 — Pick the Family

| If the request mentions… | Family |
|---|---|
| A DUG Insight project (`project.dugprj`, `.dugprj`), horizons / polygons / volumes / processes from a seismic project, OpendTect-style audit, or "what's in this DUG project" | **seismic** |
| A DOCX/Word file, OOXML, SEQ/REF fields, figure/table captions, "fix Word", "audit captions", "figure inventory", or a project handover / session resume / file audit | **tools** |
| A decision, plan, strategy, deal, prompt, compression, council, premortem, red-team, plugin packaging, or "stress-test" anything | **decision** |

If multiple signals are present, the more concrete artefact wins (a file path
to `project.dugprj` beats a generic word like "decision"; a DOCX path beats
"strategy"). Among artefact families, the file-extension or domain noun is
authoritative — a request that names *both* DUG and DOCX gets a one-line
clarifier, not a guess. If no signal is clearly present, ask one clarifier
and stop.

### Step 2a — Skill Within `decision`

Match in this order. First match wins.

| If the request… | Route to | Trigger phrase to emit |
|---|---|---|
| Concerns an upstream E&P opportunity (block, well, farm-in, FID, FLNG, JV, divestment, supermajor playbook) | `ep-council` | `/coeus:ep-council` |
| Asks to package an idea / prompt / folder as a Claude plugin | `plugin-creator` | `/coeus:plugin-creator` |
| Is "engineer this prompt", "optimise prompt", "refine my prompt for…" with NO compression need | `prompt-master` | `/coeus:prompt-master` |
| Is "compress this", "talk like caveman", "less tokens" applied to a prompt or short instruction | `caveman` | `/coeus:caveman` |
| Wants prompt-engineering THEN compression (the pipeline) | `morpheus` | `/coeus:morpheus` |
| Is a high-stakes decision / complex strategy that benefits from BOTH prompt-engineering AND adversarial deliberation | `the-architect` | `/coeus:the-architect` |
| Is a general decision, plan, or strategy that warrants multi-model stress-testing (and is NOT E&P-specific) | `llm-council` | `/coeus:llm-council` |

### Step 2b — Skill Within `tools`

Match in this order. First match wins.

| If the request… | Route to | Trigger phrase to emit |
|---|---|---|
| Mentions DOCX corruption, "unreadable content" dialog, ZIP rebuild errors, OOXML schema violations, orphaned bookmarks/comments, duplicate style IDs | `ooxml-repair` | `/coeus:ooxml-repair` |
| Concerns SEQ fields, REF fields, figure/table caption numbering, hardcoded caption numbers, broken cross-references | `ooxml-fields` | `/coeus:ooxml-fields` |
| Wants a figure or table inventory extracted from a DOCX to xlsx, a caption audit, or a list of all figures/tables | `docx-inventory` | `/coeus:docx-inventory` |
| Is about resuming a multi-session project, writing or updating a handover note, updating a changelog, or auditing project files for obsolescence | `project-lifecycle` | `/coeus:project-lifecycle` |

### Step 2c — Skill Within `seismic`

Match in this order. First match wins.

| If the request… | Route to | Trigger phrase to emit |
|---|---|---|
| Names a DUG Insight `project.dugprj` or `.dugprj` file, asks to list horizons / polygons / volumes from a DUG project, audit per-volume processes, or extract DUG project contents to xlsx | `dug_projdb` | `/coeus:dug_projdb` |

(More seismic skills will be added here as the family grows.)

---

## Tie-Breaker Rules

0. **Family first.** Always run Step 1 before Step 2. A request that contains a DOCX path goes to `tools` even if it also contains the word "decision". A request that contains "farm-in" goes to `decision` even if the user attached a DOCX.
1. **E&P vs general decision:** E&P always wins inside `decision` if any E&P terminology is present. `llm-council` is the fallback for non-E&P decisions.
2. **Architect vs Council:** Pick `the-architect` only if the user's raw input is **also a prompt that needs engineering** (not already a well-formed brief). If the brief is already crisp, route straight to `llm-council`.
3. **Morpheus vs prompt-master alone:** Pick `morpheus` only if compression is wanted; otherwise `prompt-master` alone.
4. **`ooxml-fields` vs `docx-inventory`:** Both touch captions. Inventory **lists** ("what's in the document?"), fields **changes** ("fix the numbers"). If the verb is "list / extract / audit / inventory", pick `docx-inventory`. If the verb is "fix / renumber / repair / update", pick `ooxml-fields`.
5. **`ooxml-repair` vs `ooxml-fields`:** Repair handles "Word won't open this" and structural corruption. Fields handles "Word opens it but the numbers are wrong". When in doubt, run `ooxml-repair` first — fields can run after, but fields can't fix a file Word won't open.
6. **`project-lifecycle` vs the rest:** Lifecycle covers cross-cutting session work (resume, handover, audit). It does not touch DOCX content. If the request is about session/project management rather than a specific file, route here.
7. **`dug_projdb` (seismic) vs `project-lifecycle` (tools):** A request that names `project.dugprj` specifically goes to `dug_projdb` even if it also mentions "audit". `project-lifecycle` only handles Coeus session/handover files, never seismic project artefacts.
8. **Ambiguity:** If two skills tie after all rules above, name both in a one-line clarifier and let the user pick. Do not invent a hybrid.

---

## Output Format

When routing, emit a single short block:

```
FAMILY → <decision | tools>
ROUTE  → <skill-name>
WHY    → <one-line reason>
RUN    → <slash command to invoke>
```

Then invoke the target skill in the same response. Do not summarise what the
target skill is going to do — let the target skill speak for itself.

---

## Hard Rules

- **No domain logic in this skill.** If you find yourself reasoning about the
  user's task instead of about which skill should handle it, stop.
- **No clarifier loops.** One ambiguity check max, then route.
- **No fabrication of new Coeus skills.** Route only to skills listed in
  `skills/_shared/SKILL_REGISTRY.md`.
- **Uncertainty handling** follows `skills/_shared/uncertainty_rules.md`.

---

## When NOT To Trigger

- The user explicitly names a Coeus skill (`/coeus:llm-council`, "use morpheus", etc.).
- The request is plainly outside Coeus's scope (general chat, coding tasks, file edits).
- The user has already received a routing answer in this conversation and is asking a follow-up of the routed-to skill.
