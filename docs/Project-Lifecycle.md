# Project-Lifecycle

> Five-sub-function cluster skill that manages the full lifecycle of a long-running, multi-session LLM project: kickoff, resume, handover-doc maintenance, file audit, and session close. Three core files (handover, artefacts index, telemetry log) are **created once at kickoff and updated in place** thereafter — no timestamped duplicates.

**Version:** v1.3.0 (current) | **Triggers:** `/coeus:project-lifecycle` · `"new project"` · `"resume this project"` · `"update the handover"` · `"audit the project files"` · `"session close"`

---

## What It Does

Project-Lifecycle replaces ad-hoc session management with a structured five-stage protocol. It is **not** a chatbot — it is a phase-gated cluster that creates persistent project artefacts at kickoff and refreshes them at every cadence trigger. The contract is "**one file per concern, write-once-create / update-in-place**" — the artefacts index never points at files that no longer exist, the telemetry log never fragments across timestamped files, and the handover note is the single source of truth for project state.

It is the **only** Coeus skill that fires at session boundaries (start + end). Every other skill fires on demand; this one fires on the clock.

---

## Installation

Bundled in `coeus.plugin`. No separate install.

**Recommended:**
1. Download `coeus.plugin` from [**Releases**](https://github.com/keithceh/Coeus/releases)
2. Claude Desktop / Cowork → **Settings → Capabilities → Customize → Add Plugin**
3. Select `coeus.plugin`

**Build from source:** `python scripts/build-plugin.py` (cross-platform, UTF-8-flagged for Cowork).

---

## Triggers

| Trigger | Notes | Sub-function |
|---------|-------|--------------|
| `/coeus:project-lifecycle` | Primary slash command (any sub) | router picks |
| `"new project"` / `"new chat"` / `"new session"` | Kickoff | **K** |
| `"kick off this project"` / `"project kickoff"` / `"session start"` | Kickoff | **K** |
| `"resume this project"` / `"pick up where we left off"` | Resume | **A** |
| `"update the handover"` / `"update llm handover"` / `"write a handover note"` | Handover write | **B** |
| `"update coeus llm handover"` / `"update the changelog"` | Handover write | **B** |
| `"audit the project files"` / `"what files are obsolete"` / `"clean up the project folder"` | File audit | **C** |
| `"session close"` / `"end of chat"` / `"wrap up session"` | Close | **D** |

**Auto-trigger:** firing the skill at session boundaries is its purpose — never wait for the user to ask twice if they say "new chat", "starting work on", or "session close".

**Do NOT use for:** Claude's own memory (use `memory-management`), creating specific document types (use `docx` / `xlsx` / `pptx`), or general research.

---

## The Five Sub-Functions

```
                                  PROJECT TIMELINE
                                  ─────────────────────────────────
  Session 1  │  Session 2  │  …  │  Session N
  ▼          ▼             ▼     ▼
  K          A (or K)      A     A         ← at every session start
  │          │             │     │
  ├──────────┴─────────────┴─────┤
  │   B / C fire ad-hoc          │         ← during work
  │                              │
  ▼                              ▼
  D                              D         ← at every session end
```

| Sub | When | What it does |
|---|---|---|
| **K — Kickoff** | Session start on a **new** project | Defaults silently (no menu), creates the three core files, writes the kickoff entry, restates scope |
| **A — Resume** | Session start on an **existing** project | Reads handover, reads telemetry log latest entry, surfaces pending tasks |
| **B — Handover** | Anytime during a session | Creates or updates the handover note via the 9-section template |
| **C — Audit** | Anytime during a session | Classifies every project file (Active / Superseded / Temp / Unknown), produces delete recommendations |
| **D — Close** | Session end | **HOUSEKEEPING FIRST**, then refresh handover + appendix-index + telemetry log; pop telemetry to user with Architect-consultation improvements plan |

Detail for each sub-function lives in `skills/_shared/lifecycle_{kickoff,resume,handover,audit,close}.md` — load on demand.

---

## The Three Core Files

Project-Lifecycle's defining design: every multi-session project has **exactly three persistent files**, created once at kickoff, updated in place thereafter. No timestamped duplicates. No `_telemetry/index.md` rollup. No write amplification.

| File | Path | Lifecycle |
|---|---|---|
| **Handover note** | `Outputs/<ProjectName>_LLM_Handover.md` | Created at Sub-K. Updated section-by-section by Sub-B at every cadence tick + Sub-D at session close. |
| **Artefacts index** | `Outputs/artefacts_index.md` | Created at Sub-K (empty buckets). Regenerated **in place** (overwrite) at Sub-D close and Sub-C audit. Three buckets: Active / Superseded / Temp. |
| **Telemetry log** | `Outputs/_telemetry/log.md` | Created at Sub-K with kickoff entry. **Append-only** — every cadence-tick / audit / close adds a new timestamped section to the bottom. Header `Last appended` + `Total updates` refreshed each append. |

This contract closes three failure modes:
- **FM-L2-01** (kickoff friction) — silent cadence default, no menu
- **FM-L2-02** (write amplification) — artefacts index regen on close only
- **FM-L2-03** (telemetry orphan) — single append-only log is its own index

---

## Update Cadence

Selected silently at kickoff; default = `end-of-session`. Override anytime by saying `"use ultradian"`, `"per-action"`, `"daily"`, `"milestone"`, or `"custom: <spec>"`.

| Cadence | Trigger | Best for |
|---|---|---|
| **end-of-session** (default) | Sub-D fires | Most projects; lowest write amplification |
| **per-action** | After every Coeus skill invocation | High-stakes projects where every step must be recorded |
| **ultradian** | Every ~90 minutes during work | Long single-session work; matches attention rhythm |
| **daily** | First trigger after a calendar-day boundary | Multi-day projects with daily check-ins |
| **milestone** | When the user says "milestone reached" | Project plans with explicit phase boundaries |
| **custom** | User-defined spec | Anything else |

Full options table + evidence basis in [`../skills/_shared/lifecycle_frequency.md`](../skills/_shared/lifecycle_frequency.md).

---

## Skill Telemetry — §8 of the handover

Every session, project-lifecycle maintains a structured table in §8 of the handover note tracking which Coeus skills were used and how they performed. Populated as the session runs, presented to the user at session close.

```markdown
## 8. Skill Telemetry — Session [N], [YYYY-MM-DD]

| Skill | Times invoked | Worked? | Failures | Cause | Improvements |
|---|---|---|---|---|---|
| coeus:the-architect | 1 | Yes | 0 | — | — |
| coeus:project-lifecycle | 2 | Yes | 0 | — | — |

**Improvements plan (consulted via the-architect):**
[summary]
```

**Counting rule:** count every time Claude actually loaded and acted on the skill's instructions (not just trigger-matches). Inline tool work (Bash/Read/Edit) does NOT count — only Coeus-plugin skills, anthropic-skills, and other named skills with a `SKILL.md`.

**Architect consultation:** if failures ≥ 1 OR the user requests it, run a scoped single-pass query against `the-architect`'s rule set before reporting close. NOT a full ROUTE-A council run — it's a ranked ≤5-item improvements plan with effort estimates.

---

## Session Close — The Headline Sub-Function

Sub-D (Close) is where Project-Lifecycle does its highest-value work. **Order matters:**

```
1. HOUSEKEEPING FIRST  → Sub-C audit, classify, confirm-and-delete obsolete files
2. Refresh handover §4 / §4a / §4b  → post-housekeeping reality
3. Regenerate artefacts_index.md in place  → never references deleted files
4. Append session-close entry to _telemetry/log.md  → single append, no new file
5. Update handover §3 / §7 / §8
6. Architect consultation if failures ≥ 1
7. Append changelog entry
8. Pop telemetry table + improvements plan to user
9. Wait for user action (apply / defer / discard / accept)
```

Full 11-step protocol + 13-item operator checklist in [`../skills/_shared/lifecycle_close.md`](../skills/_shared/lifecycle_close.md).

---

## Mid-Session Commands

| Command | What happens |
|---------|-------------|
| `"use ultradian"` / `"per-action"` / `"daily"` / `"milestone"` / `"custom: <spec>"` | Override cadence; record in §9 |
| `"audit now"` | Sub-C fires immediately |
| `"update handover"` | Sub-B fires immediately |
| `"force close"` | Sub-D fires immediately even if no cadence trigger |

---

## When To Use Project-Lifecycle vs Alternatives

| Use… | When |
|---|---|
| **Project-Lifecycle** | Multi-session work that will run across days/weeks; needs a persistent handover; multiple deliverables to track |
| **`memory-management`** (anthropic-skill) | Your personal `CLAUDE.md` + `memory/` knowledge base (Claude's own state, not a project) |
| **`docx`** / **`xlsx`** / **`pptx`** | Producing specific document types as the deliverable |
| **Nothing** | One-shot task that finishes inside a single session |

---

## Related Pages

- [Coeus README →](../README.md)
- [EP-Council main page →](EP-Council.md) (the E&P-specific decision skill)
- [LLM-Council main page →](LLM-Council.md) (the general-purpose decision skill)
- [Tools umbrella →](Tools.md) (DOCX-mechanic skills + project-lifecycle)
- Shared protocol files: `skills/_shared/lifecycle_{kickoff,resume,handover,audit,close,artefacts,frequency}.md`

---

## Version History

| Version | Key Changes |
|---|---|
| **v1.4.1** (current) | Close protocol step 12 (`_shared/lifecycle_close.md`): after the artefacts index is regenerated, offer a Project Atlas refresh (`/coeus:atlas refresh`) — only when `Outputs/atlas.html` already exists. Lifecycle never creates an atlas and never refreshes without the user's yes. |
| v1.4.0 | Resume step 7 renames the handover to `<task>_handover_note.md` on session resume and updates all references to it. |
| v1.3.0 | Three core files (handover, artefacts_index, telemetry log) **created once at kickoff, updated in place** thereafter. Dropped `_telemetry/<timestamp>_<event>.md` per-update files. Dropped `_telemetry/index.md` rollup file. Single append-only `_telemetry/log.md` is its own index — closes FM-L2-03 by construction. SKILL.md trimmed to ~1,853 tokens. |
| v1.2.1 | Council-driven reversals: silent default `end-of-session` cadence (no 6-option menu — closes FM-L2-01); `artefacts_index.md` regen at close only (closes FM-L2-02); NEW `_telemetry/index.md` rollup file (closes FM-L2-03). |
| v1.2 | Sub-D **housekeeping-first** close protocol. New `_shared/lifecycle_artefacts.md` + `_shared/lifecycle_frequency.md`. New handover §4a Inputs / §4b Outputs / §9 Update Cadence sections. Per-update telemetry notes (later superseded). |
| v1.1 | Sub-K kickoff added. Skill-telemetry §8 added. Architect consultation. Trigger broadened to include "update coeus llm handover" and 4 near-match variants. |
| v1.0 | Initial release. Three sub-functions: Resume / Handover / Audit. Source spec: `C:/Claude/Claude-Work/Projects/Technical_Reports/Outputs/LLM_Handover_Skill_Creation.md`. |

Go back to the [Main README](../README.md).
