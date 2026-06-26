"""Build a single-message paste-prompt for a Coeus skill.

For surfaces that cannot install Claude plugins (e.g. claude.ai web chat),
this script concatenates a skill's SKILL.md plus every `_shared/*.md` it
references into one Markdown bundle the user pastes into the chat. Loses
auto-fire and slash commands; preserves the protocol.

Usage:
    python scripts/build-skill-paste.py llm-council
    python scripts/build-skill-paste.py the-architect
    python scripts/build-skill-paste.py ep-council

Output:
    dist/coeus-<skill>.paste.md

Resolution rules:
  - Inlines every `[...](../_shared/X.md)` reference found in the SKILL.md,
    recursively (one hop only — _shared files referencing other _shared
    files are followed).
  - Strips the YAML frontmatter (the paste context has no use for triggers
    or argument-hints — users invoke by reading the prelude).
  - Prepends a paste-prelude that tells the model "follow this protocol".
"""
from __future__ import annotations
import re, sys, pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
SHARED_REF = re.compile(r'\[([^\]]+)\]\(\.\./_shared/([a-z0-9_-]+\.md)\)')


def strip_frontmatter(text: str) -> str:
    if not text.startswith('---'):
        return text
    parts = text.split('---', 2)
    return parts[2].lstrip() if len(parts) >= 3 else text


def find_shared_refs(text: str) -> list[str]:
    """Return ordered list of _shared/*.md filenames referenced in text (deduped)."""
    seen = []
    for m in SHARED_REF.finditer(text):
        fname = m.group(2)
        if fname not in seen:
            seen.append(fname)
    return seen


def build_paste(skill: str) -> pathlib.Path:
    sk = REPO / 'skills' / skill / 'SKILL.md'
    if not sk.is_file():
        raise SystemExit(f'skill not found: {sk}')

    body = strip_frontmatter(sk.read_text(encoding='utf-8'))
    shared_files = find_shared_refs(body)

    # One hop: follow shared refs in shared files too.
    deep: list[str] = list(shared_files)
    for s in shared_files:
        shared_text = (REPO / 'skills/_shared' / s).read_text(encoding='utf-8')
        for nested in find_shared_refs(shared_text):
            if nested not in deep:
                deep.append(nested)

    prelude = f'''# Coeus — `{skill}` paste prompt

> **For paste-into-chat use** (claude.ai web chat or any surface without
> plugin support). The Coeus plugin's `{skill}` skill runs natively on
> Claude Code / Cowork / Desktop — install via `/plugin marketplace add
> keithceh/Coeus-plugin` then `/plugin install coeus@coeus`. This file
> exists only for surfaces where plugin install is not available.
>
> **How to use:** paste this entire file into your chat as the first
> message. Then ask your real question in the next message. The model
> will treat the protocol below as load-bearing instructions.

---

You are now operating under the **`{skill}`** protocol from the Coeus
plugin. Follow this protocol for the user's next message. Apply all hard
rules. Produce the artifacts the protocol mandates.

---

'''

    # Body of the skill itself
    out_parts = [prelude, '# SKILL: ' + skill + '\n\n', body, '\n\n']

    # Append every referenced _shared/ file
    for s in deep:
        sf = REPO / 'skills/_shared' / s
        if not sf.is_file():
            out_parts.append(f'<!-- WARNING: shared ref {s} not found -->\n\n')
            continue
        sf_body = strip_frontmatter(sf.read_text(encoding='utf-8'))
        out_parts.append(f'\n---\n\n# SHARED REFERENCE: `_shared/{s}`\n\n')
        out_parts.append(sf_body)
        out_parts.append('\n\n')

    # Footer
    out_parts.append(f'''
---

*Paste-prompt generated from Coeus repo. For the full plugin install
path, see https://github.com/keithceh/Coeus-plugin*
''')

    dist = REPO / 'dist'
    dist.mkdir(exist_ok=True)
    out = dist / f'coeus-{skill}.paste.md'
    out.write_text(''.join(out_parts), encoding='utf-8')
    return out


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python scripts/build-skill-paste.py <skill-name>')
        print('       e.g. llm-council, the-architect, ep-council, morpheus, plugin-creator')
        sys.exit(2)
    skill = sys.argv[1]
    out = build_paste(skill)
    size_kb = out.stat().st_size / 1024
    refs = len(find_shared_refs((REPO / 'skills' / skill / 'SKILL.md').read_text(encoding='utf-8')))
    print(f'wrote {out}  ({size_kb:.1f} KB, {refs} _shared refs inlined)')
