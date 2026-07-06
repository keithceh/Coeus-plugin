#!/usr/bin/env bash
# Coeus -- reproducible local coeus.plugin build (Bash wrapper).
#
# Delegates to scripts/build-plugin.py, which is the single source of truth
# for the bundle. The Python builder guarantees UTF-8-flagged zip entries
# (0x800) and POSIX permissions, which Claude Cowork's strict upload
# validator requires. The previous `zip -r` path worked on Linux/macOS but
# produced archives that PowerShell users could not reproduce identically,
# so the wrappers now share the same backend.
#
# Run from the repo root:
#   bash scripts/build-plugin.sh

set -eu

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${REPO_ROOT}"

if [ ! -f ".claude-plugin/plugin.json" ]; then
  echo "ERROR: must be run from the Coeus repo root (.claude-plugin/plugin.json not found)" >&2
  exit 1
fi

PY="$(command -v python3 || command -v python || true)"
if [ -z "${PY}" ]; then
  echo "ERROR: python3 not found on PATH -- install Python 3 to build the plugin" >&2
  exit 1
fi

"${PY}" scripts/build-plugin.py
