#!/usr/bin/env bash
# Run BATS under tests/end-to-end. CI sets BATS_LIBS_ROOT (bats-action); locally we fetch
# bats-support + bats-assert into .cache/bats-e2e-libs/ on first run.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ -z "${BATS_LIBS_ROOT:-}" ]]; then
  LIBROOT="$ROOT/.cache/bats-e2e-libs"
  export BATS_LIBS_ROOT="$LIBROOT"
  mkdir -p "$LIBROOT"
  clone_if_missing() {
    local name="$1"
    local url="$2"
    local dest="$LIBROOT/$name"
    if [[ -f "$dest/load.bash" ]]; then
      return 0
    fi
    echo "e2e: cloning $name (first run needs git + network)…"
    rm -rf "$dest"
    git clone --depth 1 "${url}" "$dest"
  }
  clone_if_missing bats-support https://github.com/bats-core/bats-support.git
  clone_if_missing bats-assert https://github.com/bats-core/bats-assert.git
fi

if [[ $# -eq 0 ]]; then
  set -- --verbose-run tests/end-to-end
fi
exec bats "$@"
