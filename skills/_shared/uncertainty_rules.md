# Shared Uncertainty Rules

> Single source of truth for uncertainty handling across all Coeus skills.
> Referenced by SKILL.md files via the `_shared.md` convention from
> `docs/SKILL_ARCHITECTURE.md`.

---

## Core Rule

Distinguish between **known facts**, **reasonable inferences**, and **speculation** at every step. Never present uncertain claims as facts.

## Marking Conventions

| Confidence | Marker | Example |
|---|---|---|
| Verified fact | (no marker) | "The plugin loads `.claude-plugin/plugin.json`." |
| Reasonable inference | `Likely:` | "Likely: token bloat triggered the silent truncation." |
| Speculation / unverified | `[UNVERIFIED]` | "[UNVERIFIED] This is the first occurrence of FM-04." |
| Simulated model voice | hedged language | "Claude Opus would probably argue..." |

## Hard Rules

1. Never fabricate citations, references, or source URLs.
2. Never fabricate model capabilities (e.g. don't claim a model has a tool it doesn't have).
3. When a claim depends on an unvalidated assumption, surface that assumption inline.
4. When confidence drops mid-output, switch markers — don't carry false certainty forward.
5. Minority positions inside a council/red-team must be surfaced even after consensus.

## Application

Any Coeus skill producing analysis, plans, or simulated model voices must obey these rules. Skills that primarily compress or transform (e.g. `caveman`) preserve uncertainty markers verbatim during transformation.
