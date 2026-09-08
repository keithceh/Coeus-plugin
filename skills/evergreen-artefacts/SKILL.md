---
name: evergreen-artefacts
version: 1.0.0
argument-hint: "[file-or-folder to publish] [optional artefact name] | revert <artefact> to <N>"
description: >-
  Trigger on: /coeus:evergreen-artefacts, "publish to NAS", "push this artefact", "share this on the NAS", "new version of [artefact]", "evergreen link", "revert artefact". Publishes any artefact (HTML, Markdown, Office, PDF, or a folder) to the Synology NAS as a new immutable version behind a stable evergreen link that always serves the latest; revert republishes an old version as a new one with an audit record. Agent-neutral via the HANDOVER.md contract.
---

# Evergreen Artefacts — agent-neutral publishing to Synology

Follow the contract in [HANDOVER.md](HANDOVER.md) (this folder). Short form —
run the script from this skill's base directory:

```powershell
& "<skill-base-dir>\publish-artefact.ps1" -Path <file-or-folder> -Name "<artefact name>" -Publisher "claude-code"
```

Revert (nothing is ever deleted — old content is republished as a new version):

```powershell
& "<skill-base-dir>\publish-artefact.ps1" -Name "<artefact name>" -RevertTo <N> -Publisher "claude-code"
```

- Same `-Name` = new version of the same artefact; the evergreen link updates
  automatically. Versions are immutable; each carries a `publish.json` with
  publisher, timestamp, and per-file SHA-256.
- Report both printed URLs back to the user (evergreen first).
- If the script fails because the share path is wrong, ask the user for the
  correct Web Station folder and URL rather than guessing — defaults live at
  the top of the script.
