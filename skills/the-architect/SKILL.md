---
name: the-architect
version: 1.1.0
argument-hint: "[decision or plan to stress-test] [--explore | --diagnostic]"
description: >
  Trigger on /architect or /archi, "full pipeline", "architect this",
  "stress-test and plan this properly",
  "run the full council with prompt engineering".
  Use when the user faces a high-stakes decision or complex plan that benefits
  from precision prompt engineering AND adversarial multi-model deliberation.

  Adaptive combo skill that chains prompt-master, caveman, and llm-council into
  a single end-to-end pipeline. Three routes:
  - ROUTE A (default): prompt-master → caveman → council (full run).
  - ROUTE C (`--explore`): council-explore → prompt-master → caveman → council.
  - ROUTE D (`--diagnostic` or auto-detected): skip the council; single-pass
    in-line answer using the Architect's rule set. For non-council queries:
    yes/no diagnostics, "review the repo", "evaluate X", "list improvements".
    No Final_Plan/Premortem in diagnostic mode.

  Final artifacts (A/C only): Final_Plan.md + Premortem_Report.md. Caveman is
  NEVER applied to artifacts — only to prompts.
dependencies:
  - prompt-master
  - caveman
  - llm-council
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these whenever this skill emits a judgment, recommendation, or simulated voice.


# The Architect

The Architect is an adaptive combo skill that chains three sub-skills — prompt-master,
caveman, and llm-council — into a single orchestrated pipeline. It is the
highest-intensity tool in the Coeus suite and should be used when the stakes justify
the full deliberation cycle.

---

## Trigger

`/architect` or `/archi`

Optional flag: `--explore` (activates ROUTE C)

Also activate if the user says: "full pipeline", "architect this", "run the full
council with prompt engineering", "stress-test and plan this properly".

---

## Routing Decision

```
Is the user's input a council-shaped question
(decision / plan / strategy that warrants deliberation)?
    │
    ├── NO — it's a diagnostic / review / yes-no / list-the-options query → ROUTE D
    │
    └── YES
            │
            ├── Does the user want to explore the problem space first?
            │     │
            │     ├── YES (--explore, or ambiguous/novel) → ROUTE C
            │     │
            │     └── NO (default) → ROUTE A
```

| Route | When to use | Pipeline | Artifacts |
|---|---|---|---|
| **ROUTE A** (default) | Problem is clear; user wants the full council | prompt-master → caveman → council full run | `Final_Plan.md` + `Premortem_Report.md` |
| **ROUTE C** (`--explore`) | Problem is ambiguous or novel | council explore → prompt-master → caveman → council full run | `Final_Plan.md` + `Premortem_Report.md` |
| **ROUTE D** (`--diagnostic`, or auto-detected) | Non-council query: review, evaluate, list, yes/no, check, diagnose | Single-pass in-line answer using Architect's rule set | None (in-line answer only) |

### Auto-detection of ROUTE D

If the user's input matches any of these patterns, **default to ROUTE D** and ask one clarifier only if the user explicitly asks for the full council:

- "is X good enough for Y" / "check if X" / "does X cover Y"
- "review the current Z" / "evaluate Z" / "audit Z"
- "list X" / "table out X" / "rank X"
- "what should I improve" / "what's missing" / "what would you change"
- "yes or no" / "is this right" / "should I"
- Any request that names a concrete artefact to inspect (a repo, a file, a config) rather than a decision to deliberate

If in doubt: **ROUTE D is the lazy default.** Full ROUTE A is for when the user wants stress-testing, not when they want a diagnostic. Mis-routing to ROUTE A produces a 4-phase council for a question that needed two sentences — that's the dominant failure mode this branch is here to prevent.

---

## ROUTE D — Diagnostic Mode (added v1.1)

A scoped, single-pass answer using the Architect's epistemic standards and rule set, with **none of the council machinery**.

### Pipeline

1. **Read the user's input as-is.** Do NOT engineer the prompt (skip prompt-master) and do NOT compress (skip caveman). The user is asking a direct question; treat it as one.
2. **Answer in-line.** Use a structured format appropriate to the question — usually a table or a ranked list. Default to the most compact form that answers the question completely.
3. **Apply the Architect's hard rules** to the answer (uncertainty preserved, no fabricated capabilities, hedged language for unsupported empirical claims, minority positions surfaced).
4. **No artifacts.** Diagnostic mode does NOT produce `Final_Plan.md` or `Premortem_Report.md`. If the user wants those, they have asked for the wrong route — offer to escalate to ROUTE A in one line at the end.
5. **End with a one-line escalation offer:** *"Want me to escalate this to a full ROUTE-A council run?"*

### When NOT to use ROUTE D

- The user's input is genuinely a decision / plan / strategy they want stress-tested.
- The user explicitly says "full pipeline", "ROUTE A", "stress-test", "red-team", "premortem", or asks for the council.
- The artifacts (`Final_Plan.md` / `Premortem_Report.md`) are explicitly requested.

In those cases, fall through to ROUTE A or C.

---

---

## ROUTE A — Default Pipeline

### Step A1 — Prompt-Master (Craft)

Apply the full prompt-master process to the user's input:

1. Identify the target context (what will the final council prompt be used for).
2. Structure the user's request into a precision-engineered council brief.
3. Include: problem statement, key constraints, desired output format, success criteria.
4. Apply model routing: the engineered output is destined for the **LLM-council** phase.

**Hard rules (inherited from Morpheus):**
- Never fabricate capabilities
- Include output format specification
- Include uncertainty handling instruction
- Persona framing uses generic roles only

**Output:** Engineered council brief (clearly labelled block).

---

### Step A2 — Caveman (Compress)

Apply caveman to the engineered council brief from Step A1.

> **CRITICAL SCOPE RULE: Caveman is applied to the council BRIEF (prompt), NOT to any artifact, deliverable, or structured output produced by the council.**

**Compression rules (inherited from Morpheus):**
1. Strip articles where meaning is preserved
2. Remove filler phrases
3. Collapse verbose instructions
4. Preserve precision, format markers, uncertainty instructions, output format specs

**Auto-disable if:**
- Brief is already under 150 tokens
- User says "don't compress"

**Output:** Compressed council brief + compression ratio.

---

### Step A3 — LLM-Council (Full Run)

Feed the compressed council brief into the full 4-phase council pipeline:

- **Phase 1:** Socratic clarification (using the engineered brief as the starting point — clarification questions may be minimal or skipped if the brief is already precise)
- **Phase 2:** Strategic roadmap + gated approval
- **Phase 3:** Tri-team adversarial red-teaming (Blue / Red / Green factions, randomised each round)
- **Phase 4:** 6-month failure premortem engine

**Gate:** User must approve the Strategic Roadmap (Phase 2 output) before Phase 3 begins.

**Mandatory artifacts:** `Final_Plan.md` + `Premortem_Report.md` (see artifact formats in llm-council SKILL.md).

---

## ROUTE C — Deep Explore Pipeline

Use when the problem is ambiguous, novel, or the user wants the council to help
define and scope the problem before any prompt engineering occurs.

**Pipeline (4 steps C1–C4):** load [`../_shared/architect_route_c.md`](../_shared/architect_route_c.md). It contains: Step C1 (scoped council explore — Phase 1+2 only, produces Problem Definition Document), Step C2 (prompt-master craft on the confirmed definition), Step C3 (caveman compression), Step C4 (full 4-phase council on the compressed brief). Mandatory artifacts unchanged: `Final_Plan.md` + `Premortem_Report.md`.

## Pipeline Pause Conditions

Pause and surface to the user if:

- The input contains sensitive personal data (PII, credentials, financial details)
- The problem scope is so large that a single session cannot produce meaningful artifacts — recommend splitting into sub-problems
- The user's input is a deliverable, not a prompt — clarify before applying caveman
- Any phase gate (roadmap approval, problem definition confirmation) is not passed

---

## Absolute Hard Rules

**Universal:** all 9 rules in [`../_shared/decision_skill_guardrails.md`](../_shared/decision_skill_guardrails.md) apply (covers phase gates, both-artifacts-mandatory, uncertainty, no fabricated citations or capabilities, models-are-simulations, generic personas, surface dissent, caveman-not-applied-here).

**Skill-specific (Architect-only):**
- **Caveman scope (inherited from Morpheus):** compress prompts/briefs only. NEVER apply to `Final_Plan.md`, `Premortem_Report.md`, or any artifact.
- **Three-route discipline:** every input must route to ROUTE A, C, or D — never start the council without picking one.

---

## Final Deliverables

At the end of every Architect run (either route), the following must be produced:

1. **`Final_Plan.md`** — The council's synthesised recommendation with roadmap, rationale, assumptions, risks, and next steps.
2. **`Premortem_Report.md`** — 6-month failure scenario analysis with severity × probability matrix and recommended safeguards.

These artifacts are never compressed by caveman. They are delivered in full, structured markdown.

---

## Trigger Reference

| Phrase | Route |
|---|---|
| `/architect` (no qualifier) | **Auto-detect** — diagnostic patterns → ROUTE D, council-shaped → ROUTE A |
| `/archi` (no qualifier) | Same auto-detect |
| `/architect --explore` | ROUTE C |
| `/archi --explore` | ROUTE C |
| `/architect --diagnostic` | ROUTE D (forced) |
| `/archi --diagnostic` | ROUTE D (forced) |
| "full pipeline" | ROUTE A (forced) |
| "stress-test and plan this properly" | ROUTE A (forced) |
| "architect this with exploration" | ROUTE C |
| "is X good enough", "review the repo", "evaluate / list / audit" | ROUTE D (auto) |

---

## Epistemic Standards

The Architect inherits the full epistemic standards of both Morpheus and LLM-council:

1. Distinguish between known facts, reasonable inferences, and speculation at every step.
2. Flag when a claim depends on an unvalidated assumption.
3. Surface minority positions even after consensus.
4. Never present uncertain claims as facts.
5. Flag compression ratios as approximate.
6. Simulated model voices must use hedged language for unsupported empirical claims.
