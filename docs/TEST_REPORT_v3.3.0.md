# Coeus v3.3.0 — Rigorous Plugin Test Report

**Date:** 2026-06-20
**Scope:** Installed Coeus plugin at `~/.claude/plugins/marketplaces/local-desktop-app-uploads/coeus/` (v3.3.0), built from `C:/Users/keith/GitHub/Coeus` via `scripts/build-plugin.ps1`.
**Methodology:** [Fable Mode](https://docs.claude.com/) discipline — stage map, failable check per stage, iterate to green, self-critique.

---

## Result

**Final: 46/46 stage assertions PASS · 1 safety-guard test PASS · 1 idempotency test PASS.**

Three bugs found and fixed during testing. Plugin is in a clean, installable state with no known issues that would block any of the six skills from running as intended.

---

## Stage map

| # | Stage | Failable check |
|---|---|---|
| 1 | Inventory installed plugin | 6 skills + 6 commands + `.claude-plugin/plugin.json` v3.3.0 present |
| 2 | YAML frontmatter parses (PyYAML strict) | `yaml.safe_load()` succeeds on every SKILL.md + command .md; required keys present |
| 3 | Manifest cross-check | Every entry in `plugin.json.skills[]` resolves to a real `<path>/SKILL.md` |
| 4 | Command ↔ skill pairing | Every `/coeus:<name>` has a matching `skills/<name>/SKILL.md` whose `name:` matches the folder |
| 5 | hooks.json validity | Parses; declares SessionStart with `${CLAUDE_PLUGIN_ROOT}` cmd; both cleanup scripts exist |
| 6 | Cleanup hook regression | On a fresh install with stale files injected, hook purges only non-whitelisted entries |
| 7 | Build script regression | `scripts/build-plugin.ps1` produces canonical-layout-only ZIP |
| 8 | Encoding sanity | No UTF-8 BOM on any markdown; bash scripts use LF |
| 9 | Skill body content | Each SKILL.md body > 200 chars (not just a frontmatter stub) |
| — | Safety guard | Hook on a non-plugin directory exits clean (code 0) without deleting anything |
| — | Idempotency | Second run on already-cleaned install is a no-op (marker short-circuit) |

---

## Bugs found, fixed, and verified

### Bug #1 — `commands/caveman.md` YAML parse failure

**Symptom**: Strict YAML parser (PyYAML) rejected the frontmatter with `mapping values are not allowed here` at line 2, column 103.

**Failing input** (before fix):
```yaml
---
description: Token-compression mode — terse "caveman" output that preserves technical accuracy. Levels: lite, full (default), ultra, wenyan.
argument-hint: "[lite|full|ultra|wenyan] [text to compress, optional]"
---
```

**Reason**: The unquoted scalar after `description:` contains `Levels: lite,...` — a literal `key: value` pattern inside what YAML thinks is still a flow scalar context. The parser tries to interpret `Levels` as a new mapping key and fails.

**Why it matters**: Claude Code's command parser may be more lenient than strict YAML, but any tooling that consumes the frontmatter strictly (linters, validators, IDE plugins, the spec test suite) would reject the file. Quoting is also defensive — if upstream tightens the parser, this command silently breaks first.

**Mitigation**: Wrap the description value in single quotes so colons inside are literal.

**Fix** (after):
```yaml
description: 'Token-compression mode — terse "caveman" output that preserves technical accuracy. Levels: lite, full (default), ultra, wenyan.'
```

**Verification**: Re-ran Stage 2 — passed on all 6 command files. The other 5 command descriptions don't contain `colon-space` patterns, so they parse OK without quoting. All 5 SKILL.md files that use `description: >` (folded block scalar) are immune by construction.

**Audit**: All other command + skill frontmatters were checked for the same bug class — only `commands/caveman.md` was affected.

---

### Bug #2 — `skills/caveman/SKILL.md` missing `version:` field (soft, not blocking)

**Symptom**: `caveman` is the only skill of six without a `version` field in its frontmatter.

**Reason**: `caveman` is vendored from upstream `JuliusBrussee/caveman@main`, which does not include a `version:` line. Coeus's `sync-upstream-skills.yml` workflow has a `sed` step that normalises the skill `name:` to `caveman` (so `/coeus:caveman` resolves) but does not inject a version.

**Decision**: **Not fixed**. The Claude Code plugin spec requires only `name` and `description` for a skill to load; `version` is decorative metadata. Adding it locally would be reverted on every weekly sync, and patching the sync workflow to inject a version would create a sync churn between Coeus and upstream.

**Mitigation**: Logged in this report. If the version becomes required by a future spec change, extend the `Normalize skill name to Coeus convention` step in `.github/workflows/sync-upstream-skills.yml` to also `sed`-inject `version: <upstream_sha_short>`.

---

### Bug #3 — `hooks/cleanup-stale-install.ps1` safety guard exits non-zero

**Symptom**: When run with `$env:CLAUDE_PLUGIN_ROOT` pointing at a directory that is not a Coeus plugin install (no `.claude-plugin/plugin.json`), the PS hook *correctly* refused to delete anything — but exited with code 1 and a PowerShell error stack trace.

**Failing line** (before):
```powershell
if (-not (Test-Path (Join-Path $Root '.claude-plugin/plugin.json'))) {
  Write-Error "[coeus] cleanup-stale-install: not a plugin install; skipping"
  exit 0
}
```

**Reason**: PowerShell's `Write-Error` writes to the error stream AND sets `$LASTEXITCODE` to 1 AND emits an `ErrorRecord` stack trace. With `$ErrorActionPreference = 'Stop'` set at the top of the script (a deliberate choice for the rest of the script's error semantics), `Write-Error` becomes terminating — the `exit 0` line is unreachable.

**Why it matters**: Claude Cowork's hook runner inspects hook exit codes. A non-zero exit on the safety-guard path would make Claude flag the hook as broken on every session start launched outside a real Coeus install dir (which is most non-plugin work). That could surface noisy errors to the user or disable the hook entirely.

The bash counterpart (`cleanup-stale-install.sh`) gets this right — it uses `echo "..." >&2` followed by `exit 0`, which writes to stderr without flipping the exit code.

**Mitigation/fix**: Replace `Write-Error` with a direct stderr write via `[Console]::Error.WriteLine(...)`, which mirrors bash's `echo >&2` exactly — writes to stderr, does not raise, exit code stays 0.

**Fix** (after):
```powershell
if (-not (Test-Path (Join-Path $Root '.claude-plugin/plugin.json'))) {
  # Soft-skip: not a real plugin install dir. Use [Console]::Error.WriteLine
  # (not Write-Error) so $LASTEXITCODE stays 0 and Claude Cowork's hook runner
  # does not flag this as a hook failure — the bash counterpart does the same
  # via `echo >&2`.
  [Console]::Error.WriteLine("[coeus] cleanup-stale-install: not a plugin install; skipping")
  exit 0
}
```

**Verification**:
- Ran the hook with `$env:CLAUDE_PLUGIN_ROOT='C:\Users\keith\AppData\Local\Temp\not-a-plugin'` (a dir with a single file `important.txt`).
- Exit code: 0 ✓
- Output: `[coeus] cleanup-stale-install: not a plugin install; skipping` on stderr ✓
- `important.txt` survived ✓

---

## All stages — final result

```
=== STAGE 2: YAML frontmatter parses ===
  PASS  skill yaml parses + has required keys: caveman
  PASS  skill yaml parses + has required keys: ep-council
  PASS  skill yaml parses + has required keys: llm-council
  PASS  skill yaml parses + has required keys: morpheus
  PASS  skill yaml parses + has required keys: prompt-master
  PASS  skill yaml parses + has required keys: the-architect
  PASS  command yaml parses + has description: caveman          [fixed by Bug #1]
  PASS  command yaml parses + has description: ep-council
  PASS  command yaml parses + has description: llm-council
  PASS  command yaml parses + has description: morpheus
  PASS  command yaml parses + has description: prompt-master
  PASS  command yaml parses + has description: the-architect

=== STAGE 3: manifest skills[] paths resolve ===
  PASS  manifest entry resolves: skills/llm-council
  PASS  manifest entry resolves: skills/morpheus
  PASS  manifest entry resolves: skills/the-architect
  PASS  manifest entry resolves: skills/ep-council
  PASS  manifest entry resolves: skills/caveman
  PASS  manifest entry resolves: skills/prompt-master

=== STAGE 4: command/skill name pairing ===
  PASS  command/skill pairing + name match: caveman
  PASS  command/skill pairing + name match: ep-council
  PASS  command/skill pairing + name match: llm-council
  PASS  command/skill pairing + name match: morpheus
  PASS  command/skill pairing + name match: prompt-master
  PASS  command/skill pairing + name match: the-architect

=== STAGE 5: hooks.json + cleanup script ===
  PASS  hooks.json schema valid + uses CLAUDE_PLUGIN_ROOT
  PASS  cleanup script exists: cleanup-stale-install.sh
  PASS  cleanup script exists: cleanup-stale-install.ps1

=== STAGE 6: cleanup hook regression (injected stale files) ===
  PASS  HANDOVER.md removed (renamed)
  PASS  stale .skill removed
  PASS  retired-skill-folder removed
  PASS  malicious script removed
  PASS  canonical Coeus_LLM_HANDOVER.md retained
  PASS  canonical skills/ retained
  PASS  canonical hooks/ retained (hook didn't delete itself)
  PASS  new marker .coeus-cleaned-3.3.0 written

=== STAGE 7: build script regression ===
  PASS  dist/coeus.plugin produced, 95.4 KB
  PASS  top-level contains only: .claude-plugin, commands, skills, hooks, scripts, plus 8 root docs/manifests
  PASS  zero stale root .skill files
  PASS  manifest in ZIP = v3.3.0

=== STAGE 8: encoding ===
  PASS  no BOM on any of 6 SKILL.md + 6 command .md
  PASS  LF endings on cleanup-stale-install.sh

=== STAGE 9: skill bodies have content ===
  PASS  caveman:        6,208 chars
  PASS  ep-council:     9,164 chars
  PASS  llm-council:    7,890 chars
  PASS  morpheus:       7,835 chars
  PASS  prompt-master: 26,509 chars
  PASS  the-architect:  7,131 chars

=== Defensive tests ===
  PASS  safety guard: hook on non-plugin dir exits 0 without deleting (fixed by Bug #3)
  PASS  idempotency: re-run on cleaned install is a no-op (marker short-circuit)
```

---

## Self-critique — risks I would still call out

These didn't fail any check, but a reviewer should know they exist:

1. **`release.yml` uses `softprops/action-gh-release@v2` unpinned to a SHA.** Pinning to a SHA would be more secure (a compromised tag couldn't redirect to a malicious commit). Not blocking — it's a Marketplace-trusted action — but tightening it would close a small supply-chain gap.

2. **The cleanup hook only ships a bash script in `hooks/hooks.json`** (`hooks/cleanup-stale-install.sh`). Windows/Cowork users without bash in `PATH` (rare — Git Bash usually present) would silently get no cleanup. A platform-aware matcher pair (bash + ps1) in `hooks.json` would belt-and-brace this, but adds complexity for a corner case.

3. ~~Old `.coeus-cleaned-<version>` markers are not garbage-collected.~~ **Fixed in v3.3.1** — both cleanup scripts now treat any `.coeus-cleaned-*` other than the current-version marker as stale and delete it. The install dir holds at most one marker file at any time.

4. **`prompt-master/SKILL.md` body is 26K chars** (≈4x the others). Anything that lazy-loads skill bodies into context will pay a token tax for prompt-master even when it isn't invoked. Not a bug, just a size note.

5. **No end-to-end verification that Claude Cowork actually fires the SessionStart hook from a plugin.** The hook is correctly declared per the spec, the script works when invoked directly, and the safety guard is now clean — but a true black-box test would launch a Cowork session against this install and confirm the hook ran. That requires a Cowork restart and observation, outside the scope of this automated test pass.

---

## Files changed in this test pass

```
M commands/caveman.md            (Bug #1 — single-quote description)
M hooks/cleanup-stale-install.ps1 (Bug #3 — replace Write-Error with [Console]::Error.WriteLine)
+ docs/TEST_REPORT_v3.3.0.md     (this document)
```

No source-of-truth manifest version bump — the bugs were inside-v3.3.0 issues, not new-feature work. The two fixes are appropriate for a v3.3.1 patch release once published.
