---
name: morpheus
version: 1.1.0
argument-hint: "[raw request or rough prompt] [target model]"
description: >-
  Trigger on /morpheus or /morph, "engineer this prompt", "optimise this prompt", "make this prompt better", "refine my prompt for", "compress this prompt".
  Prompt engineering and compression pipeline that chains prompt-master then caveman. Crafts a precision-engineered prompt for the target model, then compresses it for token efficiency. Caveman compresses the PROMPT only - never deliverables.
dependencies:
  - prompt-master
  - caveman
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these whenever this skill emits a judgment, recommendation, or simulated voice.


# Morpheus

A two-stage prompt engineering and compression pipeline. Takes a raw user request or
rough prompt draft and produces a precision-engineered, caveman-compressed prompt
ready to paste into any AI system.

---

## Trigger

`/morpheus` or `/morph`

Also activate if the user says: "engineer this prompt", "optimise this prompt",
"compress this prompt", "make this prompt better", "refine my prompt for [model]".

---

## Pre-Flight Checks

Run all three checks before beginning the pipeline. If any check fails, surface it
to the user and pause.

### Check 1 — Architect Escalation Detector

Does the user's request involve a complex, multi-step decision, plan, or strategy
that would benefit from adversarial red-teaming and a formal premortem?

If YES → Recommend escalating to **The Architect** (`/architect`) instead. Explain
why (scope, stakes, complexity). Ask the user to confirm before proceeding with
Morpheus anyway.

If NO → Continue to Check 2.

### Check 2 — Narrow Scope Detector

Is the user's input already a well-formed, specific prompt with a clear target model
and output format?

If YES → Skip prompt-master's full structuring phase and go directly to targeted
refinement + caveman compression. Flag to the user that the prompt is already
well-formed.

If NO → Continue to Check 3.

### Check 3 — Vague Input Detector

Is the user's input too vague to produce a useful prompt without clarification?
(e.g., "make a prompt", "write something good", no clear task or goal stated)

If YES → Ask 1–2 targeted clarifying questions before proceeding. Do not guess intent.

If NO → Begin pipeline.

---

## Step 1 — Prompt-Master (Craft)

**Objective:** Transform the raw input into a precision-engineered prompt for the
correct target model.

### Tool Routing

Identify or infer the target model from context. Apply model-specific best practices:

| Target | Key Practices |
|---|---|
| **Claude** | Use XML tags for structure, explicit thinking steps, clear persona/role framing, specify output format |
| **ChatGPT / GPT-4o** | Markdown structure, system+user split if applicable, few-shot examples work well |
| **o3 / o1** | Keep prompt concise — the model reasons internally. Don't over-specify steps. Specify output format clearly |
| **Gemini** | Clear task decomposition, explicit constraints, grounded citation requests if needed |
| **Claude Code** | CLAUDE.md-style instructions, clear scope boundaries, file/tool context, test expectations |
| **Image AI (Midjourney, DALL-E, Flux, etc.)** | Style + subject + composition + lighting + mood + negative prompts. Platform-specific syntax |

### Hard Rules for Prompt-Master

1. **Never fabricate capabilities.** Only instruct the model to use tools or features it actually has.
2. **Include output format specification.** Every engineered prompt must specify what format the output should take.
3. **Include uncertainty handling.** Every engineered prompt must instruct the model to flag uncertainty rather than confabulate.
4. **Model routing is explicit.** State the target model clearly in your output to the user.
5. **Persona framing is optional but must be grounded.** If adding a persona, it must be generic (e.g., "expert software engineer") not a named real person.

### Output of Step 1

**Auto-execution rule:** If all three pre-flight checks passed without flags AND no Pipeline Pause Condition applies, do NOT present Step 1 output as an intermediate block. Proceed directly to Step 2 and deliver only the Final Delivery Format. The engineered prompt is included in the final output under `### Engineered Prompt`.

Present Step 1 output as a standalone block **only if** a gate fired (Check 2 narrow-scope flag, Check 1 escalation recommendation, or a Pipeline Pause Condition). In that case use:

```
## Engineered Prompt (for [Target Model])

[The full engineered prompt, ready to copy]
```

---

## Step 2 — Caveman (Compress)

**Objective:** Compress the engineered prompt from Step 1 for maximum token efficiency.

### Caveman Scope Rule — CRITICAL

> **Caveman compresses the PROMPT ONLY.**
> It must NEVER be applied to:
> - The user's original deliverables or content
> - Artifacts (e.g., `Final_Plan.md`, `Premortem_Report.md`)
> - Structured data, tables, or code the user wants to preserve
> - Any output the user intends to USE as-is (not as a prompt)

If the user's input is itself a deliverable (not a prompt), do NOT compress it.
Instead, note that caveman only applies to prompts and ask the user to confirm.

### Compression Rules

Apply caveman compression to the engineered prompt:

1. **Strip articles** — remove "the", "a", "an" where meaning is preserved
2. **Remove filler phrases** — "please", "could you", "I would like you to", "make sure to", etc.
3. **Collapse verbose instructions** — replace multi-sentence instructions with terse equivalents
4. **Preserve precision** — never strip words that carry semantic weight or constraint
5. **Preserve format markers** — keep XML tags, markdown headers, and structural signals intact
6. **Preserve uncertainty instructions** — never remove "flag uncertainty" or similar guardrails
7. **Preserve output format specs** — never strip format requirements

### Auto-Disable Conditions

Skip caveman compression (return the Step 1 prompt unchanged) if:

- The prompt is already under 150 tokens (compression adds no meaningful value)
- The target model is o3/o1 (these models benefit from concision already; further compression may degrade reasoning)
- The user has explicitly said "don't compress" or "keep it verbose"

If caveman is skipped, state why.

### Output of Step 2

**Auto-execution rule:** Same as Step 1 — if all checks cleared and no pause condition applies, do NOT present Step 2 output as a standalone block. Proceed directly to Final Delivery Format.

Present Step 2 output as a standalone block only if presenting Step 1 as a standalone was warranted (i.e., a gate fired). In that case use:

```
## Compressed Prompt (caveman) — [Target Model]

[The compressed prompt, ready to copy]

Compression: ~X tokens → ~Y tokens (~Z% reduction)
```

---

## Final Delivery Format

Present both versions side-by-side for easy comparison:

```
---
## Morpheus Output

**Target model:** [Model name]
**Caveman applied:** Yes / No (reason if No)

### Engineered Prompt
[Step 1 output]

### Compressed Prompt
[Step 2 output]

Compression: ~X → ~Y tokens (~Z% reduction)
---
```

---

## Step 3 — Auto-Execute (v1.1.0)

**When all stages have successfully passed, run the compressed prompt immediately in this same conversation.**

### Auto-Execute Conditions (all must be true)

1. All three pre-flight checks passed without firing a gate.
2. No Pipeline Pause Condition triggered.
3. Step 1 (prompt-master) completed without requesting clarification.
4. Step 2 (caveman) produced a compressed prompt — OR caveman was auto-disabled, in which case execute the Step 1 engineered prompt.
5. The target model is the **current runtime** (Claude / Claude Code). If the target is a different model (ChatGPT, Gemini, Midjourney, etc.), do NOT execute — only deliver the prompt for the user to paste.

### Auto-Disable Conditions for Step 3

Skip auto-execution and deliver only the final block (Steps 1+2) if **any** apply:

- Target model is not Claude / Claude Code (engineered for external tool)
- User said "just give me the prompt", "don't run it", "deliver only", or similar
- The engineered prompt is itself a prompt-template the user wants to reuse, not an immediate task
- A pause condition fired at any earlier stage

If Step 3 is skipped, state one short reason after the Morpheus Output block.

### Execution Format

When Step 3 runs:

1. Present the Morpheus Output block (Final Delivery Format above) so the user sees both versions.
2. Add a one-line marker: `**Executing compressed prompt now…**`
3. Immediately execute the compressed prompt in the same conversation, treating its instructions as the user's effective request.
4. Deliver the result of the prompt directly below.

---

## Pipeline Pause Conditions

Pause and surface to the user if:

- The input contains sensitive personal data (PII, credentials, financial details) — flag before proceeding
- The target model appears to be one that Morpheus cannot reliably engineer prompts for — name the limitation
- The input is ambiguous about whether it is a prompt or a deliverable

---

## Absolute Hard Rules

| Rule | Details |
|---|---|
| Caveman scope | Compress prompts only, never deliverables |
| No fabricated capabilities | Don't instruct a model to use features it doesn't have |
| Uncertainty preserved | Never strip uncertainty-handling instructions from prompts |
| No named personas | Persona framing uses generic roles, not real people |
| Gate on vague input | Ask before guessing intent |

---

## Trigger Reference

| Phrase | Action |
|---|---|
| `/morpheus`, `/morph` | Full pipeline |
| "engineer this prompt" | Full pipeline |
| "optimise my prompt for [model]" | Full pipeline, route to specified model |
| "compress this prompt" | Step 2 only (skip Step 1, apply caveman to provided prompt) |
| "make this prompt better" | Full pipeline |

---

## Epistemic Standards

1. Flag uncertainty when inferring the target model from context.
2. Never claim a compression ratio is exact — use "approximately" or "~".
3. If the engineered prompt contains claims the user should verify, surface them.
