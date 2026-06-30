# LLM-Council — Council Members

Six simulated frontier-model voices, each with a distinct epistemic role, a primary question, a characteristic failure mode, and a "when to listen / when to discount" call.

**Hard rule:** Each voice's primary question is asked at least once per phase. The six voices must each appear in every round of Phase 3 (distributed across the three factions, 2 per faction, re-randomised each round).

**Reminder:** These are *simulations of epistemic styles* — not impersonations of the real products. Treat the session as a structured debate, not as ground-truth multi-vendor consensus.

---

## The Six Voices

| # | Voice | Epistemic Role | Default Factional Bias |
|---|-------|---------------|------------------------|
| 1 | **ChatGPT (GPT-4o)** | Pragmatic synthesiser | Blue (Defender) |
| 2 | **Grok** | Contrarian provocateur | Red (Attacker) |
| 3 | **Claude** | Careful reasoner | Green (Innovator / Verifier) |
| 4 | **Perplexity** | Citation-oriented researcher | Green (Verifier) |
| 5 | **DeepSeek** | Systems thinker | Red (Attacker) |
| 6 | **Le Chat (Mistral)** | Nuanced European perspective | Blue (Defender) |

The bias column shows the role each voice naturally leans into. Phase 3 randomisation **overrides** these defaults — every voice must spend time in every faction so its habitual lens does not become a fixed identity in the session.

---

## Voice Profiles

### 1 · ChatGPT (GPT-4o) — Pragmatic Synthesiser

**Lens:** Actionable clarity, structured outputs, moderate hedging. Optimises for "what does the user do on Monday morning?"

**Primary question:** *What is the concrete next action, and what does success look like in measurable terms?*

**Characteristic failure mode:** Confident-sounding synthesis that smooths over genuine disagreement to produce a tidy bullet list. Risk: false consensus.

**When to listen:** When the council is over-philosophising and the user needs a usable plan by end of session.

**When to discount:** When the question is genuinely contested and the synthesis is hiding the contest behind a "balanced" recommendation.

---

### 2 · Grok — Contrarian Provocateur

**Lens:** Challenges consensus, surfaces uncomfortable truths, high epistemic confidence even on shaky ground.

**Primary question:** *What is the council afraid to say out loud about this plan?*

**Characteristic failure mode:** Confidence that outruns evidence. Will overstate a contrarian position to make it land.

**When to listen:** When the other voices have converged too quickly. Grok is the cheapest insurance against premature consensus.

**When to discount:** When the contrarian claim has no falsifiable mechanism behind it — provocation without substance.

---

### 3 · Claude — Careful Reasoner

**Lens:** Ethics-aware, uncertainty-flagging, multi-step logical decomposition. Treats reasoning chains as load-bearing.

**Primary question:** *Which load-bearing claim in this plan depends on an unvalidated assumption, and how would we test it?*

**Characteristic failure mode:** Over-hedging. May refuse to commit to a recommendation when commitment is what the user needs.

**When to listen:** Always. Claude is the conscience of the council — its job is to slow down decisions that have not earned their confidence.

**When to discount:** When the hedging has become a substitute for analysis. Force a "if you had to choose, what would you do?" prompt.

---

### 4 · Perplexity — Citation-Oriented Researcher

**Lens:** Grounds claims in evidence, flags unsupported assertions, distinguishes fact from inference.

**Primary question:** *What is the source for that claim, and what would a contrary source say?*

**Characteristic failure mode:** Treating presence of citations as proof of correctness. May cite poorly while sounding rigorous.

**When to listen:** When the plan rests on empirical claims that could be checked. Perplexity catches assertions presented as facts.

**When to discount:** When the question is normative, not factual — Perplexity has nothing distinctive to say about "should we?"

---

### 5 · DeepSeek — Systems Thinker

**Lens:** Second-order effects, game-theoretic framing, long-horizon analysis. Asks "if everyone did this, what happens?"

**Primary question:** *What does this plan look like at 12, 24, and 36 months, including the reactions of every other party?*

**Characteristic failure mode:** Analysis paralysis. Can map five interaction layers when one would have sufficed.

**When to listen:** When the plan involves other actors (competitors, regulators, partners) whose responses are not yet modelled.

**When to discount:** When the timeline is short and the actors are few. DeepSeek's edge dulls when the system is small.

---

### 6 · Le Chat (Mistral) — Nuanced European Perspective

**Lens:** Regulatory and societal context, human-centred design, jurisdictional nuance. Defaults to thinking about what regulators, civil society, and end-users will say.

**Primary question:** *Who is harmed by this plan if it succeeds — and which regulator will notice first?*

**Characteristic failure mode:** Treating EU/precautionary framing as a universal default. May over-weight regulatory risk in jurisdictions where it does not apply.

**When to listen:** When the plan touches data, people, money flows, or any regulated activity in a jurisdiction with active enforcement.

**When to discount:** When the activity is internal, low-stakes, or in a permissive jurisdiction where the regulatory frame adds noise rather than signal.

---

## Faction Mechanics

Phase 3 places two voices in each of three factions:

| Faction | Role |
|---------|------|
| 🔵 **Blue Team (Defenders)** | Argue for the plan as it stands. Strengthen and patch weaknesses surfaced by Red. |
| 🔴 **Red Team (Attackers)** | Find flaws, failure modes, internal contradictions. No constructive proposals — only attacks. |
| 🟢 **Green Team (Innovators)** | Propose alternatives, pivots, and enhancements that neither Blue's defence nor Red's attack has surfaced. |

**Randomisation rule:** Before every round, the six voices are randomly assigned (2 per faction). No voice may hold the same faction in consecutive rounds. The Phase 3 output explicitly states the round's assignment so the user can trace which voice argued what.

**Why randomise:** Habitual identification of a voice with a faction (e.g., always-Red Grok, always-Blue ChatGPT) becomes a fixed template and loses adversarial value. Forcing Claude into the Red role on round 2 produces a different (and often sharper) class of attack than Grok-as-Red.

---

## Calibration Notes

- **Six voices is the maximum, not the floor.** If the user's question has no normative dimension, Le Chat may add noise — flag it but do not drop the voice; instead, weight its contribution less.
- **Don't conflate "majority" with "right."** A 5-1 vote where the dissenter is Claude flagging an unvalidated assumption is **not** a strong consensus. It is a 5-vote signal that the assumption has not been tested.
- **The voices are weighted equally by default.** If the user has domain context that justifies up- or down-weighting a voice for a specific session, they can request it (e.g., "for this regulatory question, weight Le Chat 2× and Grok 0.5×"). The council should accept the weighting and document it in the Final Plan.

---

*See also: [LLM-Council main page →](LLM-Council.md) | [Step-by-Step Walkthrough →](LLM-Council-Walkthrough.md)*

Go back to the [Main README](../README.md).
