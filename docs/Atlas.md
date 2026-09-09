# Atlas — The Project, At A Glance

> Renders any project — codebase, report, deal, vault, field study — as one self-contained interactive HTML file a reader can open cold and understand at a glance: intent, scope, artifact map, causal history, guardrails, re-entry state.

**Version:** 1.3.0 (current) | **Triggers:** `/coeus:atlas` · `"project atlas"` · `"project map"` · `"project at a glance"` · `"visualise this project"` · `"visualize this project"` · `"explain this project visually"` · `"map my project"`

---

## What This Is

Atlas is a Tier-1 `tools`-family skill built on the house extract-then-render pattern: mine the project once into structured JSON, then render that JSON into fixed, evidence-graded regions. It fires only for a **visual overview of a whole project** — never for DUG lineage, session resume/handover, or document structuring, all of which it defers to their owner skills.

## The Four Evergreen Outputs

Atlas produces exactly four files, **created once and updated in place forever**:

| File | Role |
|---|---|
| `Outputs/atlas.json` | Structured truth — the only file the survey writes by hand (schema in [`references/schema.md`](../skills/atlas/references/schema.md)) |
| `Outputs/atlas.html` | Rendered from `references/template.html` by replacing the literal `/*__ATLAS_DATA__*/{}` injection point |
| `Outputs/atlas_moc.md` | Master of Content — the same truth as a linkable markdown directory, by-group and by-kind |
| `Outputs/atlas_toc.html` | Table of Contents — the visual front door: quick-link chips, an inline SVG ecosystem explainer, a contents grid, no-JS-complete |

A second copy of any of them — `atlas_v2`, a dated filename, a `(1).html` — is a defect. If `atlas.json` already exists, the run **is** a refresh no matter how it was invoked or what its first argument says; Atlas announces this in one line (`existing atlas found — refreshing in place`). On refresh, the MoC and ToC are derived entirely from the JSON and are overwritten in full, never merged — the one legitimate new file on a refresh is a MoC or ToC that an atlas built before it existed doesn't yet have.

## The Four Frozen Regions

Canonical order, never reordered between versions:

1. **① FRAME** — intent, scope in/out, guardrails (each linked to the beat that created it), references.
2. **② NOW** — the re-entry cue: where work stopped, open threads, next actions.
3. **③ MAP** — see below.
4. **④ STORY** — causal beats (did X → because Y → hence Z), forks as branches, guardrail badges linking back to FRAME. A dated event list is a failed Story region.

## The Map: Three Views, Not One Graph

The Map region did not start this way. v1.0.0 shipped a single full node-link graph; v1.1.0 replaced it with three views after a six-way bake-off (2026-Sep-02, recorded in `design_rules.md`) run on this repo's own atlas data (26 nodes / 37 edges / 5 groups):

- **Overview (default)** — group-level enclosures, one aggregated verb-labelled edge per ordered group pair, intra-group edges as an in-box count.
- **List** — the relation tree: every edge present as at least one named chip, chip-click jump. Zero SVG, monochrome-proof — the print form.
- **Grid** — the group-to-group matrix, cell = count + dominant verb, diagonal = intra-group, **empty cells drawn visibly**.

Node drill-in is a member panel → **ego view** (node centered, parents left / children right, every edge verb-labelled) — never a full node-link graph. **Why the full graph was rejected:** the bake-off found one hub node held 16 of the 37 edges; at that concentration its edge bundle crossed three of the five group columns and roughly a third of verb labels landed on top of node bodies, readable only by pinning — a query tool, not a map (measuring R6: "if it becomes a hairball, regroup, do not route"). In-place group expansion was tried and rejected too: expanding a group that contains a hub's targets reproduces the same occlusion in miniature, which is why drill-in opens a separate panel instead. The Grid view exists because the matrix comparison showed only 11 of 25 possible directed group-pairs carried any relation at all — negative space that a node-link form structurally cannot draw. A parallel finding: clustering the same adjacency data never recovered the five declared groups (purity 54%, adjusted Rand 0.05) — group membership is a reader's-mental-model judgment, not something to derive from link structure (R5).

## The Validated Five-Slot Palette

v1.0.0 derived each group's colour as `hsl(hue, 45%, 44%)` from an integer in `layout.hues`. Run through a CVD validator (protanopia/deuteranopia, Machado 2009), the four hues this project had picked measured a worst-pair ΔE of 5.2 against a ≥8 target — they read as grey, not as identity — and no four-hue set held up in both light and dark. Atlas now ships a **fixed, validated five-slot categorical palette**, assigned by `group_order` position and never chosen by the data: numeric `layout.hues` values are advisory and ignored, and only `"hue": null` still carries meaning (that group renders neutral grey). Past five non-neutral groups the template refuses to invent a sixth hue and goes neutral — read by the review checklist as a grouping defect to fix, not a colour problem. Shape (per-`kind` corner radius) and border-dash (per-`status`) redundancy carry the same distinctions in monochrome.

## Survey, Gate, and Truthfulness

Phase 1 (SURVEY) runs inline at the top tier and mines sources in a fixed priority order, stopping at the first that applies:

| Shape | Sources mined |
|---|---|
| a. Lifecycle-managed | Handover §1–§9, `Outputs/artefacts_index.md`, `Outputs/_telemetry/log.md` |
| b. Git repo | README, CHANGELOG, `docs/`, file tree, `git log` |
| c. Document folder | File inventory, titles/dates/status, folder structure |
| d. No files | Six-question interview: intent · scope · artifacts · history · guardrails · current state |

**Truthfulness rule (hard):** every node, edge, and beat traces to a mined source or an explicit user answer, recorded in `meta.sources[]`. What cannot be established renders as a marked `?` placeholder with `status: unknown` — never guessed, never quietly dropped. A whole-project atlas targets 25–35 map nodes; past that, Atlas regroups rather than adding nodes.

**Create/refresh gate:** Phase 2 opens by checking for `Outputs/atlas.json` before writing anything — its presence alone forces a refresh. Refresh loads the prior JSON first and preserves `layout.node_order` and `layout.group_order` verbatim; new nodes append inside their existing group, never reshuffle (R12, spatial constancy); `now` is rewritten entirely and everything that changed is marked `delta: "new"` or `"changed"` — never on a first build, since there is nothing to have changed from.

## Self-Containment

Hard rules, not preferences: no CDN, no external font, no image fetch, no network call in either derived HTML file — `atlas.html` must open from a NAS share with the network off, and the ToC must read in full with scripting off. `references/design_rules.md` and the Phase-3 self-containment check (`grep -n "http" Outputs/atlas.html`) enforce it: hits are allowed only inside the embedded JSON data, comments, or the SVG namespace constant; zero `<script src`, zero `<link href`.

## Phase 3 — Review

Four checks, always run: a **design-rule check** against the full `design_rules.md` checklist (every edge verb-labelled, ≤5 groups, no colour-only encoding, no legend, MoC and ToC each list every node exactly once); the **self-containment grep** above; an **output check** confirming `Outputs/` holds exactly the four named files and no versioned sibling; and a **render check** confirming the `window.onerror` banner is not showing and the Overview actually drew its boxes.

The render check carries a hard-won lesson. v1.2.0's headless test suite passed in full while a real user's mouse click on a group box did nothing — the pan handler called `setPointerCapture` on `pointerdown` unconditionally, so the browser retargeted the following `click` to the capturing wrapper and the group box's own handler never fired. Every automated test had driven clicks with synthetic `dispatchEvent(new MouseEvent('click'))`, which bypasses pointer capture entirely and so never caught it. The v1.2.1 fix waits for an actual drag (movement > 4px) before capturing the pointer, and the doctrine is now load-bearing: **drive clicks with real pointer input where the runner supports it (Playwright mouse), never `dispatchEvent` alone** — synthetic clicks can pass a suite while a human's click does nothing.

A fifth check, **council review**, is gated: only on explicit request does Atlas launch `Skill(skill="coeus:llm-council", args="<the atlas + its sources>")` to stress-test the atlas's claims; it is skipped silently otherwise.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [Keymaker →](Keymaker.md)
- [Project-Lifecycle →](Project-Lifecycle.md)
- [Coeus Architecture →](Coeus-Architecture.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.3.0** (current) | 2026-Sep-08 | `atlas_toc.html` — the fourth evergreen output, a visual Contents hub with an inline SVG ecosystem explainer, quick-link chips, and a by-group/by-kind contents grid. Evergreen gate now covers four files. |
| **1.2.1** | 2026-Sep-04 | Fix: Overview drill-in dead to real mouse clicks — a pointer-capture bug shipped in v1.1.0/v1.2.0. Render check now requires verification under real pointer input, not just synthetic `dispatchEvent`. |
| **1.2.0** | 2026-Sep-04 | `atlas_moc.md` — a Master of Content, the third evergreen output. Formalised the create/refresh gate: existing `atlas.json` forces a refresh regardless of how the run was invoked. |
| **1.1.0** | 2026-Sep-04 | Map region replaced with three views (Overview / List / Grid) plus member-panel → ego-view drill-in, following a six-way bake-off. Validated five-slot categorical palette replaces the raw HSL derivation that failed CVD-safety validation. |
| **1.0.0** | 2026-Sep-01 | Initial release. Four frozen regions, single node-link Map, evidence-graded `design_rules.md` doctrine. Shipped with `coeus-router` v1.7.0 (Step-2b atlas row + tie-breaker 13); routing golden set grew 29 → 31. |

Go back to the [Main README](../README.md).
