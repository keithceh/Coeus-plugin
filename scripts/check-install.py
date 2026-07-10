"""Coeus install diagnostic.

Run inside (or pointing at) a suspected Coeus install dir. Reports whether the
install matches the canonical Claude plugin spec, or whether it exhibits the
known remote-environment path-mismatch bug documented in
`docs/Skill-Install-Diagnostics.md` and `D:/Downloads/Coeus_Plugin_Error.md`.

Usage:
    python scripts/check-install.py                  # checks the repo it lives in
    python scripts/check-install.py /path/to/install # checks a different dir
    python scripts/check-install.py /mnt/skills      # checks remote skills root

Exit code: 0 = healthy, 1 = canonical layout broken, 2 = remote path-mismatch detected.
"""
from __future__ import annotations
import json, sys, pathlib

EXPECTED_SKILLS = {
    'ep-council', 'llm-council', 'morpheus', 'the-architect', 'plugin-creator',
    'coeus-router', 'ooxml-repair', 'ooxml-fields', 'docx-inventory',
    'project-lifecycle', 'caveman', 'prompt-master',
}
STALE_DIR_NAMES = {'caveman-protocol'}  # pre-v3.0.1 caveman folder name


def check(target: pathlib.Path) -> int:
    print(f'checking: {target}')

    # Mode 1: looks like a Coeus install root (has .claude-plugin/plugin.json)
    manifest = target / '.claude-plugin/plugin.json'
    if manifest.is_file():
        mf = json.loads(manifest.read_text(encoding='utf-8'))
        print(f'  manifest: {mf.get("name")} v{mf.get("version")}')
        sk_dir = target / 'skills'
        if not sk_dir.is_dir():
            print('  FAIL: skills/ directory missing'); return 1
        found = {p.name for p in sk_dir.iterdir() if p.is_dir() and not p.name.startswith('_')}
        stale = found & STALE_DIR_NAMES
        if stale:
            print(f'  WARN: stale directory names present (should have been renamed): {stale}')
        missing = EXPECTED_SKILLS - found
        extra = found - EXPECTED_SKILLS - STALE_DIR_NAMES
        if missing:
            print(f'  WARN: missing skills: {sorted(missing)}')
        if extra:
            print(f'  INFO: extra skills not in canonical list: {sorted(extra)}')
        if not missing and not stale:
            print('  PASS: canonical install layout intact')
            return 0
        return 1

    # Mode 2: remote-environment skills root (e.g. /mnt/skills)
    plugins_ns = target / 'plugins'
    user_dir = target / 'user'
    if plugins_ns.exists() or user_dir.exists():
        print('  detected: remote skills environment')
        # Path-mismatch bug: index references plugins/coeus:* but files live in user/
        broken_namespace = list(plugins_ns.glob('coeus:*')) if plugins_ns.is_dir() else []
        user_coeus_skills = []
        if user_dir.is_dir():
            for name in EXPECTED_SKILLS | STALE_DIR_NAMES:
                p = user_dir / name
                if p.is_dir():
                    user_coeus_skills.append(name)

        if not broken_namespace and user_coeus_skills:
            print(f'  DETECTED: path-mismatch bug from Coeus_Plugin_Error.md')
            print(f'    index references: plugins/coeus:<name>/  (broken)')
            print(f'    real install at:  user/<name>/')
            print(f'    skills found in user/: {sorted(user_coeus_skills)}')
            stale_in_user = set(user_coeus_skills) & STALE_DIR_NAMES
            if stale_in_user:
                print(f'    STALE NAMES (pre-v3.0.1): {sorted(stale_in_user)}')
                print(f'    workaround: resolve "caveman" -> "user/caveman-protocol/"')
            print(f'  WORKAROUND: read SKILL.md from user/<name>/ directly;')
            print(f'              do NOT trust the indexed plugins/coeus:* path.')
            return 2

    print('  no Coeus install detected here')
    return 1


if __name__ == '__main__':
    target = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 \
        else pathlib.Path(__file__).resolve().parent.parent
    sys.exit(check(target))
