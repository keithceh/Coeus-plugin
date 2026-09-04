# `atlas.json` — schema

> The structured intermediate for `skills/atlas/`. Written to `Outputs/atlas.json`,
> then injected into `references/template.html` at `/*__ATLAS_DATA__*/` to produce
> `Outputs/atlas.html`. This file is the contract between Phase 1 (survey) and the
> render shell — the template reads nothing else.

Encoding UTF-8, no BOM. Unknown top-level keys are ignored by the template;
missing optional keys degrade gracefully (the region renders with a marked gap,
never a crash).

---

## Top level

| Key | Type | Required | Purpose |
|---|---|---|---|
| `meta` | object | yes | Identity and provenance |
| `frame` | object | yes | Region ① |
| `now` | object | yes | Region ② |
| `map` | object | yes | Region ③ |
| `story` | object | yes | Region ④ |
| `layout` | object | yes | Frozen ordering; neutral-group marking |

---

## `meta`

| Key | Type | Required | Notes |
|---|---|---|---|
| `project` | string | yes | Display name, header strip |
| `generated` | string | yes | ISO-8601 date or datetime of this build |
| `atlas_version` | string | yes | Schema/generator version, `"1.1.0"` for this release |
| `sources[]` | array of object | yes | Every mined source. `{kind, path, note?}` where `kind` ∈ `handover \| artefacts_index \| telemetry \| git \| readme \| changelog \| docs \| filesystem \| interview \| user` |

`sources[]` is the traceability spine: nothing may appear in `frame`, `map`, or
`story` that does not trace to a source entry or an `interview`/`user` answer.
Keep each `path` short — the header strip prints every one of them verbatim, so
a handful of long descriptive paths turns the metaline into a paragraph. Put the
detail in `note`, which is not rendered there.

## `frame` — region ①

| Key | Type | Required | Notes |
|---|---|---|---|
| `intent` | string | yes | 1–2 sentences. Also used in the header strip (R14) |
| `scope_in[]` | array of string | yes | What this project covers |
| `scope_out[]` | array of string | yes | Explicit non-goals. An empty array is a finding, not a default |
| `guardrails[]` | array of object | yes | `{id, rule, origin_beat}` — `id` unique, `rule` ≤ 140 chars, `origin_beat` is a `story.beats[].id` or `null` when the origin is genuinely unknown |
| `references[]` | array of object | no | `{label, link?}` — external standards, specs, people, prior work |

Every guardrail badge in the STORY region links back to the guardrail here, and
each guardrail links forward to `origin_beat` (R1 contiguity, R4 causality).

## `now` — region ②

| Key | Type | Required | Notes |
|---|---|---|---|
| `last_touched` | string | yes | ISO-8601 date of the last real work, not of this build |
| `position` | string | yes | Where work stopped, in one or two sentences (R13) |
| `open_threads[]` | array of string | yes | Unresolved questions and half-finished work |
| `next[]` | array of string | yes | Concrete next actions |
| `recall_prompt` | string | no | Optional collapsed "before you look, what do you think the current state is?" prompt. Extrapolation — see `design_rules.md` uncertainty flag 7 |

`now` is rewritten in full on every refresh. It is the only region that does not
inherit from the prior file.

## `map` — region ③

```
map.groups[]  { id, label }
map.nodes[]   { id, label, kind, status, group, desc, link?, delta? }
map.edges[]   { from, to, verb, delta? }
```

| Field | Domain |
|---|---|
| `nodes[].kind` | `artifact` · `input` · `output` · `external` · `person` · `reference` |
| `nodes[].status` | `active` · `superseded` · `draft` · `unknown` |
| `nodes[].desc` | ≤ 120 characters. Rendered inside the node's card, never in a legend. **Only the first ~33 characters fit the card**; the remainder is reachable on hover — front-load the meaning into the opening words |
| `nodes[].link` | Optional path or URL. Project-reference links only |
| `edges[].verb` | **Required, non-empty.** e.g. `constrains`, `feeds`, `supersedes`, `forked-from`, `produces`, `validates` |
| `*.delta` | `new` · `changed` — set on refresh only |

Rules the survey must satisfy before writing this object:

- `edges[].from` / `edges[].to` must both resolve to a `nodes[].id`.
- `nodes[].group` must resolve to a `groups[].id`.
- Groups follow the reader's mental model — purpose, lifecycle, or ownership —
  never alphabetical or file-path order (R5).
- `kind` is the redundant, non-colour channel: the template gives each kind its
  own corner radius and no two kinds share one — `output` square, `external`
  barely rounded, `artifact` lightly rounded, `input` rounded, `reference`
  rounder, `person` stadium. `status` is the second non-colour channel, carried
  by the border dash (`superseded`, `draft`, and `unknown` each dash
  differently; `active` is solid).
- An unestablished node keeps `status: "unknown"` and a `label` that ends in
  `?`; it is never omitted and never guessed (Phase-1 truthfulness rule).

## `story` — region ④

```
story.beats[] { id, date?, what, why, outcome, type, guardrails[], parent?, branch?, delta? }
```

| Field | Domain |
|---|---|
| `type` | `decision` · `fork` · `failure` · `milestone` |
| `what` | What was done — the action |
| `why` | Why it was done, or what forced it |
| `outcome` | What resulted, including the failure if it failed |
| `guardrails[]` | `frame.guardrails[].id` values that originated at this beat |
| `parent` | Optional `beats[].id` this beat continues from — draws the causal chain |
| `branch` | Optional branch label; two beats sharing a `parent` with different `branch` values render as a fork |
| `date` | Optional. A beat without a date is still a beat; a beat without `why` is a defect |

Newest beat first in render order. `what → why → outcome` is mandatory: a beat
reduced to a dated one-liner fails R4 and the Phase-3 checklist.

## `layout` — frozen ordering

| Key | Type | Notes |
|---|---|---|
| `node_order[]` | array of node ids | Render order within the map. Inherited verbatim on refresh; new ids appended at the end of their group's run |
| `group_order[]` | array of group ids | Column/band order in the map. Inherited verbatim on refresh |
| `hues` | object `{group_id: hue}` | One entry per group. Only `null` vs non-null is read — see below. **At most 5 non-null entries** (hard cap 7) |

**Numeric `hues` values are deprecated and ignored (since 1.1.0).** The template
owns a fixed, CVD-validated five-slot categorical palette and assigns it by
`group_order` **position**, with separately-stepped light and dark values — so a
hue can no longer be chosen badly, duplicated, or left to a fallback cycle. An
integer left in the file is advisory only; it changes nothing. What the field
still decides is `null`:

`hue: null` marks a group **neutral** — it renders grey and consumes no palette
slot. It is the escape hatch when the reader's natural grouping runs to six: use
it for a layer that genuinely is not one of the peer categories (a meta or
routing layer, an "unsorted" band), never to squeeze a sixth real category past
the cap. A group **missing** from `hues` is treated as non-neutral and takes the
next slot; give every group an explicit entry, `null` included, so "neutral"
reads as a deliberate choice rather than an omission. Past the fifth non-neutral
group the template goes neutral rather than invent a sixth hue, which the Phase-3
checklist reads as a grouping defect to fix in the *data*.

The template performs a deterministic layout honouring `group_order` (the
left-to-right order of the Overview boxes, and both axes of the Grid matrix) and
`node_order` (member order inside every panel and List section) — no
force-directed physics, so the same JSON always renders the same picture (R12).

### What the Map region does with this object (1.1.0)

Three views over the one model, switched by a segmented control in the region
header and all fed by `map` + `layout`:

- **Overview** (default) — one enclosure per group in `group_order`, sized by
  member count, showing the count, an internal-edge count, and two or three
  member names. Between groups, **one aggregated edge per ordered group pair**
  that has any underlying edges, labelled with the dominant verb and its count
  plus any minority verb (`routes-to ×8 + shares-rules-with`), stroke width
  scaled mildly by edge count. Intra-group edges are the box's "N internal
  edges" line, not a self-loop.
- **List** — the relation tree: group sections, node rows carrying kind chip,
  status, description and `delta`, and relation chips. Every edge appears at
  least once. Zero SVG, and the print form.
- **Grid** — an N×N group matrix, N = group count, rows `from` / columns `to`,
  cell = edge count plus dominant verb, diagonal = the intra-group counts.
  **Empty cells stay visible** as faint outlines: the directions that carry no
  relation are part of the reading.

Drill-in is a **member panel** (group click) and then an **ego view** (node
click): the node centred, parents left, children right, every edge verb-labelled.
There is no full node-link graph and no in-place group expansion — see
`design_rules.md` §Bake-off addendum for why.

---

## Worked example (abridged, valid)

```json
{
  "meta": {
    "project": "Kestrel Field Review",
    "generated": "2026-09-01",
    "atlas_version": "1.0.0",
    "sources": [
      {"kind": "handover", "path": "Outputs/Kestrel_LLM_Handover.md"},
      {"kind": "artefacts_index", "path": "Outputs/artefacts_index.md"},
      {"kind": "interview", "path": "session 2026-09-01", "note": "scope_out, guardrail G2"}
    ]
  },
  "frame": {
    "intent": "Decide whether the Kestrel discovery justifies a 2027 appraisal well. One recommendation, defensible to the partner.",
    "scope_in": ["Volumetrics rebuild", "Partner alignment", "Appraisal well case"],
    "scope_out": ["Facilities concept", "Anything downstream of FID"],
    "guardrails": [
      {"id": "G1", "rule": "No volumetrics without the reprocessed 2025 cube.", "origin_beat": "B2"},
      {"id": "G2", "rule": "Partner sees no number before internal sign-off.", "origin_beat": null}
    ],
    "references": [{"label": "PRMS 2018", "link": null}]
  },
  "now": {
    "last_touched": "2026-08-29",
    "position": "Volumetrics rebuilt on the reprocessed cube; the P50 moved down 18% and the partner has not been told.",
    "open_threads": ["Is the 18% drop depth-conversion or reprocessing?", "Partner briefing date"],
    "next": ["Run the depth-conversion sensitivity", "Draft the partner note"],
    "recall_prompt": "Before you look: where do you think the P50 landed?"
  },
  "map": {
    "groups": [
      {"id": "data", "label": "Inputs"},
      {"id": "work", "label": "Analysis"},
      {"id": "deliv", "label": "Deliverables"}
    ],
    "nodes": [
      {"id": "cube25", "label": "2025 reprocessed cube", "kind": "input", "status": "active", "group": "data", "desc": "PSDM reprocessing, delivered 2026-06."},
      {"id": "cube19", "label": "2019 cube", "kind": "input", "status": "superseded", "group": "data", "desc": "Original vintage. Superseded for volumetrics."},
      {"id": "vols", "label": "Volumetrics model", "kind": "artifact", "status": "active", "group": "work", "desc": "P10/P50/P90 on the 2025 cube.", "delta": "changed"},
      {"id": "depth", "label": "Depth conversion ?", "kind": "artifact", "status": "unknown", "group": "work", "desc": "Method not yet established from the sources."},
      {"id": "rec", "label": "Appraisal recommendation", "kind": "output", "status": "draft", "group": "deliv", "desc": "One-page recommendation to the partner."}
    ],
    "edges": [
      {"from": "cube25", "to": "vols", "verb": "feeds"},
      {"from": "cube19", "to": "cube25", "verb": "superseded-by"},
      {"from": "depth", "to": "vols", "verb": "constrains"},
      {"from": "vols", "to": "rec", "verb": "supports", "delta": "new"}
    ]
  },
  "story": {
    "beats": [
      {"id": "B3", "date": "2026-08-29", "what": "Rebuilt volumetrics on the 2025 cube.", "why": "G1 barred the old vintage.", "outcome": "P50 fell 18%; cause not yet separated from depth conversion.", "type": "failure", "guardrails": [], "parent": "B2", "delta": "new"},
      {"id": "B2", "date": "2026-07-04", "what": "Compared 2019 and 2025 cubes at the crest.", "why": "Partner questioned the original closure.", "outcome": "2019 vintage retired for volumetrics; guardrail G1 written.", "type": "decision", "guardrails": ["G1"], "parent": "B1"},
      {"id": "B1", "date": "2026-06-11", "what": "Opened the review on the delivered reprocessing.", "why": "Appraisal slot must be committed by Q1 2027.", "outcome": "Scope fixed to subsurface only.", "type": "milestone", "guardrails": []}
    ]
  },
  "layout": {
    "node_order": ["cube25", "cube19", "vols", "depth", "rec"],
    "group_order": ["data", "work", "deliv"],
    "hues": {"data": 0, "work": 0, "deliv": null}
  }
}
```

Note in the example: `depth` is a marked unknown rather than a guess; `G2` has a
`null` origin because no beat established it; `B3` is a `failure` beat that still
carries what/why/outcome; `delta` markers appear only on items that moved since
the prior build. In `layout.hues` the two `0` values are **not** a duplicated
hue and not a bug — numeric values are ignored since 1.1.0, so `data` and `work`
simply take palette slots 1 and 2 by their position in `group_order`; `deliv` is
marked `null` and renders neutral grey. Written today the numbers would be
omitted in favour of `null`-or-not, and both spellings render identically.

This example's map yields an Overview of three boxes and two aggregated edges
(`data → work` "feeds", `work → deliv` "supports"), with the other two edges
counted as "1 internal edge" on the `data` and `work` boxes; a Grid of 9 cells,
4 populated (including two on the diagonal) and 5 shown empty; and a List in
which all four edges appear at least once.
