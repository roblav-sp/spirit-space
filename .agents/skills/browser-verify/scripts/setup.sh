#!/usr/bin/env bash
# One-time setup: install playwright core into the skill's e2e dir.
set -euo pipefail
cd "$(dirname "$0")/../e2e"
[ -d node_modules/playwright ] && { echo "already installed"; exit 0; }
npm init -y >/dev/null 2>&1 || true
npm i --no-fund --no-audit playwright-core
npx playwright install chromium
echo "setup complete"
