# Seismic Tools

> Upstream-O&G utility skills for seismic-interpretation project artefacts. Vendor-neutral by design — parses native project files directly, no proprietary runtime required.

**Version:** 1.0 (current) | **Triggers:** see each skill below

---

## What This Is

A family of seismic-domain skills that complement the Coeus **Office Tools** bundle. Where Office Tools target DOCX/OOXML mechanics, Seismic Tools target subsurface-interpretation project files: horizons, polygons, volumes, processes, well data.

Current contents:

1. **`dug_projdb`** — extract horizons, polygons, volumes, and per-volume process history (with full parameters and resolved UUIDs) from a DUG Insight `project.dugprj` SQLite database into a multi-sheet xlsx inventory.

More skills planned: OpendTect project audit, segyio / lasio batch inspection, well-log curve audit.

---

## When to Use Which

| Symptom / intent | Reach for |
|---|---|
| User has a DUG Insight `project.dugprj` and needs to know what's inside it | [dug_projdb](Seismic-Tools-DUG-ProjDB) |
| "List all horizons / polygons / volumes" against a DUG project | [dug_projdb](Seismic-Tools-DUG-ProjDB) |
| "What processes were run on this volume?" + parameter capture | [dug_projdb](Seismic-Tools-DUG-ProjDB) |
| Project handover or carry-over to OpendTect / Petrel | [dug_projdb](Seismic-Tools-DUG-ProjDB) → `project-lifecycle` |

---

## The Skill(s)

### 1. `dug_projdb`

**Purpose:** Reverse-engineer a DUG Insight `project.dugprj` (undocumented SQLite database) into an Excel inventory.

**Slash command:** `/coeus:dug_projdb`

**Triggers:** `"dug project"`, `"dug insight project"`, `"dugprj"`, `"list horizons from dug"`, `"list polygons from dug"`, `"list volumes from dug"`, `"horizon inventory"`, `"polygon inventory"`, `"volume inventory"`, `"processes per volume"`, `"what processes were run on this volume"`, `"seismic project audit"`, `"extract horizons polygons volumes"`, `"audit a dug project"`, `"dug project database"`, `"dug sqlite"`.

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

**Pipeline:**

```
scripts/01_build_inventory.py   → workbook scaffold + main sheets
scripts/02_extract_parameters.py → enriches Volume_Processes with attrType=528 params
scripts/03_resolve_uuids.py      → replaces UUIDs with «name» (kind/pidN)
```

All three accept `--db <project.dugprj>` and `--out <output.xlsx>`. Each pass edits the xlsx **in place**.

**Dependencies:** `openpyxl` only. Python's built-in `sqlite3` handles the DB read.

**Vendor-neutral bias:** No DUG Insight installation required. Database is opened read-only (`?mode=ro`) — no risk of source corruption.

**Does NOT cover:** live DUG editing, LAS/SEG-Y parsing (use `lasio` / `segyio`), non-DUG seismic projects, DOCX inventories (use `docx-inventory`).

[Full SKILL.md →](Seismic-Tools-DUG-ProjDB)

## Honest Caveats — Read Before Reporting Results

1. **DUG schema is undocumented.** Every productType→category mapping is empirical inference, verified against the reference project. Spot-check the ProductType_Map sheet before high-stakes use.
2. **Some processes are baked into volume names** ("spectral shaping", "curvature_max") — they won't appear as separate Volume_Processes rows.
3. **Types 29 and 30 remain unidentified** in the reference data (3,668 products combined). Extending the mapping requires inspecting more projects.
4. **Unresolved UUIDs are kept verbatim** rather than silently dropped — traceability over false cleanliness.

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

- [DUG Project DB → full SKILL.md](Seismic-Tools-DUG-ProjDB)
- [Office Tools →](Tools) (the DOCX / OOXML / project-lifecycle bundle)
- [Coeus README →](../README.md)

---

## Version History

| Version | Key Changes |
|---|---|
| **1.0** (current) | Initial release. `dug_projdb` skill. Introduces the `seismic` family — first non-DOCX tools family in Coeus. |

Go back to the [Main README](../README.md).
