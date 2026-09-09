---
name: keymaker
version: 1.0.0
argument-hint: "[project path] [optional: plan-only | skip-visual-pass]"
description: >-
  Trigger on: /coeus:keymaker, "keymaker", "full project pass", "end-to-end project pass", "coordinate all deliverables", "refresh every deliverable", "chain lifecycle and atlas", "sweep the project artefacts".
  Tier-2 cluster chaining project-lifecycle and atlas over every deliverable (the keyring), applying the house visual-quality bar; top-tier plan/review, delegated execution, loop until green.
  Never for one deliverable — atlas, project-lifecycle and evergreen-artefacts own those doors.
dependencies:
  - project-lifecycle
  - atlas
  - evergreen-artefacts
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these whenever this skill emits a judgment, recommendation, or simulated voice.

# Keymaker — Coordinated Project Deliverables Pass

The Keymaker opens every door in a project in one pass. It is an
**orchestration** skill: it chains `project-lifecycle` (session state — kickoff,
resume, handover, audit, close) and `atlas` (the four evergreen visual outputs),
coordinates every other deliverable through its owner skill, then holds all of
it to the house visual-quality bar. It launches its dependencies via the Skill
tool; it **never** reimplements their logic.

---

## Phase 0 — Trigger Gate

**Manual:** `/coeus:keymaker` or any Trigger-on phrase — always fires.

**Auto-fire — all three must hold:**
1. The request spans **two or more deliverable classes** (session files *and*
   the atlas, and/or other visual artefacts), or explicitly asks for an
   end-to-end / whole-project sweep.
2. The subject is a bounded project.
3. No single owner skill covers the whole ask.

**Do NOT fire on** (defer silently — no announcement):
- A visual overview alone → `atlas`.
- Session ops alone (resume, handover, audit, close) → `project-lifecycle`.
- Publishing alone → `evergreen-artefacts`.
- DUG Insight lineage → `dug_binary`.
- Structuring a document for a reader → `minto`.

State `Mode: MANUAL` or `Mode: AUTO` in one line when firing.

## Phase 1 — PLAN (top tier, never delegated)

Run at the strongest available reasoning (the session's top model —
Fable-class). Survey exactly per the `atlas` Phase-1 source priority: lifecycle
files → git repo → document folder → interview.

Build the **Keyring** — the deliverables ledger, one row per deliverable:

| Deliverable | Owner skill | State | Gap | Planned action |
|---|---|---|---|---|
| … | … | green / amber / red / unknown | … | … |

**Truthfulness rule (hard):** every row traces to a file actually read or an
explicit user answer. Unknowns are marked `?` — never guessed, never quietly
dropped.

Present the keyring and the run plan in **one screen**. The `plan-only`
argument stops here.

## Phase 2 — EXECUTE (delegate at the right tier)

An ordered chain. Each dependency is invoked under **its own SKILL.md rules**
via the Skill tool:

1. `project-lifecycle` — kickoff if no handover exists, else resume; handover
   and audit as the keyring demands.
2. `atlas` — create or refresh under its own Phase-2 gate (an existing
   `atlas.json` makes the run a refresh, whatever the invocation said).
3. Every remaining **red** keyring row, through its owner skill.

| Work | Executor |
|---|---|
| Orchestration, sequencing, keyring decisions | Inline (top tier — never delegated) |
| Independent deliverable builds (an atlas data-fill, a report section) | Subagent — **Opus** |
| Mechanical refreshes, doc regeneration, inventory sweeps | Subagent — **Sonnet** |
| Contested or cross-deliverable coherence work | Inline at top tier |

If the Agent tool or model overrides are unavailable, run everything inline —
the keyring, not the delegation, is the deliverable.

## Phase 3 — VISUAL QUALITY PASS

Enumerate every visualisation artefact in the project: `atlas.html`,
`atlas_toc.html`, lineage explorers, standalone HTML/SVG, charts, diagrams.
Check each against [references/quality_bar.md](references/quality_bar.md).

Treat **only** artefacts that fail. The pass is idempotent: an artefact already
meeting the bar is not touched.

Never break an artefact's own hard rules to meet the bar — a self-contained
offline file never gains a CDN, a webfont, or a network fetch. Where richer
session-level design skills are available (`artifact-design`, `dataviz`,
`theme-factory` or equivalents), load them and let them govern; `quality_bar.md`
is the always-available fallback contract.

Skipped entirely by the `skip-visual-pass` argument.

## Phase 4 — REVIEW (top tier), loop until green

Re-walk the keyring at the strongest model. Every row must be **green**, or
amber **explicitly accepted by the user**. Run each dependency's own review
gates: the `atlas` Phase-3 checks; lifecycle files updated in place; no
versioned or timestamped sibling of any evergreen output, anywhere.

Any red, or any unaccepted amber → return to Phase 2 / Phase 3.

**Hard cap: three full cycles.** Then stop and report what is still red and
why, honestly. A keyring declared green that isn't is a worse failure than a
reported red.

## Phase 5 — REPORT

- One keyring table: deliverable · owner · state · action taken.
- One line per visual artefact treated, naming the bar items it failed.
- Next actions.
- Offer `evergreen-artefacts` publishing — **gated, on request only**.
- Record skill invocations into handover §8 telemetry, per
  `project-lifecycle`'s counting rules.

---

## Hard Rules

- **Launches dependencies, never reimplements them.** Zero domain logic
  duplicated from `project-lifecycle`, `atlas`, or any owner skill.
- **Create-once-update-in-place is inherited everywhere.** Keymaker never
  produces a versioned or timestamped sibling of any evergreen file.
- **Never invent state.** Every keyring row traces to a file read or a user
  answer; unknowns are marked, never guessed.
- **The visual pass is idempotent** and never violates an artefact's own hard
  rules — self-containment outranks styling.
- **Caveman compression never touches deliverables.**
- **Loop until green, three-cycle cap.** Remaining reds are reported, never
  hidden.
- Uncertainty handling per `_shared/uncertainty_rules.md`.

## When NOT To Trigger

- One deliverable named → its owner skill (`atlas`, `project-lifecycle`,
  `evergreen-artefacts`, `dug_binary`, `ooxml-*`).
- The decision itself, not the deliverables → the `decision` family.
- Structuring a document for a reader → `minto`.
- A first-time build of one artefact ("draw me a map of this project") →
  `atlas` alone.
