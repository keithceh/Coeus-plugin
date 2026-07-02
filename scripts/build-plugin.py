"""Cross-platform Coeus plugin builder.

Produces dist/coeus.plugin (a .zip-format archive) with:
  - forward-slash POSIX paths
  - UTF-8 filename flag (0x800) on every entry  <-- the critical fix for
    Claude Cowork's strict validator, which rejects archives whose paths
    are not flagged UTF-8 (the default PowerShell Compress-Archive output).
  - POSIX permission bits (0644 for files, 0755 for *.sh / *.ps1 / *.py)
  - no MSDOS extra attrs, no Windows-only metadata
  - deterministic timestamp (mtime preserved per file)
  - DEFLATE compression

Run from the repo root:
    python scripts/build-plugin.py
"""

from __future__ import annotations
import json
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Skill-architecture invariants (see docs/SKILL_ARCHITECTURE.md).
# Vendored upstream skills are exempt from the 3,000-token cap because their
# size is upstream-controlled (see skills/_shared/SKILL_REGISTRY.md).
SKILL_TOKEN_CAP = 3000
TOKEN_HEURISTIC = 1.33  # words × this ≈ tokens. Replace with tiktoken in v3.9.
VENDORED_SKILLS = {'caveman', 'prompt-master'}
SHARED_DIR_PREFIX = '_'  # skills/_shared/ and any future _* are not skills
DESCRIPTION_CHAR_CAP = 500  # Cowork SKILL.md description field validator limit (tightened from 1024 in mid-2026)


def check_skills() -> int:
    """Validate skill-architecture invariants. Returns nonzero on hard failure.

    Hard fails: registry parity, token cap (non-vendored), frontmatter name match, router coverage.
    (Router coverage escalated from warning to hard fail in v3.12.0.)
    """
    skills_dir = ROOT / 'skills'
    registry = ROOT / 'skills/_shared/SKILL_REGISTRY.md'
    router = ROOT / 'skills/coeus-router/SKILL.md'

    errors: list[str] = []
    warnings: list[str] = []

    if not registry.exists():
        errors.append(f'registry missing: {registry}')
        print(f'CHECK FAILED: {errors[0]}')
        return 1

    reg_text = registry.read_text(encoding='utf-8')
    rtr_text = router.read_text(encoding='utf-8') if router.exists() else ''

    skill_dirs = sorted(
        d for d in skills_dir.iterdir()
        if d.is_dir() and not d.name.startswith(SHARED_DIR_PREFIX)
    )

    # FM-CI-04 mitigation (Premortem_Report.md): warn if any _* directory
    # contains a SKILL.md. The skip rule treats _* as "convention only, not a
    # skill"; a SKILL.md inside one is almost certainly a misplaced skill.
    for d in skills_dir.iterdir():
        if d.is_dir() and d.name.startswith(SHARED_DIR_PREFIX):
            if (d / 'SKILL.md').exists():
                warnings.append(f'{d.name}: contains SKILL.md but _* prefix says "not a skill" — rename if it is a real skill')

    for d in skill_dirs:
        name = d.name
        sk = d / 'SKILL.md'

        # name match + existence
        if not sk.exists():
            errors.append(f'{name}: SKILL.md missing')
            continue
        body = sk.read_text(encoding='utf-8')
        frontmatter_name = None
        for line in body.splitlines()[:20]:
            if line.startswith('name:'):
                frontmatter_name = line.split(':', 1)[1].strip()
                break
        # Name match: skill folder must equal frontmatter name. Vendored skills
        # ship upstream with their own names (e.g. caveman-protocol) — the sync
        # workflow re-normalises on weekly fetch but the release workflow's
        # fresh upstream swap does not. Exempt vendored from this check so the
        # release build doesn't fail on a frontmatter we don't control.
        if frontmatter_name != name and name not in VENDORED_SKILLS:
            errors.append(f'{name}: frontmatter name={frontmatter_name!r} != dir')

        # registry parity (hard fail)
        if f'`{name}`' not in reg_text:
            errors.append(f'{name}: not in SKILL_REGISTRY.md')

        # token cap (hard fail, vendored exempt)
        words = len(body.split())
        approx_tokens = int(words * TOKEN_HEURISTIC)
        if approx_tokens > SKILL_TOKEN_CAP and name not in VENDORED_SKILLS:
            errors.append(f'{name}: ~{approx_tokens} tokens > cap {SKILL_TOKEN_CAP}')

        # description char cap (hard fail) — Cowork validator limit.
        # Vendored exempt: upstream-owned, see note on name check above.
        if name not in VENDORED_SKILLS:
            try:
                import yaml as _yaml
                _fm = _yaml.safe_load(body.split('---', 2)[1]) or {}
                _desc = _fm.get('description', '') or ''
                if len(_desc) > DESCRIPTION_CHAR_CAP:
                    errors.append(f'{name}: description {len(_desc)} chars > cap {DESCRIPTION_CHAR_CAP}')
            except Exception:
                # YAML parse handled elsewhere; if it fails here just continue
                pass

        # router coverage (HARD FAIL as of v3.12.0; coeus-router itself excluded).
        # Any new skill must be added to skills/coeus-router/SKILL.md — either as
        # `<name>` in a routing row or as a /coeus:<name> reference. Otherwise
        # the router can't route to it.
        if name != 'coeus-router' and rtr_text:
            if f'`{name}`' not in rtr_text and f'/coeus:{name}' not in rtr_text:
                errors.append(f'{name}: not in coeus-router routing table (add a row to skills/coeus-router/SKILL.md)')

    if warnings:
        print('CHECK WARNINGS (will become errors in v3.9):')
        for w in warnings:
            print(f'  - {w}')
    if errors:
        print('CHECK FAILED:')
        for e in errors:
            print(f'  - {e}')
        return 1
    print(f'CHECK PASS: {len(skill_dirs)} skills, all invariants OK '
          f'({len(warnings)} warning{"s" if len(warnings) != 1 else ""})')
    return 0


# Canonical bundle contents. Order matters only for human-readable listings.
INCLUDE_DIRS = ['.claude-plugin', 'skills', 'hooks', 'scripts', 'docs']
INCLUDE_FILES = [
    'README.md',
    'CHANGELOG.md',
    'Coeus_LLM_HANDOVER.md',
    'CONTRIBUTING.md',
    'CLA.md',
    'LICENSE',
]
# Exclude these even when inside an included dir.
EXCLUDE_NAMES = {'__pycache__', '.DS_Store', 'Thumbs.db'}
EXCLUDE_PREFIX = ('_inspect_zip',)  # internal helpers
EXECUTABLE_SUFFIXES = {'.sh', '.ps1', '.py'}


def is_excluded(p: Path) -> bool:
    if p.name in EXCLUDE_NAMES:
        return True
    if p.name.startswith(EXCLUDE_PREFIX):
        return True
    return False


def iter_files() -> list[Path]:
    files: list[Path] = []
    for d in INCLUDE_DIRS:
        base = ROOT / d
        if not base.exists():
            continue
        for f in sorted(base.rglob('*')):
            if f.is_file() and not is_excluded(f) and not any(is_excluded(p) for p in f.parents):
                files.append(f)
    for name in INCLUDE_FILES:
        f = ROOT / name
        if f.is_file():
            files.append(f)
    return files


class Utf8ZipInfo(zipfile.ZipInfo):
    """Force the 0x800 UTF-8 filename flag on every entry.

    CPython's zipfile._open_to_write() resets flag_bits to 0 before writing the
    local header, then calls _encodeFilenameFlags() to compute the final flags.
    For ASCII filenames the default implementation returns the bare flag_bits
    (0) -- which is exactly what Claude Cowork rejects as "invalid characters".
    Overriding _encodeFilenameFlags to encode as UTF-8 and always OR in 0x800
    is the only reliable way to keep the flag through writestr().
    """

    def _encodeFilenameFlags(self):  # type: ignore[override]
        return self.filename.encode('utf-8'), self.flag_bits | 0x800


def make_zipinfo(rel_posix: str, src: Path) -> zipfile.ZipInfo:
    st = src.stat()
    import time
    t = time.localtime(st.st_mtime)
    zinfo = Utf8ZipInfo(filename=rel_posix, date_time=t[:6])
    zinfo.compress_type = zipfile.ZIP_DEFLATED
    # POSIX permissions in external_attr (upper 16 bits) + "regular file" (0o100000).
    if src.suffix.lower() in EXECUTABLE_SUFFIXES:
        mode = 0o100755
    else:
        mode = 0o100644
    zinfo.external_attr = mode << 16
    # Mark host system as UNIX (3) so readers honour the POSIX perms.
    zinfo.create_system = 3
    return zinfo


def build() -> Path:
    manifest = json.loads((ROOT / '.claude-plugin/plugin.json').read_text(encoding='utf-8'))
    name = manifest['name']
    version = manifest['version']
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    out = dist / f'{name}.plugin'
    if out.exists():
        out.unlink()

    files = iter_files()
    print(f'Building {name}.plugin v{version} -- {len(files)} files')

    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for f in files:
            rel = f.relative_to(ROOT).as_posix()  # forward slashes always
            zinfo = make_zipinfo(rel, f)
            with f.open('rb') as fp:
                z.writestr(zinfo, fp.read())

    size_kb = out.stat().st_size / 1024
    print(f'  -> {out}  ({size_kb:.1f} KB, v{version})')
    return out


def verify(plugin: Path) -> bool:
    """Self-check the produced zip against the strict ruleset."""
    import re
    safe = re.compile(r'^[A-Za-z0-9._/\-]+$')
    issues: list[str] = []
    with zipfile.ZipFile(plugin) as z:
        for info in z.infolist():
            n = info.filename
            if '\\' in n:
                issues.append(f'backslash in {n!r}')
            if not safe.match(n):
                issues.append(f'non-safe char in {n!r}')
            if '..' in n.split('/'):
                issues.append(f'path traversal: {n!r}')
            if not (info.flag_bits & 0x800):
                issues.append(f'missing UTF-8 flag on {n!r}')
            if info.create_system not in (0, 3):
                issues.append(f'unexpected create_system={info.create_system} on {n!r}')
    if issues:
        print('VERIFY FAILED:')
        for i in issues[:20]:
            print(' ', i)
        return False
    print('VERIFY PASS: all entries POSIX/UTF-8-flagged/safe-named')
    return True


if __name__ == '__main__':
    check_only = '--check-only' in sys.argv
    rc = check_skills()
    if rc != 0:
        sys.exit(rc)
    if check_only:
        sys.exit(0)
    out = build()
    if not verify(out):
        sys.exit(1)
    print(f'\nInstall: Claude Desktop / Cowork -> Settings -> Capabilities -> Customize -> Add Plugin -> {out}')
