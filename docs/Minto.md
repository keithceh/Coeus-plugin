# Minto — Answer-First Document Structuring

> Applies Barbara Minto's Pyramid Principle — grounded, source-verified doctrine — to structure thinking and documents: answer first under a single point, SCQ introduction, question/answer vertical logic, MECE inductive groupings, ordered by time/structure/degree.

**Version:** 1.0.0 (current) | **Triggers:** `/coeus:minto` · `"minto"` · `"pyramid principle"` · `"SCQ this"` · `"pyramid this"` · `"lead with the answer"` · `"answer-first structure"` · `"restructure this document"` · `"storyline this deck"` · `"structure my memo"`

---

## What This Is

Minto is Coeus's **writing**-family skill (the only one in that family) — it structures the communication of a decision, not the decision itself. It fires only on explicit intent to structure, restructure, or storyline an executive document, memo, report, proposal, or deck.

Its defining feature is grounding discipline: [`references/doctrine.md`](../skills/minto/references/doctrine.md) distills three parallel deep-research passes (research date 2026-Aug-28), with every claim tagged by evidence tier — **[P-DIRECT]** (Minto's own words, from sources she controls or her recorded voice), **[P-BOOK]** (page-cited book text via named third-party reproduction hosts), or **[SECONDARY]** (corroboration only — no rule originates there). Conflicts across editions (1978 → 1987 → 1996 → 2002/2010; three-vs-four-part structures; story-order label variants) are reported, not smoothed over.

The doctrine file also carries a **Myth Ledger** the skill must never repeat. The headline entry: the widely circulated claim that Minto died in 2024 is unverified and apparently false — no obituary exists, name-matched obituaries belong to different people, and she is listed as living as of the research date. Also corrected there: "first woman at McKinsey" is really "first female MBA professional hire"; MECE is Minto's own invention, not "a McKinsey framework"; her trademark term is SCQ (SCQA/SCQR are derivative labels); and the book's first publication was 1978, not 1985.

Deliverable-specific application (how the method maps onto board memos, gate reviews, stakeholder updates, and the rest) lives in [`references/playbooks.md`](../skills/minto/references/playbooks.md). The skill improves from use per [`references/evolution.md`](../skills/minto/references/evolution.md).

---

## Trigger Gate and the Hard NOT-Trigger List

**Manual:** `/coeus:minto` or any Trigger-on phrase always fires.

**Auto-fire requires all three:**
1. The task is to *structure* thinking for a reader — a new memo, report, proposal, recommendation, gate submission, update, or deck storyline, or a structural review/rebuild of an existing one.
2. The deliverable is expository business communication (Minto's own scope limit) with an identifiable reader and question.
3. No neighbouring skill owns the request.

**Minto does NOT fire on** (defers silently, no announcement):

| Request shape | Owner instead |
|---|---|
| Generic writing, copy-editing, tone, grammar, formatting | (not Minto's domain) |
| Deciding *what* to do | `llm-council` / `ep-council` — structure the communication of a decision already reasoned, don't reason it |
| Handover notes, changelogs, session resumes | `project-lifecycle` |
| DOCX mechanics — captions, fields, corruption | `ooxml-*` / `docx-inventory` |
| Prompt engineering | `prompt-master` / `morpheus` |
| Creative writing, narratives, marketing copy, UX text | other installed drafting skills own these; Minto contributes structure only if asked |
| A repeat request already rejected once this conversation | none — offer once per conversation at most |

Minto states `Mode: MANUAL` or `Mode: AUTO` in one line whenever it fires.

---

## The Four Phases

### Phase 1 — FRAME (top-tier, never delegated)

Run at the strongest available reasoning model. Reads `~/.coeus/minto/learnings.md` if present and applies its `PREF`/`STRUCTURE-*` entries for the deliverable type.

1. Identify the reader and the reader's Question, asking at most one clarifier only if genuinely undeterminable.
2. Build top-down: Subject → Question → Answer → Situation → Complication → recheck that the Complication really raises the Question. If the Answer won't come, drop to bottom-up or the R1/R2 problem-definition frame and say so.
3. Build the Key Line: inductive by default, 3–5 same-kind points, MECE-checked, ordered by time/structure/degree, each summarized by effect or implication — never a blank label.
4. Output the skeleton — SCQ + Answer + Key Line, one screen or less (the 30-second test).

**Gate:** board/investment/gate-review/proposal-class deliverables stop here for approval before drafting continues. Short or routine deliverables (email, one-pager, recurring update), or a request for the finished product in one pass, proceed straight through — Minto states which path it took.

### Phase 2 — BUILD (tiered, escalating)

| Work | Executor |
|---|---|
| Skeleton only, email/one-pager, structural review verdict | Inline (no delegation) |
| Standard sections of an approved skeleton | Subagent per section — **Sonnet** |
| High-stakes sections (board ask, valuation case, risk position), heavy synthesis, or a Sonnet draft failing pyramid QA | Escalate that section to **Opus** |
| Cross-section coherence weave, final assembly | Inline at top tier |

Each subagent gets the full skeleton, its section's Key-Line point, the relevant playbook rules, and the ban on blank headings. If subagent delegation or model overrides aren't available, everything drafts inline — the pyramid, not the delegation mechanism, is the deliverable.

### Phase 3 — REVIEW (layered, heaviest only where warranted)

1. **Pyramid QA — always, inline.** Tested against doctrine: answer first; the introduction contains only what the reader will accept as true; every grouping is same-kind, ordered, and summarized by effect/implication; vertical Q/A holds with no unraised answers or unanswered raised questions; headings read as ideas; the document reads as prose without headings; the 30-second test passes. Fixed before proceeding.
2. **Council review — gated.** Only for high-stakes deliverables (board / investor / JV / gate submissions) or on explicit request: Minto launches `Skill(skill="coeus:llm-council", args="<the deliverable + its skeleton>")` to stress-test the *argument* the structure carries. It never reimplements the council itself, and skips this step silently for routine deliverables.
3. **Final read — top tier, always.** One cold pass at the strongest model, reading as the target reader: does the first screen answer my question? Where do I stop trusting it? Fixed, then delivered.

### Phase 4 — EVOLVE

After any run where the user corrected the structure, overrode the trigger, or stated a preference, Minto appends one dated, patterns-only line to `~/.coeus/minto/learnings.md` — never document content. Entry kinds: `TRIGGER-FP`, `TRIGGER-MISS`, `PREF`, `STRUCTURE-ACCEPTED`, `STRUCTURE-REJECTED`. When a lesson repeats three or more times, Minto proposes folding it into the skill itself (a trigger-rule change, playbook amendment, or doctrine clarification) as a normal version-bump commit — never a silent in-place mutation. Doctrine changes only with new PRIMARY evidence; user preferences adapt the playbooks, never the doctrine.

---

## Hard Rules

- Every claim about what Minto taught must trace to `doctrine.md`. Never assert anything in its Myth Ledger. Direct Minto quotes stay under 15 words, attributed.
- Structure before prose: never line-edit a document whose pyramid fails the three rules — rebuild first.
- Uncertainty handling per `_shared/uncertainty_rules.md`.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [LLM-Council →](LLM-Council.md) (the gated review dependency)
- [Project-Lifecycle →](Project-Lifecycle.md) (owns handovers/changelogs — the primary NOT-trigger neighbour)
- [Coeus Architecture →](Coeus-Architecture.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.0.0** (current) | 2026-Aug-28 | Initial release. New **writing** router family; `coeus-router` v1.5.0 gains Step 2e + tie-breaker 11; golden set grows 22 → 27. |

Go back to the [Main README](../README.md).
