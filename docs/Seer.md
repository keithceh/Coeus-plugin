# Seer — Spec-Driven Routing Evaluation

> Spec-driven evaluation engine for Coeus itself: synthesizes labeled routing scenarios from skill frontmatter alone, holds the intended route as a hidden oracle, replays `coeus-router` blind, grades with a cascading decomposed rubric, and proposes golden-set rows.

**Version:** 1.0.0 (current) | **Triggers:** `/coeus:seer` · `"seer"` · `"routing eval"` · `"evaluate the router"` · `"test coeus routing"` · `"router regression"` · `"grade routing"`

---

## What This Is

Seer is Coeus's in-house measurement instrument, not a general testing tool. It adapts *Agent Seer: Synthesizing Scenarios from Specification Understanding* (Karumuri, Vemula & Lopes Pegna, Apple, arXiv 2608.26133) — a technique for generating evaluation scenarios from tool *specifications* alone, with no examples and no live execution — to Coeus's own tool surface:

- Each skill's **frontmatter is the tool specification**.
- **`coeus-router`** is the agent under test.
- The **routing golden set** (`skills/coeus-router/references/routing-golden-set.md`) is where confirmed failures become permanent regressions.

Because scenarios regenerate from the current skill registry on every run, the eval can never rot behind the catalog the way a fixed test suite would. The full rubric, cascade rules, report template, and provenance notes live in [`skills/seer/references/rubric.md`](../skills/seer/references/rubric.md).

Seer is pure prompt/protocol design — no code, no live execution. The paper's technique is entirely inference-time, and Seer stays that way.

---

## The Five Phases

**Phase 0 — Scope & Ground.** Parse arguments (default scope: every routable skill; `family <name>` or `skill <name>` narrows it). Load verbatim — never from memory — the skill registry, the router `SKILL.md`, the golden set, and the frontmatter of every in-scope skill. This encodes the headline lesson from an independent reproduction of the paper (ghchinoy/ai-paper-reproductions): the paper's judge scored a real unsupported-parameter bug a perfect 1.000 because the constraint lived outside the spec it was shown. A judge cannot penalize a rule it cannot see. Scenario budget defaults to 12, capped at 30 per run.

**Phase 1 — Interpret the Specs.** For each in-scope skill, using ONLY its frontmatter (name, description, argument-hint, dependencies) plus its registry row, emit `skill · family · does · needs · used_for · family_signals · boundary_risks`. Grounding is strict: knowledge of similarly named tools elsewhere must never add capabilities the frontmatter doesn't claim — spec-external "knowledge" is exactly how eval generators hallucinate.

**Phase 2 — Synthesize Scenarios.** Two tiers — simple (single-signal, everyday phrasing) and complex (multi-signal, needs a tie-breaker not a keyword match). Every scenario carries `query`, `tier`, `oracle` (gate outcome + family/skill, held out), `route_reason`, and `eval_value`. Coverage is forced: every in-scope skill must appear in at least one oracle, with a named-gap repair round if not. At least one BYPASS, one NO ROUTE, one two-way-tie clarifier, one sequential cross-family case, and a border case per touched tie-breaker are required. New scenarios must add coverage the golden set doesn't already have.

**Phase 3 — Blind Route.** Derive the router's answer for each query from the router `SKILL.md` alone, oracle withheld. Preferred: delegate to a subagent given only the router text and bare queries (genuine blindness). Inline fallback: produce the full routing block for every query before re-reading any oracle, and mark the report `Blindness: procedural only — same-context evaluation`.

**Phase 4 — Grade.** Deterministic checks first, never left to judgment: D1 routed skill exists in the registry, D2 output block format is legal, D3 launch stated for every PROCEED route (an actual Skill-tool call, not the inert slash command), D4 gate outcome is one of BYPASS/NO ROUTE/PROCEED/CLARIFIER. Then the decomposed rubric applies.

**Phase 5 — Report & Fold Back.** Per-family and per-tier score table, a failure taxonomy, and — for each confirmed failure — a proposed golden-set row plus, when the miss traces to a rule gap rather than a bad read, a proposed router-rule edit. **Proposals only** — Seer never edits `coeus-router` or the golden set without the user's explicit approval in the conversation.

---

## The Cascading Rubric

Full detail: [`skills/seer/references/rubric.md`](../skills/seer/references/rubric.md). Four dimensions, ten sub-dimensions, scored 0–10 and normalized:

| Dimension | Sub-dimensions |
|---|---|
| Gate (Step 0) | outcome, discipline |
| Family (Step 1) | correctness, signal_use |
| Skill (Step 2 + tie-breakers) | correctness, tie_breaker, sequencing |
| Protocol (output contract) | block, launch, restraint |

Cascading penalties exist because a plain mean over sub-scores would launder a fatal routing error into a respectable number. Applied top-down:

1. A deterministic failure (D1–D4) zeroes the whole record — no rubric pass. A route to a nonexistent skill is not "partially correct."
2. A wrong Gate outcome zeroes Family, Skill, and Protocol — nothing downstream of a wrong gate is creditable.
3. Family correctness ≤ 2 caps Skill and Protocol at 2 — a confident launch of the wrong family's skill is worse than a hesitant one.
4. Skill correctness ≤ 2 caps Protocol's launch sub-score at 2 — launching the wrong skill crisply is not protocol credit.

This is the paper's key metric contribution carried over: coarse name-match metrics score argument-value errors as perfect, and the cascade is what surfaces that failure class instead.

## Failure Taxonomy

Every non-perfect record gets exactly one primary label: `gate-forced-route`, `gate-missed-bypass`, `family-keyword-over-artefact`, `skill-tiebreaker-miss`, `skill-hallucinated`, `sequencing-dropped`, `clarifier-overuse`, `launch-omitted`, `logic-leak`, `format`.

---

## Honesty Rules

Seer is deliberately candid about what it cannot prove:

- Every report carries this line verbatim: *"Generator and judge share one model; agreement is not independent corroboration."* This replaces the paper's own judge-swap defense (Gemini vs Qwen), which held for tool-calling but broke down for coherence scoring (34% agreement within ±0.1 in the paper's own replication) — and is unavailable to a single-context skill anyway. Seer offers the user a rerun of Phase 4 through a different model when one is available.
- Grading is always against loaded text, never memory (Phase 0.2).
- Deterministic checks come before judgment, always.
- Seer never invents a skill and never accepts a route to one — D1 is a hard zero.
- Every verdict carries confidence markers per `_shared/uncertainty_rules.md`.

---

## When NOT to Use Seer

- Testing or QA of anything that isn't Coeus routing — code test suites, CI failures, other agents' evals, general prompt evaluation.
- Informational questions about Coeus or its skills ("which skill does X?", "how does the router work?") — that's router Step-0 NO-ROUTE territory; answer directly instead.
- "Audit the project files" — file-obsolescence audits belong to `project-lifecycle`, not Seer.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [Coeus Architecture →](Coeus-Architecture.md)
- [LLM-Council →](LLM-Council.md)
- [The Architect →](The-Architect.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.0.0** (current) | 2026-Aug-30 | Initial release. Five-phase Agent Seer adaptation; `coeus-router` v1.6.0 gains a Step-2a routing row + tie-breaker 12 for seer; golden set grows 27 → 29. |

Go back to the [Main README](../README.md).
