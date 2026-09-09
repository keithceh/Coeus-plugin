# Evergreen Artefacts — Agent-Neutral Publishing

> Publishes any artefact — HTML, Markdown, Office, PDF, or a folder — to the Synology NAS as a new immutable version behind a stable evergreen link that always serves the latest; revert republishes an old version as a new one with an audit record.

**Version:** 1.0.0 (current) | **Triggers:** `/coeus:evergreen-artefacts` · `"publish to NAS"` · `"push this artefact"` · `"share this on the NAS"` · `"new version of [artefact]"` · `"evergreen link"` · `"revert artefact"`

---

## What This Is

Evergreen Artefacts is a Tier-1 `tools`-family skill wrapping one PowerShell script (`publish-artefact.ps1`) and an **agent-neutral** contract file, [`HANDOVER.md`](../skills/evergreen-artefacts/HANDOVER.md), that lives in the published NAS folder itself. Any agent — Claude, ChatGPT, Codex, Cursor, or a human at a terminal — publishes the same way, by running the same script against the same folder layout. The folder layout **is** the API; nothing writes into it directly.

## The One Command

```powershell
& "<skill-base-dir>\publish-artefact.ps1" -Path <file-or-folder> -Name "<artefact name>" -Publisher "claude-code"
```

Re-publishing under the **same `-Name`** creates the next version of the same artefact and the evergreen link updates automatically; a different name creates a new artefact. `-Root`/`-BaseUrl` default to the NAS share and served URL baked into the script — override only if told to.

Revert is the same script, no `-Path`:

```powershell
& "<skill-base-dir>\publish-artefact.ps1" -Name "<artefact name>" -RevertTo <N> -Publisher "claude-code"
```

The script always prints **two URLs**, and both must be reported back to the user:

- **Evergreen link** (`…/artefacts/<slug>/`) — stable forever, always serves the latest version. This is the link to share.
- **Version link** (`…/artefacts/<slug>/vN/`) — an immutable snapshot of that one publish.

## Immutable Versions and Attribution

Every publish lands in its own `vN/` folder, never edited or deleted after the fact. Each version carries a `publish.json` attribution record: the publisher, an ISO timestamp, and a per-file SHA-256 — the integrity record collaborators use to verify a file by comparing its hash, and the tamper-evidence record for the version as a whole.

**Nothing is ever deleted.** To undo a bad publish, `-RevertTo N` republishes the content of version N as a **new** version — its `publish.json` records `revertOf` and who reverted it. The old (bad) version stays exactly where it was; the evergreen link simply moves forward to the new one, and the audit trail shows the whole history honestly rather than erasing the mistake.

## What Each File Type Does at the Evergreen Link

| Type | Behavior |
|---|---|
| `.html` / folder with HTML | Renders in the browser (an `index.html` entry point is used if present, else the first `.html` is promoted) |
| `.md` | Renders via a generated viewer (needs internet for the renderer CDN; falls back to plain text offline) — **rendered unsanitized, so publish only trusted content** |
| `.pptx`, `.docx`, `.xlsx`, `.pdf`, anything else | The evergreen link downloads the latest file; every prior version's copy is kept |

## Layout (Read-Only Facts)

```
artefacts/
  index.html                  gallery of all artefacts (generated)
  HANDOVER.md                 the agent-neutral contract
  <slug>/
    index.html                evergreen redirect -> latest version (generated)
    versions.html             version history (generated)
    v1/ … vN/                 immutable versions; never modified after publish
      publish.json            attribution record: publisher, timestamp, SHA-256 of every file
```

`-Name` is slugged to `[a-z0-9-]` and derived from the filename when omitted. Nothing in this tree is meant to be hand-edited — it is generated and read-only except through the script.

## The Two-Zone Trust Model

- **Working zone** — a Synology Drive team folder for collaborative editing. Collaborators use their own DSM accounts, Drive keeps its own per-file version history with author attribution, and reverts there happen with a click — this is where drafts live before they're ready to publish.
- **Published zone** — the `artefacts/` folder above, served by Web Station over Tailscale. Writes go through `publish-artefact.ps1` only, over SMB with the publisher's own credentials; `-Publisher` plus `publish.json` is the audit record. Read access is anyone on the private network (Tailscale/VPN) — nothing is internet-facing.

## The Agent-Neutral HANDOVER.md Contract

Because `HANDOVER.md` ships inside the published folder itself rather than only inside this plugin, any LLM or human who later opens that NAS share — regardless of what tool invoked it — finds the same one-command contract, the same argument table, and the same "never write here directly" rule without needing Coeus installed. This is the mechanism that keeps the publishing convention agent-neutral: the contract travels with the data, not with the tool that wrote it.

## Rules

1. Versions are immutable — never edit, delete, or re-number a `vN/` folder.
2. To update an artefact, re-publish with the same `-Name`; the evergreen link follows automatically.
3. `publish.json` is the integrity record collaborators use to verify a file's SHA-256.
4. If the script fails because the share path is wrong, ask the user for the correct Web Station folder and URL rather than guessing.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [Keymaker →](Keymaker.md) (offers evergreen publishing, gated, on request only)
- [Atlas →](Atlas.md) (a natural publish target)
- [Coeus Architecture →](Coeus-Architecture.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.0.0** (current) | 2026-Sep-08 | Initial release, folded in from a user-level `nas-artifacts` skill. One PowerShell script plus the agent-neutral `HANDOVER.md` contract: evergreen link, immutable `vN/` versions, `publish.json` attribution + SHA-256 integrity, revert-as-new-version, all file types, and the two-zone trust model. Shipped as part of Coeus v3.24.0. |

Go back to the [Main README](../README.md).
