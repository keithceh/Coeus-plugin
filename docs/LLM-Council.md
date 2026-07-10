# LLM-Council

> Multi-LLM adversarial deliberation engine. Seven simulated frontier models stress-test any decision, plan, or strategy across four mandatory phases — Socratic clarification, gated roadmap, tri-team red-team, and a 6-month failure premortem — then optionally deliver a single production-ready consolidated Word document.

**Version:** v1.2 (current) | **Triggers:** `/coeus:llm-council` · `/council` · `"Jedi"` · `"May 4th"` · `"stress-test this plan"` · `"red team this"` · `"premortem"`

---

## What It Does

LLM-Council replaces single-pass, single-model reasoning with a structured, phase-gated multi-model debate. It simulates seven distinct frontier AI voices — each with a documented epistemic style and failure mode — as an adversarial council that hardens any plan across two-to-three red-team rounds and a 6-month premortem before producing the final artifacts.

It is **not a chatbot**. It is a phase-gated engine. Phases cannot be skipped. The strategic roadmap cannot proceed to red-teaming without explicit user approval. The two artifacts (`Final_Plan.md` + `Premortem_Report.md`) are mandatory. The optional Phase 5 production document is opt-in and emoji-free by design.

LLM-Council is the **general-purpose** decision engine in Coeus. [EP-Council](EP-Council.md) is the domain-specific variant for upstream E&P opportunities — same phase-gate philosophy, different jury.

---

## Installation

LLM-Council is bundled in `coeus.plugin`. No separate install.

**Recommended:**
1. Download `coeus.plugin` from [**Releases**](https://github.com/keithceh/Coeus/releases)
2. Claude Desktop / Cowork → **Settings → Capabilities → Customize → Add Plugin**
3. Select `coeus.plugin`

**Build from source:**
```bash
git clone https://github.com/keithceh/Coeus.git
cd Coeus
python scripts/build-plugin.py     # cross-platform; UTF-8-flagged for Cowork
```

Then install `dist/coeus.plugin` via Add Plugin as above.

---

## Triggers

| Trigger | Notes |
|---------|-------|
| `/coeus:llm-council` | Primary slash command |
| `/council` | Short slash form (in-skill alias) |
| `"Jedi"` / `"May 4th"` | Easter-egg natural-language triggers |
| `"run the council"` | Plain English |
| `"stress-test this plan"` | Plan-first entry |
| `"red team this"` | Red-team focus |
| `"premortem this"` | Failure-mode focus |
| `"multi-model analysis"` | Multi-perspective framing |
| `"get all the AIs to weigh in"` | Layperson phrasing |
| `"simulate expert debate"` | Adversarial debate framing |
| `"adversarial review"` | Review framing |

**Auto-trigger:** Any consequential decision, plan, strategy, or technical question where depth is preferred over speed. LLM-Council leans toward firing rather than waiting for explicit invocation.

When to **not** trigger: trivial lookups, single-fact questions, code-only refactors, anything a one-pass answer handles well. Use [Morpheus](../skills/morpheus/SKILL.md) for prompt engineering and [The Architect](../skills/the-architect/SKILL.md) for the full prompt-engineering-plus-council pipeline.

---

## The Pipeline

```
[User question / decision / plan]
           │
     Phase 1: Socratic Clarification
     ─ ≤3 targeted questions to refine the problem statement
     ─ Surface ambiguities, hidden assumptions, scope edges
     ─ Short-circuit if the input is already unambiguous
           │
     Phase 2: Strategic Roadmap + Gated Approval
     ─ 7 models each propose a high-level approach
     ─ Synthesis: primary recommendation, 3-5 action steps,
       key assumptions, top 3 risks
     ─ ★ EXPLICIT USER APPROVAL REQUIRED ★
           │
     Phase 3: Tri-Team Round-Robin Red-Team (2-3 rounds)
     ─ Blue defends · Red attacks · Green proposes alternatives
     ─ Factions sized 3/2/2 (7 models don't split evenly);
       models randomly re-assigned every round
       (no model holds the same role in consecutive rounds)
     ─ Per-round synthesis incorporates strongest arguments
     ─ Convergence check after each round
           │
     Phase 4: 6-Month Failure Premortem Engine
     ─ Each model proposes 2-3 distinct failure scenarios
     ─ Scenarios clustered by theme
     ─ Severity × Probability matrix; top 3 clusters flagged
     ─ Pre-mortem mitigations baked back into the plan
           │
  [Final_Plan.md + Premortem_Report.md]
           │
     Phase 5: Production-Ready Document (OPT-IN)
     ─ Single yes/no prompt to the user
     ─ Consolidates all artifacts into one .docx
     ─ Every emoji replaced with plain-language substitute
     ─ 10-item failable QA checklist before delivery
           │
  [<topic>_Final_Production_v1.docx]
```

---

## The Seven Simulated Models

Each model plays a distinct epistemic role. Claude simulates all seven voices in turn — they are *simulations of epistemic styles*, loosely grounded in each vendor's own published model documentation as of mid-2026, not impersonations of real products.

| # | Model | Epistemic Role |
|---|-------|---------------|
| 1 | **ChatGPT (GPT-5.5)** | Pragmatic synthesiser — actionable clarity, structured outputs, moderate hedging |
| 2 | **Grok (Grok 4 Heavy)** | Contrarian provocateur — challenges consensus, surfaces uncomfortable truths, high confidence |
| 3 | **Claude (Claude Fable 5)** | Careful reasoner — ethics-aware, uncertainty-flagging, multi-step logical decomposition |
| 4 | **Perplexity (Perplexity Pro)** | Citation-oriented researcher — grounds claims in evidence, flags unsupported assertions |
| 5 | **DeepSeek (DeepSeek-V4-Pro)** | Systems thinker — second-order effects, game-theoretic framing, long-horizon analysis |
| 6 | **Le Chat (Mistral Medium 3.5)** | Nuanced European perspective — regulatory and societal context, human-centred design |
| 7 | **Gemini (Gemini Pro)** | Structural verifier — deconstruct/verify/correct loop, explicit multi-constraint structuring, calibrated risk judgment |

See [Council Members →](LLM-Council-Members.md) for the full profile of each voice (lens, primary question, characteristic failure mode, when to listen, when to discount).

---

## Tri-Team Faction Allocation

Phase 3 splits the seven models across three factions, sized **3/2/2** (seven doesn't divide evenly by three), **re-randomised every round** — including which faction carries the extra seat.

| Round | Blue Team (Defenders) | Red Team (Attackers) | Green Team (Innovators) |
|-------|---------------------|---------------------|------------------------|
| 1 | 2 or 3 models | 2 or 3 models | 2 or 3 models |
| 2 | rotated | rotated | rotated |
| 3 | rotated | rotated | rotated |

**Rules:**
- Faction sizes are 3/2/2 every round; which faction holds the extra seat rotates.
- No model holds the same faction in consecutive rounds.
- Assignments are stated at the top of every round so the user can see who is in which role.
- Minimum 2 rounds; maximum 3 unless the user explicitly requests more.
- Convergence check after each round — if factions converge, proceed to Phase 4; if not, run another round.

---

## Phase Gates

LLM-Council has **two mandatory gates** and **one optional gate**. Gates cannot be bypassed by the assistant.

| Gate | Where | What | Override |
|------|-------|------|----------|
| **Roadmap approval** | End of Phase 2 | User must explicitly approve the Strategic Roadmap before red-teaming begins. Neutral responses do not count as approval. | None — the assistant must wait or iterate. |
| **Convergence** | End of each Phase 3 round | Either factions converge → proceed to Phase 4, or another round runs. User may call a stop. | User stop. |
| **Production .docx** | End of Phase 4 | User must answer **yes** to a single offer prompt before Phase 5 generates the consolidated `.docx`. | Default: no .docx; the two markdown artifacts are the final delivery. |

---

## Output Artifacts

Both delivered as standalone code-fenced Markdown documents at the end of every council run.

**`Final_Plan.md`**
- Executive summary (2–3 sentences)
- Approved Strategic Roadmap (Phase 2 output with Phase 3 patches folded in)
- Key decisions and rationale (with reference to the debate)
- Assumptions the plan rests on
- Top 3–5 risks with brief mitigations
- Concrete, time-bound next steps

**`Premortem_Report.md`**
- Failure scenarios grouped by cluster (resource, market, internal, technical, regulatory, key-person, etc.)
- Severity × Probability matrix per cluster
- Top 3 highest-risk clusters
- Recommended safeguards embedded in the plan

**Optional `<topic>_Final_Production_v1.docx` (Phase 5)**
- All 12 consolidated sections (cover page → glossary)
- Emoji-free (canonical substitution table applied)
- 10-item pre-delivery QA passed
- Generated via `python-docx` or `pandoc`; markdown-only fallback if neither is in the runtime

See [Step-by-Step Walkthrough →](LLM-Council-Walkthrough.md) for what each artifact looks like in a real session.

---

## Mid-Session Commands

| Command | What happens |
|---------|-------------|
| `Proceed` / `Go ahead` / `Yes` | Pass the Phase 2 gate; red-teaming begins |
| `Run another round` | Add one more Phase 3 round (overrides convergence) |
| `Stop here` | Close Phase 3 early and proceed to Phase 4 |
| `Yes, generate the .docx` | Pass the Phase 5 gate; produce the consolidated Word document |
| `No, the markdown is enough` | Close the session after Phase 4 — the two .md artifacts are the final delivery |
| `Don't compress` | Disable any chained caveman compression (relevant only when invoked via Morpheus / The Architect) |

---

## Mandatory Flags & Guardrails

| Guardrail | Meaning |
|-----------|---------|
| **Phase gate enforcement** | No red-teaming without an explicit "approve" on the roadmap. No .docx without an explicit "yes" on the Phase 5 offer. |
| **Uncertainty flagging** | Every load-bearing claim must be tagged as known fact, reasonable inference, or speculation. Phrases like "I'm not certain, but…", "You should verify this…" are required. |
| **No fabricated citations** | When the Perplexity-style voice needs evidence, it must hedge ("Research generally suggests…") rather than invent paper titles. |
| **Models are simulations** | The seven voices represent distinct epistemic styles; they are NOT accurate impersonations of those products' real behaviour. The session should be read as a structured debate, not as ground-truth multi-vendor consensus. |
| **No caveman here** | LLM-Council does not compress its own outputs. Compression is handled by [Morpheus](../skills/morpheus/SKILL.md) or [The Architect](../skills/the-architect/SKILL.md) if they chain into the council. |
| **Both artifacts mandatory** | A run is not complete without `Final_Plan.md` and `Premortem_Report.md`. |
| **Phase 5 is opt-in only** | Never auto-generate the production .docx. Ask exactly once after Phase 4. |
| **Zero emojis in the .docx** | Every emoji replaced via the canonical substitution table before generation. A final regex sweep blocks delivery if any emoji slips through. |
| **Never ship .docx with failed QA** | The 10-item pre-delivery checklist must pass. A production document with an unresolved bug is worse than no document. |
| **Surface dissent** | Minority positions are documented even after consensus emerges. Intellectual honesty beats tidy output. |

---

## When To Use LLM-Council vs The Architect vs EP-Council

| Use… | When |
|------|------|
| **LLM-Council** | General-purpose decision, plan, or strategy across any domain. You already have a clear problem statement. |
| **[The Architect](../skills/the-architect/SKILL.md)** | Same, **plus** you want the input first run through Morpheus (precision prompt engineering + caveman compression). Use when the framing of the question is itself uncertain. |
| **[EP-Council](EP-Council.md)** | The decision is an upstream E&P opportunity (block, well, acquisition, farm-in, JV, divestment). EP-Council uses 9 supermajors and the T0–T12 trap screen instead of the 7-voice council. |

---

## Related Pages

- [Council Members → seven-voice profiles](LLM-Council-Members.md)
- [Step-by-Step Session Walkthrough →](LLM-Council-Walkthrough.md)
- [EP-Council main page →](EP-Council.md) (the E&P-specific sibling)
- [Coeus README →](../README.md)

---

## Version History

| Version | Key Changes |
|---------|------------|
| **v1.2** (current, v3.11.0+) | **Seventh voice added — Gemini (Gemini Pro), "Structural Verifier".** All six existing voices refreshed against each vendor's July-2026 model documentation (ChatGPT → GPT-5.5, Grok → Grok 4 Heavy, Claude → Claude Fable 5, Perplexity → Perplexity Pro, DeepSeek → DeepSeek-V4-Pro, Le Chat → Mistral Medium 3.5) with updated lenses and characteristic failure modes. Phase 3 tri-team faction sizing changed from a fixed 2/2/2 split to a rotating 3/2/2 split (seven models don't divide evenly across three factions). |
| v1.1 (v3.6.0+) | **Phase 5 added** — opt-in consolidated production-ready `.docx` after Phase 4. Canonical emoji substitution table (every emoji used in council output mapped to a plain-language substitute). 10-item failable pre-delivery QA. Three new behavioural guardrails (Phase 5 opt-in; never issue with failed QA; never ship emojis in the .docx). |
| v1.0 | Initial release. Four phases (Socratic → Roadmap → Tri-Team Red-Team → Premortem). Six-model simulation. Mandatory artifacts `Final_Plan.md` + `Premortem_Report.md`. |

Go back to the [Main README](../README.md).
