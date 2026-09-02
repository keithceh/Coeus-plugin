# Seer Rubric — decomposed scoring with cascading penalties

Read by `seer` Phase 4. Scores are 0–10 per sub-dimension, normalized to 0–1 at
dimension level (arithmetic mean of surviving sub-dimensions), record score =
mean of the four dimensions *after* cascades. Cascades exist because a mean over
sub-scores otherwise launders a fatal routing error into a respectable number —
one critical miss must collapse the record.

## Dimensions & sub-dimensions

### 1. Gate (router Step 0)
| Sub | 10 means | 0 means |
|---|---|---|
| outcome | BYPASS/NO ROUTE/PROCEED/CLARIFIER matches oracle | forced a route on a NO-ROUTE case, or routed a named-skill BYPASS |
| discipline | ≤1 clarifier, only on a genuine two-way tie | clarifier loop, or clarifier where the signal was clear |

### 2. Family (router Step 1)
| Sub | 10 means | 0 means |
|---|---|---|
| correctness | family matches oracle | wrong family |
| signal_use | concrete-artefact-wins applied (rule 0) | keyword outweighed artefact |

### 3. Skill (router Step 2 + tie-breakers)
| Sub | 10 means | 0 means |
|---|---|---|
| correctness | skill matches oracle | wrong skill |
| tie_breaker | the governing tie-breaker cited correctly in WHY | tie-breaker ignored or misapplied |
| sequencing | sequential requests: first task launched, next skill named in WHY (rule 9) | both launched, hybrid invented, or handoff dropped |

### 4. Protocol (output contract)
| Sub | 10 means | 0 means |
|---|---|---|
| block | legal FAMILY/ROUTE/WHY/RUN block (or legal gate line) | malformed or missing |
| launch | Skill-tool launch stated for PROCEED | slash command printed as if it fires |
| restraint | no domain logic leaked into the routing response | router did the task instead of routing it |

## Cascading penalties (apply top-down, in order)

1. **Deterministic failure (D1–D4) → record score 0.** No rubric pass. A route
   to a nonexistent skill is not "partially correct".
2. **Gate.outcome wrong → Gate = that sub-score alone; Family, Skill, Protocol
   all score 0.** Nothing downstream of a wrong gate is creditable.
3. **Family.correctness ≤ 2 → Skill and Protocol sub-scores cap at 2.** A
   confident launch of the wrong family's skill is worse than a hesitant one.
4. **Skill.correctness ≤ 2 → Protocol.launch caps at 2.** Launching the wrong
   skill crisply is not protocol credit.
5. Values legitimately inherited from an upstream decision are not re-penalized
   (grade the first cause once, not its echoes).

## Failure taxonomy (label every non-perfect record with exactly one primary)

`gate-forced-route` · `gate-missed-bypass` · `family-keyword-over-artefact` ·
`skill-tiebreaker-miss` · `skill-hallucinated` (D1) · `sequencing-dropped` ·
`clarifier-overuse` · `launch-omitted` · `logic-leak` · `format`

## Report template

```
# Seer Routing Eval — <date>, scope: <scope>, n=<records>
Blindness: <subagent | procedural only — same-context evaluation>
"Generator and judge share one model; agreement is not independent corroboration."

| Family | n | mean | min | perfect | primary failures |
|---|---|---|---|---|---|
(one row per family, then one per tier)

## Failures
(one block per record < 1.0: query, oracle, actual, primary label, sub-scores hit)

## Proposed golden-set rows
(| # | query | expected outcome | rule exercised | — ready to paste; user approves)

## Proposed router edits
(only when a failure traces to a rule gap; quote the rule, state the edit, cite the failing record)
```

## Provenance & the two lessons this design encodes

Protocol adapted from *Agent Seer: Synthesizing Scenarios from Specification
Understanding* (Karumuri, Vemula & Lopes Pegna, Apple, arXiv 2608.26133): a
four-stage spec-only pipeline — interpret specs, synthesize tiered scenarios
with the workflow held out as oracle, mock execution, judge with a decomposed
14-sub-dimension rubric whose cascading penalties surfaced the dominant failure
class (argument value errors) that coarse name-match metrics score as perfect.

Two findings shaped the hard rules in `SKILL.md`:

1. **A judge is blind to constraints outside its context.** An independent
   reproduction (ghchinoy/ai-paper-reproductions) showed the paper's judge
   scoring a real unsupported-parameter bug a perfect 1.000 because the
   constraint lived outside the spec it was shown. Hence Phase 0.2
   (constraints-in-context) and the deterministic-checks-first rule: a
   machine-checkable constraint is never entrusted to judgment.
2. **Same-model agreement is not corroboration.** The paper's own judge-swap
   replication (Gemini vs Qwen) held for tool-calling but broke for coherence
   (34% agreement within ±0.1). Seer's generator and judge are the same model
   in the same context — strictly weaker — so the disclaimer line is mandatory
   and the report must never present its own agreement as external validation.
