# The Architect — The Full Decision Pipeline

> An adaptive combo skill that chains three sub-skills — prompt-master, caveman, and llm-council — into a single orchestrated pipeline. The highest-intensity tool in the Coeus suite, for when the stakes justify the full deliberation cycle.

**Version:** 1.1.0 (current) | **Triggers:** `/architect` · `/archi` · `"full pipeline"` · `"architect this"` · `"stress-test and plan this properly"` · `"run the full council with prompt engineering"` · optional flag `--explore`

---

## What This Is

The Architect is Coeus's top-of-stack decision tool. Rather than owning any deliberation logic itself, it chains three existing skills in sequence:

```
prompt-master  →  caveman  →  llm-council
   (craft)         (compress)     (deliberate)
```

`prompt-master` turns the user's raw input into a precision-engineered council brief (problem statement, constraints, output format, success criteria). `caveman` compresses that brief for token efficiency — **and only the brief**: it is never applied to `Final_Plan.md`, `Premortem_Report.md`, or any artifact the council produces. `llm-council` then runs its full four-phase pipeline (Socratic clarification, strategic roadmap with a gated approval, tri-team adversarial red-teaming, and a six-month failure premortem) against the compressed brief.

Every Architect run must produce, in full uncompressed markdown: `Final_Plan.md` (the council's synthesised recommendation with roadmap, rationale, assumptions, risks, next steps) and `Premortem_Report.md` (a six-month failure scenario analysis with a severity × probability matrix and recommended safeguards) — except Route D, which produces no artifacts by design.

---

## Routing Decision

Every input must resolve to exactly one of three routes before the council starts:

```
Is the user's input a council-shaped question
(decision / plan / strategy that warrants deliberation)?
    │
    ├── NO — diagnostic / review / yes-no / list-the-options query → ROUTE D
    │
    └── YES
            │
            ├── Ambiguous or novel, or user wants to explore first?
            │     │
            │     ├── YES (--explore, or ambiguous/novel) → ROUTE C
            │     └── NO (default) → ROUTE A
```

| Route | When | Pipeline | Artifacts |
|---|---|---|---|
| **A** (default) | Problem is clear; user wants the full council | prompt-master → caveman → full council run | `Final_Plan.md` + `Premortem_Report.md` |
| **C** (`--explore`) | Problem is ambiguous or novel | scoped council explore → prompt-master → caveman → full council run | `Final_Plan.md` + `Premortem_Report.md` |
| **D** (`--diagnostic`, or auto-detected) | Non-council query: review, evaluate, list, yes/no, check, diagnose | single-pass in-line answer using the Architect's rule set | none |

**Route D is the lazy default when in doubt.** Patterns that auto-select it: "is X good enough for Y", "review the current Z", "list X" / "rank X", "what should I improve", "yes or no" / "should I", or any request naming a concrete artefact to inspect rather than a decision to deliberate. Mis-routing a diagnostic question into a full Route A council is the dominant failure mode this branch exists to prevent — Route D does not engineer or compress the prompt at all, answers directly with the Architect's epistemic standards applied, produces no artifacts, and ends with a one-line offer to escalate to Route A.

Route C differs from A only in what precedes prompt-master: a scoped council explore (Phase 1+2 only, no red-teaming) produces a **Problem Definition Document**, confirmed with the user, before Steps C2–C4 mirror Route A's craft → compress → full-council sequence exactly. Full four-step detail lives in [`skills/_shared/architect_route_c.md`](../skills/_shared/architect_route_c.md), loaded only when Route C actually fires.

---

## Pipeline Pause Conditions

The Architect pauses and surfaces to the user, on any route, if:

- The input contains sensitive personal data (PII, credentials, financial details).
- The problem scope is too large for a single session to produce meaningful artifacts — it recommends splitting into sub-problems instead.
- The user's input is a deliverable, not a prompt — caveman must not be applied to it without clarifying first.
- Any phase gate (roadmap approval, problem definition confirmation) has not been passed.

---

## When to Prefer The Architect over Morpheus or LLM-Council Alone

| Situation | Reach for |
|---|---|
| Need a precision-engineered prompt, nothing more | `morpheus` |
| Need adversarial deliberation on an already-well-framed decision | `llm-council` alone |
| Need prompt engineering + compression + full adversarial council + premortem, chained | **The Architect** |
| Question is really a review/audit/diagnostic, not a decision | The Architect Route D (or just answer directly) |

The Architect is the only Coeus skill that runs prompt-master → caveman → llm-council end to end in one invocation. Reach for it when the stakes justify the full cycle; reach for `morpheus` or `llm-council` alone when only one stage of that chain is actually needed — running the full pipeline for a question that needed two sentences is the failure mode Route D exists to prevent.

---

## Hard Rules

All 9 universal rules in [`skills/_shared/decision_skill_guardrails.md`](../skills/_shared/decision_skill_guardrails.md) apply (phase gates, both-artifacts-mandatory, uncertainty, no fabricated citations or capabilities, models-are-simulations, generic personas, surface dissent, caveman-not-applied-here). Architect-specific:

- **Caveman scope** (inherited from Morpheus): compress prompts/briefs only, never `Final_Plan.md`, `Premortem_Report.md`, or any artifact.
- **Three-route discipline**: every input routes to A, C, or D — the council never starts without a route being picked first.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [Morpheus Pipeline →](Morpheus-Pipeline.md) (the two-stage engineer/compress pipeline the Architect's Steps A1–A2 mirror)
- [LLM-Council →](LLM-Council.md) (the four-phase deliberation The Architect chains into)
- [Coeus Architecture →](Coeus-Architecture.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.1.0** (current) | not separately dated in CHANGELOG.md | ROUTE D diagnostic mode added per the SKILL.md's own "(added v1.1)" marker — auto-detects non-council queries and answers in-line without council machinery. |
| 1.0 | 2026-Jun-17 | `plugin.json` first lists `the-architect` among Coeus's initial 5 skills, chaining prompt-master → caveman → llm-council. |

Go back to the [Main README](../README.md).
