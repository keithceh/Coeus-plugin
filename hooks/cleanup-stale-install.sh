#!/usr/bin/env bash
# Coeus — clean-install hook
#
# Runs at SessionStart. Removes any file or directory in the plugin install
# root that isn't part of the canonical v3.x layout, so stale files left over
# from older versions (e.g. root-level *.skill baselines, retired workflows)
# are purged on the first session after an in-place upgrade.
#
# Idempotent: writes .coeus-cleaned-<version> marker and exits early on
# subsequent runs of the same version. Removing the marker forces a re-clean.
#
# Safe-by-default: only runs inside a directory that contains
# .claude-plugin/plugin.json (so it cannot accidentally wipe an arbitrary
# cwd if invoked without the plugin env).

set -eu

# CLAUDE_PLUGIN_ROOT is set by the Claude Code plugin runtime. Fall back to
# the script's own directory's parent if it's not present (e.g. manual run).
ROOT="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"

# Guard 1: only operate inside a real Coeus plugin install.
if [ ! -f "${ROOT}/.claude-plugin/plugin.json" ]; then
  echo "[coeus] cleanup-stale-install: not a plugin install (.claude-plugin/plugin.json missing); skipping" >&2
  exit 0
fi

# Guard 2: refuse to run inside a git repo. Install dirs never contain .git;
# source repos do. Caught a real incident in v3.7.x where running the hook
# against the source tree wiped .git, .github, dist, index.html, vercel.json.
if [ -d "${ROOT}/.git" ] || [ -d "${ROOT}/.github" ]; then
  echo "[coeus] cleanup-stale-install: refusing to run inside a git repo (.git or .github present); skipping" >&2
  exit 0
fi

VERSION="$(grep -m1 '"version"' "${ROOT}/.claude-plugin/plugin.json" | sed -E 's/.*"version"[[:space:]]*:[[:space:]]*"([^"]+)".*/\1/')"
MARKER="${ROOT}/.coeus-cleaned-${VERSION}"

if [ -f "${MARKER}" ]; then
  exit 0
fi

# Canonical top-level entries shipped by coeus.plugin v3.4.0+.
# Anything else at the install root is treated as stale and removed.
# Per docs/COEUS_EXTENSIONS.md — if you add a new top-level entry to the
# canonical layout, also add it here or the next session will delete it.
KEEP=(
  ".claude-plugin"
  "skills"
  "hooks"
  "scripts"
  "docs"
  "assets"
  "README.md"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "CLA.md"
  "LICENSE"
  "Coeus_LLM_HANDOVER.md"
  ".gitattributes"
  ".gitignore"
)

removed=0
for entry in "${ROOT}"/* "${ROOT}"/.*; do
  [ -e "${entry}" ] || continue
  base="$(basename "${entry}")"
  case "${base}" in
    "."|".."|"${MARKER##*/}") continue ;;
    # Old version markers ARE removed (only the current-version marker is kept)
    # so the install dir doesn't accumulate one .coeus-cleaned-X.Y.Z per upgrade.
  esac

  keep=0
  for k in "${KEEP[@]}"; do
    if [ "${base}" = "${k}" ]; then
      keep=1
      break
    fi
  done

  if [ "${keep}" = 0 ]; then
    rm -rf -- "${entry}"
    removed=$((removed + 1))
    echo "[coeus] cleanup-stale-install: removed stale '${base}'" >&2
  fi
done

touch "${MARKER}"

if [ "${removed}" -gt 0 ]; then
  echo "[coeus] cleanup-stale-install: ${removed} stale entries removed for v${VERSION}" >&2
fi

# Opt-in available-skills banner. Default OFF -- enable with COEUS_STARTUP_BANNER=1
# in the shell that launches Claude. Plain ASCII, single line, written to stderr
# (same channel as the cleanup messages above; consistent with existing surface
# behaviour). Listed alphabetically, no XML-like tokens, no emoji.
if [ "${COEUS_STARTUP_BANNER:-0}" = "1" ]; then
  if [ -d "${ROOT}/skills" ]; then
    SKILLS_LIST="$(ls -1 "${ROOT}/skills" 2>/dev/null | grep -v '^_' | tr '\n' ',' | sed 's/,$//' | sed 's/,/, /g')"
    echo "[coeus v${VERSION}] available skills: ${SKILLS_LIST}" >&2
  fi
fi

exit 0
