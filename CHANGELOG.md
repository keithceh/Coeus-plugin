# Changelog

---

## 2026-Jul-10 (v3.17.0) · obsidian-vault v1.2 — full obsidian-mcp parity verified from package source + 8 security guardrails

### Changed — obsidian-mcp parity behaviours verified against the package source (skill v1.0 → v1.2)
Every operation cross-checked against the `obsidian-mcp` npm package source; new `skills/obsidian-vault/references/OPERATIONS.md` carries the full specs. Parity behaviours now explicit:
- **Soft delete by default** — delete moves the note to `.trash/` with a `trash_metadata` record; permanent deletion is opt-in only.
- **Link integrity on move/delete** — move updates vault-wide wikilinks and md-links pointing at the moved note; delete reports broken backlinks and offers to strikethrough dead links.
- **Move hardening** — never overwrites an existing target, auto-creates missing target directories, assumes `.md` when no extension is given.
- **edit-note prepend** added alongside append/insert.
- **Search extensions** — filename search plus hierarchical and wildcard `tag:` search.
- **Tag semantics** — location control (frontmatter vs inline), ask-before-normalize, wildcard removal, preserve-children on hierarchical ops, and a git-status check before any vault-wide tag rename.

### Added — 8 security guardrails (prompt-injection / path-containment review)
1. `.obsidian/` is a hard write block — no skill operation may write inside it.
2. `trash_metadata.reason` is YAML-sanitized before being written.
3. Path containment operates on **resolved** (symlink-followed) paths; drive-relative (`C:foo`) and `\\?\`-prefixed paths are rejected.
4. Link rewriting on move uses regex-escaped note names — no pattern injection via filenames.
5. Consent for destructive ops is valid only from a **live user reply**; text encountered mid-scan (note content, frontmatter) can never satisfy a confirmation.
6. `insert` is a defined operation and `add-tags` is constrained to tag text only — no arbitrary-content smuggling.
7. Writes into `.trash/` are gated as the delete family, not as safe creates.
8. Wildcard operations disclose the matched set before acting; existence checks are case-insensitive.

**Files:** `skills/obsidian-vault/SKILL.md` (v1.0 → v1.2, not authored this pass), `skills/obsidian-vault/references/OPERATIONS.md` (new, not authored this pass), `skills/obsidian-vault/references/CONFIRMATION-RULES.md` (not authored this pass), `.claude-plugin/plugin.json` (3.16.0 → 3.17.0), `Coeus_LLM_HANDOVER.md`.

---

## 2026-Jul-10 (v3.16.0) · New `obsidian-vault` skill — direct Obsidian-vault file operations; coeus-router adds the `vault` family

### Added — `obsidian-vault` skill (new `vault` family)
Operational layer for working directly on a plain-text Obsidian vault via Claude's native file tools (Read/Write/Edit/Grep/Glob/Bash) and the `mcp__filesystem__*` MCP server when connected. Functional parity with the `obsidian-mcp` npm package (fs ops, search, regex tag editing) WITHOUT its network-drive rejection bug — NAS, UNC, and mapped-drive vault paths are first-class, never rejected. Vault-root scoped, path-contained against traversal. Destructive ops (overwrite, full-overwrite edit, tag removal, tag rename, move, delete) are confirmation-gated: two-strike per-type gating (1st and 2nd occurrence of a dangerous op-type each require full explicit confirmation), session-only skip offered only after the 2nd strike, and any blast-radius escalation (e.g. single-file to vault-wide) re-triggers confirmation even after a skip. Full gating detail lives in `skills/obsidian-vault/references/CONFIRMATION-RULES.md`. Defers OFM syntax to `obsidian-markdown`/`obsidian-bases`/`json-canvas` and live-app control to `obsidian-cli`.

### Changed — coeus-router v1.3.0 adds the `vault` family
Step 1 family table gets a new `vault` row (Obsidian vault, vault notes, `.obsidian`, note tags, "search my vault", moving/deleting notes). New Step 2d routes to `obsidian-vault` (`/coeus:obsidian-vault`). New tie-breaker rule: if a request names both a vault note path and another family's artefact, the more concrete artefact wins (consistent with rule 0). Frontmatter description and dependencies updated; "three families" prose becomes "four families" throughout.

**Files:** `skills/obsidian-vault/SKILL.md` (new, not authored this pass), `skills/obsidian-vault/references/CONFIRMATION-RULES.md` (new, not authored this pass), `skills/coeus-router/SKILL.md` (v1.2.0 → v1.3.0), `skills/_shared/SKILL_REGISTRY.md`, `.claude-plugin/plugin.json` (3.15.8 → 3.16.0), `Coeus_LLM_HANDOVER.md`, `README.md`, `index.html` (regenerated).

---

## 2026-Jul-08 (v3.15.8 follow-up) · Install docs re-ranked by ease; GitHub-direct install documented

### Added — Install-from-GitHub as Option 1 (Cowork + Desktop chat)
Cowork and Claude Desktop chat can now install a plugin directly from a public GitHub repo (Settings → Capabilities → Customize → Add Plugin → From GitHub → `keithceh/Coeus-plugin`). No downloads, no files, no terminal. Documented as the new easiest path.

### Changed — All install options re-ranked by ease of installation
README now runs Option 1–8 easiest-first: (1) GitHub-direct in Cowork/Desktop chat, (2) marketplace in Claude Code CLI (only true one-command update path), (3) one-line PowerShell installer, (4) Personal-upload legacy, (5) individual .skill files, (6) org-managed, (7) paste-prompt for web chat, (8) build locally. docs/Installation.md restructured to match (two "quickest path" sections up top, installer demoted to fallback). index.html regenerated. Stale "12 skills" counts fixed to 13.

---

## 2026-Jul-08 (v3.15.8) · coeus-router v1.2.0 — router must LAUNCH the routed-to skill (fixes "router never launches morpheus")

### Fixed — router printed the route but never launched the target skill
Root cause, two parts:
1. **Inert slash commands.** The router's Output Format ended with `RUN → /coeus:<name>` and the instruction "then invoke the target skill" — but never named the mechanism. Slash commands printed in model output are inert text; they only fire when the *user* types them. The model dutifully printed the block and stopped. v1.2.0 makes the mechanism explicit: every route must end with an actual `Skill(skill="coeus:<name>", args="<task>")` tool call in the same response; the `RUN →` line is reference-only. A route without the Skill-tool call is declared a routing failure in the SKILL.md itself.
2. **"morph this" matched nothing.** The router's morpheus row keyed only on "wants prompt-engineering THEN compression"; morpheus's own triggers listed `/morph` but not plain-text "morph". Bare "morph this" fired neither. Added "morph", "morph this", "morph it" to the router's Step 2a morpheus row and to morpheus's frontmatter description + Trigger sections (morpheus v1.1.0 → v1.1.1).

### Changed — router framed as the Coeus guru / skill selector
Per user intent: invoking the router means "pick the right skill AND start it". Intro rewritten accordingly; "coeus guru" and "skill selector" added to the router's trigger description. Output Format `FAMILY` line also corrected to include `seismic` (was still `<decision | tools>` from pre-v3.10).

**Files:** `skills/coeus-router/SKILL.md` (v1.1.0 → v1.2.0), `skills/morpheus/SKILL.md` (v1.1.0 → v1.1.1), `skills/_shared/SKILL_REGISTRY.md`, `README.md`, `docs/Coeus-Architecture.md` (hard rule 3 + "How To Use The Router"), `Coeus_LLM_HANDOVER.md` (header, skill table, router-discipline launch-mechanism note), `.claude-plugin/plugin.json` (3.15.7 → 3.15.8), `index.html` (regenerated).

---

## 2026-Jul-06 (v3.15.7 follow-up) · Notification frequency limits

### Changed — source repo notifications: per-push removed, release-driven cadence
`notify-collaborators.yml` rewritten. Old behaviour: one comment per push to main (noisy). New cadence:
1. One comment when a release is published.
2. One repeat comment exactly 7 days after the latest release (daily cron checks release age).
3. One monthly summary on the 1st — releases + issues opened/updated since last month (tracking issue excluded).

Issue notifications go to assignees only (native GitHub behaviour — issues are not broadcast to the tracking thread).

### Added — mirror repo reminders (`scripts/mirror-workflows/release-reminders.yml`)
Staged onto keithceh/Coeus-plugin by release.yml alongside release-announce.yml. Same cadence, Discussions delivery: 7-day repeat reminder + monthly releases-only summary (mirror has no active issue tracker). Combined mirror cadence: 1 announcement per release (existing) + 1 reminder at day 7 + 1 summary on the 1st.

---

## 2026-Jul-06 (v3.15.7) · EP-Council — ExxonMobil, ConocoPhillips, ENI, Occidental ground-truth passes (members 6–9 of 9; protocol complete)

### Changed — final four member profiles ground-truthed (Perplexity, 6 queries incl. 3 targeted follow-ups)

**ExxonMobil (member 6):** 7 CONFIRMED (XTO $31B stock + $10B debt Dec 2009; −$22.4B 2020 loss; Dow removal Aug 2020, component since 1928; Pioneer $59.5B closed May 2024 — close date added; $55.7B 2022 record; NY climate trial cleared Dec 2019 — "not guilty" reworded for a civil case; Science Jan 2023 paper). `[UNCONFIRMED exact figure]` marker RESOLVED: 2020 US gas write-down ~$17B after-tax (guided $17–20B, Nov 2020). 1 CORRECTED: Guyana "1.5 Mb/d installed capacity by 2025" → four FPSOs through 2025, gross capacity approaching ~1 Mb/d toward 2027.

**ConocoPhillips (member 7):** `[UNCONFIRMED %]` marker RESOLVED: 2016 dividend cut 66% (74¢ → 25¢, Feb 2016). CONFIRMED: Concho $9.7B all-stock Oct 2020 with synergies doubled; Shell Permian $9.5B cash 2021 (price added); Marathon $22.5B EV closed Nov 2024 in ~6 months; Venezuela ICSID ~$8.5B with annulment rejected 22 Jan 2025 (award final — date pinned). 1 CORRECTED: Willow "upheld on appeal 2025" → Ninth Circuit (13 Jun 2025) found a NEPA reasoning defect but remanded **without vacatur** — approval stands, construction continues.

**ENI (member 8):** ALL CONFIRMED: Zohr ~30 tcf in place, first gas Dec 2017 (~28 months), 10% BP + 30% Rosneft sold 2016 pre-production; Coral Sul first cargo Nov 2022 through the insurgency; Vår Energi absorbed Neptune Norway (closed 31 Jan 2024); OPL 245 ~$1.09B, Milan acquittal Mar 2021 **definitive at the Court of Cassation 2023** (finality pinned); Kashagan ~$116B with ENI 16.81% of NCOC (stake added). Coral North pinned: FID Oct 2025, hull launched Jan 2026 at Samsung HI, first LNG targeted 2028.

**Occidental (member 9):** CONFIRMED: Anadarko closed 8 Aug 2019, $38B/$55B, debt ~4× to ~$40B, Buffett $10B pref at 8%, no-vote structure (mechanism added: equity kept below NYSE 20% threshold); dividend −99% (79¢→11¢→1¢ — sequence added); CrownRock $12B Dec 2023; Berkshire ~28.2% common; Piper Alpha 167 dead / Cullen 106 recommendations. 1 CORRECTED: Icahn quotes "specially reprehensible"/"arrogant" not in the verifiable record → replaced with "one of the worst deals I've ever seen" (CNBC, Aug 2019) + proxy fight. 2 UPDATED/ADDED: OxyChem sale **closed 2 Jan 2026** ($6.5B to debt, targeting principal <$15B — Perplexity's first pass wrongly called the deal unverified; targeted follow-up confirmed against the ICIS close report); Reuters (26 Mar 2026): Hollub preparing to hand over the CEO role.

**Protocol complete: all 9 members ground-truthed (v3.15.2–3.15.7). Zero `[UNCONFIRMED]` markers remain in the Members doc.** Only `docs/EP-Council-Council-Members.md` changed this pass; skill stays v1.10. plugin.json 3.15.6 → 3.15.7; index.html regenerated.

---

## 2026-Jul-06 (v3.15.6) · EP-Council — QatarEnergy profile ground-truth pass (member 5 of 9)

### Changed — QatarEnergy institutional memory updated (Perplexity-verified, single clean pass, 10 sources)
7 claims checked. 5 CONFIRMED: 2005–Apr 2017 moratorium (12 yrs); Mobil founding partnership, #1 exporter by 2006 (first cargo refined to 1996/97 — loaded late 1996, delivered Japan early 1997); ≥75% + operating/marketing control (refined "per train" → **per project** — partners buy 25% of each project JV); NFE FID **February 2021** at $28.75B; 77→142 MTPA by 2030 official with 160-by-2035 under study. 1 CORRECTED: international diversification list — **Brazil dropped** (not in the 2023–25 record; headline plays are Namibia incl. Merlin-1X 2026, Guyana–Suriname basin re-entry via Block S4 PSA Nov 2025 after the 2024 Orinduik exit, Egypt). 2 ADDED (both directly reinforce T5): the "one strait" vulnerability fired — early-2026 Iran conflict forced NFE construction evacuations, fully resumed May 2026, first LNG pushed to early 2027; and the US overtook Qatar as #1 LNG exporter in 2025 (~111 Mt, first country over 100 Mt). Only `docs/EP-Council-Council-Members.md` changed; skill stays v1.10. plugin.json 3.15.5 → 3.15.6; index.html regenerated.

---

## 2026-Jul-06 (v3.15.5) · EP-Council — Shell profile ground-truth pass (member 4 of 9)

### Changed — Shell institutional memory updated; `[UNCONFIRMED exact R/P]` marker resolved
8 claims checked via Perplexity (single clean pass). 5 CONFIRMED: 2004 reserves scandal (4.47B, 23%, Watts resigned Mar 2004, SEC $120M — units corrected to **boe**), Arctic exit Sept 2015 after >$7B and the Burger J well, 2020 dividend cut 47¢→16¢ (−66%, first since WWII — figures added), Hague 2021 ruling overturned on appeal 12 Nov 2024 (duty affirmed, 45% target rejected), Sawan-era targets (capex $20–22B, LNG +4–5%/yr, oil ~1.4 Mb/d). 2 UPDATED: buyback streak "14+" → **17 consecutive quarters ≥$3B** (per Q4 2025 results, Feb 2026); BG "exited 10 countries" → **announced exits from up to 10 countries** (the announced plan, not a counted outcome; synergy guidance was initially up to $3.5B at ~$90/bbl, later raised toward $4.5B). 1 RESOLVED: the standing `[UNCONFIRMED exact R/P]` marker → **~7.8 years reserve life per 2025 reporting, down from 8.9 in 2024** — shortest among the majors, consistent with the T10 Duration Drift thesis. Red flag enriched: chemicals = six consecutive loss-making quarters through Q4 2025, ~$1.1B FY2025 adjusted loss, 2026 fix declared with "nothing off the table". Only `docs/EP-Council-Council-Members.md` changed; skill stays v1.10. plugin.json 3.15.4 → 3.15.5; index.html regenerated.

---

## 2026-Jul-05 (v3.15.4) · EP-Council — TotalEnergies profile ground-truth pass (member 3 of 9)

### Changed — TotalEnergies institutional memory updated (Perplexity-verified, single clean pass)
6 claims checked (the March 2026 wind buyback / Mozambique restart / ROCE claims were already verified in the v3.15.0 session). 5 CONFIRMED: Mozambique LNG FM declared 26 Apr 2021 after the Palma attack, ~$20B at FID, +$4.5B FM-period costs, first gas Jul 2024 → H1 2029 (FM lift decision pinned to **7 Nov 2025**, restart announcement 29 Jan 2026 — both now in profile); Yemen LNG shut in Apr 2015 (Total 39.6% largest shareholder, JV-operated — profile wording already accurate); two-pillar strategy 2021; Erika conviction upheld by Cour de cassation Sep 2012; dividend held through COVID (€0.66/share interim) while Shell (−66%, first cut since 1945) and BP cut. 1 MOVED: "live French greenwashing litigation" → ruled: most claims dismissed, three communications held misleading, one carbon-neutrality claim ordered removed; separate Paris ruling 25 Jun 2026 ordered emissions-risk reporting (Reuters). ADDED (one clause): French war-crimes complaint over the 2021 Palma attack response (BBC, Nov 2025) — extends home-legal-regime scrutiny to frontier conduct. Only `docs/EP-Council-Council-Members.md` changed; skill stays v1.10. plugin.json 3.15.3 → 3.15.4; index.html regenerated.

---

## 2026-Jul-05 (v3.15.3) · EP-Council — Chevron profile ground-truth pass (member 2 of 9)

### Changed — Chevron institutional memory precision fixes (Perplexity-verified)
6 load-bearing claims checked via Perplexity (direct-runner workaround; thread-URL read after two extraction misfires). 4 CONFIRMED: Anadarko walk-away with $1B break fee (terminated 9 May 2019; original deal $33B, Occidental's $38B deemed superior 6 May), Gorgon $37B sanction → ~$54B final, Hess ~$53B stock / ~$60B incl. debt for the 30% Stabroek interest, Richmond 2012 CSB findings (sulfidation corrosion; ~10 years of unimplemented internal inspection recommendations). 2 CORRECTED: "eight months later oil went negative" → **eleven months** (9 May 2019 → WTI negative 20 Apr 2020); Tengiz FGP "startup slipping to 2025" → startup happened — **first oil 23 January 2025** (3GP, Tengizchevroil). 1 precision fix: "21 months of arbitration" → 21-month pursuit dominated by ICC arbitration (filed 2024, ruling July 2025), closed **18 July 2025**. 2025–26 developments reviewed (Feb 2025 restructure, ≤20% workforce cut by end-2026, $3B cost programme) — not added; not load-bearing for the Concentrator lens. Only `docs/EP-Council-Council-Members.md` changed; skill stays v1.10. plugin.json 3.15.2 → 3.15.3; index.html regenerated.

---

## 2026-Jul-04 (v3.15.2) · EP-Council — BP profile ground-truth pass (member 1 of 9)

### Changed — BP institutional memory corrected to the current public record
Per-member ground-truth verification pass (Perplexity MCP was down — browser context dead; verification ran on direct web search against Bloomberg/CNBC/Irish Times/CNN/DOJ/BP releases). 10 load-bearing claims checked: 8 CONFIRMED (2020 40%-by-2030 target, 2023 softening to 25%, "fundamental reset" + "misplaced"/"too far, too fast" quotes, Texas City 15 dead + CSB/Baker findings, DWH $4B criminal plea + $20.8B settlement + >$65B total, Rosneft 19.75% exit at $24.4B post-tax charge). 1 CORRECTED: "chairman ousted in 2026" — the record is Lund stepped down Oct 2025 under Elliott pressure and his successor **Albert Manifold** was removed **May 2026** over "serious concerns" about governance and conduct (Ian Tyler interim chair); profile also gained the Dec 2025 ousting of **Auchincloss** (Meg O'Neill, ex-Woodside, first external CEO, effective Apr 2026 — fourth CEO in six years) and Elliott specifics (5.006%, ~$20B FCF demand). 1 UNVERIFIABLE this pass: TSR-lagging-all-peers 2020–2025 (directionally supported, exact ranking not re-verified; left as written). Only `docs/EP-Council-Council-Members.md` changed; skill file untouched (stays v1.10). plugin.json 3.15.1 → 3.15.2; index.html regenerated.

**Perplexity redo (same day, user-requested):** the MCP's four concurrent server instances all held dead Playwright contexts (`browser.js` caches the context with no self-heal; profile contention killed every Chrome). Worked around by driving the pinned package (`~/.claude/mcp/perplexity-web-mcp`) directly via a scratchpad runner (`ensureBrowser()` + `search()`). Two Perplexity passes re-confirmed all 8 CONFIRMED claims and the CORRECTED leadership sequence (Manifold removed 26 May 2026, Ian Tyler interim chair — Reuters/CNBC primary record), **upgraded the TSR claim from UNVERIFIABLE to CONFIRMED** (BP trailed every supermajor peer 2020–2025), and added one enrichment: Carol Howle interim CEO between Auchincloss (out Dec 2025) and O'Neill (eff. Apr 2026). DWH figures reconfirmed in DOJ framing ($4B criminal plea within the $4.5B package; $20.8B court-approved 2015 settlement). Suggested (permission-gated, not applied): patch the package's `browser.js` to self-heal dead contexts.

---

## 2026-Jul-03 (v3.15.1) · dug_binary — DUG productTypes 29/30 identified, horizon-property UUID rule

### Changed — ProductType map: 29 and 30 no longer unidentified
Reference-pattern analysis against DUG_Malampaya_Prime_2022 (Upstream_Workflows pending tasks 2–4):
- **Type 29 = property/axis descriptor** — one per property slot on horizons (attr 220), polygons (211–213), 2D lines (233–235), cross-sections (462); `attr 201` = slot index; a few carry units (Hz/m/ms/°). 6,921 relatedProductId references.
- **Type 30 = individual fault stick** — all 2,393 referenced exclusively by fault-stick sets (type 1) via attr 400; each carries attr 401=19.
Single-project inference — caveat retained in SKILL.md §8 and docs.

### Added — horizon-property UUID rule (SKILL.md §8, caveat 5)
UUIDs that resolve to no Product but appear as `property <uuid>` inside 528 Horizon blocks (and as `attributeType=735` values paired with 734 variable names) are **horizon property identifiers** — property names are not stored in the DB; infer TWT vs TVDSS from formula domain and bound horizon names.

### Fixed — Windows-console print crash in scripts 01–03
Non-ASCII characters (`→`, `≥`) in console `print()` output crashed under cp1252 (`UnicodeEncodeError`) after the workbook had already saved — replaced with ASCII. Scripts 04–05 were already clean.

### Files touched
`skills/dug_binary/SKILL.md` (§2 rows 29/30, §8 caveats 4–5), `skills/dug_binary/scripts/01_build_inventory.py` (PT_MAP + prints), `02_extract_parameters.py` + `03_resolve_uuids.py` (prints), `docs/Seismic-Tools.md` (caveat 3), `.claude-plugin/plugin.json` (3.15.0 → 3.15.1), `index.html` (regenerated). Analysis artefacts live in Upstream_Workflows (Horizon_Properties + Volume_Timeline sheets, `update_props_timeline_types.py`).

---

## 2026-Jul-03 (v3.15.0) · EP-Council v1.10 — T3 policy-reversal clause + TotalEnergies profile update

### Changed — T3 Integration Illusion broadened
Fires-when extended from frontier-security events to any single **security/legal/policy** event, explicitly including home-government policy reversal (a subsidy, permit, or lease regime one administration grants and the next revokes). Enforcer question updated to name all four suspension vectors (insurgency, court ruling, sanctions, policy reversal). Evidence: TotalEnergies' two US offshore wind leases (Attentive Energy NY, Carolina Long Bay; bought 2022) stranded by the 2025–26 US policy reversal and exited March 2026 via a **$928M** federal Judgment Fund settlement — challenged as unlawful by seven state AGs (June 2026) with a Senate EPW investigation open. Source: Satish Jha LinkedIn commentary (opinion tier); all load-bearing facts independently verified against the DOI announcement and ABC/CNN/Wind Power Monthly reporting — the article's "~$1 billion" corrected to the $928M public-record figure.

### Changed — TotalEnergies profile updated (docs/EP-Council-Council-Members.md)
- Lens: political adaptability across regime change; ROCE 12.6% in 2025, best among Western majors for the fourth consecutive year.
- Institutional memory: Mozambique LNG full restart announced 29 Jan 2026 at ~40% complete (first gas 2029); wind-lease buyback added with the framing that the recovery was an exceptional, legally contested settlement — not a repeatable mitigation — while the stranding itself was T3 firing on a policy-continuity assumption.
- Red flag: entries whose economics depend on one administration's policy continuity with no priced exit path.
- Canonical lesson: treat policy regimes like commodity prices — an exit made whole by an extraordinary settlement is luck, not a plan.

### Decision — no new trap
The article documents a recovery and an institutional strength (political adaptability), not an uncovered failure mode; the ≥2-case rule for a new trap was not met. Trap count stays 13 (T0–T12). Gap analysis artefact: `EP_Council_Research/Outputs/Refined_Prompt_LinkedIn_TotalEnergies_Integration.md` (outside repo).

### Files touched
`skills/ep-council/SKILL.md` (v1.9 → v1.10, T3 row), `docs/EP-Council-Trap-Screen.md` (T3 row), `docs/EP-Council-Council-Members.md` (TotalEnergies), `docs/EP-Council.md` (v9.4 + history), `README.md` (T3 row), `Coeus_LLM_HANDOVER.md`, `.claude-plugin/plugin.json` (3.14.0 → 3.15.0), `index.html` (regenerated).

---

## 2026-Jul-03 (v3.14.0) · Seismic Tools v2.0 — `dug_projdb` renamed `dug_binary`, DOCX + lineage-explorer artefacts, artefact selection

### Changed — skill renamed `dug_projdb` → `dug_binary`
Directory `skills/dug_projdb/` → `skills/dug_binary/`; slash command `/coeus:dug_binary`. All natural-language triggers ("dug project", "dugprj", …) retained. The GitHub wiki page `Seismic-Tools-DUG-ProjDB` needs a matching manual rename (wiki lives outside this repo).

### Added — steps 4 and 5 of the pipeline (back-ported from the Upstream_Workflows project)
Gap analysis against `Upstream_Workflows` (changelog + handover, 2026-Jun-30 → Jul-03) showed three shipped deliverables the skill couldn't reproduce. Now it can:
- **`scripts/04_export_docx.py`** — xlsx → per-volume Word report. Portrait A4, centered tables; two alphabetical H1 sections (volumes without / with derived processes); per-volume process table + Parents/Children lineage mini-tables; call-out box pointing to the HTML explorer. `--no-pid` emits the IDs-stripped variant and **asserts zero literal "pid"** in the saved document (the assert caught a real leak in testing: `(?29/pidN)` refs whose kind tag isn't `\w+`). Requires `python-docx`.
- **`scripts/05_lineage_explorer.py`** — xlsx → **one self-contained interactive HTML lineage explorer** (no CDNs/fonts/images; offline). Pure-Python layered layout — no graphviz dependency. Component tabs, hover-to-enlarge, click-to-pin with parent/child highlighting, sidebar, search, pan+zoom. Verified against the reference project: 174 volumes · 52 edges · 6 non-trivial components (25, 17, 5, 4, 2, 2), matching the graphviz-based original. Hardened against blank-page failures: `<noscript>` notice + `window.onerror` banner (the original artefact's "displays blank" report was environmental — code and data verified sound via headless-Edge render).
- **SKILL.md §5 lineage rule** — parents of volume V = `«name» (vol/pidN)` references in its resolved attrType-528 parameter specs; children inverse; self-loops skipped; cycle-tolerant layout.
- Both new scripts carry `--selftest`.

### Added — artefact selection at skill start
New SKILL.md Step 0: after the DB path is validated, the user picks outputs (multi-select): xlsx inventory (always produced — the base), DOCX full, DOCX no-pid, HTML explorer. Default all four. Juncture rationale documented: the choice determines which pipeline steps run and nothing learned mid-run changes the answer.

### Changed — hard no-default-input rule
The `.dugprj` path MUST be user-supplied — never assumed, globbed, remembered across sessions, or defaulted; reuse allowed only within the same task/session. Scripts require all path args (`ap.error` otherwise).

### Files touched
`skills/dug_binary/` (renamed; SKILL.md v1.0 → v2.0; scripts 04–05 added), `skills/coeus-router/SKILL.md` (description enumeration, dependencies, Step 2c, tie-breaker 7), `skills/_shared/SKILL_REGISTRY.md`, `README.md`, `docs/Seismic-Tools.md` (v2.0), `Coeus_LLM_HANDOVER.md`, `.claude-plugin/plugin.json` (3.13.0 → 3.14.0), `index.html` (regenerated).

---

## 2026-Jul-02 (v3.13.0) · EP-Council v1.9 — T12 Peak-Price Entry (CrudeTruth integration)

### Added — T12 Peak-Price Entry (ExxonMobil)
Integrated CrudeTruth Substack "Why Most Oil Acquisitions Destroy Value" (McKinsey: >50% of $1B+ upstream deals since 2011 destroyed value; commodity-price timing at entry is the single most reliable failure predictor). Gap analysis showed the mode was uncovered: an all-equity, tier-1, on-thesis acquisition at peak prices passes T2 (quality), T6 (strategy fit) and T9 (no debt) and still destroys value. T12 fires when the price clears the return hurdle only at/above the announcement strip, with no valuation test at normalized mid-cycle prices — including synergies computed at announcement strip rather than trough. Evidence (≥2-case rule): ExxonMobil–XTO ($41B at gas peak, ~$17–20B written down 2020), BHP US shale ($20.6B at $120 oil → $13B write-downs, sold at ~half), Berkshire–ConocoPhillips (2008, $140 oil), Shell–BG (synergies at ~$90/bbl, closed into $30). Full reference section incl. the three-variable framework (entry price × breakeven × leverage) and the build-vs-buy alternative in `docs/EP-Council-Trap-Screen.md`. ExxonMobil now carries T6 + T12. Guardrail precision: T9 tests the debt; T12 tests the price.

### Changed — T9 Acquisition Leverage Trap enhanced
Fires-when extended: debt serviceable only by starving the acquired assets' development capital at trough prices (the 2014–16 shale-wave mechanism — debt assumed at $100 oil left no development drilling at $50). Enforcer question extended accordingly.

### Changed — Member profiles sharpened from the same source
- **Shell** — BG institutional memory now carries the synergy-at-strip detail ($3.5B assumed ~$90/bbl; ~$30 at Feb 2016 close; 10-country exit).
- **ExxonMobil** — peak-entry red flag added (fires regardless of financing); T12 assigned.
- **Occidental** — canonical lesson now cites the three-variable frame: Anadarko survived on sub-$40 Permian breakevens alone while debt service crowded out development capex.

### Files touched
`skills/ep-council/SKILL.md` (v1.8 → v1.9, 13-trap description, T12 row + precision, T9 fires-when, member table), `docs/EP-Council-Trap-Screen.md` (T12 section, T9 row, counts), `docs/EP-Council-Council-Members.md`, `docs/EP-Council.md` (v9.3 + history), `docs/EP-Council-Walkthrough.md` (example row), `docs/LLM-Council.md` (cross-ref), `README.md`, `Coeus_LLM_HANDOVER.md`, `.claude-plugin/plugin.json` (3.12.0 → 3.13.0), `index.html` (regenerated). Analysis artefact: `EP_Council_Research/Outputs/Refined_Prompt_CrudeTruth_Integration.md` (outside repo).

---

## 2026-Jul-02 (v3.12.0) · Router audit + invariant #4 hard-fail

### Changed — Router description restores family/skill enumeration
Earlier trim from 1015 → 440 chars (to hit the 500-char per-SKILL cap) dropped the "decision (llm-council, ep-council, ...), tools (ooxml-repair, ...), seismic (dug_projdb)" enumeration inside `skills/coeus-router/SKILL.md`. That worked for the cap but weakened the router's natural-language matching surface — a user query mentioning e.g. `morpheus` no longer found the skill name in the router's description. Restored under the cap: description is now 458 chars, all 13 skills named, all triggers preserved.

### Changed — `check_skills()` invariant #4 (router coverage) promoted warning → hard fail
Per backlog. Any skill not present in `skills/coeus-router/SKILL.md` (either as `` `<name>` `` or `/coeus:<name>`) now fails the build. Prevents a new skill from being added without a matching routing row — which would leave the router unable to reach it. Prior behaviour was a silent warning that could be missed.

### Diagnosis — Router is structurally sound
Full audit against the current 13 skills: every skill appears in the router's list (lines 9–20) and has a dedicated routing rule (lines 59–99), including seismic tie-breaker for `dug_projdb`. Zero routing gaps. The pre-existing warning-only invariant #4 had never fired because every skill added since the router shipped was manually added to the routing table by convention. Promoting to hard fail closes the "convention" gap.

---

## 2026-Jul-02 (v3.12.0) · EP-Council v1.8 — 9-member research refresh + T11 Megaproject Overrun

### Changed — All 9 member profiles rebuilt from source-backed research dossiers
The Exxon research methodology (chronological timeline → verifiable successes/failures → reputable commentary → institutional personality profile) was applied to all 9 council members via Perplexity + web research (regulator/court findings > academic/investigative > business press > watchdog commentary; company self-description labelled; unverifiable figures marked `[UNCONFIRMED]`). Every profile in `docs/EP-Council-Council-Members.md` now carries: Lens · **Institutional Memory** (dated, sourced events) · Primary Question (unchanged, verbatim rule preserved) · Red Flag · **Canonical Lesson** · Council Trap. Highlights per member:
- **BP** — strategy-whiplash record completed: 2020 pivot → 2023 softening → 2025 Elliott/reset ("too far, too fast") → 2026 chairman ouster; Texas City CSB + Baker Panel findings; $24.4B Russia exit charge.
- **Chevron** — Anadarko walk-away ($1B break fee) as the canonical price-discipline case; Hess/Stabroek arbitration win (closed Jul 2025); Gorgon $37B→$54B and Tengiz FGP $37B→$48.5B as the execution counter-evidence; Richmond 2012 CSB findings.
- **TotalEnergies** — Mozambique LNG 4.5-yr force majeure, +$4.5B, first gas 2029; Erika conviction upheld 2012; two-pillar strategy held steady since 2021.
- **Shell** — 2004 reserves scandal (4.47B bbl / 23% / $120M SEC) as founding trauma; Hague appeal won Nov 2024 (duty affirmed, target rejected); Sawan-era harvest-mode critique grounding T10.
- **QatarEnergy** — 2005–2017 moratorium as the patience benchmark; 77→142 MTPA expansion economics; ≥75%-equity partner doctrine; international diversification (Namibia/Guyana/Brazil/Suriname).
- **ExxonMobil** — prior Perplexity note verified; XTO ($41B, written down 2020) anchors T6; Supran/Rahmstorf/Oreskes *Science* 2023 cited; NY fraud verdict (not guilty, 2019); Guyana/Pioneer comeback.
- **ConocoPhillips** — 2016 dividend cut as founding memory; Concho/Marathon buy-improve cycle; Venezuela ICSID $8.5B+ (annulment rejected 2025); Willow upheld 2025.
- **ENI** — Zohr <2.5-yr development + pre-production sell-down as dual-model proof; Coral Sul FLNG built through the insurgency; OPL 245 full definitive acquittal (2021); Kashagan exposure.
- **Occidental** — figures corrected to SEC-anchored values: long-term debt $23.34B at 2025-06-30 (replaces unverified ~$13.8B), Berkshire ~28.2% (replaces 26.64%); CrownRock re-lever pattern + OxyChem $9.7B sale added; Piper Alpha/Cullen findings added.

### Added — T11 Megaproject Overrun (Chevron)
New trap, justified by the ≥2-case evidence rule (4 cases surfaced in research): Gorgon +46%, Tengiz FGP +31%, Kashagan ~$116B, Mozambique LNG +$4.5B. Fires when a megaproject FID (>$5B gross capex or >3-year build) is only economic at sanction-case cost/schedule with no P90 viability test. T2 catches buying the wrong asset; T11 catches building the right asset wrongly. Scope precision added to guardrails (development FIDs only; T9 covers acquisitions). Full reference section with worked evidence table in `docs/EP-Council-Trap-Screen.md`.

### Changed — T3 Integration Illusion enhanced
Fires-when now includes integration theses resting on a frontier-stability assumption a single security/legal event can suspend (evidence: Mozambique LNG force majeure suspended TotalEnergies' integration case for 4.5 years).

### Files touched
- `skills/ep-council/SKILL.md` — v1.7 → v1.8: T11 row, T3 fires-when, Chevron lens/trap, T11 guardrail precision, all T0–T10 refs → T0–T11, 12-trap description.
- `docs/EP-Council-Council-Members.md` — full 9-profile rebuild (sourcing note added).
- `docs/EP-Council-Trap-Screen.md` — title, T3 row, T11 row + reference section, 12-trap count.
- `docs/EP-Council.md` — version banner v9.2, trap refs, version history (v9.1/v9.2 entries).
- `docs/EP-Council-Walkthrough.md` — trap-screen example extended to T10/T11.
- `docs/LLM-Council.md` — cross-reference trap count.
- `README.md` — EP-Council sections (member table, trap table, counts).
- `Coeus_LLM_HANDOVER.md` — skill table row + dated entry.
- `.claude-plugin/plugin.json` — 3.11.0 → 3.12.0.
- `index.html` — regenerated via `scripts/build-index-html.py`.

### Research artefacts (outside repo)
9 company dossiers + engineered master research prompt in `\\192.168.0.119\Big_Data_II\Claude\EP_Council_Research\Outputs\` (project-lifecycle managed).

### Validation
`python scripts/build-plugin.py --check-only` and `python scripts/coeus_full_test.py --plugin` — see test output in release notes.

---

## 2026-Jul-01 (v3.11.0) · LLM-Council v1.2 — seventh voice (Gemini) + full member refresh

### Added — Gemini (Gemini Pro) as the council's 7th simulated voice
New epistemic role: **Structural Verifier**. Runs an internal deconstruct → verify → correct loop before answering, organises multi-constraint problems into explicit structures (matrices, checklists, decision tables), and calibrates risk judgment between paranoid and reckless. Source: a July-2026 Gemini Pro capabilities/behavior guide supplied by the user — no existing voice covered this niche (self-verification loop, structural output discipline, calibrated safety thresholds distinguishing legitimate high-stakes work from actual malicious intent).

### Changed — All six existing voices refreshed against current per-vendor model docs
Each voice's lens and characteristic-failure-mode text updated from a July-2026 comprehensive guide for that vendor's current flagship model, matched 1:1 to the existing council seat:
- **ChatGPT → GPT-5.5** — kept "pragmatic synthesiser"; failure mode updated to reflect GPT-5.5's structured-decomposition habit occasionally over-formatting a genuinely fuzzy problem.
- **Grok → Grok 4 Heavy** — kept "contrarian provocateur"; lens updated for native tool-use/real-time search and Heavy-mode parallel-hypothesis weighing.
- **Claude → Claude Fable 5** — kept "careful reasoner"; failure mode broadened to include over-elaboration / re-deriving settled sub-questions on open-ended prompts (a documented Fable 5 behavioral trait), alongside the existing over-hedging risk.
- **Perplexity → Perplexity Pro** — kept "citation-oriented researcher"; lens updated for ensemble/agentic model routing and non-deterministic re-run behavior.
- **DeepSeek → DeepSeek-V4-Pro** — kept "systems thinker"; added its explicit reasoning-trace/reproducibility trait; failure mode broadened to include both-sides-ism and excessive appeasement when corrected (both documented DeepSeek-V4 community-observed behaviors).
- **Le Chat → Mistral Medium 3.5** — kept "nuanced European perspective"; lens updated to note its by-design neutrality is what makes the regulatory-first framing deliberate rather than an intrinsic bias.

### Changed — Phase 3 tri-team faction sizing: fixed 2/2/2 → rotating 3/2/2
Seven models don't split evenly across three factions. Faction sizes are now 3/2/2, rotating which faction carries the extra seat each round (still: no model repeats a faction in consecutive rounds, assignment stated at the top of every round). Green defaults to the 3-seat (Claude, Perplexity, Gemini are all verification-flavoured) but rotates like every other faction.

### Files touched
- `skills/llm-council/SKILL.md` — v1.1.0 → v1.2.0. Member table, faction mechanics, phase step counts.
- `docs/LLM-Council.md` — version banner, pipeline diagram, model table, faction-allocation table, version history.
- `docs/LLM-Council-Members.md` — full 7-voice profile rewrite, faction mechanics, calibration notes.
- `docs/LLM-Council-Walkthrough.md` — worked example updated to 3/2/2 factions with Gemini folded into Round 1 (Green) and Round 2 (Blue).
- `README.md` — LLM-council skill-reference section (model table, faction count, guardrail table).
- `skills/_shared/SKILL_REGISTRY.md` — `llm-council` token estimate corrected (stale ~2,852 → actual ~1,834, well under the 3,000 cap).
- `Coeus_LLM_HANDOVER.md` — new dated entry; stale header/skill-count line corrected.
- `.claude-plugin/plugin.json` — 3.10.1 → 3.11.0.
- `index.html` — regenerated via `scripts/build-index-html.py` (sources `docs/LLM-Council*.md` directly).

### Validation
`python scripts/coeus_full_test.py` — all assertions pass, no new trigger collisions, no token-cap or registry-parity violations.

---

## 2026-Jul-01 (v3.10.1)

### Added — Notification workflows (zero-SMTP, GitHub-native delivery)
- **Source repo:** `.github/workflows/notify-collaborators.yml` — on every push to `main`, posts a diff summary as a comment on a tracking issue. Anyone subscribed to that issue gets a GitHub notification + email. One-time setup: create the tracking issue, pin it, tag collaborators.
- **Mirror repo:** `scripts/mirror-workflows/release-announce.yml` — staged into the mirror's `.github/workflows/` by `release.yml` on every tag. Fires on `release: published` and posts the release body as a new GitHub Discussion under an "Announcements" category. Users opt in via Watch -> Custom -> Releases on the mirror, OR Subscribe on the Announcements category. Delivers via GitHub's notification system; no SMTP secrets needed.

### Changed — Stripped all `DUG_Malampaya_Prime_2022` references
Removed project-name mentions and reference-output tables from `index.html` (Seismic Tools panel and dug_projdb panel), `skills/dug_projdb/SKILL.md` (intro born-from line + section 7 reference values, sections renumbered), `docs/Seismic-Tools.md` (Reference Output block, version-history parenthetical), `CHANGELOG.md` (Validated-against sentence). Provenance now stays in commit history rather than user-facing docs.

### Fixed — Duplicate `<section id="seismic-tools">` panel in `index.html`
A hand-added panel duplicated the one already produced by `scripts/build-index-html.py`. Removed the hand-added duplicate; kept the build-script-generated panel.

---

## 2026-Jun-29 (v3.10.0) · New `seismic` family — `dug_projdb` skill

### Added — `dug_projdb` skill (Tier-1, family `seismic`)

First non-DOCX tools family in Coeus. Reverse-engineers a **DUG Insight `project.dugprj`** (undocumented SQLite database, schema v16.x) into a multi-sheet xlsx inventory:

- **Volumes** — every type-13 product with file path, 3D/2D classification, trace_count, samples, revision history, derived-workflow counts.
- **Volume_Processes** — one row per (volume, derived process). ProcessType label + **full parameter spec** from `AttributeRevision.attributeType=528` (BandpassFilter `filterType=Highpass`, VolumeMaths formulas, VelocityConversion `velocityVolumeType=vintt`, etc.).
- **Process_Catalog** — deduplicated catalogue of distinct derived processes.
- **Horizons** (gridded + markers) — productType 12 + 8.
- **Polygons** (interpreted + shapefiles) — productType 18 + 37.
- **ProductType_Map** — inferred category mapping with row counts.
- **UUID_Index** — every UUID in parameter strings resolved to a human-readable product name via two's-complement int64 → 128-bit reconstruction of `productUUIDMSB/LSB`.

**Pipeline (three scripts in `scripts/`, run in order, each editing the xlsx in place):**
1. `01_build_inventory.py` — workbook scaffold + main sheets.
2. `02_extract_parameters.py` — enrich Volume_Processes with attrType=528 params; add Process_Catalog.
3. `03_resolve_uuids.py` — replace UUIDs in params with `«name» (kind/pidN)`; add UUID_Index.

All three accept `--db <project.dugprj>` and `--out <output.xlsx>`. Dependencies: `openpyxl` only.

### Added — `seismic` family + `Seismic Tools` website tab

- Introduced the third Coeus intent family: **`seismic`** (upstream O&G subsurface project artefacts). Sits alongside `decision`, `tools`, and `meta`.
- `coeus-router` updated: Step 1 family table now includes seismic; new Step 2c (`Skill Within seismic`); new tie-breaker rule for `dug_projdb` vs `project-lifecycle`.
- `skills/_shared/SKILL_REGISTRY.md` — new row for `dug_projdb` (`seismic`, Tier 1, ~2,137 tokens, well under the 3,000-token cap). Families section expanded to three.

### Changed — Website navigation
- **Tools** tab renamed to **Office Tools** to make the family split explicit.
- New **Seismic Tools** tab added — landing page at `docs/Seismic-Tools.md` with one-skill bundle (more seismic skills planned).
- `scripts/build-index-html.py` — updated SECTIONS, MAIN_TABS, SUB_PARENT, SUB_LABEL, MD2TAB to wire both tabs and their sub-pages (`seismic-dug-projdb`).
- `index.html` regenerated.

### Updated
- `README.md` — Skills-at-a-Glance and Slash Commands tables include `dug_projdb`.
- `docs/Tools.md` — title is now "Office Tools — OOXML & Project Lifecycle"; cross-link to Seismic Tools.
- `.claude-plugin/plugin.json` — version 3.9.1 → 3.10.0; description updated to mention the seismic family.

### Honest notes — kept as in-skill caveats
- DUG schema is **undocumented**. Every productType→category mapping is empirical inference, verified against the reference project. The skill flags this prominently in the workbook README sheet and the ProductType_Map sheet.
- Types 29 (1,275) and 30 (2,393) remain unidentified in the reference project.
- Some processes are baked into volume names ("spectral shaping", "curvature_max") rather than as separate Volume_Processes rows.
- 2 of 42 UUIDs in the reference run are unresolved — they're horizon-property IDs, not Products. Kept verbatim rather than silently dropped.

---

## 2026-Jun-29 (v3.9.1) · EP-Council Skill v1.7 — Trap T10 Duration Drift

### Added — T10 Duration Drift (Shell)
New 11th trap in the Council Trap Screen, catching the *subtractive* portfolio drift T4 misses. Fires when:
- Distributions are funded before/instead of the best organic reinvestment
- R/P (reserve life) shortens materially faster than production
- M&A becomes the primary reserve-replacement mechanism without a working organic engine (acquired duration ≠ created duration)

Sits alongside T4 (Complexity Creep) under Shell — T4 catches *additive* drift, T10 catches *subtractive* drift. A major can pass T4 and still fail T10.

### Changed — Shell council member lens extended
Shell's lens now explicitly covers duration vs distribution discipline (reserve life, organic renewal, harvest-vs-compounder framing) alongside the existing portfolio-complexity lens. Primary question and red-flag list extended to cover both traps.

### Updated — All T0–T9 / "10 traps" references to T0–T10 / "11 traps"
- `skills/ep-council/SKILL.md` (v1.6 → v1.7, footer, three trap-screen call-sites, trap table)
- `docs/EP-Council-Trap-Screen.md` (title, intro, trap table, walkthrough — plus new T10 explainer section mirroring the T9 pattern)
- `docs/EP-Council.md`, `docs/EP-Council-Council-Members.md`, `docs/EP-Council-Walkthrough.md`, `docs/LLM-Council.md`
- `README.md` (trap pipeline, trap table, footer string)
- `index.html` (Overview Skill Reference table + EP-Council panel + Council Members panel + Trap Screen panel, including new T10 explainer matching the T9 pattern)

### Skipped (per maintainer note)
Separating the "harvest-vehicle vs compounder" multiple question into its own trap. Reason: the harvest-vs-compounder framing is currently covered inside T10's lens; a separate trap would only be warranted by a non-Shell case study.

---

## 2026-Jun-26 (v3.9.0 follow-up)

### Added — One-line installer (`scripts/install-coeus.ps1`)
Closes the three-surface install pain (Code + Cowork + Desktop chat) with a single PowerShell command. The three Claude surfaces don't share a plugin runtime, so the script handles each separately in one pass:
- **Claude Code (CLI)** — prints the 3 `/plugin` slash commands to paste inside a `claude` session.
- **Cowork** — downloads every `.skill` from the latest mirror release into `Downloads\Coeus-skills\` and opens the folder in Explorer for drag-into-chat.
- **Claude Desktop chat** — downloads every `.paste.md` bundle into the same folder for copy-paste-into-chat.

Usage: `iwr https://raw.githubusercontent.com/keithceh/Coeus-plugin/main/install-coeus.ps1 | iex`

The release workflow copies the installer to the mirror root on every tag so the raw URL stays stable.

### Fixed — Release skill swap clobbered `check_skills()`
Releases v3.9.0-pre runs failed with `caveman-local-backup: frontmatter name='caveman' != dir`. The `Bundle coeus.plugin` step backs up the local skills before swapping in the upstream copies, but the backup paths (`skills/caveman-local-backup`, `skills/prompt-master-local-backup`) lived inside `skills/`. `check_skills()` scans every `skills/*` dir, so the backups were treated as broken skills (name mismatch, missing from registry, over token cap). Moved backups to `/tmp/coeus-backup/` outside `skills/`.

### Fixed — `.claude-plugin/plugin.json` version drift caught by tag assertion
First v3.9.0 tag failed the `Assert plugin.json version matches release tag` guard because `plugin.json` was still on `3.8.0`. Bumped to `3.9.0`. The guard itself is working as intended — this was a process miss, not a CI bug.

### Updated — README Installation rewritten "for dummies"
- New **TL;DR** at the top: one PowerShell line installs across all three surfaces.
- New explainer: why a single click isn't structurally possible (no shared plugin runtime).
- New **Option 1 — One-line installer** with step-by-step instructions (open PowerShell, paste, follow on-screen prompts) and the SSH-host-key gotcha pre-fixed inline.
- Existing manual paths renumbered (3→4, 4→5, 5→6, 6→7); Option 2 retained as "manual marketplace install" for Code-only users who want to skip the script.
- Install-order table moved below the first two options so dummies see the easy path before the dependency graph.

---

## 2026-Jun-24 (v3.8.0) · 2026-Jun-24

### Fixed — CI release workflow hardening (3 commits before v3.9.0 tag)
First push of v3.9.0 surfaced three CI failures, each fixed independently before the tag could publish:
- **`release.yml` step name unquoted colon-space** — `Bundle coeus.plugin (single source of truth: scripts/build-plugin.py)` parsed as a YAML mapping. Quoted the name. Same regression class as v3.3.1's `caveman.md` description fix.
- **`release.yml` missing PyYAML** — `build-plugin.py`'s `check_skills()` does `import yaml`; release runner had no setup-python or pip install. Added `setup-python@v6` + `pip install pyyaml` before the bundle step.
- **`release.yml` inline upstream swap missing normalization** — `Bundle coeus.plugin` swaps in upstream `caveman` + `prompt-master`, then runs `check_skills()`. Upstream `caveman` ships as `name: caveman-protocol`; invariant #3 (name matches dir) hard-failed. Added inline `sed` normalization that mirrors `sync-upstream-skills.yml`'s step (pin `name:`, re-inject `argument-hint:`). Closes the "release-time pull bypasses the weekly normalization" gap.

### Bumped — GitHub Actions to silence Node 20 deprecation
- `actions/checkout@v4` → `@v5` (test.yml, sync-upstream-skills.yml — release.yml was already on v5)
- `actions/setup-python@v5` → `@v6` (release.yml, test.yml)

### Added — Paste-prompt install path (tier-2 B2 — web-chat fallback)
claude.ai web chat does not support plugin uploads. For web-chat users, generate a self-contained paste bundle per skill:
- **`scripts/build-skill-paste.py`** (new) — takes a skill name; strips the SKILL.md frontmatter; finds every `[..](../_shared/X.md)` reference and inlines the content; follows one hop of nested shared refs; writes `dist/coeus-<skill>.paste.md` with a paste-prelude that tells the model to treat the embedded protocol as load-bearing instructions.
- Built for 6 owned skills at release time: llm-council (19.5 KB), the-architect (16.8 KB), ep-council (14.8 KB), morpheus (12.2 KB), plugin-creator (14.6 KB), project-lifecycle (37.9 KB).
- **`release.yml`** extended — builds all 6 paste bundles after the per-skill `.skill` build and ships them as release assets alongside `coeus.plugin`.
- **README Option 5** documents the use: download the bundle, paste as first chat message, ask question in next message. Loses slash commands + auto-fire + cross-skill chaining; preserves the protocol.

### Added — Org / Enterprise managed install path (tier-3 C1)
The most durable Anthropic-supported install path — survives uninstall attempts ([#45323](https://github.com/anthropics/claude-code/issues/45323)) and bypasses all Personal-upload state bugs. **README Option 4** documents the admin setup: managed `claude-config.json` with `extraKnownMarketplaces` referencing `keithceh/Coeus-plugin` + `enabledPlugins.coeus@coeus: "required"` (auto-install, cannot uninstall) or `"installed by default"` (auto-install, can opt out). Member experience: zero install steps; `[org-managed]` marker in `/plugin list`.

### Updated — README install options (5 → 6, reordered by durability + reach)
1. **Marketplace** (recommended, persists across restart)
2. Personal-upload (legacy fallback — Anthropic state bugs)
3. Individual `.skill` files from Releases
4. **Org / Enterprise managed install** (new — most durable)
5. **Paste-prompt for web chat** (new — only path that works on claude.ai)
6. Build locally (maintainers / forks)

Now covers every Claude surface — Cowork / Code / Desktop / claude.ai web chat / Team-Enterprise org — with the durability-appropriate path documented for each.

### Added — Marketplace install path (option B from the architect diagnostic)
Closes the Anthropic-side Personal-upload friction (no-restart-persistence, dirty-disable-state bugs #40600 / #28554 / #63624) without making the source repo public.
- **`scripts/marketplace.json.template`** (new) — canonical `marketplace.json` shipped INTO the public mirror as `.claude-plugin/marketplace.json`. References the public mirror repo `keithceh/Coeus-plugin` with `source: github` + `repo` fields per the Anthropic schema.
- **`.github/workflows/release.yml`** extended with a `Publish bundle to public mirror` step. On every tag, the workflow extracts `dist/coeus.plugin`, drops the marketplace template + a public-facing README, force-pushes to `keithceh/Coeus-plugin` (history-less, source-free). Skipped with a clear bootstrap message if `COEUS_MIRROR_PAT` secret is not set.
- **README install section reordered** — marketplace is now **Option 1 (recommended)**; Personal-upload demoted to **Option 2 (legacy fallback)** with a callout linking to the relevant Anthropic bug numbers; Releases (`.skill` files) is Option 3; Build-locally is Option 4.
- **Bootstrap (one-time, manual):** user creates empty public `keithceh/Coeus-plugin` on GitHub, generates PAT with `repo` scope, adds repo secret `COEUS_MIRROR_PAT`. After that, every `git tag vX.Y.Z && git push --tags` syncs the mirror.

### Why this persists
The bug class the marketplace path closes is **on Anthropic's side**; the repo can't fix it directly. Marketplace install is the path Anthropic actually maintains — persists across restart, survives uninstall+reinstall cleanly, auto-updates. The bundle is history-less and re-pushed on every tag, so the mirror state is always a deterministic function of the latest release. The mirror repo has no source — only the runtime — so BSL 1.1 is preserved.

### Added — `docs/Project-Lifecycle.md` + own landing-page tab (5th main tab)
- `docs/Project-Lifecycle.md` — full reference page mirroring the EP-Council pattern: what it does, install, triggers table (with sub-function mapping), pipeline diagram, the five sub-functions, the three core files (handover / artefacts_index / telemetry log), cadence options table, telemetry §8 spec, session-close protocol, mid-session commands, when-to-use vs alternatives, version history (v1.0 → v1.3.0).
- `index.html` landing page extended from 4 to **5 main tabs**: Overview / EP-Council / LLM-Council / Tools / **Project-Lifecycle**. Tab carries one sub-panel (the project-lifecycle SKILL.md) plus the new `Project-Lifecycle` wiki-style cross-link target.

### Fixed — `lifecycle_close.md` drift from v1.3.0 single-log model
- Operator checklist line updated: `Outputs/_telemetry/log.md` **appended** with session-close entry (never a new timestamped file). Was stale from v1.2.1 per-update design.
- Step-7 comment updated: telemetry history lives in `Outputs/_telemetry/log.md`, not in per-update notes.
- Checklist header bumped to v1.3.

### Verified — stress test all impacted skills (3 invariants)
- check_skills PASS: 12 skills, 0 warnings.
- Orphan-skill injection → exit 1.
- 1100-char description injection → exit 1.
- All recovered to CHECK PASS after cleanup.
- Full harness: 162/162 (no plugin) and 182/182 (with plugin).
- Plugin rebuilt clean (UTF-8-flagged, POSIX-permed, every skill present).

### Added — `project-lifecycle` v1.3.0 (three core files, create-once-update-in-place)
Followed the v1.2 → v1.2.1 council pass. Replaces per-update timestamped files and the `_telemetry/index.md` rollup with a single append-only `_telemetry/log.md`.
- **Three core files** created once at Sub-K (kickoff), updated in place thereafter: `<ProjectName>_LLM_Handover.md`, `Outputs/artefacts_index.md`, `Outputs/_telemetry/log.md`. No timestamped duplicates anywhere.
- **`_telemetry/log.md`** is append-only — every cadence-tick / audit / close appends a new timestamped section at the bottom. Prior sections are immutable history. Header tracks `Last appended` + `Total updates`.
- **`_telemetry/index.md` rollup file deleted** — an append-only chronological log is its own index. Closes FM-L2-03 by construction.
- **Cadence default = `end-of-session`** (silent, no 6-option menu at kickoff; user overrides anytime). Closes FM-L2-01 kickoff friction.
- SKILL.md token estimate: ~2,935 → ~1,853 (post-refactor).

### Added — `project-lifecycle` v1.2: housekeeping-first close + artefacts index + cadence
The Sub-D (Session Close) protocol now runs **housekeeping before handover writes**, so the artefacts index never references files about to be deleted.
- **`_shared/lifecycle_artefacts.md`** (new, 220 lines) — full spec for §4a Inputs / §4b Outputs in the handover, the `Outputs/artefacts_index.md` single-source-of-truth index (clickable, three buckets), per-update telemetry notes (`Outputs/_telemetry/<timestamp>_<event>.md`), and the `Outputs/_telemetry/index.md` rollup. Closes FM-L2-03 (telemetry orphan).
- **`_shared/lifecycle_frequency.md`** (new, 98 lines) — handover update-cadence options (per-action / ultradian / end-of-session / daily / milestone / custom) with evidence basis. Referenced by handover §9.
- **`_shared/lifecycle_close.md`** rewritten as v1.2 — 11-step close protocol with HOUSEKEEPING FIRST as step 1; updated 13-item operator checklist.
- **`_shared/lifecycle_handover.md`** expanded — new §4a Inputs / §4b Outputs / §9 Update Cadence sections; §8 Skill Telemetry now points at the per-update notes for full history.

### Changed — `coeus-router` trigger coverage
Added 3 near-match phrasings for the "I don't know which skill" intent: `"i'm not sure which coeus"`, `"i am not sure which coeus"`, `"not sure which coeus"`. Closes the synonym gap caught in the trigger-eval round 2.

### Updated — `SKILL_REGISTRY.md`
- `project-lifecycle` token estimate refreshed: ~2,935 → ~1,781 (reflects the R1+R2+R3+R4 reductions and v1.2 reorg). Delegates row updated to list all six lifecycle `_shared/` references.

### Verified
- check_skills() PASS: 12 skills, all invariants OK (0 warnings).
- 3-round stress test of check_skills passes/fails as designed: orphan skill → exit 1; over-1024-char description → exit 1; `_*/SKILL.md` → warning.
- Full harness 182/182 PASS (with plugin). Plugin rebuilt clean.

### Fixed — Cowork validator rejection: `description` > 1024 chars
Cowork's SKILL.md validator caps the `description` frontmatter field at **1024 characters**. Three skills exceeded:
- `ooxml-repair` (1048) — condensed Covers list (kept all OOXML check categories) and Do-NOT-use rewrites
- `project-lifecycle` (1405) — trimmed redundant near-synonym triggers, condensed prose
- `the-architect` (1313) — condensed ROUTE descriptions, prose tightened
Trims preserved every `Trigger on:` phrase (essential for routing). After: 762 / 1048 / 968 chars respectively.

**New invariant in `check_skills()`** (`scripts/build-plugin.py`): hard fail if any description > 1024 chars. **New harness assertion** (`scripts/coeus_full_test.py` section A): per-skill char-cap check (12 new assertions, harness goes 162 → 182 with plugin). Stress-tested: injecting a 1736-char description fails build with `exit=1` and message `morpheus: description 1736 chars > cap 1024`. Restored, `CHECK PASS`.

This bug class — Cowork-side validator constraints — is now caught at commit time, not at upload time.

### Fixed — CI failure on Linux runners (`FileNotFoundError: 'powershell'`)
- **`scripts/coeus_full_test.py`** — the hook `.ps1` syntax check hard-coded `'powershell'` as the subprocess binary, which crashed `FileNotFoundError` on `ubuntu-latest` GitHub Actions runners. Replaced with `shutil.which('powershell') or shutil.which('pwsh')`; if neither is present, the test reports `syntax skipped (no powershell on PATH)` and continues. Verified locally on both paths: with powershell on PATH (syntax check runs) and with powershell hidden (syntax check skipped) — both 170/170 PASS.

### Refactored — R4 token reduction round (1,101 tokens saved, 4 more skills slimmed)
Architect council ROUTE A (autonomous, user pre-approved) ran against the 8 skills above 50% of the 3000-token cap. Verdict: ship 4 quality-safe, runtime-neutral extractions; reject 4 candidates that would compromise quality (always-loaded sections) or runtime (per-invocation file load).

**Shipped:**
- **`_shared/lifecycle_resume.md`** + **`_shared/lifecycle_close.md`** (new) — Sub-A (Session Resume) + Sub-D (Session Close) bodies extracted from `project-lifecycle`. Both fire conditionally so reference loads with the sub-function. **Saved 687 tokens (80% → 57%).**
- **`docs/Ooxml-Repair-MAE1R1-Reference.md`** (new) — project-specific Known-Good State table + Session 4/5/6 Repair History moved out of `ooxml-repair` SKILL.md (it's example data, not protocol). **Saved 193 tokens (69% → 62%).**
- **`_shared/architect_route_c.md`** (new) — ROUTE C deep-explore pipeline extracted from `the-architect`. Rare path — only fires on `--explore` or ambiguous problem. **Saved 154 tokens (77% → 72%).**
- **`_shared/plugin_build_recipes.md`** (new) — Phase 4 Bash + PowerShell build-script templates extracted from `plugin-creator`. Fires once per plugin scaffold. **Saved 67 tokens (75% → 73%).**

**Rejected (council red-team verdict):**
- `llm-council` (61%) — artifact templates fire every council run; extraction adds per-invocation latency (priority 3 violation).
- `morpheus` (72%) — tool-routing table referenced every run; same constraint.
- `ep-council` (69%) — already lean for scope; in-skill trap table is the routing index (full detail already in `docs/EP-Council-Trap-Screen.md`).
- `ooxml-fields` (52%) — barely over 50%; cosmetic-only reduction not worth churn.

**Conclusion:** the <50% target is architecturally infeasible for 4 skills given the quality + runtime constraints. The 3000-token hard cap and 2700-token authoring margin remain the load-bearing budgets. Sub-50% is cosmetic and was not pursued where it would degrade quality or add per-run latency. R4 closes the at-margin problem and is the right floor.

### Refactored — R1+R2+R3 token reduction (1,855 tokens freed across 4 skills)
Three architect-approved opt-in/cross-cutting sections extracted from at-margin skills into `_shared/`:
- **R1 — `_shared/phase5_docx_recipe.md`** (new) — full Phase 5 (12-section consolidation order, emoji-substitution table, 10-item QA checklist, python-docx → pandoc → markdown-fallback generator preference, delivery format). `llm-council` SKILL.md keeps only the user-offer prompt + pointer. **Saved 1,085 tokens** (98% → 61% of cap).
- **R2 — `_shared/lifecycle_handover.md` + `_shared/lifecycle_audit.md`** (new, 2 files) — full Sub-B handover template (8 sections + update protocol) and full Sub-C audit protocol (file-listing recipe, 4-category classifier, report template, pre-delete confirmation including the `mcp__cowork__allow_cowork_file_delete` step). `project-lifecycle` Sub-B/Sub-C keep only when/protocol-pointer rows. **Saved 584 tokens** (99% → 80% of cap).
- **R3 — `_shared/decision_skill_guardrails.md`** (new) — 9 universal hard rules common to council/decision skills (phase gates, mandatory artifacts, uncertainty flagging, no fabricated citations/capabilities, models-are-simulations, generic personas, surface dissent, caveman-not-applied-here). `llm-council`, `ep-council`, `the-architect` now keep only skill-specific guardrail additions. **Saved 186 tokens** across 3 skills.
- Quality trade-off: each `_shared/` file loads only when its phase or sub-function fires (Phase 5 is opt-in / rare; Sub-B and Sub-C fire on specific triggers; guardrails are referenced rather than always-loaded). Net-neutral for code-bearing paths; net-positive for DRY consistency.

### Added — Tier C4 cross-link extended to all 8 judgment-producing skills
The Tier C4 pointer (`> Shared rules: …_shared/uncertainty_rules.md`) now appears in ALL 8 judgment-producing skills (added to `llm-council` and `project-lifecycle` after R1+R2 freed cap headroom). Previously deferred on those two skills per the FM-CI-01 author-with-2700-margin rule.

### Added — `check_skills()` invariant enforcement in build script (Council ROUTE A approved)
- **`scripts/build-plugin.py` extended with `check_skills()`**, called from `__main__` before `build()`. Four invariants from the council Final_Plan (`C:/Claude/Claude-Work/Projects/AI_Tools/Docx skills/Final_Plan.md`):
  - **#1 Registry parity** (hard fail) — every `skills/<name>/` has a row in `SKILL_REGISTRY.md`. Closes FM-03.
  - **#2 Token cap** (hard fail, vendored exempt) — every non-vendored `SKILL.md` ≤ 3,000 tokens by `wc -w × 1.33` heuristic. Closes FM-01.
  - **#3 Name match** (hard fail) — every `SKILL.md` frontmatter `name:` matches its directory name. Closes FM-05.
  - **#4 Router coverage** (warning, → hard fail in v3.9) — every routable skill appears in `coeus-router`'s match table. Closes FM-02/FM-05.
- **`--check-only` flag** for lint-without-build (also wired into `docs/SKILL_ARCHITECTURE.md` as the pre-commit invocation).
- **FM-CI-04 mitigation** (Premortem_Report.md): warn if any `_*` directory contains a `SKILL.md` (treated as "convention only, not a skill" by the skip rule; a SKILL.md inside is almost certainly misplaced).
- **Stress-tested both directions**:
  - Inject orphan skill (no registry entry) → exit 1, message names the orphan.
  - Inject `_test_misplaced/SKILL.md` → warning fires.
  - Remove the injection → CHECK PASS, exit 0.

### Added — Remote-environment install diagnostic
- **`scripts/check-install.py`** — autodetects canonical vs remote install layouts, returns exit 0/1/2, prints path-resolution workaround if the path-mismatch bug from `D:/Downloads/Coeus_Plugin_Error.md` is detected. Catches stale `caveman-protocol/` directories (pre-v3.0.1 install marker).
- **`docs/Skill-Install-Diagnostics.md`** — full diagnostic walkthrough: symptom, severity, path resolution map (broken indexed path → real path), how to run the diagnostic, exit-code semantics, permanent fixes, how to confirm you are NOT affected.
- **`Coeus_LLM_HANDOVER.md`** — added entry pointing future LLM sessions at the diagnostic + workaround. Clarified this is NOT a repo bug; the canonical install produced by `scripts/build-plugin.py` is correct. The bug is in remote-environment install indexes that disagree with the actual filesystem.

### Changed — project-lifecycle trigger coverage
- **`project-lifecycle` triggers broadened** to catch near-match handover-update phrasings that fell through `"update the handover"` literal-match. Added: `"update the handover note"`, `"update handover"`, `"update llm handover"`, `"update coeus llm handover"`. Symptom caught during a session diagnosis where the user said `"update coeus llm handover"` and project-lifecycle did not auto-fire because its trigger string did not contain that exact substring.

### Added — Skill-invocation honesty rule (handover §)
- **New convention in `Coeus_LLM_HANDOVER.md`**: do not list a skill as "used implicitly", "de facto applied", or "pattern referenced" in session reports unless the skill's trigger fired and its content loaded. Either the skill loaded (list it) or it did not (do not). Caught a diagnosis where four skills (morpheus, project-lifecycle, plugin-creator, the-architect) were claimed as "implicit" contributors when only ponytail had actually loaded. Conflating borrowed-idea with skill-fired inflates credit and obscures real routing gaps.

### Audited — Skills not invoked this session
After-the-fact analysis of all non-invoked skills concluded:
- **project-lifecycle would have been useful** had it fired (Sub-B Handover Update directly matches the handover-edit work) — fixed by trigger broadening above.
- caveman would have curbed verbose prose — correctly silent (user did not request).
- All others (morpheus, plugin-creator, the-architect, llm-council, ep-council, coeus-router, ooxml-*) correctly did not fire — task did not match their domain.

### Added — Tier B1 enforcement: GitHub Actions test workflow
- **`.github/workflows/test.yml`** — runs `scripts/coeus_full_test.py --plugin` on every push/PR to `main`. Closes Tier B1 from `Coeus_Architecture_Improvements.md` ("CI check: registry parity — fail build if any `skills/*/` directory is missing from `SKILL_REGISTRY.md`"). The harness already covered registry-parity, frontmatter conformance, XML-token regression class (v3.5.1), cross-skill trigger collisions, dependency resolution, embedded-Python syntax, hook syntax + Guard-2, and full plugin-bundle integrity. Wiring it into Actions converts every guarantee from convention to enforcement.
- **`scripts/coeus_full_test.py` made self-locating** — ROOT now resolves from `$COEUS_ROOT`, then `$GITHUB_WORKSPACE`, then the script's parent-parent directory. No CI-side sed patching, no Windows-path hardcode for non-Windows runners. Verified portable: 169/169 PASS when invoked from any cwd.

### Verified post-CI-wire (3 rounds)
- R1 baseline: 169/169 PASS against current registered state (registry + router + arch docs already in sync per §14 of `Coeus_v3.8.0_LLM_Handover.md`).
- R2 after self-locating: 169/169 from the repo root.
- R3 cross-cwd portability: 169/169 invoked from `/tmp`.

### Added — Tools bundle (4 new skills)
Four standalone skills delivered together as one umbrella for long-running DOCX-centric project work. Sourced from `C:/Claude/Claude-Work/Projects/Technical_Reports/Outputs/LLM_Handover_Skill_Creation.md` (the architect-approved spec from the MAE-1R1 Well Completion Report project, Sessions 1–15). All four conform to the Coeus standard (front-loaded `Trigger on:` line, `argument-hint:`, no XML tokens in description, 0 cross-skill trigger collisions verified).
- **`ooxml-repair`** — diagnose and repair "Word found unreadable content" errors. Covers ZIP integrity, XML well-formedness, w14:paraId validity, orphaned bookmarkEnd tags, orphaned comment references (the most common root cause), duplicate style IDs, numbering chain integrity, relationship target existence, revision ID uniqueness, footnote integrity, mc:Requires namespace declarations. Includes the safe ZIP rebuild recipe that preserves `flag_bits` and `create_version`.
- **`ooxml-fields`** — SEQ field + REF field + caption numbering management via direct XML manipulation. Locates fields, reads/corrects cached values, detects hardcoded captions, audits sequence integrity (gaps/duplicates), checks REF target bookmarks.
- **`docx-inventory`** — extract a complete figure and table inventory from a DOCX to a two-sheet xlsx (Figures, Tables) with per-row issue flagging (no-SEQ-field, duplicates, gaps).
- **`project-lifecycle`** — three sub-functions in one cluster skill: **Resume** (orient a new LLM session on an existing project), **Handover** (create/update the 7-section handover template), **Audit** (classify project files as Active / Superseded / Temp / Unknown). Sub-functions share user-intent domain and combined token count fits within the 3,000-token cluster limit.

### Added — Umbrella reference page + landing-page tab
- `docs/Tools.md` — umbrella reference page describing what each Tool does, when to use which, real workflow chains, and how they avoid duplicating existing skills (`docx`, `xlsx`, `memory-management`).
- `index.html` landing page now has a fourth main tab **Tools** with four sub-panels (one per skill), back-bar navigation, wiki-style cross-tab links (`Tools-OOXML-Repair`, `Tools-OOXML-Fields`, `Tools-DOCX-Inventory`, `Tools-Project-Lifecycle`). Pattern matches the existing EP-Council / LLM-Council umbrellas.

### Verified
- Conformance: **75/75 PASS** (was 50/50 — +25 from the four new skills, with the harness updated to skip `_shared/` resource dirs).
- Cross-skill trigger collision audit: **0 collisions** across all 11 skills' quoted trigger phrases.
- XML-token-in-description scan: **0 hits** (passes Desktop validator that rejected v3.5.0's `<name>` token).
- Plugin builds clean with the UTF-8-flagged Python builder (Cowork-safe).
- New full-harness `coeus_full_test.py` ran 3 rounds: R1 caught 7 issues (SKILL_REGISTRY missing 4 new entries; vendored-skill required-field over-strictness), R2 after fixes 145/145 PASS, R3 with rebuilt plugin 165/165 PASS. Harness covers: per-skill frontmatter / no-BOM / no-XML-tokens / no-emoji-in-frontmatter / python-block syntax / front-loaded Trigger line (owned only); cross-skill trigger collisions + dependency resolution + SKILL_REGISTRY completeness; hook bash+PS syntax + functional Guard-2 (refuses on repo, preserves .git); plugin bundle POSIX paths + UTF-8 flag + create_system + manifest schema + every skill present + every SKILL.md re-parses from the extracted bundle.
- SKILL_REGISTRY updated with the 4 new Tools-bundle skills.

---

## 2026-Jun-24 (v3.8.0) [pre-Tools] · 2026-Jun-24

### Added — Skill Architecture v1.0 (Clustered-Modular with Delegation)
- **`docs/SKILL_ARCHITECTURE.md`** — formal spec for the three-tier model
  (nano-skill / cluster / router), 3,000-token hard cap, `skills/_shared/`
  convention, registry requirement, and the seven hard rules.
- **`docs/Coeus-Architecture.md`** — user-facing reference page (same format
  as `LLM-Council.md` and `EP-Council.md`; linked from the new top-level tab
  in the landing page).
- **`skills/_shared/`** — convention dir for cross-skill rules:
  - `uncertainty_rules.md` — single source of truth for confidence markers
    (`Likely:`, `[UNVERIFIED]`, hedged voices) and the four hard uncertainty
    rules (no fabricated citations, no fabricated capabilities, surface
    minority positions, don't carry false certainty forward).
  - `output_formats.md` — common artifact, header, table, path, and length
    conventions.
  - `SKILL_REGISTRY.md` — canonical registry of every shipped skill. Same-
    commit-entry rule enforces the FM-03 (orphan-skill) mitigation from the
    Architect premortem.
- **`skills/coeus-router/SKILL.md`** — Tier-3 meta-skill. Routes user
  requests to the correct Tier-1/2 Coeus skill using a deterministic match
  table. Contains zero domain logic — emits only a `ROUTE → / WHY → / RUN →`
  block and invokes the target skill. Triggers: `/coeus:router`,
  `/coeus-router`, `"which coeus skill"`, `"route this"`, `"pick the right
  coeus skill"`. Cross-trigger collision check vs all existing skills: zero
  collisions.

### Rationale (from The Architect council run, 2026-06-24)
The Architect ran a full 4-phase council (ROUTE A — prompt-master → caveman →
council) on the question "monolithic vs modular Coeus skill architecture?".
Outcome: clustered-modular with delegation pattern, 5:1 council vote against
the monolith. Full record in `Architect_Final_Plan_Skill_Architecture.md`;
6-month premortem with six failure modes (FM-01 cluster creep, FM-02 dead
delegation path, FM-03 orphan skill, FM-04 shared-rule divergence, FM-05
trigger war, FM-06 handover gap) in
`Architect_Premortem_Report_Skill_Architecture.md`. v3.8.0 ships the
architecture as four concrete artefacts plus this changelog entry; the
mitigation for each failure mode is captured in the architecture doc.

### Compatibility
All four artefacts follow the Claude Code plugin spec (`<plugin>/skills/<skill>/SKILL.md` with frontmatter, slash commands auto-registered from `name:`), so they load identically in **Claude Chat, Cowork, and Claude Code**. `_shared/` has no `SKILL.md` and is therefore invisible to skill auto-discovery; it is read on demand by Tier-1/2 skills that reference it.

### Compliance
- All eight skill files validated against the architecture: 7 of 8 under the 3,000-token cap. `prompt-master` (5,408 tokens) is the documented vendored-upstream exception — `skills/_shared/SKILL_REGISTRY.md` notes the rationale and the upstream-fork upgrade path.
- All eight `SKILL.md` `name:` fields match their directory names.
- All eight skills registered in `SKILL_REGISTRY.md`.
- Cross-trigger collision audit: zero collisions.

---

## 2026-Jun-24 (v3.7.0) · 2026-Jun-24

### Changed (auto-trigger reliability pass)
- **Description front-load** for all five owned skills (`ep-council`, `llm-council`, `morpheus`, `the-architect`, `plugin-creator`): the `Trigger on:` line is now the **first line** of the `description:` block, before any prose. Surfaces that truncate descriptions for intent matching see the triggers first. Vendored skills (`caveman`, `prompt-master`) untouched to avoid re-opening the upstream-sync wipe class (see v3.6.2).
- **New triggers added** (≤2 per skill, picked to be unambiguous and collision-free):
  - `ep-council`: `"farm-in"`, `"FID"`
  - `llm-council`: `"i'm torn between"`, `"weigh the options"`
  - `morpheus`: `"refine my prompt for"`, `"compress this prompt"` (promoted from body to trigger line)
  - `the-architect`: `"full pipeline"`, `"architect this"`, `"stress-test and plan this properly"`, `"run the full council with prompt engineering"` (promoted from body to trigger line)
  - Cross-skill collision audit: 0 collisions across all owned-skill trigger phrases.
- **Dropped `morpheus` and `architect` as bare-word triggers on `ep-council`** (v8 behaviour). The cross-fires caused false positives in non-E&P chats. E&P operators should now use `/coeus:ep-council`, `"board review"`, `"investible"`, `"farm-in"`, `"FID"`, or any documented natural-language trigger. The bare words now route to their canonical skills.

### Added
- **Opt-in SessionStart available-skills banner** (`COEUS_STARTUP_BANNER=1` env var). When set, both `cleanup-stale-install.sh` and `.ps1` print a single ASCII line to stderr listing every skill in `skills/`. Default OFF — no behaviour change for users who don't opt in. Uses plain `[Console]::Error.WriteLine` / `>&2` to avoid re-hitting the v3.3.1 Write-Error exit-code class.

### Fixed (this-session incident)
- **Cleanup hook `cleanup-stale-install.{sh,ps1}` now refuses to run inside a git repo.** Added Guard 2 (`.git/` or `.github/` present → exit 0, no touch). The original Guard 1 (`.claude-plugin/plugin.json` exists) was too weak: source repos have that file too, so during a hook smoke test the source tree's `.git`, `.github`, `dist`, `index.html`, and `vercel.json` got purged as "stale". Repo recovered from origin (commit `97e69fa`) and a `/tmp` clone; working-tree edits preserved. Guard 2 closes the entire mistake class.

### Changed
- **`release.yml` now delegates the `coeus.plugin` bundle step to `python3 scripts/build-plugin.py`** — the same builder used locally. Guarantees byte-for-byte parity between `dist/coeus.plugin` built on a developer machine and the asset attached to a GitHub Release, eliminating the toolchain drift between `zip -r` (release) and the local Python builder. The release still swaps in upstream-fresh `caveman` + `prompt-master` before invoking the builder, so release-time upstream freshness is preserved.

### Added
- **Morpheus v1.1.0 — Step 3 auto-execute.** When all pre-flight checks pass without flags, no pause condition fires, and the target model is the current runtime (Claude / Claude Code), Morpheus now runs the compressed prompt immediately in the same conversation. If the target is an external tool (ChatGPT, Gemini, Midjourney, etc.) or the user opts out ("just give me the prompt"), Step 3 is skipped and only the Morpheus Output block is delivered. Step 3 is also skipped if caveman auto-disabled and the user only wanted the engineered prompt back.

### Updated
- **`index.html` landing page condensed to 3 top-level tabs** — Overview, EP-Council, LLM-Council. The five companion panels (EP Members, EP Trap Screen, EP Walkthrough, LLM Members, LLM Walkthrough) remain in the document and continue to receive cross-tab link routing via `MD2TAB`, but are reached only via in-content links from their parent tab. Each sub-panel shows a `← Back to <origin>` banner that returns the reader to the tab they came from (origin stack tracked in JS).
- README, `docs/` references, and Coeus_LLM_HANDOVER updated to describe the 3-tab navigation model and the new Morpheus auto-execute behaviour.
- `.claude-plugin/plugin.json` → `3.7.0`.

---

## 2026-Jun-21 (v3.6.2) · 2026-Jun-21 17:00

### Added
- **Three new reference docs for `llm-council`** in `docs/`, mirroring the structure of the EP-Council documentation set:
  - **`docs/LLM-Council.md`** — main reference: what it does, install, triggers, pipeline diagram, six-voice table, faction allocation, phase gates, output artifacts, mid-session commands, mandatory flags & guardrails, when-to-use-this-vs-architect-vs-EP-Council, version history.
  - **`docs/LLM-Council-Members.md`** — full profile of each of the six simulated voices: lens, primary question, characteristic failure mode, when to listen, when to discount, default factional bias. Includes faction mechanics and calibration notes.
  - **`docs/LLM-Council-Walkthrough.md`** — complete worked example (warehouse consolidation) showing every phase, every gate, every artifact, the optional Phase 5 production .docx flow, and common pitfalls.
- **`scripts/build-index-html.py` extended** — `index.html` landing page now exposes 8 tabs (was 5): Overview, EP-Council + 3 EP companions, LLM-Council + 2 LLM companions. Cross-tab link map (`MD2TAB`) updated so in-doc markdown links to the new files switch tabs instead of navigating away.

### Updated
- `.claude-plugin/plugin.json` → `3.6.2`.
- README and Coeus_LLM_HANDOVER updated to point at the new LLM-Council docs.
- Archive mirror refreshed.

### Fixed
- **Regression** — the weekly `sync-upstream-skills` workflow (commit `d0ccf0e`, post-v3.4.0) wiped the Coeus-added `argument-hint:` from `skills/caveman/SKILL.md`. The workflow's name-normalisation step pinned `name:` but didn't preserve `argument-hint:`, so each sync silently stripped it. Conformance check caught it during this release. Restored the field and extended the workflow with an idempotent re-injection step: each matrix entry now carries an `argument_hint:` value, and the normalisation block re-inserts it after the `name:` line if upstream omits it. Prevents recurrence on every future sync.

---

## 2026-Jun-21 (v3.6.1) · 2026-Jun-21 16:00

### Fixed
- **Claude Cowork upload rejected `coeus.plugin` with `zip file contains path with invalid characters`.** Root cause: PowerShell's `Compress-Archive` (and even Python's `zipfile.writestr` for ASCII filenames) does not set the **0x800 UTF-8 filename flag** in zip entries. Cowork's strict validator interprets unflagged paths as CP437/legacy and rejects the archive. Desktop's validator was lenient and accepted them, masking the bug.
- **New cross-platform builder `scripts/build-plugin.py`** is now the single source of truth for the bundle. It:
  - Subclasses `ZipInfo` (`Utf8ZipInfo`) to override `_encodeFilenameFlags` and force `0x800` on every entry — CPython otherwise resets `flag_bits` to 0 in `_open_to_write` before writing the local header.
  - Writes POSIX permissions (0644 for files, 0755 for `*.sh` / `*.ps1` / `*.py`) with `create_system = 3` (UNIX).
  - Uses forward-slash POSIX paths exclusively (`Path.as_posix()`).
  - Self-verifies the produced archive against the strict ruleset before exiting.
- **`scripts/build-plugin.ps1` and `scripts/build-plugin.sh` are now thin wrappers** that delegate to `build-plugin.py`. Reason: previously each platform produced subtly different zips; the Python backend guarantees identical bytes regardless of host OS.

### Tested
Three independent rounds of build+verify confirm compliance with both Claude Cowork (strict UTF-8 flag + POSIX) and Claude Desktop (lenient):
- **R1:** Python builder → 35/35 entries UTF-8-flagged, POSIX-permissioned, safe-named.
- **R2:** Rebuild + extract-back round-trip → 0 utf8/posix/perm violations, 0 content mismatches.
- **R3:** PowerShell wrapper end-to-end + `unzip -tq` integrity scan → no errors detected.

### Updated
- `.claude-plugin/plugin.json` → `3.6.1`.
- `README.md` build instructions updated to call out the Python builder.

---

## 2026-Jun-21 (v3.6.0) · 2026-Jun-21 15:00

### Added
- **`llm-council` Phase 5 — Production-Ready Document (opt-in)**. After Phase 4 delivers `Final_Plan.md` + `Premortem_Report.md`, the council now offers the user a single consolidated `.docx` that incorporates every artifact (Strategic Roadmap, six-model synthesis, tri-team rounds, full Final Plan, full Premortem Report, ranked mitigation framework, assumptions, decision-gate appendix). The skill prompts exactly once with a yes/no gate; only on explicit "yes" does it proceed.
- **Canonical emoji substitution table** in Phase 5.3 — every emoji used anywhere in council output (severity dots, pass/fail marks, team colours, etc.) has a plain-language substitute (`[CRITICAL]`, `[PASS]`, `Blue Team`, etc.). A final regex sweep (`[\U0001F300-\U0001FAFF☀-➿️]`) aborts delivery if any emoji slips through. Reason: Word renders Unicode emojis inconsistently across locked-down corporate desktops; substitution guarantees portability.
- **10-item pre-delivery QA checklist** (failable). Covers emoji clearance, section completeness, no `TBD`/placeholder tokens, table integrity, link resolution, heading-level contiguity, page/header fields, word/section counts, source-artifact match, ownership field. Any failure blocks delivery.
- **Generator preference order**: `python-docx` → `pandoc` → fallback (deliver consolidated emoji-free markdown + one-line pandoc command for the user to run locally).

### Updated
- `skills/llm-council/SKILL.md` → v1.1.0. Added Phase 5 (6 steps), added 3 new behavioural guardrails (Phase 5 is opt-in only; never issue .docx with failed QA; never ship emojis in the production .docx).
- `.claude-plugin/plugin.json` → `3.6.0`.

### Note for downstream skills
- `the-architect` chains llm-council in its full-pipeline route, so Phase 5 surfaces automatically there too — no separate change needed in `the-architect/SKILL.md`.

---

## 2026-Jun-21 (v3.5.1) · 2026-Jun-21 14:00

### Fixed
- **`skills/plugin-creator/SKILL.md` failed Claude Desktop install** with `Skill 'skills/plugin-creator': SKILL.md description cannot contain XML tags`. The description's `skills/<name>/SKILL.md` token was parsed by the desktop validator as an XML tag. Reworded to `per-skill SKILL.md auto-registration` — angle-bracket-free. Body references using `<name>` are not affected; the validator only inspects the frontmatter `description:` field. Plugin now uploads cleanly via **Add Plugin**.

### Updated
- `.claude-plugin/plugin.json` → `3.5.1`.
- `dist/coeus.plugin` rebuilt.

---

## 2026-Jun-21 (v3.5.0) · 2026-Jun-21 12:00

### Added
- **New skill `plugin-creator`** (the "Autobot Transformer"). Packages a raw idea, a single prompt, a workflow note, or an existing folder of skills into a spec-compliant Claude Code / Cowork plugin bundle ready for desktop "Add Plugin" install. Encodes the full anthropics/knowledge-work-plugins standard plus the lessons learned across the Coeus v3.0 → v3.4.0 conformance pass: canonical 4-key manifest, `skills/<name>/SKILL.md` auto-registration (no `commands/` wrappers), optional SessionStart cleanup hook, reproducible build scripts (Bash + PowerShell), UTF-8/LF/no-BOM hygiene, and a Phase-5 conformance check that can fail before delivery.
  - **Triggers:** `/plugin-creator`, `/plugin-quick`, `"plugin this"`, `"make plugin"`, `"autobot transform"`, `"package this as a plugin"`, `"turn this into a plugin"`, `"scaffold a plugin"`.
  - **Slash command:** `/coeus:plugin-creator`.
  - **Argument hint:** `[idea, prompt, workflow, or existing folder to package as a Claude plugin]`.
  - Six phases: Intake & Classification → Canonical Layout → Optional Cleanup Hook → Build Scripts → Conformance Check → Documentation. Includes a migration patterns table for converting existing non-spec plugins.

### Fixed
- **Stale `caveman-protocol` namespace error documented in remote-environment trace** (`coeus_error.md`). Verified that the current Coeus repo (v3.4.0+) already uses `caveman` as the folder + frontmatter `name:`; the error originated from an older install in the user's `/mnt/skills/user/` environment. No code change required in the repo — the fix is delivered by re-installing the current `coeus.plugin`, whose SessionStart cleanup hook (introduced in v3.2.0) purges the stale `caveman-protocol/` directory on first session.

### Updated
- **`.claude-plugin/plugin.json`** — bumped to `3.5.0`; description now mentions `plugin-creator`.
- **`README.md`** — Skills Reference and Slash Commands tables updated with the new `plugin-creator` row.
- **`Coeus_LLM_HANDOVER.md`** — skills table extended; archive mirror at `//192.168.0.119/Big_Data_II/Claude/Archives` updated.

### Conformance
- 45/45 PASS against `anthropics/knowledge-work-plugins` standard with the new skill included (folder name matches frontmatter `name:`; description carries `Trigger on:` line; `argument-hint:` present; YAML parses).

---

## 2026-Jun-20 (v3.4.0) · 2026-Jun-20 13:00

### Removed
- **Root-level `plugin.json` mirror.** The canonical manifest lives at `.claude-plugin/plugin.json`. A duplicate at the repo root forced two-source-of-truth maintenance with no benefit. Deleted.
- **`commands/` directory** (6 wrapper `.md` files). Slash commands now auto-register from each skill's `SKILL.md` frontmatter (`name` + `argument-hint`) — matching the convention in `anthropics/knowledge-work-plugins`. The `argument-hint` values previously held in the wrappers were migrated into each skill's frontmatter.
- **`wiki/`** (5 files duplicating `docs/EP-Council*.md`). Wiki content belongs in the GitHub Wiki feature, not in the plugin tree. The four `docs/EP-Council*.md` are the canonical copies.
- **`skill_downloader.py`**. Obsolete since v3.2.0 when the official install path became `coeus.plugin` via Add Plugin. Anyone wanting individual `.skill` files now downloads them as Release assets.
- **`.github/workflows/sync-upstream-caveman.yml`**. Retired since v2.1.0 (superseded by `sync-upstream-skills.yml`); the dead file lingered in the repo.

### Changed
- **`.claude-plugin/plugin.json` slimmed to the official 4-key schema**: `{name, version, description, author{name, url}}`. Removed `slug`, `homepage` (folded into `author.url`), `license`, `skills[]`, `hooks`, `tracks_upstream`, `packaging`. Skills are auto-discovered from `skills/`. The displaced metadata is preserved in `docs/PLUGIN_MANIFEST_EXTENSIONS.md`.
- **`author` field converted to object** `{name, url}` from string, matching the official convention.
- **`hooks/cleanup-stale-install.{sh,ps1}` whitelist trimmed** — removed `commands`, `wiki`, `plugin.json`, `skill_downloader.py` from the canonical whitelist (so they get *purged* on upgrade from a v3.3.x install, completing the migration automatically).
- **`scripts/build-plugin.{sh,ps1}` updated** to bundle the new canonical layout (drops `commands/`, `plugin.json`, `skill_downloader.py`; adds `docs/`).
- **`.github/workflows/release.yml`** — bundle step updated to match; tag-vs-version assertion now checks only the canonical manifest (no reference copy to keep in sync).
- **Every SKILL.md gained `argument-hint:`** in frontmatter (caveman, ep-council, llm-council, morpheus, prompt-master, the-architect). Previously this field lived in the deleted `commands/*.md` wrappers.

### Added
- **`docs/CONFORMANCE_REPORT.md`** — full discrepancy matrix vs `anthropics/knowledge-work-plugins`. 16 axes audited; lists each fix taken and why.
- **`docs/COEUS_EXTENSIONS.md`** — documents the three deliberate divergences from the official spec (hooks/, Coeus_LLM_HANDOVER, upstream-tracked skills) with rationale for each.
- **`docs/PLUGIN_MANIFEST_EXTENSIONS.md`** — preserves the metadata displaced from the slimmed `plugin.json` (upstream-tracking provenance, packaging instructions, skill enumeration).
- Conformance test script (in maintainer's local toolchain, not bundled): 45 assertions covering manifest schema, deprecated paths, build artefacts, skill frontmatter, encoding, and hook resolvability. All pass.

### Why
- Coeus had drifted from the official `anthropics/knowledge-work-plugins` conventions over six version bumps. The accumulated extras (root manifest mirror, commands wrappers, wiki copy, downloader script, retired workflow, oversize manifest) didn't add functionality — they added maintenance surface and made Coeus visibly non-conforming to the reference standard. v3.4.0 brings the layout back in line with one decisive pass while preserving the three genuine Coeus extensions (cleanup hook for desktop-app overlay-install, LLM handover doc, vendored-with-sync upstream skills) under explicit documentation.

### Notes
- **Upgrade path**: on the first session after an in-place upgrade from v3.3.x, the SessionStart cleanup hook will purge the now-stale `commands/`, `wiki/`, `plugin.json`, `skill_downloader.py`, and any old `.coeus-cleaned-*` marker, then write `.coeus-cleaned-3.4.0`. No manual cleanup required.
- **Slash commands still resolve** as `/coeus:<skill>` — Claude Code auto-registers them from each skill's `name` field. The `argument-hint` carried over to the skill frontmatter so Cowork's UI still shows the argument prompt.
- The four `docs/EP-Council*.md` files remain at `docs/` for reference; they were already there independent of the deleted `wiki/` copies.

---

## 2026-Jun-20 (v3.3.1) · 2026-Jun-20 11:00

### Fixed
- **`commands/caveman.md` — YAML frontmatter parse error.** The `description:` value contained `Levels: lite, full (default), ultra, wenyan.` — an unquoted scalar with a colon-space that strict YAML parsers interpreted as the start of a nested mapping, producing `mapping values are not allowed here`. Wrapped the description in single quotes so colons inside are literal. Claude Code's command loader may be lenient enough to accept the original, but any strict-YAML tooling (linters, validators, future spec test suites) would reject it. See [docs/TEST_REPORT_v3.3.0.md](docs/TEST_REPORT_v3.3.0.md) Bug #1 for the full trace and audit (only `commands/caveman.md` was affected; the other 5 commands have no colon-space in their descriptions, and all 5 SKILL.md files using `description: >` folded block scalars are immune by construction).
- **`hooks/cleanup-stale-install.ps1` — safety-guard exit code.** When the hook is invoked outside a real plugin install dir (`.claude-plugin/plugin.json` missing), it correctly refused to delete anything — but `Write-Error` set `$LASTEXITCODE = 1` and (under the script's `$ErrorActionPreference = 'Stop'`) became terminating, never reaching `exit 0`. Claude Cowork's hook runner would then flag the hook as broken on every session start launched outside a Coeus install, surfacing a noisy stack trace. Replaced `Write-Error` with `[Console]::Error.WriteLine(...)` which mirrors the bash counterpart's `echo >&2` exactly — writes to stderr without raising, exit code stays 0. See [docs/TEST_REPORT_v3.3.0.md](docs/TEST_REPORT_v3.3.0.md) Bug #3.

### Added
- **`docs/TEST_REPORT_v3.3.0.md`** — full rigorous-test report for v3.3.0: stage map, all 46 assertion results, the three bugs found (2 fixed in this patch, 1 documented-but-not-fixed because the upstream sync would revert it), defensive tests (safety guard + idempotency), and a self-critique section listing five additional risks that didn't fail any check.

### Changed
- Both `plugin.json` files: `version` `3.3.0` → `3.3.1`.
- **Cleanup-hook marker GC.** Both `hooks/cleanup-stale-install.{sh,ps1}` now treat any `.coeus-cleaned-*` marker other than the current-version one as stale and delete it. Previously, the install dir accumulated one marker per upgrade (`.coeus-cleaned-3.2.0`, `.coeus-cleaned-3.3.0`, …); now it holds at most one. Verified end-to-end: injected two old markers (`3.2.0`, `3.3.0`) into a fresh v3.3.1 install, ran the hook → both removed, current `.coeus-cleaned-3.3.1` written.

### Notes
- No skill content changed; this is a patch for plugin-loading hygiene and hook robustness only.
- The cleanup hook in v3.3.1 will purge a stale `.coeus-cleaned-3.3.0` marker on first run after upgrade (markers are not whitelisted), then write a fresh `.coeus-cleaned-3.3.1` marker — same idempotency contract as before.

---

## 2026-Jun-19 (v3.3.0) · 2026-Jun-19 19:30

### Changed
- **EP-Council triggers** — `skills/ep-council/SKILL.md` (v1.5 → v1.6): natural-language triggers `"morpheus"` and `"architect"` removed; `"board review"` and `"investible"` added. The triggers now lean on the language EP investment teams actually use at the deal-screen stage and stop colliding with the `/coeus:morpheus` and `/coeus:the-architect` slash commands. README + wiki trigger tables updated to match.
- **Release version is now enforced as the source of truth.** `.github/workflows/release.yml` gained two new pre-flight steps:
  1. **Resolve release tag** — reads the tag from `release` events or `workflow_dispatch` input.
  2. **Assert plugin.json version matches release tag** — compares the tag (with optional leading `v` stripped) against the `version` field of *both* `.claude-plugin/plugin.json` and `plugin.json`. **Fails the workflow** if either disagrees with a clear "Bump both plugin.json files to X.Y.Z before re-running the release" message. This is the fix for "release not recognising actual release version" — the bundle that ships can no longer disagree with what the Release page advertises.
- **`.github/workflows/update-badge.yml` rewritten.** Now:
  - Writes a third gist file `coeus-release-count.json` for a new "release count" shields.io endpoint badge (paginates `/releases?per_page=100` until exhausted, with a 50-page guard against runaway pagination).
  - All release-event values (`tag_name`, `published_at`, repo, etc.) are passed via env vars and `set -eu` is enabled, eliminating shell-injection surface (best-practice — collaborator-controlled in a private repo, but cheap discipline).
  - Drops `actions/checkout` (the workflow only hits the API; no checkout needed).
  - Reduced `permissions:` to `contents: read`.
  - Adds the GitHub API version header (`X-GitHub-Api-Version: 2022-11-28`).
- **`README.md` + `wiki/Home.md`** — added the release-count badge under the title; updated badge-block prose; documented the version-vs-tag assertion; bumped the EP-Council trigger table.
- **`Coeus_LLM_HANDOVER.md`** (renamed from `HANDOVER.md`) — version bump, archive-mirror pointer, refs to itself updated. The repo copy is canonical; a snapshot lives at `//192.168.0.119/Big_Data_II/Claude/Archives/Coeus_LLM_HANDOVER.md`.

### Added
- **Release-count badge** — third gist-driven shields.io endpoint badge, refreshed by `update-badge.yml` on every Release. Useful at a glance ("how active is this plugin"); cheaper than scraping a GitHub UI page.

### Security
- **`skill_downloader.py`** — defence-in-depth against CVE-2007-4559 (tar-slip / Zip Slip). Both extraction sites (`build_skill_from_tarball`, `package_external_skill`) now:
  - **Skip non-regular tar members** (`if not member.isreg(): continue`) so symlinks, hardlinks, device nodes, and directories never become entries in the produced `.skill` ZIP.
  - **Explicitly reject** any path that starts with `/` or contains a `..` segment, in addition to the existing dotfile filter. End users extract these `.skill` ZIPs into their Claude Desktop install dir, so a malicious upstream tarball must not be able to write outside that dir.
- **`.github/workflows/release.yml`** — the new tag/version assertion step passes values via `env:` rather than embedding `${{ }}` expressions directly into the `run:` script. Same hardening as `update-badge.yml`.

### Renamed
- `HANDOVER.md` → `Coeus_LLM_HANDOVER.md`. All packaging manifests, hooks (`hooks/cleanup-stale-install.{sh,ps1}` whitelist), build scripts, and the release workflow updated. On in-place upgrade from v3.2.0, the SessionStart cleanup hook will treat the stale `HANDOVER.md` in the install dir as not-whitelisted and remove it automatically — no manual cleanup required.

### Notes
- The cleanup-hook whitelist now ends with `Coeus_LLM_HANDOVER.md` instead of `HANDOVER.md`. Future renames must propagate to: `hooks/cleanup-stale-install.sh`, `hooks/cleanup-stale-install.ps1`, both `plugin.json` files (packaging commands), `.github/workflows/release.yml`, and `scripts/build-plugin.{sh,ps1}`.
- The release-count badge will read `0 total` until the next published Release triggers `update-badge.yml`. Either tag-and-release `v3.3.0` (best) or run the workflow manually via `workflow_dispatch` to backfill against the latest existing Release.

---

## 2026-Jun-19 (v3.2.0) · 2026-Jun-19 18:30

### Added
- **Clean-install hook.** New `hooks/hooks.json` registers a `SessionStart` hook (`hooks/cleanup-stale-install.sh`, plus a PowerShell mirror) that runs once per version on the first session after install. The hook deletes any file or directory in the plugin install root that isn't part of the canonical v3.x layout — so when a user re-uploads an updated `coeus.plugin` via **Claude Desktop → Settings → Capabilities → Customize → Add Plugin**, stale leftovers from prior versions are purged automatically. Idempotent (writes `.coeus-cleaned-<version>` marker), safe-by-default (refuses to run if `.claude-plugin/plugin.json` is missing).
- **`scripts/build-plugin.sh` + `scripts/build-plugin.ps1`.** Reproducible local builds that produce `dist/coeus.plugin` containing ONLY the canonical layout — so manual builds match the release-workflow output. PowerShell mirror provided for Windows.
- **`.gitignore`.** Now ignores build artefacts (`*.skill`, `coeus.plugin`, `dist/`), `__pycache__`, editor cruft.

### Removed
- **Committed root-level `.skill` baselines** (`caveman.skill`, `ep-council.skill`, `llm-council.skill`, `morpheus.skill`, `prompt-master.skill`, `the-architect.skill`). These were stale build outputs that bloated the repo and confused the desktop-app install (they ended up extracted into the plugin install dir on every upload, even though `coeus.plugin` v3.1.0 already excluded them from the bundle). They're now generated fresh by `release.yml` on every Release and uploaded as Release assets, or built locally with `scripts/build-plugin.*`.

### Changed
- **`.claude-plugin/plugin.json` + `plugin.json`** — `version` `3.1.0` → `3.2.0`; added `"hooks": "hooks/hooks.json"`; packaging commands updated to include `hooks/`, `scripts/`, `CHANGELOG.md`, `HANDOVER.md`, and the root `plugin.json` reference copy.
- **`.github/workflows/release.yml`** — `coeus.plugin` bundle step now includes `hooks/`, `scripts/`, `CHANGELOG.md`, `HANDOVER.md`, and the root `plugin.json`.

### Why
- Before v3.2.0, "Add Plugin" via the desktop app did an overlay-extract: it wrote the new ZIP's files into the existing install dir but did not remove files that had been deleted between versions. Re-uploading a fresh `coeus.plugin` would still leave behind the old root-level `.skill` files (and, hypothetically, any retired skill folder from a future restructure). The new SessionStart hook makes the upload behave like a replace-install: anything outside the canonical whitelist is purged on the next session start. This means **the installed version always matches the uploaded ZIP** — no stale duplicates, no orphaned skills, no two-versions-of-the-same-skill bugs.

### Notes
- The cleanup hook's whitelist is hard-coded in `hooks/cleanup-stale-install.sh` (and `.ps1`). Any future top-level addition to the canonical layout must also be added there, otherwise the hook will delete it on the next session start. The whitelist currently covers: `.claude-plugin`, `commands`, `skills`, `hooks`, `scripts`, `assets`, `docs`, `wiki`, `plugin.json`, `skill_downloader.py`, `README.md`, `CHANGELOG.md`, `HANDOVER.md`, `CONTRIBUTING.md`, `CLA.md`, `LICENSE`, `.gitattributes`, `.gitignore`.
- Removing the `.coeus-cleaned-<version>` marker forces a re-clean on the next session start — useful for debugging.

---

## 2026-Jun-19 (v3.1.0) · 2026-Jun-19 17:30

### Changed
- **Repo restructured to the Claude Code plugin spec.** All six skill directories moved from the repo root into `skills/`:
  - `caveman/` → `skills/caveman/`
  - `ep-council/` → `skills/ep-council/`
  - `llm-council/` → `skills/llm-council/`
  - `morpheus/` → `skills/morpheus/`
  - `prompt-master/` → `skills/prompt-master/` (with `references/` preserved)
  - `the-architect/` → `skills/the-architect/`
  Moves done via `git mv` so history is preserved.
- **`.claude-plugin/plugin.json` + `plugin.json`** — `version` `3.0.1` → `3.1.0`; `skills` array entries now use `"skills/<name>"` paths (e.g. `"skills/the-architect"`); packaging commands collapsed to `skills/` instead of six per-skill paths.
- **`.github/workflows/release.yml`** — `coeus.plugin` bundle step now zips `skills/` as a single tree; per-skill `.skill` artefacts are now built from `skills/<name>/` (zipped from inside `skills/` so the archive layout stays `<name>/SKILL.md`); upstream replace step swaps `skills/caveman/` and `skills/prompt-master/` in place.
- **`.github/workflows/sync-upstream-skills.yml`** — `local_dir` for both upstream-tracked skills updated to `skills/caveman` and `skills/prompt-master`.
- **README.md + wiki/Home.md** — Repo Structure tree updated; manual packaging commands (bash + PowerShell) updated; plugin-spec note clarified.

### Why
- Coeus shipped with skills at the repo root (`<plugin>/<skill>/SKILL.md`). The Claude Code plugin spec expects skills under `<plugin>/skills/<skill>/SKILL.md`. On install, Claude Cowork registered the plugin but skipped skill auto-discovery, so even the slash-command wrappers (`/coeus:the-architect`, `/coeus:morpheus`, …) failed to resolve with `Unknown command: /coeus:the-architect`. Moving the six dirs into `skills/` brings the layout to spec; the slash commands resolve and the skills register cleanly on any machine.

### Added
- **`HANDOVER.md`** — LLM handover note covering current architecture, install paths, packaging steps, and the rationale for the v3.1.0 restructure.

### Notes
- The committed `*.skill` zip baselines at the repo root (`caveman.skill`, `the-architect.skill`, etc.) are still single-skill packages; their internal layout is unchanged (`<skill>/SKILL.md`). Only `coeus.plugin` was affected by the restructure.
- `skill_downloader.py` was already layout-agnostic (locates `SKILL.md` by suffix match in the upstream tarball), so no code change was needed.

---

## 2026-Jun-19 (v3.0.1) · 2026-Jun-19 12:45

### Changed
- **Version → 3.0.1** in both `.claude-plugin/plugin.json` and `plugin.json`. The distributed zip was labelled `Coeus-3.0.1` while the manifest still read `2.1.0`; the manifest is the source of truth, so the installed plugin reported 2.1.0. Now aligned.
- **Skill `name` fields normalised to their kebab folder names** (official skill-guide convention; makes `/coeus:<name>` predictable): `LLM-council` → `llm-council`, `caveman-protocol` → `caveman`. The other four already matched. Command wrappers and dependency references updated to the new names.
- **`.github/workflows/sync-upstream-skills.yml`** — added a post-sync **name-normalisation** step so upstream-synced skills (`caveman`, `prompt-master`) keep their Coeus folder-matching `name:` instead of reverting to the upstream value each weekly sync.
- **README.md + wiki/Home.md** — skill-name references (`caveman`, `llm-council`) and version updated.

### Why
- All six skills loaded on install, but `/coeus:caveman` and `/coeus:llm-council` could not resolve because those skills’ `name:` fields were `caveman-protocol` / `LLM-council`, not the folder/command name. Aligning the names removes that mismatch. (Whether a given surface exposes plugin slash commands at all is separate; in chat surfaces, invoke skills by intent.)

---

## 2026-Jun-18 (v2.1.0) · 2026-Jun-18 12:45

### Added
- **`commands/` directory (NEW) — six slash-command wrappers.** Adds `/coeus:llm-council`, `/coeus:morpheus`, `/coeus:the-architect`, `/coeus:ep-council`, `/coeus:caveman`, `/coeus:prompt-master`. Root cause of the prior `"/coeus:the-architect → Unknown command"` (and `/coeus:morpheus`) failures: the plugin shipped Skills only, with no `commands/` dir — typeable slash commands are sourced from `commands/*.md`. Each wrapper is a thin loader (`description` + `argument-hint` frontmatter) mirroring the bigdata-com command format. `caveman.md` loads the `caveman` skill; `llm-council.md` loads the `llm-council` skill.
- **`prompt-master.skill`** — Regenerated baseline package added at repo root (previously absent), so all six skills now ship a committed `.skill`.

### Changed
- **`.claude-plugin/plugin.json` + `plugin.json`** — `version` `1.1.0` → `2.1.0`; packaging commands now include `commands/` so the wrappers ship in manually-built `coeus.plugin` archives.
- **`.github/workflows/release.yml`** — `coeus.plugin` bundle step now includes `commands/`, so released plugins register the slash commands.
- **`skill_downloader.py`** — Added `upstream_path` to `EXTERNAL_SKILLS` (`prompt-master` = `""`, `caveman-protocol` = `"skills/caveman"`); `package_external_skill()` now keeps only that subtree and strips the prefix so `SKILL.md` lands at `caveman-protocol/SKILL.md` (previously the whole upstream repo was nested under the skill). prompt-master description `v1.6+` → `v1.7+`.
- **`skill_downloader.py` — single-skill download reworked to release-first.** Each selected Coeus skill is now pulled from the latest GitHub Release's `{skill}.skill` asset, falling back to a **layout-agnostic** build from the `main` tarball (locates the skill dir by suffix match). Added a baked-in `STATIC_SKILLS` fallback registry (menu browses with no auth) and a `--source release|main` flag; OAuth (`repo` scope) is requested lazily, only when a skill is actually fetched.
- **`README.md` + `wiki/Home.md`** — Added a **Slash Commands** section documenting the `/coeus:<name>` commands; added `commands/` to Repo Structure; manual packaging commands updated to include `commands/`; documented the release-first Skill Downloader and its `--source release|main` flag.

### Fixed
- **`ep-council/SKILL.md`** — added missing `version: 1.5` to frontmatter.
- **`skill_downloader.py` Option 3 (Coeus private-repo skills) was broken** — `list_skills()` / `package_skill()` assumed a `skills/{skill}/` layout that does not exist (skills live at the repo root), so Coeus-skill downloads 404'd / found nothing. Replaced with the release-first + layout-agnostic resolver above; the `--external` upstream path is retained.

### Notes
- **`ep-council` `"morpheus"` / `"architect"` natural-language triggers are intentional** (bare words → EP-Council; `/coeus:*` slash commands → the pipeline skills). Left as designed.

---

## 2026-Jun-18 (session 9) · 2026-Jun-18 08:57

### Verified / Docs
- **Verification pass — no source changes.** `Inputs/` empty; the session-8 bundle was re-confirmed intact (no merge required). Re-confirmed both access constraints: git checkout (`...OneDrive\Documents\GitHub\Coeus`) and network share (`\\192.168.0.119\...`) are both unreachable from the Cowork session.
- **`Coeus_HANDOVER.md`** — Advanced to session 9: added a verification block, the staged `robocopy /MOV` command to move the note to the network-share archive, and an explicit status line (bundle staged ✅ · repo push pending ⏳ · note move pending ⏳).

---

## 2026-Jun-18 (session 8) · 2026-06-18 08:03

### Added
- **`prompt-master/`** — Prompt-master is now **bundled and auto-installed exactly like caveman** (previously a manual prerequisite). Committed `prompt-master/SKILL.md` (v1.7.0) + `references/patterns.md` + `references/templates.md`, mirrored from [nidhinjs/prompt-master@main](https://github.com/nidhinjs/prompt-master).
- **`.github/workflows/sync-upstream-skills.yml`** — New unified **directory-level** upstream sync (matrix: caveman + prompt-master). Replaces the single-file caveman sync with a method that mirrors the entire upstream skill directory (so multi-file skills like prompt-master stay complete). Coeus wrapper docs (README/LICENSE/CONTRIBUTING/CLA) are preserved. Runs weekly (Mon 09:00 UTC) and on demand; `max-parallel: 1` + `git pull --rebase` to avoid push races.
- **`.github/upstream-prompt-master-sha.txt`** — Sync tracking file seeded to upstream commit `d15eabbe` so the first scheduled run is a no-op.
- **`.github/workflows/update-badge.yml`** — Un-retired. Drives the README release + release-date badges from a public Gist on every published release (see Fixed below).

### Changed
- **`.github/workflows/sync-upstream-caveman.yml`** — **Retired** (tombstone). Superseded by `sync-upstream-skills.yml`, which directory-syncs caveman with the same better method, as requested. No scheduled trigger remains.
- **`.github/workflows/release.yml`** — `coeus.plugin` now bundles **all six skills**: prompt-master is fetched from upstream `main` at release time and swapped into the bundle (same mechanism already used for caveman) and added to the plugin ZIP file list and release-summary table.
- **`.claude-plugin/plugin.json`** and **`plugin.json`** (reference copy):
  - Added `"prompt-master"` to the `skills` array (now six skills).
  - Replaced the `prerequisites` block with a `tracks_upstream` block documenting both caveman and prompt-master (source, branch, upstream path, sync + release workflows). prompt-master `latest_version` → `1.7.0`.
  - Packaging commands updated to include `prompt-master/`.
  - `version` bumped `1.0.0` → `1.1.0` (new bundled skill).
  - Top-level `description` updated to note prompt-master is bundled and auto-synced.
- **`README.md`**:
  - **Fixed broken release badge** — replaced the native `shields.io/github/v/release/keithceh/Coeus` badge (which renders "no releases / repo not found" because Coeus is a **private** repo and shields.io cannot read private repos) with two **shields.io endpoint badges** backed by a public Gist: a **release** version badge and a **released** date badge in `YYYY-MM-DD` format. Both auto-update on every release via `update-badge.yml`.
  - Notes, Prerequisites, Install Order, Options 1–4, and Repo Structure updated to reflect prompt-master as a bundled, auto-synced skill (no separate install when using the plugin). prompt-master version references `v1.6+` → `v1.7+`. Added the two upstream-SHA tracking files and the new/retired workflows to Repo Structure.
- **`wiki/Home.md`** — Prerequisites (both skills bundled + auto-synced, replacing the "Cowork marketplace" wording), Installation options, and Repo Structure brought in line with the README; prompt-master version updated; badge note added.

### Fixed
- **README header badge error "no releases or repo not found"** — root cause identified as repo privacy (native shields.io cannot read private repos). Resolved via the Gist-endpoint badge approach above, which works while the repo stays private and auto-updates with each release.

### Setup required (one-time, by maintainer)
- Add repo secret **`GIST_TOKEN`** (PAT with `gist` scope, owned by `keithceh`) so `update-badge.yml` can write the badge Gist `9d9181a0691bac7053e355ade3e9bd01`. See `APPLY_THESE_CHANGES.md`.

---

## 2026-Jun-17 (session 7)

### Fixed
- **Plugin install error: "No skills found in specified directories"** — Claude treats `skills` entries as directory paths and looks for `SKILL.md` inside them. Skills array changed from explicit file paths (`"llm-council/SKILL.md"`) to bare directory names (`"llm-council"`).
  - Both `.claude-plugin/plugin.json` (canonical) and root `plugin.json` (reference copy) updated.
  - **`README.md`** — Option 4 schema requirements note updated with correct format.
  - **`wiki/Home.md`** — Plugin schema requirements note updated; Repo Structure section updated to include `.claude-plugin/`, `plugin.json`, `CHANGELOG.md`, `caveman/`, `skill_downloader.py`, and GitHub Actions workflows (was missing these entries).

---

## 2026-Jun-17 (session 6)

### Fixed
- **Plugin install errors — schema compliance:**
  - `name` field changed from `"Coeus"` to `"coeus"` — Claude rejects names with uppercase letters
  - `skills` array changed from array-of-objects (with `name/path/description/triggers` keys) to flat array-of-strings (`"skillname/SKILL.md"`) — Claude reads skill metadata from each SKILL.md directly, not from plugin.json
  - Both `.claude-plugin/plugin.json` (canonical) and root `plugin.json` (reference copy) updated
  - Errors fixed: *"Plugin name can only contain lowercase letters, numbers, and hyphens"* and *"skills list items must be strings at index N, got dict"*
- **`README.md`** — Option 4 packaging note expanded with full plugin.json schema requirements (name format, skills array format)
- **`wiki/Home.md`** — Installation section rewritten to match current install options (plugin, individual skills, manual clone); schema requirements noted

---

## 2026-Jun-17 (session 5)

### Fixed
- **Plugin install error: "Zip must contain a .claude-plugin/plugin.json file"** — Claude requires the plugin manifest at `.claude-plugin/plugin.json` inside the ZIP, not at the root.
  - **`.claude-plugin/plugin.json`** — New canonical manifest location. Content identical to root `plugin.json`; packaging commands updated to reference `.claude-plugin/` path.
  - **`plugin.json`** (root) — Updated packaging note to clarify this is a human-readable reference copy only; `.claude-plugin/plugin.json` is canonical.
  - **`.github/workflows/release.yml`** — `zip` command updated: replaced `plugin.json` with `.claude-plugin/` so the plugin bundle contains the manifest at the correct path.
  - **`README.md`** — Repo Structure updated to show `.claude-plugin/` directory; Option 4 manual packaging instructions updated with correct ZIP commands and a warning note about the `.claude-plugin/` path requirement.

---

## 2026-Jun-17 (session 4)

### Changed
- **`wiki/Home.md`** — Removed KC-modified caveman additions block (§3 Workspace Memory Map, §4 Secure Micro-Subagent Roles, §5 Hardened Auto-Clarity Circuit Breaker). Replaced with pointer to JuliusBrussee/caveman@main and note that Coeus auto-syncs weekly.
- **`.github/PULL_REQUEST_TEMPLATE.md`** — Removed checklist items and Affected Sections entries referencing §3/§4/§5 (KC-specific additions that no longer exist in Coeus). Retained §3 entry renumbered to reflect upstream's native circuit breaker section.
- **`README.md`** — Added native GitHub release badge (`shields.io/github/v/release/keithceh/Coeus`); removed Gist-backed "Last Commit" badge.
- **`.github/workflows/update-badge.yml`** — Retired; overwritten with notice. Replaced by native GitHub releases badge (no workflow required).

---

## 2026-Jun-17 (session 3)

### Changed
- **`caveman/SKILL.md`** — KC-modified version superseded. Caveman now tracks [JuliusBrussee/caveman@main](https://github.com/JuliusBrussee/caveman) directly. Future improvements follow upstream.
- **`.github/workflows/sync-upstream-caveman.yml`** — Changed from opening a draft PR for manual review to directly committing upstream `SKILL.md` to `main` on each weekly sync. No manual merge step required.
- **`.github/workflows/release.yml`** — `caveman.skill` now built from upstream fetch rather than local `caveman/` dir. Removed `caveman-upstream` naming distinction. Simplified release artifacts: `coeus.plugin`, 5 Coeus `.skill` files, `prompt-master.skill`.
- **`plugin.json`** — Caveman description updated to reflect upstream tracking.
- **`README.md`** — Removed all KC-modified references for caveman. Updated caveman section, install order table, Option 1 (Plugin), Option 2 (Releases), Option 3 (Skill Downloader). Removed `--external caveman-protocol` from downloader docs.

---

## 2026-Jun-17 (session 2)

### Added
- **`.github/workflows/release.yml`** — CI_BUNDLE release workflow. On every GitHub release (or manual `workflow_dispatch`), automatically fetches latest `main` from `nidhinjs/prompt-master` and `JuliusBrussee/caveman`, packages each as a `.skill` ZIP, bundles all Coeus skills + prerequisites into `coeus.plugin`, and attaches all artifacts to the release. Eliminates the need for manual prerequisite install steps.

### Changed
- **`README.md`** — Installation section updated to reflect auto-bundled prerequisites:
  - Option 1 (Plugin Install) now describes downloading `coeus.plugin` from Releases (batteries included); documents the `bundled-prerequisites/` directory inside the plugin ZIP; explains how the CI workflow works.
  - Option 2 (GitHub Releases) now lists `prompt-master.skill` and `caveman-upstream.skill` as auto-built release artifacts.
  - Repo Structure updated to show all three workflow files.
- **`CHANGELOG.md`** — This entry.

All notable changes to Coeus are documented here.

---

## 2026-Jun-17 12:37

### Added
- **`plugin.json`** — Plugin manifest converting Coeus into a Claude plugin. Lists all 5 skills (llm-council, morpheus, the-architect, ep-council, caveman) with trigger keywords, inter-skill dependencies, and packaging commands for building `coeus.plugin`.
- **`CHANGELOG.md`** — This file. Full change history.
- **`skill_downloader.py` — `--external` mode** — New flag to download external prerequisite skills from public GitHub repos without OAuth. Supports `prompt-master` (nidhinjs/prompt-master, main branch) and `caveman-protocol` (JuliusBrussee/caveman, upstream original). Usage: `python3 skill_downloader.py --external [skill-name]`.

### Changed
- **`README.md`** — Major update:
  - Installation section restructured: Plugin install (Option 1) added as primary method; former options renumbered (Options 2–4); Skill Downloader section expanded to document `--external` flag for prerequisites.
  - Prerequisites section expanded with dedicated "Installing prompt-master (latest version)" subsection covering CLI (Option A) and manual ZIP (Option B) install paths.
  - "Issues and Planned Improvements" section replaced with "Changelog" (link to this file) and "Notes" (resolved/ongoing context).
  - Repo Structure updated to show `plugin.json`, `CHANGELOG.md`, `caveman/`, and `skill_downloader.py`.

### Notes
- prompt-master (nidhinjs/prompt-master) has no formal releases or tags; latest version (v1.6+) is always on `main` branch. Install instructions now reflect this.
- Caveman bundled in Coeus is the KC-modified version. The `--external caveman-protocol` flag downloads the upstream original from JuliusBrussee/caveman if needed.

---

## Prior History

Coeus is a rolling mono-repo. Changes before 2026-Jun-17 are tracked via Git commit history at https://github.com/keithceh/Coeus/commits/main.
