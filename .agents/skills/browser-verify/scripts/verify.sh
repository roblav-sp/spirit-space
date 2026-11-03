#!/usr/bin/env bash
# Runs the headless browser verification for Spirit Space.
set -euo pipefail
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO="$(cd "$SKILL_DIR/../../.." && pwd)"
E2E="$SKILL_DIR/e2e"

# Build artifacts if missing (Law 7 test needs a valid main.wasm first).
if [ ! -f "$REPO/main.wasm" ]; then
  echo "main.wasm missing — running build.sh" >&2
  (cd "$REPO" && ./build.sh)
fi

# Serve the repo root on a fixed port.
PORT=8151
python3 -m http.server "$PORT" --directory "$REPO" >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill $SERVER_PID 2>/dev/null' EXIT
sleep 1

mkdir -p "$E2E/artifacts"
cd "$E2E"
node verify.mjs "http://localhost:$PORT" "$REPO"
