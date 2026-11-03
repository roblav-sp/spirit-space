#!/usr/bin/env bash
# Build the game as WebAssembly and copy the Go JS glue file.
set -euo pipefail
cd "$(dirname "$0")"

GOOS=js GOARCH=wasm go build -o main.wasm ./cmd/game
# Go ≥1.21 ships wasm_exec.js in misc/wasm; fall back to lib/wasm for older layouts.
WASM_EXEC="$(go env GOROOT)/misc/wasm/wasm_exec.js"
[ -f "$WASM_EXEC" ] || WASM_EXEC="$(go env GOROOT)/lib/wasm/wasm_exec.js"
cp "$WASM_EXEC" ./wasm_exec.js
echo "Built main.wasm ($(du -h main.wasm | cut -f1))"
