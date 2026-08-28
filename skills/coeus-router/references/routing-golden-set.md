# Router Golden Set — labeled routing regression cases

Labeled (query → expected outcome) pairs. Two uses:
1. **Regression checklist** — after any edit to `SKILL.md`, verify each row still routes as labeled.
2. **Few-shot anchor** — the router may consult these when a live request resembles a row.

Format: outcome is `family/skill`, `CLARIFIER(a|b)`, `NO ROUTE`, or `BYPASS`.

| # | Query | Expected outcome | Rule exercised |
|---|---|---|---|
| 1 | "stress-test my market-entry plan" | decision/llm-council | 2a fallback row |
| 2 | "is this Namibia farm-in investible?" | decision/ep-council | E&P wins in decision (rule 1) |
| 3 | "morph this: write me a prompt for Midjourney" | decision/morpheus | "morph" trigger row |
| 4 | "engineer this prompt for o3, no need to shorten it" | decision/prompt-master | rule 3 — no compression |
| 5 | "compress this paragraph, less tokens" | decision/caveman | caveman row |
| 6 | "package my prompt collection as a Claude plugin" | decision/plugin-creator | plugin row |
| 7 | "high-stakes rig-contract decision, and my brief is a mess — engineer it then debate it" | decision/the-architect | rule 2 — prompt needs engineering |
| 8 | "Word says unreadable content in report.docx" | tools/ooxml-repair | 2b row 1 |
| 9 | "figure numbers in chapter 3 are out of order, fix them" | tools/ooxml-fields | verb=fix (rule 4) |
| 10 | "list every figure and table in report.docx to Excel" | tools/docx-inventory | verb=list (rule 4) |
| 11 | "resume the MAE-1R1 project, update the handover" | tools/project-lifecycle | lifecycle row |
| 12 | "list horizons and polygons from project.dugprj" | seismic/dug_binary | 2c row |
| 13 | "rename tag #wip to #active across my vault" | vault/obsidian-vault | 2d row |
| 14 | "audit X:\\Malampaya\\project.dugprj then write the session handover" | seismic/dug_binary, WHY names project-lifecycle next | rule 9 — sequential |
| 15 | "here's report.docx — help me decide whether to submit it" | tools (docx artefact wins) → CLARIFIER only if intent genuinely splits | rule 0 — concrete artefact |
| 16 | "fix the captions… or maybe just list them, not sure" | CLARIFIER(ooxml-fields\|docx-inventory) | rule 10b — two-way tie |
| 17 | "/coeus:ep-council Block 12 farm-in" | BYPASS | Step 0.1 — named skill |
| 18 | "use morpheus on this" | BYPASS | Step 0.1 — named by name |
| 19 | "what's the difference between llm-council and ep-council?" | NO ROUTE (question about Coeus, answer directly) | Step 0.2 |
| 20 | "thanks, that worked" | NO ROUTE | Step 0.2 — conversational |
| 21 | "write me a Python script to parse LAS files" | NO ROUTE (general coding task) | Step 0.2 — out of scope |
| 22 | "asdkj qpwoe zxcv" | NO ROUTE | rule 10c — no signal, never guess |
| 23 | "structure my board memo recommending the Block 12 farm-out" | writing/minto | rule 11 — decision exists, communicate it |
| 24 | "should we farm out Block 12? stress-test it" | decision/ep-council | rule 11 border — decision itself needed, E&P wins (rule 1) |
| 25 | "restructure this report so the answer comes first" | writing/minto | 2e row — answer-first rebuild |
| 26 | "update the handover note for the PERT session" | tools/project-lifecycle | rule 11 border — session docs never minto |
| 27 | "decide the farm-out, then structure the board paper" | decision/ep-council, WHY names minto next | rules 9 + 11 — sequential |

## Maintenance

- Adding a skill? Add at least one positive row and, if it borders an existing skill, one tie-breaker row.
- A row that stops routing as labeled = regression in the SKILL.md edit — fix the rules, not the label (unless the product decision genuinely changed).
