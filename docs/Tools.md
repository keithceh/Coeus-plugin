# Office Tools — OOXML & Project Lifecycle

> Four utility skills that close gaps the generic `docx` / `xlsx` / `memory-management` skills do not cover. Born from real long-running document projects where repair, field correction, inventory extraction, and multi-session continuity all became repeated workflows.

> **Sibling family:** [Seismic Tools](Seismic-Tools) covers subsurface / DUG Insight project artefacts.

**Version:** 1.0 (current) | **Triggers:** see each skill below

---

## What This Is

A bundle of four narrow, high-precision tools delivered together because they share an operational domain (long-running DOCX-centric project work) and call each other in practice:

1. **`ooxml-repair`** — diagnose and fix "Word found unreadable content" errors.
2. **`ooxml-fields`** — correct SEQ field numbering, REF field targets, caption styles.
3. **`docx-inventory`** — extract a complete figure/table inventory to xlsx.
4. **`project-lifecycle`** — session resume, handover note maintenance, file audit.

Each one is **standalone** and **non-overlapping** with the existing Coeus suite. None duplicates `llm-council`, `ep-council`, `morpheus`, `the-architect`, or `plugin-creator`.

---

## When to Use Which

| Symptom / intent | Reach for |
|---|---|
| Word opens the document with the recovery dialog | [ooxml-repair](Tools-OOXML-Repair) |
| `zipfile.BadZipFile` or `etree.XMLSyntaxError` on a `.docx` | [ooxml-repair](Tools-OOXML-Repair) |
| Orphaned comment references / bookmarks / paraId collisions | [ooxml-repair](Tools-OOXML-Repair) |
| Figure or table numbers wrong, out of sequence, duplicated | [ooxml-fields](Tools-OOXML-Fields) |
| Cross-reference (REF field) points at the wrong caption | [ooxml-fields](Tools-OOXML-Fields) |
| "Where are all the figures defined in this DOCX?" | [docx-inventory](Tools-DOCX-Inventory) |
| Need a structured xlsx audit of every caption | [docx-inventory](Tools-DOCX-Inventory) |
| Starting a new session on a multi-session project | [project-lifecycle](Tools-Project-Lifecycle) (resume) |
| Need to write or update an LLM handover note | [project-lifecycle](Tools-Project-Lifecycle) (handover) |
| Project folder is cluttered, need to know what to delete | [project-lifecycle](Tools-Project-Lifecycle) (audit) |

---

## The Four Skills

### 1. `ooxml-repair`

**Purpose:** Diagnose and repair `"Word found unreadable content"` errors and other OOXML schema violations in DOCX files.

**Slash command:** `/coeus:ooxml-repair`

**Triggers:** `"Word unreadable content"`, `"docx corrupt"`, `"fix docx error"`, `"Word recovery dialog"`, `"OOXML schema violation"`, `"repair Word document"`.

**Covers:** ZIP integrity, XML well-formedness, w14:paraId validity and cross-file uniqueness, orphaned bookmarkEnd tags, orphaned comment references (most common root cause), duplicate style IDs, numbering chain integrity, relationship target existence, revision ID uniqueness, footnote reference integrity, mc:Requires namespace declarations. Includes the safe ZIP rebuild recipe that preserves flag_bits and create_version.

**Does NOT cover:** general Word editing (use `docx`), SEQ field correction (use `ooxml-fields`), inventory extraction (use `docx-inventory`).

[Full SKILL.md →](Tools-OOXML-Repair)

---

### 2. `ooxml-fields`

**Purpose:** Manage SEQ fields, REF fields, and caption numbering inside DOCX files via direct XML manipulation.

**Slash command:** `/coeus:ooxml-fields`

**Triggers:** `"fix figure numbers"`, `"SEQ field"`, `"caption numbering wrong"`, `"table numbers out of order"`, `"cross-reference broken"`, `"REF field"`, `"figure captions incorrect"`, `"renumber figures"`, `"SEQ counter reset"`, `"caption style"`, `"hardcoded figure number"`.

**Covers:** locating SEQ fields, reading and correcting cached SEQ values, detecting hardcoded caption numbers, auditing sequence integrity (gaps/duplicates), checking REF field targets resolve to defined bookmarks.

**Does NOT cover:** DOCX corruption (use `ooxml-repair`), general editing (use `docx`), structured xlsx inventory (use `docx-inventory`).

[Full SKILL.md →](Tools-OOXML-Fields)

---

### 3. `docx-inventory`

**Purpose:** Extract a complete figure and table inventory from a DOCX file and write it to a two-sheet xlsx (Figures, Tables) with per-row issue flagging.

**Slash command:** `/coeus:docx-inventory`

**Triggers:** `"figure inventory"`, `"table inventory"`, `"list all figures"`, `"list all tables"`, `"extract captions"`, `"caption list"`, `"figure list from docx"`, `"audit captions"`, `"inventory of figures"`, `"what figures are in the document"`.

**Output:** xlsx with two sheets. Each row: paragraph index, cached SEQ number, caption text, style, detected issues (no-SEQ-field, duplicates, gaps).

**Does NOT cover:** editing (use `docx`), repair (use `ooxml-repair`), SEQ correction (use `ooxml-fields`), standalone xlsx creation (use `xlsx`).

[Full SKILL.md →](Tools-DOCX-Inventory)

---

### 4. `project-lifecycle`

**Purpose:** Manage the full lifecycle of a long-running, multi-session LLM project. Three sub-functions in one cluster skill.

**Slash command:** `/coeus:project-lifecycle`

**Triggers:** `"resume this project"`, `"pick up where we left off"`, `"update the handover"`, `"write a handover note"`, `"create a handover doc"`, `"update the changelog"`, `"audit the project files"`, `"what files are obsolete"`, `"clean up the project folder"`, `"which files can I delete"`, `"session close"`, `"end of session checklist"`.

**Sub-functions:**

| Sub | When | What it does |
|---|---|---|
| **Resume** | New session on existing project | Read handover, read latest changelog entry, read CLAUDE.md/memory, identify pending tasks, confirm session paths, report state to user |
| **Handover** | Creating or updating the LLM handover document | Apply the 7-section handover template; on update, append a session block (never overwrite), refresh File State table, refresh Pending Tasks |
| **Audit** | Project folder cleanup | Classify every file as Active / Superseded / Temp / Unknown; produce a report with delete recommendations; confirm before deletion |

**Does NOT cover:** Claude's own memory (use `memory-management`), creating specific document types (use `docx`/`xlsx`/`pptx`), or general research.

[Full SKILL.md →](Tools-Project-Lifecycle)

---

## Why These Four Belong Together

| Real workflow | Skills invoked, in order |
|---|---|
| Open a corrupt DOCX from a colleague, audit it, fix it | `ooxml-repair` → `docx-inventory` → `ooxml-fields` |
| Inherit a long-running document project at session 16 | `project-lifecycle` (resume) → `docx-inventory` → fixes as needed |
| Ship a final version and document the work | `ooxml-repair` (final check) → `project-lifecycle` (handover) |
| End of multi-session contract, file cleanup | `project-lifecycle` (audit) |

Bundled as one umbrella so a user thinking *"I have a DOCX problem and a project to manage"* sees all four together rather than hunting through the wider skill list.

---

## Related Pages

- [OOXML Repair → full SKILL.md](Tools-OOXML-Repair)
- [OOXML Fields → full SKILL.md](Tools-OOXML-Fields)
- [DOCX Inventory → full SKILL.md](Tools-DOCX-Inventory)
- [Project Lifecycle → full SKILL.md](Tools-Project-Lifecycle)
- [Coeus README →](../README.md)

---

## Version History

| Version | Key Changes |
|---|---|
| **1.0** (current) | Initial release. Four skills delivered together: ooxml-repair, ooxml-fields, docx-inventory, project-lifecycle. Born from MAE-1R1 Well Completion Report project (Sessions 1–15, June 2026). |

Go back to the [Main README](../README.md).
