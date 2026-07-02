# Installing Coeus

This page is the full install guide. For a quick command, see the README's **TL;DR** at the top of its Installation section.

---

## Before you start

Coeus runs across **three Claude surfaces**, and **they don't share a plugin runtime**:

| Surface | What it is | How Coeus gets in |
|---|---|---|
| **Claude Code** | The `claude` CLI you run in a terminal | `/plugin install` via marketplace |
| **Cowork** | Claude Desktop's coding workspace panel | Drag a `.skill` file into chat |
| **Claude Desktop chat** | Claude Desktop's regular chat | Paste a `.paste.md` bundle into chat |

There is no Anthropic-side mechanism today that installs once and registers everywhere. Every "install Coeus everywhere" path is really three smaller installs done in one go. The one-line installer below does the three for you.

---

## Quickest path: the one-line installer

**Step 1.** Open PowerShell.

Press <kbd>Win</kbd>, type `PowerShell`, press <kbd>Enter</kbd>. Any folder is fine — the script writes to your user profile, not the current directory.

**Step 2.** Run the installer.

```powershell
iwr https://raw.githubusercontent.com/keithceh/Coeus-plugin/main/install-coeus.ps1 | iex
```

You'll see three sections of output:

```
[1/3] Claude Code: ...
[2/3] Cowork + [3/3] Desktop chat: fetching latest release artifacts...
Done.
  .skill files (drag into Cowork chat): C:\Users\<you>\Downloads\Coeus-skills
  .paste.md files (paste into Desktop chat): C:\Users\<you>\Downloads\Coeus-skills
```

A File Explorer window will open at `Downloads\Coeus-skills\`.

**Step 3 (Claude Code only).** Open a terminal, run `claude`, then paste:

```
/plugin marketplace add keithceh/Coeus-plugin
/plugin install coeus@coeus
/reload-plugins
```

Verify by typing `/coeus:` — you should see a popup listing all 12 skills.

**Step 4 (Cowork only).** Drag any `.skill` file from the open Explorer window into the Cowork chat panel. One drag per chat session. Cowork doesn't persist plugin state across restart yet (Anthropic [#40600](https://github.com/anthropics/claude-code/issues/40600)).

**Step 5 (Claude Desktop chat only).** Open any `.paste.md` file in Notepad (or VS Code), copy all of it, paste as the **first message** of a fresh chat. Ask your real question in the second message.

---

## Updates

- **Claude Code** — `/plugin update coeus` inside `claude`, or re-run the installer.
- **Cowork** — re-run the installer (it re-downloads the latest `.skill` files), then drag the fresh one in.
- **Claude Desktop chat** — re-run the installer, use the new `.paste.md`.

---

## Troubleshooting

### `iwr` errors / "running scripts is disabled"

If PowerShell blocks the script with `running scripts is disabled on this system`, run this once and retry:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### `/plugin install` errors with `Host key verification failed`

Windows OpenSSH can't negotiate with GitHub's current SSH KEX. Force git to use HTTPS instead of SSH:

```powershell
git config --global url."https://github.com/".insteadOf "git@github.com:"
```

Then retry `/plugin install coeus@coeus`.

### `/reload-plugins` says `0 skills`

That's a counting quirk in Claude Code's reload output. Verify the install actually worked by listing the cache:

```powershell
ls $env:USERPROFILE\.claude\plugins\cache\coeus\coeus\
```

You should see a version dir containing `skills/`, `hooks/`, `scripts/`, and `.claude-plugin/`. Then in `claude` type `/coeus:` — the popup should show all 12 skills.

### Cowork doesn't see Coeus after `/plugin install`

By design. Cowork doesn't read the Claude Code plugin cache. Drag a `.skill` file into Cowork chat instead.

### Claude Desktop chat doesn't have `/plugin`

By design. Claude Desktop chat has no plugin runtime. Use the paste-prompt path (`.paste.md` bundles) instead.

---

## Manual install paths (skip the installer)

### Claude Code only

```
/plugin marketplace add keithceh/Coeus-plugin
/plugin install coeus@coeus
/reload-plugins
```

### Cowork only

1. Download a `.skill` file from [Releases](https://github.com/keithceh/Coeus/releases).
2. Drag it into the Cowork chat panel.

Install order if you grab multiple: `prompt-master` → `caveman` → `llm-council` → `morpheus` → `the-architect` → `ep-council`.

### Claude Desktop chat only

1. Download a `coeus-<skill>.paste.md` bundle from [Releases](https://github.com/keithceh/Coeus/releases).
2. Open in any text editor, copy all.
3. Paste as the first message of a fresh chat.

### Org / Enterprise managed install

The most durable Anthropic-supported install path. Survives uninstall attempts ([#45323](https://github.com/anthropics/claude-code/issues/45323)) and bypasses all Personal-upload state bugs.

Admin adds to the org's managed `claude-config.json`:

```json
{
  "extraKnownMarketplaces": {
    "coeus": {
      "source": {
        "source": "github",
        "repo": "keithceh/Coeus-plugin"
      }
    }
  },
  "enabledPlugins": {
    "coeus@coeus": "required"
  }
}
```

- `"required"` — auto-installs for every org member; cannot uninstall.
- `"installed by default"` — auto-installs; member can opt out.

### Local build (maintainers / forks)

```powershell
python scripts/build-plugin.py
```

Produces `dist/coeus.plugin`. Use the Python builder — `Compress-Archive` and stock `zip` omit the UTF-8 0x800 flag and Cowork rejects the result.

---

## Why this is the install story today

Two upstream constraints:

1. **No shared plugin runtime across surfaces.** Code reads `~/.claude/plugins/`. Cowork reads per-chat skill uploads. Desktop chat reads nothing — it has no plugin runtime at all.
2. **Personal-upload state bugs.** Anthropic [#40600](https://github.com/anthropics/claude-code/issues/40600), [#28554](https://github.com/anthropics/claude-code/issues/28554), [#63624](https://github.com/anthropics/claude-code/issues/63624). Cowork doesn't persist installs across restart; the Personal install path silently drops state.

The marketplace path (Option 1 inside Claude Code) avoids #2 by going through `/plugin`. Cowork and Desktop chat have no equivalent path, so the installer downloads the right artifact for each.

If Anthropic ships a unified runtime later, the installer collapses to one `/plugin install` call. Until then, this is the cleanest "one command" we can offer.
