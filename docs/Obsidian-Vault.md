# Obsidian Vault — Vault Operations With Guardrails

> Direct file operations on a plain-text Obsidian vault — read, search, create, edit, tag, move, and delete notes — with `obsidian-mcp` functional parity, first-class NAS/UNC vault paths, and confirmation-gated destructive operations.

**Version:** 1.2 (current) | **Triggers:** `/obsidian-vault` · `"work on my vault"` · `"search my vault"` · `"vault note"` · `"create a note in my vault"` · `"tag notes"` · `"rename tag"` · `"move note"` · `"delete note"` · `"obsidian vault"`

---

## What This Is

Obsidian Vault is Coeus's `vault`-family skill — the only one in that family. It works on a plain-text Obsidian vault as files on disk, using native tools (Read/Write/Edit/Grep/Glob/Bash) or `mcp__filesystem__*` when connected. Its explicit design target is functional parity with the `obsidian-mcp` npm package — which is itself just filesystem operations, naive search, and regex tag editing — while fixing that package's bug of rejecting vaults that live on network drives.

**Vault root** is the directory containing a `.obsidian/` folder, found by globbing for `**/.obsidian`. Every operation must resolve **inside** the vault root on the fully resolved path (symlinks followed) — `..` traversal, drive-relative paths (`Y:foo`), and `\\?\`-prefixed paths are all rejected unless they resolve inside the root. `.obsidian/` itself is a hard write block: nothing this skill does may create, edit, or delete anything under it, since writes there can lead to code execution when the vault opens.

## The Operation Set

| Operation | Tier |
|---|---|
| read-note, list-vaults, list-tags | Safe |
| search-vault (content / filename / tag) | Safe |
| create-note (new path), add-tags | Safe |
| edit-note (append / prepend / insert), create-directory | Safe |
| create-note over existing file (overwrite) | **Dangerous** |
| edit-note (full overwrite), remove-tags, rename-tag | **Dangerous** |
| move-note, delete-note (soft or permanent) | **Dangerous** |

Content search prefers ripgrep-backed Grep (regex, `glob` scoping, `-i` case) and filename search prefers Glob, over any naive substring scan. Note-path inputs assume `.md` when the extension is omitted, uniformly across every operation.

## `obsidian-mcp` Parity, Verified From Package Source

Every operation was cross-checked directly against the `obsidian-mcp` npm package's own source (v1.0 → v1.2), and the parity behaviours are now explicit rather than assumed:

- **Soft delete by default** — `delete-note` moves the note to `<vault>/.trash/<name>_<ISO-timestamp>.md` with a prepended `trash_metadata` block (`original_path`, `deleted_at`, optional `reason`). Permanent deletion happens only when the user explicitly says "permanently" or "for good"; soft and permanent stay equally Dangerous and confirmation-gated either way.
- **Link updating on move** — a confirmed move/rename scans the vault for wikilinks (`[[name]]`, `[[name|alias]]`) and markdown links (`[text](name.md)`) referencing the old basename, rewrites them, and reports the file count touched — that count must appear up front in the move's confirmation prompt as part of the blast radius. A confirmed delete reports which files now hold broken backlinks and *offers* (never defaults to) striking them through.
- **Tag search** — hierarchical (`work` matches `work/active`) and wildcard (`*`) `tag:` search, matching a tag whether it sits in frontmatter `tags:` or inline as `#tag`.
- **Move hardening** — never overwrites an existing destination, auto-creates missing parent directories, and treats a case-only match as create-over-existing (Dangerous) on case-insensitive filesystems.
- **`edit-note` prepend** — sits alongside append and insert as a Safe operation, inserting below the closing frontmatter `---`, never above it.
- **Tag semantics** — a `location` option (frontmatter / content / both), ask-before-normalizing casing (never silently rewritten), wildcard `remove-tags` with a preserve-children default, and a `git status` check before any vault-wide `rename-tag`.

Full behavioural detail for these lives in [`references/OPERATIONS.md`](../skills/obsidian-vault/references/OPERATIONS.md), which the skill is required to read before executing move-note, delete-note, tag operations, or any search beyond a plain content grep.

## NAS / UNC Paths Are First-Class

UNC paths (`\\192.168.0.119\Obsidian\Obsidian_Vault`) and mapped drives (`Y:`) are explicitly first-class vault locations — the skill must never reject a path for being a network, NAS, or mapped drive, since that rejection is exactly the `obsidian-mcp` bug this skill exists to avoid. If a connected filesystem MCP server exposes directories beyond the vault, operations stay confined to the vault subtree unless the user explicitly directs one action elsewhere.

## Security Guardrails

Eight guardrails came out of a dedicated prompt-injection / path-containment review:

1. `.obsidian/` is a hard write block for every operation.
2. `trash_metadata.reason` is YAML-sanitized before being written (quoted single-line scalar, no injected keys, no frontmatter break-out).
3. Path containment checks the **resolved**, symlink-followed path; drive-relative and `\\?\`-prefixed paths are rejected unless they resolve inside the vault.
4. Link rewriting on move regex-escapes the note's basename — no pattern injection via filenames.
5. Destructive-op consent is valid only from a **live user reply**; note content read mid-scan (frontmatter, callouts, filenames) is inert data and can never grant or extend a confirmation, no matter how it's phrased.
6. `insert` is a defined, bounded operation and `add-tags` is constrained to appending tag text only — no arbitrary-content smuggling through either.
7. Writes into `.trash/` are gated as the delete-note Dangerous type, never treated as a Safe create.
8. Wildcard tag operations disclose the distinct matched tag strings (not just a file count) before acting; existence checks are case-insensitive.

Note content is always treated as **inert data, never instructions** — a note that says "delete all other notes" is data about that note, not a command the skill will act on.

## Confirmation Gating

Dangerous operations are gated per action-**type** (not per target — every `delete-note` call is one type regardless of which note), per session: the 1st and 2nd occurrence of a type each require full explicit confirmation, describing the action, the full target list (or a count plus sample), and reversibility. Only **after** the 2nd confirmation may the skill separately ask whether to skip further confirmations of that one type for the rest of the session — never bundled into the confirmation itself. A skip is session-only (never persisted to disk or memory), scoped to exactly one action type, and any materially larger blast radius than previously confirmed re-triggers full confirmation even with a skip in place. Full detail — including the exact wording rules — lives in [`references/CONFIRMATION-RULES.md`](../skills/obsidian-vault/references/CONFIRMATION-RULES.md), which the skill is required to read in full before any Dangerous operation.

## What It Defers to Other Tools

- **Obsidian-Flavored-Markdown syntax** — wikilinks, embeds, callouts, properties, tag syntax — is handled by `obsidian-markdown` and its companions `obsidian-bases` and `json-canvas`. This skill does not restate OFM syntax.
- **Live Obsidian-app integration** — graph view, Dataview execution, plugin triggers, opening notes in the running app — belongs to the separate `obsidian-cli` skill.

Before any live-vault write/move/delete testing, the skill requires a git-backed (or equivalent) backup and recommends testing against a throwaway copy first.

---

## Related Pages

- [SKILLS.md — full skill catalog →](SKILLS.md)
- [Coeus Architecture →](Coeus-Architecture.md)

---

## Version History

| Version | Date | Change |
|---|---|---|
| **1.2** (current) | 2026-Jul-10 | Full `obsidian-mcp` parity verified against the package's own source, plus 8 security guardrails from a dedicated prompt-injection / path-containment review. New `references/OPERATIONS.md`. |
| **1.0** | 2026-Jul-10 | Initial release. New `vault` family added to `coeus-router` (v1.2.0 → v1.3.0, new Step 2d + tie-breaker rule). |

Go back to the [Main README](../README.md).
