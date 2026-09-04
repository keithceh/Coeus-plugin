---
name: atlas
version: 1.1.0
argument-hint: "[create|refresh|interview] [optional project path]"
description: >-
  Trigger on: /coeus:atlas, "project atlas", "project map", "project at a glance", "visualise this project", "visualize this project", "explain this project visually", "map my project". Builds one self-contained interactive HTML atlas of any project (coding or not): intent, scope, artifact map, causal history, guardrails, re-entry state. Fires only for a visual overview OF A PROJECT — never for DUG lineage, session resume or handover, or document structuring.
dependencies:
  - project-lifecycle
  - llm-council
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these whenever this skill emits a judgment, recommendation, or simulated voice.

# Atlas — Project Atlas Generator

Renders any project — codebase, report, deal, vault, field study — as **one
self-contained interactive HTML file** a reader can open cold and understand at
a glance. Two-stage pipeline, the house extract-then-render pattern:
`Outputs/atlas.json` (structured truth, schema in
[references/schema.md](references/schema.md)) → `Outputs/atlas.html` (rendered
from [references/template.html](references/template.html) by replacing its
`/*__ATLAS_DATA__*/{}` injection point — that exact literal, braces included,
replaced whole). Every layout and encoding choice is
governed by the ranked, evidence-graded rules in
[references/design_rules.md](references/design_rules.md) — read them before
altering the template or the review checklist.

Four fixed regions, canonical order, never reordered between versions:
**① FRAME** (intent, scope in/out, guardrails, references) · **② NOW**
(re-entry cue: where work stopped, open threads, next actions) · **③ MAP**
(three views — **Overview** group-level enclosures with one aggregated
verb-labelled edge per group pair, the default; **List** the relation tree, and
the print form; **Grid** the group-to-group matrix with its empty cells shown —
node drill-in is a member panel then an **ego view**, never a full node-link
graph) · **④ STORY** (causal beats — did X → broke on Y → hence Z — with forks
and guardrail badges).

---

## Phase 0 — Trigger Gate

**Manual:** `/coeus:atlas` or any Trigger-on phrase — always fires.

**Auto-fire — all three must hold:**
1. The user asks for a visual, at-a-glance, or map-shaped explanation.
2. The subject is a **project** (a bounded body of work with artifacts and a
   history), not a single idea, file, or argument.
3. No neighbouring skill owns the request (see below).

**Do NOT fire on** (defer silently — no announcement):
- DUG Insight / seismic volume lineage or `.dugprj` contents → `dug_binary`.
- Session resume, handover notes, changelogs, file-obsolescence audits →
  `project-lifecycle`. Atlas *reads* those files; it never writes them.
- Structuring a memo, report, or deck for a reader → `minto`.
- Reasoning graphs, decision trees, argument maps — out of scope; atlas maps
  projects, not thoughts.
- A request for one diagram ("draw the pipeline") — just draw it inline.

State `Mode: MANUAL` or `Mode: AUTO` in one line when firing.

## Phase 1 — SURVEY (inline, top tier, never delegated)

Run at the strongest available reasoning tier — the session's top model. Read
`~/.coeus/atlas/learnings.md` if it exists and apply its `PREF`/`SHAPE-*` entries.

Detect the project shape and mine sources in this priority order; stop at the
first that applies and fall through only for gaps:

| Shape | Sources mined |
|---|---|
| **a. Lifecycle-managed** | `*_LLM_Handover*.md` §1–§9, `Outputs/artefacts_index.md`, `Outputs/_telemetry/log.md` |
| **b. Git repo** | README, CHANGELOG, `docs/`, file tree (→ map), `git log` (→ story beats, forks) |
| **c. Document folder** | File inventory, document titles/dates/status, folder structure |
| **d. No files** | Six-question interview: intent · scope in/out · artifacts + how they relate · history beats + forks · guardrails + what caused each · current state + next action |

**Readability budget.** A whole-project atlas targets **25–35 map nodes**. Past
that, aggregate or regroup — one node per cluster, not one per file — rather than
adding nodes (R6: if it becomes a hairball, regroup, do not route). The >60-node
figure below is the *delegation* threshold for bulk data-fill, not a licence to
render sixty nodes.

**Truthfulness rule (hard):** never invent topology. Every node, edge, and beat
traces to a mined source or an explicit user answer, recorded in
`meta.sources[]`. What cannot be established is emitted as a marked `?`
placeholder with `status: unknown` — never guessed, never quietly dropped.

## Phase 2 — BUILD

1. Emit or refresh `Outputs/atlas.json` against [references/schema.md](references/schema.md).
2. Render `Outputs/atlas.html`: copy `references/template.html`, replace the
   literal `/*__ATLAS_DATA__*/{}` — comment **and** the empty braces, in one
   substitution — with the JSON. Replacing only the comment leaves a stray `{}`
   after the data and the file will not parse. No other edit to the shell.
3. Grouping: fold the natural grouping into **≤ 5 reader-model groups**, or mark
   one genuinely non-peer group neutral with `"hue": null`. Colour is not your
   decision — the template owns a fixed, validated five-slot palette and assigns
   it by `group_order` **position**. Numeric `layout.hues` values are advisory and
   ignored; only `null` still carries meaning. Give every group an entry anyway,
   `null` included, so "neutral" reads as a choice.

**Refresh rule.** If a prior `atlas.json` exists, load it first and preserve
`layout.node_order`, `layout.group_order`, and group assignment verbatim — new
nodes append inside their existing group, never reshuffle (R12, spatial
constancy). Append new story beats; rewrite `now` entirely; set `delta: "new"`
or `"changed"` on everything that moved since the prior file.

| Work | Executor |
|---|---|
| Trigger gate, source survey, topology and grouping decisions, layout freeze | Inline (no delegation) |
| Bulk data-fill of `map.nodes` / `story.beats` on a large project (>60 nodes) | Subagent per group — **mid-tier** |
| Contested provenance, guardrail-to-beat linking, assembly, render | Inline at top tier |

If the Agent tool is unavailable, build everything inline — the grounded atlas,
not the delegation, is the deliverable.

## Phase 3 — REVIEW

1. **Design-rule check — always, inline.** Run the checklist in
   [references/design_rules.md](references/design_rules.md) §Review Checklist:
   every edge carries a verb; Overview shows no more boxes than groups and every
   aggregated edge is verb-labelled; every edge appears in List at least once;
   Grid shows its empty cells; the ego view labels every edge; ≤5 groups and no
   colour-only encoding; no legend or footnote key; every guardrail links to its
   origin beat; story is causal, not a dated list; four regions in canonical
   order; unknowns marked, not invented.
2. **Self-containment check — always.** `grep -n "http" Outputs/atlas.html`:
   hits allowed only inside the embedded JSON data, comments, or the shell's SVG
   namespace constant. Zero `<script src`, zero `<link href`; `url(` only as a
   same-document fragment. Confirm `<noscript>` and the `window.onerror` banner
   survived injection. A file that needs the network is a failed atlas.
3. **Render check — always.** A file that throws on load passes both checks
   above. Load `Outputs/atlas.html` and confirm the `window.onerror` banner is
   **not** showing and the Overview actually drew its group boxes. Where a
   headless runner is available (node + jsdom, Playwright), assert it: one box
   per group and one labelled edge per ordered group pair; a group click opens
   the member panel with the right member count; a node click opens the ego view
   with the right parent/child counts; List carries every edge as at least one
   chip; Grid's cells sum to the edge count and its diagonal equals the
   intra-group counts; all three toggles and search work. Fix the *data* and
   re-render; the shell is not edited to pass a check.
4. **Council review — gated.** Only on explicit request: launch
   `Skill(skill="coeus:llm-council", args="<the atlas + its sources>")` to
   stress-test the *claims* the atlas makes. Skip silently otherwise.

## Phase 4 — EVOLVE

After any run where the user corrected the grouping, rejected a beat, overrode
the trigger, or stated a preference: append one line to
`~/.coeus/atlas/learnings.md` per [references/design_rules.md](references/design_rules.md)
§Evolution — silently, patterns only, never project content. When a lesson
repeats ≥3 times, propose folding it into this skill as a normal version-bump
commit.

---

## Hard Rules

- **Never invent topology.** Every node, edge, and beat traces to a mined source
  or an explicit user answer; unknowns render as marked `?` placeholders.
- **Verbs on edges.** An unlabeled edge is a defect ("constrains", "feeds",
  "supersedes", "forked-from" — never a bare arrow).
- **Palette is the template's, not yours.** A fixed, CVD-validated five-slot
  categorical set, assigned by `group_order` position and stepped separately for
  light and dark. `"hue": null` is the one signal the data still sends: that
  group stays neutral grey. Hues are never duplicated — past five non-neutral
  groups the template refuses to invent a sixth and goes neutral, which the
  checklist reads as a grouping defect. Redundant shape/border on every encoded
  distinction; the atlas must read in monochrome.
- **`delta` is refresh-only.** Never set `new` or `changed` on a first build:
  there is nothing to have changed from, and the markers spend the R8
  signalling budget on noise.
- **Freeze the layout.** Regions never move; node order is inherited from the
  prior `atlas.json` on every refresh.
- **Self-contained output.** One HTML file, inline CSS/JS, no CDN, font, image,
  or network fetch. It must open from a NAS share with no network.
- **History is causal.** Beats state what/why/outcome. A dated event list is a
  failed Story region.
- Uncertainty handling per `_shared/uncertainty_rules.md`; design claims trace to
  `references/design_rules.md`, including its uncertainty flags.

## When NOT To Trigger

- The subject is not a project: a single question, one file, a prompt, a dataset.
- The user wants the underlying work done (decide it, structure it, audit it) —
  the atlas explains a project, it does not advance one.
- A visualisation request with no project behind it (a chart of some numbers, a
  UI mockup, a diagram for a slide).
