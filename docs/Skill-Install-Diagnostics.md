# Skill Install Diagnostics

> If Coeus skills appear in the index but fail to load — or fire from memory instead of the real protocol — you have hit a path-mismatch bug. This doc explains how to diagnose and work around it.

---

## Known Bug — Remote-environment path mismatch

**Symptom.** The skill index lists each Coeus skill as `/mnt/skills/plugins/coeus:<name>/SKILL.md`, but that directory does not exist. The real files are under `/mnt/skills/user/<name>/`. Any tool that trusts the indexed path errors with `No such file or directory`. The skill itself still "fires" from the in-memory description, but **without the actual protocol loaded** — runs skip mandated steps (engineered brief, caveman compression, the Phase-2 approval gate, the two mandatory artifacts).

**Severity.** Medium-High. The skill *appears* to work but quietly degrades to "skill-flavoured" rather than faithful execution.

**First observed.** 2026-Jun-16, recurred 2026-Jun-25 across sessions in a remote environment. See `D:/Downloads/Coeus_Plugin_Error.md` for the original report.

---

## Path resolution map (workaround)

When the bug is present, manually resolve every Coeus skill from the `user/` directory:

| Indexed path (broken) | Real path (use this) |
|---|---|
| `plugins/coeus:the-architect/` | `/mnt/skills/user/the-architect/` |
| `plugins/coeus:llm-council/` | `/mnt/skills/user/llm-council/` |
| `plugins/coeus:prompt-master/` | `/mnt/skills/user/prompt-master/` |
| `plugins/coeus:caveman/` | `/mnt/skills/user/caveman-protocol/` ⚠ |
| `plugins/coeus:morpheus/` | `/mnt/skills/user/morpheus/` |
| `plugins/coeus:ep-council/` | `/mnt/skills/user/ep-council/` |

⚠ **Stale folder name.** In pre-v3.0.1 installs, caveman's directory was named `caveman-protocol`. The current repo ships it as `caveman/`. If your install still has `caveman-protocol/`, the install pre-dates v3.0.1 — re-install from the latest `coeus.plugin`.

---

## Run the diagnostic

`scripts/check-install.py` autodetects which case you are in and reports.

```bash
# Check the local repo
python scripts/check-install.py

# Check a specific install directory
python scripts/check-install.py /path/to/coeus/install

# Check a remote skills root (e.g. /mnt/skills)
python scripts/check-install.py /mnt/skills
```

Exit codes:
- **0** — canonical install layout intact
- **1** — canonical layout broken (missing skills, missing manifest, etc.)
- **2** — remote-environment path-mismatch bug detected (apply workaround above)

The diagnostic also catches stale `caveman-protocol/` directories and reports them as a pre-v3.0.1 install marker.

---

## Permanent fixes

Two paths:

1. **Fix the index** (preferred — plugin-side) — the install manifest should map `coeus:<name>` to the actual filesystem path, not to a `plugins/coeus:` namespace that does not exist. This is upstream of the Coeus repo — if you can edit the remote environment's plugin registry, point each entry at `user/<name>/`.

2. **Reinstall the plugin** — `coeus.plugin` built by `scripts/build-plugin.py` (or downloaded from GitHub Releases) installs the canonical layout. If the install was done from a stale source, replacing it with a fresh build resolves both the namespace issue and the `caveman-protocol` legacy name in one shot.

---

## How to confirm you are NOT affected

If you are reading this in a Claude environment that exposes Coeus as `coeus:<name>` slash commands directly (no namespace prefix in path), and `scripts/check-install.py` returns exit 0, you are running the canonical install and the remote-environment bug does not apply.

In doubt: run `ls .claude-plugin/plugin.json` inside what you think is the install dir. If it exists, you are looking at a canonical install. If it does not, you are looking at the remote-environment layout where the index lies — use the workaround above.

---

*See also: `Coeus_LLM_HANDOVER.md` for the broader skill-invocation discipline; `scripts/coeus_full_test.py` for the full-harness conformance test.*
