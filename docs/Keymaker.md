# Keymaker — Coordinated Project Deliverables Pass

> Opens every door in a project in one pass: chains `project-lifecycle` and `atlas`, sweeps every other deliverable through its owner skill, and holds the lot to the house visual-quality bar — top-tier plan and review, delegated execution, loop until green.

**Version:** 1.0.0 (current) | **Triggers:** `/coeus:keymaker` · `"keymaker"` · `"full project pass"` · `"end-to-end project pass"` · `"coordinate all deliverables"` · `"refresh every deliverable"` · `"chain lifecycle and atlas"` · `"sweep the project artefacts"`

---

## What This Is

Keymaker is Coeus's Tier-2 **orchestration** skill for a whole project at once. It is not a fourth deliverable engine sitting beside `project-lifecycle`, `atlas`, and `evergreen-artefacts` — it is the skill that chains the first two, coordinates every other deliverable through its own owner skill, and then applies one shared visual-quality bar across whatever the pass touched.

The load-bearing rule is architectural: **Keymaker launches its dependencies via the Skill tool and never reimplements their logic.** `project-lifecycle` still owns kickoff/resume/handover/audit; `atlas` still owns the four evergreen visual outputs and their own create/refresh gate; `evergreen-artefacts` publishing is offered gated, on request only. Keymaker's own contribution is the sequencing, the ledger, and the quality pass — nothing else.

---

## Phase 0 — Trigger Gate

Manual invocation always fires. Auto-fire requires all three: the request spans two or more deliverable classes (session files *and* the atlas, and/or other visual artefacts) or explicitly asks for an end-to-end/whole-project sweep; the subject is a bounded project; and no single owner skill already covers the whole ask. It states `Mode: MANUAL` or `Mode: AUTO` in one line when it fires.

## The Keyring

Phase 1 (PLAN) runs at the strongest available reasoning tier and is never delegated. It surveys sources in the same priority `atlas` Phase-1 uses — lifecycle files → git repo → document folder → interview — and builds the **Keyring**: one ledger row per deliverable, with columns for Deliverable, Owner skill, State, Gap, and Planned action.

State is one of **green / amber / red / unknown**. The truthfulness rule is hard: every row must trace to a file actually read or an explicit user answer — unknowns are marked `?`, never guessed and never quietly dropped. The keyring and run plan are presented together on one screen; the `plan-only` argument stops the run there.

## The Six Phases

| Phase | What happens |
|---|---|
| 0 — Trigger Gate | Manual or auto-fire check; states Mode |
| 1 — PLAN | Top-tier survey, builds the Keyring, `plan-only` stops here |
| 2 — EXECUTE | Ordered dependency chain, delegated at the right tier |
| 3 — VISUAL QUALITY PASS | Every visualisation artefact checked against the quality bar |
| 4 — REVIEW | Top-tier re-walk of the Keyring, loop until green |
| 5 — REPORT | Keyring table, artefacts treated, next actions, gated publish offer |

### Phase 2 — model-tier orchestration

Execution follows an ordered chain: `project-lifecycle` first (kickoff if no handover exists, else resume; handover and audit as the keyring demands), then `atlas` (create or refresh under its own Phase-2 gate — an existing `atlas.json` makes the run a refresh regardless of the invocation), then every remaining **red** keyring row through its owner skill.

Work is split by tier, not by convenience:

| Work | Executor |
|---|---|
| Orchestration, sequencing, keyring decisions | Inline — top tier, never delegated (Fable-class) |
| Independent deliverable builds (an atlas data-fill, a report section) | Subagent — **Opus** |
| Mechanical refreshes, doc regeneration, inventory sweeps | Subagent — **Sonnet** |
| Contested or cross-deliverable coherence work | Inline at top tier |

If the Agent tool or model overrides are unavailable, everything runs inline — the keyring, not the delegation mechanism, is the deliverable.

### Phase 3 — The Visual Quality Pass

Every visualisation artefact in the project — `atlas.html`, `atlas_toc.html`, lineage explorers, standalone HTML/SVG, charts, diagrams — is checked against [`skills/keymaker/references/quality_bar.md`](../skills/keymaker/references/quality_bar.md). That file is itself distilled from `atlas`'s evidence-graded `design_rules.md`; where the two disagree, `design_rules.md` wins. Its six sections:

1. **Orientation** — a cold reader understands what they're looking at in one glance; a "you are here" marker where the artefact has a current position; nothing decorative.
2. **Encoding honesty** — every arrow carries a verb; no colour-only encoding; a validated ≤5-hue categorical palette; magnitude as a single-hue ramp, never a second categorical slot; it reads in monochrome; empty cells and negative space are shown, not dropped.
3. **Direct labelling** — labels sit on the marks; no legend or footnote key where a direct label fits.
4. **Typography and surface** — a deliberate type scale, a readable measure, both light and dark themes (or one committed look painted explicitly), a print stylesheet, `prefers-reduced-motion` honoured.
5. **Self-containment and robustness** — offline artefacts stay offline (no CDN, webfont, or network call — this outranks section 4 entirely), `noscript` completeness, graceful failure on script errors.
6. **Truthfulness** — every visual element traces to real data; unknowns are marked, never invented; captions state what the reader is seeing and where it came from.

The pass treats **only** artefacts that fail — an artefact already meeting the bar is untouched. **Idempotence is the test**: re-running the pass over a passing artefact must change zero bytes; a pass that rewrites a passing file is a bug in the pass. And **self-containment outranks styling**: Keymaker never breaks an artefact's own hard rules to meet the bar — a self-contained offline file never gains a CDN, a webfont, or a network fetch just to satisfy section 4. Where richer session-level design skills are available (`artifact-design`, `dataviz`, `theme-factory`), Keymaker loads and defers to them; `quality_bar.md` is the always-available fallback contract. The `skip-visual-pass` argument skips Phase 3 entirely.

### Phase 4 — Loop Until Green

Phase 4 re-walks the keyring at the strongest model. Every row must be **green**, or amber **explicitly accepted by the user** — with each dependency's own review gates re-run (the `atlas` Phase-3 checks, lifecycle files updated in place, no versioned or timestamped sibling of any evergreen output anywhere). Any red, or any unaccepted amber, sends the run back to Phase 2/3.

**Hard cap: three full cycles.** After that, Keymaker stops and reports what is still red and why — honestly. A keyring declared green that isn't is treated as a worse failure than a reported red.

## Phase 5 — Report

A keyring table (deliverable · owner · state · action taken), one line per visual artefact treated naming the bar items it failed, next actions, a gated offer of `evergreen-artefacts` publishing (on request only), and a telemetry record into handover §8 per `project-lifecycle`'s counting rules.

---

## Hard Rules

- Launches dependencies, never reimplements them — zero domain logic duplicated from `project-lifecycle`, `atlas`, or any owner skill.
- Create-once-update-in-place is inherited everywhere; Keymaker never produces a versioned or timestamped sibling of any evergreen file.
- Never invents state — every keyring row traces to a file read or a user answer.
- The visual pass is idempotent and self-containment always outranks styling.
- Loop until green, three-cycle cap; remaining reds are reported, never hidden.

## When NOT to Use Keymaker

- **One deliverable named** — its owner skill handles it directly: "just refresh the atlas" → `atlas`, "update the handover" → `project-lifecycle`, "publish this" → `evergreen-artefacts`. Per the router's tie-breaker rule 14, a single-deliverable ask always falls through to the owner skill, never Keymaker.
- The decision itself, not the deliverables → the `decision` family.
- Structuring a document for a reader → `minto`.
- A first-time build of one artefact ("draw me a map of this project") → `atlas` alone.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [Atlas →](Atlas.md)
- [Evergreen Artefacts →](Evergreen-Artefacts.md)
- [Project-Lifecycle →](Project-Lifecycle.md)
- [Coeus Architecture →](Coeus-Architecture.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.0.0** (current) | 2026-Sep-09 | Initial release. Tier-2 cluster chaining `project-lifecycle` and `atlas` over every deliverable, gated to `evergreen-artefacts` for publishing. Part of Coeus v3.26.0; `coeus-router` gains the Step-2b keymaker row and tie-breakers 13–14 (v1.7.0 → v1.8.0); routing golden set grows 31 → 35. |

Go back to the [Main README](../README.md).
