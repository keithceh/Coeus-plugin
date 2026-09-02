# Atlas Design Rules — ranked, evidence-graded

> Doctrine file for `skills/atlas/`. Fifteen rules, ranked by evidence strength.
> The SKILL.md protocol and `template.html` both implement this file; when they
> disagree, this file is authoritative and the other two are the defect.
> Research pass: 2026-Sep-01.

---

## Verification caveat (read before citing anything here)

Full-text retrieval of scholarly domains was blocked by session egress policy.
**Every citation and number below was verified against search-result metadata and
abstract snippets retrieved in that session, not against full text.** Markers:

| Marker | Meaning |
|---|---|
| `[V]` | Citation **and** finding both appeared in retrieved results |
| `[V-cite]` | Citation confirmed; finding from an abstract snippet only |
| `[U]` | Unverified lead — do not rely on it |

Where sources disagree on effect size, **plan with the lower figure** (Mayer
handbook medians run d = 0.86–1.10; independent meta-analyses run g = 0.32–0.74).
Never cite a number from this file as full-text-verified.

---

## Tier 1 — strong (multiple meta-analyses / large replicated effects)

**R1 — Spatial contiguity.** Every label, date, and status sits *inside or
touching* the element it describes. No legends, no footnote keys, no
colour-swatch table. The best-evidenced lever in the whole file.
Ginns 2006, *Learning & Instruction* 16(6): d = 0.85 [0.68, 1.02], 50 studies,
larger for complex material `[V]`. Mayer & Fiorella, *Cambridge Handbook* ch.12:
22/22 tests, median d = 1.10 `[V]`. Noetel et al. 2022, *Review of Educational
Research* 92(3): meta-meta, 29 reviews / 1,189 studies `[V]`. 2025 *RER*
meta-analysis: contiguity g = 0.74 `[V, authors U]`.

**R2 — Coherence.** Delete anything that does not serve the reader's purpose: no
decoration, no unactioned metrics, no boilerplate sections kept "for
completeness". Mayer & Fiorella: 23/23 tests, median d = 0.86 `[V]`; seductive
details g = −0.37 to −0.41 — added interest material is *actively harmful* `[V]`.

**R3 — Labeled node-link structure, verbs on edges.** A graph of labeled
relations beats linear prose; a bare arrow carries no proposition. Nesbit &
Adesope 2006, *RER* 76(3): ≈ 0.4 SD, 55 studies, N = 5,818 `[V]`. Schroeder et
al. 2018, *Educational Psychology Review* 30(2): g = 0.58 overall — constructing
g = 0.72 > studying g = 0.43, 142 effects, N = 11,814 `[V]`. Novak & Gowin 1984
labeled-proposition tradition `[V-cite]`. **Caveat:** populations are
educational; transfer to professional onboarding is plausible but unmeasured.

**R4 — History as causal narrative, not a dated event list.** Each beat carries
what → why → outcome. Bower & Clark 1969, *Psychonomic Science* 14: delayed
recall median 93% (narrative) vs 13% (control) at equal study time `[V]`. Mar et
al. 2021, *Psychonomic Bulletin & Review* 28: >75 samples, >33,000 participants,
robust and unmoderated `[V; pooled effect size unverified]`. **Caveat:** those
studies compared prose narratives against essays; compression into diagram-scale
beat labels is untested. The causal-connectivity mechanism plausibly transfers —
that is an inference, not a citation.

**R5 — Exactly four top-level regions; hard cap 7. Chunk by the reader's mental
model** (purpose / lifecycle / ownership), never alphabetically or by file path.
Cowan 2001, *Behavioral and Brain Sciences* 24(1): capacity ≈ 4 chunks, range
3–5 `[V]`. Miller 1956, *Psychological Review* 63(2): 7 ± 2 ceiling `[V]`. Chase
& Simon 1973, *Cognitive Psychology* 4: chunking collapses when structure is
unrecognisable (the random-board result) — a grouping the reader does not
recognise buys nothing `[V]`.

**R6 — Minimise edge crossings above every other layout aesthetic.** If the map
becomes a hairball, **regroup — do not route**. Purchase 1997, *Graph Drawing
'97*, LNCS 1353: crossings dominate comprehension; bends and symmetry matter
less; minimum-angle and orthogonality were not significant `[V]`. Contested at
very large scale: GD 2014, "Are crossings important for drawing large graphs?"
`[V title/venue; findings U]`.

**R7 — Proximity and enclosure do the grouping; whitespace is semantic.**
Wagemans et al. 2012, *Psychological Bulletin* century review `[V-cite]`.
Proximity saturates grouping — adding connectedness on top of it buys nothing;
similarity alone is slow and weak `[V, exact study U]`. Connectedness, common
region, and proximity all aid visual working memory `[V-cite]`. Palmer & Rock,
uniform connectedness `[title V; venue/year U]`.

## Tier 2 — moderate

**R8 — Signal at most three things** (current focus, hard constraint, active
branch), and make the signalling collapsible for repeat readers. Richter,
Scheiter & Eitel 2016, *Educational Research Review* 17: r = 0.17 [.11, .22], 27
studies, N = 2,464; prior knowledge moderates — newcomers benefit most `[V]`.
Expertise-reversal meta-analysis 2025, *Learning & Instruction*: 176 effects, 60
studies, N = 5,924, robust and asymmetric `[V; authors U]`; Kalyuga 2007 `[V-cite]`.

**R9 — Segment into bounded, titled sections.** Segmenting d = 0.70 (handbook) /
g ≈ 0.32–0.36 (independent meta-analyses) `[V]` — **plan with the lower figure.**

**R10 — At most 5 categorical hues (hard cap 7); never colour-only encoding.**
Every colour-coded distinction carries a redundant shape or border, so the atlas
survives monochrome printing and colour-vision deficiency. Healey 1996, *IEEE
Visualization '96*: only 5–7 colours are found rapidly and accurately, 38
observers `[V; a '95-vs-'96 source discrepancy is unresolved]`. Treisman & Gelade
1980, *Cognitive Psychology* 12: feature search parallel, conjunction search
serial `[V]`. Christ 1975, *Human Factors* 17: 42 studies — colour helps *or
hurts* depending on condition `[V]`. The "~12 categorical colours" figure often
attributed to Ware is folklore `[U]`.

**R11 — Only colour-code distinctions that exist outside the artifact.** Status
(active / superseded / draft / unknown) qualifies — it is recorded in the
artefacts index. An invented colour taxonomy does not. Skulmowski 2021/22,
*Education and Information Technologies*: guidance reversal — colour cues present
at learning but absent at test produced the **worst** retention and transfer `[V]`.

**R12 — Freeze the layout.** Regions never move between versions; node order and
group assignment are inherited from the prior `atlas.json`; new nodes append
inside their group and the atlas grows in place. Larkin & Simon 1987, *Cognitive
Science* 11: locational indexing — diagrams make implicit information explicit and
cheapen search `[V]`. Robertson et al. 1998, Data Mountain, *UIST '98* `[V]`.
Scarr et al. 2012, CommandMaps, *CHI '12*: a stable spatial layout is
significantly faster for **experienced** users, no benefit to novices, and is
preferred `[V]`.

**R13 — One fixed re-entry region** (where work stopped, what is open, what is
next), always in the same place. Altmann & Trafton 2002, *Cognitive Science* 26:
memory-for-goals — suspended goals are retrieved through priming cues `[V]`.
Parnin & Rugaber 2011, *Software Quality Journal*: 10,000 sessions across 86
programmers — only 10% resume in under a minute, 93% navigate elsewhere first,
and developers improvise their own notes `[V]`.

## Tier 3 — weak, small, or convention (abandon these first under conflict)

**R14 — Short orienting statement; do not over-invest.** One or two sentences in
the header strip, then stop. Luiten, Ames & Ackerson 1980, *AERJ* 17(2): advance
organizers d = 0.21 learning / 0.26 retention — real but small; several
high-effect studies contradicted Ausubel's proposed mechanism `[V]`. Ernst &
Robillard 2023, *Empirical Software Engineering* 28(5) (arXiv:2305.17286): 65
newcomers answering architecture questions, essays vs structured documents — **no
significant format effect** `[V]`.

**R15 — Always-visible-and-expandable beats hidden-by-default.** Detail is
summarised in place and expands on click; content that matters is never fully
hidden. Disclosure loses to contiguity and coherence whenever they conflict.
Always provide search and jump-to-node. Shneiderman 1996 mantra is a taxonomy,
not an experiment `[V]` — its *relate* and *history* terms serve this artifact
most directly. Cockburn, Karlson & Bederson 2008, *ACM Computing Surveys* 41(1)
`[V]`. Hornbæk & Frøkjær: overview+detail produced better essays but slower work
`[V finding; exact citation U]`. van Ham & Perer 2009, *IEEE TVCG* 15(6):
overviews are often impractical — search first `[V]`. Progressive-disclosure
evidence is thin: Carroll & Carrithers 1984 training wheels was limited, and
Carroll & Rosson 1997 is reported as finding no general empirical support
`[V-cite via secondary]`.

---

## Mandatory uncertainty flags

These stay attached to the doctrine. Removing one is a doctrine change, not an
edit.

1. **Dual-coding mechanism is contested.** Higdon, Neath, Surprenant & Ensor
   2025, *QJEP* 78(1): picture superiority was eliminated when compared against
   visually **distinctive** words; the aphantasia finding points the same way
   `[V]`. The picture-superiority *effect* still stands. Justify text-plus-image
   through **search cost** (Larkin & Simon) and **distinctiveness**, never
   through two-channel theory.
2. **Method of loci does not transfer to diagram semantics.** The loci evidence
   (Twomey & Kroneisen 2021, *QJEP*, g = 0.65, 13 RCTs; Ondřej et al. 2025,
   *BJP*, d = 0.88) is for **ordered lists** `[V for the loci effects]`; no
   primary evidence of transfer to diagram meaning was found `[transfer claim
   unsupported]`. R12 is justified by spatial constancy and locational indexing —
   never call the atlas a memory palace.
3. **C4 model is convention, not a validated finding.** Targeted search returned
   no human-comprehension evaluation of it.
4. **"Big picture first" is a small effect** (d ≈ 0.21–0.26), and the one direct
   domain test was null (Ernst & Robillard 2023). State this honestly: the atlas
   is a bet on **mechanisms** — contiguity, labeled relations, spatial constancy
   — not on diagram format per se.
5. **Chartjunk vs memorability tension.** Bateman et al., *CHI 2010*: embellished
   charts were recalled better after 2–3 weeks and described no less accurately
   `[V]`. Borkin et al. 2013, *IEEE TVCG* 19(12), and 2015 "Beyond Memorability":
   titles and text carry the message, and redundancy helps `[V]`. Reconciliation
   (inference, not published): **coherence governs content** — cut what does not
   serve; **memorability work governs rendering** — distinctive treatment of the
   content you kept is fine.
6. **No learning-styles variants.** Do not build "visual learner" / "text
   learner" versions. Pashler, McDaniel, Rohrer & Bjork 2008, *PSPI* 9(3): the
   meshing hypothesis lacks evidence `[V]`.
7. **No spaced-repetition or quizzing machinery.** The spacing literature
   (Cepeda et al. 2006, *Psychological Bulletin*: 839 assessments — optimal
   interval scales with retention interval) concerns **fixed corpora**; project
   content changes under the reader. The legitimate narrow transfer: stable parts
   in fixed positions are reinforced on every re-visit, and volatile parts are
   quarantined in a marked region (NOW). The optional collapsed
   recall-before-reveal prompt in NOW rests on Rowland 2014 (recall > recognition)
   `[V-cite; pooled effect size unverified]` and **must be labeled an
   extrapolation** wherever it is offered.

---

## Provenance of borrowed patterns

The atlas is not novel in its parts. What each pattern was taken from, and what
was deliberately left behind:

| Pattern | Borrowed from | Note |
|---|---|---|
| Typed JSON intermediate → validation gate → one portable HTML file | **archify** (tt-a1i/archify) | Same extract-then-render split the house `dug_binary` pipeline already uses |
| "Truthful interaction" — refuse to invent topology; curated grouping instead of force-directed physics | **archify** | Becomes the Phase-1 hard rule and the deterministic layered layout in `template.html` |
| Delta / before-after receipts on refresh | **archify** (Architecture Delta) | Becomes `delta: new\|changed` markers |
| Expandable card detail levels; superseded/stale status; provenance chips | **thoughtdag** (chenxiachan/thoughtdag) | Semantic-zoom tiers adapted to R15 (summarised-and-expandable, never hidden). Its manual-workbench model and React Flow dependency were not borrowed |
| Deterministic facts first, semantic summary second; incremental refresh touching only what changed; layer colour-coding | **Understand-Anything** (Egonex-AI) | Colour-coding held to R10's ≤5 hues. Its 7-agent pipeline and dashboard build were not borrowed |
| Stable spatial hierarchy as the organizing metaphor; session transcripts as a minable source for Story | **mempalace** (MemPalace/mempalace) | Justified via spatial constancy (R12), **not** memory-palace claims. Its benchmark and popularity claims are credibly challenged in a public audit — do not cite them; the design idea stands on its own |

Convergent conclusion from all four: each built its own renderer rather than
leaning on a diagram library, and none ships a static-markdown deliverable. A
single self-contained interactive HTML file is the only format that satisfies
offline/NAS operation, zero install, any-project generality, interactivity, and
Coeus's house rules at once.

---

## Review Checklist (Phase 3 runs this inline)

Content and encoding:

- [ ] Every edge in `map.edges` carries a `verb`. No bare arrows.
- [ ] ≤ 5 non-null hues in `layout.hues` (hard cap 7); no two groups share a hue;
      a sixth group is neutral (`"hue": null`), not a duplicate. Every
      colour-coded distinction also carries a shape or border difference (R10).
- [ ] `delta` markers appear only on a refresh, never on a first build.
- [ ] Colour encodes only externally-real distinctions — status, group — never an
      invented taxonomy (R11).
- [ ] No legend, no footnote key, no swatch table; every label sits on its
      element (R1).
- [ ] Nothing decorative, no unactioned metric, no boilerplate section (R2).
- [ ] Every guardrail has an `origin_beat` that resolves to a real beat id, and
      the badge links to it (R4, R1).
- [ ] Story beats read what → why → outcome. A bare dated list fails (R4).
- [ ] Forks render as branches, not as separate lists.
- [ ] Groups follow the reader's mental model, not alphabetical or path order (R5).
- [ ] At most three signalled items (R8).

Structure and stability:

- [ ] Four regions present, canonical order FRAME · NOW · MAP · STORY (R5, R12).
- [ ] On refresh: `layout.node_order` and `layout.group_order` inherited
      verbatim; new nodes appended within their group; `delta` set on everything
      that moved (R12).
- [ ] `now` rewritten in full this run (R13).
- [ ] Header intent is one or two sentences (R14).
- [ ] Detail summarised and expandable; nothing that matters is hidden by
      default; search present and working at ≥ 2 characters (R15).

Truthfulness and containment:

- [ ] Every node, edge, and beat traces to an entry in `meta.sources[]` or an
      explicit user answer.
- [ ] Unknowns render as marked `?` placeholders with `status: unknown` — none
      guessed, none silently dropped.
- [ ] `grep -n "http" Outputs/atlas.html` returns hits only inside the embedded
      JSON data, comments, or the SVG namespace constant the shell needs for
      `createElementNS` (`.../2000/svg`) — never a fetched resource.
- [ ] Zero `<script src`, zero `<link href`. The only `url(` values are
      same-document fragments (`url(#arrow)`), never a network target.
- [ ] `<noscript>` notice and `window.onerror` banner present after injection.
- [ ] The file opens and renders with the network disconnected.
- [ ] It actually renders: the `window.onerror` banner is not showing, node and
      edge counts match `atlas.json`, and search responds at 2 characters. Both
      checks above pass on a file that throws on load — this one does not.

---

## Evolution

Learnings live **outside the repo** at `~/.coeus/atlas/learnings.md`. Append one
line per lesson, patterns only — never project content, never a node label from a
user's project.

Line format:

```
YYYY-MM-DD | TAG | one-line lesson
```

Tags: `PREF` (a user preference about rendering or grouping) · `SHAPE-<a|b|c|d>`
(a survey-path lesson for that project shape) · `TRIGGER-FP` (fired when it
should not have) · `TRIGGER-MISS` (should have fired and did not) · `RULE`
(a design-rule application the user overrode).

When one lesson repeats **≥ 3 times**, propose folding it into `SKILL.md` or this
file as a normal version-bump commit — a proposal to the user, never a silent
edit. Doctrine (R1–R15 and the uncertainty flags) changes only on new primary
evidence; user preferences adapt rendering defaults, never the doctrine.
