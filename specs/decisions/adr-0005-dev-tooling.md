# ADR-0005 — Dev-only Node/Playwright tooling is exempt from Law 6

**Status:** Accepted

**Context:** Constitution Law 6 forbids external dependencies for the game
("stdlib only; `go.mod` must never gain a `require` block"). Several
verification steps (Law 7 banner, AC-017 banner, input handling) cannot be
tested in Go because they live in the browser layer. Headless browser testing
requires Node + Playwright, i.e. a second toolchain.

**Decision:** Browser verification lives in
`.agents/skills/browser-verify/` as a dev-only skill. Its npm dependencies
(`playwright-core`, Chromium) are installed locally inside the skill's own
`e2e/node_modules` by `scripts/setup.sh` and are **not** part of the shipped
game. The repo root gains no `package.json`; `go.mod` stays dependency-free;
`build.sh` output is unchanged.

**Alternatives considered:**
- Pi MCP server (`@playwright/mcp`) — richer tool integration, but adds a
  persistent config dependency for every session; overkill for one game.
- Manual verification only — unrepeatable and unevidenced; leaves traceability
  TODOs open forever.
- Wasm-dom testing in Go — no mature stdlib-only option exists.

**Consequences:** Browser checks are automated and repeatable
(`scripts/verify.sh`), closing the manual-only traceability entries. Cost:
~150 MB Chromium download once, and a dev-only toolchain that must never leak
into the game build.

**Reconsider when:** the e2e suite grows beyond smoke checks (consider the
MCP server for interactive exploration) or a runtime dependency would be
needed in the game itself (then Law 6 must be amended first).
