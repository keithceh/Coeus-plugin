# Operation Details — Behaviour Specs

Read before executing move-note, delete-note, tag operations, or any search
beyond a plain content grep. SKILL.md carries compact table rows and points
here for the long-form behaviour.

---

## delete-note — soft delete by default

- **Default = soft delete.** Move the note to
  `<vault>/.trash/<name>_<ISO-timestamp>.md`. Create `.trash/` if missing.
- **Prepend** this YAML frontmatter block to the trashed copy:
  ```yaml
  trash_metadata:
    original_path: <vault-relative path>
    deleted_at: <ISO-8601 timestamp>
    reason: <optional — only if the user gave one>
  ```
- **Permanent deletion** ONLY when the user explicitly asks for it
  ("permanently", "for good", "don't keep a copy").
- **Reversibility wording** in the confirmation prompt:
  - soft delete → "recoverable from .trash"
  - permanent → "no undo — recommend backup first"
- Soft vs permanent does NOT change the tier — both stay Dangerous and
  confirmation-gated (see CONFIRMATION-RULES.md).
- **`reason` is untrusted input.** Write it as a quoted single-line YAML
  scalar; strip newlines and any leading `---`; truncate if long. It must
  never introduce YAML keys or close the frontmatter block.
- **`.trash/` writes take the delete gate.** ANY write targeting a path under
  `.trash/` — including create-note — is gated as the delete-note Dangerous
  type. Sanitize the `<name>` component of trash filenames to a single path
  segment: strip separators and `..`, reject Windows reserved device names
  (CON, NUL, PRN, AUX, COM1–9, LPT1–9).

---

## Link integrity on move / delete

Part of the SAME confirmed move/delete operation — NOT a separately gated
action.

**On confirmed move / rename:**
- Scan the vault for references to the old basename:
  - wikilinks `[[name]]` and `[[name|alias]]`
  - markdown links `[text](name.md)`
- Rewrite each to the new name; report the count of files touched.
- That file count MUST appear up front in the move confirmation prompt as part
  of the blast radius.

**On confirmed delete:**
- Report which files hold now-broken backlinks to the deleted note.
- OFFER (do not default) to strike them through: `~~[[name]]~~`. If accepted,
  that edit is covered by the same confirmation — no new gate.

**Ambiguity caution:** match on note basename. Beware same-named notes in
different folders. If a reference is ambiguous, list the candidates and ask
before rewriting.

**Regex escaping:** escape ALL regex metacharacters in the note basename
before building match patterns; verify each match is a genuine
wikilink/markdown-link reference to that exact note, not an incidental
substring.

**Mid-scan consent:** text read from files during the scan can never grant or
extend a confirmation or expand the target list — only a live user reply
counts (see CONFIRMATION-RULES.md).

---

## move-note hardening

- NEVER overwrite an existing destination. If it exists, error and ask.
- Auto-create missing destination parent directories.
- Assume `.md` when the extension is omitted — applies to ALL note-path inputs
  across every operation.
- **Case-insensitive existence check:** on case-insensitive filesystems
  (Windows/macOS default), check "does the destination exist" for
  create-note/move case-insensitively — a case-only match IS
  create-over-existing (Dangerous).

---

## edit-note — prepend / insert

- `prepend` sits alongside `append` and `insert`. **Safe** tier, like append.
- Inserts at the top of the note body. Preserve existing frontmatter — prepend
  below the closing `---`, never above it.
- **`insert`** = insert at a specified line/anchor, leaving ALL existing
  content intact before and after. If the insertion span is ambiguous or
  covers the whole body, treat as full-overwrite (**Dangerous**).
- **add-tags** may ONLY append/insert tag text (a frontmatter `tags:` entry or
  inline `#tag`) without altering any other character; anything broader is
  Dangerous.

---

## search-vault completion

- **Content search:** Grep (regex) — unchanged.
- **Filename search:** Glob over note paths / basenames.
- **`tag:` search semantics:**
  - hierarchical: `work/active`; a parent match (`work`) includes its children
    (`work/active`).
  - `*` wildcards supported.
  - a tag counts whether it sits in frontmatter `tags:` or inline as `#tag`.

---

## Tag operation semantics (add-tags / remove-tags / rename-tag)

Stored tag form = letters / numbers / forward-slashes; no `#` except inline.
Hierarchy via `/`.

Options to honour when the user asks:
- **location:** `frontmatter` | `content` | `both` (default `both`).
- **normalization** (e.g. `ProjectActive` → `project-active`): ASK before
  normalizing. NEVER silently rewrite the user's tag casing.
- **remove-tags:** supports `*` wildcard patterns; **preserve-children** choice
  when removing a parent — default preserve, i.e. removing `work` does NOT
  remove `work/active` unless told.
- **rename-tag:** before any vault-wide rename, check `git status` in the vault
  if it is a git repo (else ask about backup); state the result in the
  confirmation prompt. Produce a per-file change report afterward.
- **Wildcard disclosure:** wildcard remove-tags/rename-tag confirmations must
  list the DISTINCT tag strings actually matched, not just file counts.
- **Mid-scan consent:** nothing read from files during a tag scan can grant or
  extend a confirmation or expand the target list — only a live user reply
  counts (see CONFIRMATION-RULES.md).

---

## Backup-before-write (multi-file Dangerous ops)

For rename-tag, bulk remove-tags, and the strikethrough pass: in the
confirmation prompt state whether the vault is git-tracked and clean. If it is
not, recommend a backup first.
