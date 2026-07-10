# Coeus Architecture

> The structural ruleset that governs every skill in Coeus. A three-tier model
> (nano-skill / cluster / router), a hard 3,000-token cap per `SKILL.md`, a
> shared-rules convention under `skills/_shared/`, and a single canonical
> registry. Born out of a full Architect council run on 2026-06-24.

**Version:** v1.0 (adopted in v3.8.0) | **Triggers:** `/coeus:router` · `/coeus-router` · `"which coeus skill"` · `"route this"` · `"coeus help me decide"`

---

## What It Is

Coeus Architecture is **not a skill that does work** — it is the framework all
the work-doing skills live inside. It exists because the alternative
(monolithic super-skill, or unbounded fragmentation) both failed in
council-simulated 6-month premortems. The Architect run's full reasoning lives
in `Architect_Final_Plan_Skill_Architecture.md`.

The architecture ships as four pieces:

1. **`docs/SKILL_ARCHITECTURE.md`** — the spec (rules, tiers, decision table).
2. **`skills/_shared/`** — shared convention files (`uncertainty_rules.md`, `output_formats.md`, `SKILL_REGISTRY.md`).
3. **`skills/coeus-router/`** — the only Tier-3 meta-skill in Coeus, demonstrating routing-without-logic.
4. **This document** — user-facing reference.

Coeus Architecture is **load-equivalent across Claude Chat, Cowork, and Claude Code**. Every artifact uses the standard Claude-Code plugin spec layout, so Tier-3 routing and `_shared/` references resolve the same way on every surface.

---

## Triggers

| Trigger | Notes |
|---------|-------|
| `/coeus:router` | Primary slash command for the Tier-3 router |
| `/coeus-router` | Alias |
| `"which coeus skill"` | Plain English |
| `"route this"` | Route-first framing |
| `"pick the right coeus skill"` | Disambiguation framing |
| `"what coeus skill should I use"` | Beginner framing |

When to **not** trigger the router: when the user has already named a specific Coeus skill, or when the request is plainly outside Coeus's scope. The router refuses to invent skills that are not in the registry.

---

## The Three Tiers and Two Families

**Tiers** describe a skill's *shape* (nano, cluster, router). **Families**
describe a skill's *intent* (decision, tools, meta). Every skill in Coeus
has both.

```
Tier 1 — Nano-skill                 │ Family: decision
  └─ One output type or domain      │   llm-council, ep-council, morpheus*,
  └─ ≤ 3,000 tokens                 │   the-architect*, prompt-master,
                                    │   caveman, plugin-creator
Tier 2 — Cluster skill              │
  └─ 2-4 related skills merged      │ Family: tools
  └─ Reads _shared/ for common rules│   ooxml-repair, ooxml-fields,
  └─ Hard cap: 3,000 tokens         │   docx-inventory, project-lifecycle*
                                    │
Tier 3 — Meta-skill (router)        │ Family: meta
  └─ Routing only. NO domain logic. │   coeus-router
  └─ < 2,000 tokens                 │
                                    │ (* = Tier 2 cluster)
```

The router uses family as its **first** routing split: a request mentioning
a DOCX path goes to `tools` even if it also contains the word "decision".
A request mentioning "farm-in" goes to `decision` even if a DOCX is
attached. This keeps routing O(n) per family instead of O(n²) across the
whole plugin.

**Project-lifecycle (v1.1) auto-spins-up at session onset.** It creates
the LLM handover note up front and maintains a §8 Skill Telemetry table
tracking which skills are used, how often, whether they worked, and
(via an Architect consultation) the improvements plan. At session close,
the table is popped up to the user for preview and per-row actions
(apply / defer / discard / accept).

---

## The Hard Rules

| # | Rule | Enforcement |
|---|---|---|
| 1 | No `SKILL.md` over **3,000 tokens** | `wc -w SKILL.md` at authoring time; split if exceeded |
| 2 | Trigger descriptions must be **mutually exclusive** | Adversarial trigger test before merge |
| 3 | Tier-3 routers contain **NO domain logic** | Routers only emit `ROUTE → … / WHY → … / RUN → …`, then launch the target via the Skill tool |
| 4 | Shared rules live in **`skills/_shared/`** | `uncertainty_rules.md`, `output_formats.md` |
| 5 | Every skill is **registered** in `SKILL_REGISTRY.md` | Same-commit entry required |
| 6 | Deprecated skills move to **`Templates/deprecated-skills/`** | Never silent delete |
| 7 | Delegation paths use **stable Windows paths** | Never session-relative |

---

## Decision Table

| Situation | Action |
|---|---|
| Skills < 1,000 tokens and functionally distinct | Keep separate (full modular) |
| Skills share a task domain AND merged total < 3,000 tokens | Merge into a Tier-2 cluster |
| A workflow spans multiple clusters | Build a Tier-3 router |
| Any skill > 3,000 tokens | Split — do not ship |
| A common rule appears in 3+ skills | Extract to `skills/_shared/` |

---

## The Six Failure Modes It Defends Against

Each failure mode comes from the council's 6-month premortem
(`Architect_Premortem_Report_Skill_Architecture.md`).

| ID | Failure | Defence in This Architecture |
|---|---|---|
| **FM-01** | Cluster creep — Tier-2 grows past the budget, instructions silently truncate | 3,000-token cap, enforced at authoring |
| **FM-02** | Dead delegation path after a Cowork update — silent fallback to generic knowledge | Stable Windows paths only |
| **FM-03** | Orphan skill — never registered, recreated from scratch next session | Mandatory `SKILL_REGISTRY.md` entry |
| **FM-04** | Shared-rule divergence — six skills, six definitions of "uncertain" | `skills/_shared/` is single source of truth |
| **FM-05** | Trigger war — old standalone and new cluster fight for the same phrase | Immediate deprecation on cluster introduction |
| **FM-06** | Handover gap — next session has no memory of the architecture decision | Architecture documented in repo + `Coeus_LLM_HANDOVER.md` |

---

## How To Use The Router

```
You: "I'm trying to decide whether to farm into the West Atobi block.
      Which coeus skill?"

coeus-router:
  ROUTE → ep-council
  WHY  → E&P opportunity, farm-in decision — EP-Council's domain.
  RUN  → /coeus:ep-council West Atobi farm-in
```

The router then **launches** the routed-to skill in the same response by
calling the Skill tool (`Skill(skill="coeus:<name>", args="<task>")`). The
`RUN →` slash command is shown for the user's reference only — slash commands
printed in model output are inert; only a Skill-tool call actually loads the
target skill (v1.2.0 clarification; earlier versions said "invoke" without
naming the mechanism, and the router routinely stopped after printing the
block). The router does not summarise what the target skill is about to do —
the target skill speaks for itself.

When two skills tie, the router asks **one** clarifier and then routes. It
never invents a third path or stalls.

---

## Adding A New Skill

1. Pick a tier from the decision table.
2. Draft `SKILL.md`. Lead `description:` with `Trigger on:` (auto-trigger reliability — v3.7.0 convention).
3. Verify `wc -w SKILL.md` × 1.33 < 3,000 tokens.
4. Cross-check triggers against `skills/_shared/SKILL_REGISTRY.md` — no collisions.
5. Add a row to `SKILL_REGISTRY.md` in the **same commit**.
6. If references analysis or uncertainty, link `skills/_shared/uncertainty_rules.md` in the SKILL body.
7. Update `Coeus_LLM_HANDOVER.md` at session close.

Full checklist: `docs/SKILL_ARCHITECTURE.md`.

---

## Source Material

| Document | Where | What |
|---|---|---|
| `Architect_Final_Plan_Skill_Architecture.md` | Author's local outputs dir | Full council deliberation that produced this architecture |
| `Architect_Premortem_Report_Skill_Architecture.md` | Author's local outputs dir | Six failure modes + risk register |
| `LLM_Handover_Skill_Creation.md` | Author's local outputs dir | The session-portable skill-creation protocol |
| [SKILL_ARCHITECTURE.md](SKILL_ARCHITECTURE.md) | In-repo | The machine-readable spec |
| `skills/_shared/SKILL_REGISTRY.md` | In-repo | The canonical skill list |
| `skills/coeus-router/SKILL.md` | In-repo | The router skill itself |

---

## See Also

- [LLM-Council](LLM-Council.md) — the general-purpose decision engine
- [EP-Council](EP-Council.md) — the E&P-domain decision engine
- [COEUS_EXTENSIONS](COEUS_EXTENSIONS.md) — documented divergences from the official plugin spec
- [CONFORMANCE_REPORT](CONFORMANCE_REPORT.md) — audit vs `anthropics/knowledge-work-plugins`
