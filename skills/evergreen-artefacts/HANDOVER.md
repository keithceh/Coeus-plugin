# Artefact publishing — agent handover contract

This NAS folder is a static, versioned artefact library. It is published to by
**one script only**; the folder layout is the API. Any agent (Claude, ChatGPT,
Codex, Cursor, a human in a terminal) publishes the same way. Never write into
this folder directly — always go through the script.

## The one command

```powershell
& "<path-to>\publish-artefact.ps1" -Path <file-or-folder> -Name "<artefact name>" -Publisher "<agent-name>"
```

| Argument | Meaning |
| --- | --- |
| `-Path` | The artefact: a single file of any type, or a folder (an `index.html` entry point is used if present, else the first `.html` is promoted). |
| `-Name` | Optional. Display name; derived from the filename when omitted. Slugged to `[a-z0-9-]`. **Same name = same artefact**: re-publishing creates the next version. |
| `-Publisher` | Who published: `claude-code`, `chatgpt`, `codex`, or a person. Recorded in the publish record. |
| `-Root` / `-BaseUrl` | NAS share path and served URL. Defaults are baked into the script; override only if told to. |
| `-RevertTo <N>` | Revert: re-publishes the content of version N as a **new** version (requires `-Name`, no `-Path`). Nothing is deleted; the new version's `publish.json` records `revertOf` and who reverted. Example: `-Name "field notes" -RevertTo 3`. |

The script prints two URLs. **Always report both back to the user:**

- **Evergreen link** `…/artefacts/<slug>/` — stable forever, always shows/downloads the latest version. This is the link to share.
- **Version link** `…/artefacts/<slug>/vN/` — immutable snapshot of this publish.

## What each file type does at the evergreen link

| Type | Behavior |
| --- | --- |
| `.html` / folder with HTML | Renders in the browser. |
| `.md` | Renders in the browser via a generated viewer (needs internet for the renderer CDN; falls back to plain text offline). Rendered unsanitized — publish only trusted content. |
| `.pptx`, `.docx`, `.xlsx`, `.pdf`, anything else | The evergreen link downloads the latest file. Versions keep every prior copy. |

## Layout (read-only facts, do not create these yourself)

```
artefacts/
  index.html                  gallery of all artefacts (generated)
  HANDOVER.md                 this contract
  <slug>/
    index.html                evergreen redirect -> latest version (generated)
    versions.html             version history (generated)
    v1/ … vN/                 immutable versions; never modified after publish
      publish.json            attribution record: publisher, timestamp, SHA-256 of every file
```

## Rules

1. Versions are immutable. Never edit, delete, or re-number a `vN/` folder.
2. To update an artefact, re-publish with the same `-Name`. The evergreen link follows automatically.
3. `publish.json` is the integrity record — collaborators verify a file by comparing its SHA-256 against it.
4. Access model — two zones:
   - **Working zone** (Synology Drive team folder): collaborators edit drafts with their own DSM accounts; Drive keeps per-file version history with author, and reverts happen there with a click.
   - **Published zone** (this folder): write goes through this script only, over SMB with the publisher's own credentials; `-Publisher` plus `publish.json` is the audit record. To undo a bad publish use `-RevertTo` — never delete or edit a `vN/` folder.
   Read = anyone on the private network (Tailscale/VPN). Do not attempt to grant access another way.
