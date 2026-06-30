"""Coeus full skill + plugin test harness.

Sections:
  A. Per-skill SKILL.md tests (frontmatter, content hygiene, code syntax)
  B. Cross-skill tests (trigger collisions, dependency resolution, registry)
  C. Hook tests (syntax)
  D. (caller runs plugin build separately, then runs section E)
  E. Plugin bundle tests (extract, conformance, UTF-8 flags, POSIX perms)

Run:
  python coeus_full_test.py            # sections A B C
  python coeus_full_test.py --plugin   # sections A B C E (plugin must exist)
"""
import os, sys, re, json, yaml, pathlib, zipfile, ast, subprocess, shutil

# ROOT resolution order (cross-platform, no CI-side patching needed):
#   1. $COEUS_ROOT env var (explicit override)
#   2. $GITHUB_WORKSPACE (CI default)
#   3. Script's parent dir's parent (scripts/<this>.py -> repo root)
_env_root = os.environ.get('COEUS_ROOT') or os.environ.get('GITHUB_WORKSPACE')
if _env_root:
    ROOT = pathlib.Path(_env_root)
else:
    ROOT = pathlib.Path(__file__).resolve().parent.parent
OWNED = {'ep-council', 'llm-council', 'morpheus', 'the-architect', 'plugin-creator',
         'coeus-router', 'ooxml-repair', 'ooxml-fields', 'docx-inventory', 'project-lifecycle'}
VENDORED = {'caveman', 'prompt-master'}

PASS, FAIL = [], []
def ok(n): PASS.append(n)
def bad(n, r): FAIL.append((n, r))


def section(name): print(f'\n=== {name} ===')


def test_skills():
    section('A. Per-skill tests')
    for skdir in sorted((ROOT / 'skills').iterdir()):
        if not skdir.is_dir() or skdir.name.startswith('_'):
            continue
        skmd = skdir / 'SKILL.md'
        name = skdir.name

        if not skmd.is_file():
            bad(f'{name}: SKILL.md exists', 'missing')
            continue

        raw = skmd.read_bytes()
        if raw[:3] == b'\xef\xbb\xbf':
            bad(f'{name}: no BOM', 'has UTF-8 BOM')
        else:
            ok(f'{name}: no BOM')

        text = raw.decode('utf-8')
        if not text.startswith('---'):
            bad(f'{name}: frontmatter present', 'no leading ---')
            continue

        fm_block = text.split('---', 2)[1]
        try:
            fm = yaml.safe_load(fm_block) or {}
        except Exception as e:
            bad(f'{name}: yaml parses', str(e))
            continue
        ok(f'{name}: yaml parses')

        if fm.get('name') != name:
            bad(f'{name}: frontmatter name matches folder', f"got {fm.get('name')!r}")
        else:
            ok(f'{name}: frontmatter name matches folder')

        # version / argument-hint / Trigger line required on owned skills only.
        # Vendored skills (caveman, prompt-master) inherit upstream frontmatter;
        # we deliberately do not patch them to avoid the upstream-sync wipe trap
        # documented in v3.6.2 CHANGELOG. argument-hint is re-injected by the
        # sync workflow, but version + Trigger line are upstream-owned.
        required_fields = ['description']
        if name in OWNED:
            required_fields.extend(['version', 'argument-hint'])
        for field in required_fields:
            if field not in fm:
                bad(f'{name}: has {field}', 'missing')
            else:
                ok(f'{name}: has {field}')

        desc = fm.get('description', '').strip()
        # Trigger line required on owned skills only.
        if name in OWNED:
            if 'trigger on' not in desc.lower():
                bad(f'{name}: description has Trigger line',
                    'no "Trigger on" anywhere')
            else:
                ok(f'{name}: description has Trigger line')

        # Front-load check (owned skills only)
        if name in OWNED:
            first_line = desc.split('\n', 1)[0].strip()
            if not first_line.lower().startswith('trigger on'):
                bad(f'{name}: description front-loaded', f'starts with: {first_line[:80]!r}')
            else:
                ok(f'{name}: description front-loaded')

        # XML token check
        if re.search(r'<[A-Za-z_/][^>]*>', desc):
            bad(f'{name}: no XML tokens in description',
                'description would be rejected by Desktop validator')
        else:
            ok(f'{name}: no XML tokens in description')

        # description char cap (Cowork validator: 1024)
        if len(desc) > 1024:
            bad(f'{name}: description ≤ 1024 chars',
                f'has {len(desc)} — Cowork validator will reject')
        else:
            ok(f'{name}: description ≤ 1024 chars ({len(desc)})')

        # Emoji scan in frontmatter
        if re.search(r'[\U0001F300-\U0001FAFF☀-➿]', fm_block):
            bad(f'{name}: no emoji in frontmatter', 'present')
        else:
            ok(f'{name}: no emoji in frontmatter')

        # Body code-block syntax check
        body = text.split('---', 2)[2]
        py_blocks = re.findall(r'```python\s*\n(.*?)\n```', body, re.DOTALL)
        for idx, code in enumerate(py_blocks):
            try:
                ast.parse(code)
            except SyntaxError as e:
                bad(f'{name}: python block #{idx+1} parses',
                    f'line {e.lineno}: {e.msg}')
        if py_blocks:
            ok(f'{name}: {len(py_blocks)} python block(s) parse')


def test_cross():
    section('B. Cross-skill tests')

    # Trigger collision audit
    trigs = {}
    deps = {}
    for skdir in sorted((ROOT / 'skills').iterdir()):
        if not skdir.is_dir() or skdir.name.startswith('_'):
            continue
        skmd = skdir / 'SKILL.md'
        if not skmd.is_file():
            continue
        try:
            fm = yaml.safe_load(skmd.read_text(encoding='utf-8').split('---', 2)[1])
        except Exception:
            continue
        desc = fm.get('description', '')
        # quoted phrases longer than 3 chars, not common nouns
        for m in re.findall(r'"([^"]+)"', desc):
            if (len(m) >= 3 and not m.startswith(('SEQ', 'Figure', 'Table', 'Caption',
                                                   'No SEQ', 'No SEQ '))):
                trigs.setdefault(m.lower(), set()).add(skdir.name)
        deps[skdir.name] = fm.get('dependencies') or []

    collisions = [(t, s) for t, s in trigs.items() if len(s) > 1]
    if collisions:
        for t, s in collisions[:5]:
            bad('trigger collisions', f'{t!r} in {sorted(s)}')
    else:
        ok('zero cross-skill trigger collisions')

    # Dependency resolution
    all_skills = {s.name for s in (ROOT / 'skills').iterdir()
                  if s.is_dir() and not s.name.startswith('_')}
    for skill, dlist in deps.items():
        for d in dlist:
            if d not in all_skills:
                bad(f'{skill}: dependency resolves', f'{d!r} not in skills/')
            else:
                ok(f'{skill}: dependency {d} resolves')

    # SKILL_REGISTRY sanity (if present)
    reg = ROOT / 'skills/_shared/SKILL_REGISTRY.md'
    if reg.is_file():
        body = reg.read_text(encoding='utf-8')
        listed = set(re.findall(r'`([a-z0-9_-]+)`', body))
        for s in all_skills:
            if s not in listed:
                bad(f'SKILL_REGISTRY: lists {s}', 'missing')
            else:
                ok(f'SKILL_REGISTRY: lists {s}')


def test_hooks():
    section('C. Hook tests')
    sh = ROOT / 'hooks/cleanup-stale-install.sh'
    ps = ROOT / 'hooks/cleanup-stale-install.ps1'

    # Bash syntax
    if sh.is_file():
        r = subprocess.run(['bash', '-n', str(sh)], capture_output=True, text=True)
        if r.returncode != 0:
            bad('hook .sh: syntax', r.stderr.strip())
        else:
            ok('hook .sh: syntax OK')
        # CRLF check
        if b'\r\n' in sh.read_bytes():
            bad('hook .sh: LF endings', 'has CRLF')
        else:
            ok('hook .sh: LF endings')

    # PS syntax (parse only, no execute). Skip silently on hosts without
    # powershell on PATH (Linux CI runners). pwsh is also acceptable if present.
    if ps.is_file():
        ps_bin = shutil.which('powershell') or shutil.which('pwsh')
        if ps_bin is None:
            ok('hook .ps1: syntax skipped (no powershell on PATH)')
        else:
            ps_check = ('try { [System.Management.Automation.PSParser]::Tokenize('
                        '(Get-Content -Raw "' + str(ps).replace('\\', '/') +
                        '"), [ref]$null) | Out-Null; exit 0 } catch { Write-Error $_; exit 1 }')
            r = subprocess.run([ps_bin, '-NoProfile', '-Command', ps_check],
                               capture_output=True, text=True)
            if r.returncode != 0:
                bad('hook .ps1: syntax', r.stderr.strip()[:200])
            else:
                ok('hook .ps1: syntax OK')

    # Functional Guard 2 test (run hook on repo, must refuse, must not touch .git)
    git_was_present = (ROOT / '.git').is_dir()
    r = subprocess.run(['bash', str(sh)],
                       env={'CLAUDE_PLUGIN_ROOT': str(ROOT), 'PATH': '/usr/bin:/bin'},
                       capture_output=True, text=True, cwd=str(ROOT))
    if 'refusing' not in r.stderr.lower():
        bad('hook .sh Guard 2: refuses on repo', f'stderr: {r.stderr[:200]}')
    else:
        ok('hook .sh Guard 2: refuses on repo')
    if git_was_present and not (ROOT / '.git').is_dir():
        bad('hook .sh: .git preserved', 'DESTROYED .git')
    else:
        ok('hook .sh: .git preserved post-run')


def test_plugin():
    section('E. Plugin bundle tests')
    plug = ROOT / 'dist/coeus.plugin'
    if not plug.is_file():
        bad('plugin file exists', 'dist/coeus.plugin missing')
        return
    ok('plugin file exists')

    with zipfile.ZipFile(plug) as z:
        infos = z.infolist()
        ok(f'plugin opens as zip ({len(infos)} entries)')

        for info in infos:
            n = info.filename
            if '\\' in n:
                bad(f'entry posix path: {n!r}', 'has backslash')
            if not (info.flag_bits & 0x800):
                bad(f'entry UTF-8 flag: {n!r}', 'missing 0x800')
            if info.create_system not in (0, 3):
                bad(f'entry create_system: {n!r}', f'unexpected {info.create_system}')
        ok('all entries POSIX-pathed, UTF-8-flagged, sane create_system')

        # Manifest present and parseable
        try:
            mf = json.loads(z.read('.claude-plugin/plugin.json'))
            ok('manifest parses')
        except Exception as e:
            bad('manifest parses', str(e)); return
        for k in ('name', 'version', 'description', 'author'):
            if k not in mf:
                bad(f'manifest has {k}', 'missing')
            else:
                ok(f'manifest has {k}')

        # Every owned + vendored skill present in bundle
        bundled_skills = {n.split('/')[1] for n in z.namelist()
                          if n.startswith('skills/') and '/SKILL.md' in n}
        for s in OWNED | VENDORED:
            if s not in bundled_skills:
                bad(f'bundle includes {s}', 'missing')
            else:
                ok(f'bundle includes {s}')

        # Re-parse every bundled SKILL.md
        for n in z.namelist():
            if n.startswith('skills/') and n.endswith('/SKILL.md'):
                t = z.read(n).decode('utf-8')
                try:
                    yaml.safe_load(t.split('---', 2)[1])
                except Exception as e:
                    bad(f'bundled {n} parses', str(e))


def report():
    print(f'\n{"="*60}')
    print(f'PASS: {len(PASS)}   FAIL: {len(FAIL)}')
    if FAIL:
        print('\nFAILURES:')
        for n, r in FAIL:
            print(f'  - {n}\n      reason: {r}')
        sys.exit(1)
    print('\nALL TESTS PASS')


if __name__ == '__main__':
    test_skills()
    test_cross()
    test_hooks()
    if '--plugin' in sys.argv:
        test_plugin()
    report()
