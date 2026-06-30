# project-lifecycle Sub-function A — Session Resume (shared)

> Shared protocol for orienting a new LLM session on an existing long-running project. Used by `project-lifecycle` Sub-A. Load when the user is resuming a project.

**When:** User starts a new session on an existing project and needs orientation.

---

## Resume Protocol — ordered steps

1. **Read the handover note first.**
   Look for a file matching `*LLM_Handover*.md` or `*handover*.md` in the
   project's Outputs/ directory. Read it fully. This is the primary source
   of truth for project state.

2. **Read the latest changelog entry.**
   Look for `changelog_*.md` in Outputs/. Read only the last entry (most
   recent session block). Do not read the whole file unless the handover
   note references something in an earlier session.

3. **Read CLAUDE.md and memory/ if present.**
   The session memory at `C:\Users\...\spaces\...\memory\` contains user
   preferences and project facts. Read MEMORY.md index, then load relevant
   memory files.

4. **Identify pending tasks.**
   The handover note's "Pending Tasks" or "How to Resume" section lists
   what was left incomplete. Report these to the user before starting work.

5. **Do NOT read the primary artefact (e.g., the DOCX) unless specifically needed.**
   Large files are expensive. The handover note describes current file state.
   Only open the DOCX, xlsx, or other large files when the task requires it.

6. **Confirm session path.**
   Run `ls /sessions/` in bash to get the current session ID.
   All temp work goes to the session outputs dir (ephemeral).
   All saved work goes to the stable Windows path from the handover note.

---

## Resume report format

After reading the above, report to the user:

```
## Session Resume — [Project Name]

**Current master file:** [path and size]
**Last session:** [Session N, date]
**Session ID (this session):** [kind-sweet-planck or current]

### Pending tasks
1. [task 1 from handover]
2. [task 2 from handover]

### Key constraints to remember
- [any hard rules from handover, e.g., protected paragraph indices]

Ready. What would you like to tackle first?
```
