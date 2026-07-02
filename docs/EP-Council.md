# 🛢️ EP-Council

> Adversarial 9-supermajor decision council for E&P operators. Phase-gated workflow that stress-tests every opportunity against documented institutional playbooks, hard failures, and through-cycle economics.

**Version:** v9.3 (current, skill v1.9) | **Triggers:** `/ep-council` · `/coeus:ep-council` · `"board review"` · `"investible"`

---

## What It Does

EP-Council replaces gut-feel capital allocation with a structured, mandatory workflow. It simulates nine supermajor E&P companies — each with distinct institutional memory, failure modes, and primary questions — as an adversarial council that evaluates your opportunity across three red-team rounds before delivering named votes.

It is **not a chatbot**. It is a phase-gated engine. Phases cannot be skipped. The verdict cannot be reached without completing the red team.

---

## Installation

**Option 1 — Download `.skill` file (recommended)**

1. Go to [**Releases**](https://github.com/keithceh/Coeus/releases)
2. Download `ep-council-v9.skill`
3. Open Claude Desktop → **Settings → Skills → Install from file**
4. Select `ep-council-v9.skill`

**Option 2 — Build from source**

```bash
git clone https://github.com/keithceh/Coeus.git
cd Coeus

# macOS / Linux
zip -r ep-council.skill ep-council/

# Windows (PowerShell)
Compress-Archive -Path ep-council\ -DestinationPath ep-council.skill
```

---

## Triggers

| Trigger | Notes |
|---------|-------|
| `/ep-council` | Primary slash command |
| `run the ep council` | Natural language |
| `stress-test this deal` | Deal-first entry |
| `red team this opportunity` | Red-team focus |
| `is this a supermajor trap` | Trap screen entry |
| `premortem this asset` | Premortem-first |
| `through-cycle check` | Stress test shortcut |
| `compare these opportunities` | Multi-opportunity mode |

**Auto-trigger:** Describing any E&P opportunity — block, well, acquisition, farm-in, JV, FLNG, divestment, or strategic pivot — activates EP-Council automatically.

---

## The Pipeline

```
[Strategy Document / 12 Questions]
           │
     Phase 0: Strategy Brief Lock
     ─ 7 dimensions: geography, asset type, capital,
       returns, portfolio philosophy, financing, constraints
           │
     Phase 1: Opportunity Intake + Strategy Fit Check
     ─ 6-dimension fit check against Strategy Brief
     ─ T0 Strategic Drift fires if any dimension contradicts
           │
     Phase 1.5: Enforcer Selection
     ─ Opportunity-tailored recommendation first
     ─ Full 9-option menu always shown
           │
     Phase 2: Strategic Roadmap
     ─ Opportunity summary, decision type, active Enforcer,
       strategy fit results, 3 most dangerous assumptions,
       active Council Traps
     ─ ★ EXPLICIT USER APPROVAL REQUIRED ★
           │
     Phase 3: Tri-Team Red-Team (3 rounds, 3-3-3 per round)
     ─ Blue builds · Red attacks · Green verifies
     ─ Patch ratings: STRONG / PARTIAL / WEAK
     ─ Weak patches trigger mandatory re-attack
     ─ Green runs Council Trap Screen (T0–T12) after every round
     ─ Through-Cycle Stress Test mandatory in Green faction
           │
     Phase 3.5: Council Verdict
     ─ 9 named votes: PROCEED / MODIFY / REJECT
     ─ 5-4 → SPLIT COUNCIL
     ─ 6-3 → CONTESTED (minority dissent documented)
     ─ Contradicts Strategy Brief → STRATEGIC OVERRIDE
           │
     Phase 4: EP Premortem
     ─ Failure scenarios from Decision Type Classifier
     ─ 3-4 scenarios, root causes, red herrings, black swans
     ─ Ranked SEVERITY × IMPACT
           │
  [EP_Decision_Plan.md + EP_Premortem_Report.md]
```

---

## Tri-Team Faction Allocation

All rounds use a **3-3-3** split.

| Round | 🔵 Blue (Architects) | 🔴 Red (Attackers) | 🟢 Green (Verifiers) |
|-------|---------------------|-------------------|----------------------|
| 1 | 3 members | 3 members | 3 members |
| 2 | 3 members | 3 members | 3 members |
| 3 | 3 members | 3 members | 3 members |

- No member holds the same faction in consecutive rounds
- Blue builds the case
- Red attacks every assumption
- Green verifies, rates patches, runs Council Trap Screen
- The Enforcer names **one specific Strategy Brief risk** per round
- Through-Cycle Stress Test ($30 / $50 / $70 / $90/bbl) is mandatory in Green every round

---

## Output Artifacts

Both delivered as standalone code-fenced Markdown documents.

**`EP_Decision_Plan.md`**
- 9 named council votes with positions and conditions
- Tri-team red-team summary (3 rounds, patch ratings)
- Council Trap Screen results (T0–T12 status)
- Through-Cycle Stress Test outcomes
- Cycle-tested execution plan

**`EP_Premortem_Report.md`**
- Decision-type-specific failure scenarios
- Root cause, red herrings, black swan variant per scenario
- Severity × Impact ranking
- Ranked mitigation framework with named responsible parties

---

## Mid-Session Commands

| Command | What happens |
|---------|-------------|
| `Change Enforcer` | Re-runs Phase 1.5 with current context |
| `Update Strategy Brief` | Amends and re-locks the Strategy Brief |
| `Express Lane` | Quick take — Enforcer + Strategy Brief only, 3 steps |
| `Partial Express Lane` | Preliminary signal without a Strategy Brief |
| `Compare [A] vs [B]` | Side-by-side two opportunities, same Strategy Brief |

---

## Mandatory Flags

| Flag | Meaning |
|------|---------|
| `[SCALE-ADJUST]` | Figure is supermajor-scale; operator equivalent provided |
| `[UNCONFIRMED]` | Not sourced from a well-known public filing — verify before use |

---

## Related Wiki Pages

- [Council Members →](EP-Council-Council-Members)
- [Trap Screen T0–T12 →](EP-Council-Trap-Screen)
- [Step-by-Step Session Walkthrough →](EP-Council-Walkthrough)

---

## Version History

| Version | Key Changes |
|---------|------------|
| **v9.3** (current, skill v1.9) | T12 Peak-Price Entry added (ExxonMobil/XTO; normalized mid-cycle price test — evidence: XTO $41B at gas peak, BHP $20.6B at $120 oil, Berkshire-ConocoPhillips 2008, Shell-BG synergies at $90/bbl closed into $30; source: CrudeTruth "Why Most Oil Acquisitions Destroy Value" + McKinsey >50% failure finding). T9 enhanced with development-capital starvation clause. Shell (BG synergy-strip detail), ExxonMobil (T12) and Occidental (three-variable frame) profiles sharpened. |
| v9.2 (skill v1.8) | Full 9-member research refresh from source-backed dossiers (regulator/court findings, academic research, business press — Exxon-methodology applied to all members). All member profiles rebuilt with Institutional Memory + Canonical Lesson sections. T11 Megaproject Overrun added (Chevron/Gorgon; P90 cost-schedule viability test — evidence: Gorgon +46%, Tengiz FGP +31%, Kashagan ~$116B, Mozambique LNG +$4.5B). T3 enhanced with frontier-stability clause (Mozambique 4.5-yr force majeure). Occidental figures corrected to SEC-anchored values (LTD $23.34B mid-2025; Berkshire ~28.2%). |
| v9.1 (skill v1.7) | T10 Duration Drift added (Shell). |
| **v9** | Occidental Petroleum added as council member #9 — Capital Allocation Redemption Engine. T9 Acquisition Leverage Trap ($30/bbl debt service test). Faction allocation updated to 3-3-3 per round. Leveraged M&A decision type added to Decision Type Classifier. |
| **v8** | Deep 2025–2026 intelligence update across all 8 council members. ONE primary question per member enforced verbatim. `morpheus` + `architect` triggers added. Through-Cycle Stress Test mandatory in Green. Premortem tied to Decision Type Classifier. |
| v7 | Financing posture added as 7th Strategy Brief dimension. VROC defined in Glossary. |
| v6 | Phase 1.5 rebuilt: opportunity-first Enforcer recommendation. Patch rating system. |
| v5 | Multi-Opportunity Comparison mode. Decision Type Classifier added. |
| v4 | T8 Exploration Cost Trap (ENI). ENI satellite architecture established. |
| v3 | Enforcer Recommendation Matrix. T7 Shale Plateau Cliff (ConocoPhillips). |
| v2 | Express Lane mode. Phase 1.5 Enforcer framework. Through-Cycle Stress Test. |
| v1 | 9-member council. 4-phase structure. Council Traps T0–T6. |

Go back to the [Main README](../README.md).

