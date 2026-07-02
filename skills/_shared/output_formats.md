# Shared Output Format Conventions

> Common output structure rules referenced by Coeus skills via the
> `_shared.md` convention from `docs/SKILL_ARCHITECTURE.md`.

---

## Mandatory Artifact Skills

Skills that produce named artifacts (`Final_Plan.md`, `Premortem_Report.md`, `Engineered_Prompt.md`, etc.) must:

1. Emit the artifact as a **fenced markdown block** in the chat reply, AND
2. Save the artifact to the session output directory when running under Cowork / Claude Code, AND
3. Use the **exact filename** documented in the parent SKILL.md.

Artifacts are never compressed (caveman applies to prompts only, never to artifacts).

## Section Headers

- Top-level title: `# <Skill Name> — <Run Type>`
- Phase headers: `## Phase N — <Phase Name>`
- Final section: `## Final Recommendation` (for plans) or `## Risk Register` (for premortems)

## Tables

Use GitHub-flavoured markdown tables for structured comparisons (faction stances, risk registers, decision matrices). Avoid HTML tables — they break in Cowork's markdown renderer.

## Code & Path References

- Inline code: backticks
- File paths: backticks, Windows-form for documentation, POSIX-form for bash blocks
- Cross-skill references: link to the documentation page (`docs/<Skill>.md`), not the SKILL.md file

## Length

A chat-emitted artifact preview may be truncated; the saved file must always be complete.
