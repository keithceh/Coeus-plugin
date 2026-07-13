# Coeus Skill Architecture

**Status:** Adopted 2026-06-24 (v3.8.0). Source: The Architect council run.
Companion: `docs/Coeus-Architecture.md` (user-facing).
Source artifacts (local): `Architect_Final_Plan_Skill_Architecture.md`,
`Architect_Premortem_Report_Skill_Architecture.md`,
`LLM_Handover_Skill_Creation.md`.

---

## TL;DR

> **Clustered Modular with Delegation Pattern.**
> Three tiers, hard 3,000-token cap per `SKILL.md`, shared rules extracted to
> `skills/_shared/`, every skill registered in `skills/_shared/SKILL_REGISTRY.md`.

---

## The Three Tiers

| Tier | Description | Token Budget | Coeus Examples |
|---|---|---|---|
| **Tier 1 — Nano-skill** | One output type or domain, fully standalone | < 1,000 tokens | `caveman`, `docx-inventory` |
| **Tier 1+** | Standalone but content-heavy (rule-table, faction logic) | 1,000–3,000 tokens | `llm-council`, `ep-council`, `plugin-creator`, `ooxml-repair`, `ooxml-fields` |
| **Tier 2 — Cluster skill** | 2–4 related skills merged, reads `_shared.md` | 1,000–3,000 tokens | `morpheus`, `the-architect`, `project-lifecycle` |
| **Tier 3 — Meta-skill (router)** | Thin router only, NO logic | < 2,000 tokens | `coeus-router` |

The 3,000-token limit is a **hard cap**. Skills exceeding it are split before
shipping. Check with `wc -w SKILL.md` (rough proxy; 1 token ≈ 0.75 words).

## The Two Families (added v3.8.x)

Tiers describe **shape**. Families describe **intent**. Coeus now has two:

| Family | Purpose | Skills |
|---|---|---|
| **decision** | Multi-model deliberation, prompt engineering, plugin authoring | `llm-council`, `ep-council`, `morpheus`, `the-architect`, `prompt-master`, `caveman`, `plugin-creator` |
| **tools** | DOCX mechanics, project lifecycle | `ooxml-repair`, `ooxml-fields`, `docx-inventory`, `project-lifecycle` |
| **meta** | Routing only | `coeus-router` |

The router uses family as its **first** routing split (`coeus-router/SKILL.md`
Tie-Breaker 0). New families are added by extending the router's Step 1
table, not by rewriting the existing family routers.

---

## Hard Rules

1. **No `SKILL.md` over 3,000 tokens.** Split if exceeded. *Exception: vendored
   upstream skills (`caveman`, `prompt-master`) are exempt — see
   `skills/_shared/SKILL_REGISTRY.md` for the rationale.*
2. **Trigger descriptions must be mutually exclusive.** Run an adversarial trigger test before merging.
3. **Tier 3 routers contain NO domain logic.** Routing decisions only.
4. **Shared rules live in `skills/_shared/`.** Currently `uncertainty_rules.md` and `output_formats.md`.
5. **Every skill is registered.** New skill ⇒ same-commit entry in `skills/_shared/SKILL_REGISTRY.md` with a declared `family`. *(Note: this rule failed on its first test — the v3.8.0 Tools-bundle commit shipped four unregistered skills. The mitigation is a CI parity check, not a stricter rule.)*
6. **Deprecated skills move to `Templates/deprecated-skills/`.** Never silent delete.
7. **Delegation paths use stable Windows paths.** Never session-relative.

---

## Decision Table

| Situation | Action |
|---|---|
| Skills are < 1,000 tokens and functionally distinct | Keep separate (full modular) |
| Skills share a user-facing task domain AND total < 3,000 tokens merged | Merge into a Tier-2 cluster skill |
| A workflow spans multiple clusters | Build a Tier-3 meta-skill (router only) |
| Any skill > 3,000 tokens | Split — do not ship |
| Common rules appear in 3+ skills | Extract to `skills/_shared/` |

---

## Failure Modes (Premortem Summary)

| ID | Failure | Mitigation in This Architecture |
|---|---|---|
| FM-01 | Cluster creep — Tier-2 grows beyond budget | 3,000-token hard cap, enforced at authoring time |
| FM-02 | Dead delegation path after a Cowork update | Stable Windows paths only; verification step in handover |
| FM-03 | Orphan skill — unregistered, recreated next session | `SKILL_REGISTRY.md` mandatory entry |
| FM-04 | Shared-rule divergence across skills | `skills/_shared/` is the single source of truth |
| FM-05 | Trigger war between old standalone and new cluster | Immediate deprecation on cluster introduction |
| FM-06 | Handover gap — architecture amnesia across sessions | `Coeus_LLM_HANDOVER.md` updated at session close |

Full failure narratives: `Architect_Premortem_Report_Skill_Architecture.md`.

---

## Compatibility — Chat, Cowork, Code

All Coeus skills follow the Claude Code plugin spec
(`<plugin>/skills/<skill>/SKILL.md` with frontmatter), which makes them
load-equivalent in:

| Surface | Loader | Notes |
|---|---|---|
| **Claude Chat** (claude.ai with plugins) | `.claude-plugin/plugin.json` + `skills/` | Auto-discovery |
| **Cowork** (desktop) | Same | Restart required after install/update; mid-session hot-reload not supported |
| **Claude Code** (CLI) | Same | Slash commands auto-register from each `SKILL.md` frontmatter `name:` |

Tier-3 routers and `_shared/` files are read by Claude at invocation time using
the **stable Windows path** anchored to the plugin install dir — they work
identically across all three surfaces.

---

## Adding a New Skill — Checklist

- [ ] Decide tier (1, 2, or 3) using the decision table.
- [ ] Token count under 3,000 (`wc -w SKILL.md`).
- [ ] Frontmatter `name:` matches the folder name.
- [ ] `description:` leads with `Trigger on:` (auto-trigger reliability — see v3.7.0).
- [ ] Triggers do not collide with any existing skill (cross-check `SKILL_REGISTRY.md`).
- [ ] Skill references `skills/_shared/uncertainty_rules.md` if it produces analysis.
- [ ] Registered in `skills/_shared/SKILL_REGISTRY.md` in the same commit.
- [ ] Listed in `docs/Coeus-Architecture.md` (user-facing) if it changes architecture.
- [ ] If a Tier-2 cluster supersedes Tier-1 skills: deprecate them to `Templates/deprecated-skills/`.
- [ ] Handover doc (`Coeus_LLM_HANDOVER.md`) updated.

---

## Automation (added v3.8.x)

The skill-architecture invariants are now enforced by `scripts/build-plugin.py`
on every build. The check runs before bundling — a failed check aborts the
build with a nonzero exit code, so `release.yml` cannot publish a broken
plugin. Local devs can run the check standalone:

```bash
python scripts/build-plugin.py --check-only
```

### Enforced invariants

| # | Check | Severity | Closes |
|---|---|---|---|
| 1 | Every `skills/<name>/` (skipping `_*` dirs) has a row in `SKILL_REGISTRY.md` | **Hard fail** | FM-03 |
| 2 | Every non-vendored `SKILL.md` is ≤ 3,000 tokens (`wc -w × 1.33` heuristic) | **Hard fail** | FM-01 |
| 3 | Every `SKILL.md` frontmatter `name:` matches its directory name | **Hard fail** | FM-05 (drift) |
| 4 | Every routable skill appears in `coeus-router`'s match table | **Warning** (v3.9 → hard fail) | FM-02 + FM-05 (router stale) |

### Skip rules

- `skills/_*` directories — not skills, not validated. Reserved for convention
  files (currently `_shared/`).
- Vendored upstream skills (`caveman`, `prompt-master`) — exempt from invariant 2.
- `coeus-router` itself — excluded from invariant 4 (no self-routing).

### Roadmap

- **v3.9:** promote invariant 4 from warning to hard fail.
- **v3.9:** replace heuristic counter with `tiktoken`.
- **v3.9+:** ship a pre-commit hook wrapping `--check-only`.

## Open Questions

- The `_shared/` files are read at the model layer, not the runtime —
  enforcement is by convention, not by tooling. Acceptable for the current
  scale; revisit at > 20 skills.
- Invariant 4 substring-match on the router table is heuristic. A structured
  markdown-table parser would be more robust but adds complexity for marginal
  gain until a false positive is observed in the wild.
