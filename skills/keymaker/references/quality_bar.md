# Keymaker Quality Bar — the house visual taste contract

> **Provenance, stated honestly.** This file is *distilled*, not original. Its
> doctrine comes from [`skills/atlas/references/design_rules.md`](../../atlas/references/design_rules.md)
> — which is evidence-graded there, with its own verification caveat and
> uncertainty flags — plus the Anthropic `artifact-design` / `visual-explainer`
> / `dataviz` guidance available in some sessions. Nothing here supersedes
> `design_rules.md`; where the two disagree, that file wins and this one is the
> defect.
>
> | Marker | Meaning |
> |---|---|
> | `[V]` | Verified-in-repo doctrine — traceable to a numbered rule or checklist item in `design_rules.md` |
> | `[H]` | House judgment — the artifact-design / dataviz school, or Coeus convention. Reasonable, not evidenced |

Keymaker Phase 3 runs this checklist against every visualisation artefact in
the project. An artefact that passes is **not touched**.

---

## 1. Orientation

- [ ] A cold reader is oriented **in one glance** — what am I looking at, and
      what is it for. `[V]` (R14: one or two sentences, then stop)
- [ ] Where the mechanism is not self-evident, a **small labelled explainer**
      (inline SVG) shows it. It orients; it never decorates. `[H]`
- [ ] "You are here" is marked where the artefact has a current position —
      a re-entry cue, an active branch, a selected node. `[V]` (R13)
- [ ] Figures carry `figure` / `figcaption` and an `aria-label`. `[H]`
- [ ] Nothing decorative, no unactioned metric, no boilerplate section kept
      "for completeness". `[V]` (R2, coherence)

## 2. Encoding honesty

- [ ] **Every arrow and edge carries a verb or a label.** A bare arrow states
      no proposition and is a defect. `[V]` (R3)
- [ ] **No colour-only encoding.** Every colour-coded distinction also carries
      a redundant shape, border, or dash. `[V]` (R10)
- [ ] Palette is CVD-safe; **at most 5 categorical hues** (hard cap 7). A sixth
      category goes neutral rather than duplicating a hue — and that is a
      grouping defect to fix, not a colour problem. `[V]` (R10)
- [ ] Magnitude is a **single-hue ramp**, never a second categorical slot.
      Sequential data does not get rainbow. `[H]`
- [ ] **It reads in monochrome.** Print it grey and the distinctions survive.
      `[V]` (R10)
- [ ] Colour encodes only distinctions that exist **outside** the artefact
      (status, family, ownership) — never an invented taxonomy. `[V]` (R11)
- [ ] **Empty cells and negative space are shown, not dropped.** The absence of
      a relation is information; a node-link form can only draw what exists,
      which is why the matrix view exists at all. `[V]` (bake-off addendum)

## 3. Direct labelling

- [ ] Labels sit **on the marks**. Every label, date, and status is inside or
      touching the element it describes. `[V]` (R1, spatial contiguity — the
      best-evidenced lever in `design_rules.md`)
- [ ] **No legend, no footnote key, no swatch table** where direct labels fit.
      `[V]` (R1)
- [ ] No bare URLs where a labelled chip serves. `[H]`

## 4. Typography and surface

- [ ] A deliberate type scale — sizes chosen, not defaulted. `[H]`
- [ ] A reading measure (roughly 45–80 characters) for any prose. `[H]`
- [ ] A spacing rhythm: consistent vertical steps, whitespace used
      semantically for grouping. `[V]` (R7, proximity and enclosure do the
      grouping)
- [ ] **Both themes** via the three-state token pattern (bare `:root` light
      palette, `prefers-color-scheme` dark guarded against an explicit light
      choice, explicit `[data-theme="dark"]`) **or** one committed look painted
      explicitly — background and colours never left transparent. `[H]`
- [ ] A **print stylesheet** for document-shaped artefacts. `[V]` (atlas ToC
      checklist)
- [ ] `prefers-reduced-motion` honoured wherever anything animates. `[H]`

## 5. Self-containment and robustness

- [ ] **Offline artefacts stay offline.** No CDN, no webfont, no image fetch,
      no network call. **This outranks everything in section 4** — a prettier
      typeface is never worth a file that fails to open from a NAS share with
      the network down. `[V]`
- [ ] `noscript` completeness where the artefact's contract requires it: the
      content reads in full with scripting off, and the script only filters.
      Check by reading the source, not by running it. `[V]` (atlas ToC rule)
- [ ] Graceful failure where scripted: a `window.onerror` banner class, so a
      file that throws says so instead of rendering blank. `[V]`

## 6. Truthfulness

- [ ] Every visual element traces to real data — a mined source or an explicit
      user answer. `[V]` (atlas Phase-1 hard rule)
- [ ] Unknowns are **marked** (`?`, `status: unknown`), never invented and
      never silently dropped. `[V]`
- [ ] Captions state what the reader is seeing **and where it came from**. `[H]`

---

## Applying the bar

**Fix the data and the markup — do not fight the artefact's own contract.** If
meeting an item here would break a hard rule the artefact already owns
(self-containment, a frozen layout, a fixed palette assigned by position), the
artefact's rule wins and the item is recorded as an accepted exception in the
keyring, not forced through.

**Idempotence is the test.** Re-running the Keymaker visual pass over an
artefact that already meets the bar must change **zero bytes**. A pass that
rewrites a passing file is a bug in the pass, not an improvement to the file.
