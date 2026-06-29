# project-lifecycle Sub-function D — Session Close (shared)

> Shared protocol for closing a project session. Used by `project-lifecycle` Sub-D. Load when the user says "session close", "end of chat", "wrap up", or signals the session is ending.

**When:** The user says "session close", "end of chat", "wrap up", or signals the session is ending.

---

## Close Protocol — ordered steps (v1.2 — housekeeping-first)

> Order matters. Housekeeping runs BEFORE the handover note is written so
> the artefacts index never references files about to be deleted. See
> `lifecycle_artefacts.md` §6 for the rationale.

1. **HOUSEKEEPING FIRST** — run Sub-C audit (`lifecycle_audit.md`), classify files (Active / Superseded / Temp / Unknown), confirm deletions with the user, delete obsolete artefacts. Do NOT proceed to step 2 until the file system is in its final state for this session.
2. **Refresh §4 File State, §4a Inputs, §4b Outputs** in the handover note to reflect the post-housekeeping reality.
3. **Regenerate `Outputs/artefacts_index.md` in place** per `lifecycle_artefacts.md` §3 (clickable links, three output buckets — single-writer plain write; overwrite the pre-existing file created at kickoff).
4. **Append session-close entry to `Outputs/_telemetry/log.md`** per `lifecycle_artefacts.md` §4 (timestamp, skills-used table, failure analysis, defining-details-for-next-LLM). Append to the bottom of the existing file; refresh the header's `Last appended` + `Total updates`. Never create a new file.
5. **Update §3 Session History** in the handover note with this session's work (tasks completed, files modified, errors).
6. **Update §7 Pending Tasks** to reflect what's left.
7. **Finalise §8 Skill Telemetry** (latest session table only — full history lives in `Outputs/_telemetry/log.md`, the append-only project-wide log).
8. **Run the Architect consultation** (see "Skill Telemetry" in the project-lifecycle SKILL.md) if failures ≥ 1.
9. **Append a changelog entry** if the project has a `changelog_*.md`.
10. **Pop up the Skill Telemetry table to the user.** This is the headline of the close report. Present it verbatim from §8, plus the Architect's improvements plan. Ask the user:

```
Session close summary for [Project Name]:

[paste §8 telemetry table here]

**Improvements plan (Architect consultation):**
[paste improvements plan here]

Actions available:
  1. Apply improvement #N now
  2. Defer improvement #N to next session (logged to §7)
  3. Discard improvement #N (logged to §3 with reason)
  4. Accept as-is and close

Which?
```

11. **Wait for user response.** Apply, defer, or discard each item per user direction. Do not auto-apply.

---

## Close Checklist (operator-facing, v1.3)

- [ ] **Housekeeping done first** — Sub-C audit ran, obsolete artefacts deleted with user confirmation
- [ ] Handover note §4 File State + §4a Inputs + §4b Outputs reflect post-housekeeping reality
- [ ] `Outputs/artefacts_index.md` regenerated **in place** (clickable, three buckets, overwrite the kickoff-created file)
- [ ] `Outputs/_telemetry/log.md` **appended** with session-close entry (skills-used, failures, defining details for next LLM) — never a new file
- [ ] Handover note §3 Session History updated with this session's work
- [ ] Handover note §7 Pending Tasks updated
- [ ] Handover note §8 Skill Telemetry populated (latest session only) and presented to user
- [ ] Architect consultation run if any failures observed
- [ ] User actions on improvements plan recorded
- [ ] Changelog entry appended (see companion handover for format)
- [ ] All new skills registered in `LLM_Handover_Skill_Creation.md`
- [ ] All file paths in new/modified SKILL.md files are Windows paths (no session IDs)
- [ ] Any new SKILL.md files are under 3,000 tokens (`wc -w SKILL.md` × 0.75)
