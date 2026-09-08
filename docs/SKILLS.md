# Coeus Skill Catalog

> One page, every skill, in plain language. What each one is, when it fires, and what you get back. Organized by family. Frontmatter in each `skills/<name>/SKILL.md` is canonical for triggers; this page is canonical for *understanding*.

**18 skills · 6 families · Tier model:** Tier 1 = standalone nano-skill · Tier 2 = cluster/combo · Tier 3 = meta.

---

## Decision family

The reasoning engines. Everything here exists to stop a bad commitment before it happens.

### llm-council — the general-purpose adversarial council
`/coeus:llm-council` · v1.2 · Tier 1

Seven simulated frontier-model voices (ChatGPT, Grok, Claude, Perplexity, DeepSeek, Le Chat, Gemini) debate your decision through four phase-gated rounds: Socratic clarification, a roadmap you must explicitly approve, tri-team red-teaming (3/2/2 factions, re-randomized every round), and a 6-month failure premortem. Delivers `Final_Plan.md` + `Premortem_Report.md`, with an opt-in consolidated Word document. Use when the stakes outgrow a single-pass answer.

### ep-council — the E&P deal killer
`/coeus:ep-council` · v1.10 · Tier 1

The domain-specific sibling: nine supermajors (BP through Occidental), each ground-truthed against primary-source research, stress-test any upstream opportunity — block, well, farm-in, FID, JV, divestment. A Strategy Gate locks your strategy before red-teaming begins; a 13-trap screen (T0–T12) catches the institutional failure modes that killed real deals — peak-price entry, acquisition leverage, duration drift, megaproject overrun. Nine named votes close every session.

### the-architect — the full pipeline
`/coeus:the-architect` · v1.1 · Tier 2 · deps: prompt-master, caveman, llm-council

When your brief is as messy as your decision is big. Chains prompt engineering → compression → full council in one run. Route A (default) runs the pipeline; Route C (`--explore`) lets the council define the problem first; Route D (`--diagnostic`) answers review/evaluate/yes-no questions single-pass with no council overhead.

### morpheus — engineer, compress, execute
`/coeus:morpheus` · v1.2 · Tier 2 · deps: prompt-master, caveman

"Morph this." Crafts a precision prompt for the target model, compresses it per upstream caveman rules, and — in default AUTO mode — executes it immediately in the same response. Say "review first" to inspect the prompt before it fires. Compresses prompts only, never deliverables.

### prompt-master — precision prompt engineering *(vendored)*
`/coeus:prompt-master` · tracks [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) · Tier 1

Model-aware prompt crafting for Claude, ChatGPT, o-series, Gemini, image and video AI. Synced weekly from upstream; Coeus never patches its internals.

### caveman — token compression *(vendored)*
`/coeus:caveman` · tracks [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) · Tier 1

Ultra-compressed response mode — measured ~65% output-token cut with full technical accuracy. Six intensity levels from lite to classical-Chinese wenyan-ultra. Auto-clarity drops compression for security warnings and destructive-action confirmations. Synced weekly from upstream.

### plugin-creator — the autobot transformer
`/coeus:plugin-creator` · v1.0 · Tier 1

Turns an idea, a prompt, a workflow note, or a folder of skills into a spec-compliant, installable Claude plugin: canonical 4-key manifest, SKILL.md auto-registration, UTF-8/LF hygiene, and a conformance check that can fail. Encodes every hard-won lesson from Coeus's own conformance history.

### seer — the router's examiner
`/coeus:seer` · v1.0 · Tier 1 · subject under test: coeus-router

Spec-driven routing evaluation: synthesizes labeled scenarios from skill frontmatter alone, holds the intended route as a hidden oracle, replays the router blind, grades with a cascading rubric, and proposes golden-set rows. Deterministic checks run before judgment; single-model self-eval is disclosed in every report.

---

## Writing family

### minto — answer-first document structuring
`/coeus:minto` · v1.0 · Tier 2 · deps: llm-council (gated review)

Verified Barbara Minto doctrine — pyramid structure, SCQ introduction, MECE groupings, inductive key line — applied to memos, reports, proposals, gate submissions, and deck storylines. Fires only on explicit intent to *structure* a document, never on generic writing or editing. Learns from repeated corrections via a self-evolution file.

---

## Tools family

The DOCX-and-project workhorses, born from real long-running report projects.

### ooxml-repair — when Word won't open the file
`/coeus:ooxml-repair` · v1.0 · Tier 1

Diagnoses and repairs "Word found unreadable content": ZIP integrity, XML well-formedness, paraId validity, orphaned bookmarks and comment references (the most common root cause), duplicate style IDs, numbering chains, rels targets. Includes the safe ZIP-rebuild recipe.

### ooxml-fields — when the numbers are wrong
`/coeus:ooxml-fields` · v1.0 · Tier 1

SEQ fields, REF fields, caption numbering — fixed programmatically via direct XML. Catches hardcoded caption numbers masquerading as fields and verifies Caption-style usage. Repair opens the file; fields fixes what's inside it.

### docx-inventory — what's actually in the document
`/coeus:docx-inventory` · v1.0 · Tier 1

Extracts a complete figure and table inventory from a DOCX into a two-sheet xlsx — paragraph index, cached SEQ number, caption text, style, issues flagged per row. The audit before the fix.

### project-lifecycle — multi-session memory
`/coeus:project-lifecycle` · v1.4 · Tier 2

Kickoff, resume, handover, audit, close — the discipline that lets a project survive session boundaries. Three core files (handover, artefacts index, telemetry log) created once at kickoff and updated in place forever; resume renames the handover to `<task>_handover_note.md` and re-links references.

### atlas — the project, at a glance
`/coeus:atlas` · v1.3 · Tier 1 · deps: project-lifecycle (reads), llm-council (gated review)

Mines a project — lifecycle files, git repo, document folder, or a six-question interview — into four evergreen outputs, created once and updated in place forever: a self-contained offline HTML atlas (Frame / Now / Map / Story; the Map opens as a group-level Overview with drill-in to per-node ego views, plus List and Grid toggles), a markdown Master-of-Content for link-based navigation, and a visual Contents hub (`atlas_toc.html`) — a clickable table of contents linking every artefact, with an inline SVG explainer of how the outputs relate and quick links into every region and view. Causal history with forks and guardrail badges; never invents topology; unknowns render as marked placeholders.

### evergreen-artefacts — evergreen publishing
`/coeus:evergreen-artefacts` · v1.0 · Tier 1

Agent-neutral publishing to a Synology NAS: every artefact gets a stable evergreen link that redirects to the latest immutable `vN/`; every version carries a `publish.json` audit record with per-file SHA-256. Reverting republishes old content as a *new* version — nothing is ever deleted.

---

## Seismic family

### dug_binary — the DUG project X-ray
`/coeus:dug_binary` · v2.0 · Tier 1

Reverse-engineers a DUG Insight `project.dugprj` (undocumented SQLite, schema empirically mapped) into user-selected artefacts: a multi-sheet xlsx inventory of horizons, polygons, volumes and per-volume process history with resolved UUIDs; per-volume DOCX reports; a self-contained HTML volume-lineage explorer. Read-only, vendor-neutral, no DUG runtime required. Input path must be user-supplied — no defaults, ever.

---

## Vault family

### obsidian-vault — vault operations with guardrails
`/coeus:obsidian-vault` · v1.2 · Tier 1

Direct file operations on a plain-text Obsidian vault — read, search, create, edit, tag, move, delete — with verified obsidian-mcp parity: soft delete to `.trash/`, vault-wide link updating on move, hierarchical tag search. NAS/UNC/mapped-drive paths are first-class. Eight prompt-injection and path-containment guardrails; destructive operations are confirmation-gated.

---

## Meta

### coeus-router — the skill selector
`/coeus:router` · v1.7 · Tier 3 · routes to all of the above

Reads your intent, gates it (BYPASS / NO ROUTE / PROCEED), picks the family, picks the skill, and *launches it* in the same response. Sequential cross-family requests route the first task and name the handoff. Three-tier confidence fallback — it clarifies once or says "no route" rather than guess. Behaviour pinned by a 31-case golden set; examined by seer.

---

## Family map

```
decision   llm-council · ep-council · the-architect · morpheus
           prompt-master · caveman · plugin-creator · seer
writing    minto
tools      ooxml-repair · ooxml-fields · docx-inventory
           project-lifecycle · atlas · evergreen-artefacts
seismic    dug_binary
vault      obsidian-vault
meta       coeus-router
```

*Canonical registry: [`skills/_shared/SKILL_REGISTRY.md`](../skills/_shared/SKILL_REGISTRY.md). Architecture: [`SKILL_ARCHITECTURE.md`](SKILL_ARCHITECTURE.md).*
