---
name: llm-council
version: 1.2.0
argument-hint: "[decision, plan, or question to stress-test]"
description: >-
  Trigger on: /council, "Jedi", "May 4th", "run the council", "stress-test this plan", "red team this", "premortem", "multi-model analysis", "i am torn between", "weigh the options", or any second-opinion request before committing to a decision.
  Multi-LLM consensus, tri-team adversarial red-teaming, and 6-month failure premortem engine. Use whenever the user wants a rigorous, deeply reasoned answer to a consequential decision, plan, or technical question. Lean toward triggering it.
dependencies: []
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these whenever this skill emits a judgment, recommendation, or simulated voice.


# LLM-Council

A structured 4-phase multi-model deliberation pipeline that simulates expert debate
across seven distinct AI perspectives, applies adversarial red-teaming, and stress-tests
plans against plausible 6-month failure scenarios.

---

## The Seven Simulated Models

Each model plays a distinct epistemic role. Claude simulates all seven voices in turn.

| Model | Voice / Personality |
|---|---|
| **ChatGPT (GPT-5.5)** | Pragmatic synthesiser. Favours actionable clarity, structured outputs, moderate hedging |
| **Grok (Grok 4 Heavy)** | Contrarian provocateur. Challenges consensus, surfaces uncomfortable truths, high epistemic confidence |
| **Claude (Claude Fable 5)** | Careful reasoner. Strong on ethics, uncertainty flagging, and multi-step logical decomposition |
| **Perplexity (Perplexity Pro)** | Citation-oriented researcher. Grounds claims in evidence, flags unsupported assertions |
| **DeepSeek (DeepSeek-V4-Pro)** | Systems thinker. Favours second-order effects, game-theoretic framing, long-horizon analysis |
| **Le Chat (Mistral Medium 3.5)** | Nuanced European perspective. Regulatory and societal context, human-centred design |
| **Gemini (Gemini Pro)** | Structural verifier. Deconstructs and self-corrects before answering, organises multi-constraint problems explicitly, calibrates risk judgment between paranoid and reckless |

---

## Phase 1 — Socratic Clarification

**Entry condition:** User has triggered the skill with a question, plan, or decision.

**Objective:** Ensure the council is deliberating on a well-formed problem before committing resources.

**Steps:**
1. Identify the core decision or question being asked.
2. Surface any ambiguities, scope uncertainties, or hidden assumptions.
3. Ask the user up to 3 targeted clarifying questions (not more).
4. Confirm the refined problem statement before proceeding.

**Exit condition:** User approves the refined problem statement, or explicitly says "proceed as-is."

**Output:** A single clear problem statement used as the shared input for Phase 2.

---

## Phase 2 — Strategic Roadmap + Gated Approval

**Entry condition:** Approved problem statement from Phase 1.

**Objective:** Produce a concrete strategic roadmap that the user can approve before red-teaming begins.

**Steps:**
1. Each of the seven models independently proposes a high-level approach (1–2 paragraphs each).
2. Claude synthesises the six perspectives into a unified **Strategic Roadmap** with:
   - Primary recommendation
   - 3–5 key action steps
   - Key assumptions underlying the roadmap
   - Top 3 risks identified at this stage
3. Present the roadmap to the user.
4. **Gate:** User must explicitly approve the roadmap before Phase 3 begins. If the user requests changes, iterate and re-present.

**Exit condition:** User approves the Strategic Roadmap.

**Output:** Approved `Strategic Roadmap` document (inline, not a file).

---

## Phase 3 — Tri-Team Adversarial Red-Teaming

**Entry condition:** Approved Strategic Roadmap from Phase 2.

**Objective:** Stress-test the roadmap through structured adversarial debate across three factions.

### Team Composition

Three factions. Seven models don't split evenly across three factions, so sizes are **3/2/2**, rotating which faction carries the extra seat each round. **Models are randomly assigned to factions each round** — no model holds the same faction role in back-to-back rounds.

| Faction | Role |
|---|---|
| **Blue Team** | Defenders — argue for the plan, strengthen it, patch weaknesses |
| **Red Team** | Attackers — find flaws, failure modes, and contradictions |
| **Green Team** | Innovators — propose alternatives, pivots, and enhancements |

### Randomisation Rule

Before each round, randomly assign the seven models to the three factions (sizes 3/2/2, rotating which faction gets the extra seat). Explicitly state the assignment at the top of each round output so the user can see which model is in which role. No model may occupy the same faction position as the previous round.

### Round Structure (minimum 2 rounds, maximum 3 unless user requests more)

**Round N:**
1. **Red Team attacks** the current plan / previous round's synthesis.
2. **Green Team** proposes improvements or alternatives.
3. **Blue Team** defends and patches the plan in light of Red and Green input.
4. **Synthesis:** Claude produces a revised plan incorporating the strongest arguments from all three factions.
5. **Convergence check:** Are the factions converging? If yes, proceed to Phase 4. If not, run another round.

**Exit condition:** Convergence across factions, or user calls a stop.

**Output:** Final revised plan (inline synthesis document).

---

## Phase 4 — 6-Month Failure Premortem Engine

**Entry condition:** Converged plan from Phase 3.

**Objective:** Assume the plan has *already failed* six months from now. Work backwards to identify what went wrong and why.

**Steps:**
1. **Failure scenario generation:** Each of the seven models independently proposes 2–3 distinct failure scenarios that could plausibly occur within 6 months. Scenarios must be specific (not generic "execution risk") and grounded in the plan's known assumptions and context.
2. **Failure clustering:** Group scenarios by theme (e.g., resource constraints, market shifts, internal misalignment, technical failure, regulatory change, key-person risk).
3. **Severity × Probability matrix:** Rate each cluster on a 1–5 scale for likelihood and impact. Flag the top 3 highest-risk clusters.
4. **Pre-mortem mitigations:** For each top-risk cluster, propose 1–2 concrete preventive actions that can be built into the plan now.
5. **Assemble artifacts:** Produce `Final_Plan.md` and `Premortem_Report.md`.

---

## Mandatory Artifacts

Both artifacts must be produced at the end of every council run. They are delivered as formatted markdown documents.

### `Final_Plan.md`

```markdown
# Final Plan — [Topic / Decision Title]

**Date:** YYYY-MM-DD
**Council run triggered by:** [trigger phrase or user message]

## Executive Summary
[2–3 sentence summary of the recommendation]

## Strategic Roadmap
[Approved roadmap from Phase 2, updated with Phase 3 synthesis]

## Key Decisions and Rationale
[What was decided and why, with reference to the debate]

## Assumptions
[List of key assumptions the plan rests on]

## Top Risks
[3–5 risks with brief mitigations]

## Next Steps
[Concrete, time-bound action items]
```

### `Premortem_Report.md`

```markdown
# Premortem Report — [Topic / Decision Title]

**Date:** YYYY-MM-DD
**Assumed failure horizon:** 6 months from plan adoption

## Failure Scenarios

### [Cluster Name]
- **Scenarios:** [list]
- **Likelihood (1–5):** X
- **Impact (1–5):** X
- **Preventive actions:** [list]

[Repeat for each cluster]

## Top 3 Risk Clusters

| Rank | Cluster | Likelihood | Impact | Risk Score |
|---|---|---|---|---|
| 1 | ... | X | X | X×X |
| 2 | ... | X | X | X×X |
| 3 | ... | X | X | X×X |

## Recommended Safeguards
[Concrete actions to embed in the plan to address the top risks]
```

---

## Phase 5 — Production-Ready Document (Optional, User-Gated)

**Entry condition:** Both `Final_Plan.md` and `Premortem_Report.md` have been delivered.

**Phase 5 is opt-in.** Ask the user **exactly once** after Phase 4 lands:
> *"Final_Plan.md and Premortem_Report.md are delivered. Do you want a single production-ready Word document (.docx) that consolidates both artifacts, the Strategic Roadmap, and the red-team synthesis — emoji-free and distribution-ready? (yes / no)"*

**If no →** stop. The two markdown artifacts are the final delivery.
**If yes →** load the full Phase-5 recipe from [`../_shared/phase5_docx_recipe.md`](../_shared/phase5_docx_recipe.md) and execute Steps 5.2–5.6. The recipe contains: consolidation section order (12 sections), the canonical emoji-substitution table, the 10-item pre-delivery QA checklist, the python-docx → pandoc → markdown-fallback generator preference, and the delivery format.

**Hard rule (also enforced in the recipe):** never issue the .docx if any QA check failed. A production document with an unresolved bug is worse than no document.

---

## Behavioural Guardrails

**Universal:** all 9 rules in [`../_shared/decision_skill_guardrails.md`](../_shared/decision_skill_guardrails.md) apply.

**Skill-specific (Phase 5 .docx):**
- **Phase 5 is opt-in only.** Never auto-generate the production .docx. Always offer it after Phase 4 and wait for an explicit "yes".
- **Never issue the .docx if any QA check failed.** Surface the failure instead. A production document with an unresolved bug is worse than no document.
- **No emojis in the production .docx — ever.** Substitute every emoji per the canonical table in the shared Phase-5 recipe and re-sweep before delivery.
