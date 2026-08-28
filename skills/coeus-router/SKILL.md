---
name: coeus-router
version: 1.5.0
argument-hint: "[task — a decision, plan, prompt, deal, file, vault note, document to structure, or skill question]"
description: >-
  Trigger on: /coeus:router, /coeus-router, "route this", "which coeus skill", "pick the right coeus skill", "coeus help me decide", "not sure which coeus", "coeus guru", "skill selector".
  Tier-3 meta-skill router across five families: decision, tools, seismic, vault (obsidian-vault), writing (minto). Use when the user wants a Coeus skill but doesn't know which.
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
  - dug_binary
  - obsidian-vault
  - minto
---

# Coeus Router — Tier-3 Meta-Skill

This is a **router-only** skill — the Coeus guru / skill selector. It has no
analysis, no compression, no deliberation logic. Its sole job is to read the
user's request, pick the correct Coeus skill, and **launch it** (see Output
Format). A route that names a skill but does not launch it is incomplete.

If you find yourself producing analysis here, stop — you have routed to the
wrong skill. Re-route.

---

## Routing — Gate, Then Two-Step Decision

### Step 0 — Gate (does this need a route at all?)

Three outcomes, checked before any family matching:

1. **BYPASS** — the user already named a Coeus skill (slash command or by name). Launch that skill directly; emit no routing block.
2. **NO ROUTE** — the request needs no Coeus skill (general chat, a coding task, a question about Coeus itself, a follow-up to an already-routed skill). Say so in one line and answer normally. Never force a route to justify the router's existence — a confidently wrong route costs more than "no skill needed here."
3. **PROCEED** — a Coeus skill plausibly applies. Continue to Step 1.

### Steps 1–2 — Family, then skill

The router decides in two steps. **Step 1: which family.** **Step 2: which skill inside that family.** This keeps the table O(n) per family rather than O(n²) across the whole plugin, lets new families be added without rewriting existing rules, and keeps the skill list the model weighs per decision small (the catalog-degradation threshold documented for LLM tool selection is ~15–20 candidates; family-first keeps each step well under it).

### Step 1 — Pick the Family

| If the request mentions… | Family |
|---|---|
| A DUG Insight project (`project.dugprj`, `.dugprj`), horizons / polygons / volumes / processes from a seismic project, OpendTect-style audit, or "what's in this DUG project" | **seismic** |
| A DOCX/Word file, OOXML, SEQ/REF fields, figure/table captions, "fix Word", "audit captions", "figure inventory", or a project handover / session resume / file audit | **tools** |
| A decision, plan, strategy, deal, prompt, compression, council, premortem, red-team, plugin packaging, or "stress-test" anything | **decision** |
| An Obsidian vault, vault notes, `.obsidian`, note tags (add/remove/rename), "search my vault", or moving/deleting notes | **vault** |
| Structuring or restructuring a memo, report, proposal, recommendation, update, or deck storyline for a reader — "pyramid", "Minto", "SCQ", answer-first / lead-with-the-answer requests, or a structural review of an existing document | **writing** |

If multiple signals are present, the more concrete artefact wins (a file path
to `project.dugprj` beats a generic word like "decision"; a DOCX path beats
"strategy"; a named vault note path beats a generic reference to another
family). Among artefact families, the file-extension or domain noun is
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
| Says "morph", "morph this", or wants prompt-engineering THEN compression (the pipeline) | `morpheus` | `/coeus:morpheus` |
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
| Names a DUG Insight `project.dugprj` or `.dugprj` file, asks to list horizons / polygons / volumes from a DUG project, audit per-volume processes, map volume lineage, or extract DUG project contents to xlsx / DOCX / HTML explorer | `dug_binary` | `/coeus:dug_binary` |

(More seismic skills will be added here as the family grows.)

### Step 2d — Skill Within `vault`

Match in this order. First match wins.

| If the request… | Route to | Trigger phrase to emit |
|---|---|---|
| Concerns an Obsidian vault — reading, searching, creating, editing, tagging, moving, or deleting notes, including on a NAS/UNC/mapped-drive vault path | `obsidian-vault` | `/coeus:obsidian-vault` |

(More vault skills will be added here as the family grows.)

### Step 2e — Skill Within `writing`

Match in this order. First match wins.

| If the request… | Route to | Trigger phrase to emit |
|---|---|---|
| Wants a memo, report, proposal, recommendation, gate submission, update, or deck storyline structured, restructured, or reviewed against answer-first / pyramid logic | `minto` | `/coeus:minto` |

(More writing skills will be added here as the family grows.)

---

## Tie-Breaker Rules

0. **Family first.** Always run Step 1 before Step 2. A request that contains a DOCX path goes to `tools` even if it also contains the word "decision". A request that contains "farm-in" goes to `decision` even if the user attached a DOCX.
1. **E&P vs general decision:** E&P always wins inside `decision` if any E&P terminology is present. `llm-council` is the fallback for non-E&P decisions.
2. **Architect vs Council:** Pick `the-architect` only if the user's raw input is **also a prompt that needs engineering** (not already a well-formed brief). If the brief is already crisp, route straight to `llm-council`.
3. **Morpheus vs prompt-master alone:** Pick `morpheus` only if compression is wanted; otherwise `prompt-master` alone.
4. **`ooxml-fields` vs `docx-inventory`:** Both touch captions. Inventory **lists** ("what's in the document?"), fields **changes** ("fix the numbers"). If the verb is "list / extract / audit / inventory", pick `docx-inventory`. If the verb is "fix / renumber / repair / update", pick `ooxml-fields`.
5. **`ooxml-repair` vs `ooxml-fields`:** Repair handles "Word won't open this" and structural corruption. Fields handles "Word opens it but the numbers are wrong". When in doubt, run `ooxml-repair` first — fields can run after, but fields can't fix a file Word won't open.
6. **`project-lifecycle` vs the rest:** Lifecycle covers cross-cutting session work (resume, handover, audit). It does not touch DOCX content. If the request is about session/project management rather than a specific file, route here.
7. **`dug_binary` (seismic) vs `project-lifecycle` (tools):** A request that names `project.dugprj` specifically goes to `dug_binary` even if it also mentions "audit". `project-lifecycle` only handles Coeus session/handover files, never seismic project artefacts.
8. **`obsidian-vault` (vault) vs any other family:** If a request names both a vault note path (or `.obsidian`) and another family's artefact (a DOCX, a `.dugprj`, a prompt to engineer), the more concrete artefact wins — consistent with rule 0. A vault note path alone always routes to `vault`.
9. **Sequential requests (cross-family):** If the request contains two ordered tasks in different families ("audit this DUG project, then write the handover"), route and launch the FIRST task's skill now, and name the second skill as the explicit next step in the WHY line ("then hand off to `project-lifecycle`"). Never launch two skills at once; never invent a hybrid. Within one family, prefer the combo skill that already chains the steps (`morpheus`, `the-architect`) over manual sequencing.
10. **Three-tier confidence fallback:** (a) clear signal → route and launch; (b) two skills tie after all rules → one-line clarifier naming both, user picks, then route — one clarifier max; (c) no family signal at all → NO ROUTE (Step 0 outcome 2), never a guess. A router that always picks something is more dangerous than one that says it can't.
11. **`minto` (writing) vs `decision` family:** If the user needs the decision itself made or stress-tested ("should we…", "is this investible", "weigh the options"), route `decision` — even if a document is the eventual output. If the decision exists and the request is to communicate or structure it ("structure the board memo recommending X", "restructure this report"), route `writing`. A request for both is sequential (rule 9): decision first, name `minto` as the next step. Handover notes, changelogs, and session docs stay with `project-lifecycle` (rule 6) — never `minto`.

---

## Output Format

When routing (Step 0 outcome PROCEED), emit a single short block:

```
FAMILY → <decision | tools | seismic | vault>
ROUTE  → <skill-name>
WHY    → <one-line reason; for sequential requests, name the next-step skill here>
RUN    → <slash command to invoke>
```

For Step 0 outcome NO ROUTE, emit one line — `NO ROUTE → <reason>` — then answer the request normally. For BYPASS, emit nothing; just launch the named skill.

**Then, in the same response, launch the routed-to skill by calling the Skill
tool: `Skill(skill="coeus:<skill-name>", args="<the user's task>")`.** The
`RUN →` line is for the user's reference only — slash commands printed in
model output are inert text; they only fire when the *user* types them.
Emitting the block without the Skill-tool call is a routing failure.

Do not summarise what the target skill is going to do — let the target skill
speak for itself.

---

## Hard Rules

- **No domain logic in this skill.** If you find yourself reasoning about the
  user's task instead of about which skill should handle it, stop.
- **No clarifier loops.** One ambiguity check max, then route.
- **No fabrication of new Coeus skills.** Route only to skills listed in
  `skills/_shared/SKILL_REGISTRY.md`.
- **Uncertainty handling** follows `skills/_shared/uncertainty_rules.md`.
- **Regression check:** routing behaviour is pinned by the labeled golden set
  in [`references/routing-golden-set.md`](references/routing-golden-set.md).
  When editing this skill, re-check the golden set by hand — every row must
  still route as labeled.

---

## When NOT To Trigger

- The user explicitly names a Coeus skill (`/coeus:llm-council`, "use morpheus", etc.).
- The request is plainly outside Coeus's scope (general chat, coding tasks, file edits).
- The user has already received a routing answer in this conversation and is asking a follow-up of the routed-to skill.
