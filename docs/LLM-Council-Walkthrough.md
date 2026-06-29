# LLM-Council — Step-by-Step Walkthrough

A complete worked example showing how a full LLM-Council session runs from invocation to final delivery, including the optional Phase 5 production document.

---

## Before You Start

Have ready:
- A clear description of the decision, plan, or strategy you want stress-tested.
- Approximately 20–60 minutes for a full multi-round session (longer if you opt into Phase 5).
- For Phase 5 (optional): Python with `python-docx` installed, or `pandoc` on PATH. If you have neither, the council will deliver the consolidated emoji-free markdown plus a one-line conversion command.

---

## Step 1 — Invoke the Council

Trigger with any of:

```
/coeus:llm-council [your decision or plan]
/council [your decision or plan]
```

Or use natural language:

> *"Run the council on our plan to consolidate four regional data warehouses into a single lakehouse over the next 18 months."*

**What happens next:** the council opens with Phase 1 (Socratic Clarification). The clarifying questions may be minimal if your input is already well-formed.

---

## Step 2 — Phase 1 · Socratic Clarification

The council asks **up to three** decisive clarifying questions:

> 1. *"Is the 18-month horizon a hard board-mandated date, or your internal preference?"*
> 2. *"Are the four warehouses owned or contracted — do we control the migration timing, or do we depend on vendor cooperation?"*
> 3. *"Does 'lakehouse' mean a specific platform (Databricks, Snowflake, Iceberg-on-S3) or is the platform itself in scope?"*

**Your action:** answer the questions, or say "proceed as-is" if you want the council to work with stated assumptions.

> 💡 **Tip:** If your input was already unambiguous, the council short-circuits Phase 1 and goes straight to Phase 2. State your assumptions explicitly to skip this step.

---

## Step 3 — Phase 2 · Strategic Roadmap + Gated Approval

Each of the six voices independently proposes a high-level approach (1–2 paragraphs each). Claude then synthesises:

> **Strategic Roadmap (draft):**
>
> **Primary recommendation:** Phased consolidation onto Iceberg-on-S3, starting with the smallest regional warehouse as a learn-as-we-go pilot in months 1–4, then parallelising the remaining three across months 5–14, with months 15–18 reserved for decommissioning and read-traffic verification.
>
> **Key action steps:** (1) Pilot scope-lock in month 1; (2) Pilot cutover at month 4; (3) Parallel migration tracks for the remaining three warehouses with separate owner per track; (4) Read-traffic shadowing for 30 days before each cutover; (5) Decommissioning gate at month 16.
>
> **Key assumptions:** vendor cooperation on read-only mirrors is achievable; team can hire two specialised engineers by month 2; the 18-month horizon includes a 2-month buffer.
>
> **Top 3 risks:** (a) hidden semantic drift between regional schemas; (b) read-traffic dependencies the team is unaware of; (c) hiring slippage cascading into the parallel-track phase.
>
> ---
>
> **Gate:** Do I have your approval to proceed to Phase 3 (tri-team red-team)?

**Your action:** reply **"Proceed"**, **"Approve"**, or your specific changes. Neutral responses do not pass the gate — the council will repeat the roadmap until you give an explicit yes or no.

---

## Step 4 — Phase 3 · Tri-Team Round-Robin Red-Team

### Round 1

> **Faction assignment (Round 1):**
> 🔵 Blue: ChatGPT, Le Chat
> 🔴 Red: Grok, DeepSeek
> 🟢 Green: Claude, Perplexity

**Red Team attacks:**
- *Grok:* "The 'smallest first' pilot is the wrong shape — small warehouses are small for a reason (low value), so the lessons learned don't generalise. Migrate the **middle** warehouse first."
- *DeepSeek:* "The parallel-track phase assumes the four migrations are independent. In practice, the second-track team will be blocked by lessons from the first track they have not yet documented. This is a hidden serialisation."

**Green Team proposes:**
- *Claude:* "Add an explicit 'lessons log' gate at month 5 that gates the parallel-track start on the pilot having produced a written runbook."
- *Perplexity:* "There is published evidence from large warehouse-consolidation programs (Netflix 2019, Airbnb 2021) showing 12-month projects routinely run 60% over. An 18-month plan is realistically a 24-month plan with a hard deadline pressure."

**Blue Team patches:**
- *ChatGPT:* "Accept Grok's middle-warehouse-first amendment. Accept Claude's lessons-log gate. The Perplexity overrun observation is a board-conversation, not a roadmap change — flag in the Final Plan."
- *Le Chat:* "Add an explicit regulatory checkpoint: each regional warehouse may have residency requirements that differ. If the lakehouse is on US-East S3, we need a per-region legal review before each cutover."

**Round-1 synthesis:** Plan amended — pilot is now the middle-sized warehouse, lessons-log gate at month 5, per-region legal review embedded in each cutover. Perplexity's overrun warning recorded as a roadmap risk, not a roadmap change. Convergence check: factions still divergent on whether the 18-month horizon is realistic. **Run round 2.**

### Round 2

> **Faction assignment (Round 2 — re-randomised, no voice in the same role as round 1):**
> 🔵 Blue: Grok, Perplexity
> 🔴 Red: ChatGPT, Claude
> 🟢 Green: DeepSeek, Le Chat

*(Round 2 proceeds in the same shape — Red attacks the amended plan, Green proposes alternatives, Blue patches. Synthesis at the end.)*

**Round-2 synthesis:** Convergence on the technical roadmap. Remaining divergence: whether to negotiate a 21-month horizon with the board now or attempt 18 months and re-baseline at month 9.

### Round 3 (optional, user decision)

If convergence is strong enough at round 2, the council proposes proceeding to Phase 4. The user accepts, and round 3 is skipped.

---

## Step 5 — Phase 4 · 6-Month Failure Premortem

> "Assume this plan has **already failed catastrophically six months from now**. What went wrong?"

Each voice proposes 2–3 distinct failure scenarios. Scenarios are clustered:

| Cluster | Example Scenarios | Likelihood | Impact | Risk Score |
|---------|-------------------|-----------|--------|------------|
| **Hiring slippage** | The two specialised engineers never get hired; pilot slips 3 months; parallel-track phase starts late | 4/5 | 4/5 | 16 |
| **Hidden semantic drift** | Two warehouses use the same column name for different concepts; data corruption discovered in production | 3/5 | 5/5 | 15 |
| **Read-traffic surprise** | A regulatory team relies on a query the migration team didn't know existed; cutover breaks compliance reporting | 3/5 | 4/5 | 12 |
| **Vendor non-cooperation** | One vendor refuses read-only mirror access without a contractual amendment that takes 4 months | 2/5 | 4/5 | 8 |

**Top-3 mitigations** (baked back into the plan):
1. **Hiring:** Start the engineering hire process in month 0, not month 2. Have one offer accepted before pilot kick-off.
2. **Semantic drift:** Add a 2-week schema-reconciliation phase before each migration track begins, owned by a data steward from the source warehouse.
3. **Read-traffic:** Run 60 days of read-traffic logging on each warehouse **before** any cutover plan is committed. The plan currently assumes 30 days post-amendment — bump to 60 pre-amendment.

---

## Step 6 — Artifacts Delivered

The council now delivers the two mandatory artifacts inline:

```markdown
# Final Plan — Warehouse Consolidation (4→1 Lakehouse, 18 months)
...
## Executive Summary
A 4-to-1 warehouse consolidation onto Iceberg-on-S3, phased over 18 months,
starting with the middle-sized regional warehouse as a pilot in months 1–4,
followed by parallel migration tracks for the remaining three across months 5–14,
with months 15–18 reserved for decommissioning and verification...
```

```markdown
# Premortem Report — Warehouse Consolidation (4→1 Lakehouse, 18 months)
...
## Top 3 Risk Clusters
| Rank | Cluster | Likelihood | Impact | Risk Score |
|---|---|---|---|---|
| 1 | Hiring slippage | 4 | 4 | 16 |
| 2 | Hidden semantic drift | 3 | 5 | 15 |
| 3 | Read-traffic surprise | 3 | 4 | 12 |
...
```

---

## Step 7 — Phase 5 · Production Document (Optional)

After the two artifacts land, the council asks **exactly once**:

> *"Final_Plan.md and Premortem_Report.md are delivered. Do you want a single production-ready Word document (.docx) that consolidates both artifacts, the Strategic Roadmap, and the red-team synthesis — emoji-free and distribution-ready? (yes / no)"*

### If you say **no**

The session ends. The two markdown artifacts above are the final delivery. Copy them into your tracking system, share with stakeholders, or paste into a doc tool yourself.

### If you say **yes**

The council:

1. **Consolidates** all artifacts into a single document with 12 sections (cover page → executive summary → problem statement → strategic roadmap → six-model synthesis → tri-team rounds → final plan → premortem report → ranked mitigation framework → assumptions → decision-gate appendix → glossary).
2. **Substitutes every emoji** with a plain-language equivalent using the canonical table — `🔴` → `[CRITICAL]`, `🟢 Green Team` → `Green Team`, `✅` → `[PASS]`, etc.
3. **Runs a 10-item failable QA checklist:**
   - Zero emojis remain (regex sweep clean)
   - All 12 sections present and in order
   - No `TBD` / placeholder tokens
   - All tables have header + data rows
   - All cross-references resolve
   - Heading levels contiguous
   - Page numbering + document title in footer/header
   - Word count and section count reported
   - Source artifacts match what was delivered in Phase 4
   - Author/owner field matches the session
4. **Generates** the `.docx` via (in preference order) `python-docx` → `pandoc` → fallback (emoji-free markdown + one-line `pandoc` command).
5. **Delivers** with filename, word count, section count, generator tool used, and a confirmation that all 10 QA checks passed.

> ⚠️ **If any QA check fails and cannot be auto-fixed, the council refuses to issue the file** and surfaces the failure to you. A production document with an unresolved bug is worse than no document.

---

## What A Full Session Looks Like (Time-Wise)

| Phase | Typical time |
|-------|--------------|
| Phase 1 — Socratic clarification | 2–10 min (often skipped if input is precise) |
| Phase 2 — Roadmap + gate | 5–10 min, plus your approval time |
| Phase 3 — Red-team (2–3 rounds) | 10–25 min |
| Phase 4 — Premortem | 5–10 min |
| Artifacts inline | included above |
| Phase 5 — Production .docx (optional) | 2–5 min |
| **Total** | **20–60 min** end-to-end |

---

## Common Pitfalls

- **Approving the roadmap with "ok".** "Ok" is not "approve". The gate requires an explicit affirmative — the council will repeat the roadmap until you give one.
- **Asking for round 4+ without reason.** More rounds rarely improve the plan; they usually re-cycle the same arguments. Trust the convergence check.
- **Treating the six voices as ground truth.** They are simulations. The session's value is the *structure* of the debate, not the literal positions attributed to each "model".
- **Skipping Phase 5 because you "can just save the markdown".** True for personal use; if the artifact is going to a board, regulator, or non-technical stakeholder, Phase 5's emoji substitution + QA checklist is the difference between a draft and a deliverable.

---

*See also: [LLM-Council main page →](LLM-Council.md) | [Council Members →](LLM-Council-Members.md)*

Go back to the [Main README](../README.md).
