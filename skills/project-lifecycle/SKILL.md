---
name: project-lifecycle
version: 1.4.0
argument-hint: "[kickoff|resume|handover|audit|close] [optional project path]"
description: >-
  Trigger on: /project-lifecycle, "new project", "new chat", "new session", "kick off this project", "session start", "resume this project", "pick up where we left off", "update the handover", "update changelog", "audit project files", "session close", "wrap up session".
  Multi-session LLM project lifecycle: kickoff, resume, handover, audit, close. v1.3 - three core files (handover, artefacts_index, telemetry log) created ONCE at kickoff and updated in place. Cadence default end-of-session.
dependencies:
  - the-architect
---
> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply these whenever this skill emits a judgment, recommendation, or simulated voice.


# Project Lifecycle — Kickoff, Resume, Handover, Audit, Close

Five sub-functions for managing long-running multi-session projects.
Detect which the user needs from context and jump in at the right point.

| Sub-function | Triggers | Runs |
|---|---|---|
| **K — Kickoff** | "new project", "new chat", "new session", "start a project", "project kickoff" | At the **start** of any session that does not match Resume |
| **A — Resume** | "resume", "pick up where we left off" + an existing handover note is found | At the start of a session on an **existing** project |
| **B — Handover** | "update the handover", "write a handover note" | Anytime during a session |
| **C — Audit** | "audit the project files", "what files are obsolete" | Anytime during a session |
| **D — Close** | "session close", "end of chat", "wrap up session" | At the **end** of a session |

---

## Sub-function K: SESSION KICKOFF (added v1.1)

**When:** The user starts a new project, a new chat, or a new task that does
not already have a handover note. Also fires when the user explicitly says
"kick off", "session start", or "starting work on".

If a handover note already exists for the named project, **jump to Sub-function A (Resume) instead** — kickoff and resume are mutually exclusive.

### Kickoff Protocol — ordered steps (v1.2)

1. **Confirm scope.** One line: what is the project, what is the deliverable, where will outputs live. Don't ask 4 questions — make defensible defaults and move on.

2. **Pick the project root.** Default: `C:\Claude\Claude-Work\Projects\<ProjectName>\`. Create `Outputs/`, `Outputs/_telemetry/` if missing.

3. **Default cadence silently to `end-of-session` (v1.2.1 — no menu).** Do NOT present a six-option menu — the council ROUTE-A run on v1.2 reversed that choice (friction kills the kickoff path; FM-L2-01). Just surface a one-line invitation in the kickoff report:

   ```
   **Update cadence:** end-of-session (default — say "use ultradian", "per-action", "daily", "milestone", or "custom: <spec>" to override).
   ```

   Record `end-of-session` (or the user's later override) in §9 Update Cadence. Full options table + evidence basis in [`../_shared/lifecycle_frequency.md`](../_shared/lifecycle_frequency.md).

4. **Create the handover note immediately** using `../_shared/lifecycle_handover.md`. File naming: `<ProjectName>_LLM_Handover.md` inside `Outputs/`. Fill §1 (overview), §2 (paths), §4a Inputs (empty), §4b Outputs (empty), §5 (hard rules user stated), §7 (initial task list), §8 (telemetry — empty), §9 (cadence). §3 Session History = empty Session 1 block.

5. **Create `Outputs/artefacts_index.md`** per `../_shared/lifecycle_artefacts.md` §3 — empty buckets, ready to populate.

6. **Create `Outputs/_telemetry/log.md` with the first entry** per `../_shared/lifecycle_artefacts.md` §4. This is the single append-only telemetry log for the entire project — created once at kickoff, appended on every subsequent update, never split into separate files. Skills-used table is empty on the first entry but the file establishes the chronological history root.

7. **Report to the user:**

```
## Session Kickoff — [Project Name]

**Project root:** [path]
**Handover note:** [path] (created)
**Artefacts index:** [path] (created, empty)
**Telemetry log:** [path] (created with kickoff entry — single append-only log for the whole project)
**Update cadence:** end-of-session (default — say "use ultradian", "per-action", "daily", "milestone", or "custom: <spec>" to override).
**Skill telemetry:** initialised (will be populated as we work)

### Initial scope
[one-paragraph restate of what the user asked for]

### What I'll do at the next cadence trigger
- Run housekeeping (audit + delete obsolete) FIRST
- Refresh §4a Inputs / §4b Outputs in the handover (in place)
- Append a new timestamped entry to `_telemetry/log.md` (single file, never duplicated)
- Update §3, §7, §8 in the handover
- (At session close / audit) regenerate `artefacts_index.md` in place (overwrite, not duplicate)
- (At session close) pop up the telemetry table for your review

Ready. First action?
```

8. **Do NOT do any project work yet.** Kickoff is setup only.

---

## Skill Telemetry — §8 of the handover note

Every session, project-lifecycle maintains a structured table in §8 of the handover note tracking which Coeus skills were used and how they performed. This is populated as the session runs (when you observe a skill being invoked, append to it) and presented to the user at session close.

### Telemetry table format

```markdown
## 8. Skill Telemetry — Session [N], [YYYY-MM-DD]

| Skill | Times invoked | Worked as intended? | Failures (count) | Cause | Improvements |
|---|---|---|---|---|---|
| coeus:the-architect | 1 | Yes | 0 | — | — |
| coeus:project-lifecycle | 2 | Yes | 0 | — | — |
| [skill] | N | Yes/Partial/No | N | [cause] | [planned fix] |

**Improvements plan (consulted via the-architect):**
[summary of the architect's recommended fixes — see "Architect consultation" below]
```

### Counting rules

- **Times invoked**: count every time Claude actually loaded and acted on the skill's instructions (not just trigger-matches). Inline tool work (Bash/Read/Edit) does NOT count — only Coeus-plugin skills, anthropic-skills, and other named skills with a `SKILL.md`.
- **Worked as intended?**: `Yes` if it produced the expected output without operator correction. `Partial` if it produced output but required reroute or correction. `No` if it failed to fire or produced wrong output.
- **Failures**: count of partials + nos for this skill this session.
- **Cause**: one line. Common patterns: "stale match table", "trigger collision", "skill loaded but not invoked", "wrong family routed".
- **Improvements**: one line. Defer the architectural answer to the Architect consultation below.

### Architect consultation

If the failure count across the table is ≥ 1, OR the user explicitly requests it, run a **scoped Architect consultation** before reporting close. This is NOT a full ROUTE-A council run — it is a single-pass query against `the-architect`'s rule set:

> "Given these N failures with causes X, Y, Z, what is the minimum-effort improvements plan? Output: ranked list, ≤ 5 items, effort estimate per item."

Do this inline. Do not stall on the full 4-phase council unless the user asks. The Architect consultation output goes into the "Improvements plan" line directly under the telemetry table.

---

## Sub-function A: SESSION RESUME

**When:** User starts a new session on an existing project and needs orientation.

**Protocol:** load [`../_shared/lifecycle_resume.md`](../_shared/lifecycle_resume.md). It contains the 6-step resume protocol (read handover, latest changelog, CLAUDE.md/memory, identify pending tasks, skip primary artefact, confirm session path) plus the resume-report format the user expects to see.
---

## Sub-function B: HANDOVER DOCUMENT

**When:** User wants to create a new handover note, or update an existing one.

**Protocol:** load [`../_shared/lifecycle_handover.md`](../_shared/lifecycle_handover.md). It contains the 8-section handover template (Project Overview → Skill Telemetry) and the update protocol (append session-history block, refresh File State, refresh Pending Tasks, never overwrite Hard Rules without explicit user instruction).

---

## Sub-function C: PROJECT FILE AUDIT

**When:** User wants to know which files in the project directory are active, obsolete, or duplicated.

**Protocol:** load [`../_shared/lifecycle_audit.md`](../_shared/lifecycle_audit.md). It contains: the file-listing bash recipe, the 4-category classification table (Active / Superseded / Temp / Unknown), the report-format template, the pre-delete confirmation rules (including the `mcp__cowork__allow_cowork_file_delete` step for files under C:\Claude\Claude-Work\), and the post-delete handover-update step.

---

## Sub-function D: SESSION CLOSE

**When:** The user says "session close", "end of chat", "wrap up", or signals the session is ending. Also fires at every **cadence trigger** between kickoff and close (see §9 Update Cadence in the handover and [`../_shared/lifecycle_frequency.md`](../_shared/lifecycle_frequency.md)) — but the action-menu pop-up at step 10 is reserved for true close.

**Protocol:** load [`../_shared/lifecycle_close.md`](../_shared/lifecycle_close.md). v1.2 — **housekeeping runs FIRST**: Sub-C audit + obsolete-artefacts delete BEFORE handover refresh, BEFORE artefacts_index.md regen, BEFORE the telemetry-log append. This ensures the index never references doomed files.

**Companion shared file** for §4a/§4b/§9 + the artefacts index format + the telemetry log format (single append-only file, v1.3.0): load [`../_shared/lifecycle_artefacts.md`](../_shared/lifecycle_artefacts.md).
