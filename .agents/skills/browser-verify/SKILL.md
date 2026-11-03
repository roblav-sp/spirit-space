---
name: browser-verify
description: >
  Headless-browser verification for the Spirit Space game (Go WASM + Canvas).
  Use when a task requires verifying the game in a real browser, validating
  the bootstrap contract, Law 7 (visible bootstrap errors), or any
  "manual browser check" marked in tasks/ or specs/traceability.md.
---

# Browser verification for Spirit Space

Verifies `index.html` + `main.wasm` in headless Chromium via Playwright.
This is dev-only tooling; it is exempt from Constitution Law 6 (see
`specs/decisions/adr-0005-dev-tooling.md`).

## Prerequisites

- Node.js ≥ 18 (`node -v`)
- Playwright browsers installed once: `npx playwright install chromium`
  (download ~150 MB; skip if `~/.cache/ms-playwright` exists)
- No npm install needed if only `playwright` core is required — the script
  uses `playwright` from the skill's own `node_modules` (bootstrap below).

## Bootstrap (first run only)

```bash
scripts/setup.sh
```

Creates `e2e/node_modules` locally (nothing is added to the repo root; the
game's `go.mod` stays dependency-free — Law 6 untouched).

## Run all checks

```bash
scripts/verify.sh          # from anywhere; paths are resolved internally
```

Exit code 0 = all checks passed. Output is line-based: `PASS <check>` /
`FAIL <check>: <detail>` plus a final summary. Screenshots are written to
`e2e/artifacts/` on failure.

## Checks performed (maps to specs)

| Check | Spec reference |
|---|---|
| `bootstrap: no console errors on load` | bootstrap contract |
| `bootstrap: canvas is 800x600` | bootstrap contract, Law 3 |
| `law7: no error banner when wasm loads correctly` | Law 7, bootstrap contract |
| `law7: broken wasm shows visible error banner` | Law 7 (ADR-0006 context) |
| `gameplay: canvas animates without input` | rendering loop (ADR-0006); FR-003 smoke |
| `input: ArrowRight changes rendering` | FR-001, AC-001 (browser layer) |
| `input: Space fire produces visual change` | FR-002 |
| `input: KeyR while running does not crash or reset` | FR-005.2 |

Limitations: pixel-diff checks prove "rendering responds", not exact
game-over/restart flows — forcing game over requires scripted play-through
(future extension).

## Interpreting results

- A FAIL under "wasm" almost always means `./build.sh` was not run — run it
  and retry before investigating code.
- Pixel-diff checks are heuristic (they verify *something rendered changed*),
  not goldens. Do not weaken them to pass; investigate instead.
- If Chromium cannot install (offline), fall back to: report the blocker and
  mark the traceability entry `TODO` — never claim manual verification
  happened without evidence.

## Extending

Add checks in `e2e/verify.mjs` following the existing `check()` pattern.
Update the table above and `specs/traceability.md` in the same change.
