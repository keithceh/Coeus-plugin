# Decision-Skill Guardrails (shared)

> Single source of truth for the cross-cutting behavioural guardrails that apply to every Coeus decision/deliberation skill (`llm-council`, `ep-council`, `the-architect`, and any future council variant). Skill-specific guardrails (e.g. EP-Council's T0 trap, llm-council's Phase 5 emoji rule) stay in the skill's own SKILL.md.

---

## Universal hard rules

These rules apply to every council-shaped skill in Coeus. Each rule is non-negotiable.

| # | Rule | Applies when |
|---|---|---|
| 1 | **Never skip a phase gate.** Wait for explicit user approval. Neutral or absent responses do NOT count as approval. | Any phase that has a gate (roadmap approval, problem-definition confirmation, Strategy Brief lock, Phase-5 opt-in). |
| 2 | **Both mandatory artifacts must ship.** A council run is not complete without both artifacts the skill specifies (e.g. `Final_Plan.md` + `Premortem_Report.md` for llm-council; `EP_Decision_Plan.md` + `EP_Premortem_Report.md` for ep-council). | End of every full council run. |
| 3 | **Flag all uncertainty.** Distinguish known facts from inferences from speculation. Use the marker conventions from [`uncertainty_rules.md`](uncertainty_rules.md). | Every output. |
| 4 | **Never fabricate citations.** When a simulated model voice needs to cite evidence, use hedged language ("Research in this area generally suggests…") rather than inventing paper titles, authors, or numbers. | Any simulated voice that would otherwise invent a reference. |
| 5 | **Never fabricate capabilities.** Don't instruct any model to use tools or features it does not have. | Engineered prompts; any instruction to a downstream model. |
| 6 | **Models are simulations, not impersonations.** The simulated voices represent epistemic styles, not accurate representations of the named products' real behaviour. | Any session that names specific models (ChatGPT, Grok, Claude, Perplexity, DeepSeek, Le Chat, etc.). |
| 7 | **Persona framing uses generic roles only.** Never name a real person as the persona — generic ("expert software engineer") only. | Any prompt that includes a persona or role assignment. |
| 8 | **Surface minority positions.** Dissent is valuable. Do not paper over disagreement to produce a tidy-looking output. | Phase 3 / red-team / synthesis steps. |
| 9 | **Caveman is not applied here.** Council/decision skills do not compress their own outputs. Compression is the job of Morpheus or The Architect when they chain in. | Any council output (the brief is compressible; the artifact is not). |

---

## How to reference

A decision skill imports these rules by adding a single line near the top of its SKILL.md:

```markdown
> Decision-skill guardrails: see [`../_shared/decision_skill_guardrails.md`](../_shared/decision_skill_guardrails.md). All 9 universal hard rules apply to this skill.
```

The skill's own `## Behavioural Guardrails` section then only needs to list its **skill-specific** additions (e.g. EP-Council's T0 Strategic Drift stop, llm-council's Phase-5 emoji-substitution rule).
