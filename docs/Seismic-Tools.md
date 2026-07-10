# Seismic Tools

> Upstream-O&G utility skills for seismic-interpretation project artefacts. Vendor-neutral by design — parses native project files directly, no proprietary runtime required.

**Version:** 2.0 (current) | **Triggers:** see each skill below

---

## What This Is

A family of seismic-domain skills that complement the Coeus **Office Tools** bundle. Where Office Tools target DOCX/OOXML mechanics, Seismic Tools target subsurface-interpretation project files: horizons, polygons, volumes, processes, well data.

Current contents:

1. **`dug_binary`** (renamed from `dug_projdb` in v2.0) — extract horizons, polygons, volumes, per-volume process history (with full parameters and resolved UUIDs), and parent–child volume lineage from a DUG Insight `project.dugprj` SQLite database into **user-selected artefacts**: xlsx inventory, per-volume DOCX (full / no-pid), and a self-contained interactive HTML lineage explorer.

More skills planned: OpendTect project audit, segyio / lasio batch inspection, well-log curve audit.

---

## When to Use Which

| Symptom / intent | Reach for |
|---|---|
| User has a DUG Insight `project.dugprj` and needs to know what's inside it | `dug_binary` |
| "List all horizons / polygons / volumes" against a DUG project | `dug_binary` |
| "What processes were run on this volume?" + parameter capture | `dug_binary` |
| "Which volumes derive from which?" — lineage map / interactive explorer | `dug_binary` |
| Word report of processes per volume (with or without product IDs) | `dug_binary` |
| Project handover or carry-over to OpendTect / Petrel | `dug_binary` → `project-lifecycle` |

---

## The Skill(s)

### 1. `dug_binary`

**Purpose:** Reverse-engineer a DUG Insight `project.dugprj` (undocumented SQLite database) into the artefacts the user selects.

**Slash command:** `/coeus:dug_binary`

**Triggers:** `"dug project"`, `"dug insight project"`, `"dugprj"`, `"list horizons from dug"`, `"list polygons from dug"`, `"list volumes from dug"`, `"horizon inventory"`, `"polygon inventory"`, `"volume inventory"`, `"processes per volume"`, `"what processes were run on this volume"`, `"volume lineage"`, `"seismic project audit"`, `"extract horizons polygons volumes"`, `"audit a dug project"`, `"dug project database"`, `"dug sqlite"`.

**Input rule — no defaults.** The `.dugprj` path MUST be supplied by the user. The skill never assumes, globs for, or defaults to any path; a path may only be reused within the same task/session.

**Artefact selection.** At skill start (immediately after the DB path is validated) the user chooses which outputs to generate — multi-select, default all:

| Artefact | Produced by |
|---|---|
| Inventory workbook (xlsx) | scripts 01→02→03 (always produced — base for the rest) |
| Volume-processes DOCX (full, with pids) | script 04 |
| Volume-processes DOCX (no-pid — IDs stripped, asserts zero literal "pid") | script 04 `--no-pid` |
| Interactive HTML lineage explorer | script 05 |

**Output (xlsx):**

| Sheet | Rows | What |
|---|---|---|
| README | constants | Method, confidence, key assumptions, counts, caveats, update log |
| Volumes | one per type-13 product | name, owner, path, 3D/2D kind, # lines, trace count, samples, # revisions, first/last revision date, # users, # derived workflows, # vel/inv overlays |
| Volume_Processes | one per (volume, derived process) | ProcessType + full parameter string (UUIDs resolved to names) |
| Process_Catalog | one per unique derived process | Deduplicated catalogue — browse without volume cross-join |
| Horizons | type 12 + type 8 | Gridded horizons + marker / pick names |
| Polygons | type 18 + type 37 | Interpreted polygons + imported shapefiles |
| ProductType_Map | all productTypes | Inferred category mapping with row counts |
| UUID_Index | UUIDs found in params | Each UUID resolved to product (or "(not found)" for horizon-property UUIDs) |

**Output (DOCX):** portrait A4, centered tables. Title block → call-out box pointing to the HTML explorer → "Volumes with no derived processes" (alphabetical) → "Volumes with derived processes" (alphabetical; per volume: process table + Parents/Children lineage mini-tables). The `--no-pid` variant strips every product ID and asserts the literal string "pid" appears nowhere in the saved document.

**Output (HTML explorer):** one self-contained file — no CDNs, fonts, or images; works offline. Component tabs, hover-to-enlarge, click-to-pin with parent (blue) / child (orange) highlighting, clickable sidebar lists, search, whole-diagram pan+zoom. Hardened with `<noscript>` + `window.onerror` banners so a blocked script never presents as a silently blank page.

**Lineage rule:** for each workflow attached to volume V, every `«name» (vol/pidN)` reference in its resolved parameter spec (attributeType=528) identifies a parent of V; children are the inverse; self-loops skipped; singleton volumes not drawn.

**Pipeline:**

```
scripts/01_build_inventory.py    → workbook scaffold + main sheets
scripts/02_extract_parameters.py → enriches Volume_Processes with attrType=528 params
scripts/03_resolve_uuids.py      → replaces UUIDs with «name» (kind/pidN)
scripts/04_export_docx.py        → xlsx → per-volume DOCX (+ lineage tables); --no-pid variant
scripts/05_lineage_explorer.py   → xlsx → self-contained interactive HTML explorer
```

Steps 01–03 take `--db` and `--out` and edit the xlsx **in place**. Steps 04–05 take `--xlsx` and `--out` and need no DB access. All path arguments are required. Scripts 04–05 include `--selftest`.

**Dependencies:** `openpyxl` (steps 01–03, 05); `python-docx` (step 04 only). Python's built-in `sqlite3` handles the DB read.

**Vendor-neutral bias:** No DUG Insight installation required. Database is opened read-only (`?mode=ro`) — no risk of source corruption.

**Does NOT cover:** live DUG editing, LAS/SEG-Y parsing (use `lasio` / `segyio`), non-DUG seismic projects, DOCX caption audits (use `docx-inventory`).

## Honest Caveats — Read Before Reporting Results

1. **DUG schema is undocumented.** Every productType→category mapping is empirical inference, verified against the reference project. Spot-check the ProductType_Map sheet before high-stakes use.
2. **Some processes are baked into volume names** ("spectral shaping", "curvature_max") — they won't appear as separate Volume_Processes rows.
3. **Types 29/30 identification is single-project inference** — 29 = property/axis descriptors, 30 = individual fault sticks (from relatedProductId reference-pattern analysis, 2026-Jul-03). Confirm against a second project before high-stakes use.
4. **Unresolved UUIDs are kept verbatim** rather than silently dropped — traceability over false cleanliness.
5. **Lineage only sees explicit `(vol/pidN)` references** — a workflow whose spec names no input volume contributes no edge.

---

## Why This Sits Apart from Office Tools

| Office Tools | Seismic Tools |
|---|---|
| DOCX / OOXML mechanics | Subsurface-interpretation project files |
| File-format hygiene | Geophysical artefact extraction |
| Cross-industry | Upstream O&G domain |

Both families share the same delivery convention (no multiple file versions, in-place edits, full reproducibility via bundled scripts) and pair with `project-lifecycle` for multi-session continuity.

---

## Related Pages

- [Office Tools →](Tools) (the DOCX / OOXML / project-lifecycle bundle)
- [Coeus README →](../README.md)

---

## Version History

| Version | Key Changes |
|---|---|
| **2.0** (current) | Skill renamed `dug_projdb` → `dug_binary`. Added artefact selection at start (xlsx / DOCX full / DOCX no-pid / HTML explorer, default all), per-volume DOCX export with lineage tables (script 04), self-contained interactive HTML lineage explorer (script 05), volume-lineage extraction rule, and the hard no-default-input rule. Back-ported from the Upstream_Workflows project deliverables. |
| **1.0** | Initial release. `dug_projdb` skill. Introduces the `seismic` family — first non-DOCX tools family in Coeus. |

Go back to the [Main README](../README.md).
