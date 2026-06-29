# project-lifecycle — Handover Update Cadence (shared)

> Shared spec for the handover-update frequency the user picks at kickoff.
> Loaded by `project-lifecycle` Sub-K (kickoff) and referenced by Sub-D
> (close). Defaults are evidence-grounded; the user can override.

---

## Why cadence matters

The handover note is the **only** artefact that survives between sessions.
Update too rarely → next session has stale context and re-derives work.
Update too often → cognitive overhead kills throughput.

The research below gives the user six defensible defaults plus a custom slot.

---

## Frequency options

| Option | Trigger | Best for | Evidence basis |
|---|---|---|---|
| `per-action` | After every named task or file write | Short, high-stakes sessions (debugging, surgical edits) | Cepeda et al. 2008 — minimal-interval spacing maximises retention for short-retention contexts |
| `ultradian` | Every ~90 min of active work | Long, focused, single-sit sessions | Kleitman / Rossi — ultradian 90-min rhythm; the 15-20 min trough at cycle end is the natural review window |
| `end-of-session` **(default)** | At session close | Most projects | Amabile & Kramer 2011 (Progress Principle, 12k diary entries from 238 workers) — daily end-of-day journaling produced the strongest inner-work-life signal |
| `daily` | Once per calendar day if session spans days | Multi-day or multi-week work | Ebbinghaus / Cepeda 1-day spacing — durable consolidation for medium-retention |
| `milestone` | At explicit user-defined milestones | Project-managed work with clear gates | User-controlled spacing; no neuroscience prescription |
| `custom` | User-defined (minutes, action count, or trigger phrase) | Anything the table above doesn't cover | Power-user fallback |

### Recommended default

`end-of-session` for projects that span more than one chat. `ultradian` for
long single-sit sessions (>2 hours uninterrupted). `per-action` only when
operator correction cost is so high that re-derivation must never happen
(critical-systems work, regulated edits).

---

## Kickoff dialogue (v1.2.1 — silent default, no menu)

After confirming scope (Sub-K step 1), **default silently to `end-of-session`** and surface a single one-line invitation in the kickoff report:

```
**Update cadence:** end-of-session (default — say "use ultradian", "per-action", "daily", "milestone", or "custom: <spec>" to override).
```

**Do not present a 6-option menu.** The kickoff path must stay fast. Users who want a different cadence will say so; users who don't, get the evidence-best default (Amabile 2011).

Record the chosen (or default) cadence in §9 Update Cadence of the handover note.

### Mid-project override

If the user later says "switch to X cadence" or "update X cadence", change §9 and apply X from the next trigger. Do not back-fill.

### Council finding (v1.2.1, ROUTE-A run on the v1.2 morph)

The original v1.2 kickoff menu was reversed by the council on friction grounds (FM-L2-01). The full options table below is retained for reference and override; it is NOT presented at kickoff.

---

## Honouring the cadence

When the cadence trigger fires (per-action / ultradian / etc.), execute the
**Handover Update + Telemetry Note** sequence from `lifecycle_close.md`
steps 3-7 (NOT step 8 — do not pop up the action menu mid-session unless
the user is at session close). Specifically:

1. Run housekeeping (Sub-C audit + delete obsolete) — see `lifecycle_close.md`
2. Update the handover note's §3, §4, §4a/4b (inputs/outputs), §7
3. Refresh the artefacts-index file — see `lifecycle_artefacts.md`
4. **Append** a new timestamped entry to `Outputs/_telemetry/log.md` — see `lifecycle_artefacts.md` §4 (single append-only file)
5. Do not interrupt the user unless a failure surfaces

For `end-of-session` cadence, the trigger fires once at close; steps 1-5
collapse into the close protocol.

---

## Changing cadence mid-project

If the user says "switch to X cadence" mid-project, update §9 of the
handover note and apply X starting at the next trigger. Do not back-fill.

---

## Sources

- Amabile, T. & Kramer, S. (2011). *The Progress Principle*. Harvard Business Review Press.
- Cepeda, N. J., Vul, E., Rohrer, D., Wixted, J. T., & Pashler, H. (2008). Spacing Effects in Learning. *Psychological Science*, 19(11), 1095-1102.
- Kleitman, N. (1963). *Sleep and Wakefulness*. University of Chicago Press.
- Rossi, E. (1991). *The 20-Minute Break: Reduce Stress, Maximize Performance*. Tarcher.
- Ebbinghaus, H. (1885). *Memory: A Contribution to Experimental Psychology*.

`[UNVERIFIED]` — productivity-percentage claims floating around the web
("40% higher productivity from 90-min cycles") trace to second-hand summaries
of Journal of Cognition coverage and have not been independently verified
here. The frequency-options table is grounded in the named primary sources;
the productivity numbers are not load-bearing for the recommendation.
