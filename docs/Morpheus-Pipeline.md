# Morpheus Pipeline — Engineer, Compress, Execute

> A two-stage prompt engineering and compression pipeline. Takes a raw user request or rough prompt draft and produces a precision-engineered, caveman-compressed prompt ready to paste into any AI system — and, by default, runs it immediately if the target is the current session.

**Version:** 1.2.0 (current) | **Triggers:** `/morpheus` · `/morph` · `"morph this"` · `"morph it"` · `"engineer this prompt"` · `"optimise this prompt"` · `"make this prompt better"` · `"refine my prompt for [model]"` · `"compress this prompt"`

---

## What This Is

Morpheus chains two skills:

```
prompt-master  →  caveman
   (craft)          (compress)
```

`prompt-master` is vendored from [nidhinjs/prompt-master](https://github.com/nidhinjs/prompt-master) and transforms a raw idea into a precision-engineered prompt tuned to the target AI tool (Claude, ChatGPT/GPT-4o, o3/o1, Gemini, Claude Code, image-AI tools each get different guidance in Morpheus's own Step 1 routing table). `caveman` is vendored from [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) and strips filler, articles, and verbose phrasing from the *prompt itself* for token efficiency. Both are tracked upstream: Coeus fetches and normalizes them on a weekly sync workflow and again at release time (a `sed` step re-pins the `name:`/`argument-hint:` frontmatter so slash commands keep resolving after each sync), so Morpheus's own SKILL.md is the only Coeus-owned surface for this pair — the vendored files themselves are not hand-edited.

---

## AUTO vs REVIEW Mode

Default behaviour is **auto-execute** (v1.2.0): engineer, compress, and run the prompt in one pass. A user can opt into a review gate by phrasing at invocation time — "review first", "let me review", "show me the prompt before running", "check before run", or `--review` — which sets **REVIEW mode**: Morpheus runs Steps 1–2, delivers the output block, and stops with `Review mode: reply "run" to execute, or edit the prompt and resend.` It executes only on an explicit go-ahead.

Morpheus never asks "which mode do you want?" — AUTO is the default, and REVIEW is opt-in by phrasing, never by questionnaire. The active mode is stated in one word (`Mode: AUTO` or `Mode: REVIEW`) at the top of the output block.

---

## Pre-Flight Checks

All three run before the pipeline begins; any failure surfaces to the user and pauses.

1. **Architect Escalation Detector.** Does the request involve a complex, multi-step decision, plan, or strategy that would benefit from adversarial red-teaming and a formal premortem? If yes, Morpheus recommends escalating to [The Architect](The-Architect.md) instead, explains why, and asks for confirmation before proceeding with Morpheus anyway.
2. **Narrow Scope Detector.** Is the input already a well-formed, specific prompt with a clear target model and output format? If yes, Morpheus skips prompt-master's full structuring phase and goes straight to targeted refinement + compression, flagging that the prompt was already well-formed.
3. **Vague Input Detector.** Is the input too vague to produce a useful prompt without clarification (e.g. "make a prompt", "write something good")? If yes, Morpheus asks 1–2 targeted clarifying questions rather than guessing intent.

---

## Step 1 — Prompt-Master (Craft)

Transforms the raw input into a precision-engineered prompt for the identified or inferred target model, applying model-specific practices (XML tags and explicit persona framing for Claude; markdown structure and few-shot examples for GPT-4o; concise, format-specified prompts for o3/o1; explicit task decomposition for Gemini; CLAUDE.md-style scope boundaries for Claude Code; style/subject/composition/lighting/mood for image AI). Hard rules inherited into this step: never fabricate capabilities, always include an output-format specification, always include uncertainty-handling instructions, state the target model explicitly, and keep any persona generic — never a named real person.

If all pre-flight checks pass without flags, Step 1 output is folded silently into the Final Delivery block rather than shown standalone; it is shown as its own block only when a gate fired (a narrow-scope flag, an escalation recommendation, or a pause condition).

## Step 2 — Caveman (Compress)

**Scope rule — critical and absolute:** caveman compresses the PROMPT only. It must never touch the user's original deliverables or content, artifacts such as `Final_Plan.md` / `Premortem_Report.md`, structured data or code the user wants preserved, or any output the user intends to use as-is rather than as a prompt. If the input is itself a deliverable rather than a prompt, Morpheus does not compress it — it flags that caveman only applies to prompts and asks for confirmation.

Compression rules: strip articles where meaning survives; remove filler ("please", "could you", "I would like you to"); collapse verbose multi-sentence instructions into terse equivalents; but always preserve precision, format markers (XML tags, markdown headers), and uncertainty-handling instructions. The upstream caveman contract also applies to the compressed prompt itself: standard acronyms (DB/API/HTTP) are fine, but never invent abbreviations (cfg/impl/fn) and never use causal arrows (X → Y) — the tokenizer splits both the same as full words, so nothing is saved and decoding gets harder.

Compression is skipped (Step 1's prompt returned unchanged, with the reason stated) when the prompt is already under 150 tokens, the target model is o3/o1 (which benefit from concision already and can lose reasoning quality under further compression), or the user has said "don't compress" / "keep it verbose".

## Step 3 — Auto-Execute

When all pre-flight checks passed cleanly, no pause condition fired, prompt-master needed no clarification, caveman either compressed successfully or was validly auto-disabled, and the target model is the **current runtime** (Claude / Claude Code), Morpheus runs the compressed prompt immediately in the same conversation: it presents the Morpheus Output block, adds the marker `**Executing compressed prompt now…**`, executes the prompt as the user's effective request, and delivers the result directly below.

Auto-execution is skipped — delivering only the engineered/compressed prompt for the user to paste elsewhere — if REVIEW mode is active, the target model is not Claude/Claude Code, the user said "just give me the prompt" / "don't run it" / "deliver only", the engineered output is a reusable template rather than an immediate task, or a pause condition fired earlier. Morpheus states the reason in one line when Step 3 is skipped.

---

## Pipeline Pause Conditions

Morpheus pauses and surfaces to the user if the input contains sensitive personal data (PII, credentials, financial details), the target model is one Morpheus cannot reliably engineer for, or it's ambiguous whether the input is a prompt or a deliverable.

---

## The Vendoring / Weekly-Sync Arrangement

`prompt-master` and `caveman` are the two skills Coeus tracks from upstream rather than authoring itself. A weekly sync workflow (and a release-time fetch) pulls the current upstream `main` for each, and a normalization step re-pins the Coeus-required `name:`/`argument-hint:` frontmatter fields so folder names keep matching and slash commands keep resolving after each sync — otherwise an upstream rename (e.g. caveman's own `name: caveman-protocol`) would silently break `/coeus:caveman`. Coeus-owned additions that sit on top of the vendored contract are documented, not merged in: the prompt-only scope rule, preserve-format-markers / uncertainty-instructions / output-format-spec rules, the auto-disable conditions (sub-150-token prompts, o3/o1 targets), and the artifacts-never-compressed guardrail. When upstream caveman changed its own token-saving stance (banning invented abbreviations and causal arrows, having measured zero token saving under the tokenizer plus added decode cost), Morpheus's Step 2 rules were updated to match — the wrapper docs are the only Coeus-owned surface for this pair; `skills/caveman/SKILL.md` itself is never hand-edited.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [The Architect →](The-Architect.md) (the escalation target for complex, multi-step decisions Morpheus's Pre-Flight Check 1 detects)
- [Coeus Architecture →](Coeus-Architecture.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.2.0** (current) | 2026-Jul-11 | AUTO/REVIEW mode split: default is AUTO (engineer, compress, execute in one pass); REVIEW is opt-in by phrasing ("review first", `--review`) and stops after delivering the prompt until the user says "run". REVIEW added as a Step-3 auto-disable condition. |
| (no version bump) | 2026-Jul-12 | Upstream caveman contract-alignment audit: Morpheus's own Step-2 Compression Rules gain rule 8, matching caveman's current upstream stance (no invented abbreviations, no causal arrows — measured zero token saving, added decode cost). No change to the vendored `skills/caveman/SKILL.md` itself. |
| 1.1.1 | 2026-Jul-08 | Trigger fix: bare "morph", "morph this", "morph it" added to frontmatter and router — previously only `/morph` matched, so plain-text "morph this" fired nothing. |
| 1.1.0 | prior to 2026-Jul-08 (undated in CHANGELOG.md) | Step 3 auto-execute added: the pipeline runs the compressed prompt immediately when the target is the current runtime, instead of only ever delivering it. |

Go back to the [Main README](../README.md).
