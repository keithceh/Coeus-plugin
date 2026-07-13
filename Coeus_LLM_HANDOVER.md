# Coeus — LLM Handover Note (`Coeus_LLM_Coeus_LLM_HANDOVER.md`)

**For**: any LLM picking up work on this repo.
**Repo**: https://github.com/keithceh/Coeus
**Current version**: 3.17.1 (2026-Jul-11 — coeus-router v1.4.0: Step-0 gate (BYPASS/NO ROUTE/PROCEED), sequential cross-family routing, three-tier confidence fallback, routing golden set at skills/coeus-router/references/routing-golden-set.md — evaluated against RAG-MCP-lineage tool-selection guidance; vector retrieval deliberately skipped at 13 skills, revisit past ~20. Prior: 3.17.0 (2026-Jul-10 — obsidian-vault v1.2: full obsidian-mcp parity verified from the package source (soft delete to `.trash/` + trash_metadata, vault-wide link updating on move + broken-backlink reporting on delete, move hardening, prepend, filename + hierarchical/wildcard tag search, tag semantics — specs in `skills/obsidian-vault/references/OPERATIONS.md`) plus 8 security guardrails from a prompt-injection/path-containment review (`.obsidian/` hard write block, resolved-path containment, regex-escaped link rewriting, live-reply-only consent, `.trash/` writes gated as delete family, wildcard disclosure). Prior: 3.16.0 — new `obsidian-vault` skill: direct Obsidian-vault file operations (read/search/create/edit/tag/move/delete notes) on plain-text vaults incl. NAS/UNC paths, via native file tools or the filesystem MCP server, with per-type confirmation gating for destructive ops; starts the new **vault** router family. coeus-router v1.3.0 adds Step 2d routing to `obsidian-vault`. Prior: 3.15.8 — coeus-router v1.2.0: router must LAUNCH the routed-to skill via the Skill tool, not just print the `RUN →` slash command (printed slash commands are inert); "morph this" added to morpheus triggers + router morpheus row; guru/skill-selector framing. Prior: 3.15.7 — EP-Council ground-truth protocol COMPLETE: all 9 member profiles Perplexity-verified claim-by-claim across v3.15.2–3.15.7; zero `[UNCONFIRMED]` markers remain in the Members doc. Highlights: BP dual ouster (CEO Dec 2025, chair May 2026), Willow remand-without-vacatur nuance, Guyana capacity corrected to ~1 Mb/d-by-2027, OxyChem close 2 Jan 2026, Hollub succession Mar 2026. Prior: 3.15.1 dug_binary patch) — note: the header had drifted to 3.13.0 while v3.14.0 (Seismic Tools v2.0, `dug_projdb` → `dug_binary`) shipped without a header bump; CHANGELOG.md is authoritative for that release
**License**: BSL 1.1 → Apache 2.0 (2028-05-28)
**Archive copy**: a mirror of this file lives at `//192.168.0.119/Big_Data_II/Claude/Archives/Coeus_LLM_Coeus_LLM_HANDOVER.md`. The repo copy is canonical; the archive copy is a snapshot for offline reference.

> **Header maintenance note (2026-Jul-01):** this header and the `## What Coeus is` skill count had drifted — last hand-updated at v3.8.0 while the repo moved through v3.9.x (EP-Council trap additions) and v3.10.x (`dug_projdb` / Seismic Tools family, notification workflows) without a corresponding header bump. Corrected here as part of the LLM-Council v1.2 update. The dated entries below `## Repo layout` still jump from v3.8.x straight to this entry — CHANGELOG.md is the authoritative source for everything shipped in between.

---

## What Coeus is

Coeus is a **Claude Code plugin** that bundles 14 skills for high-stakes EP-industry decision-making, plugin authoring, meta-routing, upstream subsurface data extraction, and (new in v3.16.0) direct Obsidian-vault file operations — the **vault** family:

| Skill | Purpose | Slash command |
|---|---|---|
| `llm-council` | Multi-LLM consensus + adversarial red-team + 6-month premortem + optional Phase-5 consolidated .docx; v1.2 — 7 simulated voices (added Gemini as Structural Verifier), tri-team factions now 3/2/2 | `/coeus:llm-council` |
| `morpheus` | Prompt engineering + caveman compression pipeline | `/coeus:morpheus` |
| `the-architect` | prompt-master → caveman → council (adaptive end-to-end) | `/coeus:the-architect` |
| `ep-council` | 9-supermajor E&P adversarial decision engine; v1.10 — 13 traps (T0–T12), T3 covers home-government policy reversal, Shell carries T4 + T10, Chevron carries T2 + T11, ExxonMobil carries T6 + T12 | `/coeus:ep-council` |
| `caveman` | Caveman-mode compression (tracks `JuliusBrussee/caveman`) | `/coeus:caveman` |
| `prompt-master` | Precision prompt engineering (tracks `nidhinjs/prompt-master`) | `/coeus:prompt-master` |
| `plugin-creator` | Autobot transformer — package an idea/prompt/folder as a spec-compliant Claude plugin | `/coeus:plugin-creator` |
| `ooxml-repair` | Diagnose + repair OOXML schema violations in DOCX (added v3.8.0) | `/coeus:ooxml-repair` |
| `ooxml-fields` | SEQ field + REF field + caption numbering management (added v3.8.0) | `/coeus:ooxml-fields` |
| `docx-inventory` | Extract figure/table inventory from DOCX to xlsx (added v3.8.0) | `/coeus:docx-inventory` |
| `project-lifecycle` | Session resume + handover-doc + file audit (added v3.8.0) | `/coeus:project-lifecycle` |
| `dug_binary` | **Seismic Tools family** — reverse-engineers a DUG Insight `project.dugprj` into user-selected artefacts: multi-sheet xlsx (volumes, horizons, polygons, per-volume process history), per-volume DOCX (full/no-pid), self-contained HTML volume-lineage explorer (added v3.10.0 as `dug_projdb`; renamed + expanded v3.14.0) | `/coeus:dug_binary` |
| `obsidian-vault` | **Vault family** — direct file operations on a plain-text Obsidian vault (read/search/create/edit/tag/move/delete notes) via native tools or `mcp__filesystem__*`; NAS/UNC/mapped-drive paths first-class, no network-drive rejection; per-type confirmation gating for destructive ops (added v3.16.0; v1.2 adds source-verified obsidian-mcp parity — soft delete to `.trash/`, vault-wide link updating on move, tag semantics, specs in `references/OPERATIONS.md` — plus 8 prompt-injection/path-containment guardrails) | `/coeus:obsidian-vault` |
| `coeus-router` | **Tier-3 meta-skill** — the Coeus guru / skill selector: routes the user's intent to the right Coeus skill and launches it via the Skill tool in the same response, no domain logic (v1.4.0 — Step-0 gate, sequential routing, tiered fallback, golden set) | `/coeus:router` |

`morpheus` and `the-architect` depend on `prompt-master` + `caveman`. `ep-council`, `plugin-creator`, `dug_binary`, `obsidian-vault`, and all four Tools skills are standalone.

**Tools bundle** (added v3.8.0): four skills delivered together as one umbrella for long-running DOCX-centric project work — `ooxml-repair`, `ooxml-fields`, `docx-inventory`, `project-lifecycle`. They share a domain and call each other in practice (corrupt-docx workflow chains all three OOXML/inventory skills; multi-session work chains lifecycle with any of the three). Source spec: `C:/Claude/Claude-Work/Projects/Technical_Reports/Outputs/LLM_Handover_Skill_Creation.md`. Reference doc: `docs/Tools.md`. All four passed the full-harness 3-round test (170/170 final round with plugin bundle).

**Release-time normalization (v3.8.0+, ship'd 2026-Jun-26).** `release.yml`'s `Bundle coeus.plugin` step swaps in upstream-fetched `caveman` + `prompt-master`, then runs `python3 scripts/build-plugin.py`. `check_skills()` invariant #3 (frontmatter `name:` must equal dir name) hard-failed because upstream `caveman` ships as `name: caveman-protocol`. Fix: inline `sed` step after the swap that mirrors `sync-upstream-skills.yml` — pins `name:` to the Coeus dir name and re-injects `argument-hint:` if upstream stripped it. The release-time pull now gets the same canonical treatment as the weekly sync. **If you ever add another vendored skill, extend the `for entry in …` loop** in the Bundle step OR rework into a shared shell function — same `name|hint` pair format. Vendored skill list lives in two places: `VENDORED_SKILLS` in `scripts/build-plugin.py` and the loop in `release.yml`'s Bundle step.

**CI runner Python deps (v3.8.0+).** `release.yml` needs `pip install pyyaml` before the bundle step because `build-plugin.py`'s `check_skills()` imports yaml. `test.yml` already had this — release.yml caught up 2026-Jun-26. If you add another `import` to anything `release.yml` or `test.yml` runs, **install it explicitly in the workflow** — `ubuntu-latest` ships a bare Python; do not assume packages are available.

**Action-version cascade.** GitHub deprecates Node runtimes on a rolling schedule. As of 2026-Jun, baseline pins are: `actions/checkout@v5`, `actions/setup-python@v6`. When a deprecation warning surfaces, bump the named action in all four workflow files (`release.yml`, `test.yml`, `sync-upstream-skills.yml`, `update-badge.yml`) in one commit.

**Paste-prompt install (v3.8.0+, web-chat fallback).** claude.ai web chat does not support plugin uploads (Anthropic product design — chat surface has MCPs + built-in tools only, no `Add Plugin`). For web-chat users, `scripts/build-skill-paste.py <skill>` generates a self-contained `dist/coeus-<skill>.paste.md` (12–38 KB) that concatenates the SKILL.md + every `_shared/*.md` it references. User pastes it as the first chat message; subsequent messages run under the embedded protocol. Loses slash commands + auto-fire + cross-skill chaining; preserves the protocol. Built for 6 owned skills (llm-council, the-architect, ep-council, morpheus, plugin-creator, project-lifecycle) and shipped as release assets via release.yml.

**Org / Enterprise install path (v3.8.0+, Team/Enterprise plans only).** The most durable install path Anthropic offers — survives uninstall attempts ([#45323](https://github.com/anthropics/claude-code/issues/45323)) and bypasses every Personal-upload state bug. Admins add to managed `claude-config.json`: `extraKnownMarketplaces` block referencing `keithceh/Coeus-plugin` + `enabledPlugins.coeus@coeus: "required"` (auto-install, cannot uninstall) or `"installed by default"` (auto-install, member can opt out). Member experience = zero install steps. Documented as Option 4 in README install section.

**Marketplace install path (v3.8.0+, ship'd 2026-Jun-25).** Coeus is distributed via a public mirror at `keithceh/Coeus-plugin` — the source repo (this one) stays private; the mirror carries only the built plugin runtime. Install: `/plugin marketplace add keithceh/Coeus-plugin` then `/plugin install coeus@coeus`. **Persists across Cowork restart** (Personal-upload path did not — closes Anthropic [#40600](https://github.com/anthropics/claude-code/issues/40600)) and **auto-updates** on `/plugin marketplace update coeus && /plugin update coeus` (closes the per-release re-upload friction; the marketplace-update half is mandatory — Claude installs from a local marketplace clone that ONLY that command refreshes). Architecture: `.github/workflows/release.yml` extracts `dist/coeus.plugin`, drops `scripts/marketplace.json.template` as `.claude-plugin/marketplace.json`, force-pushes to the public mirror on every tag. Mirror has no source history, no .git of the private repo — bundle + marketplace.json + a tag-versioned README. **Bootstrap (one-time, manual):** create empty public `keithceh/Coeus-plugin` on GitHub, generate PAT with `repo` scope, add as repo secret `COEUS_MIRROR_PAT`. After that, every `git tag vX.Y.Z && git push --tags` triggers the sync automatically. The workflow's "Mirror skipped (no PAT)" step prints the bootstrap instructions if the secret is missing.

**Known bug — remote-environment path mismatch (Coeus_Plugin_Error.md).** Some remote Claude environments index Coeus skills at `/mnt/skills/plugins/coeus:<name>/SKILL.md` but install them at `/mnt/skills/user/<name>/`. The index lies; any tool that trusts the indexed path errors. Skills then "fire" from in-memory description without the protocol loaded — runs become skill-flavoured, not faithful. Severity: medium-high. First observed 2026-Jun-16, recurred 2026-Jun-25. **This is NOT a repo bug** — the canonical install layout produced by `scripts/build-plugin.py` is correct. The bug is in remote install indexes. Full diagnostic + workaround in `docs/Skill-Install-Diagnostics.md`. To diagnose any environment: `python scripts/check-install.py [/path/to/skills/root]` (exit 2 = mismatch detected; provides path map to work around). Pre-v3.0.1 installs may also have `caveman-protocol/` instead of `caveman/` — the diagnostic flags this too.

**Skill-invocation honesty rule (added v3.8.0+).** Do not list a skill as "used implicitly", "de facto applied", or "pattern referenced" in a session report when the skill's trigger did not fire and its content did not load into context. Either the skill loaded (list it) or it did not (do not). A diagnosis in this session caught four false-positive entries — morpheus, project-lifecycle, plugin-creator, and the-architect were all claimed as "implicit" contributors when only ponytail had actually loaded. Conflating "I borrowed an idea from this skill's docs" with "this skill ran" inflates credit and obscures real routing gaps. If you genuinely want to credit a pattern from a skill that did not fire, say "applied pattern from X" — explicit, accurate, no inflation.

**Tier C4 cross-link (v3.8.0+).** Per `Coeus_Architecture_Improvements.md` Tier C4 — every judgment-producing skill now opens with `> Shared rules: …_shared/uncertainty_rules.md`. Applied to ALL 8 judgment-producing skills as of the R1+R2+R3 refactor (ep-council, llm-council, morpheus, the-architect, ooxml-repair, plugin-creator, coeus-router, project-lifecycle). Reason: forces the shared rule to be read, not just to exist.

**R4 token-reduction round (v3.8.0+).** Architect council ROUTE A authorised a fourth round of extractions against the 8 skills above 50% of cap. Shipped 4 quality-safe, runtime-neutral extractions (saved 1,101 tokens total): `project-lifecycle` Sub-A/Sub-D → `_shared/lifecycle_{resume,close}.md` (80% → 57%); `ooxml-repair` MAE-1R1 reference data → `docs/Ooxml-Repair-MAE1R1-Reference.md` (69% → 62%); `the-architect` ROUTE C → `_shared/architect_route_c.md` (77% → 72%); `plugin-creator` Phase 4 build-scripts → `_shared/plugin_build_recipes.md` (75% → 73%). Rejected 4 candidates where extraction would violate priority 1 (quality) or priority 3 (runtime): `llm-council` artifact templates always-loaded; `morpheus` tool-routing table always-referenced; `ep-council` already lean; `ooxml-fields` cosmetic-only at 52%. **The <50% target is architecturally infeasible** for 4 of the 8 skills given quality+runtime constraints — the 3000-token hard cap and 2700-token authoring margin remain the load-bearing budgets.

**R1+R2+R3 token-reduction refactor (v3.8.0+).** Three opt-in / cross-cutting sections extracted from at-margin skills into `_shared/`:
- **R1 — `_shared/phase5_docx_recipe.md`** — full Phase 5 (12-section consolidation order, emoji-substitution table, 10-item QA checklist, generator preference, delivery format). `llm-council` SKILL.md now keeps only the offer prompt + pointer.
- **R2 — `_shared/lifecycle_handover.md` + `_shared/lifecycle_audit.md`** — full Sub-B handover template (8 sections + update protocol) and full Sub-C audit protocol (file-listing recipe, 4-category classifier, report template, pre-delete confirmation). `project-lifecycle` Sub-B/Sub-C now keep only when/protocol-pointer rows.
- **R3 — `_shared/decision_skill_guardrails.md`** — 9 universal hard rules common to council/decision skills (phase gates, mandatory artifacts, uncertainty flagging, no fabricated citations/capabilities, models-are-simulations, generic personas, surface dissent, caveman-not-applied-here). `llm-council`, `ep-council`, and `the-architect` now keep only skill-specific guardrail additions.
- **Total saved:** 1855 tokens. Both cliff-edge skills (llm-council, project-lifecycle) restored to under 80% of cap. Quality-neutral: each `_shared/` file loads only when its phase or sub-function fires.

**Project-lifecycle trigger broadened (v3.8.0+).** The skill missed firing on `"update coeus llm handover"` because the literal trigger phrase was `"update the handover"` only. Added five near-match variants: `"update the handover note"`, `"update handover"`, `"update llm handover"`, `"update coeus llm handover"`. Symptom of a class of issue: triggers should cover the actual phrasings users use, not just the canonical short form. Run the cross-skill collision audit (`scripts/coeus_full_test.py` section B) after any trigger addition.

**Full-harness test contract.** `scripts/coeus_full_test.py` is the canonical end-to-end check, now self-locating (ROOT resolves from `$COEUS_ROOT`, then `$GITHUB_WORKSPACE`, then the script's parent-parent dir — works on Windows, macOS, Linux, CI).
- `python scripts/coeus_full_test.py` — sections A (per-skill), B (cross-skill), C (hooks) → ~145 assertions
- `python scripts/coeus_full_test.py --plugin` — adds section E (plugin bundle) → ~170 assertions, requires `dist/coeus.plugin` to exist

**CI enforcement (v3.8.0+):** `.github/workflows/test.yml` runs the `--plugin` form on every push/PR to `main`. Closes Tier B1 from `Coeus_Architecture_Improvements.md`. Any new skill commit that fails registry parity, breaks a trigger collision invariant, ships an XML token in `description:`, **exceeds the `DESCRIPTION_CHAR_CAP` (currently 500 chars) on `description:`** (added 2026-Jun-25 at 1024, tightened mid-2026), or breaks the plugin bundle will fail the build. Harness is platform-portable: hook `.ps1` syntax check uses `shutil.which('powershell') or shutil.which('pwsh')` and skips silently on Linux runners.

**Description cap (v3.8.0+, tightened v3.16.x):** the cap is `DESCRIPTION_CHAR_CAP` in `scripts/build-plugin.py` — currently **500** chars (tightened from Cowork's original 1024 in mid-2026). `check_skills()` enforces it at build time; `coeus_full_test.py` parses the same constant from build-plugin.py, so the two cannot drift. When trimming descriptions to fit, **preserve every `Trigger on:` phrase** — they're load-bearing for routing. Compress the prose half (the "Use when…" / "Covers…" sentences) instead.

Vendored skills (`caveman`, `prompt-master`) are exempt from `version:` / `argument-hint:` / `Trigger on:` assertions because their frontmatter is upstream-owned (touching it gets wiped on next sync per the v3.6.2 regression class). The sync workflow re-injects `argument-hint:` after every sync; `version:` and `Trigger on:` remain upstream's call.

Both upstream-tracked skills (`caveman`, `prompt-master`) are **bundled in-repo** and weekly auto-synced from their canonical sources — no separate install needed when you ship `coeus.plugin`.

---

## Repo layout (post v3.2.0 — Claude Code plugin spec)

```
Coeus/
├── .claude-plugin/plugin.json    # CANONICAL manifest (what Claude reads inside the ZIP)
├── skills/                       # All skill definitions — Claude auto-discovers from here
│   ├── llm-council/SKILL.md
│   ├── morpheus/SKILL.md
│   ├── the-architect/SKILL.md
│   ├── ep-council/SKILL.md
│   ├── caveman/SKILL.md          # synced from JuliusBrussee/caveman@main:skills/caveman/
│   └── prompt-master/            # synced from nidhinjs/prompt-master@main:.
│       ├── SKILL.md
│       └── references/{patterns,templates}.md
├── hooks/                        # Plugin lifecycle hooks
│   ├── hooks.json                # SessionStart registration
│   ├── cleanup-stale-install.sh  # Purges stale install files on first session post-upgrade
│   └── cleanup-stale-install.ps1
├── scripts/                      # Reproducible build (matches release.yml output)
│   ├── build-plugin.sh
│   └── build-plugin.ps1
├── docs/                         # CONFORMANCE_REPORT, COEUS_EXTENSIONS, PLUGIN_MANIFEST_EXTENSIONS, TEST_REPORT, EP-Council reference (3 files), LLM-Council reference (3 files, added v3.6.2)
├── .github/workflows/
│   ├── release.yml                  # Builds coeus.plugin + per-skill .skill on every release
│   ├── sync-upstream-skills.yml     # Weekly sync of caveman + prompt-master into skills/
│   └── update-badge.yml             # Release-date badge gist
├── .gitignore                    # Excludes *.skill, coeus.plugin, dist/ — those are build artefacts
└── README.md / CHANGELOG.md / Coeus_LLM_HANDOVER.md / CONTRIBUTING.md / CLA.md / LICENSE
```

**Build artefacts (NOT committed):**
- `*.skill` per skill — produced by `release.yml` (per Release) or `scripts/build-plugin.*` (locally). Available as Release assets.
- `coeus.plugin` — same.
- `dist/` — local build output dir.

### v3.15.0 — EP-Council v1.10 (T3 policy-reversal clause from LinkedIn/TotalEnergies integration)

1. **Source:** Satish Jha LinkedIn commentary on TotalEnergies' US offshore wind exit (opinion tier). All load-bearing facts verified via Perplexity against the DOI/ABC/CNN public record before touching the skill — the article's "~$1B" corrected to **$928M** (Judgment Fund, March 2026, Attentive Energy NY + Carolina Long Bay; seven state AGs sued June 2026). Verification + gap analysis artefact: `EP_Council_Research/Outputs/Refined_Prompt_LinkedIn_TotalEnergies_Integration.md`.
2. **No new trap** — the article documents a recovery/strength (political adaptability), not an uncovered failure mode; ≥2-case rule not met. Trap count stays 13.
3. **T3 broadened:** stability assumption now covers any single security/legal/**policy** event, incl. home-government policy reversal. Enforcer question names all four suspension vectors.
4. **TotalEnergies profile:** political-adaptability lens + ROCE 12.6% (best of majors, 4th year), Mozambique restart 29 Jan 2026 (~40% complete, first gas 2029), wind-buyback memory ("exceptional settlement is luck, not a plan"), policy-continuity red flag.
5. **Files touched:** ep-council SKILL.md (v1.10), Trap-Screen (T3 row), Members (Total), EP-Council.md (v9.4), README (T3 row), plugin.json (3.15.0), index.html regen. Also fixed this header's version drift (was 3.13.0; v3.14.0 Seismic Tools had shipped without a bump).

### v3.13.0 — EP-Council v1.9 (T12 Peak-Price Entry from CrudeTruth integration)

1. **Source:** CrudeTruth Substack "Why Most Oil Acquisitions Destroy Value" (business-analysis tier commentary; McKinsey finding: >50% of $1B+ upstream deals since 2011 destroyed value). Gap-tested its three mechanisms against T0–T11 under the ≥2-case rule; analysis artefact: `EP_Council_Research/Outputs/Refined_Prompt_CrudeTruth_Integration.md`.
2. **T12 — Peak-Price Entry added (ExxonMobil/XTO).** The uncovered failure mode: an all-equity, tier-1, on-thesis acquisition at peak prices passes T2/T6/T9 and still destroys value. Test = price vs normalized mid-cycle earnings power, never the announcement strip. Cases: XTO $41B at gas peak, BHP $20.6B at $120 oil (→$13B write-downs, sold at half), Berkshire-ConocoPhillips 2008 at $140 oil, Shell-BG synergies assumed $90/bbl and closed into $30. ExxonMobil now carries two traps (T6 + T12), like Shell and Chevron.
3. **T9 enhanced:** fires also when debt is serviceable only by starving the acquired assets' development capital at trough prices (2014–16 shale-wave mechanism).
4. **Member profiles sharpened:** Shell (BG synergy-at-strip detail), ExxonMobil (T12 + peak-entry red flag), Occidental (three-variable frame: Anadarko survived on sub-$40 breakevens alone).
5. **Files touched:** ep-council SKILL.md (v1.9), EP-Council-Trap-Screen.md (T12 section), EP-Council-Council-Members.md, EP-Council.md (v9.3), EP-Council-Walkthrough.md, LLM-Council.md, README.md, plugin.json (3.13.0), index.html regen.

### v3.12.0 — EP-Council v1.8 (9-member research refresh + T11 Megaproject Overrun)

1. **All 9 member profiles rebuilt from source-backed dossiers.** The Exxon research methodology (timeline → verifiable successes/failures → reputable commentary → institutional personality) was applied to every council member via Perplexity + web research. Profiles in `docs/EP-Council-Council-Members.md` now carry Institutional Memory (dated, sourced events) and Canonical Lesson sections in the Occidental-style rich format. Primary questions unchanged (verbatim rule preserved). Source tiering: regulator/court > academic/investigative > business press > watchdog; `[UNCONFIRMED]` marks unverified figures.
2. **T11 — Megaproject Overrun added (Chevron).** Justified by the ≥2-case rule with 4 cases from research: Gorgon $37B→$54B, Tengiz FGP $37B→$48.5B, Kashagan ~$116B, Mozambique LNG +$4.5B. Fires on megaproject FIDs (>$5B / >3-yr build) with no P90 cost/schedule viability test. T2 = buying the wrong asset; T11 = building the right asset wrongly. Chevron now carries two traps (like Shell).
3. **T3 enhanced:** integration theses resting on frontier-stability assumptions (Mozambique 4.5-yr force majeure evidence).
4. **Occidental corrections:** long-term debt $23.34B at 2025-06-30 per SEC filing (the circulating ~$13.8B figure is contradicted — do not reintroduce it); Berkshire stake ~28.2% (2025); CrownRock re-lever pattern and $9.7B OxyChem sale added.
5. **Research artefacts** (dossiers ×9 + engineered master research prompt) live OUTSIDE the repo at `\\192.168.0.119\Big_Data_II\Claude\EP_Council_Research\Outputs\` under project-lifecycle management. The dossiers are the citation trail for every profile fact.
6. **Files touched:** ep-council SKILL.md (v1.8), EP-Council-Council-Members.md (rebuild), EP-Council-Trap-Screen.md (T11 section), EP-Council.md (v9.2 history), EP-Council-Walkthrough.md, LLM-Council.md (cross-ref), README.md, plugin.json (3.12.0), index.html regen. Full list in CHANGELOG.

### v3.11.0 — LLM-Council v1.2 (7th voice — Gemini — + full member refresh)

1. **Seventh council seat added: Gemini (Gemini Pro), epistemic role "Structural Verifier.**" Source: a July-2026 comprehensive guide for each of seven current frontier models, supplied by the repo owner, matched 1:1 against the six existing council seats plus one leftover (Gemini) with no existing seat — resolved by adding a 7th member rather than dropping the file or merging it into an existing voice. Gemini's differentiator vs. the other six: an explicit internal deconstruct → verify → correct loop, structural (matrix/checklist) output discipline on multi-constraint problems, and a calibrated safety/risk-proportionality check — none of the other six voices own that niche.
2. **All six existing voices refreshed** against their vendor's current flagship-model documentation, same seat mapping throughout (no reassignment): ChatGPT → GPT-5.5, Grok → Grok 4 Heavy, Claude → Claude Fable 5, Perplexity → Perplexity Pro, DeepSeek → DeepSeek-V4-Pro, Le Chat → Mistral Medium 3.5. Lens and characteristic-failure-mode text updated per voice in `docs/LLM-Council-Members.md`; one-line table entries updated in `skills/llm-council/SKILL.md`, `docs/LLM-Council.md`, `README.md`.
3. **Phase 3 tri-team faction sizing changed from fixed 2/2/2 to rotating 3/2/2** — seven models don't divide evenly across three factions. Mechanic, randomisation rule, and the worked example in `docs/LLM-Council-Walkthrough.md` all updated; Green carries the default 3-seat (Claude/Perplexity/Gemini are all verification-flavoured) but rotates like every faction.
4. **`skills/llm-council/SKILL.md` version 1.1.0 → 1.2.0.** Token count corrected: `skills/_shared/SKILL_REGISTRY.md` had a stale `~2,852` estimate; actual is `~1,834` (well under the 3,000-token Tier-1 cap) — the stale figure predates this session and its cause wasn't investigated further.
5. **Validation:** `python scripts/coeus_full_test.py --plugin` → `PASS: 192 FAIL: 0`. `python scripts/build-plugin.py --check-only` → `CHECK PASS: 13 skills, all invariants OK (0 warnings)`. `index.html` regenerated via `scripts/build-index-html.py` (sources `docs/LLM-Council*.md` directly, no hand-editing needed).
6. **Plugin version 3.10.1 → 3.11.0** (`.claude-plugin/plugin.json`). Full changelog entry in `CHANGELOG.md`.

### v3.8.x — project-lifecycle v1.3.0 (three core files: create-once-at-kickoff, update-in-place)
1. **One file per concern, created at kickoff** — handover note, `artefacts_index.md`, and `_telemetry/log.md` are all created ONCE during Sub-K (kickoff). Subsequent updates write **into the existing files** (append for the log, overwrite-in-place for the artefacts index, section-by-section for the handover). No timestamped duplicates anywhere.
2. **`_telemetry/log.md` is append-only single file** — every cadence-tick / audit / close appends a new timestamped section at the bottom. Prior sections are immutable history; header `Last appended` + `Total updates` refreshed on each append. Replaces the v1.2.1 design that wrote `<timestamp>_<reason>.md` per update + a `_telemetry/index.md` rollup.
3. **Dropped `_telemetry/index.md` rollup file entirely** — an append-only chronological log is its own index. The rollup file (added in v1.2.1 to close FM-L2-03) is no longer needed; FM-L2-03 closes by construction now.
4. **No file is created during a close or cadence tick** — all writes go to files that already exist from kickoff. Removes a class of "did we write the file with the right name?" failures.
5. **Token count:** 1,781 → 1,853 (within cap; small increase from clarified kickoff step 6 + report).
6. **Validation:** `CHECK PASS: 12 skills, 0 warnings` + `PASS: 162  FAIL: 0`. Zero stale references to the dropped per-note design (one intentional changelog reference retained in `lifecycle_artefacts.md` §4 for migration context).

### v3.8.x — project-lifecycle v1.2.1 (council-driven refinements) + llm-council/coeus-router uncertainty triggers
1. **ROUTE-A council run on the v1.2 morph** surfaced three reversals: (C1) silent default `end-of-session` cadence at kickoff — no 6-option menu (closes FM-L2-01 kickoff friction); (C2) `artefacts_index.md` regen at close only — no atomic-rename (closes FM-L2-02 write amplification); (C3) NEW `Outputs/_telemetry/index.md` rollup file regenerated at close with one row per past per-update note + clickable link + defining-detail highlight (closes FM-L2-03 telemetry directory discoverability).
2. **Q2 trigger-gap fix (revised after collision-risk review)**: user said "I am not sure what are the best options" and no skill auto-fired. Root cause: NO skill in the suite had `"not sure"` / `"i am not sure"` in trigger lists. **Initial fix** added the `"not sure which"` family to BOTH `llm-council` and `coeus-router`. **Collision review** flagged FM-05 risk: bare `"not sure which"` on llm-council would substring-match user inputs like "I'm not sure which coeus skill" that ALSO match the router's stricter `"not sure which coeus"`. Indeterminate routing between the two skills. **Final fix:** triggers exist on `coeus-router` ONLY. The router then forwards to llm-council (or any other skill) if the actual intent turns out to be a decision rather than a skill pick — which is exactly the router's job. Architecturally cleaner; zero collision.
3. **the-architect still has zero uncertainty triggers** — not added this round; the auto-detect for ROUTE D already covers diagnostic intent. If "not sure" should trigger Architect ROUTE A directly (not via the router), add in v3.9.
4. **Council artefacts** (mandatory per Architect hard rules): `Final_Plan_v1.2.1.md` + `Premortem_Report_v1.2.1.md` in `C:/Claude/Claude-Work/Projects/AI_Tools/Docx skills/`. Six failure modes catalogued (FM-L2-01…07); three closed by v1.2.1, four open with priorities P1–P3.

### v3.8.x — project-lifecycle v1.2 (cadence + inputs/outputs + artefacts index + per-update telemetry notes)
1. **User-selectable update cadence at kickoff** — Sub-K now asks one question with six evidence-grounded options (per-action, ultradian, end-of-session [default], daily, milestone, custom). Recorded in handover §9. Full options table + neuroscience grounding (Amabile 2011 Progress Principle, Cepeda 2008 spacing effect, Kleitman/Rossi ultradian) in `skills/_shared/lifecycle_frequency.md`. `[UNVERIFIED]` flag on second-hand productivity-percentage claims.
2. **§4a Inputs / §4b Outputs lists** added to the handover template. §4a tracks every file/URL the LLM read; §4b tracks every artefact it produced with status (draft / active / superseded) and authoring skill.
3. **`Outputs/artefacts_index.md`** — new auto-regenerated single-source-of-truth file. Clickable Markdown links, ≤120-char descriptions, three output buckets (Active / Superseded / Drafts). Atomic write (`.tmp` + rename). Full spec in `skills/_shared/lifecycle_artefacts.md` §3.
4. **Per-update telemetry note** — every handover update writes a NEW timestamped file at `Outputs/_telemetry/YYYY-MM-DDTHHMM_<reason>.md` with skills-used table, failure analysis, Architect-consultation improvements plan, and a mandatory "defining details for the next LLM" section. Full history preserved (handover §8 is latest-only). Spec in `skills/_shared/lifecycle_artefacts.md` §4.
5. **Housekeeping FIRST in close** — Sub-D protocol reordered (v1.2): Sub-C audit + obsolete-delete runs BEFORE handover refresh, BEFORE artefacts-index regen, BEFORE telemetry note write. Rationale in `lifecycle_artefacts.md` §6: the index must never reference doomed files.
6. **Token count**: 2,935 → 1,781 (post-R4 extraction left room; the v1.2 additions are referenced into two new shared files, `lifecycle_frequency.md` + `lifecycle_artefacts.md`). All 162 harness assertions still PASS.

### v3.8.x — CI skill-architecture enforcement (build-plugin.py check_skills)
1. **`scripts/build-plugin.py`** extended with a `check_skills()` function that runs **before** `build()`. Fails the build (rc=1) on any of: registry-parity violation, non-vendored cap exceeded, or frontmatter-name-vs-dir mismatch. Issues a warning (escalates to hard fail in v3.9) on router-coverage miss.
2. **`--check-only` flag** lets devs lint without bundling: `python scripts/build-plugin.py --check-only`. Wire into pre-commit at your discretion.
3. **Skip rules:** `skills/_*` dirs (not skills), vendored upstream skills (`caveman`, `prompt-master`) exempt from the cap, `coeus-router` excluded from invariant 4.
4. **Why this and not a new GH Action:** `release.yml` already invokes `build-plugin.py`. Adding the check there gives both local-dev and CI coverage in one file. Costs ~70 lines vs ~30 minutes of YAML + a separate workflow surface to maintain.
5. **Validated against current repo state:** `CHECK PASS: 12 skills, all invariants OK (0 warnings)`. Stress-tested by injecting a fake orphan skill — caught with 3 distinct findings and correct rc=1.
6. **Source artefacts:** Final_Plan.md + Premortem_Report.md in `C:/Claude/Claude-Work/Projects/AI_Tools/Docx skills/` (council ROUTE A, 4 phases, 6 voices).

### v3.8.x — the-architect v1.1 (ROUTE D diagnostic mode)
1. **`skills/the-architect/SKILL.md`** morphed to v1.1.0. New **ROUTE D — Diagnostic Mode**: skips prompt-master, caveman, and the council entirely; answers the user's question in-line using the Architect's rule set as a single-pass query. Produces NO `Final_Plan.md` / `Premortem_Report.md` — diagnostic only.
2. **Auto-detection**: `/architect` with no qualifier now picks between ROUTE A and ROUTE D based on the input shape. Patterns like "is X good enough", "review the repo", "evaluate / list / audit", "what would you change" auto-route to D. Council-shaped inputs ("stress-test", "premortem", "full pipeline") still go to A.
3. **Explicit flag added**: `--diagnostic` forces ROUTE D when auto-detection might mis-route to A. Existing `--explore` flag (ROUTE C) unchanged.
4. **Failure-mode addressed**: this session's telemetry showed 3× partial failures where the Architect was loaded by a diagnostic / morph / yes-no query and the runtime short-circuited the 4-phase council per ponytail. ROUTE D makes that explicit and structured rather than ad-hoc.
5. **Token count**: ~1,591 → ~2,334 (in cap).

### v3.8.x — project-lifecycle v1.1 (kickoff + telemetry + close pop-up)
1. **`skills/project-lifecycle/SKILL.md`** morphed to v1.1.0. New `Sub-function K — SESSION KICKOFF` runs at the **start** of every project / chat / task: confirms scope, picks a project root, **creates the LLM handover note immediately** with a populated §1/§2/§5/§7 and an empty §8 Skill Telemetry table. New triggers added so Claude auto-loads the skill on session-start phrases ("new project", "new chat", "new session", "kick off", "starting work on").
2. **§8 Skill Telemetry** — new mandatory section in every project handover note. Tracks per-session: which Coeus / anthropic skills were invoked, how many times, whether they worked as intended, failure count, cause, and an improvements plan derived from a **scoped Architect consultation** (a single-pass query against the-architect's rule set — not a full 4-phase council run unless the user asks).
3. **New `Sub-function D — SESSION CLOSE`** — formalises the close protocol. At end of session, project-lifecycle **pops up the §8 telemetry table to the user** with per-row actions (apply / defer / discard / accept). The skill waits for user direction; nothing auto-applies.
4. **Token count:** project-lifecycle grew from ~1,472 to ~2,935 tokens — still inside the 3,000-token Tier-2 cap but with little headroom. Next morph either splits a sub-function out or accepts a Tier-2+ exemption like `prompt-master`.

### v3.8.0 — Skill Architecture v1.0 + coeus-router (Tier-3 meta-skill)
1. **`docs/SKILL_ARCHITECTURE.md`** and **`docs/Coeus-Architecture.md`** — formal spec and user-facing reference for the Clustered-Modular-with-Delegation architecture adopted from the 2026-06-24 Architect council run. Three tiers (nano / cluster / router), hard 3,000-token cap per `SKILL.md`, `skills/_shared/` convention, registry requirement. See `Architect_Final_Plan_Skill_Architecture.md` and `Architect_Premortem_Report_Skill_Architecture.md` for the council deliberation and the six failure modes the architecture defends against (FM-01…FM-06).
2. **`skills/_shared/`** — new convention dir with `uncertainty_rules.md`, `output_formats.md`, and the canonical `SKILL_REGISTRY.md`. Read on demand by Tier-1/2 skills; invisible to skill auto-discovery (no `SKILL.md`).
3. **`skills/coeus-router/SKILL.md`** — new Tier-3 meta-skill. Routes user intent to the correct Coeus skill via a deterministic match table; emits only a `ROUTE → / WHY → / RUN →` block then invokes the target. Cross-skill trigger collision audit: zero collisions.
4. **`prompt-master` documented exception** — at ~5,400 tokens it exceeds the 3,000-token cap. The vendored-upstream sync contract means we don't patch it locally; the exception and the upstream-fork upgrade path are recorded in `skills/_shared/SKILL_REGISTRY.md`.

### v3.7.0 — Morpheus auto-execute + 3-tab landing page
1. **Morpheus v1.1.0 — Step 3 auto-execute** (`skills/morpheus/SKILL.md`). When all pre-flight checks pass without firing a gate, no Pipeline Pause Condition applies, and the target model is the current runtime (Claude / Claude Code), Morpheus now runs the compressed prompt immediately in the same conversation after delivering the Morpheus Output block. Skipped for external targets (ChatGPT, Gemini, Midjourney, etc.) and on user opt-out ("just give me the prompt", "deliver only"). If caveman is auto-disabled, Step 3 executes the Step 1 engineered prompt instead.
2. **`index.html` landing page condensed to 3 top-level tabs** — Overview, EP-Council, LLM-Council. The five companion panels (EP Members, EP Trap Screen, EP Walkthrough, LLM Members, LLM Walkthrough) remain in the DOM and continue to receive cross-tab link routing via `MD2TAB`, but are reachable only via in-content links from their parent tab. Each sub-panel shows a `← Back to <origin>` banner that returns the reader to the tab they came from (origin stack tracked in JS so multi-hop paths return correctly).
3. **`scripts/build-index-html.py` extended** with a `parent_main_tab` column per section, a `SUB_PARENT` map in the emitted JS, and a `.backbar` element/CSS so future rebuilds preserve the 3-tab nav and back-navigation behaviour.

### v3.4.0 conformance pass — what changed vs prior versions
1. **Manifest is now slim** (4 keys: `name`, `version`, `description`, `author`). The previous extras (`slug`, `skills[]`, `hooks`, `tracks_upstream`, `packaging`) moved to `docs/PLUGIN_MANIFEST_EXTENSIONS.md`.
2. **No root-level `plugin.json` mirror** — only `.claude-plugin/plugin.json` is canonical.
3. **No `commands/` directory** — slash commands auto-register from each `SKILL.md` frontmatter (`name` + `argument-hint`).
4. **The skills `caveman` and `prompt-master` are vendored upstream copies** — don't edit by hand; they get overwritten by the weekly sync. Patch upstream instead, or extend the workflow's exclusion list.
5. **`docs/CONFORMANCE_REPORT.md` is the audit** vs `anthropics/knowledge-work-plugins`. `docs/COEUS_EXTENSIONS.md` lists the three deliberate divergences from the official spec (cleanup hook, LLM handover, vendored skills) — those are Coeus-only features with documented rationale.

---

## Why v3.2.0 exists (clean in-place upgrades)

Before v3.2.0, "Add Plugin" via Claude Desktop did an **overlay-extract**: it wrote the new ZIP's files into the existing install dir at `~/.claude/plugins/marketplaces/local-desktop-app-uploads/coeus/`, but did not remove files that had been deleted between versions. So re-uploading a fresh `coeus.plugin` left behind:
- The old root-level `.skill` baselines from v3.0.x packages
- (Hypothetically) any skill folder removed in a future restructure
- Any retired top-level file

v3.2.0 ships a **SessionStart cleanup hook** (`hooks/cleanup-stale-install.sh` + `.ps1`, registered in `hooks/hooks.json`). On the first session after an in-place upgrade, the hook:
1. Reads the version from `.claude-plugin/plugin.json`.
2. Checks for `.coeus-cleaned-<version>` marker; if present, exits.
3. Iterates the install root and removes anything not in the canonical whitelist (`.claude-plugin`, `commands`, `skills`, `hooks`, `scripts`, `assets`, `docs`, `wiki`, `plugin.json`, `skill_downloader.py`, `README.md`, `CHANGELOG.md`, `Coeus_LLM_HANDOVER.md`, `CONTRIBUTING.md`, `CLA.md`, `LICENSE`, `.gitattributes`, `.gitignore`).

**Guard 2 (v3.7.0+):** the hook refuses to run if `.git/` or `.github/` exists in `${CLAUDE_PLUGIN_ROOT}`. Install dirs never contain these; source repos always do. This blocks the entire class of "ran the hook against the source tree" mistakes that destroyed working-repo files in v3.7.x development.

**Opt-in available-skills banner (v3.7.0+):** set `COEUS_STARTUP_BANNER=1` in the shell that launches Claude. The hook then prints a single ASCII line to stderr listing every skill in `skills/`. Default OFF — no behaviour change unless opted in.
4. Writes the marker and exits.

Result: the installed plugin always matches the uploaded ZIP. If you add a new top-level entry to the canonical layout, **also add it to the whitelist** in both scripts.

To force a re-clean (e.g. for debugging): delete the `.coeus-cleaned-<version>` marker from the install dir and start a new session.

---

## Why v3.1.0 exists (the bug it fixed)

Before v3.1.0, skill dirs lived at the **repo root** (`<plugin>/<skill>/SKILL.md`). On install, Claude Cowork registered the plugin but skipped skill auto-discovery — even the slash-command wrappers failed: `Unknown command: /coeus:the-architect`.

The Claude Code plugin spec expects skills under `<plugin>/skills/<skill>/SKILL.md`. v3.1.0 moves the six dirs into `skills/` (via `git mv`, history preserved) and updates `skills` array in `plugin.json` to use `"skills/<name>"` paths. The slash commands and skill auto-discovery now both resolve on any machine after a normal `coeus.plugin` install.

If you ever see `Unknown command: /coeus:<name>` again, check in order:
1. Is the plugin actually installed? (`~/.claude/plugins/known_marketplaces.json` + `~/.claude/settings.json:enabledPlugins`)
2. Did the install put the manifest at `.claude-plugin/plugin.json` inside the ZIP (not the root)?
3. Are skills under `skills/<name>/SKILL.md` inside the ZIP?
4. Does each `SKILL.md`'s frontmatter `name:` match its folder name? (See `sync-upstream-skills.yml` for the post-sync name-normalisation step that pins this — upstream renames will otherwise drift away.)

---

## How to ship a release

1. Bump `version` in `.claude-plugin/plugin.json` (single source of truth as of v3.4.0).
2. Write a CHANGELOG entry at the top (`## YYYY-MMM-DD (vX.Y.Z) · YYYY-MMM-DD HH:MM`).
3. Tag and push: `git tag vX.Y.Z && git push --tags`.
4. Create a GitHub Release on that tag. `release.yml` fires automatically:
   - Pulls `caveman` from `JuliusBrussee/caveman@main:skills/caveman` and `prompt-master` from `nidhinjs/prompt-master@main:.`.
   - Swaps the local `skills/caveman/` and `skills/prompt-master/` with fresh upstream copies.
   - Builds six `<skill>.skill` files (zipped from inside `skills/` so the archive layout is `<skill>/SKILL.md`).
   - Builds `coeus.plugin` containing `.claude-plugin/`, `commands/`, `skills/`, `skill_downloader.py`, and the wrapper docs.
   - Uploads all seven artefacts to the Release.

Reproducible local build (matches the release-workflow output, ensures the ZIP contains only the canonical layout so the SessionStart cleanup hook has nothing to purge):

```bash
bash scripts/build-plugin.sh           # -> dist/coeus.plugin
```

```powershell
powershell .\scripts\build-plugin.ps1  # -> dist\coeus.plugin
```

---

## Coeus-router discipline (v3.12.0+)

**Whenever a new skill is added**, three edits happen together — the build now enforces the third:
1. `skills/<name>/SKILL.md` (the skill itself)
2. `skills/_shared/SKILL_REGISTRY.md` (registry parity — hard fail)
3. **`skills/coeus-router/SKILL.md`** — add either a `` `<name>` `` mention or a `/coeus:<name>` reference. Router-coverage invariant #4 promoted from warning to hard fail in v3.10.2 — build now refuses if a skill exists in `skills/` but not in the router.

Also update the router's frontmatter `description` to include the skill name inside its family enumeration (decision / tools / seismic). The description is what Claude uses for natural-language matching to activate the router in the first place — leaving a new skill out of it degrades routing recall even if the routing table itself is complete. Description hard-capped at 500 chars.

**Launch mechanism (v3.15.8 / router v1.2.0).** The router must end every route with an actual `Skill(skill="coeus:<name>", args="<task>")` tool call. Root cause of the "router never launches morpheus" bug: pre-v1.2.0 the SKILL.md said "invoke the target skill" but only showed a `RUN → /coeus:<name>` line — and slash commands printed in model output are inert text (they only fire when the *user* types them), so the model printed the block and stopped. If routing ever regresses to print-and-stop, check that the Output Format section still names the Skill tool explicitly.

---

## Notification workflows (v3.10.x+)

Two workflows wire up notifications without any external SMTP infrastructure — GitHub's own notification system does the delivery.

**Source repo — `.github/workflows/notify-collaborators.yml`** (frequency-limited v3.15.7)
Comments on the pinned tracking issue (#14). Cadence: 1 comment per published release, 1 repeat comment exactly 7 days after the latest release (daily cron checks age), 1 monthly summary (releases + issues since last month) on the 1st. Per-push notifications removed by design. Issues notify assignees only — native GitHub behaviour; they are not broadcast to the tracking thread. Permission: `issues: write`. `GITHUB_TOKEN` only.

**Mirror repo — `scripts/mirror-workflows/release-announce.yml` + `release-reminders.yml`**
Both staged into the mirror's `.github/workflows/` by `release.yml` on every tag (the mirror is force-pushed history-less, so these files must be re-shipped each release). `release-announce.yml` fires on `release: published` and posts the release body as a Discussion under "Announcements". `release-reminders.yml` (daily cron) posts the 7-day repeat reminder and the monthly releases-only summary on the 1st. Users opt in via Watch -> Custom -> Releases, OR Subscribe on the Announcements category. Permission: `discussions: write`. One-time setup on the mirror: enable Discussions, create an "Announcements" category (Announcement format), pin a "Get release notifications" discussion.

Why not a literal email-input form: GitHub already owns the user's verified email + unsubscribe path. Building an SMTP + subscriber-file pipeline re-implements infrastructure GitHub gives away free, plus adds GDPR / bounce-handling overhead. Discussions + Watch is the lazy-but-correct path. If a literal form is required later, the additions are an issue-form template, a process-subscription workflow that writes to a separate persistent branch (so the `main` force-push doesn't wipe it), and SMTP secrets on the mirror.

---

## How an end user installs Coeus

**TL;DR — recommended path:** one PowerShell line covers all three Claude surfaces.

```powershell
iwr https://raw.githubusercontent.com/keithceh/Coeus-plugin/main/install-coeus.ps1 | iex
```

`scripts/install-coeus.ps1` (shipped to mirror root by `release.yml`) does:
1. **Claude Code (CLI)** — prints the 3 `/plugin` slash commands to paste inside `claude`.
2. **Cowork** — downloads every `.skill` to `Downloads\Coeus-skills\` and opens Explorer.
3. **Claude Desktop chat** — downloads every `.paste.md` bundle to the same folder.

**Why no single-click:** Anthropic doesn't share a plugin runtime across Code / Cowork / Desktop chat. Each surface has its own install mechanism; the installer just handles them in one pass.

### Manual paths (if user skips the installer)

- **Claude Code** — inside a `claude` session: `/plugin marketplace add keithceh/Coeus-plugin` → `/plugin install coeus@coeus` → `/reload-plugins`. Auto-updates with `/plugin marketplace update coeus && /plugin update coeus` (both halves required — see stale-clone gotcha below). Persists across restart.
- **Cowork** — drag a `.skill` file from a release into the chat panel. One drag per chat. Does NOT persist across Cowork restart (Anthropic #40600).
- **Claude Desktop chat** — copy a `.paste.md` bundle into the first message of a fresh chat. No slash commands; no auto-fire.
- **Org / Enterprise** — managed `claude-config.json` with `extraKnownMarketplaces` + `enabledPlugins.coeus@coeus: "required"`. Most durable path.
- **Build locally** — `python scripts/build-plugin.py` → `dist/coeus.plugin`. Use the Python builder, not Compress-Archive (Cowork rejects without UTF-8 0x800 flag).

### Common install gotchas

- **`Host key verification failed` on `/plugin install`** — Windows OpenSSH can't negotiate with GitHub's KEX. Fix: `git config --global url."https://github.com/".insteadOf "git@github.com:"`. Documented inline in the README.
- **`/reload-plugins` reports `0 skills`** — counting quirk in Claude Code's reload output; check the actual plugin cache at `~/.claude/plugins/cache/coeus/coeus/<version>/skills/` to verify. Type `/coeus:` in chat to confirm the popup appears.
- **Cowork doesn't see plugin installed via `/plugin`** — by design; Cowork doesn't read the Claude Code plugin cache. Each surface is separate.

---

## Common gotchas

- **Slash commands come from `commands/*.md`, not `skills/*/SKILL.md`.** A skill registered without a corresponding `commands/<name>.md` wrapper cannot be invoked with `/coeus:<name>` — only via natural-language trigger phrases listed in its `SKILL.md` frontmatter.
- **`ep-council` no longer triggers on the bare words `"morpheus"` or `"architect"`** (removed in v3.7.x; was historical v8 behaviour). Cross-fires caused false positives in non-E&P chats. E&P operators should use `/coeus:ep-council`, `"board review"`, `"investible"`, or any documented natural-language trigger; the bare words now route to morpheus and the-architect as expected.
- **Upstream rename of `name:` in `SKILL.md`** would break `/coeus:<name>` resolution. The sync workflow has a `sed` step that pins `name:` to the Coeus folder name after every pull. Keep that step in place.
- **Two `plugin.json` files.** The root one is reference only. Always edit `.claude-plugin/plugin.json` first, then mirror to root.
- **Private repo + release badges.** The version/date shields on the README cannot read GitHub Releases directly (private repo). They're driven by a public Gist refreshed by `update-badge.yml` on every published release.

---

## Where to look first if something breaks

| Symptom | Look at |
|---|---|
| `Unknown command: /coeus:<name>` | `commands/<name>.md` exists? Plugin installed? `.claude-plugin/plugin.json` in ZIP? |
| Skill loads but does nothing | `skills/<name>/SKILL.md` frontmatter `name:` matches folder + command? |
| Weekly sync overwrote local edit | Check `sync-upstream-skills.yml` excludes; don't edit `skills/caveman/` or `skills/prompt-master/` directly |
| Release didn't attach `.skill` files | `release.yml` job logs; check `skills/<name>/` directory existed in the checkout |
| Version mismatch (zip vs plugin.json) | Both `plugin.json` files bumped? Tag matches? |
| Skill downloader 404s | `skill_downloader.py` is release-first; private repo needs OAuth `repo` scope. Try `--source main`. |

---

## Open work / known limitations

- Both `plugin.json` files must be hand-synced; no enforcement. Adding a CI check that diffs them would prevent drift.
- The `skill_downloader.py` OAuth flow requires `repo` scope to pull from the private Coeus repo. Public mirrors / mirrors-by-release would simplify install for non-collaborators.
- `caveman.skill` and `prompt-master.skill` baselines committed at the repo root are static; they're refreshed by the workflow on release, not on every commit. If you need a current per-commit copy, build with `skill_downloader.py --source main`.
