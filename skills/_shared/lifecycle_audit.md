# project-lifecycle Sub-function C — Project File Audit (shared)

> Shared protocol for auditing a project directory to identify obsolete, duplicate, or misplaced files. Used by `project-lifecycle` Sub-C. Load this file when the user asks for a file audit.

**When:** User wants to know which files in the project directory are active,
obsolete, or duplicated.

---

## Audit protocol

1. **List all files with sizes and dates:**

```bash
find "/sessions/<id>/mnt/Technical_Reports" -type f \
  -exec ls -la --time-style=+"%Y-%m-%d %H:%M" {} \; | sort -k6,7
```

2. **Categorise each file:**

| Category | Criteria |
|---|---|
| **Active** | Referenced in the handover note OR created in the current/last session |
| **Superseded** | An older version exists (e.g., v09.xlsx when v11.xlsx exists) |
| **Temp** | Contains session ID in path, or named `*_temp*`, `*_backup*`, `*_base_fixed*` |
| **Unknown** | Not referenced in handover; not obviously temp or versioned |

3. **Report format:**

```markdown
## Project File Audit — [Project Name]
**Date:** YYYY-MM-DD

### Active files (keep)
| File | Size | Last modified | Reason |
|---|---|---|---|

### Superseded files (recommend delete)
| File | Size | Superseded by | Reason safe to delete |
|---|---|---|---|

### Temp/scratch files (recommend delete)
| File | Size | Notes |
|---|---|---|

### Unknown files (review needed)
| File | Size | Notes |
|---|---|---|

### Summary
- Total files: N
- Recommended for deletion: N (saves X MB)
- Action needed from user: [confirm deletes / classify unknowns]
```

4. **Before deleting:**
   - Confirm with user
   - For files in `C:\Claude\Claude-Work\...`, call
     `mcp__cowork__allow_cowork_file_delete` with the folder path
     to get delete permission before using bash `rm` or the filesystem tool

5. **After deleting:** Update the handover note's File State table.
