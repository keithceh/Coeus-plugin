---
name: dug_binary
version: 2.0
argument-hint: "[path to DUG Insight project.dugprj — required, never assumed] [optional output folder]"
description: >-
  Trigger on: /coeus:dug_binary, "dug project", "dugprj", "list horizons from dug", "list polygons from dug", "list volumes from dug", "processes per volume", "volume lineage", "seismic project audit", "audit a dug project", "dug sqlite".
  Extract horizons, polygons, volumes, per-volume processes (params, resolved UUIDs) and volume lineage from a DUG Insight project.dugprj (SQLite). User picks artefacts at start: xlsx, DOCX full/no-pid, HTML lineage explorer. Read-only, no DUG runtime.
dependencies: []
---

> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply when emitting any judgment or interpretation. **Reverse-engineered schema** — every productType→category mapping below is empirical, not from documented DUG schema. Flag uncertainty when reporting to the user.

# DUG Binary — Project Inventory, Process Audit & Lineage

Parses a DUG Insight `project.dugprj` file (SQLite, schema v16.x) and produces
the artefacts the user selects: an Excel inventory of horizons, polygons,
volumes and every process performed on each volume (full parameter capture,
UUID resolution), per-volume Word reports (with or without product IDs), and
a self-contained interactive HTML volume-lineage explorer.

---

## 0. Input Rule + Artefact Selection (do this FIRST)

**Input rule — no defaults, ever.** The `.dugprj` path MUST be supplied by the
user. Never assume, glob for, remember across sessions, or default to any
path. A path already given earlier **in the same task/session** may be
reused; anything else requires asking the user. Validate the path exists and
is SQLite before proceeding.

**Artefact selection.** Immediately after the DB path is validated, ask the
user which artefacts to generate (AskUserQuestion, multiSelect):

| Option | Produced by | Notes |
|---|---|---|
| Inventory workbook (xlsx) | scripts 01→02→03 | Always produced — every other artefact derives from it |
| Volume-processes DOCX (full, with pids) | script 04 | Full detail incl. derived pids |
| Volume-processes DOCX (no-pid) | script 04 `--no-pid` | IDs stripped; script asserts zero literal "pid" |
| Interactive HTML lineage explorer | script 05 | One self-contained file, offline |

Default when the user gives no answer (or the session is non-interactive):
**all four**. Rationale for asking at start rather than mid-run: the choice
determines which pipeline steps execute, and nothing learned mid-run would
change the user's answer — start is the most logical juncture.

## 1. What's Inside a `project.dugprj`

`project.dugprj` is an undocumented SQLite database. Twelve tables; the load-bearing ones are:

| Table | Rows (typical) | Role |
|---|---|---|
| `Product` | 8,000+ | Master object table. Every horizon, polygon, volume, well, log, workflow is a Product with `productType` (int discriminator) and `owner`. |
| `AttributeRevision` | 80,000+ | Attributes attached to products. `attributeType` discriminator. Holds names, file paths, CRS, full process parameter specs, etc. |
| `Revision` + `ProductRevision` | 30,000 + 400,000 | Every edit event. `Revision.revisionTime` is epoch-ms; `Revision.user` is the editor. |
| `volume_headers` / `volume_metadata` / `volume_mtimes` | 92 distinct UUIDs | Physical seismic data — trace_count, samples, increments, geometry. 2D surveys appear as multiple rows sharing one UUID. |
| `BinaryValue` | varies | Blob storage referenced by `AttributeRevision.binaryValueId` (colormaps, display blobs — not parameters). |
| `ProjectMetadata` | <20 | schemaVersion, projectUUID, forkRevisionId, etc. |

## 2. ProductType → Category Mapping (inferred)

Verified by joining UUIDs across `Product ↔ volume_headers` and inspecting
`120hors/`, `100sei/`, `191culture/` file-path prefixes in attribute values.
**Not from documented schema** — always confirm with the project owner.

| productType | Category | Notes |
|---|---|---|
| **12** | **HORIZON (gridded)** | Path under `120hors/`. The main "horizon" deliverable. |
| **13** | **VOLUME (seismic)** | Path under `100sei/`. 3D cubes + 2D survey containers. Matches all `volume_headers` rows. |
| **18** | **POLYGON / contour / outline** | Includes AOIs, depth contours, fault polygons. |
| **8** | Horizon marker / pick name | Formation tops as labels. Treat as part of horizon work. |
| **37** | Culture shapefile | Imported `.shp` under `191culture/`. Polygons in shapefile form. |
| **17** | Workflow / process | Process step (BandpassFilter, SpectralShaping, VolumeMaths, …). Carries full parameter spec via `attributeType=528`. |
| **52** | Display / velocity overlay | Vel/inversion display overlays. Parameters in `attributeType=25800`–`25805`. |
| 1 | Fault sticks | |
| 2 | Well | |
| 3 / 4 / 5 / 6 | Picks / VSP / wireline / log curve | |
| 9 / 10 / 11 | Processing project / 2D survey / 2D line | |
| 23 / 28 | Wavelet / wavelet file | |
| 40 | Curve maths | |
| 41 / 43 / 46 | Litho model / sequence / loop | |
| 47 | Text overlay (`.txt`) | |
| 51 / 53 / 54 | Drilling radius / wells-delta / regression model | |
| 14 / 19 / 31 / 49 | Folder / cross-section / project / scenario | |
| **29** | Property / axis descriptor | One per property slot on horizons (attr 220), polygons (211–213), 2D lines (233–235), cross-sections (462). `attr 201` = slot index; a few carry units (Hz/m/ms/°). Identified 2026-Jul-03 from 6,921 `relatedProductId` references. |
| **30** | Individual fault stick | One per stick — referenced exclusively by fault-stick sets (type 1) via attr 400; each carries attr 401=19. Identified 2026-Jul-03. |

## 3. AttributeType Map (the ones that matter)

| `attributeType` | Holds |
|---|---|
| `1` | Object name (the most important field) |
| `3` | Description / "Generated for…" text |
| `4` | Owner (user) |
| `7` | File path within project tree (`120hors/...`, `100sei/...`) |
| `8` | SHA-1 hash |
| `10` | CRS (e.g. `EPSG:32650`) |
| `101` / `102` | Measure type / unit |
| `500` | **ProcessType label** (BandpassFilter, VolumeMaths, …) for type-17 products |
| **`528`** | **FULL process parameter spec** as indented key/value text (type-17). Contains the workflow UUID then every parameter — filter cutoffs, formula text, source UUIDs, etc. |
| `25800` / `25802` / `25804` / `25805` | Display-overlay kind / tag / colormap / source-product name (type-52) |

## 4. UUID Encoding (verified)

`Product.productUUIDMSB` and `productUUIDLSB` are **signed int64** columns
holding the top 64 and bottom 64 bits of the 128-bit UUID. SQLite stores
unsigned-int64 as signed — round-trip via two's-complement:

```python
def u64_to_s64(x):
    return x - 0x10000000000000000 if x >= 0x8000000000000000 else x
def s64_to_u64(x):
    return x + 0x10000000000000000 if x < 0 else x
def uuid_to_msb_lsb(u):
    h = u.replace("-", "").lower()
    return u64_to_s64(int(h[:16], 16)), u64_to_s64(int(h[16:], 16))
def msb_lsb_to_uuid(msb, lsb):
    msb, lsb = s64_to_u64(msb), s64_to_u64(lsb)
    h = f"{msb:016x}{lsb:016x}"
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"
```

Use this to (a) resolve UUIDs embedded in `attributeType=528` parameter strings, and (b) look up products by string UUID.

## 5. Volume Lineage Rule (verified against reference project)

For each workflow (type-17 product) attached to volume **V_owner**, every
`«name» (vol/pidN)` reference in its resolved parameter spec (from
`attributeType=528`, after step 3) identifies an input volume **V_input**
which is a **parent** of V_owner. Children are the inverse relation.
Self-loops (a volume referencing itself) are skipped. Components are the
weakly-connected components of the resulting digraph; singletons are not
drawn. Reference-project shape: 174 nodes · 52 edges · 6 non-trivial
components (25, 17, 5, 4, 2, 2) · 1 cycle (mutual dependency — the layout is
cycle-tolerant).

## 6. Pipeline — Five Scripts (run the ones the selection requires, in order)

```
scripts/01_build_inventory.py    →  workbook scaffold + main sheets
scripts/02_extract_parameters.py →  enriches Volume_Processes with attrType=528 params + adds Process_Catalog
scripts/03_resolve_uuids.py      →  replaces UUIDs in parameter strings with «name» (kind/pidN)
scripts/04_export_docx.py        →  xlsx → per-volume DOCX (+ lineage tables); --no-pid for the IDs-stripped variant
scripts/05_lineage_explorer.py   →  xlsx → single self-contained interactive HTML lineage explorer
```

```bash
python scripts/01_build_inventory.py    --db <project.dugprj> --out <inventory.xlsx>
python scripts/02_extract_parameters.py --db <project.dugprj> --out <inventory.xlsx>
python scripts/03_resolve_uuids.py      --db <project.dugprj> --out <inventory.xlsx>
python scripts/04_export_docx.py        --xlsx <inventory.xlsx> --out <report.docx> [--no-pid] [--explorer-name <file.html>]
python scripts/05_lineage_explorer.py   --xlsx <inventory.xlsx> --out <explorer.html> [--title "<Project>"]
```

All paths are **required** — the scripts refuse to run with defaults. Steps
01–03 edit the xlsx **in place** (no v2/v3 files, per the Coeus
project-lifecycle convention). Steps 04–05 read the workbook only — no DB
access needed. Scripts 04 and 05 carry `--selftest` self-checks.

## 7. Output Artefacts — Reference

### 7a. Workbook (`.xlsx`) — steps 01–03

| Sheet | Source | Contents |
|---|---|---|
| **README** | Built-in | Method, confidence, key assumptions, counts, caveats, update log |
| **Volumes** | type-13 ⋈ `volume_headers` ⋈ `ProductRevision` ⋈ `Revision` | One row per volume: pid, name, owner, file path, 3D/2D kind, # lines, trace count, samples, # revisions, first/last revision date, # users, # derived workflows, # vel/inv overlays |
| **Volume_Processes** | `AttributeRevision.relatedProductId` lineage | One row per (volume, derived process). Columns: ProcessType, derived name/description, full parameter string |
| **Process_Catalog** | Deduplicated from Volume_Processes | One row per unique derived process — browse processes without volume cross-join |
| **Horizons** | type-12 + type-8 | Gridded horizons + marker/pick names |
| **Polygons** | type-18 + type-37 | Interpreted polygons + imported shapefiles |
| **ProductType_Map** | All productTypes | Inferred category map with row counts and caveats |
| **UUID_Index** | After step 3 | Every UUID found in parameter strings + resolved name / kind / pid (unresolved kept verbatim) |

Substitution format after step 3:
`inputVolumeProduct=«1.1. volume integration» (vol/pid12524)` instead of the raw UUID.

### 7b. Per-volume DOCX — step 04

Portrait A4 (1.5 cm margins), centered tables, Calibri. Title block (source,
timestamp, counts) → yellow call-out box pointing to the HTML explorer → H1
"Volumes with no derived processes" (alphabetical list) → H1 "Volumes with
derived processes" (alphabetical; per volume: heading, process table,
Parents (blue) / Children (orange) lineage mini-tables where relationships
exist). `--no-pid` drops the pid column, strips heading pid suffixes,
rewrites `«name» (vol/pidN)` → `«name» (vol)`, and **asserts** zero literal
"pid" occurrences in the saved document.

### 7c. HTML lineage explorer — step 05

One self-contained file (no CDNs, fonts, or images — works offline and from
a file share). Component tabs (non-trivial components, largest first),
hover-to-enlarge, click-to-pin (parents blue, children orange, rest dimmed),
sidebar with clickable parent/child lists, search (≥2 chars), whole-diagram
pan+zoom, colour legend. Hardened: `<noscript>` notice and a `window.onerror`
banner — script failure shows a visible message, never a silent blank page.

## 8. Honest Caveats

1. **Schema is undocumented.** Every productType/attributeType label is empirical inference. Verify with the project owner before any high-stakes use.
2. **Some processes are baked into volume names** ("spectral shaping", "curvature_max") and won't appear as separate Volume_Processes rows.
3. **Type-13 volumes without `volume_headers` rows are virtual** (derived volumes with no on-disk data). The Volumes sheet flags these as `kind = "(no data)"`.
4. **Types 29/30 identification is single-project inference** (property/axis descriptors and individual fault sticks, from relatedProductId reference patterns) — confirm against a second project before relying on it.
5. **Unresolved UUIDs are kept verbatim** rather than silently dropped — traceability over false cleanliness. Known non-Product UUIDs: horizon **property identifiers** appearing as `property <uuid>` in 528 Horizon blocks and as `attributeType=735` values (paired with 734 = variable name). Property names are not stored in the DB; infer TWT vs TVDSS from formula domain and bound horizon names.
6. **Lineage only sees explicit `(vol/pidN)` references.** A volume derived through a workflow whose spec names no input volume shows no parent.

## 9. Dependencies

```bash
pip install openpyxl --break-system-packages          # steps 01–03, 05
pip install python-docx --break-system-packages       # step 04 only (skip if no DOCX selected)
```

Built-in: `sqlite3`, `re`, `json`, `html`, `datetime`, `pathlib`.

No DUG Insight installation required. Database is opened **read-only** (`file:...?mode=ro` URI) — no risk of corrupting the source.

## 10. Cross-Skill Pairings

- After running this skill, pair with **`project-lifecycle`** to capture the artefacts as deliverables under a properly-tracked project (handover note, changelog, telemetry).
- For DOCX-based deliverables describing the inventory, use **`docx`** then **`docx-inventory`** to audit figure/table captions.
