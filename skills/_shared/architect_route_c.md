# the-architect ROUTE C — Deep Explore Pipeline (shared)

> Shared recipe for the Architect's deep-explore route. Used by `the-architect` ROUTE C (rare path — fires only on `--explore` or when the problem is ambiguous/novel). Load when the user invokes deep-explore.

Use when the problem is ambiguous, novel, or the user wants the council to help
define and scope the problem before any prompt engineering occurs.

---

### Step C1 — Council Explore

Run a **scoped explore session** using LLM-council (Phase 1 + Phase 2 only, no
red-teaming yet):

1. The six models each offer an initial framing of the problem.
2. Key assumptions, definitions, and scope boundaries are surfaced.
3. The council produces a **Problem Definition Document** (not a full plan).
4. Present to the user and confirm the problem definition before proceeding.

**Output:** Confirmed Problem Definition Document.

---

### Step C2 — Prompt-Master (Craft)

Apply prompt-master to the confirmed Problem Definition Document from Step C1.
Same rules as Step A1, but the input is now the council-validated problem definition.

**Output:** Engineered council brief.

---

### Step C3 — Caveman (Compress)

Apply caveman to the engineered brief from Step C2.
Same rules and scope restrictions as Step A2.

**Output:** Compressed council brief.

---

### Step C4 — LLM-Council (Full Run)

Feed the compressed brief into the full 4-phase council pipeline (same as Step A3).

**Mandatory artifacts:** `Final_Plan.md` + `Premortem_Report.md`.
