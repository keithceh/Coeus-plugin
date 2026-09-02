---
name: minto
version: 1.0.0
argument-hint: "[document, deck, memo, or draft to structure — or text to review against the pyramid]"
description: >-
  Trigger on: /coeus:minto, "minto", "pyramid principle", "SCQ this", "pyramid this", "lead with the answer", "answer-first structure", "restructure this document", "storyline this deck", "structure my memo". Auto-fire only on explicit intent to STRUCTURE, restructure, or storyline an executive document, memo, report, proposal, or deck — never on generic writing, editing, formatting, or file-mechanics requests. Verified Barbara Minto doctrine: pyramid, SCQ, MECE, inductive key line.
dependencies:
  - llm-council
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these whenever this skill emits a judgment, recommendation, or simulated voice.

# Minto — Pyramid Principle Structuring Engine

Applies Barbara Minto's Pyramid Principle — grounded, source-verified doctrine in
[references/doctrine.md](references/doctrine.md) — to structure thinking and
documents: answer first under a single point, SCQ introduction, question/answer
vertical logic, MECE inductive groupings, ordered by time/structure/degree.
Deliverable-specific application lives in
[references/playbooks.md](references/playbooks.md); the skill improves from use
per [references/evolution.md](references/evolution.md).

---

## Trigger Gate (Phase 0)

**Manual:** `/coeus:minto` or any Trigger-on phrase — always fires.

**Auto-fire — ALL three must hold:**
1. The task is to *structure* thinking for a reader: a new memo, report,
   proposal, recommendation, gate submission, update, or deck storyline — or a
   structural review/rebuild of an existing one.
2. The deliverable is expository business communication (Minto's own scope
   limit) with an identifiable reader and question.
3. No neighbouring skill owns the request (see NOT-trigger).

**Do NOT fire on** (defer silently — no announcement):
- Generic writing, copy-editing, tone, grammar, or formatting requests.
- Deciding WHAT to do (that is `llm-council` / `ep-council` territory — Minto
  structures the communication of a decision already reasoned; if the user needs
  the decision itself stress-tested, route there first, structure after).
- Handover notes, changelogs, session resumes (`project-lifecycle` owns these).
- DOCX mechanics — captions, fields, corruption (`ooxml-*` / `docx-inventory`).
- Prompt engineering (`prompt-master` / `morpheus`).
- Creative writing, narratives, marketing copy, UX text, or any non-expository
  form. Other installed skills (stakeholder-update, content-creation,
  doc-coauthoring) own drafting workflows: if one has already fired, contribute
  the structure ONLY if asked.
- A repeat request in a conversation where the user already rejected a Minto
  structuring offer. When uncertain whether structuring is wanted: don't fire;
  offer in one line at most once per conversation.

State `Mode: MANUAL` or `Mode: AUTO` in one line when firing.

## Phase 1 — FRAME (plan at top tier)

Run at the strongest available reasoning (the session's top model — Fable-class;
never delegate framing). Read `~/.coeus/minto/learnings.md` if it exists and
apply `PREF`/`STRUCTURE-*` entries for this deliverable type.

1. Identify the reader and the reader's Question (doctrine §12). Ask the user at
   most ONE clarifier, only if reader or question is genuinely undeterminable.
2. Build top-down (doctrine §11): Subject → Question → Answer → Situation →
   Complication → recheck C raises Q. If the Answer won't come, drop to
   bottom-up or the R1/R2 problem-definition frame (§9) and say so.
3. Build the Key Line: inductive by default (§4), 3–5 same-kind points,
   MECE-checked (§6), ordered by time/structure/degree (§8), each summarized by
   effect or implication — never a blank label (§7).
4. Output the **skeleton**: SCQ + Answer + Key Line, ≤ one screen (the
   30-second test, §13), per the deliverable's playbook.

**Gate:** for board/investment/gate-review/proposal-class deliverables, present
the skeleton and wait for approval before drafting. For short or routine
deliverables (email, one-pager, recurring update) or when the user asked for the
finished product in one pass, proceed straight through — state which path was
taken.

## Phase 2 — BUILD (execute at the right tier, escalate as needed)

| Work | Executor |
|---|---|
| Skeleton only, email/one-pager, structural review verdict | Inline (no delegation) |
| Standard sections of an approved skeleton | Subagent per section — **Sonnet** |
| High-stakes sections (board ask, valuation case, risk position), heavy synthesis, or a Sonnet draft failing pyramid QA | Escalate that section to **Opus** |
| Cross-section coherence weave, final assembly | Inline at top tier |

Each subagent receives: the full skeleton, its section's Key-Line point, the
playbook rules for the deliverable, and the ban on blank headings. If the Agent
tool or model overrides are unavailable, draft everything inline — the pyramid,
not the delegation, is the deliverable.

## Phase 3 — REVIEW (layered, heaviest only where warranted)

1. **Pyramid QA — always, inline.** Test against doctrine: Answer first; intro
   contains only what the reader will accept as true; every grouping same-kind,
   ordered, summarized by effect/implication; vertical Q/A holds (no unraised
   answers, no unanswered raised questions); headings read as ideas; document
   reads as prose without headings; 30-second test passes. Fix before proceeding.
2. **Council review — gated.** Only for high-stakes deliverables (board /
   investor / JV / gate submissions) or on request: launch
   `Skill(skill="coeus:llm-council", args="<the deliverable + its skeleton>")`
   to stress-test the ARGUMENT the structure carries. Never reimplement the
   council here. Skip silently for routine deliverables.
3. **Final read — top tier, always.** One pass at the strongest model, reading
   as the target reader, cold: does the first screen answer my question? Where
   do I stop trusting it? Fix, then deliver.

## Phase 4 — EVOLVE

After any run where the user corrected the structure, overrode the trigger, or
stated a preference: append one line to `~/.coeus/minto/learnings.md` per
[references/evolution.md](references/evolution.md) — silently, patterns only,
never document content. When a lesson repeats ≥3 times, propose folding it into
this skill as a normal version-bump commit.

---

## Hard Rules

- **Grounding:** every claim about what Minto taught must trace to
  [references/doctrine.md](references/doctrine.md). Never assert items in its
  Myth Ledger. Direct Minto quotes stay under 15 words, attributed.
- **Structure before prose.** Never line-edit a document whose pyramid fails the
  three rules — rebuild first (§14).
- Doctrine changes only with new PRIMARY evidence; user preferences adapt the
  playbooks, never the doctrine.
- Uncertainty handling per `_shared/uncertainty_rules.md`.
