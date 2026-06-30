---
name: dug_projdb
version: 1.0
argument-hint: "[path to DUG Insight project.dugprj] [optional output xlsx path]"
description: >
  Trigger on: /coeus:dug_projdb, "dug project", "dugprj", "list horizons from dug",
  "list polygons from dug", "list volumes from dug", "processes per volume",
  "seismic project audit", "audit a dug project", "dug sqlite".

  Extract horizons, polygons, volumes, and per-volume process history
  (with full parameters and resolved UUIDs) from a DUG Insight
  `project.dugprj` (undocumented SQLite) into a multi-sheet xlsx:
  Volumes, Volume_Processes, Process_Catalog, Horizons, Polygons,
  ProductType_Map, UUID_Index, README. Vendor-neutral — built-in
  `sqlite3` + `openpyxl`, no DUG runtime required. Use when the user
  has a DUG project and needs to audit it without opening DUG. Do NOT
  use for live DUG editing, LAS/SEG-Y parsing, or DOCX inventories
  (use `docx-inventory`).
dependencies: []
---

> Shared rules: confidence markers and hedged voices come from [`_shared/uncertainty_rules.md`](../_shared/uncertainty_rules.md). Apply when emitting any judgment or interpretation. **Reverse-engineered schema** — every productType→category mapping below is empirical, not from documented DUG schema. Flag uncertainty when reporting to the user.

# DUG Project Database — Inventory & Process Audit

Parses a DUG Insight `project.dugprj` file (SQLite, schema v16.x) and produces
an Excel inventory of horizons, polygons, volumes, and every process performed
on each volume — with full parameter capture and UUID resolution.

---

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
| 29 / 30 | Unidentified | Largest counts (1,275 + 2,393 in MAE-1R1 ref data). Likely Property/Tag holders. |

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

## 5. Pipeline — Three Scripts (run in order)

```
scripts/01_build_inventory.py   →  builds workbook scaffold + main sheets
scripts/02_extract_parameters.py →  enriches Volume_Processes with attrType=528 params + adds Process_Catalog
scripts/03_resolve_uuids.py      →  replaces UUIDs in parameter strings with «name» (kind/pidN)
```

All three accept the same arguments:

```bash
python scripts/01_build_inventory.py   --db path/to/project.dugprj --out path/to/output.xlsx
python scripts/02_extract_parameters.py --db path/to/project.dugprj --out path/to/output.xlsx
python scripts/03_resolve_uuids.py      --db path/to/project.dugprj --out path/to/output.xlsx
```

Each pass edits the xlsx **in place** — no v2/v3 files. Per the Coeus
project-lifecycle convention, this respects the "no multiple versions of an
Office file" rule.

## 6. Output Workbook — Sheet Reference

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

## 7. Honest Caveats

1. **Schema is undocumented.** Every productType/attributeType label is empirical inference. Verify with the project owner before any high-stakes use.
2. **Some processes are baked into volume names** ("spectral shaping", "curvature_max") and won't appear as separate Volume_Processes rows.
3. **Type-13 volumes without `volume_headers` rows are virtual** (derived volumes with no on-disk data). The Volumes sheet flags these as `kind = "(no data)"`.
4. **Types 29 and 30 remain unidentified** in the reference project. Largest by count; extending the mapping requires inspecting more projects.
5. **Unresolved UUIDs are kept verbatim** rather than silently dropped — traceability over false cleanliness.

## 8. Dependencies

```bash
pip install openpyxl --break-system-packages
```

Built-in: `sqlite3`, `re`, `datetime`, `pathlib`.

No DUG Insight installation required. Database is opened **read-only** (`file:...?mode=ro` URI) — no risk of corrupting the source.

## 9. Cross-Skill Pairings

- After running this skill, pair with **`project-lifecycle`** to capture the inventory as a deliverable under a properly-tracked project (handover note, changelog, telemetry).
- For DOCX-based deliverables describing the inventory, use **`docx`** then **`docx-inventory`** to audit figure/table captions.
