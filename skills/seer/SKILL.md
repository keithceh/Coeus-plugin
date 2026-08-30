---
name: seer
version: 1.0.0
argument-hint: "[scope — all | family <name> | skill <name>] [optional scenario count, default 12]"
description: >-
  Trigger on: /coeus:seer, "seer", "routing eval", "evaluate the router", "test coeus routing", "router regression", "grade routing". Spec-driven evaluation engine for Coeus itself: synthesizes labeled routing scenarios from skill frontmatter alone, holds the intended route as a hidden oracle, replays coeus-router blind, grades with a cascading decomposed rubric, and proposes golden-set rows. Never fires on generic testing/QA of non-Coeus code or agents.
dependencies:
  - coeus-router
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these to every score and verdict this skill emits.

# Seer — Spec-Driven Routing Evaluation

Adapts the Agent Seer protocol (Karumuri, Vemula & Lopes Pegna, arXiv 2608.26133 — evaluation scenarios synthesized from tool *specifications*, with no examples and no live execution) to Coeus's own tool surface: each skill's frontmatter **is** a tool specification, `coeus-router` is the agent under test, and the routing golden set is where confirmed failures become permanent regressions. Scenarios regenerate from the current registry on every run, so the eval can never rot behind the catalog. Full rubric, cascade rules, report template, and provenance: [references/rubric.md](references/rubric.md).

---

## Phase 0 — Scope & Ground

1. Parse arguments. Default scope: every routable skill in the registry (all families; `coeus-router` itself is the subject, never a route target). `family <name>` or `skill <name>` narrows it.
2. Load into context, verbatim: `skills/_shared/SKILL_REGISTRY.md`, `skills/coeus-router/SKILL.md`, `skills/coeus-router/references/routing-golden-set.md`, and the frontmatter of every in-scope `SKILL.md`. **A judge cannot penalize a rule it cannot see** — never grade from memory of these files. If any fails to load, stop and say which.
3. State the scenario budget: default 12, cap 30 per run.

## Phase 1 — Interpret the Specs

For each in-scope skill, using ONLY its frontmatter (name, description, argument-hint, dependencies) plus its registry row (family, tier), emit a compact interpretation record:

```
skill · family · does · needs · used_for · family_signals · boundary_risks
```

`boundary_risks` names the neighbour skills that could plausibly claim the same request — these seed the border scenarios. Ground every field strictly in the spec: knowledge of similarly named tools elsewhere must not add capabilities the frontmatter doesn't claim. Spec-external capabilities are exactly how eval generators hallucinate.

## Phase 2 — Synthesize Scenarios

Two tiers. **Simple** = commonplace, single-signal, the request a real user types on an ordinary day. **Complex** = multi-signal queries where the correct route needs a tie-breaker, not a keyword match. Every scenario record carries all fields — the rationale fields force route-reasoning at generation time, not post-hoc:

```
query:        realistic user phrasing (casual tone, typos, file paths, E&P context all welcome)
tier:         simple | complex
oracle:       gate outcome (BYPASS | NO ROUTE | PROCEED) + family/skill [+ next-skill if sequential]
route_reason: why this route is right, citing the router rule it exercises
eval_value:   the routing failure this scenario would catch
```

Composition rules:

1. **Coverage is forced.** Every in-scope skill appears in at least one oracle. After the first pass, list any uncovered skills BY NAME and generate a repair round that combines them with already-covered ones.
2. Include at least one each: BYPASS, NO ROUTE, two-way-tie clarifier, sequential cross-family request (router rule 9), and a border case for every tie-breaker the scope touches.
3. Do not duplicate golden-set rows — those are already pinned. New scenarios must add coverage the golden set lacks.
4. The oracle is **held out**: it exists to grade against, never to be shown to the routing pass.

## Phase 3 — Blind Route

Derive the router's answer for each query from the router `SKILL.md` rules alone, oracle withheld. Preferred (Claude Code): delegate to a subagent given only the router `SKILL.md` text and the bare queries — genuine blindness. Inline fallback (single context): produce the full routing block for every query, in order, *before* re-reading any oracle, then mark the report `Blindness: procedural only — same-context evaluation`.

## Phase 4 — Grade

Deterministic checks first — never spend judgment on the machine-checkable:

- **D1** routed skill exists in the registry
- **D2** output block format is legal (`FAMILY/ROUTE/WHY/RUN`, or a legal gate line)
- **D3** launch stated for every PROCEED route (Skill-tool call, not just the inert slash command)
- **D4** gate outcome is one of BYPASS / NO ROUTE / PROCEED / CLARIFIER

Then apply the decomposed rubric in [references/rubric.md](references/rubric.md): four dimensions (Gate, Family, Skill, Protocol), sub-scored 0–10, with **cascading penalties** — a wrong gate zeroes everything downstream; a wrong family caps Skill and Protocol at 2. One critical error must collapse the record's score, not average away into a 0.9.

## Phase 5 — Report & Fold Back

Emit the report per the template in [references/rubric.md](references/rubric.md): per-family and per-tier score table, failure taxonomy, and — for each confirmed failure — a proposed golden-set row (per that file's maintenance rule) plus, when the miss traces to a rule gap rather than a bad read, a proposed router rule edit. **Proposals only**: never edit `coeus-router` or the golden set without the user's explicit approval in this conversation.

---

## Honesty Rules (hard)

- Every report carries this line verbatim: *"Generator and judge share one model; agreement is not independent corroboration."* Offer the user a rerun of Phase 4 through a different model when one is available to them.
- Grade against loaded text, never memory (Phase 0.2).
- Deterministic checks before judgment, always.
- Never invent a skill; never accept a route to one (D1 is a hard zero).
- Confidence markers on every verdict per `_shared/uncertainty_rules.md`.

## When NOT To Trigger

- Testing or QA of anything that is not Coeus routing: code test suites, CI failures, other agents' evals, prompt evaluation in general.
- Informational questions about Coeus or its skills ("which skill does X?", "how does the router work?") — that is router Step-0 NO-ROUTE territory; answer directly.
- "Audit the project files" — file-obsolescence audits belong to `project-lifecycle`, not seer.
