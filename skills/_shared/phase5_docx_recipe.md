# Phase 5 — Production-Ready .docx Recipe (shared)

> Shared, opt-in recipe for consolidating council artifacts into a single distribution-ready Word document. Used by `llm-council`'s Phase 5 (and any downstream skill that chains it). Load this file only when the user has opted into the .docx upgrade.

**Entry condition:** Both `Final_Plan.md` and `Premortem_Report.md` have been delivered to the user.

**Objective:** Produce a single `.docx` that incorporates every artifact, is emoji-free, and has passed pre-delivery QA.

---

## Step 5.1 — Offer the upgrade

After Phase 4 artifacts land, ask the user **exactly once**:

> *"Final_Plan.md and Premortem_Report.md are delivered. Do you want a single production-ready Word document (.docx) that consolidates both artifacts, the Strategic Roadmap, and the red-team synthesis — emoji-free and distribution-ready? (yes / no)"*

If the user replies **no** (or anything other than affirmative) → stop. The two markdown artifacts are the final delivery.

If the user replies **yes** → proceed to Step 5.2.

---

## Step 5.2 — Consolidate

Assemble a single document in this exact section order:

1. **Cover page** — title, date, council session id, presiding chancellor, version line.
2. **Executive Summary** (lifted from `Final_Plan.md`, tightened to 1 paragraph).
3. **Problem Statement** (from Phase 1).
4. **Strategic Roadmap** (approved Phase 2 roadmap with Phase 3 patches folded in).
5. **Six-Model Council Synthesis** (the per-model perspectives + the synthesis table).
6. **Tri-Team Red-Team Rounds** (full per-round Blue/Red/Green output + per-round synthesis).
7. **Final Plan** (full body of `Final_Plan.md` minus the duplicate Executive Summary).
8. **Premortem Report** (full body of `Premortem_Report.md`).
9. **Ranked Mitigation Framework** (severity × impact table).
10. **Assumptions, Open Questions, Epistemic Flags**.
11. **Appendix A — Decision Gates** (which gates were passed, by whom, when).
12. **Appendix B — Glossary** (only if the document uses terms a downstream reader may not know).

---

## Step 5.3 — Emoji substitution pass (mandatory)

Word does not render every Unicode emoji consistently across machines (Calibri fallback, missing colour-emoji fonts on locked-down corporate desktops, Track Changes corruption). Replace **every** emoji with a plain-language substitute before generation. Use this canonical table; extend as needed but never leave a bare emoji.

| Emoji | Substitute |
|---|---|
| 🔴 | `[CRITICAL]` |
| 🟠 | `[HIGH]` |
| 🟡 | `[MEDIUM]` |
| 🟢 | `[LOW]` |
| 🔵 | `[INFO]` |
| ⚪ | `[NEUTRAL]` |
| ✅ | `[PASS]` |
| ❌ | `[FAIL]` |
| ⚠️ | `[WARNING]` |
| 🚨 | `[ALERT]` |
| ✔ | `[YES]` |
| ✖ | `[NO]` |
| ⛔ | `[STOP]` |
| 👑 | `[CHANCELLOR]` |
| 💾 | `[ARTIFACT]` |
| ⚙ | `[SETTINGS]` |
| 🔄 | `[ITERATE]` |
| 🎯 | `[TARGET]` |
| 📌 | `[NOTE]` |
| 📊 | `[METRIC]` |
| 🛡 | `[SAFEGUARD]` |
| 🧠 | `[REASONING]` |
| 🟦 / Blue Team | `Blue Team` |
| 🟥 / Red Team | `Red Team` |
| 🟩 / Green Team | `Green Team` |

After substitution, run a final regex sweep (`[\U0001F300-\U0001FAFF☀-➿️]`) over the consolidated text. **Any hit aborts delivery** — fix and re-sweep.

---

## Step 5.4 — Pre-delivery QA (failable checks)

Before issuing the `.docx`, verify each check. Any failure → fix and re-run the affected step. Do not deliver until all pass.

```
[ ] Zero emojis remain (regex sweep clean)
[ ] All 12 sections present and in order
[ ] No "TBD", "[insert ...]", or placeholder tokens
[ ] All tables have header row + at least one data row (no orphan headers)
[ ] All markdown cross-references resolve (no broken [link](anchor) fragments)
[ ] Heading levels are contiguous (no jump from H1 directly to H4)
[ ] Page numbering present in footer; document title in header
[ ] Total word count and section count reported to the user
[ ] Source artifacts (Final_Plan.md, Premortem_Report.md) match what was delivered in Phase 4
[ ] Author/owner field matches the council session, not the runtime
```

---

## Step 5.5 — Generate the .docx

Generate the Word document via whichever tool is available in the runtime, in this preference order:

1. **`python-docx`** — preferred. Preserves heading hierarchy, tables, page breaks, and TOC field codes natively. Save as `<topic-slug>_Final_Production_v1.docx`.
2. **`pandoc`** — `pandoc consolidated.md -o out.docx --reference-doc=reference.docx --toc --toc-depth=2`. Fast and reliable; requires pandoc on PATH.
3. **Fallback** — if neither tool is available in the runtime, deliver the fully consolidated, emoji-free markdown file (`<slug>_Final_Production_v1.md`) together with the one-line command the user can run locally: `pandoc <file>.md -o <file>.docx --toc`. State clearly that the markdown is delivery-ready and only the binary conversion is deferred.

---

## Step 5.6 — Deliver

Issue **one and only one** file (plus the markdown source if it was used for generation). State:
- File name
- Word count
- Section count
- Generation tool used
- Confirmation that all QA checks passed

If any QA check failed and could not be fixed, do **not** issue the file. Surface the failure to the user and ask for direction.
