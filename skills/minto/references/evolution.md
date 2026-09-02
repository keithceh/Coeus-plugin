# Minto Skill — Self-Evolution Protocol

The skill improves from use. Evolution DATA lives outside the repo (an installed
plugin is a marketplace clone that updates clobber); the PROTOCOL lives here.

## The learnings file

Path: `~/.coeus/minto/learnings.md` (Windows: `C:\Users\<user>\.coeus\minto\learnings.md`).
Create it (and parent dirs) on first write. Never store learnings inside the
plugin directory.

Entry format — one dated line each, newest last:

```text
2026-08-28 | TRIGGER-FP | fired on "update the handover" — lifecycle territory; tightened NOT-trigger
2026-08-28 | PREF | board memos: Key Line capped at 4 supports; user merged risk+doability
2026-08-28 | STRUCTURE-ACCEPTED | gate review G2: structural order by gate criteria worked unchanged
2026-08-28 | STRUCTURE-REJECTED | monthly update: user reordered to cost-first; degree order = cost impact
```

Kinds: `TRIGGER-FP` (fired when it shouldn't), `TRIGGER-MISS` (should have fired,
didn't — user invoked manually after writing started), `PREF` (a stated or
demonstrated user preference), `STRUCTURE-ACCEPTED` / `STRUCTURE-REJECTED`
(which pyramids survived contact with the user).

## When to write

- After any run where the user corrects the structure, overrides a trigger
  decision, or states a preference — one line, at the end of the run, silently
  (no ceremony in the conversation).
- Never log document content — patterns only. No client names, no numbers.

## When to read

- At Phase 1 (Frame) of every run: read the file if it exists; apply `PREF` and
  `STRUCTURE-*` entries to the current deliverable type before proposing a
  pyramid.

## Folding learnings back into the skill

When the same lesson appears ≥3 times, or a `TRIGGER-FP` repeats: propose to the
user (one line) folding it into the skill proper — a trigger-rule change, a
playbook amendment, or a doctrine clarification. On approval, this is a normal
Coeus version-bump commit (SKILL.md / playbooks.md edit + CHANGELOG + registry),
never a silent in-place mutation of the installed plugin. The learnings file
keeps its history; folded entries get ` [FOLDED vX.Y.Z]` appended.

Doctrine (doctrine.md) only changes with new PRIMARY evidence — user preference
never rewrites what Minto said; it goes in playbooks.md as a local adaptation.
