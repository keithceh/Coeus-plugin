# project-lifecycle Sub-function B — Handover Document (shared)

> Shared protocol for creating or updating an LLM handover document. Used by `project-lifecycle` Sub-B. Load this file when the user wants to create or update a handover note.

**When:** User wants to create a new handover note, or update an existing one.

---

## Handover document structure

Every LLM handover document for a multi-session project must contain:

```markdown
# LLM Handover — [Project Name]
**Last updated:** [YYYY-MM-DD] (Session N, [session-id])
**Primary file:** [Windows path to main deliverable]
**Project folder:** [Windows path to project root]

## 1. Project Overview
[1–3 sentences: what the project is, what the deliverable is]

## 2. Working Environment
- **Stable project path:** C:\...
- **Session path pattern:** /sessions/<session-id>/mnt/Technical_Reports/
  (changes every session — use Windows paths in documentation)
- **Current session ID:** [current]
- **Session outputs (temp):** C:\Users\...\...\outputs\

## 3. Session History
[One block per session, newest first:]

### Session N — [YYYY-MM-DD]
- Tasks completed: [list]
- Files modified: [list with reasons]
- Errors encountered: [list with fixes]
- Pending items: [list]

## 4. File State
| File | Location | Status | Notes |
|---|---|---|---|
| [filename] | Inputs/ | Active | [description] |

## 4a. Inputs
| File / Source | Location | Provided by | Used by | Notes |
|---|---|---|---|---|
| [name] | [path or URL] | user / web / prior session | [skill or task] | one-line |

## 4b. Outputs
| File | Location | Produced by | Status | Description |
|---|---|---|---|---|
| [name] | [path] | [skill] | draft / active / superseded | one-line |

> Full spec for §4a / §4b: load [`lifecycle_artefacts.md`](lifecycle_artefacts.md). The companion `Outputs/artefacts_index.md` is the single-source-of-truth index regenerated on every handover update.

## 5. Key Constraints / Hard Rules
[Any MUST NOT rules — protected indices, locked files, etc.]
[IMPORTANT: these must be preserved verbatim across all sessions]

## 6. How to Resume
1. Read this document
2. Read latest changelog entry
3. Open [primary file] for inspection
4. Current pending tasks: [list]

## 7. Pending Tasks (for next session)
[Numbered list — most important first]

## 8. Skill Telemetry (latest session)
[Telemetry table as defined in the project-lifecycle "Skill Telemetry" section — keep
only the most recent session's table here; older sessions' tables live in
§3 Session History blocks. Full history lives in `Outputs/_telemetry/` —
see `lifecycle_artefacts.md` §4.]

## 9. Update Cadence
**Selected at kickoff:** [per-action | ultradian | end-of-session | daily | milestone | custom: <spec>]
**Next scheduled trigger:** [auto-computed from cadence + current time]
**Last update:** [YYYY-MM-DDTHH:MM]

> Full options + evidence basis: load [`lifecycle_frequency.md`](lifecycle_frequency.md).
```

---

## Handover update protocol

When updating (not creating):
- Append a new block to §3 Session History (do not overwrite old blocks)
- Update §4 File State table to reflect current reality
- Update §7 Pending Tasks to reflect what is now pending
- Update the header's "Last updated" line
- Do not change §5 Hard Rules without explicit user instruction
